# To run this script, a file with predictions of SQL queries must be provided in the same format as the labels file.
# The script executes each predicted SQL query against a database constructed from the provided schema and data,
# and compares the results to the expected results from the labels file.
#
# Reported metrics:
#   - Exact accuracy:           fraction of queries whose result multiset matches exactly (original metric)
#   - Partial score (row F1):   per-query F1 over the result rows, so partial hits earn partial credit
#   - Weighted variants:        both metrics weighted by question length (word count), so longer questions count more
#   - Breakdown by length:      scores per question-length tercile (short / medium / long)
#
# Labels without a matching prediction, and predictions without a matching label, are skipped (and counted).

import csv
import json
import re
import sqlite3
from collections import Counter, defaultdict, deque
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent
LABELS_PATH = DATA_DIR / "restaurants_dataset.csv"
PREDICTIONS_PATH = DATA_DIR / "restaurants_dataset_predictions.csv"
SCHEMA_PATH = DATA_DIR / "restaurants-schema.csv"
DATABASE_PATH = DATA_DIR / "restaurants-db.txt"

def sqlite_type(schema_type):
    normalized_type = schema_type.strip().lower()
    if normalized_type.startswith("int"):
        return "INTEGER"
    if normalized_type.startswith("decimal") or normalized_type.startswith("float"):
        return "REAL"
    return "TEXT"


def load_database():
    tables = {}
    with SCHEMA_PATH.open(encoding="utf-8", newline="") as schema_file:
        for table, field, primary_key, _foreign_key, column_type in csv.reader(
            schema_file, skipinitialspace=True
        ):
            table = table.strip()
            field = field.strip()
            if table == "-":
                continue
            tables.setdefault(table, []).append(
                (field, sqlite_type(column_type), primary_key.strip().lower() == "y")
            )

    connection = sqlite3.connect(":memory:")
    for table, columns in tables.items():
        definitions = []
        for field, column_type, primary_key in columns:
            definition = f'"{field}" {column_type}'
            if primary_key:
                definition += " PRIMARY KEY"
            definitions.append(definition)
        connection.execute(f'CREATE TABLE "{table}" ({", ".join(definitions)})')

    with DATABASE_PATH.open(encoding="utf-8") as database_file:
        for line_number, line in enumerate(database_file, start=1):
            match = re.fullmatch(r"([A-Z_]+)\((.*)\)", line.rstrip("\r\n"))
            if match is None:
                raise ValueError(f"Invalid database record on line {line_number}")

            table, values_text = match.groups()
            if table not in tables:
                raise ValueError(f"Unknown table {table!r} on line {line_number}")

            values = next(csv.reader([values_text], skipinitialspace=True))
            columns = tables[table]
            if len(values) != len(columns):
                raise ValueError(
                    f"Expected {len(columns)} values for {table} on line "
                    f"{line_number}, got {len(values)}"
                )

            converted_values = []
            for value, (_field, column_type, _primary_key) in zip(values, columns):
                if column_type == "INTEGER":
                    converted_values.append(int(value))
                elif column_type == "REAL":
                    converted_values.append(float(value))
                else:
                    converted_values.append(value)

            placeholders = ", ".join("?" for _ in columns)
            connection.execute(
                f'INSERT INTO "{table}" VALUES ({placeholders})', converted_values
            )

    return connection


def row_multiset(rows):
    return Counter(tuple(row) for row in rows)


def partial_score(predicted_rows, expected_rows):
    """Row-level F1 between predicted and expected result multisets (1.0 == exact match)."""
    predicted = row_multiset(predicted_rows)
    expected = row_multiset(expected_rows)
    if not predicted and not expected:
        return 1.0
    overlap = sum((predicted & expected).values())
    if overlap == 0:
        return 0.0
    precision = overlap / sum(predicted.values())
    recall = overlap / sum(expected.values())
    return 2 * precision * recall / (precision + recall)


def question_weight(question):
    """Weight of a query = number of words in its question (longer question -> higher reward)."""
    return max(1, len(question.split()))


def weighted_mean(values, weights):
    total_weight = sum(weights)
    return sum(v * w for v, w in zip(values, weights)) / total_weight


def main():
    csv.field_size_limit(1_000_000_000)
    labels_by_question = defaultdict(deque)
    with LABELS_PATH.open(encoding="utf-8", newline="") as source:
        for line_number, row in enumerate(csv.DictReader(source), start=2):
            try:
                result = json.loads(row["result"])
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON label result on line {line_number} "
                    f"of {LABELS_PATH}"
                ) from error
            if not isinstance(result, list):
                raise ValueError(
                    f"Expected a JSON array label result on line {line_number} "
                    f"of {LABELS_PATH}"
                )
            labels_by_question[row["question"]].append(result)

    connection = load_database()
    exact_scores, partial_scores, weights = [], [], []
    execution_errors = 0
    skipped_predictions = 0
    try:
        with PREDICTIONS_PATH.open(encoding="utf-8", newline="") as source:
            for line_number, row in enumerate(csv.DictReader(source), start=2):
                question = row["question"]
                if not labels_by_question[question]:
                    skipped_predictions += 1
                    continue

                expected_rows = labels_by_question[question].popleft()
                weight = question_weight(question)
                try:
                    predicted_rows = connection.execute(
                        row["predicted_sql"]
                    ).fetchall()
                except sqlite3.Error:
                    # A broken prediction is a wrong prediction, not a reason to abort the whole run.
                    execution_errors += 1
                    exact_scores.append(0.0)
                    partial_scores.append(0.0)
                    weights.append(weight)
                    continue

                exact_scores.append(
                    1.0 if row_multiset(predicted_rows) == row_multiset(expected_rows) else 0.0
                )
                partial_scores.append(partial_score(predicted_rows, expected_rows))
                weights.append(weight)

        skipped_labels = sum(len(results) for results in labels_by_question.values())
    finally:
        connection.close()

    total = len(exact_scores)
    if total == 0:
        raise ValueError(f"No predictions matched any label in {PREDICTIONS_PATH}")

    correct = int(sum(exact_scores))
    unit = [1.0] * total

    print(f"Exact accuracy:              {weighted_mean(exact_scores, unit):.4f}  ({correct}/{total})")
    print(f"Partial score (row F1):      {weighted_mean(partial_scores, unit):.4f}")
    print(f"Weighted exact accuracy:     {weighted_mean(exact_scores, weights):.4f}")
    print(f"Weighted partial score:      {weighted_mean(partial_scores, weights):.4f}")
    print(f"Execution errors:            {execution_errors}/{total}")
    print(f"Skipped labels (no prediction):  {skipped_labels}")
    print(f"Skipped predictions (no label):  {skipped_predictions}")

    # Breakdown by question-length tercile.
    order = sorted(range(total), key=lambda i: weights[i])
    third = max(1, total // 3)
    buckets = {
        "short": order[:third],
        "medium": order[third : 2 * third],
        "long": order[2 * third :],
    }
    print()
    print(f"{'Length':<10} {'n':>5} {'Exact':>8} {'Partial':>8}")
    for name, indices in buckets.items():
        if not indices:
            continue
        exact = sum(exact_scores[i] for i in indices) / len(indices)
        partial = sum(partial_scores[i] for i in indices) / len(indices)
        print(f"{name:<10} {len(indices):>5} {exact:>8.4f} {partial:>8.4f}")


if __name__ == "__main__":
    main()

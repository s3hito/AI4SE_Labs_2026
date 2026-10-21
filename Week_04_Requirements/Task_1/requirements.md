# Technical Requirements

Below are the technical requirements selected for implementation.

## Current inventory and category breakdown reports
ID: 1
Priority: High

Provide current, at-a-glance inventory counts broken down by customizable categories (examples: total items, holds, adult fiction, board books, or other categories the library defines). Counts must be able to include items in all relevant statuses (checked in, checked out, on hold) and be reportable at location/granularity (per branch) with the ability to report the number of holds per category.

Sources:
- conversations\conv_pines014_material_volume.eml

---

## Historical volume tracking and acquisition date
ID: 2
Priority: Mid

Track and report collection volume over time to support historical comparisons (e.g., acquisitions, on‑shelf items, items out in circulation). Item acquisition date must be recorded so changes in volume can be reported over specific time periods (quarterly, seasonal, custom ranges).

Sources:
- conversations\conv_pines014_material_volume.eml

---

## System capacity overview dashboard (aggregate and drill-down)
ID: 3
Priority: High

Provide a capacity/usage dashboard showing high-level summary metrics for all branches with the ability to drill down into individual branches. The interface must support aggregation from the centralized database, filtering/grouping (by region, system, branch type), sorting (by capacity metrics and other criteria), and show trend data (growing/shrinking) over time. Export to CSV should be available. Capacity metrics should be clearly defined (e.g., number of items vs. shelf space, configured limits vs. physical items, circulation volume vs. processing capacity), color-coded status indicators (green/yellow/red) may be used, and the dashboard must perform efficiently and scale to large numbers of locations (e.g., hundreds of branches) with features such as grouping or region filtering to keep overviews usable.

Sources:
- conversations\conv_pines015_capacity_interface.eml

---

## Shelf‑space and genre/format utilization and comparison reports
ID: 4
Priority: Low

Generate reports that, for each genre and format, compare: percentage of total circulations, percentage of the collection, and the percentage of total shelf space (when shelf space is estimated). The system must count items by genre/format, sum checkouts by genre/format, and estimate shelf space (using item dimensions or using item counts as a proxy). Reports must be available at library and system levels, support multi‑level breakdowns and side‑by‑side comparisons of libraries to detect outliers, and include filtering by library/system and by date range (quarterly, seasonal, custom). Provide aggregation and outlier identification features to highlight unusual discrepancies.

Sources:
- conversations\conv_pines016_shelf_space.eml

---

## Batch transfer utility for moving items between branches
ID: 5
Priority: High

Provide a transfer utility to move batches of items between branches that includes: a query builder to identify candidate materials, ability to save/share queries for reuse, manual selection of items from query results, preview of transfers before execution, and generation of printable pull/transit labels (with barcodes). The utility must perform bulk updates of item location fields (and related copy/volume records as needed), generate pull lists, allow undo/preview and provide permission controls (restricting operations to authorized roles), maintain a transfer history/audit log, support auto‑reversion of transfers (time‑based or event‑based criteria such as status change or checkout activity), notify staff of transfer delays or issues, and support temporary transfers for events/programs with automatic revert.

Sources:
- conversations\conv_pines018_item_transfer.eml

---

## Missing/damaged and in‑transit item reporting
ID: 6
Priority: High

Provide separate reports for missing/damaged items and for items in transit. Missing/damaged reports (e.g., monthly per branch) must list affected items and include condition notes (e.g., 'water damage', 'vandalism') to support accountability and process improvement. The in‑transit report must identify items that have been in transit longer than a configurable threshold (default 7 days), merge transit‑to and transit‑from records into a single view, allow configurable date ranges, and be sortable (e.g., by due date) so staff can prioritize oldest items. Items should be identified as in‑transit by date fields (e.g., null arrival with departure older than X days). Ensure separate handling/logging of missing/damaged vs in‑transit workflows and verify technical feasibility.

Sources:
- conversations\conv_pines019_020_missing_intransit.eml

---

## Item purging, batch status changes, last‑copy protection and safe deletion utilities
ID: 7
Priority: Mid

Provide utilities and reports to identify and manage candidate item records for purging based on customizable criteria (status, time in status, time since last circulation, damaged, last‑copy status). The system must: allow combining multiple criteria with logical AND/OR, present read‑only candidate reports, support batch status conversions, provide last‑copy reports at library and system levels to avoid deleting sole copies, permit deleting volume and associated copy entries and records with no items, include safety measures (read‑only candidate lists, separate confirmation step), maintain an audit trail for purges, and optionally schedule/automate purging runs (e.g., yearly).

Sources:
- conversations\conv_pines021_item_purging.eml

---

## Deletion tracking, audit logging and reporting
ID: 8
Priority: Top

Track deletions (and denied deletion attempts) of records (item, patron, bibliographic, etc.) with a full audit trail: store record type and record ID, who deleted it, when (timestamp), user location, and optional reason or prior status. Implement automatic logging (e.g., database triggers writing to an audit table) with required fields (record_type, record_id, deleted_by, deleted_at, location), provide a reporting interface to query/aggregate logs (by date range, user, record type, location), produce administrative reports (totals by period, by type, by location, top deleting users), and ensure deletion tracking supports compliance with data retention policies and accountability/troubleshooting.

Sources:
- conversations\conv_pines022_deletions.eml

---

## Inactive‑patron/outreach reporting (configurable inactivity and export)
ID: 10
Priority: Mid

Provide an inactivity/outreach report that lists patrons with no circulation or electronic activity within a configurable inactivity period (X days; e.g., 30, 90, 180, 365, or any number of days). Reports must be configurable to multiple scope levels (System, Home Library, County, etc.), include electronic activity (OPAC login, online hold placement, online renewals, digital resource access), include current mailing addresses for outreach, identify inactive patrons who owe fines separately, support exclusion of specific patron types (do not disturb, VIP, staff, opted‑out), be exportable (CSV) for outreach systems, and be optimized for large databases (background processing, caching).

Sources:
- conversations\conv_pines024_inactive_patrons.eml

---

## Authentication, login options and role‑based access control
ID: 13
Priority: Top

Support multiple staff authentication methods (card‑swipe/streamlined login and traditional username/password) concurrently, with streamlined login optional and never required. Even with card swipe, the system must identify which individual staff member is logged in for auditing. Implement role‑based access control via security groups and roles (predefined roles such as front desk staff, department heads, administrators), support access assignment for individuals, workgroups and arbitrary staff groups, make role/permission administration easy (change by role assignment rather than individual permission edits), discourage password sharing and ensure terminals are not left logged in, and accommodate varying infrastructure (fallback options where hardware may be unavailable).

Sources:
- email_staff_login.eml

---

# Blacklist

Below are blacklisted requirements and the reasons they were discarded.

## Missing/Damaged and In-Transit Item Reporting
ID: 5
Reason: The requirement includes a vague/duplicative statement: it asks to "confirm overall feasibility/technical capability" for these reports, which is nonsensical in a requirements list (feasibility confirmation is not a functional requirement). The actual functional parts (missing/damaged and in-transit criteria, thresholds, configurability, sorting, merging, grouping) are already clear and implementable, so only the feasibility-verification clause is effectively unsupported.
Conflicts with: 5

## Missing/Damaged and In-Transit Items Reporting
ID: 5
Reason: Contradiction/ambiguity with scope and feasibility: requirement 7 mandates deletion auditing via database triggers and a separate audit table, but requirement 5 does not define any relationship between in-transit detection and deletion or audit/compliance constraints. Additionally, requirement 5 says “ensure the reports are technically feasible to generate” while relying on “null arrival with departure older than X days” and “merging transit-to and transit-from records,” which is underspecified (which tables/fields, whether departure/arrival are reliably null/filled). This makes it potentially non-implementable as stated. Kept requirements 1/2/6/7 which are more concretely implementable and do not require merging underspecified transit schemas.
Conflicts with: 7

## Patron demographic reporting, filtering and grouping
ID: 9
Reason: Potential nonsensical requirement: #9 requires dynamic age computation from birth_date for grouping and also requires configurable age brackets, null-handling with AND/OR logic for demographic filters. While implementable, it becomes nonsensical without clarifying timezone/reference date for 'age' (e.g., as-of today vs as-of report end date). Because #10 and #11 already depend on similar time-based activity windows, the absence of an 'as-of' date definition makes the grouping ambiguous/unimplementable in a consistent way across the system. Discarding #9 avoids under-specified 'age' semantics.
Conflicts with: 10

## Financial and value reporting (patron accounts, payments, item value)
ID: 11
Reason: Conflicts with/overlaps ambiguity regarding data retention and privacy/compliance constraints: #11 mandates retaining financial/accounting records for 7 years and maintaining a detailed payment ledger for reconciliation, while #12 introduces a 'transaction archive' that 'protects patron privacy' under 'State Law'. Without explicit reconciliation, this can contradict whether detailed transaction data for accounting (e.g., ledger linkages) is retained vs. archived/redacted. Since #11 specifies explicit retention and ledger traceability requirements, keep #11 and discard #12’s privacy-archive portion to prevent conflict.
Conflicts with: 12

## Query tool, report templates, permissions, queuing, board reports and transaction archive
ID: 12
Reason: Conflicts with/weakens requirement 8’s deletion tracking scope and audit requirements: requirement 12 adds a privacy-focused 'transaction archive' with compliance constraints, while requirement 8 requires full deletion audit logging (including denied deletion attempts) with required fields and compliance/accountability. The more specific, auditable deletion-tracking mandate in #8 should prevail over the less specific/possibly privacy-restricting 'transaction archive' described in #12. Discarding #12 here avoids an implementation ambiguity where the archive could contradict 'full audit trail' expectations.
Conflicts with: 8, 11

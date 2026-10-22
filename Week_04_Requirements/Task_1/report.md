Current pipeline: load_docs → extractor → dedup → conflict_resolver → priority → id_assigner → reviewer → (retry → extractor | done → render_doc)

load_docs (deterministic) - Walks the input directory recursively and loads every file

extractor (LLM, gpt-4.1-nano) - Runs once per document and extracts information

dedup (LLM, gpt-5-mini) - Receives one numbered list of all raw requirements and removes duplicates

conflict_resolver (LLM, gpt-5.4-nano) - Looks for requirements that contradict each other.

priority (LLM, gpt-5-mini) - Assigns a priority to all requirements in one batch call

id_assigner (deterministic) - Assigns sequential identifiers

reviewer (LLM, gpt-4o-mini) - checks completeness

render_doc (deterministic) - Writes the final single .md document

With this in mind it's fair to say that with the amount of time that has been spent on this 'lab' my disappointment is immesurable and my day is ruined.
# Research and Synthesis Protocol

Use this protocol for new research, catalog updates, and node-focused expansion.

## 1. Frame the question

Record the topic, technical boundary, date range, languages, source types, known terminology, and any seed papers, patents, authors, organizations, or algorithms. Preserve the user's exclusions. If the request is open ended, choose a defensible scope and state it before searching.

Do not assume the user's example vocabulary is complete. Build a small synonym table covering abbreviations, older terms, spelling variants, related tasks, inputs, outputs, and algorithm families.

## 2. Search papers and patents separately

Use available scholarly, patent, web, and local-document tools. Prefer primary records and full text. Search papers and patents with distinct query families because their language and metadata differ.

For each query, append a record to `search-log.json` with:

- query text and filters;
- search service or collection;
- execution date;
- whether it is a seed, synonym, citation, author, organization, classification, or adjacent-problem expansion;
- result count inspected and source IDs retained.

Do not claim exhaustive coverage unless the search actually supports it.

## 3. Expand in bounded rings

Default to one expansion ring. Add another ring only when the preceding ring reveals a new method family, workflow structure, terminology branch, or patent classification.

Expansion options:

- backward references and forward citations;
- related work and similar-document links;
- recurring authors, research groups, inventors, and assignees;
- algorithm names and aliases found in retained sources;
- neighboring workflow steps, inputs, and outputs;
- patent CPC/IPC classes, cited patents, citing patents, and patent families.

Stop when a complete ring yields no new normalized node, workflow structure, or algorithm family; when additions are predominantly duplicates; or when the agreed result, date, time, or ring limit is reached. Log the stopping reason.

## 4. Deduplicate before synthesis

For papers, prioritize DOI, then stable repository ID, then normalized title, year, and first author. Link preprint and published versions instead of counting both independently.

For patents, group family members. Preserve jurisdiction-specific publication numbers but designate one representative source for workflow counts. Do not interpret legal status without a dated authoritative record.

## 5. Extract evidence atomically

Extract evidence at the level of a workflow step or algorithm claim, not only at the document level. Each mapping should capture:

- normalized node;
- what the source contributes at that node;
- algorithm or mechanism, when stated;
- original author term, when useful for audit;
- section, page, figure, table, paragraph, or patent claim locator;
- access level and mapping confidence;
- whether the statement is reported, inferred, or unresolved.

Keep quotations short. Prefer precise paraphrase with a locator.

## 6. Build the normalized node vocabulary

Start with concepts supported by the retained evidence. Reuse an existing node when input, operation, and output semantics match closely enough for comparison. Similar names alone are insufficient.

Use domain-neutral labels when they remain precise. Preserve important domain distinctions instead of collapsing them into vague verbs such as "process" or "optimize".

If a source contains an unmatched step, create a node with `scope: "paper-specific"`, connect it to the closest surrounding normalized nodes, and explain the distinction. A later update may recommend promotion to `scope: "common"`, but must not perform that promotion when it would invalidate user classification or annotations without reporting the change.

## 7. Form multiple workflows

Cluster sources by ordered node sequence, input/output semantics, optimization strategy, and constraint-handling pattern. Do not cluster only by shared keywords.

Create:

- a `common` workflow when multiple independent sources support a coherent normalized sequence;
- a `paper-specific` workflow when a source presents a coherent route that does not fit existing common workflows without distortion.

A workflow can share nodes with other workflows. A paper can support more than one workflow when different parts of the paper genuinely do so. Record coverage and confidence rather than declaring one workflow universally correct.

## 8. Verify and challenge the synthesis

Before delivery, check:

- every referenced source ID exists;
- every algorithm claim has evidence;
- common workflows have more than a single-source rationale, or are explicitly marked provisional;
- paper-specific nodes are not mislabeled as common;
- conflicting orders or incompatible assumptions remain visible;
- access limitations and inferred mappings are disclosed;
- user annotations remain byte-for-byte unchanged unless the user asked to edit them.

## 9. Write the report

Organize `report.md` as:

1. Scope and search limits.
2. Workflow catalog overview.
3. One section per common workflow.
4. Paper-specific workflows.
5. Node-by-node algorithm comparison.
6. Patent coverage and patent-family notes.
7. Conflicts, weak evidence, and unresolved mappings.
8. Research gaps and plausible combinations, clearly labeled as synthesis rather than source claims.

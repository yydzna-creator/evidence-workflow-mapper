---
name: evidence-workflow-mapper
description: Research a technical direction across papers and patents, expand from seed sources, and produce one or more normalized, evidence-linked workflows plus an interactive research notebook. Use for literature landscapes, patent landscapes, method pipelines, cross-paper workflow comparison, visual note-taking, or updates to an existing workflow catalog. Do not use for a plain bibliography or a single-document summary that does not need workflow synthesis.
---

# Evidence Workflow Mapper

Build a traceable catalog of technical workflows. Organize knowledge around normalized process nodes rather than around a flat source list.

## Select the operating mode

- **Create:** Research a new direction and create a workflow catalog.
- **Update:** Add sources to an existing catalog without replacing stable IDs or user annotations.
- **Deepen:** Expand searches around selected workflow nodes, algorithms, authors, citations, patent classes, or assignees.
- **Compare:** Compare selected common or paper-specific workflows without performing a new search unless requested.
- **Render:** Validate an existing bundle and rebuild its interactive viewer.

For Create, Update, or Deepen, read [references/research-protocol.md](references/research-protocol.md). For any mode that writes or modifies JSON, read [references/workflow-schema.md](references/workflow-schema.md). Read [references/output-spec.md](references/output-spec.md) before delivering a bundle. When the topic concerns analog or mixed-signal physical design, also read [references/analog-routing-profile.md](references/analog-routing-profile.md).

## Non-negotiable model

1. A topic may contain multiple categories and multiple common workflows. Never force the literature into one universal pipeline.
2. A source that does not fit a common workflow may have a paper-specific workflow.
3. Display only normalized workflows. Do not generate a separate original-author workflow view.
4. Preserve the author's original term, source locator, and mapping confidence inside each evidence mapping so the normalization remains auditable.
5. If a source step cannot map honestly to an existing normalized node, create a stable `paper-specific` node near the closest common concept. Do not silently generalize it.
6. Keep generated workflow data separate from user annotations and notebook state. Updating research must not overwrite `annotations.json` or an exported notebook file.
7. Every method or algorithm claim attached to a node must cite at least one source and include a useful locator when full text or patent claims are available.
8. Mark evidence access explicitly as `full-text`, `abstract-only`, or `metadata-only`. Never present abstract- or snippet-level inference as full-text verification.

## Required outputs

Produce a bundle containing at least:

- `workflow.json` - categories, normalized nodes, common workflows, paper-specific workflows, and evidence mappings.
- `sources.json` - deduplicated paper and patent metadata.
- `annotations.json` - user-owned annotations; initialize only when absent.
- `search-log.json` - search date, query, source, expansion reason, and result count for research modes.
- `report.md` - concise synthesis organized by workflow rather than source order.
- `index.html` - offline GoodNotes-like research notebook generated from the JSON bundle. It must keep papers/patents in a compact side shelf and expand one selected source at a time.

Use stable lowercase kebab-case IDs. During updates, reuse existing IDs even when labels are improved.

## Validate and render

From the skill directory, run:

```bash
python scripts/validate_workflow.py <bundle-directory>
python scripts/build_viewer.py <bundle-directory> --output <bundle-directory>/index.html
python scripts/check_viewer.py <bundle-directory>/index.html
```

Fix validation errors before delivery. Warnings about weak evidence may remain only when they are clearly disclosed in `report.md`.

## Completion report

State the search scope and date, number of papers and patents, number of common and paper-specific workflows, evidence-access limitations, unresolved mappings, and the paths to `report.md` and the notebook `index.html`.

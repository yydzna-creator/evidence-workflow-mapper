# Evidence Workflow Mapper

Evidence Workflow Mapper is a reusable Codex skill for researching papers and patents, expanding from seed literature, and mapping methods onto one or more normalized, evidence-linked workflows.

It can generate an offline, GoodNotes-like research notebook in which workflow nodes remain visible on the canvas while papers and patents stay collapsed in a compact side shelf. Selecting a source reveals its method, algorithms, locators, and mapping confidence.

## What the skill supports

- multiple workflow categories and multiple common workflows per technical direction;
- paper-specific workflows when a method cannot be aligned without distortion;
- normalized nodes for cross-paper comparison;
- evidence mappings with original terminology, algorithm, source locator, access level, and confidence;
- paper and patent expansion from seed sources;
- offline notebook generation with annotations and portable import/export;
- update, deepen, compare, and render modes for an existing catalog.

## Install

Ask Codex to use `$skill-installer` with this repository's skill directory:

```text
$skill-installer
Install the skill from https://github.com/<owner>/evidence-workflow-mapper/tree/main/skills/evidence-workflow-mapper
```

For manual installation, copy `skills/evidence-workflow-mapper` to:

```text
%USERPROFILE%\.codex\skills\evidence-workflow-mapper
```

Restart Codex after installation so the skill is discovered.

## Use

```text
$evidence-workflow-mapper
Research analog integrated-circuit routing papers and patents. Expand one citation ring, derive multiple normalized workflows where supported, preserve paper-specific workflows, and generate the interactive notebook.
```

You may also ask the skill to update an existing catalog, deepen one workflow node, compare selected workflows, or rebuild the notebook from an existing bundle.

## Generated research bundle

The skill creates the following files in a user-selected output directory:

```text
workflow.json
sources.json
annotations.json
search-log.json
report.md
index.html
```

`annotations.json` is user-owned. Updating research data must not overwrite annotations or an exported notebook.

## Privacy

This repository contains only the reusable skill, scripts, references, and notebook template. It does not contain the author's research bundles, paper lists, patents, notes, annotations, search logs, or generated notebooks.

## Requirements

Python 3 is required for validation and notebook generation. Runtime scripts use only the Python standard library.

## License

MIT

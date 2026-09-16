# Evidence Workflow Mapper

一个适合初学者的 Codex 研究 Skill：通过论文、专利和可追溯流程图，快速了解某个技术领域的主要方向、典型流程、关键步骤与代表方法。

Evidence Workflow Mapper is a beginner-friendly Codex skill for quickly understanding a technical field. It researches papers and patents, expands from seed literature, and organizes the results into one or more normalized, evidence-linked workflows.

It can generate an offline, GoodNotes-like research notebook in which workflow nodes remain visible on the canvas while papers and patents stay collapsed in a compact side shelf. Selecting a source reveals its method, algorithms, locators, and mapping confidence.

You do not need to know the field's terminology or workflow in advance. Start with a topic or a few seed papers, and the skill will help build a structured map from the broad landscape down to individual methods and evidence.

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
Install the skill from https://github.com/yydzna-creator/evidence-workflow-mapper/tree/main/skills/evidence-workflow-mapper
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

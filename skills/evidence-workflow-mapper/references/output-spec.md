# Output and Research Notebook Specification

## Bundle contents

Deliver research results as one self-contained directory:

```text
research-bundle/
|-- workflow.json
|-- sources.json
|-- annotations.json
|-- search-log.json
|-- report.md
`-- index.html
```

Do not place downloaded copyrighted papers in a distributable bundle. Preserve stable links, identifiers, metadata, short evidence paraphrases, and locators instead.

## Interactive research notebook

Build `index.html` with `scripts/build_viewer.py`. The resulting page must work offline without a web server or external JavaScript libraries. Treat it as a GoodNotes-like research notebook, not a dashboard.

The notebook provides:

- a left page rail containing a research overview, one page per common or paper-specific workflow, and a free-note page;
- a central paper canvas where normalized workflow nodes can be moved, zoomed, drawn on, highlighted, and annotated with sticky notes;
- a compact right paper shelf designed for large source collections; each source stays collapsed as a small side thumbnail until selected;
- one-source-at-a-time expansion showing metadata, methods, algorithms, original terminology, locators, and every normalized step mapped to that source;
- bidirectional navigation: selecting a source highlights its nodes, and selecting a node exposes its source evidence;
- import of a generated `workflow.json` + `sources.json` bundle into the notebook;
- local persistence plus portable notebook JSON export/import for node positions, ink strokes, highlights, and sticky notes;
- explicit labels for provisional, contested, inferred, and weakly verified content.

Do not place every paper on the canvas. The workflow is the main spatial object; papers and patents belong in the compact side shelf so the interface continues to work with hundreds of sources.

Do not show an original-author workflow. Show `original_term` and `locator` only in the evidence card for audit.

## Report conventions

- Lead with the identified workflow families and their differences.
- Keep common and paper-specific workflows distinct.
- Report source coverage rather than treating publication count as truth.
- Separate source-backed statements from synthesis and research-gap hypotheses.
- Include the search execution date and limitations.
- Link workflow and node IDs in prose when useful for cross-reference.

## Updating a bundle

Before updating, copy or hash `annotations.json` and preserve any exported `*-notebook.json`. After updating and rendering, verify user-owned state is unchanged unless the user explicitly requested annotation edits. New workflows and nodes must receive new stable IDs; existing IDs must not change only because wording was refined.

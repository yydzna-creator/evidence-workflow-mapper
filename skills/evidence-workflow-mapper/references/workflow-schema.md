# Workflow Bundle Schema

The bundle uses four JSON files. Version this contract with `schema_version`. Current version: `1.0`.

## workflow.json

```json
{
  "schema_version": "1.0",
  "project": {
    "id": "analog-routing-landscape",
    "title": "Analog Routing Workflow Landscape",
    "topic": "analog integrated-circuit routing",
    "generated_at": "2026-09-16T00:00:00Z"
  },
  "categories": [
    {
      "id": "constraint-driven",
      "title": "Constraint-driven routing",
      "description": "Workflows that explicitly derive and propagate analog constraints."
    }
  ],
  "nodes": [
    {
      "id": "extract-constraints",
      "title": "Extract design constraints",
      "scope": "common",
      "summary": "Derive routing constraints from available design representations.",
      "inputs": ["layout and connectivity data"],
      "outputs": ["normalized constraint set"],
      "aliases": ["constraint generation"]
    }
  ],
  "workflows": [
    {
      "id": "constraint-first-routing",
      "title": "Constraint-first routing",
      "kind": "common",
      "category_id": "constraint-driven",
      "summary": "Extract constraints before topology construction.",
      "status": "supported",
      "steps": [
        {
          "id": "constraint-first.extract",
          "node_id": "extract-constraints",
          "summary": "Create explicit symmetry, matching, and protection constraints.",
          "algorithms": ["graph matching", "rule-based extraction"],
          "evidence": [
            {
              "source_id": "paper-example",
              "contribution": "Builds a normalized constraint graph before routing.",
              "algorithm": "graph matching",
              "original_term": "constraint graph construction",
              "locator": "Section III-A",
              "mapping_confidence": "high",
              "statement_basis": "reported"
            }
          ]
        }
      ],
      "edges": []
    }
  ]
}
```

### Enumerations

- Node `scope`: `common` or `paper-specific`.
- Workflow `kind`: `common` or `paper-specific`.
- Workflow `status`: `supported`, `provisional`, or `contested`.
- Evidence `mapping_confidence`: `high`, `medium`, or `low`.
- Evidence `statement_basis`: `reported`, `inferred`, or `unresolved`.
- Edge `type`: `sequence`, `iteration`, `optional`, or `alternative`.

Each workflow step references exactly one normalized node. A paper-specific workflow still uses normalized nodes. It does not recreate an original-author flow. Original terminology is allowed only inside evidence mappings.

An edge has `from`, `to`, and `type`; `from` and `to` reference step IDs within the same workflow. Use an optional `label` for a branch or iteration condition.

## sources.json

```json
{
  "schema_version": "1.0",
  "sources": [
    {
      "id": "paper-example",
      "type": "paper",
      "title": "Example title",
      "year": 2025,
      "authors": ["A. Author"],
      "url": "https://example.org/record",
      "identifiers": {"doi": "10.0000/example"},
      "access_level": "full-text",
      "verification_status": "verified",
      "is_demo": false
    }
  ]
}
```

Source `type` is `paper`, `patent`, or `other`. `access_level` is `full-text`, `abstract-only`, or `metadata-only`. `verification_status` is `verified`, `partial`, or `unverified`.

For patents, add `publication_number`, `family_id`, `jurisdiction`, `assignees`, `inventors`, and optional dated `legal_status`. Count a patent family once in summaries unless the user requests jurisdiction-level analysis.

## annotations.json

```json
{
  "schema_version": "1.0",
  "project_id": "analog-routing-landscape",
  "annotations": [
    {
      "id": "note-001",
      "target_type": "step",
      "target_id": "constraint-first.extract",
      "body": "Compare this with the topology-first branch.",
      "tags": ["follow-up"],
      "created_at": "2026-09-16T00:00:00Z",
      "updated_at": "2026-09-16T00:00:00Z"
    }
  ]
}
```

Valid annotation targets are `workflow`, `step`, `node`, and `source`. User annotations are independent state. Research updates must not recreate, reorder, rewrite, or delete them without explicit instruction.

## search-log.json

```json
{
  "schema_version": "1.0",
  "project_id": "analog-routing-landscape",
  "searches": [
    {
      "id": "search-001",
      "executed_at": "2026-09-16T00:00:00Z",
      "service": "example scholarly index",
      "query": "analog routing symmetry constraint",
      "expansion_type": "seed",
      "reason": "Establish the core vocabulary.",
      "results_inspected": 20,
      "retained_source_ids": ["paper-example"]
    }
  ],
  "stopping_reason": "One complete expansion ring produced no new workflow structure."
}
```

## Stable-ID rules

- Use lowercase kebab-case IDs for projects, categories, nodes, workflows, and sources.
- Step IDs use `<workflow-id>.<local-step-id>`.
- Never derive IDs from array positions.
- Reuse IDs across updates even when titles change.
- Never reuse a deleted ID for a different concept.
- When merging nodes, retain redirects in the surviving node's optional `legacy_ids` array so annotations can be migrated deliberately.

# Analog and Mixed-Signal Routing Starter Profile

Use this profile as a search and normalization seed, not as a claim that every analog-routing method follows the same pipeline.

## Input representations

Possible inputs include DEF/LEF or technology LEF, circuit netlists, placed devices, device-group or matching information, routing and design-rule constraints, blockages, existing layout geometry, and performance targets. Do not claim that DEF alone contains all symmetry, matching, differential-pair, shielding, or sensitivity constraints.

## Candidate normalized nodes

Create only nodes supported by the actual source set. Useful initial candidates include:

- ingest-design-data
- normalize-connectivity
- identify-sensitive-nets
- extract-symmetry-constraints
- extract-matching-constraints
- derive-shielding-constraints
- decompose-multi-pin-nets
- prioritize-nets
- construct-routing-topology
- allocate-routing-regions
- perform-global-routing
- perform-detailed-routing
- enforce-paired-routing
- insert-shields-and-guards
- optimize-parasitics
- repair-design-rule-violations
- verify-geometric-constraints
- verify-electrical-performance
- iterate-routing-and-evaluation

Use `scope: "paper-specific"` for a specialized operation until evidence supports treating it as common.

## Search vocabulary

Combine the application term with process, constraint, and algorithm terms. Examples:

- analog integrated circuit routing
- analog layout automation routing
- symmetry constrained routing
- matching aware routing
- differential pair routing
- multi-pin net decomposition analog layout
- rectilinear Steiner topology analog routing
- constraint graph analog routing
- performance driven analog routing
- parasitic aware analog routing
- analog routing patent

Expand with terminology encountered in retained sources. Search patents using equivalent functional language, assignees, inventors, citations, and relevant classifications rather than relying only on academic phrases.

## Comparison dimensions

When sources permit, compare workflows along:

- input representations and required annotations;
- explicit versus inferred constraints;
- multi-pin decomposition and topology model;
- sequential versus joint optimization;
- net ordering and criticality treatment;
- global/detailed routing relationship;
- symmetry, matching, differential, shielding, and guard-ring handling;
- objective functions and solver family;
- DRC and electrical-performance feedback;
- benchmark type, scale, technology assumptions, and reproducibility.

Treat algorithm names as evidence-backed attributes of a normalized step, not as normalized workflow nodes unless the algorithm itself is the process stage being compared.

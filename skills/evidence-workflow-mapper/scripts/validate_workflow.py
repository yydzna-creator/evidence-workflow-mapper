#!/usr/bin/env python3
"""Validate an Evidence Workflow Mapper research bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ID_PATTERN = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
REQUIRED_FILES = ("workflow.json", "sources.json", "annotations.json", "search-log.json")


def _load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing required file: {path.name}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"{path.name}: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name}: top-level value must be an object")
        return {}
    return value


def _require_string(obj: dict[str, Any], field: str, where: str, errors: list[str]) -> str:
    value = obj.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{where}: '{field}' must be a non-empty string")
        return ""
    return value


def _check_id(value: str, where: str, errors: list[str]) -> None:
    if value and not ID_PATTERN.fullmatch(value):
        errors.append(f"{where}: ID '{value}' must use lowercase letters, digits, hyphens, or dots")


def _unique_ids(items: Any, where: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        errors.append(f"{where}: must be an array")
        return {}
    result: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        item_where = f"{where}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_where}: must be an object")
            continue
        item_id = _require_string(item, "id", item_where, errors)
        _check_id(item_id, item_where, errors)
        if item_id in result:
            errors.append(f"{item_where}: duplicate ID '{item_id}'")
        elif item_id:
            result[item_id] = item
    return result


def validate_bundle(bundle: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    bundle = bundle.resolve()

    workflow_data = _load_json(bundle / "workflow.json", errors)
    source_data = _load_json(bundle / "sources.json", errors)
    annotation_data = _load_json(bundle / "annotations.json", errors)
    search_data = _load_json(bundle / "search-log.json", errors)

    for filename, data in (
        ("workflow.json", workflow_data),
        ("sources.json", source_data),
        ("annotations.json", annotation_data),
        ("search-log.json", search_data),
    ):
        if data and data.get("schema_version") != "1.0":
            errors.append(f"{filename}: schema_version must be '1.0'")

    project = workflow_data.get("project", {})
    if not isinstance(project, dict):
        errors.append("workflow.json: 'project' must be an object")
        project = {}
    project_id = _require_string(project, "id", "workflow.json.project", errors)
    _check_id(project_id, "workflow.json.project", errors)
    _require_string(project, "title", "workflow.json.project", errors)
    _require_string(project, "topic", "workflow.json.project", errors)
    _require_string(project, "generated_at", "workflow.json.project", errors)

    categories = _unique_ids(workflow_data.get("categories"), "workflow.json.categories", errors)
    nodes = _unique_ids(workflow_data.get("nodes"), "workflow.json.nodes", errors)
    workflows = _unique_ids(workflow_data.get("workflows"), "workflow.json.workflows", errors)
    sources = _unique_ids(source_data.get("sources"), "sources.json.sources", errors)

    for category_id, category in categories.items():
        _require_string(category, "title", f"category '{category_id}'", errors)

    for node_id, node in nodes.items():
        where = f"node '{node_id}'"
        _require_string(node, "title", where, errors)
        if node.get("scope") not in {"common", "paper-specific"}:
            errors.append(f"{where}: scope must be 'common' or 'paper-specific'")
        for field in ("inputs", "outputs", "aliases"):
            value = node.get(field, [])
            if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
                errors.append(f"{where}: '{field}' must be an array of strings")

    source_types = {"paper", "patent", "other"}
    access_levels = {"full-text", "abstract-only", "metadata-only"}
    verification_states = {"verified", "partial", "unverified"}
    for source_id, source in sources.items():
        where = f"source '{source_id}'"
        _require_string(source, "title", where, errors)
        if source.get("type") not in source_types:
            errors.append(f"{where}: type must be one of {sorted(source_types)}")
        if source.get("access_level") not in access_levels:
            errors.append(f"{where}: access_level must be one of {sorted(access_levels)}")
        if source.get("verification_status") not in verification_states:
            errors.append(f"{where}: verification_status must be one of {sorted(verification_states)}")
        if source.get("type") == "patent" and not source.get("publication_number"):
            warnings.append(f"{where}: patent has no publication_number")

    step_ids: set[str] = set()
    source_usage: set[str] = set()
    common_count = 0
    paper_specific_count = 0
    allowed_status = {"supported", "provisional", "contested"}
    allowed_confidence = {"high", "medium", "low"}
    allowed_basis = {"reported", "inferred", "unresolved"}
    allowed_edge_types = {"sequence", "iteration", "optional", "alternative"}

    for workflow_id, workflow in workflows.items():
        where = f"workflow '{workflow_id}'"
        _require_string(workflow, "title", where, errors)
        kind = workflow.get("kind")
        if kind == "common":
            common_count += 1
        elif kind == "paper-specific":
            paper_specific_count += 1
        else:
            errors.append(f"{where}: kind must be 'common' or 'paper-specific'")
        if workflow.get("status") not in allowed_status:
            errors.append(f"{where}: status must be one of {sorted(allowed_status)}")
        category_id = workflow.get("category_id")
        if category_id not in categories:
            errors.append(f"{where}: unknown category_id '{category_id}'")

        steps = workflow.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"{where}: steps must be a non-empty array")
            steps = []
        local_steps: dict[str, dict[str, Any]] = {}
        workflow_sources: set[str] = set()
        for index, step in enumerate(steps):
            step_where = f"{where}.steps[{index}]"
            if not isinstance(step, dict):
                errors.append(f"{step_where}: must be an object")
                continue
            step_id = _require_string(step, "id", step_where, errors)
            _check_id(step_id, step_where, errors)
            if step_id and not step_id.startswith(f"{workflow_id}."):
                errors.append(f"{step_where}: step ID must start with '{workflow_id}.'")
            if step_id in step_ids:
                errors.append(f"{step_where}: duplicate global step ID '{step_id}'")
            if step_id:
                step_ids.add(step_id)
                local_steps[step_id] = step
            node_id = _require_string(step, "node_id", step_where, errors)
            if node_id not in nodes:
                errors.append(f"{step_where}: unknown node_id '{node_id}'")
            elif kind == "common" and nodes[node_id].get("scope") == "paper-specific":
                errors.append(f"{step_where}: common workflow cannot use paper-specific node '{node_id}'")

            algorithms = step.get("algorithms", [])
            if not isinstance(algorithms, list) or not all(isinstance(x, str) for x in algorithms):
                errors.append(f"{step_where}: algorithms must be an array of strings")
                algorithms = []
            evidence_items = step.get("evidence", [])
            if not isinstance(evidence_items, list):
                errors.append(f"{step_where}: evidence must be an array")
                evidence_items = []
            evidence_algorithms: set[str] = set()
            for evidence_index, evidence in enumerate(evidence_items):
                evidence_where = f"{step_where}.evidence[{evidence_index}]"
                if not isinstance(evidence, dict):
                    errors.append(f"{evidence_where}: must be an object")
                    continue
                source_id = _require_string(evidence, "source_id", evidence_where, errors)
                if source_id not in sources:
                    errors.append(f"{evidence_where}: unknown source_id '{source_id}'")
                else:
                    source_usage.add(source_id)
                    workflow_sources.add(source_id)
                    if sources[source_id].get("access_level") == "full-text" and not evidence.get("locator"):
                        warnings.append(f"{evidence_where}: full-text evidence has no locator")
                _require_string(evidence, "contribution", evidence_where, errors)
                if evidence.get("mapping_confidence") not in allowed_confidence:
                    errors.append(f"{evidence_where}: mapping_confidence must be one of {sorted(allowed_confidence)}")
                if evidence.get("statement_basis") not in allowed_basis:
                    errors.append(f"{evidence_where}: statement_basis must be one of {sorted(allowed_basis)}")
                algorithm = evidence.get("algorithm")
                if isinstance(algorithm, str) and algorithm:
                    evidence_algorithms.add(algorithm.casefold())
            for algorithm in algorithms:
                if algorithm.casefold() not in evidence_algorithms:
                    errors.append(f"{step_where}: algorithm '{algorithm}' has no matching evidence mapping")

        edges = workflow.get("edges", [])
        if not isinstance(edges, list):
            errors.append(f"{where}: edges must be an array")
            edges = []
        for edge_index, edge in enumerate(edges):
            edge_where = f"{where}.edges[{edge_index}]"
            if not isinstance(edge, dict):
                errors.append(f"{edge_where}: must be an object")
                continue
            if edge.get("from") not in local_steps or edge.get("to") not in local_steps:
                errors.append(f"{edge_where}: from/to must reference steps in the same workflow")
            if edge.get("type") not in allowed_edge_types:
                errors.append(f"{edge_where}: type must be one of {sorted(allowed_edge_types)}")

        if kind == "common" and len(workflow_sources) < 2 and workflow.get("status") != "provisional":
            warnings.append(f"{where}: common workflow has fewer than two source records; consider status 'provisional'")

    all_targets = set(workflows) | set(nodes) | set(sources) | step_ids
    annotations = _unique_ids(annotation_data.get("annotations"), "annotations.json.annotations", errors)
    if annotation_data.get("project_id") != project_id:
        errors.append("annotations.json: project_id does not match workflow.json project.id")
    valid_target_types = {"workflow", "step", "node", "source"}
    for annotation_id, annotation in annotations.items():
        where = f"annotation '{annotation_id}'"
        if annotation.get("target_type") not in valid_target_types:
            errors.append(f"{where}: target_type must be one of {sorted(valid_target_types)}")
        target_id = _require_string(annotation, "target_id", where, errors)
        if target_id not in all_targets:
            warnings.append(f"{where}: target_id '{target_id}' is not present in this bundle")
        _require_string(annotation, "body", where, errors)

    if search_data.get("project_id") != project_id:
        errors.append("search-log.json: project_id does not match workflow.json project.id")
    searches = _unique_ids(search_data.get("searches"), "search-log.json.searches", errors)
    for search_id, search in searches.items():
        where = f"search '{search_id}'"
        _require_string(search, "executed_at", where, errors)
        _require_string(search, "service", where, errors)
        _require_string(search, "query", where, errors)
        retained = search.get("retained_source_ids", [])
        if not isinstance(retained, list):
            errors.append(f"{where}: retained_source_ids must be an array")
        else:
            for source_id in retained:
                if source_id not in sources:
                    errors.append(f"{where}: unknown retained source '{source_id}'")

    for source_id in sorted(set(sources) - source_usage):
        warnings.append(f"source '{source_id}' is not mapped to any workflow step")

    if not workflows:
        errors.append("workflow.json: at least one workflow is required")
    if not sources:
        warnings.append("sources.json: no sources are present")

    stats = {
        "categories": len(categories),
        "nodes": len(nodes),
        "workflows": len(workflows),
        "common_workflows": common_count,
        "paper_specific_workflows": paper_specific_count,
        "sources": len(sources),
        "annotations": len(annotations),
        "searches": len(searches),
    }
    return errors, warnings, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path, help="Directory containing workflow.json and companion files")
    args = parser.parse_args()

    errors, warnings, stats = validate_bundle(args.bundle)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    summary = ", ".join(f"{key}={value}" for key, value in stats.items())
    print(f"Summary: {summary}")
    if errors:
        print(f"Validation failed with {len(errors)} error(s) and {len(warnings)} warning(s).")
        return 1
    print(f"Validation passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

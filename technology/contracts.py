"""Small, offline contract checks shared by the optional technology/trace tools.

Only the JSON Schema keywords used in the bundled schemas are implemented.
These checks establish record integrity, never the truth of recorded evidence.
"""
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess


def need(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result
    def invalid(value):
        raise ValueError(f"non-finite JSON number: {value}")
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique,
                      parse_constant=invalid)


def shape(value, rule, schema=None, at="record"):
    schema = rule if schema is None else schema
    if "$ref" in rule:
        need(rule["$ref"].startswith("#/$defs/"), "only local schema references are supported")
        return shape(value, schema["$defs"][rule["$ref"].split("/")[-1]], schema, at)
    if "anyOf" in rule:
        errors = []
        for choice in rule["anyOf"]:
            try:
                shape(value, choice, schema, at)
                return
            except ValueError as error:
                errors.append(str(error))
        raise ValueError(f"{at}: no allowed shape ({'; '.join(errors)})")
    kind = rule.get("type")
    checks = {"object": isinstance(value, dict), "array": isinstance(value, list),
              "string": isinstance(value, str), "boolean": type(value) is bool,
              "integer": type(value) is int, "number": type(value) in (int, float),
              "null": value is None}
    need(kind in checks and checks[kind], f"{at}: expected {kind}")
    if "const" in rule:
        need(value == rule["const"], f"{at}: expected {rule['const']}")
    if "enum" in rule:
        need(value in rule["enum"], f"{at}: unsupported value {value!r}")
    if kind == "object":
        need(set(rule.get("required", [])) <= value.keys(), f"{at}: missing required fields")
        properties = rule.get("properties", {})
        if rule.get("additionalProperties") is False:
            need(value.keys() <= properties.keys(), f"{at}: unexpected fields {sorted(value.keys() - properties.keys())}")
        for key, child in value.items():
            if key in properties:
                shape(child, properties[key], schema, at + "." + key)
    elif kind == "array":
        need(len(value) >= rule.get("minItems", 0), f"{at}: too few items")
        need(len(value) <= rule.get("maxItems", len(value)), f"{at}: too many items")
        if rule.get("uniqueItems"):
            need(len({json.dumps(x, sort_keys=True) for x in value}) == len(value), f"{at}: duplicate items")
        for i, child in enumerate(value):
            shape(child, rule["items"], schema, f"{at}[{i}]")
    elif kind == "string":
        need(len(value.strip()) >= rule.get("minLength", 0), f"{at}: empty text")
        if "pattern" in rule:
            need(re.fullmatch(rule["pattern"], value) is not None, f"{at}: invalid format")
    elif kind in ("integer", "number"):
        need((type(value) is int or math.isfinite(value)) and value >= rule.get("minimum", -math.inf),
             f"{at}: invalid number")


def local(root, path):
    need(isinstance(path, str) and path and not Path(path).is_absolute(), "reference path must be repository relative")
    target = (root / path).resolve()
    need(target.is_relative_to(root.resolve()) and target.is_file(), f"missing/unsafe reference: {path}")
    return target


def check_ref(root, ref):
    target = local(root, ref["path"])
    data = target.read_bytes()
    need(hashlib.sha256(data).hexdigest() == ref["sha256"], f"reference hash mismatch: {ref['path']}")
    if ref["lines"] is not None:
        first, last = ref["lines"]
        need(1 <= first <= last <= len(data.decode("utf-8").splitlines()), f"invalid reference lines: {ref['path']}")
    if ref["source_revision"] is not None:
        run = subprocess.run(["git", "show", f"{ref['source_revision']}:{ref['path']}"],
                             cwd=root, capture_output=True)
        need(run.returncode == 0 and hashlib.sha256(run.stdout).hexdigest() == ref["sha256"],
             f"source revision/hash mismatch: {ref['path']}")


def refs(root, records):
    result = {}
    for ref in records:
        need(ref["id"] not in result, "duplicate reference ID: " + ref["id"])
        check_ref(root, ref)
        result[ref["id"]] = ref
    return result


def links(values, known, label, nonempty=False):
    need(not nonempty or values, label + ": evidence is required")
    need(len(set(values)) == len(values) and all(x in known for x in values), label + ": unresolved/duplicate IDs")


def immutable(root, baseline, patterns):
    if baseline is None:
        return
    need(re.fullmatch(r"[0-9a-f]{40}", baseline) is not None, "immutable base must be a full commit SHA")
    run = subprocess.run(["git", "diff", "--name-status", baseline, "--", *patterns],
                         cwd=root, capture_output=True, text=True)
    need(run.returncode == 0, "cannot compare immutable base")
    need(all(row.startswith("A\t") for row in run.stdout.splitlines()),
         "immutable record changed/deleted: append a new version/ID")


def history(root, record, prefix):
    previous = record["previous"]
    if previous is None:
        need(record["version"] == 1, "later versions require a previous record reference")
        return
    check_ref(root, previous)
    target = local(root, previous["path"])
    need(target.is_relative_to((root / prefix).resolve()), "previous record must belong to the same store")
    old = load(target)
    need(isinstance(old, dict) and old.get("schema") == record["schema"] and
         old.get("id") == record["id"] and type(old.get("version")) is int and
         old["version"] + 1 == record["version"], "invalid version ancestry")


def public_record(root, path):
    need(path.resolve().is_relative_to(root.resolve()) and path.is_file(), "record must be a public repository file, not an external/symlink escape")
    return load(path)


def stored_path(path, root, record, prefix):
    if path.absolute().is_relative_to((root / prefix).absolute()):
        need(path.resolve().is_relative_to((root / prefix).resolve()), "record escapes its store")
        need(record["fixture"] is False, "synthetic fixtures cannot enter a live record store")
        expected = root / prefix / record["id"] / f"v{record['version']:04d}.json"
        need(path.resolve() == expected.resolve(), "record path/ID/version mismatch")
        def placeholder(value):
            if isinstance(value, str):
                return "REPLACE" in value
            if isinstance(value, dict):
                return any(placeholder(x) for x in value.values())
            if isinstance(value, list):
                return any(placeholder(x) for x in value)
            return False
        need(not placeholder(record), "complete template placeholders before publishing a live record")

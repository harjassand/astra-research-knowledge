#!/usr/bin/env python3
"""Build the current public projection from base records and append-only shards.

The checkpoint-pinned v1-v4 readers/builders remain historical. V5 merges
claim, status, catalog, alias, and semantic-notice shards in memory and writes a
dated manifest. It preserves byte-identical per-card views from the v4
manifest when only the global snapshot marker changes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import build_access as legacy

ROOT = legacy.ROOT
MANIFEST_PATH = "agent/access_manifest.2026-10-25-later-v5.json"
PACKET = "research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-later-completed-sources"
PRIOR_MANIFEST = "agent/access_manifest.2026-10-24-constructive-universal-v4.json"
ORIGINAL_JSONL = legacy.jsonl
ORIGINAL_JSON = json


def files(root: Path, directory: str, suffix: str):
    folder = root / directory
    return sorted(p for p in folder.glob("*" + suffix) if p.is_file()) if folder.is_dir() else []


def jsonl_v5(root: Path, name: str):
    result = ORIGINAL_JSONL(root, name)
    directory = {
        "indexes/claims.jsonl": "indexes/claims.d",
        "frontier/CURRENT_CLAIM_STATUS.jsonl": "frontier/CURRENT_CLAIM_STATUS.d",
        "agent/SEMANTIC_NOTICES.jsonl": "agent/SEMANTIC_NOTICES.d",
    }.get(name)
    if directory:
        for path in files(root, directory, ".jsonl"):
            result.extend(ORIGINAL_JSONL(root, path.relative_to(root).as_posix()))
    return result


def merged_loads(root: Path, text: str, *args, **kwargs):
    value = ORIGINAL_JSON.loads(text, *args, **kwargs)
    if not isinstance(value, dict):
        return value
    text_bytes = text if isinstance(text, bytes) else text.encode("utf-8")
    raw_catalog = (root / "indexes/agent_catalog.json").read_bytes()
    if hashlib.sha256(raw_catalog).hexdigest() == hashlib.sha256(text_bytes).hexdigest():
        value = dict(value)
        catalog = list(value["claims"])
        for path in files(root, "indexes/agent_catalog.d", ".json"):
            part = ORIGINAL_JSON.loads(path.read_text(encoding="utf-8"))
            catalog.extend(part["claims"])
        value["claims"] = catalog
        return value
    raw_aliases = (root / "indexes/query_aliases.json").read_bytes()
    if hashlib.sha256(raw_aliases).hexdigest() == hashlib.sha256(text_bytes).hexdigest():
        value = dict(value)
        aliases = dict(value)
        for path in files(root, "indexes/query_aliases.d", ".json"):
            aliases.update(ORIGINAL_JSON.loads(path.read_text(encoding="utf-8")))
        return aliases
    return value


def preserve_v4_card_views(root: Path, outputs: dict[str, bytes]):
    path = root / PRIOR_MANIFEST
    if not path.is_file():
        return
    prior = ORIGINAL_JSON.loads(path.read_text(encoding="utf-8"))
    prior_outputs = prior.get("outputs", {})
    for name, generated in list(outputs.items()):
        if not name.startswith(("frontier/dossiers/", "frontier/connections/", "frontier/proof_ranges/")):
            continue
        old_hash = prior_outputs.get(name)
        existing_path = root / name
        if not old_hash or not existing_path.is_file():
            continue
        existing = existing_path.read_bytes()
        if legacy.digest(existing) != old_hash:
            continue
        try:
            if legacy.stable_projection(name, existing) == legacy.stable_projection(name, generated):
                outputs[name] = existing
        except (ORIGINAL_JSON.JSONDecodeError, UnicodeDecodeError):
            continue


def build(root=ROOT, base_revision=None):
    root = Path(root)
    v5_shards = []
    for directory in ("indexes/claims.d", "indexes/agent_catalog.d", "indexes/query_aliases.d",
                      "frontier/CURRENT_CLAIM_STATUS.d", "agent/SEMANTIC_NOTICES.d"):
        v5_shards.extend(p.relative_to(root).as_posix() for p in files(root, directory, ".jsonl" if directory.endswith(".d") and directory != "indexes/agent_catalog.d" and directory != "indexes/query_aliases.d" else ".json"))
    source_manifest = root / PACKET / "source_manifest.json"
    source_files = ORIGINAL_JSON.loads(source_manifest.read_text(encoding="utf-8"))["files"]
    source_paths = [f"{PACKET}/{item['retained_path']}" for item in source_files]
    prior_manifest_path = root / PRIOR_MANIFEST
    prior_outputs = ORIGINAL_JSON.loads(prior_manifest_path.read_text(encoding="utf-8")).get("outputs", {}) if prior_manifest_path.is_file() else {}
    preserved_paths = [name for name in prior_outputs if name.startswith(("frontier/dossiers/", "frontier/connections/", "frontier/proof_ranges/"))]
    v5_inputs = [
        *legacy.INPUTS,
        "frontier/build_access_v4.py", "frontier/retrieve_v4.py", "frontier/test_access_v4.py",
        "frontier/build_access_v5.py", "frontier/retrieve_v5.py", "frontier/test_access_v5.py", "state/check_v5.py",
        f"{PACKET}/source_manifest.json", f"{PACKET}/README.md", f"{PACKET}/verify_manifest.py",
        PRIOR_MANIFEST, *preserved_paths,
        "research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/README.md",
        *v5_shards, *source_paths,
    ]
    legacy.INPUTS = list(dict.fromkeys(v5_inputs))
    legacy.jsonl = jsonl_v5
    # The core v1 builder is pinned. Install a narrow JSON proxy to merge only
    # the catalog and alias files while keeping its other JSON behavior intact.
    legacy.json = SimpleNamespace(**{name: getattr(ORIGINAL_JSON, name) for name in dir(ORIGINAL_JSON) if not name.startswith("_")})
    legacy.json.loads = lambda text, *args, **kwargs: merged_loads(root, text, *args, **kwargs)
    legacy.preserve_unchanged_card_views = lambda current_root, outputs: preserve_v4_card_views(Path(current_root), outputs)
    outputs, manifest = legacy.build(root=root, base_revision=base_revision)
    outputs.pop("agent/access_manifest.json", None)
    # Keep v4 routes byte-stable while publishing a separate current tree.
    prior_path = root / PRIOR_MANIFEST
    prior_manifest = ORIGINAL_JSON.loads(prior_path.read_text(encoding="utf-8")) if prior_path.is_file() else {"outputs": {}}
    for name, generated in list(outputs.items()):
        if name.startswith("frontier/dossiers/"):
            current_name = "frontier/dossiers_v5/" + name.removeprefix("frontier/dossiers/")
            current_data = generated.replace(b"frontier/connections/", b"frontier/connections_v5/")
        elif name.startswith("frontier/connections/"):
            current_name = "frontier/connections_v5/" + name.removeprefix("frontier/connections/")
            current_data = generated
        else:
            continue
        outputs[current_name] = current_data
        old_hash = prior_manifest.get("outputs", {}).get(name)
        existing_path = root / name
        if old_hash and existing_path.is_file() and legacy.digest(existing_path.read_bytes()) == old_hash:
            outputs[name] = existing_path.read_bytes()
        else:
            outputs[name] = generated
    for name in ("agent/concepts.txt", "agent/RECENT.tsv"):
        if name in outputs:
            outputs[name] = outputs[name].replace(b"frontier/dossiers/", b"frontier/dossiers_v5/")
    current = outputs["agent/CURRENT.txt"]
    current = current.replace(
        b"Freshness: frontier/build_access.py check checks current input/output hashes and regeneration.\n",
        (b"Freshness: python3 frontier/build_access_v5.py check verifies merged claim/status/catalog/alias/notice shards and source hashes.\n"
         + f"Current access manifest: {MANIFEST_PATH}; current local reader: frontier/retrieve_v5.py.\n".encode()),
    )
    outputs["agent/CURRENT.txt"] = current
    manifest["outputs"]["agent/CURRENT.txt"] = legacy.digest(current)
    legacy_manifest = ORIGINAL_JSON.loads(outputs["agent/manifest.json"])
    legacy_manifest["public_access"] = {
        "manifest": MANIFEST_PATH,
        "snapshot": manifest["snapshot"],
        "scope": "Current v5 projection merges append-only claim/status/catalog/alias/notice shards; earlier v1-v4 manifests remain historical snapshots",
        "routes": {"dossiers": "frontier/dossiers_v5/<route-ID>.txt", "connections": "frontier/connections_v5/<route-ID>.json"},
    }
    outputs["agent/manifest.json"] = legacy.encoded(legacy_manifest)
    manifest["outputs"] = {name: legacy.digest(data) for name, data in sorted(outputs.items())}
    outputs[MANIFEST_PATH] = legacy.encoded(manifest)
    return outputs, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--base-revision")
    args = parser.parse_args()
    manifest_path = ROOT / MANIFEST_PATH
    base_revision = args.base_revision
    if base_revision is None and manifest_path.exists():
        base_revision = ORIGINAL_JSON.loads(manifest_path.read_text())["snapshot"]["base_revision"]
    if base_revision is None:
        prior = ROOT / PRIOR_MANIFEST
        if prior.exists():
            base_revision = ORIGINAL_JSON.loads(prior.read_text())["snapshot"]["base_revision"]
    if base_revision is None:
        base_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run(["git", "cat-file", "-e", base_revision + "^{commit}"], cwd=ROOT, check=True, capture_output=True)
    subprocess.run(["python3", f"{PACKET}/verify_manifest.py"], cwd=ROOT, check=True, capture_output=True, text=True)
    outputs, manifest = build(base_revision=base_revision)
    if args.command == "build":
        prior_path = manifest_path if manifest_path.exists() else ROOT / PRIOR_MANIFEST
        if prior_path.exists():
            old = ORIGINAL_JSON.loads(prior_path.read_text())
            historical_manifests = {
                "agent/access_manifest.json",
                "agent/access_manifest.2026-10-24-constructive-universal.json",
                PRIOR_MANIFEST,
            }
            removed = set(old.get("outputs", {})) - outputs.keys() - historical_manifests
            if removed:
                raise ValueError("Generated routes would disappear; provide explicit migration: " + str(sorted(removed)))
        for name, data in outputs.items():
            target = ROOT / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    else:
        stale = [name for name, data in outputs.items() if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != data]
        if stale:
            raise ValueError("Missing/stale merged v5 views: " + ", ".join(stale[:10]))
    print(json.dumps({"command": args.command, "counts": manifest["counts"],
                      "input_sha256": manifest["snapshot"]["input_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, ORIGINAL_JSON.JSONDecodeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))

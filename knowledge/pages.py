"""Bounded, byte-preserving web projection for the existing Pages publisher.

Originals, historical interfaces and native indexes remain in the public source
repository. This command creates no workflow, service, schedule or permission.
"""
import argparse
from contextlib import contextmanager
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "harjassand/astra-research-knowledge"
REMOTE = "https://github.com/" + REPOSITORY + ".git"
BRANCH = "codex/astra-pages"
SCHEMA = "astra.pages-view.v1"
MAX_BYTES = 500_000_000
PREFIXES = ("knowledge/current/packets/", "knowledge/current/content/",
            "knowledge/current/postings/", "knowledge/current/browse/")
EXACT = {"knowledge/current/catalog.json", "knowledge/current/search_manifest.json",
         "knowledge/current/coverage.json"}
SOURCE_FILES = ("knowledge/index.html", "knowledge/search.js", "knowledge/README.md",
                "knowledge/INTAKE.md", "knowledge/PAGES.md", "agent/ACCESS.txt",
                "00_START_HERE.txt", "AGENTS.md")


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args, data=None):
    return subprocess.run(["git", *args], cwd=root, input=data,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout


def path_ok(path):
    return (isinstance(path, str) and bool(path) and not PurePosixPath(path).is_absolute()
            and not any(part in ("", ".", "..") for part in path.split("/"))
            and not any(c in path for c in ("\\", "\0", "\n", "\r")))


@contextmanager
def blobs(root, revision):
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=root,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def read(path):
        if not path_ok(path):
            raise ValueError("Invalid publication path")
        process.stdin.write((revision + ":" + path + "\n").encode()); process.stdin.flush()
        header = process.stdout.readline().split()
        if len(header) != 3 or header[1] != b"blob":
            raise ValueError("Required publication source is missing: " + path)
        data = process.stdout.read(int(header[2]))
        if process.stdout.read(1) != b"\n":
            raise ValueError("Incomplete publication source: " + path)
        return data

    try:
        yield read
    finally:
        process.stdin.close()
        process.wait(timeout=30)
        process.stdout.close()


def source_url(revision, path, raw=True):
    from urllib.parse import quote
    if not re.fullmatch("[0-9a-f]{40}", revision) or not path_ok(path):
        raise ValueError("Invalid pinned source route")
    host = "https://raw.githubusercontent.com/" if raw else "https://github.com/"
    middle = "/" if raw else "/blob/"
    return host + REPOSITORY + middle + revision + "/" + quote(path, safe="/")


def validate_site(output, max_bytes=MAX_BYTES):
    output = Path(output)
    manifest = json.loads((output / "publication.json").read_bytes())
    if (manifest.get("schema") != SCHEMA or not re.fullmatch("[0-9a-f]{40}", manifest.get("source_revision", ""))
            or not re.fullmatch("[0-9a-f]{64}", manifest.get("input_version", ""))):
        raise ValueError("Invalid owned public-view manifest")
    if any(p.is_symlink() for p in output.rglob("*")):
        raise ValueError("Public view contains a symlink")
    expected = manifest["files"]
    actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if actual != set(expected) | {"publication.json"}:
        raise ValueError("Public view has missing or unowned files")
    total = (output / "publication.json").stat().st_size
    for name, metadata in expected.items():
        if not path_ok(name) or (output / name).is_symlink():
            raise ValueError("Invalid public-view file")
        data = (output / name).read_bytes(); total += len(data)
        if sha(data) != metadata["sha256"] or len(data) != metadata["bytes"]:
            raise ValueError("Changed public-view bytes: " + name)
    summary = {key: manifest[key] for key in ("schema", "source_revision", "input_version", "search_manifest_sha256")}
    markers = re.findall(r'<script id="publication" type="application/json">(.*?)</script>',
                         (output / "knowledge/index.html").read_text(), re.S)
    if len(markers) != 1 or json.loads(markers[0]) != summary:
        raise ValueError("Public HTML and publication source versions disagree")
    search_raw = (output / "knowledge/current/search_manifest.json").read_bytes()
    search = json.loads(search_raw)
    if sha(search_raw) != summary["search_manifest_sha256"] or search["input_version"] != summary["input_version"]:
        raise ValueError("Public search manifest and source version disagree")
    for name, metadata in expected.items():
        if name.startswith(PREFIXES[:3]) or name == "knowledge/current/catalog.json":
            if search["outputs"].get(name) != metadata["sha256"]:
                raise ValueError("Public search file is outside its canonical manifest: " + name)
    routes = json.loads((output / "source-routes.json").read_bytes())
    if routes["source_revision"] != summary["source_revision"]:
        raise ValueError("Archived source routes have the wrong source version")
    if sum(name.startswith("knowledge/current/packets/") for name in expected) != manifest["scientific_records"]:
        raise ValueError("Public packet count and declared coverage disagree")
    if total > min(max_bytes, MAX_BYTES):
        raise ValueError("Public view exceeds its byte budget: " + str(total))
    return manifest, total


def stage(revision, output, root=ROOT, max_bytes=MAX_BYTES):
    """Read one committed source tree, never a mixture of working-tree files."""
    if not re.fullmatch("[0-9a-f]{40}", revision):
        raise ValueError("A full source revision is required")
    root, output = Path(root), Path(output)
    if output.resolve().is_relative_to(root.resolve()):
        raise ValueError("Stage the public view outside the source checkout")
    members = set(git(root, "ls-tree", "-r", "-z", "--name-only", revision).decode().split("\0")) - {""}
    if output.exists():
        prior, size = validate_site(output, max_bytes)
        if prior["source_revision"] != revision:
            raise ValueError("Existing public-view directory belongs to another version; use a new directory")
        return prior, size
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".astra-pages-", dir=output.parent) as temporary, blobs(root, revision) as read:
        work = Path(temporary) / "view"; work.mkdir()
        canonical = json.loads(read("knowledge/current/manifest.json"))
        required = set(canonical["inputs"]) | set(canonical["outputs"])
        if required - members:
            raise ValueError("Published source tree lacks required inputs/views: " + ", ".join(sorted(required - members)[:8]))
        selected = sorted(p for p in canonical["outputs"] if p.startswith(PREFIXES) or p in EXACT)
        if not EXACT <= set(selected):
            raise ValueError("Browser manifest/catalog/coverage closure is incomplete")
        records_raw = read("knowledge/current/records.jsonl")
        if sha(records_raw) != canonical["outputs"]["knowledge/current/records.jsonl"]:
            raise ValueError("Canonical record stream does not match its manifest")
        records = {json.loads(line)["id"] for line in records_raw.splitlines() if line.strip()}
        packet_ids, files = set(), {}

        def put(name, data):
            if not path_ok(name):
                raise ValueError("Invalid generated publication path")
            target = work / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
            files[name] = {"sha256": sha(data), "bytes": len(data)}

        for name in selected:
            data = read(name)
            if sha(data) != canonical["outputs"][name]:
                raise ValueError("Canonical browser view changed: " + name)
            if name.startswith("knowledge/current/packets/"):
                packet_ids.add(json.loads(data)["id"])
            put(name, data)
        if packet_ids != records:
            raise ValueError("Browser packets do not cover the complete canonical record set")
        summary = {"schema": SCHEMA, "source_revision": revision,
                   "input_version": canonical["input_version"],
                   "search_manifest_sha256": canonical["outputs"]["knowledge/current/search_manifest.json"]}
        for name in SOURCE_FILES:
            data = read(name)
            if name in canonical["inputs"] and sha(data) != canonical["inputs"][name]:
                raise ValueError("Browser source differs from normalized source version: " + name)
            if name == "knowledge/index.html":
                anchor = '<script type="module" src="search.js"></script>'
                if data.decode().count(anchor) != 1:
                    raise ValueError("Browser publication anchor is not unique")
                marker = '<script id="publication" type="application/json">' + encoded(summary).decode() + '</script>'
                data = data.decode().replace(anchor, marker + anchor).encode()
            if name == "knowledge/search.js" and (b"astra.pages-view.v1" not in data or b"sourceURL" not in data):
                raise ValueError("Source browser does not implement the pinned publication protocol")
            put(name, data)
        put(".nojekyll", b"")
        put("source-routes.json", encoded({"source_revision": revision, "paths": sorted(members)}))
        tree = "https://github.com/" + REPOSITORY + "/tree/" + revision
        put("index.html", ('<!doctype html><meta charset="utf-8"><title>Astra knowledge</title>'
            '<meta http-equiv="refresh" content="0;url=knowledge/">'
            '<p><a href="knowledge/">Current scientific search</a></p><p><a href="history.html">Public originals and history</a></p>').encode())
        archives = [(p, source_url(revision, p, raw=False)) for p in
                    ("00_START_HERE.txt", "agent/CURRENT.txt", "index-historical-20261025.html") if p in members]
        history = ('<!doctype html><meta charset="utf-8"><title>Astra source history</title>'
            '<h1>Public originals and historical interfaces</h1><p>The originals, result identities and frozen interfaces already published in this repository remain at this immutable source version. '
            'The Pages projection serves current search and packets; original proofs, downloads and historical payloads use their exact GitHub versions.</p>'
            '<p><a href="' + tree + '">Complete source tree and Git history</a></p><ul>' +
            ''.join('<li><a href="' + html.escape(url, quote=True) + '">' + html.escape(p) + '</a></li>' for p, url in archives) +
            '</ul><p><a href="knowledge/">Current search</a></p>')
        put("history.html", history.encode())
        fallback = '''<!doctype html><meta charset="utf-8"><title>Astra archived source</title>
<h1>Original source access</h1><p id="source">Checking the pinned public source route…</p><p><a href="/astra-research-knowledge/knowledge/">Current search</a> · <a href="/astra-research-knowledge/history.html">History</a></p>
<script>const prefix='/astra-research-knowledge/';const expected='REVISION';
fetch(prefix+'source-routes.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Source map unavailable');return r.json()}).then(map=>{
if(map.source_revision!==expected)throw Error('Publication changed; reload this page');
const p=decodeURIComponent(location.pathname);if(!p.startsWith(prefix))throw Error('Outside this source collection');
const path=p.slice(prefix.length);if(!map.paths.includes(path)||!/^[0-9a-f]{40}$/.test(map.source_revision))throw Error('No preserved route at this version');
const link=document.createElement('a');link.href='https://raw.githubusercontent.com/harjassand/astra-research-knowledge/'+map.source_revision+'/'+path.split('/').map(encodeURIComponent).join('/');link.textContent='Read exact original: '+path;document.querySelector('#source').replaceChildren(link);
}).catch(e=>{document.querySelector('#source').textContent=e.message});</script>'''
        put("404.html", fallback.replace("REVISION", revision).encode())
        manifest = {**summary, "scientific_records": len(records), "files": files,
                    "scope": "Generated navigation only. Original bytes and history remain at the pinned public Git revision; no scientific acceptance is inferred."}
        (work / "publication.json").write_bytes(encoded(manifest))
        result, size = validate_site(work, max_bytes)
        work.rename(output)
        return result, size


def remote_revision(root, branch):
    result = git(root, "ls-remote", "origin", "refs/heads/" + branch).decode().split()
    if not result:
        return None
    if len(result) != 2 or not re.fullmatch("[0-9a-f]{40}", result[0]):
        raise ValueError("Invalid publication remote revision")
    return result[0]


def publish(revision, root=ROOT):
    """Advance only the owned generated branch; never change main or permissions."""
    if git(root, "remote", "get-url", "origin").decode().strip() != REMOTE:
        raise ValueError("Publication remote is not the known public repository")
    if remote_revision(root, "main") != revision:
        raise ValueError("Publish the actual latest reviewed merged main")
    previous = remote_revision(root, BRANCH)
    if previous:
        git(root, "fetch", "--no-tags", "--no-write-fetch-head", "origin", previous)
        prior = json.loads(git(root, "show", previous + ":publication.json"))
        if prior.get("schema") != SCHEMA:
            raise ValueError("Existing publication branch is not an owned generated projection")
        members = set(git(root, "ls-tree", "-r", "-z", "--name-only", previous).decode().split("\0")) - {""}
        if members != set(prior["files"]) | {"publication.json"}:
            raise ValueError("Publication branch has unowned or missing files; preserve it for review")
    with tempfile.TemporaryDirectory(prefix="astra-pages-publish-") as temporary:
        output = Path(temporary) / "site"
        manifest, size = stage(revision, output, root)
        index = Path(temporary) / "index"
        import os
        env = dict(os.environ, GIT_INDEX_FILE=str(index))
        def indexed(*args, data=None):
            return subprocess.run(["git", *args], cwd=root, env=env, input=data,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
        indexed("read-tree", "--empty")
        entries = []
        for path in sorted(output.rglob("*")):
            if not path.is_file():
                continue
            identifier = git(root, "hash-object", "-w", "--stdin", data=path.read_bytes()).decode().strip()
            entries.append(("100644 " + identifier + "\t" + path.relative_to(output).as_posix()).encode())
        indexed("update-index", "-z", "--index-info", data=b"\0".join(entries) + b"\0")
        tree = indexed("write-tree").decode().strip()
        if previous and git(root, "rev-parse", previous + "^{tree}").decode().strip() == tree:
            return {"result": "unchanged", "source_revision": revision, "publication_revision": previous, "bytes": size}
        parent = ["-p", previous] if previous else []
        commit = git(root, "commit-tree", tree, *parent, data=("Publish Astra view for " + revision + "\n").encode()).decode().strip()
        if remote_revision(root, "main") != revision:
            raise ValueError("Main advanced during publication; stage the current source version")
        git(root, "push", "origin", commit + ":refs/heads/" + BRANCH)
        return {"result": "pushed_existing_publisher_source", "source_revision": revision,
                "input_version": manifest["input_version"], "publication_revision": commit, "bytes": size,
                "next": "Verify the existing Pages deployment and actual search/source routes. No successful deployment is inferred from this push."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("stage", "check", "publish"))
    parser.add_argument("--revision")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        if args.command == "publish":
            result = publish(args.revision)
        elif args.command == "stage":
            if not args.revision or not args.output:
                raise ValueError("stage requires --revision and --output")
            manifest, size = stage(args.revision, Path(args.output))
            result = {"result": "staged", "source_revision": manifest["source_revision"], "input_version": manifest["input_version"], "bytes": size}
        else:
            if not args.output:
                raise ValueError("check requires --output")
            manifest, size = validate_site(Path(args.output))
            result = {"result": "valid", "source_revision": manifest["source_revision"], "bytes": size}
        print(json.dumps(result))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("PUBLICATION FAILED: " + str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

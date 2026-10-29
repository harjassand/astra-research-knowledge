"""Request-triggered refresh of a read-only, published Astra corpus.

No scheduler, scientist form, private database, scientific execution or credential
access. New data becomes visible only after the ordinary manifest checks pass.
"""
from __future__ import annotations

from collections import OrderedDict
from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import threading
import time
import urllib.request
import uuid

from knowledge.mcp_adapter import ResearchAdapter
from knowledge.model import digest, encoded

RELEASE_URL = "https://raw.githubusercontent.com/harjassand/astra-research-knowledge/main/knowledge/current/release.json"
RELEASE_SCHEMA = "astra.public-corpus-release.v1"
REPOSITORY_URL = "https://github.com/harjassand/astra-research-knowledge.git"
SOFTWARE = ("knowledge/model.py", "knowledge/build.py", "knowledge/retrieve.py",
            "knowledge/operations.py", "knowledge/agent_search.py", "knowledge/contextual_search.py", "knowledge/evidence.py",
            "knowledge/interfaces.py", "knowledge/mcp_adapter.py", "knowledge/published.py",
            "plugins/astra-research/server.py")


def read_release():
    # A mutable raw-main URL can remain in a CDN cache after a merge. Resolve
    # the tiny public Git ref, then read the marker at that immutable revision.
    try:
        ref = subprocess.run(["git", "ls-remote", REPOSITORY_URL, "refs/heads/main"],
            text=True, capture_output=True, timeout=12, check=True).stdout.split()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        raise ValueError("Cannot check the published main revision") from error
    if len(ref) != 2 or ref[1] != "refs/heads/main" or not re.fullmatch(r"[0-9a-f]{40}", ref[0]):
        raise ValueError("Invalid public main revision")
    url = RELEASE_URL.replace("/main/", "/" + ref[0] + "/")
    request = urllib.request.Request(url, headers={
        "User-Agent": "Astra-published-corpus/1", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(request, timeout=10) as response:
        if response.geturl().split("/", 3)[:3] != RELEASE_URL.split("/", 3)[:3]:
            raise ValueError("Unexpected published-release host")
        raw = response.read(8193)
    if len(raw) > 8192:
        raise ValueError("Published release exceeds its small metadata budget")
    value = json.loads(raw)
    value["published_revision"] = ref[0]
    return value


def release_version(value):
    if (not isinstance(value, dict) or value.get("schema") != RELEASE_SCHEMA
            or not re.fullmatch(r"[0-9a-f]{64}", str(value.get("input_version", "")))):
        raise ValueError("Invalid published corpus release")
    return value["input_version"]


class GitSnapshots:
    """Sparse immutable worktrees; Git refs preserve every served source version."""
    def __init__(self, root, cache, software=None, repository_url=REPOSITORY_URL):
        self.root, self.cache = Path(root).resolve(), Path(cache).resolve()
        self.cache.mkdir(parents=True, exist_ok=True)
        self.registry_path = self.cache / "served-versions.json"
        self.versions = json.loads(self.registry_path.read_bytes()) if self.registry_path.exists() else {}
        normalize = lambda url: url.replace("git@github.com:", "https://github.com/").rstrip("/").removesuffix(".git")
        if normalize(self.git(self.root, "remote", "get-url", "origin")) != normalize(repository_url):
            raise ValueError("Published snapshot origin must be the configured Astra repository")
        code_root = Path(__file__).resolve().parents[1]
        self.software = ({name: digest((code_root / name).read_bytes()) for name in SOFTWARE}
                         if software is None else software)

    @contextmanager
    def transaction(self):
        # Native and remote MCP processes may share this cache. Serialize their
        # Git/worktree/registry changes without creating a background worker.
        with (self.cache / "refresh.lock").open("a+b") as stream:
            if stream.tell() == 0:
                stream.write(b"0"); stream.flush()
            stream.seek(0)
            deadline = time.monotonic() + 10
            while True:
                try:
                    if os.name == "nt":
                        import msvcrt
                        msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl
                        fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError as error:
                    if time.monotonic() >= deadline:
                        raise ValueError("Published snapshot cache is busy; retry the request") from error
                    time.sleep(0.05)
            try:
                self.versions = json.loads(self.registry_path.read_bytes()) if self.registry_path.exists() else {}
                yield
            finally:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

    def git(self, root, *args, input=None, binary=False):
        # A cold sparse materialization can touch many thousands of files.
        # Keep network/metadata operations bounded separately from that work.
        command = args[2] if args[:2] == ("-c", "fetch.negotiationAlgorithm=noop") else args[0]
        budget = 120 if command in ("checkout", "checkout-index") else 45
        try:
            result = subprocess.run(["git", "-C", str(root), *args], input=input,
                                    text=not binary, capture_output=True, timeout=budget, check=True)
        except subprocess.TimeoutExpired as error:
            raise ValueError("Published Git operation timed out: " + command
                             + " (budget " + str(budget) + " seconds)") from error
        except subprocess.CalledProcessError as error:
            # Git can include host paths in stderr. Keep tool errors portable.
            raise ValueError("Published Git operation failed: " + command
                             + " (exit " + str(error.returncode) + ")") from error
        return result.stdout if binary else result.stdout.strip()

    def materialized(self, path, revision, version):
        """HEAD alone is set even by worktree add --no-checkout."""
        marker = Path(path) / "knowledge/current/manifest.json"
        try:
            return (marker.is_file() and json.loads(marker.read_bytes()).get("input_version") == version
                    # The full index includes deliberately unmaterialized
                    # promisor blobs. Verify its exact tree without fetching
                    # every unrelated historical object. Finished selected
                    # bytes are independently checked by ResearchAdapter.
                    and self.git(path, "write-tree", "--missing-ok")
                    == self.git(path, "rev-parse", revision + "^{tree}"))
        except (OSError, ValueError):
            return False

    def quarantine(self, path, revision):
        """Preserve an owned,unpublished partial copy without force or deletion."""
        path = Path(path).resolve()
        if (path.parent != self.cache or path == self.root
                or not (path.name == revision or path.name.startswith(".staging-" + revision + "-"))
                or self.git(path, "rev-parse", "HEAD") != revision):
            raise ValueError("Cannot quarantine a snapshot outside owned staging")
        common = lambda p: (Path(p) if Path(p).is_absolute() else path / p).resolve()
        source_common = self.git(self.root, "rev-parse", "--git-common-dir")
        source_common = (Path(source_common) if Path(source_common).is_absolute() else self.root / source_common).resolve()
        if common(self.git(path, "rev-parse", "--git-common-dir")) != source_common:
            raise ValueError("Cannot quarantine an unrelated Git checkout")
        folder = self.cache / "failed-staging"
        folder.mkdir(exist_ok=True)
        target = folder / (revision + "-" + uuid.uuid4().hex[:12])
        self.git(self.root, "worktree", "move", str(path), str(target))
        return target

    def remember(self, adapter, owned=False):
        try:
            self.git(self.root, "merge-base", "--is-ancestor", adapter.revision, "origin/main")
        except ValueError as error:
            raise ValueError("Serve only snapshots from published main history; fetch main before deployment") from error
        name = "refs/astra/served/" + adapter.version
        known = self.versions.get(adapter.version)
        if known:
            if self.git(self.root, "rev-parse", "--verify", name) != known["revision"]:
                raise ValueError("Retained corpus revision binding changed")
            # Equal inputs can occur at several published Git revisions. Their
            # payloads contain pinned URLs, so a served handle must keep its
            # first binding even when another server bootstraps at a later one.
            return
        try:
            bound = self.git(self.root, "rev-parse", "--verify", name)
        except ValueError:
            bound = None
        if bound:
            manifest = json.loads(self.git(self.root, "show", bound + ":knowledge/current/manifest.json"))
            if manifest.get("input_version") != adapter.version:
                raise ValueError("Retained corpus ref has a different input identity")
            path = adapter.root if bound == adapter.revision else self.cache / bound
            self.versions[adapter.version] = {"revision": bound,
                "path": str(path), "owned": owned if bound == adapter.revision else True}
        else:
            self.versions[adapter.version] = {"revision": adapter.revision,
                "path": str(adapter.root), "owned": owned}
            self.git(self.root, "update-ref", name, adapter.revision, "")
        with tempfile.NamedTemporaryFile(dir=self.cache, delete=False) as stream:
            stream.write(encoded(self.versions)); temporary = Path(stream.name)
        temporary.replace(self.registry_path)

    def stage(self, version, historical=False):
        known = self.versions.get(version)
        if known:
            revision = known["revision"]
            prior = Path(known["path"])
            if prior.exists():
                if self.git(prior, "rev-parse", "HEAD") != revision:
                    raise ValueError("Retained snapshot revision changed")
                if not self.materialized(prior, revision, version):
                    raise ValueError("Retained snapshot is incomplete or its index changed; preserve it and restore its original supported bytes")
                if historical:
                    return prior
        else:
            if historical:
                raise ValueError("Unknown historical corpus version; search the current corpus")
            self.git(self.root, "fetch", "--no-tags", "origin", "main")
            revision = self.git(self.root, "rev-parse", "FETCH_HEAD")
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Invalid published Git revision")
        manifest = json.loads(self.git(self.root, "show", revision + ":knowledge/current/manifest.json"))
        if manifest.get("input_version") != version:
            raise ValueError("Published release/main changed during refresh; retry with the new release")
        if not historical:
            marker = json.loads(self.git(self.root, "show", revision + ":knowledge/current/release.json"))
            if release_version(marker) != version:
                raise ValueError("Published release does not match its committed manifest")
            if any(manifest["inputs"].get(name) != expected for name, expected in self.software.items()):
                raise ValueError("Published runtime code changed; deploy the reviewed server before serving this release")
        if known and prior.exists():
            return prior
        target = self.cache / revision
        if target.exists():
            if self.git(target, "rev-parse", "HEAD") != revision:
                raise ValueError("Snapshot cache path is occupied by a different revision")
            if self.materialized(target, revision, version):
                return target
            # Recover the exact failure left by an interrupted older stager.
            # This version was never registered/served. Keep all bytes/index
            # evidence,then retry at a fresh path rather than reuse partial data.
            if known:
                raise ValueError("Retained snapshot is incomplete; no replacement is silently published")
            if any(p.name != ".git" for p in target.iterdir()):
                raise ValueError("Unregistered incomplete cache contains files; preserve it for inspection before retrying")
            self.quarantine(target, revision)
        required = set(manifest["inputs"]) | set(manifest["outputs"]) | {"knowledge/current/manifest.json"}
        paths = required | {"knowledge/mcp_adapter.py", "knowledge/published.py",
            "plugins/astra-research/server.py", ".gitignore"}
        for name in sorted(paths):
            parsed = PurePosixPath(name)
            if (parsed.is_absolute() or ".." in parsed.parts or ".git" in parsed.parts
                    or any(ord(c) < 32 for c in name)):
                raise ValueError("Nonportable path in published manifest")
        staging = self.cache / (".staging-" + revision + "-" + uuid.uuid4().hex[:12])
        self.git(self.root, "worktree", "add", "--detach", "--no-checkout", str(staging), revision)
        try:
            # Keep the complete committed index, but materialize only exact
            # manifest paths. NUL streams preserve whitespace, metacharacters
            # and unselected non-UTF8 names without glob matching every path.
            self.git(staging, "read-tree", "--no-sparse-checkout", revision)
            entries = self.git(staging, "ls-files", "--stage", "-z", binary=True)
            modes, blobs = {}, {}
            for entry in entries.split(b"\0"):
                if entry:
                    header, name = entry.split(b"\t", 1)
                    mode, blob, index_stage = header.split()
                    if index_stage != b"0":
                        raise ValueError("Published index contains an unresolved entry")
                    modes[name] = mode
                    blobs[name] = blob
            members = set(modes)
            tracked = b"\0".join(sorted(members)) + b"\0"
            if not {name.encode("utf-8") for name in required} <= members:
                raise ValueError("Required published manifest paths are absent from its committed tree")
            selected = b"\0".join(sorted(name.encode("utf-8") for name in paths
                                        if name.encode("utf-8") in members)) + b"\0"
            self.git(staging, "update-index", "--skip-worktree", "-z", "--stdin", input=tracked, binary=True)
            self.git(staging, "update-index", "--no-skip-worktree", "-z", "--stdin", input=selected, binary=True)
            reused = self.reuse_files(staging, revision, manifest, modes)
            remaining = [name for name in selected.split(b"\0") if name and name not in reused]
            if remaining:
                self.prefetch_blobs(staging, {blobs[name] for name in remaining})
                pending = b"\0".join(remaining) + b"\0"
                self.git(staging, "checkout-index", "-z", "--stdin", input=pending, binary=True)
            # Reused independent files have no checkout-created index stat
            # cache. Refresh it while staging is private, so later read-only
            # diff checks do not resolve promised blobs one at a time (or hit
            # the observed Git2.50 cold-index failure). No content is staged.
            self.git(staging, "update-index", "--refresh")
            if not self.materialized(staging, revision, version):
                raise ValueError("Sparse snapshot did not materialize its committed manifest and index")
            self.git(self.root, "worktree", "move", str(staging), str(target))
        except ValueError as error:
            # Never expose this directory as the revision cache. Preserve even
            # partial/untracked data for diagnosis; no force/reset/source copy.
            try:
                if staging.exists():
                    self.quarantine(staging, revision)
            except ValueError:
                raise ValueError(str(error) + "; incomplete owned staging retained; quarantine could not finish") from error
            raise ValueError(str(error) + "; incomplete owned staging retained for diagnosis; retry the request") from error
        return target

    def prefetch_blobs(self, staging, objects):
        """Fetch only absent selected blobs together in a partial clone.

        checkout-index faults missing objects in individually. A normal full
        clone hid this cost in an earlier benchmark. Inventory explicitly
        without lazy fetching, then use the already validated origin once.
        No ref, FETCH_HEAD, filter configuration, old file or history changes.
        """
        if not objects:
            return
        if any(not re.fullmatch(rb"[0-9a-f]{40}", oid) for oid in objects):
            raise ValueError("Invalid selected published blob identity")
        requested = b"\n".join(sorted(objects)) + b"\n"

        def missing():
            lines = self.git(staging, "rev-list", "--objects", "--missing=print",
                             "--no-object-names", "--stdin", input=requested, binary=True).splitlines()
            if {line.removeprefix(b"?") for line in lines} != objects:
                raise ValueError("Unexpected published blob inventory")
            return {line[1:] for line in lines if line.startswith(b"?")}

        absent = missing()
        if not absent:
            return
        # A corrupt ordinary clone is not silently repaired as a partial one.
        if self.git(staging, "config", "--bool", "--get", "remote.origin.promisor") != "true":
            raise ValueError("Selected published blobs are missing outside a promisor clone")
        # Match Git's own promisor fetch: negotiate no commit graph for direct
        # blob wants. Ordinary negotiation can fail with promised old blobs in
        # an otherwise valid shallow clone. This is a per-command option only.
        self.git(staging, "-c", "fetch.negotiationAlgorithm=noop", "fetch", "origin",
                 "--no-tags", "--no-write-fetch-head",
                 "--no-auto-maintenance", "--recurse-submodules=no", "--filter=blob:none",
                 "--stdin", input=b"\n".join(sorted(absent)) + b"\n", binary=True)
        if missing():
            raise ValueError("Selected published blobs remain missing after batch fetch")

    def reuse_files(self, staging, revision, manifest, modes):
        """Copy unchanged committed bytes, never hardlink mutable worktrees.

        New/changed paths still use Git. Every reused stream is checked against
        the new manifest; ResearchAdapter validates the entire finished snapshot
        before any active reader can switch. No source or prior snapshot changes.
        """
        previous = json.loads(self.git(self.root, "show", "HEAD:knowledge/current/manifest.json"))
        prior = previous["inputs"] | previous["outputs"]
        expected = manifest["inputs"] | manifest["outputs"]
        changed = set(self.git(self.root, "diff", "--name-only", "-z", "--no-renames", "HEAD", revision,
                               "--", binary=True).split(b"\0"))
        reused = set()
        directories = {staging}
        source_directories = {self.root}
        try:
            for name, checksum in sorted(expected.items()):
                raw_name = name.encode("utf-8")
                if (raw_name in changed or raw_name not in modes or prior.get(name) != checksum
                        or modes[raw_name] not in (b"100644", b"100755")):
                    continue
                source = self.root / name
                if source.parent not in source_directories:
                    if source.parent.resolve() != source.parent:
                        continue
                    source_directories.add(source.parent)
                try:
                    source_stat = source.lstat()
                except FileNotFoundError:
                    continue
                if not stat.S_ISREG(source_stat.st_mode):
                    continue
                target = staging / name
                if target.parent not in directories:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    directories.add(target.parent)
                # Independent files preserve history even if either working
                # copy is later edited. Stream validation avoids trusting cache
                # timestamps, sizes, path identity or an unverified old byte.
                observed = hashlib.sha256()
                with source.open("rb") as original, target.open("xb") as output:
                    while chunk := original.read(1024 * 1024):
                        output.write(chunk)
                        observed.update(chunk)
                if observed.hexdigest() != checksum:
                    raise ValueError("Cached snapshot bytes differ from the committed source; preserve and repair them")
                target.chmod(0o755 if modes[raw_name] == b"100755" else 0o644)
                reused.add(raw_name)
        except OSError as error:
            raise ValueError("Published snapshot copy failed; incomplete owned staging retained") from error
        return reused

    def prune(self, retained):
        retained = {Path(path).resolve() for path in retained} | {self.root}
        removed = set()
        for entry in self.versions.values():
            path = Path(entry["path"])
            if (not entry["owned"] or not path.exists() or path.resolve() in retained
                    or path.parent.resolve() != self.cache or path.name != entry["revision"]):
                continue
            if path in removed or self.git(path, "status", "--porcelain"):
                continue
            # No force/removal of edited files. The permanent served-version Git
            # ref and registry retain exact reconstruction and public citations.
            self.git(self.root, "worktree", "remove", str(path)); removed.add(path)


class PublishedAdapter:
    def __init__(self, root, method="portable", page_bytes=24000, cache=None,
                 poll_seconds=30, adapter_factory=None, release_reader=None,
                 snapshots=None, clock=None):
        if not 0 <= poll_seconds <= 300:
            raise ValueError("Published poll interval must be in 0..300 seconds")
        self.factory = adapter_factory or (lambda path: ResearchAdapter(path, method, page_bytes))
        self.active = self.factory(Path(root).resolve())
        self.snapshots = snapshots or GitSnapshots(root, cache or (Path(root).resolve().parent / ".astra-published-cache"))
        self.transaction = getattr(self.snapshots, "transaction", nullcontext)
        with self.transaction():
            self.snapshots.remember(self.active, owned=False)
            canonical = self.snapshots.stage(self.active.version, historical=True)
            if Path(canonical).resolve() != self.active.root:
                self.active = self.factory(canonical)
        self.adapters = OrderedDict([(self.active.version, self.active)])
        self.read_release = release_reader or read_release
        self.clock, self.poll_seconds = clock or time.monotonic, poll_seconds
        self.last_check = None
        self.checked_at = None
        self.expected = None
        self.published_revision = None
        self.lock = threading.RLock()

    def refresh(self):
        now = self.clock()
        started = datetime.now(timezone.utc).isoformat()
        try:
            if not self.active.root.exists():
                # Another process may have evicted this clean cache copy. Its
                # version/ref survives; never read a partly replaced directory.
                self.active = self.factory(self.snapshots.stage(self.active.version, historical=True))
                self.adapters[self.active.version] = self.active
            if self.last_check is not None and now - self.last_check < self.poll_seconds:
                return
            release = self.read_release()
            self.expected = release_version(release)
            self.published_revision = release.get("published_revision")
            if self.expected != self.active.version:
                candidate_root = self.snapshots.stage(self.expected)
                candidate = self.factory(candidate_root)
                if candidate.version != self.expected:
                    raise ValueError("Validated snapshot differs from the published input version")
                self.snapshots.remember(candidate, owned=True)
                self.active = candidate
                self.adapters[candidate.version] = candidate
            else:
                self.active.current()
        except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
            self.last_check = None
            self.checked_at = datetime.now(timezone.utc).isoformat()
            # No old result is returned as current when checking/staging fails.
            raise ValueError(json.dumps({"status": "published_refresh_failed",
                "served_input_version": self.active.version, "published_input_version": self.expected,
                "published_revision": self.published_revision,
                "checked_at": self.checked_at, "blocker": str(error),
                "action": "Retry if owned staging was interrupted; otherwise restore published-source support/access or deploy the reviewed runtime as the blocker requires. The prior snapshot is retained; it is not certified current."})) from error
        self.last_check = now
        self.checked_at = started

    def finish(self, value, adapter):
        historical = adapter.version != self.active.version
        metadata = value["metadata"]
        metadata["freshness"] = {"status": "historical_snapshot" if historical else "current",
            "published_input_version": self.expected, "current_input_version": self.active.version,
            "published_revision": self.published_revision,
            "current_revision": self.active.revision, "checked_at": self.checked_at,
            "check_interval_seconds": self.poll_seconds,
            "check_age_seconds_at_response": round(max(0, self.clock() - self.last_check), 3),
            "scope": "Published input version matched at checked_at; cached checks expire between requests, while network/validation costs remain visible in check age. No scheduled process. Historical conditions/corrections are then-current only; fetch the named current contexts before reuse."}
        if historical:
            current_contexts = []
            parts = value["id"].split(":")
            if parts[2] in ("record", "current", "history"):
                identifiers = [parts[3]]
            else:
                ref = adapter.references.get(parts[3])
                # An original can first acquire a correction/citing record in
                # a later intake. Keep its old payload, but also name current
                # contexts for that exact artifact identity, never another hash.
                key = (ref["path"], ref["sha256"]) if ref else None
                identifiers = sorted(set(adapter.contexts.get(key, [])) |
                                     set(self.active.contexts.get(key, []))) if ref else []
            for identifier in identifiers:
                if identifier in self.active.library.records:
                    current_contexts.append(self.active.handle("current", identifier))
            metadata["freshness"]["required_current_context_ids"] = current_contexts
        self.adapters.move_to_end(adapter.version)
        self.adapters.move_to_end(self.active.version)
        while len(self.adapters) > 2:
            self.adapters.popitem(last=False)
        try:
            self.snapshots.prune([a.root for a in self.adapters.values()])
        except (OSError, ValueError) as error:
            metadata["freshness"]["cache_cleanup_blocker"] = str(error)
        return value

    def search(self, query):
        with self.lock, self.transaction():
            self.refresh()
            return self.finish(self.active.search(query), self.active)

    def fetch(self, identifier):
        with self.lock, self.transaction():
            if isinstance(identifier, str) and not identifier.startswith("astra:"):
                # Preserve the existing direct-current-ID route. Only explicit
                # version handles may select a historical snapshot.
                self.refresh()
                return self.finish(self.active.fetch(identifier), self.active)
            parts = identifier.split(":") if isinstance(identifier, str) else []
            if len(parts) not in (4, 5) or parts[0] != "astra" or not re.fullmatch(r"[0-9a-f]{64}", parts[1]):
                raise ValueError("Invalid version-bound Astra handle")
            version = parts[1]
            if version != self.active.version and version not in self.adapters:
                # A handle may have come from another, newer server process.
                # Check an unknown version before labelling it old. A retained
                # historical continuation follows the ordinary30-second TTL;
                # it must not force another network check on every page.
                self.last_check = None
            self.refresh()
            adapter = self.adapters.get(version)
            if adapter is None or not adapter.root.exists():
                adapter = self.factory(self.snapshots.stage(version, historical=True))
                if adapter.version != version:
                    raise ValueError("Historical handle cannot resolve to a different corpus")
                self.adapters[version] = adapter
            return self.finish(adapter.fetch(identifier), adapter)

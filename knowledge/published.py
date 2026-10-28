"""Request-triggered refresh of a read-only, published Astra corpus.

No scheduler, scientist form, private database, scientific execution or credential
access. New data becomes visible only after the ordinary manifest checks pass.
"""
from __future__ import annotations

from collections import OrderedDict
from contextlib import contextmanager, nullcontext
from datetime import datetime, timezone
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile
import threading
import time
import urllib.request

from knowledge.mcp_adapter import ResearchAdapter
from knowledge.model import digest, encoded

RELEASE_URL = "https://raw.githubusercontent.com/harjassand/astra-research-knowledge/main/knowledge/current/release.json"
RELEASE_SCHEMA = "astra.public-corpus-release.v1"
REPOSITORY_URL = "https://github.com/harjassand/astra-research-knowledge.git"
SOFTWARE = ("knowledge/model.py", "knowledge/build.py", "knowledge/retrieve.py",
            "knowledge/operations.py", "knowledge/agent_search.py", "knowledge/evidence.py",
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

    def git(self, root, *args, input=None):
        try:
            result = subprocess.run(["git", "-C", str(root), *args], input=input,
                                    text=True, capture_output=True, timeout=45, check=True)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            # Git can include host paths in stderr. Keep tool errors portable.
            raise ValueError("Published Git operation failed: " + args[0]) from error
        return result.stdout.strip()

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
        target = self.cache / revision
        if target.exists():
            if self.git(target, "rev-parse", "HEAD") != revision:
                raise ValueError("Snapshot cache path is occupied by a different revision")
            return target
        paths = set(manifest["inputs"]) | set(manifest["outputs"]) | {
            "knowledge/current/manifest.json", "knowledge/mcp_adapter.py", "knowledge/published.py",
            "plugins/astra-research/server.py", ".gitignore"}
        patterns = []
        for name in sorted(paths):
            parsed = PurePosixPath(name)
            if (parsed.is_absolute() or ".." in parsed.parts or ".git" in parsed.parts
                    or any(ord(c) < 32 for c in name)):
                raise ValueError("Nonportable path in published manifest")
            patterns.append("/" + re.sub(r"([\\*?\[\]])", r"\\\1", name))
        self.git(self.root, "worktree", "add", "--detach", "--no-checkout", str(target), revision)
        try:
            self.git(target, "sparse-checkout", "set", "--no-cone", "--stdin", input="\n".join(patterns) + "\n")
            self.git(target, "checkout", "--detach", revision)
        except ValueError:
            # Only this newly created, unpublished cache is eligible for cleanup.
            try:
                self.git(self.root, "worktree", "remove", str(target))
            except ValueError:
                pass
            raise
        return target

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
                "action": "Restore published-source access or deploy the reviewed runtime, then retry. The prior snapshot is retained; it is not certified current."})) from error
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
                identifiers = sorted(adapter.contexts.get((ref["path"], ref["sha256"]), [])) if ref else []
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
            if version != self.active.version:
                # A handle may have come from another, newer server process.
                # Resolve current correction context before labelling it old.
                self.last_check = None
            self.refresh()
            adapter = self.adapters.get(version)
            if adapter is None or not adapter.root.exists():
                adapter = self.factory(self.snapshots.stage(version, historical=True))
                if adapter.version != version:
                    raise ValueError("Historical handle cannot resolve to a different corpus")
                self.adapters[version] = adapter
            return self.finish(adapter.fetch(identifier), adapter)

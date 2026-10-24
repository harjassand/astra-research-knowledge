"""Acquire reproducible software and a primary-source molecular benchmark."""
import hashlib
import json
from pathlib import Path
import subprocess
import time
import urllib.request

BASE = Path(__file__).resolve().parent
BASE.mkdir(parents=True, exist_ok=True)
PYTHON = "/Users/harjas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"


def fetch(url, name):
    t0 = time.perf_counter()
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    path = BASE / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return dict(url=url, path=str(path), bytes=len(data),
                sha256=hashlib.sha256(data).hexdigest(),
                wall_seconds=time.perf_counter()-t0)


def run(args, name):
    t0 = time.perf_counter()
    result = subprocess.run(args, capture_output=True, text=True)
    (BASE/name).write_text(result.stdout+result.stderr)
    receipt = dict(args=args, returncode=result.returncode,
                   wall_seconds=time.perf_counter()-t0, log=str(BASE/name))
    if result.returncode:
        print(json.dumps(receipt), flush=True)
        raise RuntimeError(receipt)
    return receipt


def main():
    receipts = []
    receipts.append(fetch("https://api.github.com/repos/block-hczhai/block2-preview/git/trees/master?recursive=1", "source/block2_tree.json"))
    tree=json.loads((BASE/"source/block2_tree.json").read_text())
    print(json.dumps(dict(tree_sha=tree.get("sha"), candidates=[x for x in tree.get("tree",[]) if "fcidump" in x["path"].lower() or ("h2o" in x["path"].lower() and x.get("size",0)<1000000)])), flush=True)
    venv=BASE/".venv"
    if not venv.exists():
        receipts.append(run([PYTHON,"-m","venv",str(venv)],"venv_setup.txt"))
    wheels=BASE/"wheels"
    wheels.mkdir(exist_ok=True)
    receipts.append(run([str(venv/"bin/python"),"-m","pip","download","--only-binary=:all:","--dest",str(wheels),"pyscf==2.14.0"],"pip_download.txt"))
    receipts.append(dict(wheel_artifacts=[dict(name=p.name, bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in wheels.iterdir()]))
    receipts.append(run([str(venv/"bin/python"),"-m","pip","install","--no-index","--find-links",str(wheels),"pyscf==2.14.0"],"pip_install.txt"))
    (BASE/"ACQUISITION.json").write_text(json.dumps(receipts,indent=2))
    print(json.dumps(receipts),flush=True)


if __name__ == "__main__":
    main()

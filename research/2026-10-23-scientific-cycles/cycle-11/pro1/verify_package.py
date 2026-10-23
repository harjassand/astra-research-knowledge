#!/usr/bin/env python3
"""Source integrity only. No old or new scientific suite is automatically run."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
PREV="2337488bcda1a996e3a2779e5b8a826513c3db80f27d13d825cf04f6dc1c5440"

def expand(path,seen=()):
    path=Path(path)
    if path in seen: raise ValueError("cyclic TeX input")
    text=(ROOT/path).read_text()
    def replace(match):
        sub=Path(match.group(1))
        if sub.is_absolute() or ".." in sub.parts: raise ValueError("unsafe TeX input")
        if not sub.suffix: sub=sub.with_suffix(".tex")
        return "% BEGIN INCLUDED: "+str(sub)+"\n"+expand(sub,seen+(path,))+"\n% END INCLUDED: "+str(sub)+"\n"
    return re.sub(r"\\input\{([^}]+)\}",replace,text)

def main():
    manifest=ROOT/"MANIFEST.sha256"
    count=0
    for line in manifest.read_text().splitlines():
        expected,relative=line.split("  ",1)
        p=Path(relative)
        assert not p.is_absolute() and ".." not in p.parts
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==expected,relative
        count+=1
    prev=ROOT/"preserved/Astra_Amplification_Cycle10_PRO1_20261023.zip"
    assert prev.stat().st_size==6547665
    assert hashlib.sha256(prev.read_bytes()).hexdigest()==PREV
    for row in json.loads((ROOT/"evidence/INHERITED_DEPENDENCIES.json").read_text()):
        p=ROOT/row["path"];raw=p.read_bytes()
        assert len(raw)==row["bytes"] and hashlib.sha256(raw).hexdigest()==row["sha256"]
    expanded=expand("ENTROPY_DRIFT_AND_DEPTH_COST.tex")
    assert expanded.encode()==(ROOT/"COMPLETE_PROOF.tex.txt").read_bytes()
    combined=("# CYCLE11 COMPLETE NEW PROOF — recursive expansion\n\n"+expanded+
              "\n\n# UNCHANGED CYCLE10 COMPLETE PROOF — byte-identical body follows\n\n").encode()+(ROOT/"dependencies/cycle10/COMPLETE_PROOF.tex.txt").read_bytes()
    assert combined==(ROOT/"COMPLETE_SOURCE_PROOFS.txt").read_bytes()
    print(json.dumps({"status":"PASS_SOURCE_INTEGRITY","manifest_files_checked":count,
      "unchanged_predecessor_sha256":PREV,"selected_dependencies_checked":8,
      "merged_proof_exact":True,"scientific_replay_performed":False}))
if __name__=="__main__": main()

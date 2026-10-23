#!/usr/bin/env python3
"""Integrity verification only. Mathematical review requires reading the proof."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    checked=0
    for line in (ROOT/"MANIFEST.sha256").read_text().splitlines():
        digest,relative=line.split("  ",1)
        p=ROOT/relative
        assert p.is_file(),relative
        assert sha(p)==digest,relative
        checked+=1
    p=ROOT/"preserved/Astra_Amplification_Cycle8_PRO1_20261022.zip"
    assert p.stat().st_size==5315015
    assert sha(p)=="7b6e4d30b874601c4df8422ead96a3427c075c3091134363bbe5ba6c543f4aaa"
    review=json.loads((ROOT/"contributions/clipping_challenge/INTEGRATED_MANUSCRIPT_REVIEW.json").read_text())
    final=review["final_delta_review"]
    mainfile=ROOT/"SPECTRAL_CLIPPING_CAPACITY.tex"
    assert sha(mainfile)==final["source_sha256"]
    assert mainfile.stat().st_size==final["source_bytes"]
    comparison=ROOT/"representation/transfer_comparison.json"
    assert sha(comparison)==final["comparison_sha256"]
    print(json.dumps({"manifest_files_checked":checked,"predecessor_identity":"matched",
                      "final_review_binding":"matched","scope":"Integrity only; not scientific acceptance."},indent=2))
if __name__=="__main__":main()

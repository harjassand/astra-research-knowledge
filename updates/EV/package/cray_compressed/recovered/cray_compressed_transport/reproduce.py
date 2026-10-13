"""Regenerate exact bounds and finite diagnostics. No configuration graph."""
from __future__ import annotations
import json,platform,time
from pathlib import Path
import numpy as np
import test_research,test_balanced
from probability_certificate import evaluate as deterministic
from balanced_certificate import evaluate as balanced

ROOT=Path(__file__).resolve().parent

def write(name,content):
    (ROOT/name).write_text(json.dumps(content,indent=2)+'\n')

def main():
    start=time.perf_counter()
    write('probability_certificate.json',deterministic())
    t=time.perf_counter();new=balanced();new['evaluation_seconds']=time.perf_counter()-t
    write('balanced_certificate.json',new)
    first=test_research.run();write('test_results.json',first)
    second=test_balanced.run();write('balanced_tests.json',second)
    summary=dict(status='passed',python=platform.python_version(),numpy=np.__version__,
                 final_lower_endpoint=new['lower_endpoint'],
                 gate_lower=new['gate_lower'],
                 scalar_certificate_seconds=new['evaluation_seconds'],
                 total_seconds=time.perf_counter()-start,
                 caution='Finite tests and exact arithmetic do not replace independent review of the general proofs.')
    write('reproduction_summary.json',summary);print(json.dumps(summary,indent=2))

if __name__=='__main__':main()

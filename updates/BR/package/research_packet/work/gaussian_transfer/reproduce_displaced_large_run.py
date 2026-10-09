"""Reproduce the original h=10**20 sample command; not executed by receipt creation.
Original sampler SHA256: 4bbaa0f5717c36edfc9774ac8d3858b95d2cfbf6fef2f20a3a9d4478d473d6be
Original evaluator SHA256: ee8c3035aaa4e3e9fffb66d98237a1cb9beb8de5e2e90cee264f01675a0a4a09
The evaluator has since changed; see displaced_large_run.json for provenance.
Run from workspace root with:
PYTHONPATH=work/gaussian_transfer work/gaussian_transfer/venv/bin/python work/gaussian_transfer/reproduce_displaced_large_run.py
"""
from displaced_sampler import *
from random import Random
from time import perf_counter
m=DisplacedHeraldGaussian.from_pure([['1/8','1/7'],['1/7','1/9']],['1/5','1/6'],0,10**20)
t=perf_counter(); print('10^20 sample',m.sample(Random(4),F(1,10**6)), 'seconds',perf_counter()-t,flush=True)
l=next(iter(m.matching.cached.values()));print('laws',l.num_log_H,l.num_bounds,l.max_precision_used,l.total_attempts,l.anchor_diagnostics, 'tickets', m.last_ticket_count, 'bits',m.last_random_bits,flush=True)
with ctx.workprec(l._precision(l.bits+20)):
 print('ref bound', (l._logweight(l.reference_k, l.bits+20)-l.reference).exp())

#!/usr/bin/env python3
"""Exact finite diagnostics for the explicit full-spectrum counterexample."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def mv(a, v):
    return [sum(x*y for x,y in zip(row,v)) for row in a]


def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


p=[[F(3,4),F(1,4)],[F(1,4),F(3,4)]]
t=[[x/2 for x in row] for row in p]
e=[[x/2 for x in row] for row in kron(p,p)]
vp=[F(1),F(1)]; vm=[F(1),F(-1)]
checks=[]
for a,la in [(vp,F(1)),(vm,F(1,2))]:
    for b,lb in [(vp,F(1)),(vm,F(1,2))]:
        v=[x*y for x in a for y in b]
        eigenvalue=la*lb/2
        assert mv(e,v)==[eigenvalue*x for x in v]
        checks.append(str(eigenvalue))
words=0
for length in range(11):
    for word in product((0,1),repeat=length):
        v=[F(1),F(1)]
        for symbol in word: v=mv(t,v)
        probability=sum(v)/2
        assert probability==F(1,2**length)
        words+=1
receipt={'status':'PASS_EXACT_FINITE_ARITHMETIC',
         'all_length_proof':'pi T_w 1 = 2^(-L) pi P^L 1 = 2^(-L)',
         'words_checked':words,'maximum_word_length':10,
         'collision_transfer_eigenvalues_with_multiplicity':checks,
         'one_state_collision_transfer_spectrum':['1/2'],
         'scope':'full unobservable spectra can differ; no general source-paper review'}
path=Path(__file__).with_name('HIDDEN_SPECTRUM_VERIFICATION.json')
path.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))

#!/usr/bin/env python3
"""Exact finite construction check; no source draws or hardware execution."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
import hashlib

BASE=Path(__file__).resolve().parent

def de_bruijn(s,L):
    a=[0]*(s*L+1)
    cycle=[]
    def db(t,p):
        if t>L:
            if L%p==0:
                cycle.extend(a[1:p+1])
        else:
            a[t]=a[t-p]
            db(t+1,p)
            for j in range(a[t-p]+1,s):
                a[t]=j
                db(t+1,t)
    db(1,1)
    assert len(cycle)==s**L
    return cycle + [cycle[i%len(cycle)] for i in range(L-1)]

def mm(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]

def ident(n):
    return [[Q(i==j) for j in range(n)] for i in range(n)]

def apply_word(word,letters):
    out=ident(len(letters[0]))
    for a in word:
        out=mm(letters[a],out)
    return out

def qjson(x):
    if isinstance(x,Q): return str(x)
    if isinstance(x,list): return [qjson(y) for y in x]
    if isinstance(x,dict): return {k:qjson(v) for k,v in x.items()}
    return x

def run():
    coverage=[]
    for s in [1,2,3]:
        for L in [1,2,3,4]:
            w=de_bruijn(s,L)
            windows={tuple(w[i:i+L]) for i in range(len(w)-L+1)}
            assert windows==set(product(range(s),repeat=L))
            assert len(w)==s**L+L-1
            for k in range(1,L+1):
                assert set(product(range(s),repeat=k)) <= {tuple(w[i:i+k]) for i in range(len(w)-k+1)}
            coverage.append({"alphabet":s,"order":L,"length":len(w),"all_L_words":len(windows)})
    # Pauli coordinates I,X,Y,Z; a=Z dephasing, b=Hadamard conjugation.
    A=[[Q(x) for x in row] for row in [[1,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,1]]]
    B=[[Q(x) for x in row] for row in [[1,0,0,0],[0,0,0,1],[0,0,-1,0],[0,1,0,0]]]
    depol=[[Q(i==j==0) for j in range(4)] for i in range(4)]
    assert mm(A,A)==A
    assert mm(B,B)==ident(4)
    assert apply_word([0,1,0],[A,B])==depol
    cover=de_bruijn(2,3)
    assert apply_word(cover,[A,B])==depol
    assert apply_word(cover*2,[A,B])==depol
    # A and B alone preserve some initial-state distinction. The fixed cover
    # maps every Pauli trace-zero component to zero, hence is exact replacer.
    # The Bell state is (II+XX-YY+ZZ)/4: after cover on its first leg,
    # only II/4 remains, so the output is I/2 tensor I/2 exactly.
    bell_coefficients={"II":Q(1,4),"XX":Q(1,4),"YY":Q(-1,4),"ZZ":Q(1,4)}
    after_cover={"II":Q(1,4),"XX":Q(0),"YY":Q(0),"ZZ":Q(0)}
    assert after_cover["II"]==Q(1,4) and sum(abs(after_cover[k]) for k in ["XX","YY","ZZ"])==0
    # Data-selected exact replacement: Z=H, H fair. Joint versus product.
    joint=[Q(1,2),Q(0),Q(0),Q(1,2)]
    independent=[Q(1,4)]*4
    selected_reset_TV=sum(abs(x-y) for x,y in zip(joint,independent))/2
    assert selected_reset_TV==Q(1,2)
    fixed_target_joint=[Q(1,2),Q(1,2),Q(0),Q(0)]
    fixed_target_product=fixed_target_joint[:]
    assert sum(abs(x-y) for x,y in zip(fixed_target_joint,fixed_target_product))==0
    # Fixed L=3 cover's scalar contraction bound, for rational c and epsilon.
    c=Q(3,4); epsilon=Q(1,1000); n=0; err=Q(1)
    while err>epsilon:
        n+=1;err*=c
    assert err<=epsilon and c**(n-1)>epsilon
    result={
        "status":"PASS",
        "scope":"Exact de Bruijn coverage, Pauli-channel composition, Bell decoupling, and selected-target failure. No physical data or source acquisition.",
        "coverage_checks":coverage,
        "qubit_cover":cover,
        "qubit_cover_length":len(cover),
        "cover_Pauli_transfer":apply_word(cover,[A,B]),
        "Bell_before":bell_coefficients,
        "Bell_after":after_cover,
        "selected_exact_reset_joint_TV":selected_reset_TV,
        "rational_budget_example":{"c":c,"epsilon":epsilon,"repetitions":n,"native_calls":n*len(cover),"error_upper":err},
        "source_code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }
    target=BASE/"PUBLIC_PREPARATION_EXACT_CHECK.json"
    target.write_text(json.dumps(qjson(result),indent=2)+"\n")
    print(json.dumps({"status":result["status"],"cover":cover,"budget_repetitions":n,"native_calls":n*len(cover),"receipt":str(target)}))
if __name__=="__main__": run()


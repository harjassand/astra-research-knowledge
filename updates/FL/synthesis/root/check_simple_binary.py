"""Exact decoder, finite-bin acquisition, and multiplicity boundary checks."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
checks=[]
def check(name,ok):
    if not ok: raise AssertionError(name)
    checks.append(name)

def histogram(n,high,pl,ph):
    coefficients=[F(1)]
    for p in [ph]*high+[pl]*(n-high):
        nxt=[F(0)]*(len(coefficients)+1)
        for k,prob in enumerate(coefficients):
            nxt[k]+=prob*(1-p);nxt[k+1]+=prob*p
        coefficients=nxt
    return coefficients

def decoder(n,k,pl,ph):
    return ph**(n-k)*(-(1-ph))**k/(ph-pl)**n

for pl,ph in [(F(0),F(1)),(F(1,100),F(99,100)),(F(1,5),F(3,5)),(F(49,100),F(51,100))]:
    for n in range(1,9):
        for j in range(n+1):
            expectation=sum(p*decoder(n,k,pl,ph) for k,p in enumerate(histogram(n,j,pl,ph)))
            check('avoidance projection '+str((pl,ph,n,j)),expectation==int(j==0))

n,q=4,6
sets=list(combinations(range(q),n))
normalizer=sum(range(1,len(sets)+1))
law={tuple(ss):F(i+1,normalizer) for i,ss in enumerate(sets)}
pl,ph=F(1,100),F(99,100)
void={}
for bits in product((0,1),repeat=q):
    B=frozenset(j for j,v in enumerate(bits) if v)
    bins=[sum(mass*histogram(n,sum(j in B for j in ss),pl,ph)[k] for ss,mass in law.items()) for k in range(n+1)]
    void[B]=sum(p*decoder(n,k,pl,ph) for k,p in enumerate(bins))
    check('binary subset avoidance '+str(bits),void[B]==sum(mass for ss,mass in law.items() if not B.intersection(ss)))
recovered={}
for ss,mass in law.items():
    B=frozenset(set(range(q))-set(ss))
    recovered[ss]=void[B]
    check('one-mask-per-history recovery '+str(ss),void[B]==mass)
for size in range(q+1):
    for ss in combinations(range(q),size):
        outside=set(range(q))-set(ss)
        recovered_mass=sum((-1)**len(T)*void[frozenset(outside|set(T))] for k in range(len(ss)+1) for T in combinations(ss,k))
        check('occupied-set Mobius inversion '+str(ss),recovered_mass==law.get(ss,F(0)))

base=(0,1,5)
perms=list(permutations(base))
def inversion_parity(perm):
    return sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2
E=[p for p in perms if inversion_parity(p)==0]
O=[p for p in perms if inversion_parity(p)==1]
check('distinct multiset laws',set(E).isdisjoint(O) and len(E)==len(O)==3)
for mask in product((0,1),repeat=3):
    def count_law(bank):
        return [sum(histogram(6,sum(occ[j]*mask[j] for j in range(3)),pl,ph)[k] for occ in bank)/3 for k in range(7)]
    check('all-binary multiplicity countermodel '+str(mask),count_law(E)==count_law(O))
supportE=Counter(tuple(j for j,v in enumerate(p) if v) for p in E)
supportO=Counter(tuple(j for j,v in enumerate(p) if v) for p in O)
check('same support-set law in multiplicity counterexample',supportE==supportO)

receipt=dict(status='PASS',scope='Exact finite decoder and known-bin law checks; analytic ideal-limit theorem uses stated proof. No laboratory or efficient general tomography certification.',
             checks_passed=len(checks),checks=checks,p_low=str(pl),p_high=str(ph),n=n,q=q,
             histories=len(law),binary_masks_for_explicit_recovery=len(law),necessary_histogram_dimension_bound=4,
             R_bound=str((ph/(ph-pl))**n),law={str(k):str(v) for k,v in law.items()},
             multiplicity_counterexample=dict(even=E,odd=O,all8_binary_histograms_match=True,underlying_support_laws_match=True))
(OUT/'SIMPLE_BINARY_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ['status','checks_passed','histories','binary_masks_for_explicit_recovery','R_bound']},indent=2))

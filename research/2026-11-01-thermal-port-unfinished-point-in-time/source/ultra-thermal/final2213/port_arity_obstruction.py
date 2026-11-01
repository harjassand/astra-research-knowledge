"""Exact Pauli arithmetic for the matched-port arity obstruction.

This is a fixed-reference/selected-code obstruction, NOT an impossibility
theorem for general two-body autonomous quantum memories.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import numpy as np
from port_model import I,X,Y,Z,ten,word,comm

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/thermal_ports_20261101'
CHECKS=['XZZXI','IXZZX','XIXZZ','ZXIXZ']
TABLE={('X','Y'):(1j,'Z'),('Y','Z'):(1j,'X'),('Z','X'):(1j,'Y'),
       ('Y','X'):(-1j,'Z'),('Z','Y'):(-1j,'X'),('X','Z'):(-1j,'Y')}
def mul(a,b):
    phase=1;chars=[]
    for x,y in zip(a,b):
        if x=='I':chars.append(y)
        elif y=='I':chars.append(x)
        elif x==y:chars.append('I')
        else:
            p,z=TABLE[x,y];phase*=p;chars.append(z)
    return phase,''.join(chars)
def anticommute(a,b):return sum(x!='I' and y!='I' and x!=y for x,y in zip(a,b))%2==1
def weight(a):return sum(x!='I' for x in a)


def main():
    matrices=[word(x) for x in CHECKS];hd=sum((np.eye(32)-s)/2 for s in matrices)
    stab=[]
    for bits in itertools.product((0,1),repeat=4):
        phase=1;w='IIIII'
        for bit,c in zip(bits,CHECKS):
            if bit:
                p,w=mul(w,c);phase*=p
        stab.append((phase,w))
    assert all(weight(w)==4 for p,w in stab if w!='IIIII')
    rho=sum(p*word(w) for p,w in stab)/32
    faithful=[]
    for size in (1,2,3):
        for sites in itertools.combinations(range(5),size):
            rest=[i for i in range(5) if i not in sites]
            # Exact binary-rational partial traces; no spectral tolerance.
            reduced=np.zeros((2**size,2**size),complex)
            for i in range(2**size):
                for j in range(2**size):
                    for r in range(2**len(rest)):
                        ibits=[0]*5;jbits=[0]*5
                        for k,s in enumerate(sites):ibits[s]=(i>>(size-1-k))&1;jbits[s]=(j>>(size-1-k))&1
                        for k,s in enumerate(rest):ibits[s]=jbits[s]=(r>>(len(rest)-1-k))&1
                        a=sum(x<<(4-k) for k,x in enumerate(ibits));b=sum(x<<(4-k) for k,x in enumerate(jbits))
                        reduced[i,j]+=rho[a,b]
            assert np.array_equal(reduced,np.eye(2**size)/2**size)
            faithful.append({'sites':list(sites),'minimum_marginal_eigenvalue':str(Fraction(1,2**size))})
    seeds=['I'*i+p+'I'*(4-i) for i in range(5) for p in 'XYZ']
    images=[comm(hd,word(p)) for p in seeds]
    gram=np.array([[np.trace(a.conj().T@b) for b in images] for a in images])
    counts=[sum(anticommute(p,c) for c in CHECKS) for p in seeds]
    expected=np.diag([32*t for t in counts])
    assert np.array_equal(gram,expected)
    assert all(t>0 for t in counts)
    # Independent complete bilinear DATA/qubit-controller Gram fixture.
    hc=2*np.array([[0,0],[0,1]],complex);href=ten(hd,I)+ten(np.eye(32),hc)
    bs=[ten(word(p),c) for p in seeds for c in (X,Y,Z)]
    cs=[comm(href,b) for b in bs]
    fullgram=np.array([[np.trace(a.conj().T@b) for b in cs] for a in cs])
    full_expected=np.diag([64*(t+(4 if c in (0,1) else 0)) for t in counts for c in range(3)])
    assert np.array_equal(fullgram,full_expected)
    # Exact supports of the actual selected lowering operators; coefficients
    # are integer multiples of 1/2^t and fourth roots of unity.
    lowering=[]
    for seed in seeds:
        active=[c for c in CHECKS if anticommute(seed,c)];t=len(active)
        for omega in range(t%2,t+1,2):
            coeff={}
            for signs in itertools.product((-1,1),repeat=t):
                if sum(signs)!=-omega:continue
                for bits in itertools.product((0,1),repeat=t):
                    phase=1;w=seed;sgn=1
                    for bit,s,c in zip(bits,signs,active):
                        if bit:
                            p,w=mul(w,c);phase*=p;sgn*=s
                    coeff[w]=coeff.get(w,0)+phase*sgn
            coeff={w:z for w,z in coeff.items() if z!=0}
            support=[i for i in range(5) if any(w[i]!='I' for w in coeff)]
            if omega>0:assert len(support)>=4
            lowering.append({'seed':seed,'omega':omega,'data_support':support,
                             'Pauli_monomials':len(coeff),'largest_Pauli_weight':max(map(weight,coeff)),
                             'coefficient_denominator':2**t})
    out={'code':'[[5,1,3]] perfect-code fixture, not the 3D RX/RZ family',
         'nonidentity_stabilizer_weights':sorted(weight(w) for p,w in stab if w!='IIIII'),
         'faithful_marginals':faithful,
         'exact_data_commutator_Gram_diagonal':[int(x) for x in np.diag(expected)],
         'one_data_Pauli_commutator_rank':15,
         'exact_bilinear_controller_Gram_diagonal':[int(x) for x in np.diag(full_expected)],
         'bilinear_coupler_kernel_dimension':0,'port_supports':lowering,
         'conclusion':'No nonzero strictly energy-lowering operator on <=3 data sites for this code; individually matched ports require >=4 data sites. Moreover no sum of one-data-Pauli/controller interactions can preserve the full-rank product Gibbs reference for this code, even with arbitrary finite controller operators, under the Pauli-independence criterion proved in SELECTOR_OBSTRUCTION.txt.',
         'scope':'Exact fixed-reference/matched-port obstruction; not a generic two-body or three-body quantum-memory no-go, not a statement about the source 3D family all local checks',
         'program_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'model_sha256':hashlib.sha256((Path(__file__).parent/'port_model.py').read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True);path=OUT/'port_arity_obstruction.json';path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'passed':True,'output':str(path),'one_data_rank':15,'bilinear_kernel_dimension':0,
                      'positive_frequency_port_minimum_support':min(len(p['data_support']) for p in lowering if p['omega']>0)}))


if __name__=='__main__':main()

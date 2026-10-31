"""Supplemental independent signed/finite-rational coupling audit."""
import copy
import hashlib
import json
import random
from fractions import Fraction
from pathlib import Path
import numpy as np
from acquire_clifford_source import acquire
from acquire_pauli_coupling import acquire_coupling, expectation
from test_acquisition import unitary, pauli_matrix
from test_pauli_coupling import dense_terms


def run():
    rng=random.Random(908731)
    cases=checks=0;max_error=0.
    for n in range(1,5):
        for _ in range(8):
            prep=[]
            for __ in range(20):
                op=rng.choice(['H','S','SDG','X','Z']+(['CX','SWAP'] if n>1 else []))
                prep.append([op,*rng.sample(range(n),2 if op in ['CX','SWAP'] else 1)])
            p={'n':n,'env':n,'gates':[['SWAP',j,n+j] for j in range(n)]+prep}
            c=acquire(p)
            # Use the original intended preparation, not the synthesized one.
            psi=unitary(prep,n)[:,0]
            for x in range(1<<n):
                for z in range(1<<n):
                    mu=expectation(c['constant_state_stabilizers'],n,x,z)
                    actual=np.vdot(psi,pauli_matrix((x&z).bit_count()%4,x,z,n)@psi)
                    assert abs(mu-actual)<1e-10
                    checks+=1
            terms=[{'coefficient':str(Fraction(rng.randrange(-9,10),rng.randrange(1,11))),
                    'system_x':rng.randrange(4),'system_z':rng.randrange(4),
                    'source_x':rng.randrange(1<<n),'source_z':rng.randrange(1<<n)} for __ in range(40)]
            out=acquire_coupling(p,c,{'system_qubits':2,'terms':terms})
            k=dense_terms(out['original_terms'],2,n);kc=dense_terms(out['centered_terms'],2,n)
            mean=np.zeros((4,4),complex)
            for t in out['mean_terms']:
                x,z=t['system_x'],t['system_z']
                mean+=float(Fraction(t['coefficient']))*pauli_matrix((x&z).bit_count()%4,x,z,2)
            embed=np.kron(np.eye(4),psi[:,None])
            err=max(np.linalg.norm(embed.conj().T@k@embed-mean),np.linalg.norm(k-kc-np.kron(mean,np.eye(1<<n))),np.linalg.norm(embed.conj().T@kc@embed))
            assert err<1e-10;max_error=max(max_error,float(err));cases+=1
    p={'n':1,'env':1,'gates':[['SWAP',0,1],['X',0]]};c=acquire(p)
    base={'coefficient':'1','system_x':0,'system_z':0,'source_x':0,'source_z':1}
    huge=Fraction((1<<521)+1,(1<<257)+3)
    # Huge exact opposite coefficients vanish BEFORE any numerical arithmetic.
    spec={'system_qubits':1,'terms':[dict(base,coefficient=str(huge)),dict(base,coefficient=str(-huge)),dict(base,coefficient='7/11')]}
    out=acquire_coupling(p,c,spec)
    assert out['scalar_mean']=='-7/11' and out['nontrivial_mean_lcu_bound']=='0'
    assert out['physical_mean_commutator_is_zero'] is True
    assert out['centered_lcu_bound']=='14/11'
    nontrivial=copy.deepcopy(spec)
    for term in nontrivial['terms']:term['system_z']=1
    nontrivial_out=acquire_coupling(p,c,nontrivial)
    assert nontrivial_out['physical_mean_commutator_is_zero'] is False
    assert nontrivial_out['nontrivial_mean_lcu_bound']=='7/11'
    empty=acquire_coupling(p,c,{'system_qubits':1,'terms':[]})
    assert empty['original_lcu_bound']==empty['mean_lcu_bound']==empty['centered_lcu_bound']=='0'
    invalid=[]
    for value in [True,False,1.,float('inf'),'1/0','1/-2',' 1/2','1e3','1/2/3','nan','',[],{}]:
        bad=copy.deepcopy(spec);bad['terms'][0]['coefficient']=value;invalid.append(bad)
    for key in ['system_x','system_z','source_x','source_z']:
        for value in [-1,2,True,1.,None]:
            bad=copy.deepcopy(spec);bad['terms'][0][key]=value;invalid.append(bad)
    invalid += [None,[],{'system_qubits':0,'terms':[]},{'system_qubits':1,'terms':[{}]}]
    for bad in invalid:
        try:acquire_coupling(p,c,bad)
        except ValueError:continue
        raise AssertionError('Malformed specification accepted')
    root=Path(__file__).parent
    result={'source_sha256':hashlib.sha256((root/'acquire_pauli_coupling.py').read_bytes()).hexdigest(),
            'random_source_cases':cases,'signed_expectations':checks,'dense_centering_cases':cases,
            'maximum_dense_error':max_error,'large_exact_rational_cancellation':True,
            'scalar_negative_mean_preserved':True,'empty_zero_list':True,
            'malformed_specifications_rejected':len(invalid),'passed':True}
    path=root/'pauli_independent_adversarial_checks.json'
    path.write_text(json.dumps(result,indent=2)+'\n');print(path.read_text())


if __name__=='__main__':run()

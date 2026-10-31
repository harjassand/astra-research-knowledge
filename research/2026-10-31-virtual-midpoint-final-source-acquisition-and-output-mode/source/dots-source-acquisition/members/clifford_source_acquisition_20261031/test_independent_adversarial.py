"""Independent supplemental audit; dense helpers only in tests, never finder.

Records discovered verifier failures without hiding their original reproducer.
"""
import copy
import hashlib
import json
import random
from pathlib import Path
import numpy as np
from acquire_clifford_source import acquire, verify, conjugate, validate
from test_acquisition import dense_check, unitary, pauli_matrix


def run():
    root = Path(__file__).parent
    rng = random.Random(830176)
    counts = {}
    # Exhaustive single-gate conjugation, including all Y phases and CX order.
    gates = [[o, i] for o in ['H','S','SDG','X','Z'] for i in range(3)]
    gates += [[o,i,j] for o in ['CX','SWAP'] for i in range(3) for j in range(3) if i != j]
    for gate in gates:
        u = unitary([gate],3)
        for x in range(8):
            for z in range(8):
                p=(x&z).bit_count()%4
                assert np.linalg.norm(u @ pauli_matrix(p,x,z,3) @ u.conj().T - pauli_matrix(*conjugate((p,x,z),[gate]),3)) < 1e-10
    counts['single_gate_all_pauli_checks']=len(gates)*64
    # New independent seed, larger system, nontrivial environment and signs.
    hist={}
    for n,e,number in [(1,2,40),(2,2,40),(3,1,40)]:
        for _ in range(number):
            gs=[]
            for __ in range(24):
                op=rng.choice(['H','S','SDG','X','Z','CX','SWAP'])
                gs.append([op,*rng.sample(range(n+e),2 if op in ['CX','SWAP'] else 1)])
            c=dense_check({'n':n,'env':e,'gates':gs})
            hist[c['status']]=hist.get(c['status'],0)+1
    counts['new_dense_cases']=120;counts['new_dense_statuses']=hist
    # All reset outputs are pure but may have complex/entangled signs.
    phase_checks=0
    for n in [1,2,3]:
        for _ in range(12):
            prep=[]
            for __ in range(10):
                op=rng.choice(['H','S','SDG','X','Z']+(['CX'] if n>1 else []))
                prep.append([op,*rng.sample(range(n),2 if op=='CX' else 1)])
            p={'n':n,'env':n,'gates':[['SWAP',j,n+j] for j in range(n)]+prep}
            c=dense_check(p);assert c['status']=='accepted_pure_return'
            minus=copy.deepcopy(p);minus['gates'] += [['X',0],['Z',0],['X',0],['Z',0]]
            cm=dense_check(minus)
            cp=unitary(c['c_preparation_with_clean_source_work'],2*n)[:,0]
            cpm=unitary(cm['c_preparation_with_clean_source_work'],2*n)[:,0]
            assert np.linalg.norm(cp+cpm)<1e-10
            assert not verify(minus,c)
            phase_checks+=1
    counts['phase_sensitive_reset_pairs']=phase_checks
    p0={'n':1,'env':1,'gates':[['SWAP',0,1]]}
    base=dense_check(p0)
    base_c=unitary(base['c_preparation_with_clean_source_work'],2)[:,0]
    for power in range(1,9):
        pp=copy.deepcopy(p0);pp['gates'] += [['H',0],['S',0]]*(3*power)
        cc=dense_check(pp)
        actual_c=unitary(cc['c_preparation_with_clean_source_work'],2)[:,0]
        assert np.linalg.norm(actual_c-np.exp(1j*np.pi*power/4)*base_c)<1e-10
        assert not verify(pp,base)
    counts['eighth_root_global_phase_checks']=8
    p={'n':1,'env':1,'gates':[['SWAP',0,1]]};c=acquire(p)
    forged=copy.deepcopy(c)
    forged.update(filtration=[c['filtration'][0],[0],[0]],status='persistent_pauli',stabilization_step=2)
    counts['zero_only_persistent_forgery_rejected']=not verify(p,forged)
    malformed=[None,[],0,'x',{}, {'filtration':None}]
    rejected=0;raises=[]
    for bad in malformed:
        try:
            if verify(p,bad) is False: rejected+=1
        except Exception as exc: raises.append(type(exc).__name__)
    counts['malformed_top_level_rejected']=rejected;counts['malformed_top_level_raises']=raises
    invalid_programs=[None,[],0,'x',{}, {'n':True,'env':0,'gates':[]},
                      {'n':1,'env':0,'gates':{}}, {'n':1,'env':0,'gates':''},
                      {'n':1,'env':0,'gates':()}, {'n':1,'env':0,'gates':None},
                      {'n':1,'env':0,'gates':[['H',False]]},
                      {'n':2,'env':0,'gates':[['CX',0,0]]},
                      {'n':1,'env':0,'gates':[[[],0]]}]
    invalid_accepted=[]
    for i,bad in enumerate(invalid_programs):
        try:validate(bad);invalid_accepted.append(i)
        except (ValueError,TypeError,KeyError,IndexError):pass
    counts['malformed_program_checks']=len(invalid_programs)
    counts['malformed_programs_accepted']=invalid_accepted
    counts['source_sha256']=hashlib.sha256((root/'acquire_clifford_source.py').read_bytes()).hexdigest()
    counts['mathematical_dense_checks_passed']=True
    counts['verifier_adversarial_checks_passed']=counts['zero_only_persistent_forgery_rejected'] and rejected==len(malformed) and not raises and not invalid_accepted
    out=root/'independent_adversarial_checks.json'
    out.write_text(json.dumps(counts,indent=2)+'\n')
    print(out.read_text())


if __name__=='__main__':run()

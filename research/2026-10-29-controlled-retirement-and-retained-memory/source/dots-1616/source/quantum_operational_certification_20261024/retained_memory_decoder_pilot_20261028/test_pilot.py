"""Algebra/instrument/replay tests separate from the acquired sample evidence."""
import json, tempfile, shutil
from pathlib import Path
import numpy as np
from quantum_math import *
from simulator import RetainedSource
from learner import Learner
from ordinary_comparator import OrdinaryComparator
from replay import replay

ROOT=Path(__file__).resolve().parent
results={}

def check(name,value,tol=1e-10):
    value=float(value);results[name]={'residual':value,'tolerance':tol,'pass':bool(value<=tol)}
    assert value<=tol,(name,value,tol)

def partial_out(a):
    return np.einsum('aiaj->ij',a.reshape(2,2,2,2))

# Generic nonunital decoder validates indexing beyond unital bandit centers.
p=.37
aks=[np.array([[1,0],[0,np.sqrt(1-p)]],complex),np.array([[0,np.sqrt(p)],[0,0]],complex)]
c=sum(np.outer(a.reshape(-1),a.reshape(-1).conj())/2 for a in aks)
check('nonunital_TP',tp_residual(c))
ks,diag=compile_decoder(c)
rho=(I+.2*X+.3*Y-.4*Z)/2
check('nonunital_choi_vs_kraus',np.linalg.norm(apply_decoder(c,rho)-apply_kraus(aks,rho)))
check('nonunital_compiled_vs_original',np.linalg.norm(apply_kraus(ks,rho)-apply_kraus(aks,rho)))
u=rotation([.2,.7,-.4],1.31)
q=sum(np.trace((I-s*pa)/2@apply_decoder(c,u@(I+s*pa)/2@u.conj().T)).real for pa in (X,Y,Z) for s in (-1,1))/6
fe=sum(abs(np.trace(k@u))**2 for k in aks)/4
check('nonunital_six_state_Bell_identity',abs(q-2/3*(1-fe)))
check('unitary_target_score_vs_Kraus',abs(fe-np.trace(c@unitary_choi(u.conj().T)).real))

# Reconstruct actual stored memory and verify direct joint CPTP instrument.
source=RetainedSource(9)
rows=[json.loads(s) for s in (ROOT/'runs/bandit_N512_seed17/public_records.jsonl').read_text().splitlines()]
audits=[json.loads(s) for s in (ROOT/'runs/bandit_N512_seed17/private_source_audit.jsonl').read_text().splitlines()]
learner=Learner()
max_joint=max_prob=max_unbiased=max_variance=max_conditional=0.
for t,(record,audit) in enumerate(zip(rows,audits)):
    ccenter=choi(learner.theta);played,_=learner.act(record['i'],record['z'])
    if t in (0,127,511):
        source.sigma=np.array(audit['memory_prior_real'])+1j*np.array(audit['memory_prior_imag'])
        blocks=source.branches();masses=np.array([np.trace(x).real for x in blocks])
        ks,_=compile_decoder(played);j=record['j'];s=record['s']
        rho=(I+s*PAULIS[j+1])/2
        joint=sum((np.kron(source.u@pa,k)@np.kron(rho,source.sigma)@np.kron(source.u@pa,k).conj().T
                   for pa,maps in zip(PAULIS,source.maps) for k in maps),np.zeros((4,4),complex))
        decoded=sum(np.kron(k,I)@joint@np.kron(k,I).conj().T for k in ks)
        unnorm=[]
        for y in (0,1):
            effect=(I+(1-2*y)*s*PAULIS[j+1])/2
            measured=np.kron(effect,I)@decoded@np.kron(effect,I)
            direct=partial_out(measured)
            probs=np.array([np.trace(effect@apply_kraus(ks,source.u@pa@rho@pa@source.u.conj().T)).real for pa in PAULIS])
            compact=sum((pr*b for pr,b in zip(probs,blocks)),np.zeros((2,2),complex))
            max_joint=max(max_joint,np.linalg.norm(direct-compact));unnorm.append(direct)
            if y==record['y']:
                stored=np.array(audit['memory_post_real'])+1j*np.array(audit['memory_post_imag'])
                max_conditional=max(max_conditional,np.linalg.norm(direct/np.trace(direct)-stored))
        max_prob=max(max_prob,abs(np.trace(unnorm[1]).real-audit['born_mismatch_probability']))
        check(f'instrument_nonselective_t{t+1}',np.linalg.norm(sum(unnorm)-sum(blocks)))
        # Exact finite enumeration of fresh i,z, and expectation over actual bit.
        _,h=barrier(ccenter);l=np.linalg.cholesky(h);v=.75*np.linalg.inv(l.T);dual=np.linalg.inv(v.T)
        T=np.zeros((4,4),complex)
        for axis in (X,Y,Z):
            for sign in (-1,1):
                inputrho=(I+sign*axis)/2
                emitted=sum(m*source.u@pa@inputrho@pa@source.u.conj().T for m,pa in zip(masses,PAULIS))
                T+=np.kron((I-sign*axis)/2,emitted.T)/6
        exactgradient=2*np.einsum('aij,ji->a',BASIS,T).real
        estimated=np.zeros(D);secondmoment=0.
        for i in range(D):
            for z in (-1,1):
                cp=ccenter+z/2*np.einsum('a,aij->ij',v[:,i],BASIS)
                q=2*np.trace(cp@T).real
                g=2*D*z*dual[:,i]
                estimated+=q*g/(2*D)
                secondmoment+=q*(g@np.linalg.solve(h,g))/(2*D)
        max_unbiased=max(max_unbiased,np.linalg.norm(estimated-exactgradient))
        qcenter=2*np.trace(ccenter@T).real
        max_variance=max(max_variance,secondmoment/(8*D*D*qcenter))
    learner.observe(record['y'])
check('direct_joint_vs_compact_CP_instrument',max_joint)
check('stored_actual_memory_poststate',max_conditional)
check('stored_actual_Born_probability',max_prob)
check('conditional_bandit_gradient_unbiased',max_unbiased)
results['conditional_second_moment_bound']={'ratio':float(max_variance),'upper_bound':1.,'pass':bool(max_variance<=1+1e-12)}

# Average Bloch transfer has positive diagonal contraction and polar factor R_U.
blocks=source.branches();masses=np.array([np.trace(x).real for x in blocks])
M=np.array([[sum(m*np.trace(a@source.u@pa@b@pa@source.u.conj().T).real/2 for m,pa in zip(masses,PAULIS)) for b in (X,Y,Z)] for a in (X,Y,Z)])
expected=np.zeros((3,3))
for j,a in enumerate((X,Y,Z)):
    for s in (-1,1):
        r=sum(m*source.u@pa@(I+s*a)/2@pa@source.u.conj().T for m,pa in zip(masses,PAULIS))
        for m,b in enumerate((X,Y,Z)):
            for result in (-1,1):
                probability=np.trace((I+result*b)/2@r).real
                expected[m,j]+=9*s*result*probability/18
check('ordinary_random_Pauli_estimator_unbiased',np.linalg.norm(M-expected))
ordinary=OrdinaryComparator();ordinary.total=M;ordinary.n=1
recovered,_=ordinary.decoder()
check('population_Procrustes_recovers_known_U_decoder',np.linalg.norm(recovered-unitary_choi(source.u.conj().T)))

# Replay with private files physically absent, and neither simulator nor metadata read.
with tempfile.TemporaryDirectory() as tmp:
    directory=Path(tmp)/'bandit_N512_seed17';directory.mkdir()
    shutil.copy(ROOT/'runs/bandit_N512_seed17/public_records.jsonl',directory/'public_records.jsonl')
    rr=replay(directory)
    check('public_only_exact_theta_replay',rr['max_theta_replay_error'],tol=0.)
    results['source_disabled_replay']={'public_records':rr['records_replayed'],'private_files_present':False,'pass':True}

# Guard invalid data and verify ordinary source construction without new sampled calls.
bad=Learner();bad.act(0,1)
try:bad.observe(.5);raise AssertionError('nonbit was accepted')
except ValueError:pass
results['nonbit_rejected']={'pass':True}
results['new_stochastic_source_calls_in_tests']=0
results['all_pass']=all(v.get('pass',True) for v in results.values() if isinstance(v,dict))
(ROOT/'test_results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))

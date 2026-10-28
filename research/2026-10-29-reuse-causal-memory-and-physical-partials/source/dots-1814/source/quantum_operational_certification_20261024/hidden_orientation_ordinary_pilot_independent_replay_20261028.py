#!/usr/bin/env python3
"""Audit pilot accounting and replay exact bytes in a temporary directory.
The original author files are never modified. This is simulation, not hardware.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,platform
import numpy as np

ROOT=Path(__file__).resolve().parent
source=ROOT/'hidden_orientation_ordinary_pilot_20261028.py'
original=ROOT/'hidden_orientation_ordinary_pilot_20261028.json'
sha=lambda b:hashlib.sha256(b).hexdigest()
with tempfile.TemporaryDirectory(prefix='orientation_pilot_review_') as tmp:
    copied=Path(tmp)/source.name
    copied.write_bytes(source.read_bytes())
    proc=subprocess.run([sys.executable,str(copied)],capture_output=True,text=True,check=True)
    replay_bytes=(Path(tmp)/original.name).read_bytes()
assert replay_bytes==original.read_bytes(), 'Same-environment byte replay changed author output'
data=json.loads(replay_bytes)
assert data['independent_runs']==768==len(data['runs'])
assert data['simulated_calls']==688128==sum(row['N'] for row in data['runs'])

# Reconstruct the individual RNG labels/Bernoulli outcomes separately. Integer
# sufficient statistics avoid the author's np.add.at floating accumulation.
rng=np.random.default_rng(data['seed'])
q=np.array([1.,2.,3.,4.]);q/=np.linalg.norm(q)
w,x,y,z=q
R=np.array([[1-2*(y*y+z*z),2*(x*y-w*z),2*(x*z+w*y)],
            [2*(x*y+w*z),1-2*(x*x+z*z),2*(y*z-w*x)],
            [2*(x*z-w*y),2*(y*z+w*x),1-2*(x*x+y*y)]])
I=np.eye(2,dtype=complex)
P=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
U=q[0]*I-1j*sum((q[j+1]*P[j] for j in range(3)),np.zeros((2,2),complex))
R_physical=np.array([[np.trace(P[a]@U@P[j]@U.conj().T).real/2 for j in range(3)] for a in range(3)])
assert np.max(abs(R-R_physical))<1e-14
assert np.max(abs(R.T@R-np.eye(3)))<1e-14 and abs(np.linalg.det(R)-1)<1e-14
records_digest=hashlib.sha256();run_evidence=[]
max_loss_diff=max_fit_physicality=max_objective_gap=0.
cursor=0
for p in [.001,.01,.1,1.]:
    for N in [128,512,2048]:
        for rep in range(64):
            row=data['runs'][cursor];cursor+=1
            assert (row['p'],row['N'],row['rep'])==(p,N,rep)
            j=rng.integers(0,3,N);a=rng.integers(0,3,N)
            sg=2*rng.integers(0,2,N)-1
            flag=rng.random(N)<p
            mean=sg*np.where(flag,R[a,j],(a==j).astype(float))
            assert np.min(mean)>=-1-1e-14 and np.max(mean)<=1+1e-14
            b=np.where(rng.random(N)<(1+mean)/2,1,-1)
            raw=np.column_stack([j,a,sg,flag.astype(int),b]).astype(np.int8).tobytes()
            records_digest.update(raw)
            signed_counts=np.zeros((3,3),dtype=np.int64)
            for aa in range(3):
                for jj in range(3):
                    selected=(a==aa)&(j==jj)&flag
                    signed_counts[aa,jj]=np.sum(sg[selected]*b[selected])
            M=signed_counts*(9./N)
            L,sval,Vh=np.linalg.svd(M)
            correction=np.diag([1.,1.,np.linalg.det(L@Vh)])
            fit=L@correction@Vh
            loss=p*np.linalg.norm(fit-R,'fro')**2/8
            assert int(flag.sum())==row['leakage_count']
            max_loss_diff=max(max_loss_diff,abs(loss-row['loss']))
            assert abs(loss-row['loss'])<1e-14
            # Independently cross-check the SO(3) objective through quaternion K.
            A=M
            K=np.array([[np.trace(A),A[2,1]-A[1,2],A[0,2]-A[2,0],A[1,0]-A[0,1]],
              [A[2,1]-A[1,2],A[0,0]-A[1,1]-A[2,2],A[0,1]+A[1,0],A[0,2]+A[2,0]],
              [A[0,2]-A[2,0],A[0,1]+A[1,0],-A[0,0]+A[1,1]-A[2,2],A[1,2]+A[2,1]],
              [A[1,0]-A[0,1],A[0,2]+A[2,0],A[1,2]+A[2,1],-A[0,0]-A[1,1]+A[2,2]]])
            objective_gap=abs(np.linalg.eigvalsh(K)[-1]-np.sum(fit*M))
            max_objective_gap=max(max_objective_gap,float(objective_gap))
            phys=max(float(np.max(abs(fit.T@fit-np.eye(3)))),abs(float(np.linalg.det(fit))-1))
            max_fit_physicality=max(max_fit_physicality,phys)
            assert phys<1e-13 and objective_gap<1e-13
            assert -1e-14<=loss<=p+1e-14
            run_evidence.append({'p':p,'N':N,'rep':rep,'record_sha256':sha(raw),
                                 'leakage_count':int(flag.sum()),
                                 'integer_signed_counts':signed_counts.tolist()})

summary_cases=0
for summary in data['summary']:
    rows=[r for r in data['runs'] if r['p']==summary['p'] and r['N']==summary['N']]
    assert len(rows)==64
    losses=np.array([r['loss'] for r in rows])
    vals={'mean_loss':float(np.mean(losses)),
          'se_loss':float(np.std(losses,ddof=1)/np.sqrt(len(rows))),
          'mean_leakage':float(np.mean([r['leakage_count'] for r in rows])),
          'theoretical_expected_cap':min(summary['p'],41/summary['N'])}
    assert all(abs(vals[k]-summary[k])<1e-15 for k in vals)
    summary_cases+=1

out={'status':'PASS_INDEPENDENT_SAME_ENVIRONMENT_BYTE_REPLAY_AND_PER_CALL_ACCOUNTING',
     'author_source_sha256':sha(source.read_bytes()),'author_output_sha256':sha(original.read_bytes()),
     'independent_script_sha256':sha(Path(__file__).read_bytes()),
     'same_environment_byte_identical':True,'python':platform.python_version(),'numpy':np.__version__,
     'independent_runs':768,'individually_simulated_calls_per_replay':688128,
     'reviewer_simulation_passes':2,'reviewer_total_simulated_calls':1376256,
     'physical_source_calls':0,'retained_summary_cases':summary_cases,
     'reconstructed_record_stream_sha256':records_digest.hexdigest(),
     'max_loss_recompute_difference':max_loss_diff,'max_float_fit_physicality_residual':max_fit_physicality,
     'max_float_quaternion_objective_discrepancy':max_objective_gap,
     'evidence_class':'Actual per-call RNG simulation, not aggregate-count-only simulation; source labels regenerated from fixed seed. Binary64 fits are NOT exactly physical rational controls or a production compiler.',
     'limitations':['No hardware source','No raw per-call records retained in original author JSON',
       'Byte-identical replay asserted only in this recorded Python/NumPy environment',
       'Monte Carlo means/standard errors are not a proof of expected or tail guarantees',
       'One fixed source rotation and declared parameter grid, not exhaustive noise testing'],
     'run_record_digest_and_integer_statistics':run_evidence}
(ROOT/'hidden_orientation_ordinary_pilot_independent_replay_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='run_record_digest_and_integer_statistics'},indent=2))

"""Independent branch prep, matrix-state DP, and grouped Pauli-code checks.
Reuses declared source generators/acquired frame and reviewed exact field decoder;
does not claim hardware execution or dense 32**31 quantum-state simulation.
"""
import runpy,contextlib,io,json,itertools,math
import numpy as np
from pathlib import Path
HERE=Path(__file__).resolve().parent
captured=io.StringIO()
with contextlib.redirect_stdout(captured):
    d=runpy.run_path(str(HERE.parent/'complete_noreset_learn_and_guard_v8.py'))
# Author JSON reproducibility, and continuity/dataflow boundary checks.
author_text=captured.getvalue()
assert author_text==(HERE.parent/'complete_noreset_learn_and_guard_v8.json').read_text()
old=d['old']
J=np.zeros((16,9))
for i in range(1,4):
    for j in range(1,4):J[4*i+j,3*(i-1)+j-1]=1
assert np.array_equal(J,old.Jembed)
# The fit is recomputed from only observed counters and the known identity embedding.
from scipy.linalg import polar,expm
from scipy.spatial.transform import Rotation
frames=[np.eye(3)]
for pairbank in old.sums:
    _,_,vt=np.linalg.svd(pairbank/1000000-J)
    A=np.sqrt(3)*vt[-1].reshape(3,3)
    candidates=[]
    for sign in [1,-1]:
        u,sv,vh=np.linalg.svd(sign*A)
        candidates.append(u@np.diag([1,1,np.linalg.det(u@vh)])@vh)
    err=[np.linalg.norm(candidates[0]-A),np.linalg.norm(candidates[1]+A)]
    frames.append(candidates[int(err[1]<err[0])])
frame_res=max(np.linalg.norm(x-y) for x,y in zip(frames,d['frames']))
carry_res=np.linalg.norm(d['sigma']-np.outer(old.bath,old.bath.conj()))
assert frame_res<1e-12 and carry_res<1e-15
assert np.linalg.norm(d['Ugood']-old.Us[0])<1e-15
assert abs(np.trace(d['sigma'])-1)<1e-12
continuity={'counter_only_frame_reconstruction_residual':float(frame_res),'final_bath_density_carry_residual':float(carry_res),'final_bath_density_real':d['sigma'].real.tolist(),'final_bath_density_imag':d['sigma'].imag.tolist(),'final_acquisition_parity':int(old.lastparity),'declared_guard_source_variant':0,'identity_embedding_is_known_constant':True,'author_rerun_byte_identical':True,'yield_scope':'guard probabilities conditional on this one realized million-call acquisition record, not averaged over all training records'}
# Explicit pure branch preparation at each pair, not projected-sector input oracle.
sing=np.array([0,1,-1,0])/np.sqrt(2);t0=np.array([0,1,1,0])/np.sqrt(2)
omega=(np.kron([1,0,0,0],[0,0,0,1])-np.kron(t0,t0)+np.kron([0,0,0,1],[1,0,0,0]))/np.sqrt(3)
def permute(v,order):
    out=np.zeros_like(v)
    for x in range(16):
        y=sum(((x>>(3-i))&1)<<(3-order[i]) for i in range(4));out[y]=v[x]
    return out
preps=[]
for i,j in itertools.combinations(range(4),2):
    order=[i,j]+[x for x in range(4) if x not in [i,j]]
    preps.append([d['Vhat']@permute(np.kron(sing,sing),order),d['Vhat']@permute(omega,order)])
def physical_test_map(U,sigma,fail):
    result=np.zeros((2,2),complex)
    for S,vs in zip(d['Ss'],preps):
        for sign,v in zip([-1,1],vs):
            # n4 signed preparation probabilities exactly 1/2.
            inp=np.kron(np.outer(v,v.conj())/2,sigma)
            effect=(np.eye(16)+(-sign if fail else sign)*S)/2
            Y=np.kron(effect,np.eye(2));out=Y@U@inp@U.conj().T@Y
            result+=sum(out[2*x:2*x+2,2*x:2*x+2] for x in range(16))/6
    return result
prep_res=[]
for U,model in zip([d['Ugood'],d['Uburst']],d['mp']):
    for fail,name in [(False,'testpass'),(True,'testfail')]:
        cols=[]
        for i in range(2):
            for j in range(2):
                sig=np.zeros((2,2));sig[i,j]=1;cols.append(physical_test_map(U,sig,fail).reshape(-1))
        res=np.linalg.norm(np.stack(cols,axis=1)-model[name]);prep_res.append(float(res));assert res<1e-12
# Independent count DP: faults first, services second, explicit 2x2 memory axes.
def apply(S,states):return np.einsum('abij,fsij->fsab',S.reshape(2,2,2,2),states)
def weight(x):return float(np.trace(x,axis1=-2,axis2=-1).real.sum())
def independent_dp(burst):
    state=np.zeros((8,156,2,2),complex);state[0,0]=d['sigma'];accepted=np.zeros((8,2,2),complex);abort=0.;cost=0.
    for call in range(1,1401):
        cost+=weight(state)
        model=d['mp'][int(burst and 500<=call<=511)]
        good=d['s']*apply(model['good'],state)
        bad=d['s']*apply(model['bad'],state)
        passing=d['a']*apply(model['testpass'],state)
        abort+=d['a']*weight(apply(model['testfail'],state))
        nxt=passing.copy();nxt[:,1:]+=good[:,:-1]
        nxt[1:,1:]+=bad[:-1,:-1];nxt[-1,1:]+=bad[-1,:-1]
        accepted+=nxt[:,155];nxt[:,155]=0;state=nxt
    cap=weight(state);abort+=cap
    return {'accept':weight(accepted),'accepted_bad':weight(accepted[-1]),'abort':abort,'cap_abort':cap,'expected_calls':cost}
dps=[]
for burst,author in zip([False,True],d['out']):
    calc=independent_dp(burst);ex=author['exact_compressed_memory_DP']
    rem={'accept':'accept_probability','accepted_bad':'accepted_more_than_t_fault_weight','abort':'abort_probability','cap_abort':'cap_abort_probability','expected_calls':'expected_source_calls'}
    residual=max(abs(calc[k]-ex[v]) for k,v in rem.items());assert residual<1e-8
    dps.append({'burst':burst,**calc,'max_author_comparison_residual':residual})
# Trace-dual Z mapping: exhaust all fields and bit coordinates.
g=d['g'];duals=d['duals']
for bit in range(5):
    for x in range(32):assert g.trace(g.mul(duals[bit],x))==((x>>bit)&1)
# Independently construct grouped e,f from binary symplectic masks, not author's function.
rng=np.random.default_rng(553199);checked=0;max_inner=0
for typ in ['spread','clustered','random']:
    for rep in range(12):
        labels=np.zeros(155,dtype=int)
        if typ=='spread':
            groups=rng.choice(31,6,replace=False)
            for group in groups:labels[5*group+(rep%5)]=1+rep%3
        elif typ=='clustered':
            # More than six inner faults, but at most six grouped outer symbols.
            groups=rng.choice(31,6,replace=False)
            for group in groups:labels[5*group:5*group+5]=rng.integers(1,4,size=5)
        else:
            loc=rng.choice(155,rep%7,replace=False);labels[loc]=rng.integers(1,4,size=len(loc))
        ex=[];fz=[]
        for chunk in labels.reshape(31,5):
            xv=sum((int(p) in [1,2])*(1<<j) for j,p in enumerate(chunk))
            zv=0
            for j,p in enumerate(chunk):
                if p in [2,3]:zv^=duals[j]
            ex.append(xv);fz.append(zv)
        x,z,ok=d['grs'].one_way_correction(g,d['code'],ex,fz)
        assert ok and all(v==0 for v in x+z)
        checked+=1;max_inner=max(max_inner,int(np.count_nonzero(labels)))
result={'all_assertions_passed':True,'actual_pure_signed_preparation_map_residuals':prep_res,'independent_matrix_state_DP':dps,'dual_Z_basis_exhaustive_checks':160,'independent_grouped_decoder_patterns':checked,'maximum_inner_faults_in_corrected_clustered_pattern':max_inner,'exact_reported_NB':'1/128','optional_ideal_C3_NB':'1/2187','continuity':continuity,'final_bank_calls':1000000,'all_finite_bank_calls':1000000,'scope':'Source-generator simulation with actual branch-prep map and exact field decoder checks; no physical experiment or full outer amplitude simulation'}
(HERE/'check_noreset_complete.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

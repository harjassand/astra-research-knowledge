"""Exact quantum-trajectory event law, sampled on a finite Steane fixture.

Base recovery is the IDEAL full-block syndrome-recovery channel at rate k.
It is NOT the finite-controller or four-body device. Flags and DATA faults
are physical local Lindblad jumps; the state, including Choi reference,
is a pure stabilizer trajectory. No classical logical-bit surrogate is used.
"""
from __future__ import annotations
import hashlib,json,math,time
from pathlib import Path
import numpy as np
from steane_model import choi_stabilizer,recover,target_fidelity,conjugate_cnot
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/latched_gate_20261101'

def one(rng,gamma,kappa,horizon,data_rate,pump,mode):
    state=choi_stabilizer();flags=[1]*7;dirty=[False,False]
    # Initial analytical W frame has the desired transversal logical CNOT.
    for i in range(7):state.cnot(i,i+7)
    t=0.;events={'down':0,'up':0,'recover':0,'data_X':0,'data_Y':0,'data_Z':0}
    if mode=='scheduled':
        # Same ideal memory, same flags/pump/data environment, one actual
        # externally scheduled transversal pulse; flags are spectators.
        pass
    while t<horizon:
        channels=[]
        channels += [(gamma,'down',i) for i,f in enumerate(flags) if f]
        channels += [(pump,'up',i) for i,f in enumerate(flags) if not f and pump]
        if data_rate:channels += [(14*data_rate,'data',0)]
        channels += [(kappa,'recover',b) for b in range(2) if dirty[b]]
        total=sum(r for r,_,_ in channels)
        if not total:break
        t+=rng.exponential(1/total)
        if t>horizon:break
        pick=rng.random()*total
        for rate,kind,index in channels:
            pick-=rate
            if pick<0:break
        if kind in ('down','up'):
            flags[index]=0 if kind=='down' else 1
            # W† sigma_F^-/+ W = CNOT_i sigma_F^-/+.
            if mode=='autonomous':state.cnot(index,index+7);dirty=[True,True]
            events[kind]+=1
        elif kind=='recover':
            recover(state,index,rng);dirty[index]=False;events['recover']+=1
        else:
            site=int(rng.integers(14));axis=int(rng.integers(3))
            xx,zz,pp=((1,0,0),(1,1,1),(0,1,0))[axis]
            a=(xx<<site,zz<<site,pp)
            if mode=='autonomous' and flags[site%7]:a=conjugate_cnot(a,site%7,site%7+7)
            state.pauli(a)
            if a[0]&127 or a[1]&127:dirty[0]=True
            if a[0]>>7 or a[1]>>7:dirty[1]=True
            events[['data_X','data_Y','data_Z'][axis]]+=1
    # Return to the actual physical DATA frame. This is an analytical
    # evaluation; no flag-dependent gate is supplied to the decoder.
    if mode=='autonomous':
        for i,f in enumerate(flags):
            if f:state.cnot(i,i+7)
    recover(state,0,rng);recover(state,1,rng)
    return target_fidelity(state),sum(flags),events

def main():
    seed=2026110107;repeats=3000;rng=np.random.default_rng(seed);start=time.monotonic()
    specs=[('slow_clean',.01,1.,600.,0.,0.,'autonomous'),
           ('slow_unbalanced_noise',.01,1.,600.,2e-5,1e-5,'autonomous'),
           ('fast_flag_failure',1000.,1.,600.,0.,0.,'autonomous'),
           ('scheduled_same_memory_noise',.01,1.,600.,2e-5,1e-5,'scheduled')]
    rows=[]
    for name,g,k,t,d,p,mode in specs:
        vals=[];unfinished=[];counts={}
        for _ in range(repeats):
            f,u,e=one(rng,g,k,t,d,p,mode);vals.append(f);unfinished.append(u)
            for key,v in e.items():counts[key]=counts.get(key,0)+v
        mean=float(np.mean(vals));se=float(np.std(vals,ddof=1)/np.sqrt(repeats))
        # Distribution-free Hoeffding interval for bounded fidelities.
        half=math.sqrt(math.log(40)/(2*repeats))
        rows.append({'name':name,'mode':mode,'gamma':g,'recovery_rate_per_block':k,'time':t,
                     'data_Pauli_rate_per_qubit_total':d,'flag_upward_rate':p,'trajectories':repeats,
                     'mean_target_CNOT_entanglement_fidelity':mean,'sample_standard_error':se,
                     'individual_95pct_Hoeffding_interval':[max(0.,mean-half),min(1.,mean+half)],
                     'mean_unfinished_flags':float(np.mean(unfinished)),
                     'mean_events':{key:v/repeats for key,v in counts.items()}})
        print(json.dumps(rows[-1]),flush=True)
    assert rows[0]['mean_target_CNOT_entanglement_fidelity']>rows[2]['mean_target_CNOT_entanglement_fidelity']+.3
    assert rows[3]['mean_target_CNOT_entanglement_fidelity']>.95
    result={'scope':'sampled stabilizer quantum trajectories with IDEAL nonlocal block recovery; no finite-controller simulation',
            'seed':seed,'runtime_seconds':time.monotonic()-start,'rows':rows,
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'model_sha256':hashlib.sha256(Path(__file__).with_name('steane_model.py').read_bytes()).hexdigest()}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'stochastic_gate_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'runtime_seconds':result['runtime_seconds'],'status':'PASS'}),flush=True)
if __name__=='__main__':main()

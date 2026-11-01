#!/usr/bin/env python3
"""Ordinary retained interval-MDP baseline, same partition/row observations.

No claim of new planner. Row envelopes cover arbitrary microscopic feedback;
actual batched forward rollouts give a goal-specific sharper policy lower bound.
All prefixes/validation batches are charged. Frozen originals are read only.
"""
from pathlib import Path
import gzip,hashlib,json,math,sys,time
import numpy as np
import sympy as s
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(PARENT))
from retained_large_acquisition import R,clog2,eb_radius
from large_routing_source import RoutingSource,acquire_partition


def extremize(lo,hi,value,maximize):
    p=lo[:];remaining=1-sum(p)
    assert min(p)>=0 and all(a<=b<=1 for a,b in zip(lo,hi)) and remaining>=0 and sum(hi)>=1
    order=sorted(range(len(p)),key=lambda j:(value[j],-j),reverse=maximize)
    for j in order:
        z=min(remaining,hi[j]-p[j]);p[j]+=z;remaining-=z
    assert remaining==0
    return sum(x*y for x,y in zip(p,value))


def plan_interval(lower,upper,terminal,L):
    m=len(lower);r=len(terminal);low=terminal[:];high=terminal[:];policies=[];trace=[];peak=1
    for _ in range(L):
        nextlo=[];nexthi=[];policy=[]
        for g in range(r):
            candidates=[extremize(lower[a][g],upper[a][g],low,False) for a in range(m)]
            optimistic=[extremize(lower[a][g],upper[a][g],high,True) for a in range(m)]
            a=max(range(m),key=lambda j:(candidates[j],-j));policy.append(a);nextlo.append(candidates[a]);nexthi.append(max(optimistic))
        low=nextlo;high=nexthi;policies.append(policy)
        for x in low+high:peak=max(peak,int(x.p).bit_length(),int(x.q).bit_length())
        trace.append({'lower':list(map(str,low)),'upper':list(map(str,high))})
    return {'policy_by_remaining_steps':policies,'lower':list(map(str,low)),'upper':list(map(str,high)),
            'trace':trace,'bellman_scalar_products':2*L*m*r*r,'max_value_rational_component_bits':peak}


class BatchedOrdinarySource:
    """Source-side implementation: actual independent vectorized transitions.

    Private fixture wiring is used ONLY by this ordinary source adapter. The
    learner supplies named labels/actions and receives destination labels.
    Branch probabilities use exact integer counts out of100000.
    """
    def __init__(self,n,seed):
        q=RoutingSource(n);self.n=n;self.rng=np.random.default_rng(seed)
        self.adj=np.asarray(q._adj,dtype=np.int64);self.groups=np.asarray(q._groups,dtype=np.int64)
        self.which=q._which;self.actions=np.asarray(q._actions,dtype=np.int64)
        self.global_dest=np.asarray(q._global,dtype=np.int64);self.reset=np.asarray(q._reset,dtype=np.int64)
        self.calls=0
    def step(self,states,actions):
        N=len(states);assert len(actions)==N and np.all((0<=states)&(states<self.n)) and np.all((0<=actions)&(actions<2))
        branch=self.rng.integers(100000,size=N);out=np.empty(N,dtype=np.int64)
        mask=branch<95998;ids=np.flatnonzero(mask)
        out[ids]=self.adj[actions[ids],states[ids],self.rng.integers(16,size=len(ids))]
        ids=np.flatnonzero((branch>=95998)&(branch<99998));g=self.actions[actions[ids],self.which[states[ids]]]
        out[ids]=self.groups[g,self.rng.integers(self.n//4,size=len(ids))]
        ids=np.flatnonzero(branch==99998);out[ids]=self.global_dest[actions[ids],states[ids]]
        ids=np.flatnonzero(branch==99999);out[ids]=self.reset[actions[ids],self.rng.integers(self.n//2,size=len(ids))]
        self.calls+=N;return out


def evaluate(policy,which,initial_mask,terminal,N,seed,delta):
    source=BatchedOrdinarySource(len(which),seed);support=np.flatnonzero(initial_mask)
    states=source.rng.choice(support,size=N);which=np.asarray(which);pol=np.asarray(policy);b=np.asarray(terminal)
    for actions in pol[::-1]:states=source.step(states,actions[which[states]])
    outcomes=b[states];count=int(outcomes.sum());K=R(7,10)*clog2(4/delta)
    rad=eb_radius(count,N,K);lo=max(R(0),R(count,N)-rad);hi=min(R(1),R(count,N)+rad)
    packed=np.packbits(outcomes.astype(np.uint8),bitorder='little').tobytes()
    return {'episodes':N,'successes':count,'confidence':str(delta),'K':str(K),'mean':str(R(count,N)),
      'lower':str(lo),'upper':str(hi),'actual_simulated_transitions':source.calls,
      'outcome_bits_sha256':hashlib.sha256(packed).hexdigest(),'seed':seed},packed


def run(output_dir=None):
    start=time.perf_counter();model=json.loads((PARENT/'history_sensitive_4096_result.json').read_text())
    raw=(PARENT/'history_sensitive_4096_observations.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==model['transcript_gzip_sha256']
    records=json.loads(gzip.decompress(raw))['records'];n=model['n'];m=model['m'];L=model['length'];delta=R(1,1000)
    coarse=[z['counts'] for z in records if z['kind']=='coarse']
    parts,which,proposal=acquire_partition(coarse,model['task_b'],model['task_ell_numer'])
    assert parts==model['partition'] and R(model['fixture_tau'])==R(1,25)
    assert n==4096 and m==2 and L==24
    r=len(parts);terminal=[model['task_b'][p[0]] for p in parts]
    initial=[R(sum(model['task_ell_numer'][i] for i in p),model['task_ell_denominator']) for p in parts]
    counts=[[[0]*r for _ in range(n)] for _ in range(m)];N=0;calls=0
    proposal_calls=sum(z['N'] for z in records if z['kind'] in ('column','coarse'))
    for z in records:
        if z['kind']=='pilot':
            a=z['a'];assert z['N']==2048
            for i,row in enumerate(z['counts']):
                assert sum(row)==z['N']
                counts[a][i]=row[:]
            calls+=n*z['N']
    N=2048;K=R(7,10)*clog2(4*m*n*r*6/(delta/2));attempts=[];eval_calls=0
    # Every possible prefix0..5 has a fixed, nonanticipating row sample count;
    # allocate delta/2 over all six, not just the three eventually observed.
    for turn in range(len(model['cross_rounds'])):
        selected=[z for z in records if z['kind']=='incoming_pair' and z['turn']==turn]
        expected_reps=model['cross_rounds'][turn]['incoming_replicates'];Ni=model['cross_rounds'][turn]['incoming_per_row_half']
        assert len(selected)==m*expected_reps
        assert sorted((z['a'],z['replicate']) for z in selected)==[(a,j) for a in range(m) for j in range(expected_reps)]
        for z in selected:
            assert z['N']==Ni
            for half in z['counts']:
                assert len(half)==n
                for i,row in enumerate(half):
                    assert len(row)==r and all(type(v) is int and v>=0 for v in row) and sum(row)==Ni
                    for h,v in enumerate(row):counts[z['a']][i][h]+=v
            calls+=2*n*Ni
        N+=2*Ni*expected_reps;assert all(sum(row)==N for M in counts for row in M)
        radius={};lower=[[[R(1)]*r for _ in parts] for _ in range(m)];upper=[[[R(0)]*r for _ in parts] for _ in range(m)]
        for a in range(m):
            for i,row in enumerate(counts[a]):
                g=which[i]
                for h,c in enumerate(row):
                    if c not in radius:radius[c]=eb_radius(c,N,K)
                    lower[a][g][h]=min(lower[a][g][h],max(R(0),R(c,N)-radius[c]))
                    upper[a][g][h]=max(upper[a][g][h],min(R(1),R(c,N)+radius[c]))
        plan=plan_interval(lower,upper,terminal,L)
        lo=sum(w*R(v) for w,v in zip(initial,plan['lower']));hi=sum(w*R(v) for w,v in zip(initial,plan['upper']))
        # Candidate is fixed before its fresh evaluation batch. Three fixed
        # attempts, each delta/6, total delta/2; no reuse/postselection claim.
        ev,bits=evaluate(plan['policy_by_remaining_steps'],which,model['task_ell_numer'],model['task_b'],250000,810001+turn,delta/6)
        eval_calls+=ev['actual_simulated_transitions']
        if output_dir is not None:(Path(output_dir)/('policy_outcomes_prefix'+str(turn)+'.bin')).write_bytes(bits)
        gap=max(R(0),hi-max(lo,R(ev['lower'])))
        rec={'prefix_round':turn,'per_row_samples':N,'row_observation_calls':calls,'proposal_observation_calls':proposal_calls,
          'cumulative_fresh_evaluation_calls':eval_calls,'prospective_total_calls':calls+proposal_calls+eval_calls,
          'K':str(K),'interval_lower':[[list(map(str,row)) for row in M] for M in lower],
          'interval_upper':[[list(map(str,row)) for row in M] for M in upper],
          'plan':plan,'robust_value_lower':str(lo),'optimal_value_upper':str(hi),'pure_interval_regret':str(hi-lo),
          'fresh_policy_evaluation':ev,'certified_regret_with_fresh_evaluation':str(gap),
          'robust_lower_float':float(lo),'optimal_upper_float':float(hi),'evaluated_lower_float':float(R(ev['lower'])),
          'regret_float':float(gap),'scope':'On simultaneous confidence event, upper covers arbitrary microscopic/history policies; chosen block policy lower is certified from independent actual forward rollouts.'}
        attempts.append(rec);print(json.dumps({k:rec[k] for k in ['prefix_round','per_row_samples','prospective_total_calls','robust_lower_float','optimal_upper_float','evaluated_lower_float','regret_float']},indent=2),flush=True)
    return {'status':'COMPLETED_STRONG_INTERVAL_COMPARATOR','attempts':attempts,'confidence':str(delta),
      'actual_fresh_simulated_transitions':eval_calls,'retained_original_acquisition_calls':model['logical_forward_calls'],
      'scope':'No refund of original acquisition in this experiment. Prospective baseline ledger uses only proposal+row batches and its own paid evaluations; old outgoing/norm records are unused. Ordinary interval-MDP planning, not a new algorithm. Fresh source adapter exposes only sampled labels. No independent review yet.',
      'seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'base_model_sha256':hashlib.sha256((PARENT/'history_sensitive_4096_result.json').read_bytes()).hexdigest(),
      'observations_sha256':hashlib.sha256(raw).hexdigest()}


if __name__=='__main__':
    out=run(output_dir=ROOT);(ROOT/'interval_comparison_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'actual_fresh_simulated_transitions':out['actual_fresh_simulated_transitions'],'seconds':out['seconds']},indent=2))

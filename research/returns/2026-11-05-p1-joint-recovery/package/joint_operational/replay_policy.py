#!/usr/bin/env python3
"""Replay saved physical policies without recomputing representation bases.

Positive projection and a common input normalization specify CPTP maps from
finite-precision matrices. Reported errors follow the global Clifford twirl.
"""
from control_search import *


def physical_instrument(channels,o,d):
    positive=[]
    for j in channels:
        w,v=la.eigh(herm(j));positive.append(herm((v*np.maximum(w,0))@v.conj().T))
    a=herm(sum(choi_marginal(j,o,d) for j in positive));w,v=la.eigh(a)
    r=(v/np.sqrt(w))@v.conj().T;b=np.kron(np.eye(o),r)
    return [herm(b@j@b) for j in positive]


def physical_kraus(coeff,bases):
    ks=[]
    for x,b in zip(coeff,bases):
        w,v=la.eigh(herm(x));keep=w>0;a=v[:,keep]*np.sqrt(w[keep])
        ks.extend(np.einsum('ar,auij->ruij',a,b,optimize=True).reshape(-1,b.shape[-2],b.shape[-1]))
    ks=np.array(ks);a=herm(np.sum(ks.conj().transpose(0,2,1)@ks,axis=0));w,v=la.eigh(a)
    return ks@((v/np.sqrt(w))@v.conj().T)


def apply_kraus(rho,ks):
    h=rho.shape[0]//ks.shape[-1];k=np.array([np.kron(np.eye(h),a) for a in ks])
    return herm(np.sum((k@rho)@k.conj().transpose(0,2,1),axis=0))


def replay(path):
    with np.load(path) as z:data={k:z[k] for k in z.files}
    theta=float(data['source_theta']);m=int(data['memory_dimension']);model=CollisionModel(m,theta);rho=data['initial_joint_state'].copy()
    if 'policy' in data:
        policy=data['policy']
        if policy.ndim==5:
            C=policy.shape[1]
            for maps in policy:
                source=[model.source(x) for x in rho];next_rho=np.zeros_like(rho)
                for x,row in enumerate(maps):
                    instrument=physical_instrument(row,m,2*m)
                    for y,j in enumerate(instrument):next_rho[y]+=apply_local(source[x],j,m,2*m)
                rho=next_rho
            fe=0.
            for x,dec in zip(rho,data['decoders']):
                j=physical_instrument([dec],2,m)[0];fe+=trace_pair(model.bell_rsq,apply_local(x,j,2,m))
        else:
            for j in policy:rho=apply_local(model.source(rho),physical_instrument([j],m,2*m)[0],m,2*m)
            j=physical_instrument([data['decoder']],2,m)[0];fe=trace_pair(model.bell_rsq,apply_local(rho,j,2,m))
    else:
        keys=sorted([k for k in data if k.startswith('policy_block_')],key=lambda k:int(k.rsplit('_',1)[-1]));n=len(data[keys[0]])
        bases=[data['channel_base_'+str(k)] for k in range(len(keys))]
        for t in range(n):rho=apply_kraus(model.source(rho),physical_kraus([data[k][t] for k in keys],bases))
        if 'decoder' in data:
            j=physical_instrument([data['decoder']],2,m)[0];out=apply_local(rho,j,2,m)
        elif 'decoder_base_0' in data:
            dkeys=sorted([k for k in data if k.startswith('decoder_block_')],key=lambda k:int(k.rsplit('_',1)[-1]));db=[data['decoder_base_'+str(k)] for k in range(len(dkeys))]
            out=apply_kraus(rho,physical_kraus([data[k] for k in dkeys],db))
        else:
            j=physical_instrument([data['decoder_block_0']],2,m)[0];out=apply_local(rho,j,2,m)
        fe=trace_pair(model.bell_rsq,out)
    recorded=data['states'][-1]
    drift=float(sum(la.norm(a-b,'nuc') for a,b in zip(rho,recorded))) if rho.ndim==3 else float(la.norm(rho-recorded,'nuc'))
    return dict(file=str(path),fidelity=fe,twirled_halfdiamond_error=1-fe,trace_norm_replay_drift=drift)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('paths',nargs='+');p.add_argument('--out');a=p.parse_args();results=[replay(path) for path in a.paths]
    if a.out:Path(a.out).write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

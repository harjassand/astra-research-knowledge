#!/usr/bin/env python3
"""Exact population fixture. No physical acquisition or finite-sample claim."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json, math, hashlib

N=8; K=2; DEPTH=3
PI=[F(1,N)]*N
LABEL=[x//4 for x in range(N)]


def repair_block(Fmat, rows, cols):
    H=[r[:] for r in Fmat]
    for i,row in enumerate(H):
        s=sum(row)
        t=min(F(1),rows[i]/s) if s else F(0)
        H[i]=[x*t for x in row]
    for j in range(len(cols)):
        s=sum(H[i][j] for i in range(len(rows)))
        t=min(F(1),cols[j]/s) if s else F(0)
        for i in range(len(rows)): H[i][j]*=t
    dr=[rows[i]-sum(H[i]) for i in range(len(rows))]
    dc=[cols[j]-sum(H[i][j] for i in range(len(rows))) for j in range(len(cols))]
    d=sum(dr)
    assert d==sum(dc) and min(dr+dc)>=0
    if d:
        H=[[H[i][j]+dr[i]*dc[j]/d for j in range(len(cols))] for i in range(len(rows))]
    assert [sum(r) for r in H]==rows
    assert [sum(H[i][j] for i in range(len(rows))) for j in range(len(cols))]==cols
    norm=sum(abs(H[i][j]-Fmat[i][j]) for i in range(len(rows)) for j in range(len(cols)))
    rowerr=sum(abs(sum(Fmat[i])-rows[i]) for i in range(len(rows)))
    colerr=sum(abs(sum(Fmat[i][j] for i in range(len(rows)))-cols[j]) for j in range(len(cols)))
    assert norm<=rowerr+colerr
    return H


def make_kernel(w, base, hflip, tiny):
    T=[[F(0) for _ in range(N)] for _ in range(N)]
    for x in range(N):
        a=LABEL[x]; z=(x%4)//2; h=x%2
        sign=1 if (z+h)%2==0 else -1
        cross=base*(1+tiny*sign)/w[a]
        T[x][x+4 if a==0 else x-4]=cross
        T[x][x+1 if h==0 else x-1]=hflip
        T[x][x]=1-cross-hflip
    m=[F(w[LABEL[x]],4*sum(w)) for x in range(N)]
    assert all(sum(row)==1 and min(row)>=0 for row in T)
    assert all(m[x]*T[x][y]==m[y]*T[y][x] for x in range(N) for y in range(N))
    assert all(T[x][y]==0 for x in range(N) for y in range(N) if (x%4)//2!=(y%4)//2)
    return T,m


def repair(T,mu):
    mass=[sum(mu[x] for x in range(N) if LABEL[x]==a) for a in range(K)]
    C=[[sum(mu[x]*sum(T[x][y] for y in range(N) if LABEL[y]==b) for x in range(N) if LABEL[x]==a)/mass[a] for b in range(K)] for a in range(K)]
    r=[[sum(T[x][y] for y in range(N) if LABEL[y]==b)-C[LABEL[x]][b] for b in range(K)] for x in range(N)]
    ds=[[sum(mu[x]*abs(r[x][b]) for x in range(N) if LABEL[x]==a) for b in range(K)] for a in range(K)]
    delta_bound=[sum(ds[a][b]+ds[b][a] for b in range(K))/(2*mass[a]) for a in range(K)]
    eps2=sum(mu[x]*r[x][1]**2 for x in range(N))/(mass[0]*mass[1])
    flux=[[F(0) for _ in range(N)] for _ in range(N)]
    for a in range(K):
        ii=[x for x in range(N) if LABEL[x]==a]
        for b in range(a,K):
            jj=[y for y in range(N) if LABEL[y]==b]
            block=[[mu[x]*T[x][y] for y in jj] for x in ii]
            rr=[mu[x]*C[a][b] for x in ii]; cc=[mu[y]*C[b][a] for y in jj]
            B=repair_block(block,rr,cc)
            if a==b: B=[[(B[i][j]+B[j][i])/2 for j in range(len(jj))] for i in range(len(ii))]
            for i,x in enumerate(ii):
                for j,y in enumerate(jj):
                    flux[x][y]=B[i][j]; flux[y][x]=B[i][j]
    T0=[[flux[x][y]/mu[x] for y in range(N)] for x in range(N)]
    assert all(sum(row)==1 and min(row)>=0 for row in T0)
    assert all(mu[x]*T0[x][y]==mu[y]*T0[y][x] for x in range(N) for y in range(N))
    assert all(sum(T0[x][y] for y in range(N) if LABEL[y]==b)==C[LABEL[x]][b] for x in range(N) for b in range(K))
    delta=[sum(mu[x]*sum(abs(T[x][y]-T0[x][y]) for y in range(N))/2 for x in range(N) if LABEL[x]==a)/mass[a] for a in range(K)]
    assert all(x<=y for x,y in zip(delta,delta_bound))
    return T0,C,eps2,delta,delta_bound


def record_probs(Ts,policy,initial):
    level={((),0):initial}
    for depth in range(DEPTH):
        nxt={}
        for (record,node),v in level.items():
            T=Ts[policy[node]]
            moved=[sum(v[x]*T[x][y] for x in range(len(v))) for y in range(len(v))]
            for a in range(K):
                labels=LABEL if len(v)==N else list(range(K))
                nxt[(record+(a,),2*node+1+a)]=[moved[y] if labels[y]==a else F(0) for y in range(len(v))]
        level=nxt
    return [sum(v) for _,v in sorted(level.items())]


def main():
    tiny=F(1,1000)
    pairs=[make_kernel([1,1],F(1,4),F(1,8),tiny),make_kernel([1,2],F(1,3),F(1,6),tiny)]
    Ts=[p[0] for p in pairs]
    repaired=[repair(*p) for p in pairs]
    C=[v[1] for v in repaired]
    Delta=max(v for r in repaired for v in r[4])
    maxjoint=F(0); maxeta2=F(0); maxcoarse=F(0)
    winner_joint=None; winner_eta=None
    for policy in product(range(2),repeat=2**DEPTH-1):
        laws=[record_probs(Ts,policy,[F(i==x) for i in range(N)]) for x in range(N)]
        coarse=[record_probs(C,policy,[F(i==a) for i in range(K)]) for a in range(K)]
        joint=sum(PI[x]*sum(abs(laws[x][r]-coarse[LABEL[x]][r]) for r in range(2**DEPTH))/2 for x in range(N))
        assert joint<=DEPTH*Delta
        if joint>maxjoint: maxjoint,winner_joint=joint,policy
        actual=[sum(PI[x]*laws[x][r] for x in range(N)) for r in range(2**DEPTH)]
        model=[sum(F(1,2)*coarse[a][r] for a in range(K)) for r in range(2**DEPTH)]
        tv=sum(abs(x-y) for x,y in zip(actual,model))/2
        maxcoarse=max(maxcoarse,tv)
        for event in range(2**(2**DEPTH)):
            f=[sum(row[r] for r in range(2**DEPTH) if event>>r&1) for row in laws]
            pf=[sum(f[x] for x in range(N) if LABEL[x]==a)/4 for a in range(K)]
            eta2=sum(PI[x]*(f[x]-pf[LABEL[x]])**2 for x in range(N))
            assert eta2<=DEPTH*Delta
            if eta2>maxeta2: maxeta2,winner_eta=eta2,(policy,event)
    eps=max(math.sqrt(float(r[2])) for r in repaired)
    receipt={
        'status':'PASS','scope':'Exact population algebra; no data acquisition, hardware test or end-to-end finite confidence budget',
        'hidden_states':N,'visible_labels':K,'operations':2,'frozen_hidden_bit':True,
        'all_depth_three_feedback_policies':2**(2**DEPTH-1),'all_record_events_per_policy':2**(2**DEPTH),
        'epsilon_squared':[str(r[2]) for r in repaired],
        'repair_conditional_TV':[[str(v) for v in r[3]] for r in repaired],
        'conditional_TV_bounds':[[str(v) for v in r[4]] for r in repaired],
        'Delta':str(Delta),'three_stage_joint_bound':str(DEPTH*Delta),
        'exact_max_joint_initial_hidden_and_record_TV':str(maxjoint),'max_joint_TV_float':float(maxjoint),
        'exact_max_baseline_coarse_record_TV':str(maxcoarse),
        'exact_max_omitted_effect_norm_squared':str(maxeta2),'max_omitted_effect_norm':math.sqrt(float(maxeta2)),
        'certificate_eta_three':min(.5,math.sqrt(float(DEPTH*Delta))),
        'illustrative_40_stage_original_eta':min(.5,eps/2*sum(math.sqrt(2)**i for i in range(40))),
        'illustrative_40_stage_transport_eta':min(.5,math.sqrt(float(40*Delta))),
        'note_on_40_stages':'Certificate evaluation only; no enumeration of depth40 policies. Differing-weight old Gamma bound is at least the displayed Gamma=1 comparison.',
        'proof_sha256':hashlib.sha256(Path(__file__).with_name('POSITIVE_FLUX_REPAIR_AND_FULL_RECORD_BOUND.md').read_bytes()).hexdigest(),
    }
    out=Path(__file__).with_name('POSITIVE_FLUX_REPAIR_EXACT_CHECK.json')
    out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()

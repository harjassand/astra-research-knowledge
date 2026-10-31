#!/usr/bin/env python3
"""Exact common-generator fixtures, physical coarse-graining and clock inversion.

All word laws here are computed mathematical inputs. No experimental records
or independent stationary preparations have been acquired by these controls.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
from collections import defaultdict
import json
import sys
import time

ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'outputs/coherent_generator'
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT/'work'))
from aliasfree import plan,reconstruct,erlang_plan
from entropy_cone import log_bounds
from ctmc_reflection_control import exp_negative_bounds,dyadic_enclose


def identity(m):return [[Q(i==j) for j in range(m)] for i in range(m)]
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),Q(0)) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A,v):return [sum((a*b for a,b in zip(row,v)),Q(0)) for row in A]


def inverse(A):
    m=len(A);out=[list(row)+eye for row,eye in zip(A,identity(m))]
    for k in range(m):
        pivot=next(i for i in range(k,m) if out[i][k]);out[k],out[pivot]=out[pivot],out[k]
        scale=out[k][k];out[k]=[x/scale for x in out[k]]
        for i in range(m):
            if i==k:continue
            factor=out[i][k]
            if factor:out[i]=[x-factor*y for x,y in zip(out[i],out[k])]
    return [row[m:] for row in out]


def inspection(P,cap,clock):
    m=len(P);A=[[(cap+clock)*Q(i==j)-cap*P[i][j] for j in range(m)] for i in range(m)]
    return [[clock*x for x in row] for row in inverse(A)]


def word_probability(P,pi,labels,word):
    mass=[p*Q(a==word[0]) for p,a in zip(pi,labels)]
    for letter in word[1:]:mass=[sum((mass[i]*P[i][j] for i in range(len(pi))),Q(0))*Q(labels[j]==letter) for j in range(len(pi))]
    return sum(mass)


def predictions(P,labels,L):
    out={():[Q(1)]*len(P)}
    for length in range(1,L+1):
        for word in product((0,1),repeat=length):
            b,w=word[0],word[1:]
            out[word]=mv(P,[v*Q(a==b) for v,a in zip(out[w],labels)])
    return out


def source_model(b=Q(1,2)):
    states=list(product((-1,1),repeat=2));index={state:i for i,state in enumerate(states)};P=[[Q(0)]*4 for _ in range(4)]
    for i,(s,t) in enumerate(states):
        P[i][index[s,-t]]=(1+b*s*t)/2;P[i][index[-s,t]]=(1-b*s*t)/2
    return P,[Q(1,4)]*4,[int(s<0) for s,t in states]


def entropy_bounds(J):
    low=high=Q(0)
    for i,row in enumerate(J):
        for j,mass in enumerate(row):
            if not mass:continue
            assert J[j][i]>0
            lo,hi=log_bounds(mass/J[j][i],100);low+=mass*lo;high+=mass*hi
    return dyadic_enclose(low,high,96)


def simplex_round(probabilities,k):
    cumulative=[];total=Q(0);breaks={Q(0),Q(1)}
    for p in probabilities:
        total+=k*p;cumulative.append(total)
        frac=total-(total.numerator//total.denominator)
        if frac:breaks.add(1-frac)
    assert total==k
    points=sorted(breaks);out=defaultdict(Q)
    for lo,hi in zip(points,points[1:]):
        U=(lo+hi)/2;last=0;counts=[]
        for c in cumulative:
            value=c+U;floor=value.numerator//value.denominator
            counts.append(floor-last);last=floor
        out[tuple(counts)]+=hi-lo
    assert sum(out.values())==1
    assert all(sum(c)==k and min(c)>=0 for c in out)
    for j,p in enumerate(probabilities):assert sum(w*c[j]/k for c,w in out.items())==p
    return dict(out)


def quantize(P,pi,labels,plus,minus,L,k):
    leaves=list(product((0,1),repeat=L));rounds=[];nodes=set()
    for x in range(len(P)):
        rp=simplex_round([plus[w][x] for w in leaves],k)
        rm=simplex_round([minus[w][x] for w in leaves],k);row={}
        for (p,wp),(m,wm) in product(rp.items(),rm.items()):row[labels[x],p,m]=wp*wm
        rounds.append(row);nodes.update(row)
    nodes=sorted(nodes);idx={node:i for i,node in enumerate(nodes)};n=len(nodes);J=[[Q(0)]*n for _ in range(n)]
    for x,y in product(range(len(P)),repeat=2):
        if not P[x][y]:continue
        for (i,wi),(j,wj) in product(rounds[x].items(),rounds[y].items()):J[idx[i]][idx[j]]+=pi[x]*P[x][y]*wi*wj
    mu=list(map(sum,J));assert all(mu[i]>0 and sum(J[j][i] for j in range(n))==mu[i] for i in range(n))
    R=[[x/mu[i] for x in row] for i,row in enumerate(J)]
    return nodes,J,mu,R,leaves


def node_prefix(node,side,word,leaves,k):
    return sum((Q(n,k) for n,w in zip(node[side+1],leaves) if w[:len(word)]==word),Q(0))


def conditional_generator_controls(P,pi,labels):
    cap=Q(1);count=0
    for clock in (Q(1),Q(2)):
        B=inspection(P,cap,clock);back=[[pi[j]*B[j][i]/pi[i] for j in range(4)] for i in range(4)]
        pr=predictions(B,labels,2);mr=predictions(back,labels,2)
        Pback=[[pi[j]*P[j][i]/pi[i] for j in range(4)] for i in range(4)]
        for transition,fields in ((P,pr),(Pback,mr)):
            for word,values in fields.items():
                if not word:continue
                b,w=word[0],word[1:]
                rhs=[(cap+clock)*values[x]-clock*Q(labels[x]==b)*fields[w][x] for x in range(4)]
                assert mv(transition,values)==rhs
                count+=4
        for word in product((0,1),repeat=3):
            value=sum(pi[x]*Q(labels[x]==word[1])*mr[word[0],][x]*pr[word[2],][x] for x in range(4))
            assert value==word_probability(B,pi,labels,word)
    # Independent inspections are resolvents, not uniformization events.
    P2=[[Q(1,2)]*2 for _ in range(2)];B2=inspection(P2,Q(2),Q(2))
    assert B2==[[Q(3,4),Q(1,4)],[Q(1,4),Q(3,4)]] and B2!=P2
    return {'exact_resolvent_conditional_identities':count,'inspection_vs_uniformization_counterexample_checked':True}


def finite_physical_approximation(P,pi,labels):
    source_entropy=entropy_bounds([[pi[i]*P[i][j] for j in range(4)] for i in range(4)])
    back=[[pi[j]*P[j][i]/pi[i] for j in range(4)] for i in range(4)]
    plus=predictions(P,labels,2);minus=predictions(back,labels,2);out=[]
    for k in (4,8,16):
        nodes,J,mu,R,leaves=quantize(P,pi,labels,plus,minus,2,k)
        bounds=entropy_bounds(J);assert bounds[0]<=source_entropy[1]
        maxTV=Q(0)
        for length in range(1,6):
            tv=sum(abs(word_probability(P,pi,labels,w)-word_probability(R,mu,[n[0] for n in nodes],w)) for w in product((0,1),repeat=length))/2
            maxTV=max(maxTV,tv)
        elo,ehi=exp_negative_bounds(Q(1));mass=sum((Q(1,__import__('math').factorial(j)) for j in range(5)),Q(0))
        tail=1-elo*mass
        out.append({'mesh':k,'source_specific_support_nodes':len(nodes),
                    'new_generator_escape_cap':'1','entropy_interval':[str(x) for x in bounds],
                    'entropy_preview':float(sum(bounds)/2),
                    'max_fine_word_TV_through_length5':str(maxTV),
                    'full_observed_path_TV_upper_on_time1':float(min(Q(1),maxTV+tail)),
                    'scope':'source-specific physical approximation, not a generic inverse-program state-count assumption'})
    return out


def inspection_quantization(P,pi,labels):
    cap=clock=Q(1);B=inspection(P,cap,clock);back=[[B[j][i] for j in range(4)] for i in range(4)]
    pr=predictions(B,labels,1);mr=predictions(back,labels,1)
    nodes,J,mu,R,leaves=quantize(P,pi,labels,pr,mr,1,8)
    maximum=Q(0)
    for i,node in enumerate(nodes):
        for side,b in product((0,1),(0,1)):
            val=node_prefix(node,side,(b,),leaves,8)
            nxt=sum((J[i][j] if side==0 else J[j][i])*node_prefix(other,side,(b,),leaves,8) for j,other in enumerate(nodes))
            residual=cap*nxt-mu[i]*((cap+clock)*val-clock*Q(node[0]==b))
            assert abs(residual)<=(cap+clock)*mu[i]/8
            maximum=max(maximum,abs(residual)/mu[i])
    actual=inspection(R,cap,clock);err=Q(0)
    for w in product((0,1),repeat=3):
        predicted=sum(mu[i]*Q(n[0]==w[1])*node_prefix(n,1,(w[0],),leaves,8)*node_prefix(n,0,(w[2],),leaves,8) for i,n in enumerate(nodes))
        true=word_probability(B,pi,labels,w)
        assert predicted==true
        err=max(err,abs(word_probability(actual,mu,[n[0] for n in nodes],w)-true))
    assert err<=2*(cap+clock)/8/clock
    return {'source_specific_support_nodes':len(nodes),'exact_data_features_preserved':True,
            'maximum_conditional_residual_per_mass':str(maximum),
            'actual_new_generator_triple_error':str(err),
            'one_generator_realized':True,'finite_tolerance_not_claimed_exact_data_reproduction':True}


def fixed_time_correlation(P,pi,labels,t,order=100):
    f=[1 if y==0 else -1 for y in labels];vector=list(map(Q,f));total=Q(0);term=Q(1);mass=Q(0)
    for k in range(order+1):
        total+=term*sum(pi[i]*f[i]*vector[i] for i in range(len(pi)));mass+=term
        vector=mv(P,vector);term*=t/(k+1)
    elo,ehi=exp_negative_bounds(t);tail=1-elo*mass
    return dyadic_enclose(min(elo*total,ehi*total)-tail,max(elo*total,ehi*total)+tail,96)


def inversion_controls(P,pi,labels):
    f=[1 if y==0 else -1 for y in labels];out=[]
    for clock,t in ((Q(8),Q(1,4)),(Q(8),Q(1)),(Q(1),Q(4))):
        specification=plan(1,clock,t,Q(1,100),Q(1,40),160)
        B=inspection(P,Q(1),clock);vector=list(map(Q,f));moments=[]
        for j in range(specification['degree']+1):
            moments.append(sum(pi[i]*f[i]*vector[i] for i in range(4)));vector=mv(B,vector)
        result=reconstruct(specification,moments);true=fixed_time_correlation(P,pi,labels,t)
        assert Q(result['lower'])<=true[0]<=true[1]<=Q(result['upper'])
        out.append({'clock_rate':str(clock),'physical_time':str(t),'degree':specification['degree'],
                    'amplification':specification['moment_amplification_preview'],
                    'operator_error_upper':specification['operator_error_preview'],
                    'true_correlation_interval':[str(x) for x in true],
                    'reconstruction_interval':[result['lower_preview'],result['upper_preview']],
                    'sufficient_independent_preparations':specification['sufficient_independent_preparations'],
                    'sufficient_binary_readouts':specification['sufficient_binary_readouts'],
                    'expected_model_duration':specification['expected_model_duration'],
                    'new_acquired_records':0,
                    'scope':'exact-law arithmetic reconstruction and sufficient budget only; not acquired data or a power claim',
                    'ordinary_Erlang_design':erlang_plan(1,t,Q(1,100),Q(1,40))})
    return out


def main():
    start=time.perf_counter();P,pi,labels=source_model();B=inspection(P,Q(1),Q(1))
    for name,R in [('driven',P),('reversible',[[Q(1,2) if sum(a!=b for a,b in zip(s,t))==1 else Q(0) for t in product((-1,1),repeat=2)] for s in product((-1,1),repeat=2)])]:
        observed=inspection(R,Q(1),Q(1));prob=[word_probability(observed,pi,labels,w) for w in product((0,1),repeat=3)]
        data={'alphabet_size':2,'depth':1,'kinetic_cap':'1','inspection_rate':'1',
              'probabilities':list(map(str,prob)),'input_status':'exact mathematical source law; no observations acquired'}
        (HERE/(name+'_input.json')).write_text(json.dumps(data,indent=2)+'\n')
    out={'scope':__doc__,'generator_identities':conditional_generator_controls(P,pi,labels),
         'finite_physical_approximations':finite_physical_approximation(P,pi,labels),
         'inspection_coordinate_quantization':inspection_quantization(P,pi,labels),
         'aliasfree_reconstructions':inversion_controls(P,pi,labels),
         'status':'COHERENT_GENERATOR_EXACT_CONTROLS_PASSED','new_record_acquisitions':0,
         'seconds':time.perf_counter()-start}
    (HERE/'control_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'generator':out['generator_identities'],
        'physical_approximations':out['finite_physical_approximations'],
        'inversions':[{'clock':v['clock_rate'],'time':v['physical_time'],'degree':v['degree'],
                      'amplification':v['amplification'],'sufficient_preparations':v['sufficient_independent_preparations']} for v in out['aliasfree_reconstructions']],
        'seconds':out['seconds']},indent=2))


if __name__=='__main__':main()

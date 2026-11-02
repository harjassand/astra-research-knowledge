#!/usr/bin/env python3
"""Exact seven-state launch, including all source/overlap exits and clock."""
from fractions import Fraction as F
from pathlib import Path
import json

P=Path(__file__).resolve().parent
Y=((0,0,0),(1,1,0),(2,1,1),(3,2,2))

def arm(b,c,a,peer0,start):
    r=(a[1]*(b+1),2*a[2]*(b+1)*(c+1),
       6*a[3]*(b+2)*(b+1)*(c+2)*(c+1))
    h=((('neutral',a[0],0),),
       (('repaying',a[0],-1),('repaying',2*a[1]*(b+1),-1)),
       (('harmful',a[0],2),('harmful',3*a[1]*(b+2),2),
        ('harmful',6*a[2]*(b+2)*(c+2),3)))
    reach=start;clock=F(0);out=[];occupation=[]
    for phase in range(3):
        total=r[phase]+sum(v for _,v,_ in h[phase])+peer0
        occupation.append(reach/total);clock+=reach/total
        for source,(kind,rate,delta) in enumerate(h[phase]):out.append((kind,phase+1,reach*rate/total,delta,source))
        out.append(('clean' if phase<2 else 'unclean',phase+1,reach*peer0/total,0,None))
        reach*=F(r[phase],total)
    return out,clock,reach,occupation,r

def launch(base,a=(1,1,1,1),b=(1,1,1,1)):
    bb,c,e,f=base;s=a[0]+b[0]
    o1,t1,ret1,occ1,r1=arm(bb,c,a,b[0],F(a[0],s))
    o2,t2,ret2,occ2,r2=arm(e,f,b,a[0],F(b[0],s))
    kill=1-ret1-ret2
    assert kill>0
    probs={k:F(0) for k in ('neutral','repaying','harmful','clean','unclean')}
    delta=F(0);second=F(0)
    for kind,phase,p,d,_ in o1+o2:
        probs[kind]+=p/kill;delta+=p*d/kill;second+=p*d*d/kill
    assert sum(probs.values())==1
    # All identities here are on COMPLETE first absorption, not one excursion.
    assert a[0]*occ1[0]==F(a[0],b[0])*(b[0]*occ1[0])
    assert b[0]*occ2[0]==F(b[0],a[0])*(a[0]*occ2[0])
    assert r1[2]*occ1[2]<=r1[0]*occ1[0]
    assert r2[2]*occ2[2]<=r2[0]*occ2[0]
    cb=max(F(a[1]*(a[0]+a[1]+a[2]),a[3]*b[0]),
           F(b[1]*(b[0]+b[1]+b[2]),b[3]*a[0]))
    cc=max(F(a[0],b[0]),F(b[0],a[0]))
    cu=max(F(a[1],6*a[3]),F(b[1],6*b[3]))
    assert probs['harmful']<=cb*probs['clean']
    assert probs['neutral']<=cc*probs['clean']
    assert probs['unclean']<=cu*probs['clean']
    assert probs['repaying']+probs['clean']>=1/(1+cb+cc+cu)
    joint=[]
    m=lambda a:(0,2,4)[a] if a<3 else 7
    Z=lambda x:15+sum(x)-m(x[0])-m(x[3])
    for block,events in enumerate((o1,o2)):
        for kind,phase,p,d,source in events:
            pre=[0,bb,c,0,e,f];off=3*block
            for j in range(3):pre[off+j]+=Y[phase][j]
            out=pre.copy()
            if source is None:
                off2=3*(1-block)
                for j in range(3):out[off2+j]+=Y[1][j]
            else:
                for j in range(3):out[off+j]+=Y[(source+1)%4][j]-Y[source][j]
            assert min(out)>=0 and Z(out)-Z(pre)==d
            joint.append({'active_block':block,'active_phase':phase,'exit_type':kind,
                          'own_raw_source_index':source,'probability_exact':str(p/kill),
                          'actual_pre_event_state':list(map(str,pre)),
                          'actual_output_state':list(map(str,out)),'delta_Z':d})
    assert sum(F(v['probability_exact']) for v in joint)==1
    return {'base':list(map(str,base)),'alpha':a,'beta':b,
            'probabilities':{k:str(v) for k,v in probs.items()},
            'physical_mean':str((F(1,s)+t1+t2)/kill),
            'mass_mean':str(delta),'mass_second':str(second),
            'harmful_cost_over_clean_probability':str(3*probs['harmful']/probs['clean']),
            'uniform_bound_on_that_ratio':str(3*cb),
            'probabilities_float':{k:float(v) for k,v in probs.items()},
            'physical_mean_float':float((F(1,s)+t1+t2)/kill),
            'complete_actual_joint_exit_law':joint}

def main():
    fixtures=((0,0,0,0),(0,0,100,100),(3,3,10000,10000),
              (100,100,10000,10000),(10000,10000,10000,10000),
              (0,10000,10000,0),(10**25,10**25,10**100,10**100))
    rows=[]
    for a,b in (((1,1,1,1),(1,1,1,1)),((1,2,3,5),(2,1,4,3))):
        for base in fixtures:rows.append(launch(base,a,b))
    out={'exact_cases':rows,
         'scope':'Exact complete seven-state killed law and uniform repayment/activation identities; no general global recurrence or independent audit.'}
    (P/'results/star_launch_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'exact_cases':len(rows),'summary':[
        {'base':v['base'],'alpha':v['alpha'],'mean_time':v['physical_mean_float'],
         'probabilities':v['probabilities_float'],
         'harmful_cost_over_clean_probability':float(F(v['harmful_cost_over_clean_probability']))}
        for v in rows[:7]]},indent=2))

if __name__=='__main__':main()

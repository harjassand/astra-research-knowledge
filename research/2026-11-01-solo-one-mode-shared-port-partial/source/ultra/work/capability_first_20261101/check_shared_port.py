"""Exact raw-generator checks for acquired shared-port Foster functions."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json
import random
from shared_port_modules import acquire,actual_check,norm,make_state


def generated(rng,k):
    specs=[];dimension=1
    for j in range(k):
        width=rng.randint(1,2);vv=[rng.randint(1,2) for _ in range(width)]
        r=rng.randint(1,3);steps=rng.randint(1,2);m=rng.randint(0,3)
        cc=[v*steps+rng.randint(0,1) for v in vv]
        specs.append((list(range(dimension,dimension+width)),r,vv,steps,m,cc,rng.randint(0,2)))
        dimension+=width
    catalyst=dimension;dimension+=1
    x0=[0]+[rng.randint(0,5) for _ in range(dimension-2)]+[rng.randint(0,3)]
    raw=[]
    for indices,r,vv,steps,m,cc,cat in specs:
        vertices=[]
        for z in range(steps+1):
            y=[0]*dimension;y[0]=m+r*z;y[catalyst]=cat
            for i,v,c in zip(indices,vv,cc):y[i]=c-v*z
            vertices.append(tuple(y))
        for i,y in enumerate(vertices):
            raw.append((y,vertices[(i+1)%len(vertices)],F(rng.randint(1,7),rng.randint(1,3))))
    return raw,tuple(x0)


def check(cert,rng):
    if cert['kind']=='bounded':
        # Its acquired norm is a plus finitely bounded phase contributions.
        coordinate_sets=[]
        for b in cert['blocks']:
            c=b['cert']
            width=c['outside_high']-c['outside_low'] if c['kind']=='bounded_outside' else 0
            coordinate_sets.append(sorted({0,width//2,width}))
        count=0
        for qs in product(*coordinate_sets):
            offset=norm(cert,0,qs)
            a=max(0,cert['head']-offset)
            assert cert['lam']*(cert['t']-1)-cert['mu']*a*(1-1/cert['t'])<=-cert['nu']
            assert sum(make_state(cert,a,qs))<=cert['count_offset']+cert['count_slope']*norm(cert,a,qs)
            count+=1
        return count
    count=0;blocks=cert['blocks']
    for a in range(cert['M']+cert['shift']+2):
        for _ in range(10):
            coordinates=[]
            for b in blocks:
                c=b['cert']
                if c['kind']=='rank_one_profile':coordinates.append(rng.randrange(0,2*c['Z0']+2))
                elif c['kind']=='bounded_outside':coordinates.append(rng.randrange(c['outside_high']-c['outside_low']+1))
                else:coordinates.append(0)
            actual_check(cert,a,coordinates);count+=1
            xx=make_state(cert,a,coordinates)
            assert sum(xx)<=cert['count_offset']+cert['count_slope']*norm(cert,a,coordinates)
    # All competing bulk orders, dormant inputs, last-copy entrances and head
    # thresholds. Large exponentials are canceled, never materialized.
    bases=[0]*len(blocks)
    for i,b in enumerate(blocks):
        c=b['cert']
        if c['kind']=='rank_one_profile':
            for q in [c['Z0'],b['qcut']-1,b['qcut'],cert['head']+b['qcut'],10**100+cert['head']]:
                for a in sorted({0,max(0,cert['M']-1),cert['M'],cert['Acut']-1,cert['Acut']}):
                    coordinates=bases.copy();coordinates[i]=q
                    actual_check(cert,a,coordinates);count+=1
    for a in [cert['head'],cert['head']+1]:actual_check(cert,a,bases);count+=1
    all_large=[cert['head']+b.get('qcut',0) if b['cert']['kind']=='rank_one_profile' else 0 for b in blocks]
    for a in [0,cert['M'],cert['Acut']]:actual_check(cert,a,all_large);count+=1
    assert cert['rho']>1 and cert['rho']**cert['count_slope']<=cert['t']
    assert cert['stationary_total_moment_bound']['coefficient']>0
    return count


def main():
    rng=random.Random(11010937)
    named=[
      ([((1,0),(0,1),1),((0,1),(1,0),1)],(0,7)),
      ([((1,2,0),(2,1,0),1),((2,1,0),(3,0,0),2),((3,0,0),(1,2,0),3),
        ((2,0,2),(3,0,1),5),((3,0,1),(4,0,0),7),((4,0,0),(2,0,2),11)],(0,4,5)),
      ([((0,0,1),(1,1,0),1),((1,1,0),(0,0,1),2)],(0,2,3))]
    rows=[];total=0
    for i,(raw,x0) in enumerate(named+[generated(rng,1+i%3) for i in range(12)]):
        lam,mu=F(rng.randint(1,3),rng.randint(1,3)),F(rng.randint(1,3),rng.randint(1,3))
        cert=acquire(raw,x0,lam,mu);count=check(cert,rng);total+=count
        rows.append(dict(input=i,species=len(x0),channels=len(raw),blocks=len(cert['blocks']),
                         acquired=cert['kind'],profile_exponent=cert.get('p'),head_bits=cert['head'].bit_length(),
                         exact_states=count))
    # A bounded internal phase alongside two nonlinear unbounded modules.
    raw0,x00=named[1];raw=[]
    for y,z,k in raw0:raw.append((tuple(y)+(0,0),tuple(z)+(0,0),k))
    raw += [((0,0,0,0,1),(1,0,0,1,0),1),((1,0,0,1,0),(0,0,0,0,1),3)]
    cert=acquire(raw,(0,4,5,2,3));count=check(cert,rng);total+=count
    rows.append(dict(input='bounded_phase_join',species=5,channels=len(raw),blocks=len(cert['blocks']),
                     acquired=cert['kind'],profile_exponent=cert.get('p'),head_bits=cert['head'].bit_length(),exact_states=count))
    # The completed cubic prototype has a genuinely higher-rank coupled block.
    prototype=[((2,1,0),(0,2,1),1),((0,2,1),(1,0,2),2),
               ((1,0,2),(1,1,1),3),((1,1,1),(2,1,0),5)]
    rejected=False
    try:acquire(prototype,(0,7,0))
    except ValueError as e:rejected='rank exceeds one' in str(e)
    assert rejected
    result=dict(exact_state_checks=total,raw_inputs=len(rows),cases=rows,
                coupled_rank_two_scope_rejection=True,
                factored_stationary_total_count_moments_acquired=True,
                inference='These exact controls supplement the general source-dominance and shared-head proof; they do not establish its universal quantifiers.')
    Path('outputs/capability_first_20261101/shared_port_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

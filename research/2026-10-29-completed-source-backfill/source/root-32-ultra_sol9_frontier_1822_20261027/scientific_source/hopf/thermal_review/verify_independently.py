#!/usr/bin/env python3
"""Independent exact consumer: no producer import or producer verifier.

Saved exact traces are checked as inputs. This implementation uses Horner
summation and the independent coarse tail bound e^x<=3^ceil(x), rather than
the author's exponential-tail evaluator or Chebyshev/multiple-precision code.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import factorial,ceil,gcd,prod
from functools import lru_cache
import json,time,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)

HERE=Path(__file__).resolve().parent
WORK=HERE.parents[1]
PRIOR=WORK.parent/'sol8_opportunity_selection_20261027/obstruction_first/continuation/data'
THERMAL=WORK/'thermal/results'

def plus(x,y):return x[0]+y[0],x[1]+y[1]
def times(a,x):return (a*x[0],a*x[1]) if a>=0 else (a*x[1],a*x[0])
def difference(x,y):return x[0]-y[1],x[1]-y[0]

@lru_cache(None)
def exponential(x):
    x=Q(x)
    if x<0:
        lo,hi=exponential(-x);return 1/hi,1/lo
    degree=256
    assert x<=30
    term=Q(1);s=Q(1)
    for j in range(1,degree+1):term=term*x/j;s+=term
    return s,s+term*x/(degree+1)/(1-x/(degree+2))

def trace_box(rec,beta,bonds):
    a=[int(v) for v in rec['trace_2H_powers']]
    d=len(a)-1;t=-beta/2;value=Q(a[-1])
    for k in range(d-1,-1,-1):value=a[k]+t*value/(k+1)
    x=6*bonds*beta
    tail=Q(5**rec['n']*3**ceil(x))*x**(d+1)/factorial(d+1)
    return value-tail,value+tail

def quadratic(c,m,shift):
    z=(Q(0),Q(0))
    for i in range(len(c)):
        for j in range(len(c)):z=plus(z,times(c[i]*c[j],m[i+j+shift]))
    return z

def z4_energy_counts():
    counts={}
    for ja in range(5):
        for jb in range(5):
            for jt in range(abs(ja-jb),ja+jb+1):
                E=(jt*(jt+1)-ja*(ja+1)-jb*(jb+1))//2
                counts[E]=counts.get(E,0)+2*jt+1
    assert sum(counts.values())==625
    return counts

def input_checks(open_records,cycle_records):
    controls=[]
    analytic={1:{0:5},2:{j*(j+1)//2-6:2*j+1 for j in range(5)}}
    triples={}
    for outer in range(5):
        for total in range(abs(outer-2),outer+3):
            E=(total*(total+1)-outer*(outer+1)-6)//2
            triples[E]=triples.get(E,0)+2*total+1
    assert sum(triples.values())==125;analytic[3]=triples
    for n,counts in analytic.items():
        expected=[sum(d*(2*E)**k for E,d in counts.items()) for k in range(193)]
        assert expected==list(map(int,open_records[n]['trace_2H_powers']))
        controls.append({'open_chain':n,'all_193_analytic_moments':'PASS'})
    metadata=[]
    for rec in cycle_records:
        n=rec['n'];d=rec['degree'];dim=5**n;a=list(map(int,rec['trace_2H_powers']))
        moduli=rec['CRT_primes'];M=prod(moduli)
        assert len(a)==d+1 and a[0]==dim and a[1]==0
        assert all(gcd(x,y)==1 for i,x in enumerate(moduli) for y in moduli[:i])
        bound=dim*(12*n)**d
        assert int(rec['CRT_modulus'])==M and int(rec['unique_reconstruction_bound'])==bound
        assert M>2*bound and all(abs(v)<=dim*(12*n)**k for k,v in enumerate(a))
        assert a[2]==48*n*dim and a[3]==-48*n*dim
        metadata.append({'twist':rec['twist'],'moment_count':len(a),'moduli':len(moduli),
            'bound_bits':bound.bit_length(),'modulus_bits':M.bit_length(),
            'signed_reconstruction_unique':True,'all_moment_physical_bounds':True})
    return controls,metadata

def run():
    start=time.perf_counter()
    op={r['n']:r for r in json.loads((PRIOR/'open_moments_exact_degree192.json').read_text())['chains']}
    tw={r['twist']:dict(r,n=4) for r in json.loads((PRIOR/'twisted4_moments_exact_degree192.json').read_text())['records']}
    cycle_data=json.loads((THERMAL/'cycle6_moments_exact_degree192.json').read_text())
    six={r['twist']:r for r in cycle_data['records']};assert set(six)=={'I','P'}
    controls,metadata=input_checks(op,list(six.values()))
    counts=z4_energy_counts();rows=[]
    choices=[(Q(3,4),[Q(8,625),Q(-91,100),Q(-1)],Q(233,25),Q(3),Q(21,5),Q(184,25),4),
             (Q(3,2),[Q(37,100),Q(-1),Q(-17,1000)],Q(285),Q(141),Q(197),Q(257),6)]
    for beta,c,theta,ri,ro,rn,pn in choices:
        moments=[(Q(1),Q(1)),(Q(1),Q(1))]
        moments += [times(Q(1,5**n),trace_box(op[n],beta,n-1)) for n in range(2,6)]
        norm=quadratic(c,moments,0);numerator=quadratic(c,moments,1)
        gap=numerator[0]-theta*norm[1]
        assert norm[0]>0 and gap>0
        M4=(Q(0),Q(0))
        for E,deg in counts.items():M4=plus(M4,times(Q(deg,625),exponential(-beta*E)))
        P4=times(Q(1,625),trace_box(tw['P'],beta,4))
        C4=times(Q(1,625),trace_box(tw['C'],beta,4))
        I4=times(Q(1,12),plus(plus(M4,times(3,P4)),times(8,C4)))
        O4=times(Q(1,12),difference(plus(M4,times(3,P4)),times(4,C4)))
        if pn==4:N=times(Q(1,4),difference(M4,P4))
        else:N=times(Q(1,4*5**6),difference(trace_box(six['I'],beta,6),trace_box(six['P'],beta,6)))
        residual=I4[1]-theta**4
        assert residual<ri**4 and 0<O4[0] and O4[1]<ro**4
        assert 0<N[0] and N[1]<rn**pn and max(ri,ro,rn)<theta
        tau=(ri/theta)**256+2*(ro/theta)**256+3*(rn/theta)**256
        rows.append({'beta':str(beta),'trial':list(map(str,c)),
            'norm_lower':str(norm[0]),'rayleigh_gap_lower':str(gap),
            'theta_lower':str(theta),'sector_radii':list(map(str,[ri,ro,rn])),
            'I_radius_power_slack':str(ri**4-residual),
            'O_radius_power_slack':str(ro**4-O4[1]),
            'N_moment':pn,'N_radius_power_slack':str(rn**pn-N[1]),
            'tau_upper':str(tau),'tau_upper_float_diagnostic':float(tau)})
    twarm,tcold=(Q(row['tau_upper']) for row in rows)
    assert 4*twarm<Q(1,10**24) and 2*tcold<Q(3,10**11)
    result={'status':'INDEPENDENT_EXACT_CONNECTED_INCREMENT_PASS',
        'analytic_controls':controls,'cycle6_CRT_metadata':metadata,'rows':rows,
        'connected_increment_strict_lower':'-3/100000000000',
        'connected_increment_strict_upper':'1/1000000000000000000000000',
        'S256_beta3over2_strict_lower':'1-3/100000000000',
        'cold_lower_arithmetic_slack':str(Q(3,10**11)-2*tcold),
        'connected_upper_arithmetic_slack':str(Q(1,10**24)-4*twarm),
        'scope':'one connected increment; no later increments, final cold temporal purity, uniform gap or physical claim',
        'seconds':time.perf_counter()-start}
    (HERE/'REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'tau_upper_float_diagnostics':[float(twarm),float(tcold)],
        'controls':controls,'cycle6_CRT_metadata':metadata,'seconds':result['seconds']},indent=2))

if __name__=='__main__':run()

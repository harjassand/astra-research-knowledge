"""Directed one-dimensional Gibbs moments for the two specified N32 accesses.

Composite Simpson values carry an explicit fourth-derivative remainder
on every interval. Gaussian tail bounds close the infinite domain.
There is no quadrature-library success flag, Bessel oracle or trajectory.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D
import json,hashlib,sys,time

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'independent_construction'))
from decimal_intervals import I,DN,UP,NEAR
DN.prec=UP.prec=NEAR.prec=80

def qi(x):
    x=F(x);return I(x.numerator)/x.denominator

def derivative_four(beta,m):
    p={m:F(1)}
    for _ in range(4):
        q={}
        for k,c in p.items():
            if k:q[k-1]=q.get(k-1,F(0))+k*c
            q[k+1]=q.get(k+1,F(0))-c
            q[k+3]=q.get(k+3,F(0))-beta*c
        p={k:c for k,c in q.items() if c}
    return [qi(abs(p.get(k,F(0)))).hi for k in range(max(p)+1)]

def abs_poly_upper(coeff,x):
    z=D(0)
    for c in reversed(coeff):z=UP.add(UP.multiply(z,x),c)
    return z

def moment_case(name,d,g,cells=2048):
    start=time.perf_counter();beta=d*d/2;B=qi(beta)
    L=D(12);step=L/D(cells);half=step/2
    nodes=[D(j)*half for j in range(2*cells+1)]
    exponentials=[]
    for x in nodes:
        z=I(x);q=z.sq()/2+B*z.sq().sq()/4
        exponentials.append((-q).exp())
    vals={m:[z*I(x).sq() if m==2 else z for x,z in zip(nodes,exponentials)] for m in [0,2]}
    totals={m:I(0) for m in [0,2]};errors={m:D(0) for m in [0,2]}
    coeff={m:derivative_four(beta,m) for m in [0,2]}
    hfactor=qi(F(step)**5/2880).hi
    for j in range(cells):
        right=nodes[2*j+2];left_exp=exponentials[2*j].hi
        for m in [0,2]:
            v=vals[m]
            totals[m]=totals[m]+(v[2*j]+4*v[2*j+1]+v[2*j+2])*I(step)/6
            derivative=UP.multiply(left_exp,abs_poly_upper(coeff[m],right))
            errors[m]=UP.add(errors[m],UP.multiply(hfactor,derivative))
    gaussian=(-I(L).sq()/2).exp()
    tails={0:(gaussian/I(L)).hi,2:(gaussian*(I(L)+1/I(L))).hi}
    integrals={m:I(DN.subtract(totals[m].lo,errors[m]),
                   UP.add(UP.add(totals[m].hi,errors[m]),tails[m])) for m in [0,2]}
    assert integrals[0].lo>0
    m2=integrals[2]/integrals[0]
    local_variance=qi(d)*m2
    contrast=qi(g*g/d)*(1-m2)
    assert 0<m2.lo<m2.hi<1 and contrast.lo>0
    return {
      'name':name,'N':32,'theta':'1','Delta':'1/2','observed_port':1,'quartic_vertex':32,
      'Rpp_equals_Rvv':str(d),'Rpv':str(g),'standardized_quartic_beta':str(beta),
      'integration_domain':['0','12'],'Simpson_cells':cells,'exponential_nodes':len(nodes),
      'half_line_integrals':{str(m):integrals[m].encode() for m in [0,2]},
      'summed_Simpson_remainder':{str(m):str(errors[m]) for m in [0,2]},
      'Gaussian_tail_upper':{str(m):str(tails[m]) for m in [0,2]},
      'standardized_second_moment':m2.encode(),'hidden_variance_at_Delta':local_variance.encode(),
      'stationary_port_variance_decrease_at_Delta':contrast.encode(),
      'seconds_afterimports':time.perf_counter()-start,
      'scope':'Directed composite Simpson plus analytic global Gaussian tails. Exact known K/theta/one-quartic model; no measured law, trajectory, unqualified numerical quadrature or independent equilibrium sample.'}

def main():
    start=time.perf_counter()
    source=BASE/'thermal_time_trace'/'INTERFACE.json'
    packet=json.loads(source.read_text())
    d=F(packet['b_equals_d']['exact']);g=F(packet['g']['exact'])
    cases=[moment_case('unit_shunted_path_K3',d,g),
           moment_case('shunt_free_path_K2',F(32,33),F(1,33))]
    out={'status':'TWO_ACTUAL_N32_DIRECTED_GIBBS_MOMENT_INPUTS_ACQUIRED',
         'cases':cases,'same_source_interface_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'seconds_afterimports':time.perf_counter()-start,'new_topologies':0,'simulated_trajectories':0,
         'physical_readouts':0,'historical_priority':'UNKNOWN',
         'scope':'Only the two assigned accesses. Physical bath, calibration, sampling and model qualification remain separate.'}
    (HERE/'MOMENTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()

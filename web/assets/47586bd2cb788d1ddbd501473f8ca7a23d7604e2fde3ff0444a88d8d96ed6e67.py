#!/usr/bin/env python3
"""One generic finite Trotter local-filter path with certified output enclosures.

The seed is supplied rational I/2. This is a path component, not acquisition
of the Gibbs seed law, importance resampling, or full quantum preparation.
"""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    out=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(out)
    return out
base=module('iv_path',HERE/'certified_two_spin.py')
normal=module('normal_path',HERE/'certified_normal.py')
root=module('root_path',HERE/'certified_psd_root.py')
IV,iv=base.IV,base.iv


def ci(r=0,i=0): return (iv(r),iv(i))
def ca(x,y): return (x[0]+y[0],x[1]+y[1])
def cm(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def conjugate(x): return (x[0],-x[1])
def cs(x,t): return (x[0]*t,x[1]*t)
def mm(A,B):
    result=[]
    for i in range(2):
        row=[]
        for j in range(2):
            x=ci()
            for k in range(2): x=ca(x,cm(A[i][k],B[k][j]))
            row.append(x)
        result.append(row)
    return result
def adj(A): return [[conjugate(A[j][i]) for j in range(2)] for i in range(2)]
def square(x):
    hi=max(x.lo*x.lo,x.hi*x.hi)
    lo=F(0) if x.lo<=0<=x.hi else min(x.lo*x.lo,x.hi*x.hi)
    return IV(lo,hi)
def filter_matrix(coefficients):
    r=base.sqrt_iv(sum((square(x) for x in coefficients),iv(0)))
    assert r.hi<=1
    c=base.even_series_iv(r,'cosh')
    s=base.even_series_iv(r,'sinch')
    x,y,z=[s*x for x in coefficients]
    return [[ci(c+z),ci(x,-y)],[ci(x,y),ci(c-z)]]
def midpoint(x): return (x.lo+x.hi)/2

# Exact rational complex arithmetic for a positive output description.
def qc(r=0,i=0): return (F(r),F(i))
def qa(x,y): return (x[0]+y[0],x[1]+y[1])
def qm(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def qconj(x): return (x[0],-x[1])
def qmm(A,B):
    return [[qa(qm(A[i][0],B[0][j]),qm(A[i][1],B[1][j])) for j in range(2)] for i in range(2)]
def qadj(A): return [[qconj(A[j][i]) for j in range(2)] for i in range(2)]


def log_scalar(z):
    assert z>0
    x=(z-1)/(z+1)
    assert abs(x)<=F(1,2)
    tol=F(1,1<<(IV.P+8))
    total,term,n=F(0),x,0
    while True:
        total+=2*term/(2*n+1)
        next_term=term*x*x
        rem=2*abs(next_term)/((2*n+3)*(1-x*x))
        base.ledger.see(total,term,rem)
        base.ledger.add('log_atanh_series_terms')
        if rem<=tol: break
        term=next_term
        n+=1
    return IV(total-rem,total+rem)


def main():
    start,cpu=time.perf_counter(),time.process_time()
    N,m,L,ell=64,2,F(4),24
    b=[F(1,32),F(-1,16),F(1,8)]
    t=time.perf_counter()
    root.base.ledger=root.base.Ledger()
    root_data=root.root(root.FIXTURES['rank2'],ell)
    root_cost={**root.base.ledger.snapshot(),'wall_seconds':time.perf_counter()-t}
    normals=[]
    for fraction in [F(1,5),F(2,5),F(3,5),F(4,5),F(1,3),F(2,3)]:
        bits=ell+normal.ceil_fraction(L*L)+8
        raw=(fraction*(1<<bits)).numerator//(fraction*(1<<bits)).denominator
        normal.base.ledger=normal.base.Ledger()
        t=time.perf_counter()
        data=normal.generate(L,ell,raw)
        data['costs']={**normal.base.ledger.snapshot(),'wall_seconds':time.perf_counter()-t}
        normals.append(data)
    base.ledger=base.Ledger()
    IV.precision(80)
    t=time.perf_counter()
    columns=[[IV(F(root_data['root_entry_enclosures'][i][j]['lo']),
                 F(root_data['root_entry_enclosures'][i][j]['hi'])) for i in range(3)] for j in range(3)]
    sn=base.sqrt_iv(iv(N))
    s=sn*base.sqrt_iv(sn)
    scale=1/(2*base.sqrt_iv(iv(2*m))*s)
    g=[[ci(1),ci()],[ci(),ci(1)]]
    order=[]
    for step in range(m):
        for j in range(3):
            zdata=normals[3*step+j]
            z=F(zdata['output_rational'])
            hz=F(zdata['ideal_clipped_normal_coupling_error_upper'])
            zi=IV(z-hz,z+hz)
            g=mm(filter_matrix([zi*scale*x for x in columns[j]]),g)
            order.append({'step':step,'column':j,'normal_rational':str(z),
                          'normal_coupling_enclosure':zi.json()})
        g=mm(filter_matrix([iv(x)/(4*m*s) for x in b]),g)
    tau=[[ci(F(1,2)),ci()],[ci(),ci(F(1,2))]]
    X=mm(mm(g,tau),adj(g))
    trace=X[0][0][0]+X[1][1][0]
    assert trace.lo>0
    rho=[[(x[0]/trace,x[1]/trace) for x in row] for row in X]
    # Positive rational local state from the midpoint trajectory matrix.
    ghat=[[(midpoint(x[0]),midpoint(x[1])) for x in row] for row in g]
    Xhat=qmm(ghat,qadj(ghat))
    Xhat=[[(r/2,i/2) for r,i in row] for row in Xhat]
    that=Xhat[0][0][0]+Xhat[1][1][0]
    assert that>0 and Xhat[0][0][1]==0 and Xhat[1][1][1]==0
    rhohat=[[(r/that,i/that) for r,i in row] for row in Xhat]
    # Congruence construction proves positivity; verify its 2x2 determinant too.
    determinant=rhohat[0][0][0]*rhohat[1][1][0]-(rhohat[0][1][0]**2+rhohat[0][1][1]**2)
    assert determinant>=0 and rhohat[0][0][0]+rhohat[1][1][0]==1
    error=F(0)
    for i in range(2):
        for j in range(2):
            for component in range(2):
                interval=rho[i][j][component]
                x=rhohat[i][j][component]
                error+=max(abs(x-interval.lo),abs(x-interval.hi))
    tensor_error=min(F(1),N*error)
    assert tensor_error<F(1,1000)
    logw=N*IV(log_scalar(trace.lo).lo,log_scalar(trace.hi).hi)
    bloch=[2*rhohat[0][1][0],-2*rhohat[0][1][1],rhohat[0][0][0]-rhohat[1][1][0]]
    assert sum(x*x for x in bloch)<=1
    path_cost={**base.ledger.snapshot(),'wall_seconds':time.perf_counter()-t}
    tail=sum(F(x['normal_tail_probability_upper']) for x in normals)
    data={'worker_id':'c07_s03','status':'CERTIFIED_RETAINED_CLIPPED_LOCAL_FILTER_PATH',
          'input':{'N':N,'m':m,'C':root_data['input_C'],'A':'C-(1/2)I; norm<=1/2 from the acquired PSD/row-norm bound',
                   'b':[str(x) for x in b],'seed_local_state':'I/2 supplied exactly',
                   'field_and_filters_noncommuting':True},
          'root_certificate':root_data,'normal_certificates':normals,'filter_order':order,
          'exact_rational_local_density':[[[str(r),str(i)] for r,i in row] for row in rhohat],
          'exact_rational_local_bloch_vector':[str(x) for x in bloch],
          'local_trace_distance_upper_to_coupled_clipped_path':str(error),
          'N_fold_product_trace_distance_upper_to_coupled_clipped_path':str(tensor_error),
          'local_trace_interval':trace.json(),'ideal_clipped_path_logweight_interval':logw.json(),
          'unclipped_normal_exception_union_bound':str(min(F(1),tail)),
          'ideal_fair_bits_for_all_6_normal_prefixes':sum(x['exact_fair_random_bit_count'] for x in normals),
          'costs':{'root':root_cost,'path_enclosures':path_cost,
                   'total_wall_seconds':time.perf_counter()-start,
                   'total_cpu_seconds':time.process_time()-cpu},
          'local_emission_interface':{'description':'64 identical copies of the returned rational density',
                                     'single_qubit_error_allocation':'Any native per-qubit error d adds at most 64d',
                                     'gate_compilation':'NOT EXECUTED; generic Bloch direction requires finite-angle gate compilation',
                                     'hardware_executed':False},
          'limits':['One supplied seed and one trajectory component, not the target Gibbs mixture',
                    'The normal transcript is deterministic; its ideal fair-bit coupling contract is supplied',
                    'Clipped/unclipped exception union bound is not an importance-weighted Gibbs error bound',
                    'No seed rejection, proposal array, public moment acquisition or final importance selection executed']}
    path=HERE/'evidence'/'generic_filter_path.json'
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'output':str(path),
                      'N_fold_trace_error_upper':float(tensor_error),
                      'local_trace_lo':float(trace.lo),'local_trace_hi':float(trace.hi),
                      'normal_bits':data['ideal_fair_bits_for_all_6_normal_prefixes'],
                      'total_wall_seconds':data['costs']['total_wall_seconds']}))


if __name__=='__main__': main()

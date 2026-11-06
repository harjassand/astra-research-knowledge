"""Replay delivered certificates using only Python's standard library.

No proposal, optimization package, source state or new source call is used.
The checker verifies the finite execution; general theorems are proved in
THEOREM.txt rather than inferred from this finite replay.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import hashlib, json, time
from exact import require, psd, encode
from certify import (assembled_inputs, outer_tasks, ground_certificate,
    residual, energy, design, robust_design_certificate, matrix_bound)

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/'results'/name).read_text())
def vec(x):return list(map(Q,x))
def mat(x):return [vec(r) for r in x]


def polynomial_identity(T,beta,h,p):
    """Compare coefficients of W(q)-W(p) and the nonnegative identity."""
    n=len(p);zero=(0,)*n
    def add(poly,coef,terms):
        key=[0]*n
        for i,degree in terms:key[i]+=degree
        key=tuple(key);poly[key]=poly.get(key,Q(0))+coef
    left={zero:-energy(T,beta,h,p)};right={}
    for i in range(n):
        add(left,beta[i]/4,[(i,4)])
        add(left,T[i][i]/2,[(i,2)])
        add(left,-h[i],[(i,1)])
        add(right,beta[i]/4,[(i,4)])
        add(right,-beta[i]*p[i]**2/2,[(i,2)])
        add(right,beta[i]*p[i]**4/4,[])
        add(right,h[i]/(2*p[i]),[(i,2)])
        add(right,-h[i],[(i,1)])
        add(right,h[i]*p[i]/2,[])
        for j in range(i+1,n):
            c=-T[i][j]
            add(left,-c,[(i,1),(j,1)])
            add(right,c*p[j]/(2*p[i]),[(i,2)])
            add(right,c*p[i]/(2*p[j]),[(j,2)])
            add(right,-c,[(i,1),(j,1)])
    require({k:v for k,v in left.items() if v}=={k:v for k,v in right.items() if v},
            'Global polynomial identity mismatch')
    return len(set(left)|set(right))


def main():
    start=time.perf_counter();I=read('INPUTS.json');n=I['n'];ground_count=0;bracket_count=0
    paths=[ROOT/'inputs'/f'component_{s}_model.json' for s in 'AB']
    require([hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]==I['source_model_sha256'])
    S,d,E,errors=assembled_inputs(paths,Q(I['reciprocal_coupling_calibration_operator_bound']))
    require(encode(S)==I['static_model'] and encode(d)==I['entrywise_outer_radius'])
    require(encode(errors)==I['source_errors_rounded_up'] and E==Q(I['total_static_operator_bound']))
    def check_ground(T,b,h,c):
        nonlocal ground_count
        now=ground_certificate(T,b,h,vec(c['candidate']))
        require(encode(now)==c and now['gap']<Q(1,10**16))
        ground_count+=1
    def check_bracket(T,b,h,c):
        nonlocal bracket_count
        l=vec(c['lower']);u=vec(c['upper'])
        require(all(0<=x<=y for x,y in zip(l,u)))
        if max(u)==0:require(all(f==0 for f in h) and psd(T))
        else:
            require(min(l)>0)
            require(max(residual(T,b,h,l))<=0 and min(residual(T,b,h,u))>=0)
        bracket_count+=1
    C=mat(I['C']);beta=vec(I['beta']);be=vec(I['beta_error']);h=[Q(0)]*n
    for row in read('PHASE_SCAN.json'):
        g=Q(row['g']);T=[[(Q(1) if i==j else Q(0))-g*C[i][j] for j in range(n)] for i in range(n)]
        require(encode(T)==row['T'])
        K=[[S[i][j]-T[i][j] for j in range(n)] for i in range(n)]
        require(encode(K)==row['physical_K'])
        check_ground(T,beta,h,row['nominal'])
        check_bracket(T,beta,h,row['nominal_bracket'])
        lt,ut=outer_tasks(T,beta,h,d,be,h)
        check_ground(*lt,row['lower_outer_task']);check_ground(*ut,row['upper_outer_task'])
        check_bracket(*lt,row['lower_endpoint_bracket']);check_bracket(*ut,row['upper_endpoint_bracket'])
        require(row['source_and_calibration_amplitude_box']['lower']==row['lower_endpoint_bracket']['lower'])
        require(row['source_and_calibration_amplitude_box']['upper']==row['upper_endpoint_bracket']['upper'])
        lo=vec(row['source_and_calibration_amplitude_box']['lower']);hi=vec(row['source_and_calibration_amplitude_box']['upper'])
        require(sum(x*x for x in lo)/n==Q(row['box_mean_intensity_lower']))
        require(sum(x*x for x in hi)/n==Q(row['box_mean_intensity_upper']))
        dis=psd([[T[i][j]-(E if i==j else 0) for j in range(n)] for i in range(n)])
        ordered=not psd([[T[i][j]+(E if i==j else 0) for j in range(n)] for i in range(n)])
        phase='all compatible systems disordered' if dis else ('all compatible systems ordered' if ordered else 'phase not resolved by this outer certificate')
        require(phase==row['phase'])
    P=read('PROGRAMMED_PATTERN.json');p=vec(P['target_amplitude']);beta=vec(P['beta']);h=vec(P['field_in_gauge'])
    T,K=design(p,beta,h,mat(P['W']),S,P['sign_pattern'])
    require(encode(T)==P['T_in_gauge'] and encode(K)==P['physical_K'])
    check_ground(T,beta,h,P['nominal']);coefficients=polynomial_identity(T,beta,h,p)
    cert=robust_design_certificate(T,beta,h,p,d,vec(P['beta_error']),vec(P['field_error']),Q(1,100))
    require(encode(cert)==P['robust_one_percent_certificate'])
    lt,ut=outer_tasks(T,beta,h,d,vec(P['beta_error']),vec(P['field_error']))
    check_ground(*lt,P['lower_endpoint_certificate']);check_ground(*ut,P['upper_endpoint_certificate'])
    check_bracket(*lt,P['tighter_outer_lower']);check_bracket(*ut,P['tighter_outer_upper'])
    controls=read('CONTROLS.json');M=controls['metastability'];T2=mat(M['T']);q2=vec(M['mixed_sign_equilibrium'])
    require(residual(T2,[Q(1)]*2,[Q(0)]*2,q2)==[0,0])
    require(energy(T2,[Q(1)]*2,[Q(0)]*2,q2)==Q(M['energy']))
    H=[[T2[i][j]+(3*q2[i]**2 if i==j else 0) for j in range(2)] for i in range(2)]
    require(encode(H)==M['hessian'] and H==[[7,-1],[-1,7]])
    require(Q(M['global_energy'])==-18 and Q(M['strict_suboptimality_gap'])==10)
    F=controls['frustration_reduction'];edges=F['edges'];m=F['nodes'];y=vec(F['soft_candidate'])
    deg=[sum(i in e for e in edges) for i in range(m)];mass=sum(v*v for v in deg)
    b=Q(F['beta']);require(b==32*mass+4*max(deg)+1)
    minimum=min(sum(s[i]*s[j] for i,j in edges) for s in product((-1,1),repeat=m))
    fv=b/4*sum((v*v-1)**2 for v in y)+sum(y[i]*y[j] for i,j in edges)
    low=Q(minimum)-2*mass/b
    require(Q(F['soft_energy'])==fv and Q(F['certified_soft_lower_energy'])==low)
    require(0<=fv-low<Q(1,8))
    signs=[1 if v>=0 else -1 for v in y]
    require(sum(signs[i]*signs[j] for i,j in edges)==minimum)
    result={'status':'PASS','global_energy_certificates_replayed':ground_count,
            'endpoint_brackets_replayed':bracket_count,
            'exact_design_polynomial_coefficients_checked':coefficients,
            'metastability_checked':True,'frustrated_finite_control_checked':True,
            'new_source_calls':0,'floating_proposal_calls':0,
            'elapsed_seconds':time.perf_counter()-start,
            'scope':'finite execution replay; general proof is in THEOREM.txt'}
    (ROOT/'results/REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

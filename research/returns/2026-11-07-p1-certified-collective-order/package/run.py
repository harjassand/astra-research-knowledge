"""Finite execution of the collective-order certificates; no source calls."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import hashlib, json, time, platform, sys
import numpy as np
import scipy
from scipy.optimize import root, minimize
from exact import dyadic, psd, require
from certify import (matvec, energy, residual, matrix_bound, connected_z,
    ground_certificate, relative_bracket, assembled_inputs, outer_tasks,
    design, robust_design_certificate, max_fraction_bits, save)

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'results';OUT.mkdir(exist_ok=True)
COUNTS={'root_calls':0,'root_function_evaluations':0,'root_jacobian_evaluations':0,
        'minimize_calls':0,'minimize_function_evaluations':0,
        'ground_checks':0,'bracket_checks':0,'new_source_calls':0}


def propose(T,beta,h):
    connected_z(T)
    if all(f==0 for f in h) and psd(T):return [Q(0)]*len(T)
    A=np.array(T,dtype=float);b=np.array(beta,dtype=float);f=np.array(h,dtype=float)
    eig,v=np.linalg.eigh(A);v=np.abs(v[:,0])
    scale=max(.2,np.sqrt(max(.01,-eig[0])/max(1e-12,np.dot(b,v**4))))
    x0=np.maximum(scale*v,.05)
    def F(x):return A@x+b*x**3-f
    def J(x):return A+np.diag(3*b*x*x)
    sol=root(F,x0,jac=J,method='hybr',options={'xtol':1e-11,'maxfev':1000})
    COUNTS['root_calls']+=1;COUNTS['root_function_evaluations']+=int(sol.nfev)
    COUNTS['root_jacobian_evaluations']+=int(getattr(sol,'njev',0))
    x=sol.x
    if min(x)<=1e-7 or max(abs(F(x)))>1e-8:
        def E(x):return .5*x@A@x+np.sum(b*x**4)/4-f@x
        m=minimize(E,np.ones(len(T)),jac=F,method='L-BFGS-B',
                   bounds=[(1e-10,None)]*len(T),options={'maxiter':1000,'ftol':1e-15,'gtol':1e-11})
        COUNTS['minimize_calls']+=1
        COUNTS['minimize_function_evaluations']+=int(m.nfev)
        sol=root(F,m.x,jac=J,method='hybr',options={'xtol':1e-11,'maxfev':1000})
        COUNTS['root_calls']+=1;COUNTS['root_function_evaluations']+=int(sol.nfev)
        COUNTS['root_jacobian_evaluations']+=int(getattr(sol,'njev',0));x=sol.x
    require(min(x)>0,'Optional proposal did not find the positive branch')
    return [dyadic(Q(float(v)),40) for v in x]


def solve(T,beta,h):
    q=propose(T,beta,h)
    cert=ground_certificate(T,beta,h,q);COUNTS['ground_checks']+=1
    bracket=relative_bracket(T,beta,h,q);COUNTS['bracket_checks']+=1
    require(cert['gap']<Q(1,10**16),'Executed global gap target not met')
    return cert,bracket


def main():
    clock=time.perf_counter();n=6
    paths=[ROOT/'inputs'/f'component_{s}_model.json' for s in 'AB']
    calibration=Q(1,4096)
    S,d,Etot,errors=assembled_inputs(paths,calibration)
    C=[[Q(0) if i==j else (Q(1,4) if min((i-j)%n,(j-i)%n) in (1,3) else Q(1,8))
        for j in range(n)] for i in range(n)]
    require(all(sum(row)==1 for row in C))
    base_beta=list(map(Q,[1,Q(5,4),Q(3,4),Q(3,2),Q(7,8),Q(9,8)]))
    be=[Q(1,4096)]*n
    common={'n':n,'static_model':S,'source_errors_rounded_up':errors,
            'reciprocal_coupling_calibration_operator_bound':calibration,
            'total_static_operator_bound':Etot,'entrywise_outer_radius':d,
            'C':C,'beta':base_beta,'beta_error':be,
            'source_model_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
            'access':'only retained model JSON; no new experiments or hidden states',
            'uncertainty_scope':'outer enlargement; not the sharp joint record posterior'}
    save(OUT/'INPUTS.json',common)
    phases=[]
    for g in map(Q,['1/2','19/20','199/200','1','201/200','51/50','6/5','8/5']):
        T=[[(Q(1) if i==j else Q(0))-g*C[i][j] for j in range(n)] for i in range(n)]
        K=[[S[i][j]-T[i][j] for j in range(n)] for i in range(n)]
        h=[Q(0)]*n
        nominal,nb=solve(T,base_beta,h)
        lower_task,upper_task=outer_tasks(T,base_beta,h,d,be,[Q(0)]*n)
        lower_cert,lower_br=solve(*lower_task)
        upper_cert,upper_br=solve(*upper_task)
        psd_all=psd([[T[i][j]-(Etot if i==j else 0) for j in range(n)] for i in range(n)])
        negative_all=not psd([[T[i][j]+(Etot if i==j else 0) for j in range(n)] for i in range(n)])
        phase='all compatible systems disordered' if psd_all else (
            'all compatible systems ordered' if negative_all else 'phase not resolved by this outer certificate')
        boxlo=lower_br['lower'];boxhi=upper_br['upper']
        require(all(l<=u for l,u in zip(boxlo,boxhi)))
        entry={'g':g,'T':T,'physical_K':K,'K_operator_upper':matrix_bound(K),
               'phase':phase,'nominal':nominal,'nominal_bracket':nb,'lower_outer_task':lower_cert,
               'upper_outer_task':upper_cert,'lower_endpoint_bracket':lower_br,
               'upper_endpoint_bracket':upper_br,'source_and_calibration_amplitude_box':{'lower':boxlo,'upper':boxhi},
               'box_mean_intensity_lower':sum(x*x for x in boxlo)/n,
               'box_mean_intensity_upper':sum(x*x for x in boxhi)/n,
               'nominal_mean_intensity':sum(x*x for x in nominal['candidate'])/n,
               'new_source_calls':0}
        phases.append(entry)
    save(OUT/'PHASE_SCAN.json',phases)
    # A new signed amplitude task specified after acquisition, with nonzero
    # stationary coefficient calibration allowances and a small positive field.
    p=list(map(Q,['1','3/4','5/4','1/2','9/8','7/8']))
    sigma=[1,1,-1,1,-1,-1]
    beta=[8*x for x in base_beta];h=[Q(1,64)]*n;he=[Q(1,8192)]*n
    W=[[x/2 for x in row] for row in C]
    T,K=design(p,beta,h,W,S,sigma)
    nominal=ground_certificate(T,beta,h,p);COUNTS['ground_checks']+=1
    robust=robust_design_certificate(T,beta,h,p,d,be,he,Q(1,100))
    low_task,high_task=outer_tasks(T,beta,h,d,be,he)
    lowc,lowb=solve(*low_task);highc,highb=solve(*high_task)
    physical_box=[]
    for s,l,u in zip(sigma,robust['lower'],robust['upper']):
        physical_box.append([l,u] if s==1 else [-u,-l])
    designed={'target_amplitude':p,'sign_pattern':sigma,'physical_target':[s*x for s,x in zip(sigma,p)],
              'T_in_gauge':T,'W':W,'beta':beta,'field_in_gauge':h,
              'physical_field':[s*x for s,x in zip(sigma,h)],'field_error':he,
              'beta_error':be,'physical_K':K,'K_operator_upper':matrix_bound(K),
              'nominal':nominal,'robust_one_percent_certificate':robust,
              'physical_amplitude_box':physical_box,
              'tighter_outer_lower':lowb,'tighter_outer_upper':highb,
              'lower_endpoint_certificate':lowc,'upper_endpoint_certificate':highc,
              'new_source_calls':0,'automatic_global_relaxation_from_arbitrary_initial_state':False}
    save(OUT/'PROGRAMMED_PATTERN.json',designed)
    # Exact metastability family member: mu=5,c=1,beta=1.
    T2=[[Q(-5),Q(-1)],[Q(-1),Q(-5)]];q2=[Q(2),Q(-2)]
    require(residual(T2,[Q(1)]*2,[Q(0)]*2,q2)==[0,0])
    H2=[[Q(7),Q(-1)],[Q(-1),Q(7)]]
    require(psd([[H2[i][j]-(Q(6) if i==j else 0) for j in range(2)] for i in range(2)]))
    metastable={'T':T2,'mixed_sign_equilibrium':q2,'energy':energy(T2,[Q(1)]*2,[Q(0)]*2,q2),
                'hessian':H2,'hessian_eigenvalues':[6,8],'global_energy':Q(-18),
                'global_amplitudes_squared':[6,6],'strict_suboptimality_gap':Q(10),'status':'PASS'}
    # Explicit finite check accompanying (not proving) the general reduction.
    edges=[(0,1),(1,2),(2,3),(3,0),(0,2),(3,4),(4,5),(5,6),(6,7),(7,4),(1,6),(2,7)]
    m=8;D=[sum(i in e for e in edges) for i in range(m)]
    M=sum(x*x for x in D);b=Q(32*M+4*max(D)+1)
    energies=[(sum(s[i]*s[j] for i,j in edges),s) for s in product((-1,1),repeat=m)]
    ei,spins=min(energies)
    def soft(x):return float(b)/4*np.sum((x*x-1)**2)+sum(x[i]*x[j] for i,j in edges)
    def softg(x):
        z=float(b)*(x*x-1)*x
        for i,j in edges:z[i]+=x[j];z[j]+=x[i]
        return z
    opt=minimize(soft,np.array(spins,dtype=float),jac=softg,method='L-BFGS-B',
                 options={'ftol':1e-15,'gtol':1e-10,'maxiter':1000})
    COUNTS['minimize_calls']+=1;COUNTS['minimize_function_evaluations']+=int(opt.nfev)
    y=[dyadic(Q(float(v)),40) for v in opt.x]
    fv=b/4*sum((x*x-1)**2 for x in y)+sum(y[i]*y[j] for i,j in edges)
    lower=Q(ei)-2*M/b;gap=fv-lower
    rounded=[1 if x>=0 else -1 for x in y];rounded_e=sum(rounded[i]*rounded[j] for i,j in edges)
    require(0<=gap<Q(1,8) and rounded_e==ei)
    reduction={'nodes':m,'edges':edges,'degree':D,'M':M,'beta':b,
               'enumerated_discrete_assignments':2**m,'ising_minimum':ei,
               'soft_candidate':y,'soft_energy':fv,'certified_soft_lower_energy':lower,
               'certified_soft_gap':gap,'rounding_loss_bound':2*M/b,
               'rounded_spins':rounded,'rounded_ising_energy':rounded_e,
               'scope':'finite 256-assignment control; general NP-hardness proved in THEOREM.txt','status':'PASS'}
    save(OUT/'CONTROLS.json',{'metastability':metastable,'frustration_reduction':reduction})
    seconds=time.perf_counter()-clock
    bits=max_fraction_bits([common,phases,designed,metastable,reduction])
    summary={'phase_rows':[{'g':float(x['g']),'phase':x['phase'],
            'nominal_mean_intensity':float(x['nominal_mean_intensity']),
            'intensity_lower':float(x['box_mean_intensity_lower']),
            'intensity_upper':float(x['box_mean_intensity_upper'])} for x in phases],
        'pattern_target':list(map(float,designed['physical_target'])),
        'pattern_physical_box':[[float(v) for v in row] for row in physical_box],
        'pattern_lower_margin':float(robust['lower_margin']),
        'pattern_upper_margin':float(robust['upper_margin']),
        'source_errors':list(map(float,errors)),'total_static_operator_bound':float(Etot),
        'pattern_K_operator_upper':float(matrix_bound(K)),
        'pattern_beta_max':float(max(beta)),'pattern_field':float(h[0]),
        'retained_rational_certificate_bits_max':bits,'counts':COUNTS,
        'elapsed_seconds':seconds,'python':platform.python_version(),
        'numpy':np.__version__,'scipy':scipy.__version__,
        'general_SOCP':'proved and costed, not executed',
        'general_acquisition_SDP':'predecessor proved and costed, not executed',
        'additional_source_calls':0,'source_native_state_access':False,
        'physical_assembly_or_run':False,'status':'PASS'}
    save(OUT/'SUMMARY.json',summary)
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()

"""Outward finite-DATA algebra receipt, not validated trajectory integration.

The source's exact rational hidden Q qualifies its stored energy defects and
state errors for audit ONLY. It is not passed to the learner. A real physical
instrument would need independent calibration/error warrants instead.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools,json,math,time
import numpy as np
from flint import arb,arb_mat,fmpq,ctx

ctx.prec=160


def a(x):
    if isinstance(x,arb):return x
    x=F(float(x)) if isinstance(x,(float,np.floating)) else F(x)
    return arb(fmpq(x.numerator,x.denominator))


def norm(mat):
    total=arb(0)
    for row in mat.tolist():
        for x in row:
            u=abs(x).upper();total+=u*u
    return total.sqrt()


def bounds(x):
    def d(z):
        m,e=z.man_exp();m,e=int(m),int(e)
        q=F(m*(1<<e)) if e>=0 else F(m,1<<-e)
        return [q.numerator,q.denominator]
    return {'lower':d(x.lower()),'upper':d(x.upper()),'display':float(x)}


def cenergy(x,K,g):
    re,im=[list(map(a,vec)) for vec in (x.real,x.imag)]
    linear=sum(K[i][j]*(re[i]*re[j]+im[i]*im[j]) for i in range(len(x)) for j in range(len(x)))
    fourth=sum((re[i]*re[i]+im[i]*im[i])**2 for i in range(len(x)))
    return linear+g*fourth/2


def main():
    start=time.perf_counter();root=Path(__file__).parent;d=np.load(root/'DATA.npz')
    src=json.loads((root/'SYNTHETIC_SOURCE.json').read_text());n=5
    Q=[[a(x) for x in row] for row in src['Q_exact']];K=[[a(x) for x in row] for row in src['K_exact']]
    A=d['A'];b=d['b'];theta=d['theta'];M,m=A.shape
    Ap=arb_mat([[a(x) for x in row] for row in A]);bp=arb_mat([[a(x)] for x in b])
    P=np.linalg.pinv(A);Pp=arb_mat([[a(x) for x in row] for row in P])
    defect=norm(arb_mat(np.eye(m,dtype=int).tolist())-Pp*Ap)
    pn=norm(Pp);assert defect<1
    sigma=(1-defect)/pn
    keys=list(itertools.combinations_with_replacement(range(n),4));truth=[]
    for key in keys:
        multiplicity=len(set(itertools.permutations(key)))
        truth.append(sum(Q[j][key[0]]*Q[j][key[1]]*Q[j][key[2]]*Q[j][key[3]] for j in range(n))*arb(multiplicity).sqrt())
    truth=arb_mat([[x] for x in truth]);estimate=arb_mat([[a(x)] for x in theta])
    true_res=norm(Ap*truth-bp);fit_res=norm(Ap*estimate-bp)
    tensor_bound=(true_res+fit_res)/sigma
    actual_theta_error=norm(estimate-truth)
    assert actual_theta_error<tensor_bound
    # All scalar energy defects of the STORED finite source vectors are
    # certified even though their ODE trajectory error is not certified.
    defects=[];state_errors=[];g=a(F(7,20))
    for j,(xp,yp) in enumerate(zip(d['ode_initial'],d['ode_final'])):
        defects.append(abs(cenergy(yp,K,g)-cenergy(xp,K,g)).upper())
        for physical,estimated in ((xp,d['X'][:,j]),(yp,d['Y'][:,j])):
            re=[];im=[]
            for k in range(n):
                re.append(sum(Q[i][k]*a(physical[i].real) for i in range(n))-a(estimated[k].real))
                im.append(sum(Q[i][k]*a(physical[i].imag) for i in range(n))-a(estimated[k].imag))
            state_errors.append(sum(x*x for x in re+im).sqrt().upper())
    # A truth-qualified synthetic input bound; not inferred merely from a fit.
    dK=max(abs(a(x)-a(q)).upper() for x,q in zip(d['lam'],src['lambda_exact']))
    de=sum((a(x)-a(q))**2 for x,q in zip(d['c'],src['port_overlap_exact'])).sqrt()
    C=d['Chat'];sobs=np.linalg.svd(C,compute_uv=False)[-1]
    # Display-only ordinary analytical budget using the certified synthetic
    # source errors; a certified measured s_o is a separate instrument gate.
    R=1.500001;obs=math.sqrt(32)*1e-9
    dC=math.sqrt(sum((float(de)+t*float(dK))**2 for t in np.arange(32)*.5))
    state_budget=(obs+dC*R)/sobs+15.5*float(dK)*R
    dE=max(defects);eb=4*float(dK)*R*R/.35+8*max(abs(d['lam']))*R*state_budget/.35+2*float(dE)/.35
    generic=(float(fit_res)+math.sqrt(M)*(eb+8*R**3*state_budget*math.sqrt(n)))/float(sigma)
    # Native off-state error cost is charged using a conservative bound on
    # the actual finite steering waveforms, no extra pulse/ODE grid.
    B=d['Bhat'];pin=np.linalg.pinv(B);rng=np.random.default_rng(202610299701)
    target=rng.normal(size=(n,m))+1j*rng.normal(size=(n,m));target/=np.linalg.norm(target,axis=0)
    target=np.repeat(target,2,axis=1)*np.tile([1.,1.5],m)
    prep=pin@target;reset=-pin@(np.exp(-1j*d['lam'][:,None]*31.5)*d['Y'])
    maxL2=math.sqrt(.5)*max(np.linalg.norm(prep,axis=0).max(),np.linalg.norm(reset,axis=0).max())
    linear_R=1.500001+4*maxL2
    out={'status':'PASS_OUTWARD_FINITE_DATA_ALGEBRA',
         'scope':'exact stored design/source-contract arithmetic; not physical or validated ODE acquisition',
         'left_inverse_defect_F':bounds(defect),'pseudoinverse_F':bounds(pn),
         'design_sigma_min_certified_lower':bounds(sigma),
         'source_truth_residual':bounds(true_res),'fitted_residual':bounds(fit_res),
         'tensor_error_certified_upper_from_actual_source_contract':bounds(tensor_bound),
         'actual_tensor_coefficient_error':bounds(actual_theta_error),
         'source_energy_defect_certified_upper':bounds(arb(max(defects))),
         'source_state_reconstruction_error_certified_upper':bounds(arb(max(state_errors))),
         'synthetic_linear_K_error':bounds(arb(dK)),'synthetic_port_vector_error':bounds(de),
         'generic_instrument_budget_DISPLAY_ONLY':{'state_error':state_budget,
                'tensor_error_upper_using_float_readout_singular_value':generic,
                'readout_sigma_min_NOT_outward_certified':float(sobs)},
         'conservative_linear_control_norm_bound':linear_R,
         'off_state_nonlinearity_error_rate_multiplier':32*linear_R**3,
         'off_state_multiplier_scope':'steering/reset intervals only; full linear interval bound is separate',
         'whole_cycle_off_state_error_rate_multiplier':63*linear_R**3,
         'precision_or_global_actuator_acquired_in_a_device':False,
         'seconds':time.perf_counter()-start}
    (root/'ENERGY_CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('source_truth_residual','fitted_residual')},indent=2))


if __name__=='__main__':main()

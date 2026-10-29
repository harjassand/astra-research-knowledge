"""Construct/certify an UNEXECUTED finite calibration cancellation command.

Only stored coefficients, rational timings and exact linear propagators are
used. No source/science ODE, source rerun or new fit is called. Original data
remain two separately zero-initialized segments. All new trajectory/rank
claims are conditional where an old ODE error would be needed.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,time
import numpy as np
from flint import arb,acb,acb_mat,fmpq,ctx

ctx.prec=192
P=F(16);W=F(32);p=F(1,5);h=F(1,2);READ=F(31,2)
BITS=48


def ar(x):
    if isinstance(x,arb):return x
    x=F(float(x)) if isinstance(x,(float,np.floating)) else F(x)
    return arb(fmpq(x.numerator,x.denominator))


def z(x):return acb(ar(float(np.real(x))),ar(float(np.imag(x))))


def phase(lam,t):return acb(0,-lam*ar(t)).exp()


def integral(lam,t):
    if lam==0:return acb(ar(t))
    return (1-phase(lam,t))/acb(0,lam)


def norm(mat):
    s=arb(0)
    for row in mat.tolist():
        for x in row:
            u=abs(x).upper();s+=u*u
    return s.sqrt()


def frac(x):
    m,e=x.man_exp();m,e=int(m),int(e)
    return F(m*(1<<e)) if e>=0 else F(m,1<<-e)


def bounds(x):
    lo,hi=frac(x.lower()),frac(x.upper())
    return {'lower':[lo.numerator,lo.denominator],'upper':[hi.numerator,hi.denominator],
            'display':float(x)}


def round_component(x):
    return F(round(frac(x.mid())*(1<<BITS)),1<<BITS)


def rounded_matrix(mat):
    exact=[];saved=[]
    for row in mat.tolist():
        er=[];sr=[]
        for x in row:
            re,im=round_component(x.real),round_component(x.imag)
            er.append(acb(ar(re),ar(im)))
            sr.append([[re.numerator,re.denominator],[im.numerator,im.denominator]])
        exact.append(er);saved.append(sr)
    return acb_mat(exact),saved


def main():
    start=time.perf_counter();root=Path(__file__).parent;old=root.parent
    data=np.load(old/'DATA.npz');source=json.loads((old/'SYNTHETIC_SOURCE.json').read_text())
    oldcert=json.loads((old/'ENERGY_CERTIFICATE.json').read_text())
    n=5;L=32;m=32
    lam=[ar(v) for v in data['lam']];c=[ar(v) for v in data['c']]
    lt=[ar(v) for v in source['lambda_exact']];ct=[ar(v) for v in source['port_overlap_exact']]
    Bbar=data['Bhat'];Cbar=data['Chat']
    PB=acb_mat([[z(x) for x in row] for row in np.linalg.pinv(Bbar)])
    PC=acb_mat([[z(x) for x in row] for row in np.linalg.pinv(Cbar)])
    def Bmatrix(ll,cc):
        return acb_mat([[cc[j]*phase(ll[j],P-(k+1)*h)*integral(ll[j],h) for k in range(L)] for j in range(n)])
    def Cmatrix(ll,cc):
        return acb_mat([[cc[j]*phase(ll[j],k*h) for j in range(n)] for k in range(m)])
    def Dmatrix(ll,t):return acb_mat([[phase(ll[j],t) if j==k else 0 for k in range(n)] for j in range(n)])
    Bhat=Bmatrix(lam,c);Chat=Cmatrix(lam,c)
    Bt=Bmatrix(lt,ct);Ct=Cmatrix(lt,ct)
    I=acb_mat(np.eye(n,dtype=int).tolist())
    pbn=norm(PB);pcn=norm(PC)
    rb=norm(Bhat*PB-I);rc=norm(PC*Chat-I)
    assert rb<1 and rc<1
    sp=(1-rb)/pbn;so=(1-rc)/pcn
    dK=max(abs(a-b).upper() for a,b in zip(lam,lt))
    de=sum((a-b)*(a-b) for a,b in zip(c,ct)).sqrt()
    dB=ar(L).sqrt()*ar(h)*(de+ar(P)*dK)
    dC=sum((de+ar(k*h)*dK)**2 for k in range(m)).sqrt()
    xhat=acb_mat([[c[j]*phase(lam[j],W)*integral(lam[j],p)] for j in range(n)])
    xt=acb_mat([[ct[j]*phase(lt[j],W)*integral(lt[j],p)] for j in range(n)])
    command,saved_command=rounded_matrix(-PB*Dmatrix(lam,P)*xhat)
    eta_cmd=norm(Dmatrix(lam,P)*xhat+Bhat*command)
    cn=norm(command);xn=norm(xhat)
    delta_cal=ar(p)*de+ar(p*W+p*p/2)*dK
    reset_bound=delta_cal+ar(P)*dK*xn+dB*cn+eta_cmd
    reset_direct=norm(Dmatrix(lt,P)*xt+Bt*command)
    assert reset_direct<reset_bound
    power=ar(h)*cn*cn
    peak=max(abs(x).upper() for row in command.tolist() for x in row)
    # Same allowed science control, compiled once to finite coefficients.
    feedback_ideal=-PB*Dmatrix(lam,P+READ)*PC
    feedback,saved_feedback=rounded_matrix(feedback_ideal)
    df=norm(feedback-feedback_ideal)
    eb=rb+dB*pbn;ec=rc+dC*pcn
    Bupper=ar(L).sqrt()*ar(h);Cupper=ar(m).sqrt()
    alpha=ar(P+READ)*dK+eb+ec+eb*ec+Bupper*Cupper*df
    noise_gain=(1+eb)*pcn+Bupper*df
    alpha_direct=norm(Dmatrix(lt,P+READ)+Bt*feedback*Ct)
    assert alpha_direct<alpha
    # Optional FINAL command rounding to48 fractional bits. Raw detector
    # numbers are finite; exact dyadic matrix products need no float branch.
    coeff_round=ar(2*L).sqrt()/ar(1<<(BITS+1))
    state_round=Bupper*coeff_round
    eta=ar(F(1,10**9));eta_vector=ar(m).sqrt()*eta
    target=ar(F(1500001,1000000));rsteady=(alpha*((1+eb)*target+state_round)+noise_gain*eta_vector+state_round)/(1-alpha)
    rbar=max(reset_bound.upper(),rsteady.upper())
    pulse_R=ar(rbar)+(1+eb)*target+state_round
    assert pulse_R<ar(F(8,5))
    flow_lip=(3*ar(F(7,20))*ar(F(8,5))**2*ar(F(13,10))).exp()
    q=alpha*flow_lip;assert q<1
    # Exact-flow comparison only. No rank transfer from old solver arrays is
    # asserted, because their flow error is unqualified.
    injected=2*noise_gain*eta_vector+2*state_round
    different_word_floor=injected/(1-q)
    comparison=reset_bound
    common_word=[]
    for i in range(140):
        common_word.append(bounds(comparison))
        comparison=q*comparison+2*state_round
    cost={'additional_control_duration':str(P),'new_scalar_readouts':0,
          'command_bins':L,'bin_duration':str(h),'fractional_bits':BITS,
          'integrated_squared_drive_bound':bounds(power),'peak_drive_bound':bounds(arb(peak)),
          'old_normalized_protocol_time':8994.904477036298,
          'prospective_normalized_protocol_time':9010.904477036298}
    result={'status':'CONSTRUCTED_UNEXECUTED_MODEL_RESET_BRIDGE',
            'date':'2026-10-30','no_source_or_science_flow_rerun':True,
            'original_execution':'two separately zero-initialized calibration/science segments',
            'bootstrap_initial_zero':'still the original explicit model premise; only the SECOND zero is repaired',
            'linear_errors':'qualified from existing synthetic source; not a physical inference',
            'dK':bounds(arb(dK)),'de':bounds(de),'steering_sigma_lower':bounds(sp),
            'readout_sigma_lower':bounds(so),'pseudoinverse_B_norm_F':bounds(pbn),
            'pseudoinverse_C_norm_F':bounds(pcn),'calibration_history_prediction_error':bounds(delta_cal),
            'nominal_calibration_state_norm':bounds(xn),'command_arithmetic_residual':bounds(eta_cmd),
            'reset_residual_general_bound':bounds(reset_bound),
            'reset_residual_source_specific_analytic_bound_NOT_measured':bounds(reset_direct),
            'science_feedback_rounding_operator_error':bounds(df),
            'science_reset_gain_general_bound':bounds(alpha),
            'science_reset_gain_source_specific_analytic_bound':bounds(alpha_direct),
            'post_reset_noise_gain_bound':bounds(noise_gain),
            'finite_output_command_rounding_state_error':bounds(state_round),
            'absolute_post_reset_state_bound':bounds(arb(rbar)),
            'absolute_science_pulse_norm_bound':bounds(pulse_R),
            'exact_flow_Lipschitz_bound':bounds(flow_lip),'exact_cycle_contraction_bound':bounds(q),
            'different_bounded_noise_word_reset_difference_floor':bounds(different_word_floor),
            'common_word_reset_difference_bounds':common_word,
            'proper_protocol_rank_or_actual_error_from_old_arrays':'NOT_QUALIFIED: old numerical trajectory error is UNKNOWN',
            'old_data_energy_defect_is_NOT_flow_error':True,
            'cost':cost,'seconds':time.perf_counter()-start}
    (root/'COMMAND.json').write_text(json.dumps({'status':'UNEXECUTED finite port command',
         'complex_encoding':'[[re_num,re_den],[im_num,im_den]]',
         'bootstrap_command':saved_command,'science_feedback_matrix':saved_feedback},indent=2)+'\n')
    original=[]
    for name in ('energy_experiment.py','DATA.npz','ENERGY_EXECUTION.json','ENERGY_CERTIFICATE.json',
                 'ORDINARY_FIT.json','PROOF.md','RESULT.md','FINAL_RECEIPT.json'):
        raw=(old/name).read_bytes();original.append({'path':name,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
    result['unchanged_original_bindings']=original
    (root/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('common_word_reset_difference_bounds','unchanged_original_bindings')},indent=2))


if __name__=='__main__':main()

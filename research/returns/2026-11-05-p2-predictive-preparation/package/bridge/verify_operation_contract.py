"""Exact parameter implications for the new acquired-response operation.

This binds and composes existing exact predictor certificates. It checks no old
research package and does not validate floating source trajectories or hardware.
"""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import ast
import hashlib
import json

HERE=Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sqrt_up(q,bits=64):
    q=F(q); scale=1<<bits
    n=isqrt(q.numerator*scale*scale//q.denominator)
    if F(n*n,scale*scale)<q: n+=1
    ans=F(n,scale)
    assert ans*ans>=q
    return ans


def exp_minus_upper(x,target):
    """Positive Taylor sum <= exp(x), proved using rational arithmetic."""
    x=F(x); target=F(target)
    total=term=F(1); n=0
    while 1/total>target:
        n+=1; assert n<10000
        term*=x/n; total+=term
    return 1/total,dict(exponent_exact=str(x),Taylor_degree=n,
        exponential_lower_bound_exact=str(total),
        negative_exponential_upper_bound_exact=str(1/total))


def literals(path):
    out={}
    def ev(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(str,int)):return F(n.value)
        if isinstance(n,ast.Name) and n.id in out:return out[n.id]
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -ev(n.operand)
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='Q':
            q=[ev(a) for a in n.args]
            return q[0] if len(q)==1 else q[0]/q[1]
        if isinstance(n,ast.BinOp):
            a,b=ev(n.left),ev(n.right)
            if isinstance(n.op,ast.Add):return a+b
            if isinstance(n.op,ast.Sub):return a-b
            if isinstance(n.op,ast.Mult):return a*b
            if isinstance(n.op,ast.Div):return a/b
            if isinstance(n.op,ast.Pow) and b.denominator==1:return a**int(b)
        raise ValueError()
    for n in ast.parse(path.read_text()).body:
        if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name):
            try:out[n.targets[0].id]=ev(n.value)
            except ValueError:pass
    return out


def power_two(q):
    n=max(1,-((-q.numerator)//q.denominator))
    return 1<<(n-1).bit_length()


def main():
    names=['acquired_response_source.py','acquired_step_response.json',
        'physical_execution_receipt.json','retained_source_diagnostics.json',
        'exact_step_prediction.py','verify_step_prediction.py',
        'exact_prediction_path.json','exact_prediction_compiler_results.json',
        'exact_prediction_verifier_results.json','verify_operation_contract.py']
    hashes={n:sha(HERE/n) for n in names}
    load=lambda n:json.loads((HERE/n).read_text())
    table=load('acquired_step_response.json'); r=table['resources']
    receipt=load('physical_execution_receipt.json')
    comp=load('exact_prediction_compiler_results.json')
    ver=load('exact_prediction_verifier_results.json')
    path=load('exact_prediction_path.json')
    reports=load('retained_source_diagnostics.json')
    p=literals(HERE/'acquired_response_source.py')
    checks=[]
    def ck(label,condition):
        assert condition,label
        checks.append(label)
    th=hashes['acquired_step_response.json']; ph=hashes['exact_prediction_path.json']
    ck('physical receipt table/source hashes',receipt['acquired_table_sha256']==th and receipt['source_program_sha256']==hashes['acquired_response_source.py'])
    ck('source report and path bind table',reports['table_sha256']==th and path['acquired_table_sha256']==th)
    ck('compiler current hashes',comp['table_sha256']==th and comp['path_sha256']==ph)
    ck('independent path verifier current hashes',ver['verified'] and ver['table_sha256']==th and ver['path_sha256']==ph)
    T,A,h,b,mesh=(p[k] for k in ('T','A','H','B','DELTA'))
    clear,tau,clock,pc,lat=(p[k] for k in ('CLEAR','TAU_SENSOR','CLOCK','PROGRAM_CLOCK','LATENCY'))
    E0,Ed,Em=(p[k] for k in ('E_INITIAL','E_DEP','E_DEP_DURING'))
    gamma,mu,mass=(F(table[k]) for k in ('gamma_exact','stiffness_exact','mass_exact'))
    ck('normalized fixture and positive scales',(gamma,mu,mass,T)==(1,1,1,1) and min(A,h,b,mesh,clear,tau)>0)
    dc,dd,aq=p['DELTA_CAL'],p['DELTA_DEP'],p['ALPHA_Q']
    Dc,Dd=p['D_CAL'],p['D_DEP']
    ck('complete guarded calibration slot',Dc==clear+2*b+T+h+2*clock==F(r['calibration_slot_exact']))
    ck('complete guarded deployment slot',Dd==clear+b+lat+T+2*clock==F(r['deployment_slot_exact']))
    Nc,Nd=r['calibration_slots'],r['deployment_slots']
    ck('finite power-of-two slot counts',Nc==power_two(E0*Dc/(gamma*aq*dc*dc)) and Nd==power_two(Ed*Dd/(gamma*aq*dd*dd)))
    qc,qd=E0*Dc/(gamma*Nc*dc*dc),Ed*Dd/(gamma*Nd*dd*dd)
    ck('quiet event allocations',qc<=aq and qd<=aq)
    ck('private bit counts',r['calibration_private_bits']==Nc.bit_length()-1 and r['deployment_private_bits']==Nd.bit_length()-1)
    jc,jd=r['calibration_selected_index'],r['deployment_selected_index']
    ck('finite selected indices',0<=jc<Nc and 0<=jd<Nd)
    wc,wd=jc*Dc,jd*Dd
    ck('realized waits',wc==F(r['calibration_actual_wait_exact']) and wd==F(r['deployment_actual_wait_exact']))
    actual,worst=wc+Dc+wd+Dd+h,Nc*Dc+Nd*Dd+h
    ck('full realized and worst time including return',actual==F(r['actual_protocol_time_exact']) and worst==F(r['worst_total_protocol_time_exact']) and actual<=worst)
    ticks=-((-(worst/pc).numerator)//(worst/pc).denominator)
    ck('finite timer width',ticks.bit_length()<=receipt['memory']['timer_counter_bits_at_declared_resolution'])
    ck('all calibration data and return inside guards',clock+clear+b+T+b+h+clock==Dc)
    ck('all forecast and latency inside guards',clock+clear+b+lat+T+clock==Dd)

    times=list(map(F,table['times_exact'])); vals=list(map(F,table['values_exact']))
    ck('finite ordered table',len(times)==len(vals)==101 and times[0]==vals[0]==0 and times[-1]==T and all(v>u for u,v in zip(times,times[1:])))
    ck('declared mesh and passive response clipping',max(v-u for u,v in zip(times,times[1:]))==mesh and all(0<=v<=2/mu for v in vals))
    rawbase=F(reports['calibration_raw_baseline_exact']); signals=list(map(F,reports['calibration_raw_reports_exact']))
    raw=[rawbase]+signals+[F(table['deployment_baseline_exact'])]
    step=p['ADC_STEP']; bits=int(p['ADC_BITS'])
    ck('finite ADC record counts',len(raw)==102==r['raw_position_boxes'] and len(raw)*bits==r['raw_adc_payload_bits'])
    ck('finite ADC raw grid and range',all((v/step).denominator==1 and -(2**(bits-1))<=v/step<=2**(bits-1)-1 for v in raw))
    ck('exact table encoding',[F(0)]+[min(2/mu,max(F(0),(v-rawbase)/A)) for v in signals]==vals)
    Ls=F(r['source_step_lipschitz_bound_used_exact'])
    ck('step speed from joint mass/spring storage',Ls*Ls*mu*mass>=1)
    cal={k:F(v) for k,v in table['calibration_error_terms_exact'].items()}
    expected=dict(quiet=dc/A,finite_positive_ramp=Ls*h/2,finite_position_box=Ls*b/2,
        linear_interpolation=Ls*mesh/2,deterministic_meter_difference=2*p['METER_BIAS']/A,
        simultaneous_meter_noise=p['NOISE_CAL']/A,finite_clock=Ls*clock)
    for k,v in expected.items():ck('calibration '+k,cal[k]>=v)
    eta=sum(cal.values(),F(0)); ck('response error sum',eta==F(table['response_error_exact']))
    ready={k:F(v) for k,v in table['readiness_error_terms_exact'].items()}
    init=sum(ready.values(),F(0)); delivery=F(table['delivery_error_exact'])
    bk=p['BACKACTION']; fe=p['FORCE_ERROR']
    baseline_force=2*bk*sqrt_up((clear+b+2*clock)/(2*mu*gamma))
    cal_force=(fe+3*bk)*sqrt_up(Dc/(2*mu*gamma))/A
    forecast_force=(fe+bk)*sqrt_up(T/(2*mu*gamma))
    ck('guarded baseline backaction',baseline_force<=ready['baseline_only_backaction'])
    ck('calibration force/backaction',cal_force<=cal['force_and_backaction'])
    ck('separate forecast delivery',forecast_force<=delivery)
    ck('readiness terms and sum',ready['quiet']==dd and ready['deterministic_baseline_meter']>=p['METER_BIAS'] and ready['baseline_noise']>=p['NOISE_DEP'] and init==F(table['readiness_error_exact']))

    # Both box endpoints may use the separately specified duration precision.
    bmin=b-2*pc; ck('positive minimum box duration',bmin>0)
    an=F(1,250); ao=F(1,1000000); taylor={}; noise={}
    for label,x,mult in (
        ('calibration',p['NOISE_CAL']**2*bmin/(4*p['V_X']),2*len(signals)),
        ('deployment',p['NOISE_DEP']**2*bmin/(2*p['V_X']),2)):
        u,proof=exp_minus_upper(x,an/mult)
        noise[label]=mult*u; taylor['noise_'+label]=proof
        ck(label+' Gaussian union bound',noise[label]<=an)
    # Compute the quintic squared integral, not a floating approximation.
    coeff=[F(0),F(0),F(0),F(10),F(-15),F(6)]
    rs=sum((x*y/F(i+j+1) for i,x in enumerate(coeff) for j,y in enumerate(coeff)),F(0))
    ck('quintic integral',rs==F(181,462))
    Pcal=A*A*(T+b-h+2*h*rs)
    ck('complete nominal calibration energy',Pcal==F(r['nominal_probe_force_squared_integral_exact']))
    Ecal=E0+(sqrt_up(Pcal)+(fe+bk)*sqrt_up(Dc))**2/(4*gamma)
    ck('calibration energy fits next preparation',Ecal<Ed)
    ck('calibration position/velocity cap one',2*Ecal<min(mu,mass))
    program=path['force_program']
    ck('executed program shape',len(program)==1 and F(program[0]['start_exact'])==0)
    amp,qh=F(program[0]['increment_exact']),F(program[0]['ramp_exact'])
    ck('executed query values',amp==F(4,5) and qh==F(1,20))
    Pquery=amp*amp*(T-qh+(qh+h)*rs)
    Equery=Ed+(sqrt_up(Pquery)+(fe+bk)*sqrt_up(Dd+h))**2/(4*gamma)
    ck('query plus final return energy',Equery<Em)
    ck('calibration reaction including force error',A+fe+sqrt_up(2*Ecal/mu)<=F(str(r['calibration_reaction_force_cap'])))
    ck('query reaction including force error',amp+fe+sqrt_up(2*Equery/mu)<=F(str(r['query_reaction_force_cap'])))

    clear_tail,proof=exp_minus_upper(clear/tau,F(1,100000000));taylor['sensor_clearing']=proof
    meter={}; overflow={}
    for label,Ec,count in [('calibration',Ed,101),('deployment',Em,1)]:
        X,V=sqrt_up(2*Ec/mu),sqrt_up(2*Ec/mass)
        lag=V*tau+X*clear_tail
        normalization=X*2*pc/(b-2*pc)
        endpoint=2*V*pc
        residual=p['METER_BIAS']-lag-step/2-normalization-endpoint
        ck(label+' finite meter headroom',residual>F(1,20000))
        meter[label]=dict(position_cap_exact_upper=str(X),velocity_cap_exact_upper=str(V),
            lag_transient_exact_upper=str(lag),quantization_half_step_exact=str(step/2),
            duration_normalization_exact_upper=str(normalization),endpoint_motion_exact_upper=str(endpoint),
            remaining_calibration_integration_budget_exact=str(residual))
        margin=p['ADC_HALF_RANGE']-step-X-p['METER_BIAS']
        ck(label+' ADC margin',margin>0)
        u,proof=exp_minus_upper(margin*margin*bmin/(2*p['V_X']),ao/(2*count))
        taylor['ADC_'+label]=proof;overflow[label]=2*count*u
        ck(label+' ADC overflow allocation',overflow[label]<=ao)
    speed=15*A/(8*h);rise=15*amp/(8*qh);ret=15*amp/(8*h)
    cacc=10*sqrt_up(F(3))*A/(3*h*h)
    racc=10*sqrt_up(F(3))*amp/(3*qh*qh)
    oacc=10*sqrt_up(F(3))*amp/(3*h*h)
    ck('waveform timing force allowance',speed*pc<fe/10)
    ck('global hardware caps cover query return',ret<=speed and oacc<=cacc)
    variation=sum((abs(F(q['increment_exact'])) for q in program),F(0))
    actual_bound=init+variation*eta+delivery;all_bound=init+eta+delivery
    ck('actual variation',variation==F(4,5)==F(path['variation_upper_bound_exact']))
    ck('exact actual prediction composition',actual_bound==F(path['uniform_physical_error_bound_exact'])==F(comp['uniform_physical_error_bound_exact'])==F(ver['uniform_physical_error_bound_exact']))
    ck('zero polynomial implementation error',F(path['numerical_polynomial_error_exact'])==0)
    success=1-2*aq-2*an-2*ao
    ck('joint conditional success',success==F(r['joint_valid_event_probability_exact']))
    out={
        'status':'passed exact rational operation-contract implication checks',
        'scope':'Checks declared-parameter implications, exact encodings, and certificate hashes. Does not validate floating plant integration, a laboratory instrument, private entropy, or the physical class.',
        'input_sha256':hashes,'checks_passed':len(checks),'checks':checks,
        'clock':dict(calibration_quiet_failure_exact=str(qc),deployment_quiet_failure_exact=str(qd),
            calibration_slots=Nc,deployment_slots=Nd,private_bits=Nc.bit_length()+Nd.bit_length()-2,
            actual_time_exact=str(actual),worst_time_exact=str(worst),timer_ticks=ticks,timer_bits=ticks.bit_length()),
        'energy':dict(ramp_square_exact=str(rs),nominal_calibration_force_energy_exact=str(Pcal),
            post_calibration_exact_upper=str(Ecal),post_calibration_upper=float(Ecal),
            nominal_query_and_return_force_energy_exact=str(Pquery),
            post_query_and_return_exact_upper=str(Equery),post_query_and_return_upper=float(Equery)),
        'metrology':dict(minimum_box_duration_exact=str(bmin),noise_bounds_exact={k:str(v) for k,v in noise.items()},
            ADC_overflow_bounds_exact={k:str(v) for k,v in overflow.items()},sensor_budgets=meter,
            positive_Taylor_proofs=taylor,raw_reports=len(raw),raw_ADC_bits=len(raw)*bits),
        'force_error':dict(calibration_exact_upper=str(cal_force),baseline_exact_upper=str(baseline_force),forecast_exact_upper=str(forecast_force)),
        'nominal_control_caps_exact_upper':dict(calibration_speed=str(speed),calibration_acceleration=str(cacc),
            query_rise_speed=str(rise),query_rise_acceleration=str(racc),query_return_speed=str(ret),
            query_return_acceleration=str(oacc),global_speed=str(max(speed,rise,ret)),
            global_acceleration=str(max(cacc,racc,oacc)),calibration_travel=str(2*A/mu),query_travel_with_return=str(2*amp/mu)),
        'prediction':dict(response_error_exact=str(eta),readiness_error_exact=str(init),delivery_error_exact=str(delivery),
            actual_variation_exact=str(variation),actual_query_bound_exact=str(actual_bound),actual_query_bound=float(actual_bound),
            all_W_at_most_one_bound_exact=str(all_bound),all_W_at_most_one_bound=float(all_bound),
            conditional_success_exact=str(success)),
        'clarifications':[
            'Query rise speed is 30; final return speed is 75. The apparatus calibration cap 93.75 covers both.',
            'Floating acceleration displays are approximate; this receipt supplies exact outward rational bounds.',
            'Report timing denotes net evaluation-time error relative to the within-slot nominal program; program timing is separately charged in force delivery.',
            'Remaining deterministic meter headroom is a hardware calibration/integration requirement, not a validation of floating source integration.',
            'Nominal center derivative/travel bounds do not bound derivatives or total variation of arbitrary tracking errors. Actual actuator caps remain calibrated contracts.',
            'The existing exact path verification is bound by hashes; no unrelated prior scientific audits are rerun.',
            'Physical class, energy, private randomness, off-mode independence, clock, metrology and reliable arithmetic/memory remain supplied contracts.']}
    (HERE/'operation_contract_verification.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(dict(verified=True,checks_passed=len(checks),table_sha256=th,path_sha256=ph,
        all_W_at_most_one_bound=float(all_bound),actual_query_bound=float(actual_bound),
        confidence=float(success),post_calibration_energy_upper=float(Ecal),
        post_query_and_return_energy_upper=float(Equery)),indent=2))


if __name__=='__main__':main()

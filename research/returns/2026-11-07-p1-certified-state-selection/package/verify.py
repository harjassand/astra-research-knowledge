"""Audit the entire emitted transcript against the integer control/error contract."""
import hashlib, json, struct, time
from fractions import Fraction as Q
from plan import ROOT, make_plan, encode, save
from exact import require
from family_certificate import certificate


def main():
    start=time.perf_counter();plan=make_plan()
    require(encode(plan)==json.loads((ROOT/'results/PLAN.json').read_text()),'Planner certificate changed')
    fam=certificate();save(ROOT/'results/FAMILY_CERTIFICATE.json',fam)
    run=json.loads((ROOT/'results/EXECUTION.json').read_text())
    p=plan['fixed_point_fraction_bits'];scale=1<<p
    K=[[int(x*scale) for x in row] for row in plan['K_fixed']]
    beta=[int(x*scale) for x in plan['beta_fixed']];field=[int(x*scale) for x in plan['field_fixed']]
    target=[int(x*scale) for x in plan['target']]
    first_late=int(plan['settling_time_after_switch']/plan['sample_interval'])
    upper_cmd=(plan['retention_ideal_command_norm_upper']+plan['control_evaluation_error_L2'])**2*scale**2
    upper_read=(plan['retention_state_norm_upper']+plan['measurement_error_L2'])**2*scale**2
    read_limit=upper_read.numerator//upper_read.denominator;cmd_limit=upper_cmd.numerator//upper_cmd.denominator
    maxnum,maxden=0,1; rows=0;digest=hashlib.sha256();max_round_integer_error=0
    with (ROOT/'results/PORT_RECORDS.bin').open('rb') as f:
        while True:
            block=f.read(96*1024)
            if not block:break
            require(len(block)%96==0);digest.update(block)
            for values in struct.iter_unpack('<12q',block):
                y=values[:6];c=values[6:]
                require(sum(x*x for x in y)<=read_limit)
                require(sum(x*x for x in c)<=cmd_limit)
                for i in range(6):
                    # Check the mathematical rounding inequality, not the particular
                    # tie rule or controller implementation which generated the record.
                    ideal_numerator=(sum(K[i][j]*y[j] for j in range(6))<<(2*p))-beta[i]*y[i]**3+(field[i]<<(3*p))
                    error=abs((c[i]<<(3*p))-ideal_numerator)
                    require(error<=1<<(3*p-1))
                    max_round_integer_error=max(max_round_integer_error,error)
                    if rows>=first_late:
                        num=abs(y[i]-target[i]);den=abs(target[i])
                        if num*maxden>maxnum*den:maxnum,maxden=num,den
                rows+=1
    require(rows==run['record_rows']==plan['executed_schedule_intervals'])
    require(digest.hexdigest()==run['record_sha256'])
    max_record=Q(maxnum,maxden)
    # The general theorem supplies the continuous output derivative bound.
    # Each recorded sample starts one actual uniform hold interval, including
    # the final interval through the requested end time.
    continuous=max_record+(plan['measurement_error_L2']+
                  plan['output_time_derivative_bound']*plan['sample_interval'])/min(plan['target_amplitudes'])
    require(continuous<Q(1,5000)) # 0.02 percent, for this particular complete record
    result={'status':'PASS','rows_checked':rows,'integer_command_inequalities_checked':6*rows,
        'record_sha256':digest.hexdigest(),'maximum_recorded_relative_error_exact':max_record,
        'maximum_scaled_rounding_error_integer':max_round_integer_error,
        'a_posteriori_continuous_relative_port_error':continuous,
        'a_posteriori_scope':'exact reference source with this emitted transcript; final one-unit retention interval; uses warranted read error and the proved derivative bound',
        'family_scope_relative_error':plan['port_relative_error_after_settling'],
        'verification_wall_seconds':time.perf_counter()-start}
    save(ROOT/'results/VERIFICATION.json',result)
    print('Transcript audit PASS:',rows,'rows; continuous relative error <=',float(continuous),flush=True)


if __name__=='__main__':main()

"""Read-only audit of actual rotor measurements; no workbook dependency.

Source: Paulsen, figshare 28856705 v1, CC BY 4.0.
All kinematic calculations are predictions, not new physical observations.
Run with Python 3. Output: RESULTS.json.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
import statistics
import time
import xml.etree.ElementTree as ET
import zipfile

BASE = Path(__file__).resolve().parent
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read_xlsx(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        strings = [''.join(el.itertext()) for el in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        book = ET.fromstring(z.read('xl/workbook.xml'))
        rel = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets = {r.attrib['Id']: r.attrib['Target'] for r in rel}
        for sheet in book.find('s:sheets', NS):
            rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            target = targets[rid]
            target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            data = {}
            for c in ET.fromstring(z.read(target)).findall('.//s:c', NS):
                v = c.find('s:v', NS)
                if v is None:
                    continue
                value = v.text
                data[c.attrib['r']] = strings[int(value)] if c.attrib.get('t') == 's' else float(value)
            out[sheet.attrib['name']] = data
    return out


def spring_fit(x, f):
    xm, fm = statistics.mean(x), statistics.mean(f)
    k = sum((a-xm)*(b-fm) for a,b in zip(x,f)) / sum((a-xm)**2 for a in x)
    intercept = fm-k*xm
    resid = [b-k*a-intercept for a,b in zip(x,f)]
    return dict(n=len(x), k_N_per_m=k, rest_length_m=-intercept/k,
                rmse_N=math.sqrt(statistics.mean(r*r for r in resid)),
                max_abs_residual_N=max(map(abs,resid)),
                measured_length_range_m=[min(x),max(x)])


def coupling_torque(k, rest, spacing, li, lj, ti, tj):
    length = math.hypot(spacing+lj*math.sin(tj)-li*math.sin(ti),
                        lj*math.cos(tj)-li*math.cos(ti))
    return k*li*(spacing*math.cos(ti)+lj*math.sin(tj-ti))*(1-rest/length)


def pair_torque(k, rest, spacing, li, lj, ti, tj):
    return (coupling_torque(k,rest,spacing,li,lj,ti,tj)+
            coupling_torque(k,rest,spacing,-li,-lj,ti,tj))


def drive_torque(k, rest, y, x, lever, theta, gamma):
    length = math.hypot(gamma+x-lever*math.sin(theta), y+lever*math.cos(theta))
    return lever*k*math.cos(theta)*(gamma+x+y*math.tan(theta))*(1-rest/length)


def root(f, lo=-200, hi=200):
    fl, fh = f(lo), f(hi)
    assert fl < 0 < fh, (fl,fh)
    for _ in range(90):
        mid = (lo+hi)/2
        if f(mid) > 0:
            hi=mid
        else:
            lo=mid
    return (lo+hi)/2


def latch_prediction():
    """Independent translation of published Kinematic-model.nb parameters."""
    result={}
    angles=[math.radians(18.3),math.radians(38.8)]
    xs=[-8.1,-16.35]
    for i in range(2):
        j=1-i
        for branch, own in [('+',-1),('-',1)]:
            for other in [-1,1]:
                ti,tj=own*angles[i],other*angles[j]
                # Reverse spacing and both attachment signs on swapping i,j.
                spacing=15.24 if i==0 else -15.24
                li,lj=(4.731,-4.731) if i==0 else (-4.731,4.731)
                tc=pair_torque(.190,4.1,spacing,li,lj,ti,tj)
                fn=lambda gamma: drive_torque(.190,4.1,9.4,xs[i],6.31,ti,gamma)+tc
                label=f'g_{i+1}^{branch}({"+" if other==1 else "-"})'
                result[label]=root(fn)
    return result


def stable(state, gamma, thresholds):
    for i in range(2):
        branch='+' if state[i]==-1 else '-'
        th=thresholds[(i,branch,state[1-i])]
        if (state[i]==-1 and gamma>th) or (state[i]==1 and gamma<th):
            return False
    return True


def advance(state, start, endpoint, thresholds):
    """Quasistatic continuous monotone ramp. Fail on ambiguous avalanches."""
    state=list(state)
    gamma=start
    direction=1 if endpoint>start else -1
    for _ in range(32):
        unstable=[]
        for i in range(2):
            branch='+' if state[i]==-1 else '-'
            th=thresholds[(i,branch,state[1-i])]
            if (state[i]==-1 and gamma>th) or (state[i]==1 and gamma<th):
                unstable.append(i)
        if unstable:
            assert len(unstable)==1, 'Avalanche ordering unmeasured'
            state[unstable[0]]*=-1
            continue
        candidates=[]
        for i in range(2):
            if state[i]==-direction:
                branch='+' if direction==1 else '-'
                th=thresholds[(i,branch,state[1-i])]
                if (gamma <= th < endpoint) if direction==1 else (gamma >= th > endpoint):
                    candidates.append((th,i))
        if not candidates:
            assert stable(state,endpoint,thresholds)
            return tuple(state)
        threshold,i=(min(candidates) if direction==1 else max(candidates))
        gamma=threshold
        state[i]*=-1
    raise RuntimeError('No settling certificate')


def run_protocol(initial, peaks, thresholds):
    gamma=F(0); state=initial
    for endpoint in peaks:
        state=advance(state,gamma,endpoint,thresholds)
        gamma=endpoint
    return state


def solve_fraction(matrix, rhs):
    a=[[F(x) for x in row]+[F(y)] for row,y in zip(matrix,rhs)]
    n=len(a)
    for c in range(n):
        p=next(r for r in range(c,n) if a[r][c])
        a[c],a[p]=a[p],a[c]
        scale=a[c][c]; a[c]=[v/scale for v in a[c]]
        for r in range(n):
            if r!=c:
                scale=a[r][c]; a[r]=[x-scale*y for x,y in zip(a[r],a[c])]
    return [row[-1] for row in a]


def main():
    began=time.perf_counter()
    path=BASE/'sources'/'Source Data.xlsx'
    sheets=read_xlsx(path)
    springs=sheets['Fig. 1B']
    fits={}
    for label,xc,yc in [('0.46','A','B'),('0.19','C','D'),('0.07','E','F')]:
        rows=[r for r in range(3,32) if f'{xc}{r}' in springs]
        fits[label]=spring_fit([springs[f'{xc}{r}'] for r in rows],
                               [springs[f'{yc}{r}'] for r in rows])
    latch=sheets['Fig. 3B']
    measurements={latch[f'A{r}']:latch[f'B{r}'] for r in [3,4,5,6,8,9,10,11]}
    pubmodel={latch[f'A{r}']:latch[f'C{r}'] for r in [3,4,5,6,8,9,10,11]}
    prediction=latch_prediction()
    numerical_error=max(abs(prediction[k]-pubmodel[k]) for k in measurements)
    assert numerical_error<0.000051
    model_errors={k:prediction[k]-measurements[k] for k in measurements}
    thresholds={}
    for i in range(2):
        for branch in ['+','-']:
            for s in [-1,1]:
                label=f'g_{i+1}^{branch}({"+" if s==1 else "-"})'
                thresholds[(i,branch,s)]=F(str(measurements[label]))
    start_states=[s for s in product([-1,1],repeat=2) if stable(s,F(0),thresholds)]
    protocols={'published_set':[F(10),F(0)],
               'published_reset':[F(32),F(0)],
               'direct_negative_reset':[F('-1.8'),F(0)],
               'threshold_trimmed_set':[F('7.0'),F(0)]}
    nominal={name:[list(run_protocol(s,seq,thresholds)) for s in start_states]
             for name,seq in protocols.items()}
    # Sensitivity calculation only: treat source ruler uncertainty as a box.
    # This does not establish that drift or rate dependence stay in the box.
    keys=list(thresholds)
    count=0; robust={name:True for name in protocols}
    targets={'published_set':(1,-1),'threshold_trimmed_set':(1,-1),
             'published_reset':(-1,-1),'direct_negative_reset':(-1,-1)}
    for signs in product([-1,1],repeat=8):
        th={k:thresholds[k]+F(s,10) for k,s in zip(keys,signs)}
        for name,seq in protocols.items():
            for peak_error,base_error in product([F(-1,10),F(1,10)],repeat=2):
                actual=[seq[0]+peak_error,base_error]
                for s in start_states:
                    outcome=run_protocol(s,actual,th)
                    robust[name] &= outcome==targets[name]
                    count+=1
    assert all(robust.values())
    coupling={}
    for i in range(2):
        vals={b:float((thresholds[(i,b,-1)]-thresholds[(i,b,1)])/2) for b in ['+','-']}
        vals['minimum_individual_threshold_uncertainty_for_common_J_cm']=abs(vals['+']-vals['-'])/2
        vals['common_J_compatible_with_plus_minus_0.1_cm_per_threshold']=abs(vals['+']-vals['-'])<=.2+1e-12
        coupling[str(i+1)]=vals
    events=sheets['Fig. 5D']
    eventrows=[(events[f'A{r}'],events[f'B{r}']) for r in range(2,18)]
    q=solve_fraction([[1,3],[F(1,10),1]],[1,1])
    assert q==[F(-20,7),F(9,7)]
    # A sign-compatible three-cycle violating diagonal symmetrizability.
    J=[[F(0),F(2),F(1)],[F(1),F(0),F(2)],[F(2),F(1),F(0)]]
    clockwise=J[0][1]*J[1][2]*J[2][0]
    reverse=J[1][0]*J[2][1]*J[0][2]
    result=dict(status='STOP_NEW_OPERATION_CLAIM__HOLD_NEW_HARDWARE_VALIDATION',
        source=dict(doi='10.6084/m9.figshare.28856705.v1',bytes=path.stat().st_size,
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest()),
        spring_fits=fits,actual_latch_thresholds_cm=measurements,
        independent_kinematic_prediction_cm=prediction,
        model_replay_max_difference_from_published_rounded_model_cm=numerical_error,
        model_minus_measured_cm=model_errors,
        max_abs_model_measurement_discrepancy_cm=max(map(abs,model_errors.values())),
        common_interaction_matrix_fit=coupling,
        latch_stable_states_at_zero=start_states,nominal_protocol_results=nominal,
        interval_corner_protocol_audit=dict(
            threshold_box_cm=.1,actuator_endpoint_box_cm=.1,executed_trajectories=count,
            all_corner_outcomes_match=robust,
            limitation='Box premise is hypothetical. No repeated drift/fatigue or actuator-error dataset was acquired.'),
        reset_obstruction=dict(start='+−',first_exit_negative_cm=-1.5,first_exit_positive_cm=30.7,
            nominal_invariant_interval_cm=[-1.5,30.7],
            common_invariant_interval_under_threshold_box_cm=[-1.4,30.6],
            positive_only_claim='Every drive waveform confined to [0,30.6] leaves +− unchanged under the stated box.'),
        four_rotor_observations=dict(event_rows=len(eventrows),unique_events=len(set(eventrows)),
            unique_state_labels=len(set(s for s,g in eventrows)),binary_state_labels_possible=16,
            second_block_identical_to_first=eventrows[:8]==eventrows[8:],
            limitation='Only an observed cycling path. No full experimentally measured transition table or all-initial-state reset test.'),
        conditional_joint_realizability_examples=dict(
            zero_rest_limit_only=True,width_constraint_matrix=[['1','3'],['1/10','1']],
            q_solution=[str(v) for v in q],positive_q_exists=False,
            cycle_forward_product=str(clockwise),cycle_reverse_product=str(reverse),
            cycle_is_symmetrizable=clockwise==reverse),
        physical_experiment_run=False,inference_tokens=None,inference_cost=None,inference_energy=None,
        execution_seconds=time.perf_counter()-began)
    (BASE/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','model_replay_max_difference_from_published_rounded_model_cm',
        'max_abs_model_measurement_discrepancy_cm','common_interaction_matrix_fit',
        'interval_corner_protocol_audit','four_rotor_observations','execution_seconds']},indent=2))


if __name__=='__main__':
    main()

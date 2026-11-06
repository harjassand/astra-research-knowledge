"""Exact controls at the actual claim boundaries, with their costs retained."""
from pathlib import Path
from fractions import Fraction as Q
import copy,json,time
from exact import C,require,encode,sqrt_up
from acquisition import certify
from native import fixture


def obstruction():
    rows=[]
    for k in [8,32,256,4096]:
        p=Q(k*k-1,k*k+1);q=Q(2*k,k*k+1)
        require(p*p+q*q==1)
        e=q*q;w=1/e;A=2-e;c=e*(1-e)*(w-1)**2
        G=C(1-e)/C(1,w)+C(e)/C(w,w)
        gain=C(1)/(C(1)/G-C(0,w));gap=gain-C(1)
        gap2=gap.re**2+gap.im**2
        formula=(1-e)**2*(1+e*e)/(1+(2-e)**2)
        require(e<=Q(1,16) and gap2==formula and gap2>=Q(9,64))
        rows.append(encode({'k':k,'port_coefficients':[p,q],'e':e,
            'high_mode_rate_and_later_skew_gain':w,'a':Q(1),'A':A,
            'hidden_coupling_variance':c,'open_loop_L1_difference':e*(1-e),
            'exact_closed_gain':gain,'closed_gain_gap_squared':gap2,
            'steady_gain_gap_lower_bound':Q(3,8),
            'finite_horizon':Q(8),'startup_correction_bound':Q(1,64),
            'finite_horizon_output_gap_lower_bound':Q(23,64),
            'later_input_amplitude':Q(1),'later_input_energy':Q(8)}))
    return {'status':'PASS','scope':'two ports; no common hidden-coupling bound; fixed native noise and finite acquisition effort',
            'proof':'THEOREM.txt section 7','witnesses':rows}


def main():
    output=Path(__file__).resolve().parent/'results'
    controls={'obstruction':obstruction(),'known_source_checks':[],'negative_controls':[]}
    for which,label in enumerate(['component_A','component_B']):
        record=json.loads((output/(label+'_port_record.json')).read_text())
        model=json.loads((output/(label+'_model.json')).read_text())
        source=fixture(which);r=record['contract']['r'];start=time.perf_counter()
        max_error=Q(0)
        # This is an EXTRA paid, known-source validation. Neither the fitted
        # model nor its certificate receives these exact transfer values.
        for obs in record['observations']:
            w=Q(obs['frequency']);gamma=Q(obs['certified_coordinate_error'])
            for i in range(r):
                for j in range(r):
                    actual=sum((C(row[i]*row[j])/C(lam,w)
                                for lam,row in zip(source['rates'],source['B'])),C())
                    report=C(*obs['response_matrix'][i][j]);delta=actual-report
                    err=max(abs(delta.re),abs(delta.im));max_error=max(max_error,err)
                    require(err<=gamma)
        controls['known_source_checks'].append(encode({'component':label,'status':'PASS',
            'maximum_observed_coordinate_discrepancy':max_error,
            'weighted_complex_mode_terms':len(source['rates'])*r*r*len(record['observations']),
            'additional_acquisition_calls':0,
            'private_validation_seconds':time.perf_counter()-start,
            'qualification':'known-source exact rational validation; excluded from learner and model certificate'}))
        if which==0:
            bad_model=copy.deepcopy(model)
            bad_model['A'][0][0]=str(Q(bad_model['A'][0][0])+1)
            bad_grid=copy.deepcopy(record)
            bad_grid['contract']['frequencies'][-1]='1000000'
            bad_noise=copy.deepcopy(record)
            bad_noise['observations'][0]['certified_coordinate_error']='-1/1000'
            for name,rr,mm in [('corrupted_model',record,bad_model),
                               ('corrupted_frequency_grid',bad_grid,model),
                               ('negative_noise_bound',bad_noise,model)]:
                try:certify(rr,mm)
                except ValueError as err:result={'control':name,'status':'REJECTED','reason':str(err)}
                else:raise ValueError('Unsafe certificate accepted: '+name)
                controls['negative_controls'].append(result)
    # Compact outward rational summary; full exact family coefficients above.
    for row in controls['known_source_checks']:
        from exact import up
        row['maximum_observed_coordinate_discrepancy']=str(up(Q(row['maximum_observed_coordinate_discrepancy']),80))
    (output/'controls.json').write_text(json.dumps(controls,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'obstruction':'PASS','known_source_checks':controls['known_source_checks'],
                      'negative_controls':controls['negative_controls']}),flush=True)


if __name__=='__main__':main()

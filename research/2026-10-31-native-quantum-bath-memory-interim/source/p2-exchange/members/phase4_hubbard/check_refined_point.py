"""Reproduce the selected regime and resolve its ramp-integration risk."""
from pathlib import Path
import json
from scipy.linalg import norm
from check_finite_hubbard import setup,run_case

ROOT=Path(__file__).resolve().parent

def main():
    model=setup()
    rows=[]
    for ramp in [20.,40.]:
        answer,k=run_case(model,50.,ramp,80,True,0.)
        rows.append(answer)
        print({key:answer[key] for key in ['ramp_time_U_units','code_reject_probability','worst_false_accept_probability','code_final_charge_probability','total_duration_U_units']},flush=True)
        if ramp==40.:
            coarse=k
    fine,kfine=run_case(model,50.,40.,160,True,0.)
    data=dict(refined_cases=rows,selected_point_fine=fine,
              selected_point_convergence=dict(steps=[80,160],
                accepted_operator_difference=float(norm(coarse-kfine,2)),
                code_reject_probability_difference=abs(rows[-1]['code_reject_probability']-fine['code_reject_probability']),
                charge_probability_difference=abs(rows[-1]['code_final_charge_probability']-fine['code_final_charge_probability']),
                false_accept_probability_difference=abs(rows[-1]['worst_false_accept_probability']-fine['worst_false_accept_probability'])))
    (ROOT/'refined_charge_closure_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data['selected_point_convergence']),flush=True)

if __name__=='__main__':main()

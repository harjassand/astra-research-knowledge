"""Independent exact received-word and design-certificate replay."""
from fractions import Fraction as F
from math import comb
from hashlib import sha256
from pathlib import Path
import json
import numpy as np

HERE=Path(__file__).resolve().parent


def main():
    protocol_path=HERE/"transfer_protocol.json"
    protocol=json.loads(protocol_path.read_text())
    certificate=json.loads((HERE/"transfer_timing_certificate.json").read_text())
    controller=json.loads((HERE/"acquired_transfer_timing_controller.json").read_text())
    record_path=HERE/protocol["actual_received_record"]
    eta=F(protocol["weak_contrast"]);length=int(protocol["weak_length"])
    p=(1+eta)/2
    t=sum(F(comb(length,k))*p**k*(1-p)**(length-k)for k in range(length//2+1))
    gamma=(1-2*t)**2
    assert gamma==F(certificate["score_gamma_exact"])
    term=exp_sum=F(1)
    for k in range(1,certificate["exp_Taylor_degree"]+1):
        term*=F(7,k);exp_sum+=term
    assert exp_sum==F(certificate["exp_Taylor_partial_sum_exact"])and exp_sum>1000
    count=[0]*5;signed=[0]*5
    with np.load(record_path)as record:
        for index,axis,pre,post in zip(record["duration_index"],record["outer_axis"],record["pre_words"],record["post_words"]):
            index=int(index);assert 0<=index<5 and int(axis)in(0,1,2)
            assert int(pre)>>length==int(post)>>length==0
            value=1 if (int(pre).bit_count()>length//2)==(int(post).bit_count()>length//2)else -1
            count[index]+=1;signed[index]+=value
    computed=[]
    for i,row in enumerate(certificate["duration_results"]):
        assert count[i]==row["received_calls"]==protocol["calls_per_duration"]
        assert signed[i]==row["paired_signed_sum"]
        estimate=F(3,4)*(1-F(signed[i],count[i])/gamma)
        assert estimate==F(row["received_error_estimate_exact"])
        radius=F(row["statistical_radius_upper_exact"])
        assert radius>=0 and radius**2>=F(9,16)/gamma**2*F(14,count[i])
        duration=F(str(protocol["duration_menu"][i]));cycles=int(protocol["cycles"])
        v=F(protocol["v_bound"]);jmax=F(protocol["J_absolute_bound"])
        kappa=F(protocol["kappa_M_bound"])+4*jmax*v
        coefficient=kappa/4+v*v/2
        assert kappa==F(protocol["kappa_bound"])and coefficient==F(protocol["cycle_error_coefficient"])
        epsilon=min(F(1),coefficient*duration**2/cycles+4*cycles*F(protocol["pair_pulse_half_diamond_allowance"])
                    +F(protocol["residual_interface_gap_duration"])*F(protocol["residual_gap_local_norm_bound"]))
        assert epsilon==F(row["closure_allowance_exact"])
        upper=min(F(1),max(F(0),estimate+radius+2*epsilon))
        assert upper==F(row["actual_current_error_upper_exact"])
        assert F(row["short_current_error_upper_exact"])>=upper
        computed.append(upper)
    winner=min(range(5),key=lambda i:(computed[i],i))
    assert winner==controller["selected_duration_index"]==certificate["selected"]["duration_index"]
    assert F(controller["current_bad_operation_weight_upper_exact"])==computed[winner]
    assert controller["calibration_record_sha256"]==certificate["calibration_record_sha256"]==sha256(record_path.read_bytes()).hexdigest()
    assert controller["protocol_sha256"]==certificate["protocol_sha256"]==sha256(protocol_path.read_bytes()).hexdigest()
    result={
        "received_only":True,"learner_or_native_plant_imported":False,
        "paired_words_replayed":sum(count),"duration_counts":count,"signed_totals":signed,
        "exact_design_allowances_and_statistical_bounds_checked":True,
        "selected_duration_index":winner,"selected_duration_exact":controller["selected_duration_exact"],
        "short_uniform_current_transfer_bad_weight_upper":controller["short_current_bad_operation_weight_upper_exact"],
        "sharp_uniform_current_transfer_bad_weight_upper_display":float(computed[winner]),
        "failure_probability":protocol["confidence_failure"],
        "conditional_scope":"Uniform current transfer under the given Hamiltonian class and stated design/pulse/gap bounds, including arbitrary A/M input. The received scores do not establish those physical premises. A and M were not reset for this scalar acquisition. Final receiver isolation is an explicit operation; no free stream extraction is claimed.",
        "controller_sha256":sha256((HERE/"acquired_transfer_timing_controller.json").read_bytes()).hexdigest(),
        "certificate_sha256":sha256((HERE/"transfer_timing_certificate.json").read_bytes()).hexdigest(),
    }
    (HERE/"transfer_timing_independent_review.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()

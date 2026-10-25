"""Received-only selection of a DD-protected exchange duration.

Reads the public structural/design protocol and actual paired weak words.
It receives no native exchange J, interaction matrices, bath state or errors.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb, isqrt
from pathlib import Path
import argparse
import json
import numpy as np

HERE=Path(__file__).resolve().parent


def sqrt_upper(x,bits=48):
    x=F(x);den=1<<bits
    target=x.numerator*den*den
    numerator=isqrt(target//x.denominator)
    if numerator*numerator*x.denominator<target:numerator+=1
    out=F(numerator,den)
    assert out*out>=x
    return out


def tail(eta,length):
    p=(1+eta)/2
    return sum(F(comb(length,j))*p**j*(1-p)**(length-j)
               for j in range(length//2+1))


def design_allowance(protocol,duration):
    cycles=int(protocol["cycles"])
    v=F(protocol["v_bound"])
    j_bound=F(protocol["J_absolute_bound"])
    kappa_m=F(protocol["kappa_M_bound"])
    kappa=kappa_m+4*j_bound*v
    assert kappa==F(protocol["kappa_bound"])
    coefficient=kappa/4+v*v/2
    assert coefficient==F(protocol["cycle_error_coefficient"])
    pairs=int(protocol["pair_pulses_per_cycle"])*cycles
    pulse=F(protocol["pair_pulse_half_diamond_allowance"])*pairs
    gap=F(protocol["residual_interface_gap_duration"])*F(protocol["residual_gap_local_norm_bound"])
    truncation=coefficient*duration*duration/cycles
    return min(F(1),truncation+pulse+gap),{
        "finite_cycle_term":str(truncation),"pulse_term":str(pulse),"residual_gap_term":str(gap),
        "cycle_coefficient":str(coefficient),"physical_pair_pulses":pairs,
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--protocol",type=Path,default=HERE/"transfer_protocol.json")
    parser.add_argument("--record",type=Path,default=None)
    parser.add_argument("--output",type=Path,default=HERE)
    args=parser.parse_args()
    protocol=json.loads(args.protocol.read_text())
    record_path=args.record or args.protocol.parent/protocol["actual_received_record"]
    durations=[F(str(x))for x in protocol["duration_menu"]]
    k=len(durations);delta=F(protocol["confidence_failure"])
    assert k==5 and delta==F(1,100)
    length=int(protocol["weak_length"])
    eta=F(protocol["weak_contrast"])
    assert 0<eta<1 and length%2==1
    weak_gain=1-2*tail(eta,length);gamma=weak_gain*weak_gain
    assert weak_gain==F(*protocol["weak_gain_fraction"])
    assert gamma==F(*protocol["score_gamma_fraction"])
    with np.load(record_path)as record:
        indices=record["duration_index"].astype(int)
        assert set(np.unique(indices))==set(range(k))
        assert set(np.unique(record["outer_axis"]))<={0,1,2}
        pre=record["pre_words"].copy();post=record["post_words"].copy()
        assert np.all(pre>>length==0)and np.all(post>>length==0)
    before=np.array([1-2*(int(word).bit_count()>length//2)for word in pre],dtype=np.int8)
    after=np.array([1-2*(int(word).bit_count()>length//2)for word in post],dtype=np.int8)
    score=before*after
    term=exp_sum=F(1);degree=0
    while exp_sum<=1000:
        degree+=1;term*=F(7,degree);exp_sum+=term
    rows=[]
    for index,duration in enumerate(durations):
        selected=indices==index;n=int(selected.sum())
        assert n==int(protocol["calls_per_duration"])
        signed=int(np.sum(score[selected],dtype=np.int64))
        estimate=F(3,4)*(1-F(signed,n)/gamma)
        radius=F(3,4)/gamma*sqrt_upper(F(14,n))
        isolation,terms=design_allowance(protocol,duration)
        ideal_upper=estimate+radius+isolation
        actual_upper=min(F(1),max(F(0),ideal_upper+isolation))
        short=F((actual_upper.numerator*1000+actual_upper.denominator-1)//actual_upper.denominator,1000)
        rows.append({
            "duration_index":index,"duration_exact":str(duration),"duration_display":float(duration),
            "received_calls":n,"paired_signed_sum":signed,
            "received_error_estimate_exact":str(estimate),"received_error_estimate_display":float(estimate),
            "statistical_radius_upper_exact":str(radius),"statistical_radius_upper_display":float(radius),
            "closure_allowance_exact":str(isolation),"closure_allowance_display":float(isolation),
            "closure_terms":terms,
            "ideal_reference_error_upper_exact":str(ideal_upper),
            "actual_current_error_upper_exact":str(actual_upper),"actual_current_error_upper_display":float(actual_upper),
            "short_current_error_upper_exact":str(short),"short_current_error_upper_display":float(short),
        })
    winner=min(rows,key=lambda row:(F(row["actual_current_error_upper_exact"]),row["duration_index"]))
    controller={
        "format":"astra_acquired_exchange_duration_v1",
        "selected_duration_index":winner["duration_index"],
        "selected_duration_exact":winner["duration_exact"],
        "selected_duration_display":winner["duration_display"],
        "decoupling_cycles":int(protocol["cycles"]),
        "current_bad_operation_weight_upper_exact":winner["actual_current_error_upper_exact"],
        "short_current_bad_operation_weight_upper_exact":winner["short_current_error_upper_exact"],
        "current_bad_operation_weight_upper_display":winner["actual_current_error_upper_display"],
        "failure_probability":str(delta),
        "native_J_bath_or_hidden_error_labels_received":False,
        "physical_target":protocol["task"],
        "physical_class":protocol["physical_class"],
        "scope":"One current transfer using the actual selected synchronized-pulse duration and explicit output isolation. No protected many-output stream or free physical extraction is implemented by relabeling tensor factors.",
        "calibration_record_sha256":sha256(record_path.read_bytes()).hexdigest(),
        "protocol_sha256":sha256(args.protocol.read_bytes()).hexdigest(),
    }
    certificate={
        "received_only":True,"native_J_bath_matrix_state_or_error_labels_read":False,
        "duration_menu_count":k,"calibration_calls":len(indices),
        "weak_gain_exact":str(weak_gain),"score_gamma_exact":str(gamma),
        "failure_probability":str(delta),"two_sided_union_factor":1000,
        "rational_log_upper":"7","exp_Taylor_degree":degree,"exp_Taylor_partial_sum_exact":str(exp_sum),
        "duration_results":rows,"selected":winner,
        "estimator":"qhat=3/4*(1-mean(pre_majority*post_majority)/gamma)",
        "statistical_proof":"Five bounded conditional-score means, two tails and delta=.01 give log1000<7. Actual A/M histories may be arbitrary. Scalar reference task effects, derived from the declared exchange class, make the ideal q(T) independent of those states. Exact physical Pauli framing and the uniform channel design bound limit calibration Pauli-event bias by epsilon(T).",
        "selection_proof":"Every duration's upper bound holds on the same confidence event. Minimise qhat+r+epsilon_cal+epsilon_deploy; here both epsilon values are the separately charged public design allowance. The selected duration need not estimate J itself.",
        "design_information_not_acquired":"Exact isotropic-exchange symmetry, coupling/commutator bounds, pair-pulse quality, residual-gap bound, trusted full weak instruments and matched Pauli frames are physical design premises. The five scores do not prove absence of an exchange-modulated bath or an unmodelled bypass.",
        "duration_coverage":"The certificate is for the chosen finite menu. A claim that some duration approximates a swap requires a separate timing/parameter-range coverage argument; no native J label is supplied to this observer.",
        "physical_resource_scope":protocol["no_many_output_claim"],
        "calibration_record_sha256":controller["calibration_record_sha256"],
        "protocol_sha256":controller["protocol_sha256"],
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/"acquired_transfer_timing_controller.json").write_text(json.dumps(controller,indent=2)+"\n")
    (args.output/"transfer_timing_certificate.json").write_text(json.dumps(certificate,indent=2)+"\n")
    print(json.dumps({"rows":rows,"selected":winner},indent=2))


if __name__=="__main__":main()

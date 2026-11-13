"""ROOT-owned introduced operation screens; no experimental properties are supplied."""
import json, math
from pathlib import Path

def chemical_competition(n, q, rho):
    f = rho*q/(1-q+rho*q)
    e = -math.expm1(math.log(.9)/n)
    return dict(steps=n, feed_wrong=q, relative_wrong_acceptance=rho,
                wrong_at_incorporation=f, whole_correct=(1-f)**n,
                maximum_feed_wrong_for_90pct=e/(rho*(1-e)+e))

def gamma_cdf_integer(n,x):
    p=math.exp(-x); s=p
    for j in range(1,n):
        p *= x/j
        s += p
    return max(0.0,min(1.0,1-s))

def handover(n, correct, wrong, loss, window, release=.95):
    lam=correct+wrong+loss
    complete=gamma_cdf_integer(n,lam*window)
    any_full=((correct+wrong)/lam)**n*complete
    good_full=(correct/lam)**n*complete
    p=math.exp(-lam*window); unfinished=p
    for j in range(1,n):
        p *= (correct+wrong)*window/j
        unfinished += p
    hydrolyzed=1-any_full-unfinished
    categories=dict(correct_complete=good_full, wrong_complete=any_full-good_full,
                    unfinished=unfinished, hydrolyzed=hydrolyzed)
    assert min(categories.values()) > -1e-12
    assert abs(sum(categories.values())-1)<1e-12
    return dict(steps=n, correct_rate=correct, wrong_rate=wrong, loss_rate=loss,
                window_s=window, categories=categories,
                correctness_among_complete=good_full/any_full if any_full else None,
                correct_released_fraction=release*good_full,
                correct_released_nmol_from_2nmol=2*release*good_full,
                rate_ratios=dict(wrong_to_correct=wrong/correct,loss_to_correct=loss/correct))

def reset(pass_success,persistent,passes,stock=32):
    left=persistent+(1-persistent)*(1-pass_success)**passes
    return dict(pass_success=pass_success,persistent_fraction=persistent,passes=passes,
                remaining_fraction=left,remaining_nmol=stock*left)

def material():
    t=.038
    n=20; area=80; transferred=.98; removed=4.655
    gross=n*area*t
    extra=transferred*gross-removed
    local_extra=6*area*t-.931
    return dict(scope="Declared film geometry; no installed material, weld, fatigue or machining property",
                initial_thickness_mm=t,patch_area_mm2=area,patches=n,
                gross_patch_mm3=gross,placed_patch_mm3=transferred*gross,
                removed_old_mm3=removed,net_extra_solid_mm3=extra,
                equivalent_new_single_layer_area_mm2=extra/t,
                local_six_extra_patches_minus_one_removal_mm3=local_extra,
                local_extra_area_at_original_gauge_mm2=local_extra/t,
                eight_layers=dict(thickness_mm=8*t,
                    fully_bonded_bending_rigidity_relative_to_one=8**3,
                    freely_sliding_equal_layers_relative_to_one=8,
                    nominal_outer_fibre_strain_at_2mm_radius=8*t/(2*2)))

def run():
    competition=[chemical_competition(20,q,r) for r in (1,10,20,100) for q in (.0001,.001)]
    cases=[handover(20,.1,.0003,.0002,600),
           handover(20,.1,.003,.0002,600),
           handover(20,.02,.0003,.0002,600),
           handover(20,.1,.0003,.005,600),
           handover(100,.1,.0003,.0002,3600)]
    z=[reset(.95,z,k) for z in (0,.001,.005,.01) for k in (1,3,6)]
    return dict(scope="INTRODUCED models only: no measured reaction rates, purity, local register, reagent, device, advantage or independent physical validation",
                chemical_competition=competition,
                finite_incorrect_stock_counting=dict(programs=16,accepted_nmol_each=1,
                    total_growth_nmol=320,feed_excess=8,feed_wrong=.001,
                    incorrect_input_nmol=320*8*.001,
                    per_program_worstcase_90pct_count_allowance_nmol=.1,
                    note="Only a conservative counting allowance; no inference that all incorrect stock incorporates, or that errors concentrate in one program"),
                product_handover=cases,reset_with_persistent_sites=z,
                constant_gauge_material_balance=material())

if __name__=="__main__":
    p=Path(__file__).with_suffix(".json")
    p.write_text(json.dumps(run(),indent=2,sort_keys=True)+"\n")
    print(json.dumps(dict(path=str(p),bytes=p.stat().st_size)))

"""Exact finite-state reliability formulas; hypothetical rates, not measurements."""
import json, math
from pathlib import Path

def survival(t, damage, repair):
    a = repair + 3 * damage
    gap = math.sqrt(a*a - 8*damage*damage)
    slow = (-a+gap)/2
    fast = (-a-gap)/2
    # S(0)=1 and S'(0)=0 because two separate failures are needed.
    return (-fast*math.exp(slow*t)+slow*math.exp(fast*t))/gap

def main():
    assert abs(survival(2, 1, 0) - (2*math.exp(-2)-math.exp(-4))) < 1e-14
    rows=[]
    for ratio in [0,1,10,100,1000]:
        s=survival(1,1,ratio)
        rows.append({"repair_over_damage":ratio,
                     "mean_patch_lifetime_in_damage_units":(ratio+3)/2,
                     "patch_survival_at_one_damage_time":s,
                     "100_patch_frame_survival":s**100})
    ambiguity=[]
    for k in range(1,11):
        targets=list(range(2**k))
        # Any fixed output distribution sums to one over disjoint correct targets.
        uniform_guess=[1/len(targets)]*len(targets)
        assert abs(sum(uniform_guess)/len(targets)-2**(-k)) < 1e-15
        ambiguity.append({"erased_routing_bits":k,"average_success_upper":2**(-k)})
    out={"status":"synthetic exact-formula checks only; not enzyme kinetics or physical validation",
         "formula":"mean_absorption=(mu+3lambda)/(2lambda^2)",
         "hypothetical_rates":True,"reliability":rows,"routing_ambiguity":ambiguity}
    p=Path(__file__).with_name("repair_model_results.json")
    p.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))

if __name__ == "__main__": main()

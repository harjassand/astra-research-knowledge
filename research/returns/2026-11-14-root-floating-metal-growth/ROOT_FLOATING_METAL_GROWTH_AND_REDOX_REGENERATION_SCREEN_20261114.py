#!/usr/bin/env python3
"""Introduced floating-conductor kinetics and finite redox regeneration.
Not a fit, physical experiment, electroplating recipe, or field solver.
Serial standard-library calculation. No external code/data or network.
"""
import math, json
from pathlib import Path

F = 96485.33212
R = 8.31446261815324
T = 298.15
VT = R*T/F
ZM = 2.0
MCU = 0.063546              # kg/mol, nominal reference, not material qualification
RHO = 8960.0               # kg/m3, INTRODUCED nominal density
LENGTH = 0.020             # INTRODUCED m
DIAMETER = 50e-6           # INTRODUCED m
VOLUME = math.pi*(DIAMETER/2)**2*LENGTH
TARGET_MOL = RHO*VOLUME/MCU
TARGET_Q = ZM*F*TARGET_MOL
R0 = 12e-6                # INTRODUCED mol reduced carrier
O0 = 12e-6                # INTRODUCED mol oxidized carrier
CU0 = 100e-6              # INTRODUCED dissolved copper mol
FEED0 = 100e-6            # INTRODUCED external copper donor mol
E_R0 = -0.100             # INTRODUCED V formal carrier potential
PHI_D = 0.120             # INTRODUCED solution potential at growth patch
PHI_A = 0.0               # INTRODUCED solution potential at existing patch A
PHI_B = -0.040            # INTRODUCED solution potential at joined old patch B
I0_D = 20e-6              # INTRODUCED aggregate exchange-current coefficient
I0_A = 200e-6             # INTRODUCED coefficient for existing metal patch A
I0_B = 200e-6
I0_R = 400e-6
JOIN_TIME = 100.0
# State: reduced, oxidized, dissolved-Cu, donor-Cu, growth-charge,
# old-A signed oxidative-charge, old-B signed oxidative-charge,
# regeneration-charge, gross-A-oxidation, gross-B-oxidation, regenerator-work.
# Positive metal current dissolves metal. Negative current deposits metal.

def currents(v, reduced, oxidized, cu, joined=False, field_guard=False, block_b=1.0, collector_guard=False, guard_error=0.):
    c = cu/CU0
    def metal(i0, phi, w=v):
        a = ZM*(w-phi)/(2*VT)
        ep, em = math.exp(a), math.exp(-a)
        return i0*(ep-c*em), i0*ZM/(2*VT)*(ep+c*em)
    d, dd = metal(I0_D, PHI_D)
    a, da = metal(I0_A, PHI_A)
    b, db = metal(I0_B*block_b, PHI_A if field_guard else PHI_B) if joined else (0.,0.)
    phi_r=0.
    if collector_guard:
        # INTRODUCED independently controlled ionic potential at the
        # carrier collector. It is not an electronic wire to the product.
        # The field guard separately puts all old metal at phi_A.
        # All needed state/geometry knowledge is ideal and explicitly paid
        # as an unresolved physical sensing/control operation.
        desired=PHI_A+VT/ZM*math.log(c)+guard_error
        total_metal=metal(I0_D,PHI_D,desired)[0]+metal(I0_A,PHI_A,desired)[0]
        if joined:total_metal+=metal(I0_B*block_b,PHI_A if field_guard else PHI_B,desired)[0]
        q=-total_metal/I0_R
        rr,oo=reduced/R0,oxidized/O0
        z=(q+math.sqrt(q*q+4*rr*oo))/(2*rr)
        phi_r=desired-E_R0-2*VT*math.log(z)
    ar = (v-phi_r-E_R0)/(2*VT)
    ep, em = math.exp(ar), math.exp(-ar)
    rr, oo = reduced/R0, oxidized/O0
    redox = I0_R*(rr*ep-oo*em)
    dr = I0_R/(2*VT)*(rr*ep+oo*em)
    return (d,a,b,redox), dd+da+db+dr

def solve(reduced, oxidized, cu, joined=False, field_guard=False, block_b=1.0, collector_guard=False, guard_error=0.):
    if min(reduced,oxidized,cu) <= 0: raise ValueError("finite stock exhausted")
    lo, hi, v = -.5, .5, 0.0
    for _ in range(70):
        js, deriv = currents(v,reduced,oxidized,cu,joined,field_guard,block_b,collector_guard,guard_error)
        total = sum(js)
        if abs(total) < 2e-15: return v, js, total
        if total > 0: hi = v
        else: lo = v
        proposal = v-total/deriv
        v = proposal if lo < proposal < hi else (lo+hi)/2
    raise ArithmeticError("floating-potential solve failed")

def rhs(y, case, joined):
    v, (jd,ja,jb,jr), residual = solve(y[0],y[1],y[2],joined,case["field_guard"],case["block_b"],case["collector_guard"],case["guard_error_V"])
    # Explicitly ideal, observed well-mixed carrier feedback; no real sensor,
    # mixing, membrane, transport delay, or selective regenerator supplied.
    desired = max(0., (y[1]-O0)*F/case["tau_s"])
    regen = min(case["regen_max_A"],desired) if y[3] > 0 else 0.
    # Ideal separate regenerator: O+e -> R; Cu(feed) -> Cu++ + 2e.
    # Its counterelectrode and compatibility are introduced, not constructed.
    return [(regen-jr)/F,(jr-regen)/F,(regen-jr)/(ZM*F),-regen/(ZM*F),
            -jd,ja,jb,regen,max(ja,0.),max(jb,0.),case["regen_V"]*regen]

def rk4(y,dt,case,joined):
    k1=rhs(y,case,joined)
    k2=rhs([a+dt*b/2 for a,b in zip(y,k1)],case,joined)
    k3=rhs([a+dt*b/2 for a,b in zip(y,k2)],case,joined)
    k4=rhs([a+dt*b for a,b in zip(y,k3)],case,joined)
    return [a+dt*(b+2*c+2*d+e)/6 for a,b,c,d,e in zip(y,k1,k2,k3,k4)]

def integrate(case, dt):
    y=[R0,O0,CU0,FEED0,0.,0.,0.,0.,0.,0.,0.]
    t=0.; joined=False; first_a_oxidation=None; first_b_oxidation=None
    max_residual=0.; vm_min=1.; vm_max=-1.; join_receipt=None
    samples=[]; next_sample=0.; limiter_events=[]
    while t < 1800 and y[4] < TARGET_Q:
        if case["join"] and not joined and t >= JOIN_TIME-1e-9:
            before=solve(y[0],y[1],y[2],False,case["field_guard"],case["block_b"],case["collector_guard"],case["guard_error_V"])
            joined=True
            after=solve(y[0],y[1],y[2],True,case["field_guard"],case["block_b"],case["collector_guard"],case["guard_error_V"])
            join_receipt={"time_s":t,"before_V":before[0],"after_V":after[0],
                          "before_currents_A":before[1],"after_currents_A":after[1],
                          "isolated_B_potential_before_V":PHI_B+VT/ZM*math.log(y[2]/CU0)}
        v,js,res=solve(y[0],y[1],y[2],joined,case["field_guard"],case["block_b"],case["collector_guard"],case["guard_error_V"])
        max_residual=max(max_residual,abs(res)); vm_min=min(vm_min,v);vm_max=max(vm_max,v)
        if js[1] > 1e-12 and first_a_oxidation is None:first_a_oxidation=t
        if js[2] > 1e-12 and first_b_oxidation is None:first_b_oxidation=t
        if t >= next_sample-1e-8:
            samples.append({"t_s":t,"Vm_V":v,"R_umol":y[0]*1e6,"O_umol":y[1]*1e6,
                            "growth_Q_C":y[4],"old_A_Q_C":y[5],"old_B_Q_C":y[6],
                            "current_A":js})
            next_sample += 100.
        h=min(dt,1800-t)
        if case["join"] and not joined and t < JOIN_TIME:h=min(h,JOIN_TIME-t)
        candidate=rk4(y,h,case,joined)
        # Split the first entry into current limiting. The regulator is
        # continuous but its slope changes here; stepping across that kink
        # otherwise dominates the coarse-step convergence comparison.
        limit=case["regen_max_A"]*case["tau_s"]
        s0=(y[1]-O0)*F-limit
        s1=(candidate[1]-O0)*F-limit
        if case["regen_max_A"]>0 and s0 < -1e-12 and s1 > 0:
            lo,hi=0.,h
            for _ in range(38):
                mid=(lo+hi)/2
                if (rk4(y,mid,case,joined)[1]-O0)*F < limit:lo=mid
                else:hi=mid
            h=(lo+hi)/2;candidate=rk4(y,h,case,joined)
            limiter_events.append(t+h)
        if candidate[4] >= TARGET_Q:
            lo,hi=0.,h
            for _ in range(36):
                mid=(lo+hi)/2
                if rk4(y,mid,case,joined)[4] < TARGET_Q:lo=mid
                else:hi=mid
            h=(lo+hi)/2;candidate=rk4(y,h,case,joined)
        y=candidate;t+=h
    v,js,res=solve(y[0],y[1],y[2],joined,case["field_guard"],case["block_b"],case["collector_guard"],case["guard_error_V"])
    # Old A/B start with one target-volume of metal EACH. B exists even
    # when disconnected. Signed dissolution lowers each local inventory.
    initial_cu=CU0+FEED0+2*TARGET_MOL
    final_cu=y[2]+y[3]+y[4]/(ZM*F)+(TARGET_MOL-y[5]/(ZM*F))+(TARGET_MOL-y[6]/(ZM*F))
    carrier_error=y[0]+y[1]-R0-O0
    copper_error=final_cu-initial_cu
    # Ideal regenerative charge and finite stock accounting, NOT wall power.
    return {"case":case["name"],"dt_s":dt,"tip_charge_target_reached":y[4]>=TARGET_Q*(1-1e-10),
            "tip_charge_target_time_s":t,"tip_growth_charge_C":y[4],"target_volume_mm3":VOLUME*1e9,
            "target_mass_mg":TARGET_MOL*MCU*1e6,
            "old_A_net_loss_fraction":y[5]/TARGET_Q,"old_B_net_loss_fraction":y[6]/TARGET_Q,
            "old_A_gross_oxidation_C":y[8],"old_B_gross_oxidation_C":y[9],
            "retains_each_old_patch_within_one_percent_net_loss":max(y[5],y[6])<=.01*TARGET_Q,
            "each_old_patch_absolute_net_mass_change_under_one_percent":max(abs(y[5]),abs(y[6]))<=.01*TARGET_Q,
            "first_A_positive_oxidation_s":first_a_oxidation,"first_B_positive_oxidation_s":first_b_oxidation,
            "remaining_R_umol":y[0]*1e6,"remaining_O_umol":y[1]*1e6,
            "remaining_ion_Cu_umol":y[2]*1e6,"remaining_donor_Cu_umol":y[3]*1e6,
            "regeneration_C":y[7],"regenerator_only_J":y[10],
            "Vm_range_V":[vm_min,vm_max],"final_V":v,"final_currents_A":js,
            "carrier_balance_error_mol":carrier_error,"copper_balance_error_mol":copper_error,
            "max_sampled_current_closure_residual_A":max(max_residual,abs(res)),
            "join_transition":join_receipt,"regenerator_limit_events_s":limiter_events,"samples":samples}

def initial_critical_stock():
    # Pre-merge, no regeneration. If x mol R has been oxidized, charge
    # conservation gives dissolved Cu = CU0 - x/2, even when the two
    # copper patches exchange material. At zero current on old A,
    # Vm = phi_A + E_Cu, an exact threshold for this kinetic model.
    def fn(x):
        cu=CU0-x/ZM;v=PHI_A+VT/ZM*math.log(cu/CU0)
        js,_=currents(v,R0-x,O0+x,cu)
        return sum(js),v
    lo,hi=0.,R0*(1-1e-10)
    assert fn(lo)[0] > 0 and fn(hi)[0] < 0
    for _ in range(70):
        mid=(lo+hi)/2
        if fn(mid)[0] > 0:lo=mid
        else:hi=mid
    x=(lo+hi)/2
    return {"oxidized_R_umol_at_old_A_zero_current":x*1e6,
            "net_metal_charge_C_at_threshold":x*F,"threshold_V":fn(x)[1],
            "residual_A":fn(x)[0]}

def unguarded_off_state(reduced,oxidized,cu,joined,block_b=1.0):
    # Instantaneous rates only after all solution potential differences
    # and active guards are removed. The introduced downhill carrier is
    # NOT inert merely because the external spatial drive is off.
    c=cu/CU0
    def evaluate(v):
        a=ZM*v/(2*VT); ep,em=math.exp(a),math.exp(-a)
        unit=ep-c*em
        jd,ja,jb=I0_D*unit,I0_A*unit,(I0_B*block_b*unit if joined else 0.)
        b=(v-E_R0)/(2*VT)
        jr=I0_R*((reduced/R0)*math.exp(b)-(oxidized/O0)*math.exp(-b))
        return (jd,ja,jb,jr)
    lo,hi=-.5,.5
    for _ in range(80):
        mid=(lo+hi)/2
        if sum(evaluate(mid)) > 0:hi=mid
        else:lo=mid
    v=(lo+hi)/2;js=evaluate(v)
    return {"Vm_V":v,"currents_A":js,"initial_old_A_fractional_mass_change_rate_s_inv":-js[1]/TARGET_Q,
            "scope":"instantaneous state only, no constant-rate extrapolation, installed reaction map or passive lifetime"}

def main():
    base={"regen_max_A":0.,"tau_s":5.,"regen_V":1.,"join":False,"field_guard":False,"block_b":1.,"collector_guard":False,"guard_error_V":0.}
    settings=[
        dict(base,name="finite_unregenerated"),
        dict(base,name="regenerated",regen_max_A=.004),
        dict(base,name="rate_limited_regenerator",regen_max_A=.001),
        dict(base,name="regenerated_then_merge",regen_max_A=.004,join=True),
        dict(base,name="merge_with_introduced_B_passivation",regen_max_A=.004,join=True,block_b=.001),
        dict(base,name="merge_with_introduced_field_guard",regen_max_A=.004,join=True,field_guard=True),
        dict(base,name="merge_with_two_ionic_guards",regen_max_A=.004,join=True,field_guard=True,collector_guard=True),
        dict(base,name="two_guards_plus_1mV_error",regen_max_A=.004,join=True,field_guard=True,collector_guard=True,guard_error_V=.001),
        dict(base,name="two_guards_plus_2mV_error",regen_max_A=.004,join=True,field_guard=True,collector_guard=True,guard_error_V=.002)
    ]
    results=[integrate(c,dt) for c in settings for dt in (.2,.1,.05)]
    for out in results:
        setting=next(c for c in settings if c["name"]==out["case"])
        nr=out["remaining_R_umol"]*1e-6;no=out["remaining_O_umol"]*1e-6;cu=out["remaining_ion_Cu_umol"]*1e-6
        out["instant_unguarded_off_state"]=unguarded_off_state(nr,no,cu,setting["join"],setting["block_b"])
        deficit=max(0.,(R0-nr)*F)
        # Conditional isolate-FIRST restoration, not free withdrawal:
        # assume ALL product-metal/electrolyte reaction paths are removed,
        # then finish regeneration at 4mA. No real drain/rinse/film-clearing
        # device, its time or energy is supplied by this calculation.
        out["conditional_isolate_then_restore"]={
          "unconstructed_condition":"all product reactions blocked before guards are disabled; exact final stock observation",
          "restore_carrier_charge_C":deficit,"extra_regenerator_time_s_at_4mA":deficit/.004,
          "extra_regenerator_J_at_1V":deficit,
          "remaining_external_donor_Cu_umol_after_restoration":out["remaining_donor_Cu_umol"]-deficit/(ZM*F)*1e6,
          "final_R_umol":R0*1e6,"final_O_umol":O0*1e6,
          "final_ion_Cu_umol":(cu+deficit/(ZM*F))*1e6,
          "omitted":"physical quench/drain/rinse/carryover/membrane/observation/feeder/pump costs and time"}
    convergence=[]
    for c in settings:
        rs=[r for r in results if r["case"]==c["name"]]
        convergence.append({"case":c["name"],
            "charge_target_time_range_s":max(r["tip_charge_target_time_s"] for r in rs)-min(r["tip_charge_target_time_s"] for r in rs),
            "old_A_loss_range":max(r["old_A_net_loss_fraction"] for r in rs)-min(r["old_A_net_loss_fraction"] for r in rs),
            "old_B_loss_range":max(r["old_B_net_loss_fraction"] for r in rs)-min(r["old_B_net_loss_fraction"] for r in rs)})
    assert all(r["tip_charge_target_reached"] for r in results)
    assert max(abs(r["copper_balance_error_mol"]) for r in results)<1e-15
    assert max(abs(r["carrier_balance_error_mol"]) for r in results)<1e-15
    assert max(r["max_sampled_current_closure_residual_A"] for r in results)<2.1e-15
    assert max(r["charge_target_time_range_s"] for r in convergence)<1e-5, json.dumps(convergence)
    for r in results:
        if r["case"] in ("regenerated","merge_with_introduced_B_passivation","merge_with_introduced_field_guard"):
            assert r["retains_each_old_patch_within_one_percent_net_loss"]
        if r["case"]=="regenerated_then_merge":
            assert not r["retains_each_old_patch_within_one_percent_net_loss"]
        if r["case"] in ("merge_with_two_ionic_guards","two_guards_plus_1mV_error"):
            assert r["each_old_patch_absolute_net_mass_change_under_one_percent"]
        if r["case"]=="two_guards_plus_2mV_error":
            assert not r["each_old_patch_absolute_net_mass_change_under_one_percent"]
    # A matched ideal WIRED, spatially confined deposition reference has
    # the same tip kinetic law and prescribed -0.12 V overpotential, no
    # old wetted patches, no redox carrier. Not an installed machine.
    wired_current=2*I0_D*math.sinh(ZM*.12/(2*VT))
    output={"scope":"INTRODUCED quasistatic lumped electrochemical kinetics, finite stocks, ideal external regenerator; no field/flow/shape/contact/chemistry qualification",
       "constants":{"F":F,"VT_V":VT,"z_Cu":ZM,"nominal_Cu_molar_mass_kg_mol":MCU,
                    "introduced_Cu_density_kg_m3":RHO,"wire_length_m":LENGTH,"wire_diameter_m":DIAMETER,
                    "R0_mol":R0,"O0_mol":O0,"Cu_ions0_mol":CU0,"donor0_mol":FEED0,
                    "formal_carrier_E_V":E_R0,"phi_growth_V":PHI_D,"phi_A_V":PHI_A,"phi_B_V":PHI_B,
                    "I0_growth_A":I0_D,"I0_oldA_A":I0_A,"I0_oldB_A":I0_B,"I0_carrier_A":I0_R},
       "target":{"mol":TARGET_MOL,"charge_C":TARGET_Q,"volume_mm3":VOLUME*1e9,"mass_mg":RHO*VOLUME*1e6},
       "analytic_stock_threshold":initial_critical_stock(),
       "uniform_retention_error_bound":{"introduced_max_duration_s":600.,"introduced_max_Cu_activity_ratio":1.01,
          "introduced_fractional_net_mass_tolerance":.01,
          "sufficient_absolute_overpotential_error_V":2*VT/ZM*math.asinh(.01*TARGET_Q/(2*I0_A*math.sqrt(1.01)*600.)),
          "scope":"only the stated uniform-patch kinetic law; not morphology, installed potential accuracy or geometry"},
       "wired_ideal_reference":{"tip_current_A":wired_current,"time_s":TARGET_Q/wired_current,
                              "scope":"same nominal tip kinetic law, ideal contact and localized wetting; ordinary machine costs/life/preparation not supplied"},
       "case_settings":settings,"convergence":convergence,"results":results,
       "limitations":["no measured exchange currents, redox couple, formal potentials, material density or field values",
                      "no selected actual carrier or qualified compatible three-interface regeneration chemistry",
                      "no flow/mixing/migration/concentration-boundary-layer/cavitation/bubble solver",
                      "ideal observed well-mixed feedback, zero-delay topology merge, no contact resistance or capacitance",
                      "coating and field guard are explicit introduced physical operations, not supplied hardware",
                      "net patch mass is not local morphology, adhesion, conductivity, structural function or selective erasure",
                      "only regenerator electrical work is calculated, not feeder wall power/pumps/thermal/full-cycle cost",
                      "the downhill introduced carrier can continue electroless growth with spatial drive off; isolate-first restoration is conditional and unbuilt",
                      "no new algorithm, physical invention, novelty or whole-operation advantage established"]}
    destination=Path(__file__).with_suffix(".json")
    destination.write_text(json.dumps(output,indent=2)+"\n")
    for name in [c["name"] for c in settings]:
        r=next(r for r in results if r["case"]==name and r["dt_s"]==.05)
        print(json.dumps({k:r[k] for k in ["case","tip_charge_target_time_s","old_A_net_loss_fraction","old_B_net_loss_fraction","each_old_patch_absolute_net_mass_change_under_one_percent","remaining_R_umol","regeneration_C","regenerator_only_J","first_A_positive_oxidation_s","first_B_positive_oxidation_s","join_transition"]}))
    print(json.dumps({"critical":output["analytic_stock_threshold"],"target":output["target"],"wired":output["wired_ideal_reference"],"guard_tolerance":output["uniform_retention_error_bound"],"convergence":convergence}))
if __name__=="__main__":main()


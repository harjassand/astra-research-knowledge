"""ROOT finite-stiffness passive-capture and screw-clock screens.
Independent scalar mechanics. No producer code, acquired hardware or physical execution.
"""
from pathlib import Path
import json,math,itertools
cf=1/2e6;cb=1/5e6;c=cf+cb;r0=.0004;T0=2600.
coarse=.002/72
fine=(.002-.0019)/72
rows=[]
for kj,kl,step,install,sign in itertools.product([.5e6,5e6],[1e6,10e6,36e6],[coarse,fine],[0.,10e-6,25e-6,50e-6],[-1,1]):
    eps=sign*(step+install)
    rj=r0-T0/kj;rl=r0+T0/kl+eps
    R=-kl*eps/(1+c*(kj+kl))
    req=r0-c*R
    T=kj*(req-rj);L=kl*(req-rl)
    rfree=(kj*rj+kl*rl)/(kj+kl)
    t_free=kj*(rfree-rj);l_free=kl*(rfree-rl)
    # Linear undamped instant-rest-offset proxy: r ranges from r0 to 2req-r0.
    ends=[r0,2*req-r0]
    peakT=max(abs(kj*(r-rj)) for r in ends)
    peakL=max(abs(kl*(r-rl)) for r in ends)
    peakR=2*abs(R)
    Ueq=.5*kj*(req-rj)**2+.5*kl*(req-rl)**2
    Ufree=.5*kj*(rfree-rj)**2+.5*kl*(rfree-rl)**2
    extraction=.5*R*R*(c+1/(kj+kl))
    assert abs(T+L-R)<1e-8 and abs(t_free+l_free)<1e-8
    assert abs(Ueq-Ufree-R*R/(2*(kj+kl)))<1e-9
    rows.append({"kj_N_m":kj,"kl_N_m":kl,"lead_clock_step_m":step,"additional_error_m":install,
       "rest_offset_error_m":eps,"static_outer_R_N":R,"static_internal_jam_N":T,
       "static_internal_latch_N":L,"undamped_step_peak_outer_N":peakR,
       "undamped_step_peak_jam_N":peakT,"undamped_step_peak_latch_N":peakL,
       "equilibrium_interface_separation_m":req,"free_captured_separation_m":rfree,
       "free_captured_internal_N":t_free,"free_captured_energy_J":Ufree,
       "host_and_cartridge_adjustment_energy_J":extraction,
       "instant_rest_offset_excitation_energy_J":.5*(kl*eps)**2/(1/c+kj+kl),
       "outer_static_within80N":abs(R)<=80,"peak_latch_within3kN":peakL<=3000})
# A particular misleading outer-force example.
example=next(z for z in rows if z["kj_N_m"]==.5e6 and z["kl_N_m"]==36e6 and
             z["lead_clock_step_m"]==coarse and z["additional_error_m"]==0 and z["rest_offset_error_m"]>0)
summaries=[]
for name,step in [("introduced_2mm_lead_72teeth",coarse),("introduced_2minus1p9mm_differential_72teeth",fine)]:
    q=[z for z in rows if z["lead_clock_step_m"]==step]
    summaries.append({"name":name,"axial_clock_m":step,"cases":len(q),
        "max_static_outer_N":max(abs(z["static_outer_R_N"]) for z in q),
        "max_step_peak_latch_N":max(z["undamped_step_peak_latch_N"] for z in q),
        "both_pass_count":sum(z["outer_static_within80N"] and z["peak_latch_within3kN"] for z in q)})
out={"scope":"Introduced scalar elastic model; no actual dog-engagement, backlash-impact, damping, friction, manufacture, life or six-axis capture certificate.",
     "parameters":{"cf_m_N":cf,"cb_m_N":cb,"host_relative_compliance_m_N":c,"baseline_relative_separation_m":r0,
                   "introduced_internal_preload_N":T0,"introduced_latch_capacity_N":3000},
     "relations":{"outer_static":"R=-kl*eps/[1+c*(kj+kl)]","host_constraint":"r=r0-c*R",
                   "free_cartridge":"r_free=(kj*rj+kl*rl)/(kj+kl); internal opposing forces persist",
                   "instant_offset_energy":"(kl*eps)^2/[2*(1/c+kj+kl)]",
                   "outer_adjustment_release":"0.5*R^2*[c+1/(kj+kl)]",
                   "clock":"axial step = net screw lead / tooth count; does not include installation, thread, bearing, wear or temperature errors"},
     "specific_false_assurance_example":example,"summaries":summaries,
     "force_margin_requirement":{"at_36MN_m_max_extra_rest_error_for_T0plus_kl_eps_below3kN_m":(3000-T0)/36e6,
                                  "scope":"Necessary one-sign initial-force condition in the instant-offset proxy, not a sufficient dynamic/strength certificate."},
     "kinematic_cost":{"coarse_turns_for_0p78mm":.00078/.002,
                        "differential_turns_for_0p78mm":.00078/(.002-.0019),
                        "speed_ratio_at_same_input_rpm":.002/(.002-.0019),
                        "ideal_3kN_output_lead_torque_Nm":3000*.002/(2*math.pi),
                        "ideal_3kN_differential_input_torque_Nm":3000*(.002-.0019)/(2*math.pi),
                        "scope":"Ideal reversible work only. Both differential thread interfaces carry axial load; actual friction, preload, bearings, capture, gearing and heat must be paid."},
     "cases":rows}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!="cases"},indent=2))

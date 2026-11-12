"""ROOT independent cut-witness, captive-cassette rollback and service-port screens.
No producer code or physical experiment. All unreferenced properties introduced.
"""
from pathlib import Path
import math,itertools,json

def inverse(M):
    n=len(M);a=[list(map(float,row))+[float(i==j) for j in range(n)] for i,row in enumerate(M)]
    for j in range(n):
        p=max(range(j,n),key=lambda i:abs(a[i][j]))
        if abs(a[p][j])<1e-12:raise ValueError("singular")
        a[j],a[p]=a[p],a[j];v=a[j][j];a[j]=[z/v for z in a[j]]
        for i in range(n):
            if i!=j:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    return [r[n:] for r in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return math.sqrt(dot(a,a))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def mv(a,x):return [dot(r,x) for r in a]
cols=[];legs=[]
for i in range(6):
    theta=math.radians(i*60);alpha=theta+math.radians(40 if i%2==0 else -40)
    ra,rb=(.250,.220) if i%2==0 else(.330,.300)
    A=[-.170,ra*math.cos(alpha),ra*math.sin(alpha)]
    B=[.170,rb*math.cos(theta),rb*math.sin(theta)]
    d=[a-b for a,b in zip(A,B)];L=norm(d);n=[v/L for v in d];col=n+cross(B,n);cols.append(col)
    legs.append({"A_m":A,"B_m":B,"L_m":L})
W=[list(r) for r in zip(*cols)];Wi=inverse(W)
maxloads=[1000*norm(r[:3])+250*norm(r[3:]) for r in Wi]
# Small motion J q = gap, J = W^T. An explicit linear pose-error corner screen.
Ji=inverse(cols)
corners=[]
for signs in itertools.product([-1,1],repeat=6):
    q=mv(Ji,[s*65e-6 for s in signs]);corners.append({"signs":signs,"translation_m":norm(q[:3]),"rotation_rad":norm(q[3:])})
# A common wrench does not reveal a seventh hidden path.
h=[0,0,1,0,0,0];z=mv(Wi,h)
res=mv(W,z)
witness={"geometry":legs,"max_static_leg_N_over_simultaneous_F1000_M250":maxloads,
         "largest_65um_deadband_corner":max(corners,key=lambda x:x["translation_m"]),
         "six_leg_reaction_cancellation_per_N_hidden_zpath":z,
         "cancellation_equilibrium_residual":max(abs(a-b) for a,b in zip(res,h)),
         "scope":"Linear six-axial-leg model only; no actual universal joints, catches, contacts, stiffness or collision qualification."}
# Portable sensor validity: g_true(t) >= g_observed - bias - bounded closing speed * age.
gap=20e-6;bias=5e-6;closing=100e-6
scan=[]
for age in [.01,.1,.5,1,12,72]:
    scan.append({"age_s":age,"guaranteed_gap_m":gap-bias-closing*age})
# Zero remote shank force under a proof tool need not unload the tested connection.
kf=2e6;kb=5e6;Fext=1000.;delta=.0001;kj=5e6;kt=10e6;preload=0.
xB=Fext/kf;xC=delta
T=kj*(xB-xC)+preload
u=-T
R=T+u
# Entire fault-plus-counterforce cartridge can be removed at its two zero-resultant outer ports,
# retaining internal stress/energy until a paid rack reset. The carrier is a required construction.
stages=[
 {"state":"baseline verified frame and supported first-end workpiece","xB_m":xB,"xC_m":xC,"outer_R_N":0.},
 {"state":"failed second-end contact counterheld by service tool","joint_internal_T_N":T,"tool_N":u,"remote_shank_N":R,"outer_R_N":R,
  "joint_unloaded":False},
 {"state":"fault and counterholder captured in one rigid removable cartridge","outer_R_N":R,
  "captured_joint_T_N":T,"captured_counterholder_N":u,"stored_energy_J":T*T/(2*kj)+u*u/(2*kt)},
 {"state":"whole captured cartridge extracted; faulty contact not opened","frame_xB_m":xB,"workpiece_xC_m":xC,
  "outer_R_N":0.,"energy_travels_with_cartridge_J":T*T/(2*kj)+u*u/(2*kt)},
 {"state":"rack deenergization and refurbishment required before ready","energy_to_release_or_recover_J":T*T/(2*kj)+u*u/(2*kt)}
]
rollback={"introduced_kframe_N_m":kf,"introduced_kbar_N_m":kb,"introduced_kjam_N_m":kj,"introduced_kcounterholder_N_m":kt,
          "introduced_frame_load_N":Fext,"introduced_workpiece_natural_offset_m":delta,"stages":stages,
          "if_counterholder_released_without_captured_contact_removal":{
              "remaining_contact_force_at_old_positions_N":T,
              "linear_frame_displacement_scale_m":abs(T/kf),
              "linear_bar_displacement_scale_m":abs(T/kb)},
          "outer_force_error_bound_N":80.,
          "frame_position_error_bound_m":80/kf,"workpiece_position_error_bound_m":80/kb,
          "relative_position_error_bound_m":80/kf+80/kb,
          "scope":"Introduced coaxial scalar construction. It requires a stiff, mechanically retained carrier containing EVERY jam/contact/tool force path, two unloadable external interfaces, actual capture and extraction access. No proof for moments, hidden outer self-stress, energy release, real tool or collision-free trajectory."}
# Star-node local geometry for the cubic lattice family. Opposite rays are not infinite lines.
dirs=[]
for v in itertools.product([-1,0,1],repeat=3):
    if any(v):
        n=norm(v);dirs.append(tuple(t/n for t in v))
def raydist(s,u,v):
    q=[s*x for x in u];t=max(0.,dot(q,v));return norm([a-t*b for a,b in zip(q,v)])
rtube=math.sqrt(2)*.030/2
rtool=.040
relative_error=.0035+.015
clearances=[]
for s in [.090,.100,.120,.150,.180,.200]:
    d=min(raydist(s,u,v) for u in dirs for v in dirs if u!=v)
    clearances.append({"port_station_m":s,"min_ray_centerline_distance_m":d,
                       "tube_circumradius_m":rtube,"tool_outer_radius_m":rtool,
                       "introduced_relative_pose_drift_budget_m":relative_error,
                       "remaining_radial_clearance_m":d-rtube-rtool-relative_error})
# Whole-service overhead arithmetic uses rounded producer ledger; not a free-calibration design.
cost={"P1_operational_h":16.556,"P1_assisted_h":76.667,
      "tenfold_ceiling_h":76.667/10,"needed_reduction_h":16.556-76.667/10,
      "initial_plus_periodic_calibration_h":6+3.333,
      "IF_free_all_calibration_remaining_h":16.556-6-3.333,
      "IF_free_all_calibration_ratio":76.667/(16.556-6-3.333),
      "P2_candidate_total_paid_h":3.014,"P2_assisted_total_paid_h":3.448,
      "P2_total_paid_ratio":3.448/3.014,
      "P2_distributed_pin_plus_witness_capital_USD":112000+19950,
      "P2_portable_challenge_installed_USD":193300,
      "scope":"Current estimates only; calibration and portable instrumentation must actually be manufactured, operated and paid, with equivalent evidence/access. Intervention and total labor are different."}
out={"scope":"ROOT original conditional constructions/screens, not physical validation or an all-design obstruction.",
     "P1_six_axis_topology_and_reaction_screen":witness,
     "portable_gap_witness":{"introduced_observed_gap_m":gap,"introduced_installed_bias_m":bias,"introduced_closing_speed_m_s":closing,
         "maximum_age_for_strictly_positive_gap_s":(gap-bias)/closing,"age_sweep":scan,
         "scope":"A shared probe needs a physical freeze or a sufficient bounded drift/freshness contract; reading an old positive gap is insufficient. No actual drift or lock certificate supplied."},
     "P2_captive_rollback":rollback,
     "local_service_port":{"ray_count":len(dirs),"clearances":clearances,
                          "minimum_station_for_zero_clearance_m":(rtube+rtool+relative_error)/math.sqrt(1/3),
                          "scope":"Static straight-ray local screen only, introduced outer tool radius/drift. Does not include actual hub shape, fingers, cables, wrist, holder, carried bar or a complete robot trajectory."},
     "whole_service_cost_constraints":cost}
out["hardware_compatibility"]={"P1_module_kg":85,"gravity_N":85*9.81,"P2_retained_tool_budget_N":100,"gravity_over_retained_tool_budget":85*9.81/100,"hypothetical_42kg_P1_nodes_on_32node_P2_frame_kg":42*32,"P2_original_above_pedestal_frame_kg":209.18,"mass_ratio":42*32/209.18,"scope":"Illustrates why shared topology ideas do not supply compatible hardware; actual mounting and load allocation may differ."}
# An observation-only controller for the scalar captive rollback. Plant parameters remain private.
controlled=[]
for hidden_kj,hidden_t0,biasR,biasU in itertools.product([.5e6,2e6,5e6],[500.,1500.,2500.],[-30.,30.],[-5.,5.]):
    denominator=1+hidden_kj*(1/kf+1/kb)
    command=0.;history=[]
    for iteration in range(300):
        applied=command+biasU
        trueR=(hidden_t0+applied)/denominator
        observedR=trueR+biasR
        history.append((command,observedR))
        if abs(observedR)<=20:break
        # Controller uses only observedR and command history, not denominator, t0 or trueR.
        command=max(-2990.,min(2990.,command-max(-100.,min(100.,observedR))))
    else:raise RuntimeError("bounded example did not converge")
    controlled.append({"private_plant_kjam_N_m":hidden_kj,"private_plant_internal_T0_N":hidden_t0,
        "private_sensor_bias_N":biasR,"private_actuator_bias_N":biasU,"iterations":iteration,
        "observed_R_N":observedR,"true_outer_R_N":trueR,"counterholder_force_N":applied,
        "joint_internal_force_N":trueR-applied,"frame_offset_from_prior_m":-trueR/kf,
        "workpiece_offset_from_prior_m":trueR/kb,"controller_pass":abs(observedR)<=20,
        "plus_admitted_drag20_within_release80":abs(trueR)+20<=80})
out["observation_only_captive_rollback"]={"cases":len(controlled),"all_pass":all(z["controller_pass"] and z["plus_admitted_drag20_within_release80"] for z in controlled),
    "max_iterations":max(z["iterations"] for z in controlled),"max_actual_counterholder_N":max(abs(z["counterholder_force_N"]) for z in controlled),
    "max_actual_joint_internal_N":max(abs(z["joint_internal_force_N"]) for z in controlled),
    "max_true_outer_N":max(abs(z["true_outer_R_N"]) for z in controlled),"case_results":controlled,
    "scope":"A bounded scalar observation-feedback construction only. Requires physical force metrology, mechanically retained 3kN-class captive carrier, safe trajectory, finite stocks and paid energy reset. Not the full P2 construction service or a hidden-label controller."}
out["local_service_port"]["independent_node_drift_33_5mm_case"]={"relative_budget_m":.0335,
    "zero_clearance_station_m":(rtube+rtool+.0335)/math.sqrt(1/3),
    "clearance_at_150mm_m":.150/math.sqrt(3)-rtube-rtool-.0335,
    "clearance_at_180mm_m":.180/math.sqrt(3)-rtube-rtool-.0335,
    "scope":"Two independently bounded15mm node motions can consume30mm relative allowance before3.5mm positioning. The18.5mm case is a separate introduced relative bound, not implied by those node bounds."}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(out,indent=2,allow_nan=False))

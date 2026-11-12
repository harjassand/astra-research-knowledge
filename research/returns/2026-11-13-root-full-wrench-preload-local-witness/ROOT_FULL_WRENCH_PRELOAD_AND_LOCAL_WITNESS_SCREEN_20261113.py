"""ROOT-owned linear preload ambiguity and introduced flexure design screen.

All spring, geometry, material and sensor parameters below are introduced.
No source-table property, vendor rating or physical test is supplied.
"""
import json
import math
import random


def cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0]]


def norm(a):
    return math.sqrt(sum(x*x for x in a))


RADIUS = .1
SPRING = 1e6
POINTS = [(RADIUS*math.cos(2*math.pi*i/3),
           RADIUS*math.sin(2*math.pi*i/3), 0.) for i in range(3)]
# Three identical isotropic point springs on an ideal rigid moving plate.
# Sum r_i=0, so translational/rotational blocks decouple.
STIFFNESS = [3*SPRING]*3 + [1.5*SPRING*RADIUS**2]*2 + [3*SPRING*RADIUS**2]


def state(wrench, radial_preload):
    q = [v/k for v, k in zip(wrench, STIFFNESS)]
    forces=[]
    for r in POINTS:
        move=[u+v for u,v in zip(q[:3],cross(q[3:],r))]
        forces.append([SPRING*u+radial_preload*x/RADIUS for u,x in zip(move,r)])
    total=[sum(f[j] for f in forces) for j in range(3)]
    moments=[cross(r,f) for r,f in zip(POINTS,forces)]
    total += [sum(m[j] for m in moments) for j in range(3)]
    return {"pose":q,"contact_forces_N":forces,
            "contact_resultant_N":[norm(f) for f in forces],
            "measured_global_wrench":total,
            "equilibrium_residual":max(abs(a-b) for a,b in zip(total,wrench))}


def proof():
    load=[0.,0.,1000.,250.,0.,0.]
    unpreloaded=state(load,0.)
    self_stressed=state(load,1500.)
    # Same complete small-signal stiffness for all probes, not just one axis.
    rng=random.Random(1622)
    err=0.
    for _ in range(100):
        w=[rng.uniform(-1000,1000) for _ in range(3)]+[rng.uniform(-250,250) for _ in range(3)]
        a,b=state(w,0.),state(w,1500.)
        assert a['pose']==b['pose']
        err=max(err,max(abs(x-y) for x,y in zip(a['measured_global_wrench'],b['measured_global_wrench'])))
    limit=2000.
    assert max(unpreloaded['contact_resultant_N'])<limit
    assert max(state([0.]*6,1500.)['contact_resultant_N'])<limit
    assert max(self_stressed['contact_resultant_N'])>limit
    return {"introduced_contact_radius_m":RADIUS,
            "introduced_isotropic_point_spring_N_m":SPRING,
            "complete_stiffness_diagonal":STIFFNESS,
            "service_wrench_Fxyz_N_Mxyz_Nm":load,
            "introduced_local_force_limit_N":limit,
            "unpreloaded":unpreloaded,"self_stressed_1500N_radial":self_stressed,
            "global_probe_comparison_max_roundoff":err,
            "source_of_nonidentifiability":"self-equilibrated initial contact forces do not enter the tangent rigid-body stiffness in this linear model",
            "limits":"ideal rigid plates, bilateral linear springs and no geometric stiffness; nonlinear real responses may reveal preload but need their own model and resolution"}


def opposed_pair_proof():
    # Each point's net spring is split into two half-stiffness branches.
    # Opposite preload cancels at EACH point, avoiding the uncancelled
    # geometric-stiffness problem of spatially separated radial preload.
    wrench=[0.,0.,1000.,250.,0.,0.]
    outer=state(wrench,0.)
    p=700.
    pairs=[]
    for f in outer['contact_forces_N']:
        pairs.append([[v/2+(p if j==2 else 0) for j,v in enumerate(f)],
                      [v/2-(p if j==2 else 0) for j,v in enumerate(f)]])
    restored=[[sum(pair[h][j] for h in range(2)) for j in range(3)] for pair in pairs]
    err=max(abs(a-b) for f,g in zip(restored,outer['contact_forces_N']) for a,b in zip(f,g))
    baseline=[norm(f)/2 for f in outer['contact_forces_N']]
    hidden=[norm(f) for pair in pairs for f in pair]
    limit=1000.
    assert max(baseline)<limit and p<limit and max(hidden)>limit and err<1e-9
    return {"outer_state":outer,"introduced_preload_per_opposed_branch_N":p,
            "baseline_individual_branch_force_N":baseline,
            "opposed_preloaded_branch_vectors_N":pairs,
            "opposed_preloaded_branch_resultants_N":hidden,
            "introduced_individual_branch_limit_N":limit,
            "net_contact_force_difference_N":err,
            "nonlinear_coaxial_pair_identity":"k(L-L0-P/k)+k(L-L0+P/k)=2k(L-L0); collinear opposite initial forces cancel for every L",
            "limits":"collocated effective endpoints and matching branch force laws; actual finite spacing, force-law mismatch, buckling, internal sensors and independently releasing a branch can expose the state"}


def flexure():
    # A candidate guarded single force path, not an actual three-axis load cell.
    modulus,length,width,thickness=200e9,.03,.04,.005
    force=2000.
    inertia=width*thickness**3/12
    stiffness=3*modulus*inertia/length**3
    stress=6*force*length/(width*thickness**2)
    strain_per_N=6*length/(modulus*width*thickness**2)
    return {"introduced_E_Pa":modulus,"introduced_l_w_t_m":[length,width,thickness],
            "force_N":force,"I_m4":inertia,"stiffness_N_m":stiffness,
            "deflection_mm":force/stiffness*1000,
            "root_nominal_stress_MPa":stress/1e6,
            "surface_strain_microstrain":stress/modulus*1e6,
            "strain_budget_for_total_5N_force_error_microstrain":5*strain_per_N*1e6,
            "introduced_10microstrain_per_K_uncorrected_thermal_error_N_per_K":10/(strain_per_N*1e6),
            "minimum_nominal_yield_for_introduced_factor2_MPa":2*stress/1e6,
            "limits":"no qualified material, notch/end/clamp/shear/cross-axis/fatigue/gauge/ADC/temperature/hysteresis map; source datasheet was inaccessible and not imported"}


if __name__=='__main__':
    print(json.dumps({"frozen_geometry_radial_example":proof(),
                      "opposed_branch_pair":opposed_pair_proof(),
                      "local_flexure_witness":flexure()},indent=2))

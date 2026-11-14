"""Independent selector-error and geometric-acceptance diagnostics.
Anchor dimensions are producer-INTRODUCED geometry from the AVAILABLE text,
not qualified hardware and not reconstructed linked code or files.
Only this OWN NumPy script is executed.
"""
from pathlib import Path
import numpy as np, math, json
AZ=np.arange(3)*2*math.pi/3
A=np.c_[.014*np.cos(AZ),.014*np.sin(AZ),np.full(3,.007)]
RAD=np.array([.009,.014,.019])
BXY=np.c_[RAD*np.cos(AZ+math.pi/3),RAD*np.sin(AZ+math.pi/3)]
B0=np.c_[BXY,np.full(3,-.007)]
ELL=np.linalg.norm(A-B0,axis=1)
def hat(v):
    x,y,z=v
    return np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])
def rotation(k):
    v=.05*np.r_[k,0.];a=float(np.linalg.norm(v));K=hat(v)
    return np.eye(3) if a==0 else np.eye(3)+math.sin(a)/a*K+(1-math.cos(a))/a**2*K@K
def state(k):
    Q=rotation(k);qa=A@Q.T;dxy=qa[:,:2]-BXY
    rad=ELL**2-np.sum(dxy*dxy,axis=1)
    assert rad.min()>0
    h=qa[:,2]-np.sqrt(rad)
    B=np.c_[BXY,h]
    u=(qa-B)/ELL[:,None]
    H=np.cross(qa,u)/u[:,2,None]
    assert np.max(np.abs(np.linalg.norm(qa-B,axis=1)-ELL))<1e-14
    assert np.linalg.svd(H,compute_uv=False).min()>1e-4
    return Q,h,H
rows=[]
for x in [-2,0,2]:
    for y in [-2,0,2]:
        Q,h,H=state([x,y]);sv=np.linalg.svd(H,compute_uv=False)
        rows.append(dict(kappa_per_m=[x,y],height_m=h.tolist(),height_jacobian_m_per_rad=H.tolist(),
            singular_values_m_per_rad=sv.tolist(),
            one_um_per_coordinate_angle_bound_rad=float(math.sqrt(3)*1e-6/sv[-1])))
# An OWN illustrative transition, not the producer's unavailable cam profile/order.
ka=np.array([-2.,0.]);kb=np.array([-2.,2.]);span=math.radians(38)
def hcurve(theta):
    t=theta/span;w=10*t**3-15*t**4+6*t**5
    return state(ka+(kb-ka)*w)[1]
theta=span/2;eps=1e-6
v=(hcurve(theta+eps)-hcurve(theta-eps))/(2*eps)
Q,h,H=state((ka+kb)/2)
Jinv=np.linalg.inv(H);control=Jinv@v
# Choose an angular error perpendicular to the one-dimensional control direction.
axis=np.eye(3)[np.argmin(abs(control))]
direction=np.cross(control,axis);direction/=np.linalg.norm(direction)
raw_height=H@direction
e=raw_height*(1e-6/np.linalg.norm(raw_height))
raw_angle=Jinv@e
best_theta=float(control@raw_angle/(control@control))
residual_angle=raw_angle-control*best_theta
assert abs(best_theta)<1e-10
assert np.linalg.norm(residual_angle)>.999999*np.linalg.norm(raw_angle)
# On the flat locked land, derivative h'(theta)=0: no local correction at all.
flat_e=np.array([1e-6,-1e-6,1e-6]);flat_H=state([0,0])[2]
flat_angle=np.linalg.solve(flat_H,flat_e)
# Separate physical error from measurement uncertainty.
base_mm=2.468;height_um=1.316;transfer_mm_per_um=.337
physical_bound_mm=base_mm+height_um*transfer_mm_per_um
noise_per_coordinate_mm=.060
noise_ball_mm=math.sqrt(3)*noise_per_coordinate_mm
safe_observation_threshold_mm=3-noise_ball_mm
true_errors_mm=np.array([2.95,3.05]);noise_mm=np.array([.05,-.05])
assert np.allclose(true_errors_mm+noise_mm,[3.,3.])
# Hypothetical differential expansion. Not measured Al/steel properties.
alpha_contrast_per_K=11e-6;gauge_m=.014;delta_T_K=2.
thermal_offset_um=1e6*alpha_contrast_per_K*gauge_m*delta_T_K
thermal_bound_increment_mm=thermal_offset_um*transfer_mm_per_um
# Quoted fixed-ledger arithmetic is a finite assessment diagnostic only.
cost=dict(candidate=4446.,stock=2159.,ordinary_forming=2524.)
cost["candidate_with_free_stock"]=cost["candidate"]-cost["stock"]
cost["thirty_percent_target"]=.7*cost["ordinary_forming"]
cost["remaining_gap_after_free_stock"]=cost["candidate_with_free_stock"]-cost["thirty_percent_target"]
result=dict(scope="INTRODUCED local constraint/control model and separate physical/observational bounds; not physical qualification",
    geometry=dict(upper_anchors_m=A.tolist(),lower_xy_m=BXY.tolist(),fixed_prop_lengths_m=ELL.tolist(),
        source="dimensions exposed in P2 AVAILABLE return; not producer code/report/ZIP recovery"),
    stations=rows,
    one_control_moving_example=dict(introduced_transition="quintic between (-2,0) and (-2,2); NOT supplied producer profile",
        span_deg=38.,derivative_m_per_rad=v.tolist(),height_error_m=e.tolist(),
        raw_angular_error_rad=raw_angle.tolist(),best_selector_change_rad=best_theta,
        remaining_angular_error_rad=residual_angle.tolist(),
        angular_residual_deg=float(np.linalg.norm(residual_angle)*180/math.pi),
        height_error_norm_um=float(np.linalg.norm(e)*1e6),
        controllable_rank=1,uncontrolled_linear_dimensions=2),
    flat_land=dict(derivative_zero_assumption=True,controllable_rank=0,
        independent_height_error_m=flat_e.tolist(),angular_error_rad=flat_angle.tolist(),
        angular_error_deg=float(np.linalg.norm(flat_angle)*180/math.pi),
        constraints="accepted locked state stays on flat land with same pin/geometry"),
    accuracy=dict(physical_bound_mm=physical_bound_mm,remaining_physical_margin_mm=3-physical_bound_mm,
        noise_per_coordinate_mm=noise_per_coordinate_mm,noise_norm_bound_mm=noise_ball_mm,
        safe_measured_norm_threshold_mm=safe_observation_threshold_mm,
        physical_bound_plus_noise_is_NOT_a_physical_error=True,
        ambiguous_observation=dict(true_errors_mm=true_errors_mm.tolist(),noise_mm=noise_mm.tolist(),
            observed_norm_mm=[3.,3.],both_allowed_noise=True),
        hypothetical_thermal_height_offset_um=thermal_offset_um,
        hypothetical_physical_increment_mm=thermal_bound_increment_mm,
        hypothetical_physical_bound_with_uncancelled_thermal_mm=physical_bound_mm+thermal_bound_increment_mm,
        unknowns="actual temperature field, installed calibration, common-mode cancellation and material coefficients"),
    fixed_ledger=cost,
    ordinary_readiness_ratio=372/342,ordinary_former_ratio=482/342,
    complete_prepare_to_ready_s=dict(candidate=1028,ordinary_clamp=770,ordinary_former=646),
    checks=dict(nine_real_station_geometries=True,prop_length_identity=True,
        local_constraint_invertible=True,uncontrolled_error_constructed=True,
        same_observation_good_bad=True),
    limits=["Local first variations do not prove finite cam reachability, contact stiffness, life or stability.",
        "Profile errors could be corrected by additional independent physical adjustments, remanufacture or another lock; those operations are not constructed here.",
        "The campaign already allows small persistent errors to remain while measured function passes; no automatic failure is inferred.",
        "Measurement noise limits observation-based acceptance, not the physical shape itself.",
        "Unqualified thermal constants and an exposed aggregate sensitivity are not an installed thermal error map.",
        "A fixed ledger diagnostic does not rule out other designs, logistics or all geometry-writing inventions."])
path=Path(__file__).with_suffix(".json");path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({k:result[k] for k in ["one_control_moving_example","flat_land","accuracy","fixed_ledger","checks"]},indent=2))


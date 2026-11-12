"""ROOT-owned passive magnetic contact / backing-compliance model.
Standard library only. No producer code, hardware or qualified material data.
The force-gap law and every array property are introduced, not a fit to a source.
"""
from pathlib import Path
import json, math

SIGNS=[(-1,-1),(-1,1),(1,-1),(1,1)]
V=[sx*sy for sx,sy in SIGNS]
A=.0125  # m; 20 mm cells centered at +/-12.5 mm occupy a 45 mm square
GC=.00025
F0=180.0
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def fm(q,amp):return amp/(1+q/GC)**2
def dfm(q,amp):return -2*amp/GC/(1+q/GC)**3
def all_equilibria(k,h,rest,amps,fn,mx,my):
    # B columns (1, sy, -sx), scaled rotations have units of length.
    tpart=[fn/4+sy*mx/(4*A)-sx*my/(4*A) for sx,sy in SIGNS]
    kg=k/4
    def forces(q):
        s=dot(V,[x-r for x,r in zip(q,rest)])
        return [p-kg*v*s for p,v in zip(tpart,V)]
    def build(q,free):
        ts=forces(q);nr=[fm(x,f)-t for x,f,t in zip(q,amps,ts)]
        if any(nr[i]<-1e-7 for i in range(4) if i!=free):return None
        if free is not None and (q[free]<h[free]-1e-12 or abs(nr[free])>1e-6):return None
        # Nondegenerate seated contacts or a strict interior one-cell minimum.
        # Exact zero-reaction seated degeneracies require a unilateral second-
        # variation analysis; this calculation does not certify such states.
        if any(abs(nr[i])<1e-8 for i in range(4) if i!=free):return None
        curve=None if free is None else kg+dfm(q[free],amps[free])
        if free is not None and curve<=1e-8:return None
        ds=[t/k+x-r for t,x,r in zip(ts,q,rest)]
        z=sum(ds)/4
        py=sum(sy*d for (_,sy),d in zip(SIGNS,ds))/4
        px=-sum(sx*d for (sx,_),d in zip(SIGNS,ds))/4
        # x/y signs correspond to d=z+sy*py-sx*px.
        opens=[z+sy*(.025/A)*py-sx*(.025/A)*px for sx,sy in SIGNS]
        return {"open_cell":free,"cell_gaps_m":q,"transmitted_N":ts,
                "contact_compression_N":nr,"z_m":z,
                "rotation_rad":math.hypot(px,py)/A,
                "largest_absolute_corner_motion_m":max(map(abs,opens)),
                "reduced_open_cell_curvature_N_m":curve,
                "equilibrium_residual":max(abs(sum(ts)-fn),
                    abs(sum(sy*t for (_,sy),t in zip(SIGNS,ts))-mx/A),
                    abs(sum(-sx*t for (sx,_),t in zip(SIGNS,ts))-my/A)),
                "local_normal_compliance_scope":"Static four-cell model, compression allowed; no keys, shear, material creep, dynamics or contact-strength qualification."}
    ans=[]
    e=build(h[:],None)
    if e:ans.append(e)
    # With n=4 normal supports and three rigid-plate DOF, elastic reduced
    # Hessian k*N has rank one. For >=2 freely opening live magnetic cells,
    # diag(f') is negative along a null vector: no strictly stable equilibrium.
    # Consequently all strict local minima have zero or one free gap.
    for j in range(4):
        # F(q)=C-kg*q-fm(q). F is concave; its decreasing-side root is stable.
        c=tpart[j]-kg*V[j]*sum(V[i]*(h[i]-rest[i]) for i in range(4) if i!=j)+kg*rest[j]
        upper=c/kg
        if upper<h[j]-1e-12:continue
        peak=(2*amps[j]*GC*GC/kg)**(1/3)-GC if amps[j]>0 else h[j]
        lo=max(h[j],peak);hi=upper
        fun=lambda q:c-kg*q-fm(q,amps[j])
        if hi<lo or fun(lo)<-1e-9:continue
        for _ in range(85):
            mid=(lo+hi)/2
            if fun(mid)>0:lo=mid
            else:hi=mid
        q=h[:];q[j]=(lo+hi)/2
        e=build(q,j)
        if e and not any(max(abs(x-y) for x,y in zip(e["cell_gaps_m"],old["cell_gaps_m"]))<1e-10 for old in ans):ans.append(e)
    return ans

def representative(k,h,preset,amps=None,fn=500,mx=0,my=0):
    amps=amps or [F0]*4
    es=all_equilibria(k,h,h[:] if preset else [0.]*4,amps,fn,mx,my)
    return {"k_N_m":k,"initial_gaps_m":h,"individually_reset_rest_lengths":preset,
            "F0_N":amps,"Fn_N":fn,"Mx_Nm":mx,"My_Nm":my,
            "strictly_stable_static_states":es,
            "meaning_of_empty":"No nondegenerate strictly stable state found in this four-cell force-gap model; exact zero-contact-reaction degeneracies are uncertified. Not proof of failure of an actual magnet or all possible interfaces."}

# Finite examples and a normal+bending envelope sweep. No shear capability assumed.
examples=[]
for k in [1e6,2e6,4e6,8e6]:
    for preset in [False,True]:
        examples.append(representative(k,[.0001,0.,0.,0.],preset))
examples.extend([representative(1e6,[0.]*4,False),
                 representative(1e6,[0.]*4,False,fn=0,mx=5),
                 representative(8e6,[0.]*4,True,amps=[0.,F0,F0,F0])])
grid=[]
defects={"clean":[0.]*4,"one20um":[20e-6,0.,0.,0.],
         "one50um":[50e-6,0.,0.,0.],"one100um":[100e-6,0.,0.,0.],
         "diagonal50um":[50e-6,0.,0.,50e-6],"all100um":[100e-6]*4}
for k in [.5e6,1e6,2e6,4e6,8e6]:
    for label,h in defects.items():
        for preset in [False,True]:
            count=0;within=0;largest_motion=0.;worst_residual=0.
            for fraction in [0.,.25,.5,.75,1.]:
                for ai in range(16):
                    angle=2*math.pi*ai/16
                    es=all_equilibria(k,h,h[:] if preset else [0.]*4,[F0]*4,
                                      500*fraction,5*(1-fraction)*math.cos(angle),
                                      5*(1-fraction)*math.sin(angle))
                    if es:
                        count+=1
                        e=min(es,key=lambda x:x["largest_absolute_corner_motion_m"])
                        largest_motion=max(largest_motion,e["largest_absolute_corner_motion_m"])
                        worst_residual=max(worst_residual,e["equilibrium_residual"])
                        if e["largest_absolute_corner_motion_m"]<=.0002:within+=1
            grid.append({"k_N_m":k,"gap_case":label,"preset":preset,
                         "sampled_normal_bending_loads":80,
                         "have_strict_stable_state":count,"also_within_0_2mm":within,
                         "max_motion_of_selected_stable_states_m":largest_motion,
                         "max_equilibrium_residual":worst_residual})
# Clean constrained face: force per contact = Fn/4 +/- M/(4a).
# The maximum of a linear functional over Fn/500+|M|/5<=1 is the
# maximum at a pure endpoint; arbitrary bending direction matters.
normal_extreme=500/4
moment_extreme=5*math.sqrt(2)/(4*A)
normal_force_needed_for_friction_shear=1000/.3
footprint=.05**2
required_flux_for_friction=math.sqrt(2*4*math.pi*1e-7*normal_force_needed_for_friction_shear/footprint)
# Source points only: do not combine the small measured device with introduced F0.
# An inverse-square law fitted to the first two points misses the third.
gfit=.0001/(math.sqrt(14.6/7.7)-1)
source_comparison={"Wang_Stokes_main_points_N_at_gap_m":[[0.,14.6],[.0001,7.7],[.001,2.34]],
 "inverse_square_fit_first_two_gc_m":gfit,
 "first_two_point_model_at_1mm_N":14.6/(1+.001/gfit)**2,
 "scope":"Diagnostic inadequacy of this two-point scalar surrogate, not a paper reconstruction or universal magnetic law.",
 "Li_2026_read_TableI_radius_m":.032,
 "Li_2026_read_magnetic_assembly_mass_kg":.272,
 "radius_32mm_exceeds_50mm_square_width":True}
out={"scope":"INTRODUCED quasi-static normal contact model only. A current curve or pulse is not supplied; no useful working joint, 500-cycle life, actual sensor, manufacturing yield or cost advantage.",
 "derivation":{"potential":"0.5*k*sum((B.T*a-q+rest)^2)+sum(-F0*gc/(1+q/gc))-w.a, q>=h",
 "normal_transmission":"t=tpart-(k/4)*v*(v.(q-rest)), v=(1,-1,-1,1)",
 "reduced_free_gap_hessian":"k*v*v.T/4+diag(fmag_prime); with >=2 positive-amplitude free cells it has a negative direction",
 "stability_claim":"Local static stability only; exact zero-reaction seated degeneracies are uncertified. Equilibrium selection from assembly history, dynamic basin, rate dependence, hysteresis, B-H state and finite compression capacity remain open."},
 "examples":examples,"grid":grid,"source_comparison":source_comparison,
 "geometry_and_traction":{"support_half_span_m":A,"footprint_m":[.05,.05],
 "introduced_single_cell_footprint_m":[.02,.02],
 "introduced_single_cell_F0_N":F0,"introduced_gc_m":GC,
 "max_single_cell_tension_over_full_normal_bending_envelope_N":max(normal_extreme,moment_extreme),
 "normal_endpoint_N_per_cell":normal_extreme,"arbitrary_angle_bending_endpoint_N_per_cell":moment_extreme,
 "introduced_single_cell_average_B_T_from_Maxwell_pressure":math.sqrt(2*4*math.pi*1e-7*F0/.02**2),
 "clean_8MN_per_cell_max_independent_reset_error_m_from_static_margin_only":(F0-max(normal_extreme,moment_extreme))/8e6,
 "clean_8MN_per_cell_force_error_N_for_each_5um_reset_error":8e6*5e-6,
 "introduced_four_cell_magnetic_potential_depth_J":4*F0*GC,
 "energy_scope":"Magnetic mechanical potential depth is not switching energy or a whole-cycle purchased-energy estimate.",
 "friction_mu_introduced":.3,"pure1000Nshear_requires_normal_clamp_N":normal_force_needed_for_friction_shear,
 "ideal_uniform_flux_T_over_entire_footprint_for_that_clamp":required_flux_for_friction,
 "key_note":"A positive shear key can change this friction requirement but is the actual mechanical joint. Bearing, cam-out, backlash, access, wear and receiver preparation must then be constructed and paid."}}
# Meaningful internal checks: closed-contact force/moment solution and stationary stability.
clean=all_equilibria(1e6,[0.]*4,[0.]*4,[F0]*4,500,0,0)[0]
assert max(abs(t-125) for t in clean["transmitted_N"])<1e-9
assert abs(clean["z_m"]-.000125)<1e-12
assert 2*A+.02<=.05
assert max(x["equilibrium_residual"] for e in examples for x in e["strictly_stable_static_states"])<1e-6
assert all(e["reduced_open_cell_curvature_N_m"] is None or e["reduced_open_cell_curvature_N_m"]>0 for e in examples for e in e["strictly_stable_static_states"])
dest=Path(__file__).with_suffix(".json")
dest.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"output":str(dest),"examples":[{"k":e["k_N_m"],"preset":e["individually_reset_rest_lengths"],
 "count":len(e["strictly_stable_static_states"]),"states":[{"open":x["open_cell"],"gap_um":[q*1e6 for q in x["cell_gaps_m"]],
 "forces":x["transmitted_N"],"corner_um":x["largest_absolute_corner_motion_m"]*1e6} for x in e["strictly_stable_static_states"]]} for e in examples],
 "source_comparison":source_comparison,"traction":out["geometry_and_traction"]},indent=2))

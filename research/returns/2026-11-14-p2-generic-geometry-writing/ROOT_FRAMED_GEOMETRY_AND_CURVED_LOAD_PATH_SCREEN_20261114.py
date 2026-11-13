"""Introduced framed-rod kinematics and curved-load-path diagnostics.
No material fit, hardware, physical experiment, or full-class service certificate.
R maps material vectors to world coordinates, opposite to Q in Gazzola 2018.
Only NumPy is used, serially. No producer source/code is executed.
"""
from pathlib import Path
import json, math
import numpy as np

L, ZONES = 0.5, 10
HZ = L / ZONES
E, WIDTH, DEPTH, DENSITY = 5e8, .04, .035, 1200.
AREA = WIDTH * DEPTH
MASS = DENSITY * AREA * L
BEND = np.array([E*WIDTH*DEPTH**3/12, E*DEPTH*WIDTH**3/12])
# Torsional and transverse rigidities are independent INTRODUCED effective values.
TORSION = 40.
SHEAR = np.array([2e5, 2e5, E*AREA])
GRAVITY = np.array([0., -MASS*9.81/L, 0.])
E3 = np.array([0.,0.,1.])

def crossmat(v):
    x,y,z=v
    return np.array([[0.,-z,y],[z,0.,-x],[-y,x,0.]])

def step_geometry(r,R,k,h):
    K=crossmat(k); mag=float(np.linalg.norm(k)); th=mag*h
    if mag < 1e-12:
        A=np.eye(3); J=h*np.eye(3)
    else:
        A=np.eye(3)+math.sin(th)/mag*K+(1-math.cos(th))/mag**2*(K@K)
        J=h*np.eye(3)+(1-math.cos(th))/mag**2*K+(th-math.sin(th))/mag**3*(K@K)
    return r+R@(J@E3), R@A

def trace(program, nper=20):
    r=np.zeros(3); R=np.eye(3); rs=[r.copy()]; Rs=[R.copy()]
    for xy in program:
        k=np.array([xy[0],xy[1],0.])
        for _ in range(nper):
            r,R=step_geometry(r,R,k,HZ/nper)
            rs.append(r.copy());Rs.append(R.copy())
    return np.array(rs),np.array(Rs)

def rotation_angle(R):
    return math.acos(float(np.clip((np.trace(R)-1)/2,-1,1)))

def compliance(program, torsion=TORSION, nper=20):
    rs,Rs=trace(program,nper)
    n=len(rs)-1; h=L/n
    weights=np.ones(n+1)*h;weights[[0,-1]]*=.5
    q=np.zeros_like(rs)
    # q(s) = integral_s^L (r(u)-r(s)) du.
    tail=np.zeros(3)
    for j in range(n,-1,-1):
        if j<n:tail+=.5*h*(rs[j]+rs[j+1])
        q[j]=tail-(L-j*h)*rs[j]
    C=np.zeros((6,6)); load_g=np.zeros(6)
    invB=np.diag(1/np.r_[BEND,torsion]); invS=np.diag(1/SHEAR)
    for j,(r,R,w) in enumerate(zip(rs,Rs,weights)):
        J=-crossmat(rs[-1]-r)@R
        H=np.vstack([J,R])
        C+=w*(H@invB@H.T)
        force_map=R@invS@R.T
        C[:3,:3]+=w*force_map
        load_g+=w*(H@invB@R.T@np.cross(q[j],GRAVITY))
        load_g[:3]+=w*force_map@(GRAVITY*(L-j*h))
    A=C[:3,:3]; D=C[3:,:3]
    val,vec=np.linalg.eigh(A)
    F=10*vec[:,-1]
    if (A@F)@load_g[:3]<0:F=-F
    response=C[:,:3]@F+load_g
    return dict(C=C,g=load_g,F=F,response=response,r=rs,R=Rs,
        translation_upper_mm=1000*(10*val[-1]+np.linalg.norm(load_g[:3])),
        rotation_upper_deg=180/math.pi*(10*np.linalg.svd(D,compute_uv=False)[0]+np.linalg.norm(load_g[3:])),
        particular_translation_mm=1000*np.linalg.norm(response[:3]),
        particular_rotation_deg=180/math.pi*np.linalg.norm(response[3:]))

def qrot(q):
    q=q/np.linalg.norm(q);w,x,y,z=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
        [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
        [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])

def integrate_loaded(program,F,m0,nper,torsion=TORSION):
    # Geometrically exact inextensible/unshearable static rod, dead force and
    # distributed gravity. Finite Newton/RK4 diagnostics only, no stability proof.
    invb=1/np.r_[BEND,torsion]
    y=np.r_[np.zeros(3),[1.,0.,0.,0.],m0]
    h=HZ/nper
    for j in range(ZONES):
        k0=np.r_[program[j],0.]
        def rhs(s,z):
            R=qrot(z[3:7]);t=R@E3
            k=k0+invb*(R.T@z[7:])
            qw,qx,qy,qz=z[3:7]; kx,ky,kz=k
            dq=.5*np.array([-qx*kx-qy*ky-qz*kz,
                qw*kx+qy*kz-qz*ky,qw*ky+qz*kx-qx*kz,
                qw*kz+qx*ky-qy*kx])
            return np.r_[t,dq,-np.cross(t,F+GRAVITY*(L-s))]
        for a in range(nper):
            s=j*HZ+a*h
            k1=rhs(s,y);k2=rhs(s+h/2,y+h*k1/2)
            k3=rhs(s+h/2,y+h*k2/2);k4=rhs(s+h,y+h*k3)
            y+=h*(k1+2*k2+2*k3+k4)/6
            y[3:7]/=np.linalg.norm(y[3:7])
    return y

def nonlinear(program,F,nper=20,torsion=TORSION):
    r,R=trace(program,nper); h=L/(len(r)-1)
    integ=h*(.5*r[0]+np.sum(r[1:-1],axis=0)+.5*r[-1])
    m0=np.cross(r[-1],F)+np.cross(integ,GRAVITY)
    residual=math.inf; iterations=0
    for iterations in range(12):
        out=integrate_loaded(program,F,m0,nper,torsion);res=out[7:]
        residual=float(np.linalg.norm(res))
        if residual<1e-9:break
        eps=1e-5; J=np.empty((3,3))
        for a in range(3):
            v=m0.copy();v[a]+=eps
            J[:,a]=(integrate_loaded(program,F,v,nper,torsion)[7:]-res)/eps
        dm=np.linalg.solve(J,-res)
        # This low-load solve is not a continuation through buckling branches.
        m0+=dm
    out=integrate_loaded(program,F,m0,nper,torsion)
    residual=float(np.linalg.norm(out[7:]))
    return dict(translation_mm=float(1000*np.linalg.norm(out[:3]-r[-1])),
        rotation_deg=float(rotation_angle(qrot(out[3:7])@R[-1].T)*180/math.pi),
        terminal_moment_residual_Nm=residual,iterations=iterations+1,
        root_moment_Nm=m0.tolist(),converged=bool(residual<1e-8),
        stretch_and_shear_omitted=True)

straight=np.zeros((10,2),dtype=int)
commutator=np.array([[2,0]]*2+[[0,2]]*2+[[-2,0]]*2+[[0,-2]]*2+[[0,0]]*2)
reverse=commutator[::-1].copy()
choices=np.array([(x,y) for x in [-2,0,2] for y in [-2,0,2]])
programs=[("straight",straight),("commutator",commutator),("reverse_order",reverse)]
programs += [(f"uniform_{x}_{y}",np.tile([x,y],(10,1))) for x,y in choices if x or y]
# A fixed finite collection, not a statistical sample of the whole class.
rng=np.random.default_rng(20261114)
programs += [(f"finite_{i:03d}",choices[rng.integers(0,9,size=10)]) for i in range(64)]
rows=[]; full={}
for name,p in programs:
    c=compliance(p);full[name]=(p,c)
    rows.append(dict(name=name,program=p.tolist(),tip_m=c["r"][-1].tolist(),
        endpoint_rotation_deg=float(rotation_angle(c["R"][-1])*180/math.pi),
        integrated_curvature=np.sum(p,axis=0).tolist(),
        translation_upper_mm=float(c["translation_upper_mm"]),
        rotation_upper_deg=float(c["rotation_upper_deg"]),
        particular_translation_mm=float(c["particular_translation_mm"]),
        particular_rotation_deg=float(c["particular_rotation_deg"]),
        test_force_N=c["F"].tolist()))
worst=max(rows,key=lambda v:v["translation_upper_mm"])
worst_rotation=max(rows,key=lambda v:v["rotation_upper_deg"])
keynames=list(dict.fromkeys(["straight","commutator",worst["name"],worst_rotation["name"]]))
nonlinear_checks={}
for name in keynames:
    p,c=full[name];coarse=nonlinear(p,c["F"],10);fine=nonlinear(p,c["F"],20)
    assert coarse["converged"] and fine["converged"]
    nonlinear_checks[name]=dict(coarse=coarse,fine=fine,
        displacement_refinement_change_mm=abs(coarse["translation_mm"]-fine["translation_mm"]),
        rotation_refinement_change_deg=abs(coarse["rotation_deg"]-fine["rotation_deg"]),
        linear_particular_displacement_mm=c["particular_translation_mm"],
        linear_particular_rotation_deg=c["particular_rotation_deg"],
        linear_includes_introduced_shear_extension=True,
        nonlinear_is_inextensible_unshearable=True)
torsion_screen=[]
for pname in ["straight","commutator","uniform_0_-2"]:
    for C in [40.,4.,.4]:
        c=compliance(full[pname][0],torsion=C)
        torsion_screen.append(dict(program_name=pname,torsion_Nm2=C,
            translation_upper_mm=float(c["translation_upper_mm"]),
            rotation_upper_deg=float(c["rotation_upper_deg"]),
            particular_translation_mm=float(c["particular_translation_mm"]),
            particular_rotation_deg=float(c["particular_rotation_deg"]),
            small_rotation_screen_0_1rad=bool(np.linalg.norm(c["response"][3:])<=.1)))
st=compliance(straight,nper=80);force=np.array([0.,-10.,0.])
soft_program=full["uniform_0_-2"][0]
soft_response=compliance(soft_program,torsion=4.)
soft_coarse=nonlinear(soft_program,soft_response["F"],10,torsion=4.)
soft_fine=nonlinear(soft_program,soft_response["F"],20,torsion=4.)
assert soft_coarse["converged"] and soft_fine["converged"]
analytic=(10*L**3/(3*BEND[0])+np.linalg.norm(GRAVITY)*L**4/(8*BEND[0])
    +10*L/SHEAR[1]+np.linalg.norm(GRAVITY)*L**2/(2*SHEAR[1]))
calc=np.linalg.norm((st["C"][:,:3]@force+st["g"])[:3])
assert abs(calc-analytic)<1e-7
for p,c in full.values():
    assert np.max(np.abs(c["C"]-c["C"].T))<1e-12
    assert np.linalg.eigvalsh(c["C"]).min()>0
r0,R0=trace(commutator);r1,R1=trace(reverse)
maxK=math.sqrt(8);alpha=maxK*L
minimumRigidity=min(*BEND,TORSION)
bound_mm=1000*((10*L**3/3+np.linalg.norm(GRAVITY)*L**4/8)/minimumRigidity
    +(10*L+np.linalg.norm(GRAVITY)*L**2/2)/min(SHEAR))
result=dict(scope="INTRODUCED geometry/linear-elastic/static-shooting diagnostics; no material or physical qualification",
    source_scope="Gazzola 2018 main lines 136-363 read; existing rod framework, not new rod theory",
    introduced=dict(length_m=L,mass_kg=MASS,section_m=[WIDTH,DEPTH],
        E_Pa=E,density_kg_m3=DENSITY,bending_Nm2=BEND.tolist(),
        torsion_Nm2=TORSION,shear_extension_N=SHEAR.tolist(),gravity_N_per_m=GRAVITY.tolist()),
    full_ideal_kinematic_class=dict(count=9**10,max_curvature_per_m=maxK,
        tangent_angle_bound_rad=alpha,root_axis_derivative_lower_bound=math.cos(alpha),
        centerline_injective=True,physical_solid_and_writer_access_certificate=False,
        hypotheses="exact assigned material curvature, unshearable/inextensible smooth or piecewise-continuous rod; no activation or load error"),
    noncommuting_example=dict(program=commutator.tolist(),component_integrals_rad=(HZ*np.sum(commutator,axis=0)).tolist(),
        endpoint_frame_rotation_deg=float(rotation_angle(R0[-1])*180/math.pi),
        reverse_order_same_component_integrals=True,
        order_change_endpoint_distance_mm=float(1000*np.linalg.norm(r0[-1]-r1[-1])),
        order_change_frame_distance_deg=float(rotation_angle(R0[-1]@R1[-1].T)*180/math.pi),
        intrinsic_twist_zero=True,global_frame_holonomy_is_not_intrinsic_twist=True),
    full_class_linear_sufficient_displacement_upper_mm=bound_mm,
    bound_above_gate_is_not_failure=True,
    finite_cases=len(rows),finite_collection_not_full_class_certificate=True,
    worst_translation=worst,worst_rotation=worst_rotation,rows=rows,
    straight_check=dict(analytic_mm=1000*analytic,quadrature_mm=1000*calc,
        absolute_difference_mm=1000*abs(calc-analytic)),
    nonlinear_checks=nonlinear_checks,torsion_screen=torsion_screen,
    soft_torsion_nonlinear=dict(program="uniform_0_-2",torsion_Nm2=4.,
        coarse=soft_coarse,fine=soft_fine,
        displacement_refinement_change_mm=abs(soft_coarse["translation_mm"]-soft_fine["translation_mm"]),
        rotation_refinement_change_deg=abs(soft_coarse["rotation_deg"]-soft_fine["rotation_deg"])),
    checks=dict(compliance_symmetric_positive=True,analytic_straight_check=True,
        terminal_moment_solves=True,exact_piecewise_SE3_kinematics=True),
    limitations=["Unqualified instantaneous, torsional, shear, long-time and transition properties.",
        "No local activation, durable lock, writer, installed sensor, thermal or chemical renewal construction.",
        "First variations do not prove nonlinear stability, 24-hour creep or whole-class service.",
        "Finite Newton roots and mesh comparisons do not prove uniqueness, global branch or continuum error bounds.",
        f"All {len(rows)} finite cases and {len(nonlinear_checks)+1} shooting settings are diagnostics, not manufacturing trials.",
        "No cross-section overlap, full swept paths, base/interface accuracy, cycle life or cost advantage is certified."])
path=Path(__file__).with_suffix(".json");path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({k:result[k] for k in ["introduced","full_ideal_kinematic_class",
    "noncommuting_example","full_class_linear_sufficient_displacement_upper_mm",
    "finite_cases","worst_translation","worst_rotation","straight_check",
    "nonlinear_checks","torsion_screen","soft_torsion_nonlinear","checks"]},indent=2))


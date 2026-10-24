"""Complete passive-cell force-loading calculation; no scipy dependency."""
import json, math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent

# Literal passive spring energy:
# .5(x1-x2)^2 + .5*x2^2 + .5(x1-y)^2 + V0(y).
def V0(y): return .75*(y*y-1)**2-y*y/6
def state(F,y):
    x1=(2*y+F)/3
    x2=(y+2*F)/3
    e=x2-x1
    U=.5*e*e+.5*x2*x2+.5*(x1-y)**2+V0(y)
    # Fully relaxed internal energy, at fixed dead load.
    F0=.75*(y*y-1)**2
    assert abs(U-(F*F/3+F0)) < 1e-9
    return dict(F=F,y=y,x1=x1,x2=x2,threat_extension=e,
                coupling_extension=x1-y,U=U,F0=F0,
                reduced_potential=U-F*x2)

def roots(F):
    rs=np.roots([9.,0.,-9.,-F])
    return sorted(float(r.real) for r in rs if abs(r.imag)<1e-7)
def positive(F): return max(roots(F))
def negative(F): return min(roots(F))
def bisect(fun,a,b):
    assert fun(a)*fun(b)<=0
    for _ in range(100):
        m=(a+b)/2
        if fun(a)*fun(m)<=0: b=m
        else: a=m
    return (a+b)/2

T=1.5  # both threatened and coupling springs fail at absolute extension T
S=4.0  # direct support fails at absolute extension S
Y=1.5  # bistable coordinate travel/failure limit, equally applied
Fspin=2*math.sqrt(3)
yi=-1/math.sqrt(3); yf=2/math.sqrt(3)
snap_i=state(Fspin,yi); snap_f=state(Fspin,yf)

# The favorable preselected branch has the exact same physical energy,
# spring geometry, nonlinear flexure, initial preparation energy and limits.
# Both initial global minima y=+/-1 have relaxed internal energy zero.
assert abs(state(0,-1)["U"]-state(0,1)["U"])<1e-12
# Establish that no physical spring or travel limit fails before either path
# reaches the common positive branch after the delayed snap.
for F in np.linspace(0,Fspin-1e-8,5001):
    for y in [negative(F),positive(F)]:
        q=state(F,y)
        assert abs(q["threat_extension"])<T
        assert abs(q["coupling_extension"])<T
        assert abs(q["x2"])<S
        assert abs(y)<Y
assert abs(snap_f["threat_extension"])<T
assert abs(snap_f["x2"])<S
assert abs(yf)<Y

def margin(F):
    q=state(F,positive(F))
    return max(abs(q["threat_extension"])/T,abs(q["coupling_extension"])/T,
               abs(q["x2"])/S,abs(q["y"])/Y)-1
Ffailure=bisect(margin,Fspin,10)
final=state(Ffailure,positive(Ffailure))
dU=snap_f["U"]-snap_i["U"]
W=Fspin*(snap_f["x2"]-snap_i["x2"])
D=W-dU
assert abs(D-2.25)<1e-12
assert abs(dU+.25)<1e-12
assert abs(W-2)<1e-12
# The branches are conservative outside the jump.
W_favorable=final["U"]-state(0,1)["U"]
W_delayed=final["U"]-state(0,-1)["U"]+D
res=dict(model="literal three positive springs plus bounded bistable flexure",
         physical_energy="0.5(x1-x2)^2+0.5x2^2+0.5(x1-y)^2+0.75(y^2-1)^2-y^2/6",
         controls="dead load f=(0,F), increasing F quasistatically",
         thresholds=dict(threat=T,coupling=T,direct_support=S,travel=Y),
         spinodal=dict(F=Fspin,before=snap_i,after=snap_f,
                       external_work=W,internal_energy_change=dU,dissipation=D),
         failure=final,
         comparison=dict(preparation_energy_difference=0.,
                         delayed_peak_stable_force=Ffailure,
                         favorable_peak_stable_force=Ffailure,
                         favorable_input_work=W_favorable,
                         delayed_input_work=W_delayed,
                         extra_hysteretic_absorption=D,
                         same_terminal_state=True),
         claims=dict(mechanical_model="verified finite reduced model",
                     added_fracture_strength="none over preselected favorable branch in this model",
                     material_mass_advantage="not evaluated; no fabrication law acquired",
                     novelty="UNKNOWN; generic mechanism occupied by transformation/snapping toughening"))
(HERE/"cell_comparison.json").write_text(json.dumps(res,indent=2)+"\n")
print(json.dumps(res["comparison"],indent=2))
print("All conventional-spring and flexure travel limits applied.")
print("FAILURE STATE:",json.dumps(final,indent=2))


"""ROOT-owned introduced shared-head and retained-open-contact screen."""
import json, math
from pathlib import Path

def simulate(contact_g, resistance, dt=.0001):
    t0=25.; ts=70.; tm=60.
    cj=cn=4e-5; latent=.002
    ch=.05; gh=.0005; gj=gn=.0002; pmax=.1; kp=.05
    n=4; lorenz=2.44e-8
    e=cj*(t0-t0); tn=th=t0
    melt_start=cj*(tm-t0); melt_end=melt_start+latent
    warm_s=-ch/gh*math.log1p(-gh*(ts-t0)/pmax)
    warm_j=pmax*warm_s
    th=ts
    release=None; opened=None; cooling=None; supplied=0.
    maxima=[t0,t0,th]
    def tj_from_e(e):
        if e<melt_start:return t0+e/cj
        if e<=melt_end:return tm
        return tm+(e-melt_end)/cj
    for k in range(int(8/dt)):
        t=k*dt; tj=tj_from_e(e)
        g=contact_g if opened is None else 0.
        qh=g*(th-tj)
        qb=(n*lorenz/(2*resistance))*((tj+273.15)**2-(tn+273.15)**2) if opened is None else 0.
        p=min(pmax,max(0.,gh*(ts-t0)+kp*(ts-th)))
        e += dt*(qh-qb-gj*(tj-t0))
        tn += dt*(qb-gn*(tn-t0))/cn
        th += dt*(p-qh-gh*(th-t0))/ch
        supplied += dt*p
        maxima=[max(maxima[0],tj_from_e(e)),max(maxima[1],tn),max(maxima[2],th)]
        if release is None and e>=melt_start+.95*latent:release=t+dt
        if release is not None and opened is None and t+dt>=release+.25:opened=t+dt
        if opened is not None and cooling is None and tj_from_e(e)<=30 and tn<=30:cooling=t+dt
    assert max(maxima)<=70.0001
    return dict(contact_g_WK=contact_g,resistance_ohm=resistance,dt_s=dt,
                model_95pct_melt_time_s=release,model_open_time_s=opened,
                model_two_nodes_at_most_30C_time_s=cooling,
                peak_joint_C=maxima[0],peak_neighbour_C=maxima[1],peak_head_C=maxima[2],
                cold_head_warmup_s=warm_s,cold_head_warmup_J=warm_j,
                head_supply_J_in_8s=supplied,standby_head_W=gh*(ts-t0),
                scope="All simultaneous thermal and control parameters introduced; melt fraction is plant state, not a supplied controller observation; opening and capture unconstructed")

def force_and_geometry():
    n=4; r=50e-6; tension=.6; pressure=30000; length=100e-6
    area=.6e-3*.3e-3; vacuum=50000
    rho=1e-6; density=8000
    force=n*(2*math.pi*r*tension+math.pi*r*r*pressure)
    vol=n*math.pi*r*r*length
    return dict(scope="Introduced wetted-radius, surface-tension and curvature-pressure bounds, resistivity, density and ideal vacuum seal; not actual alloy properties",
                bridge_force_bound_N=force,ideal_vacuum_force_N=area*vacuum,
                four_probe_load_N=4*.05,probe_to_ideal_vacuum_ratio=4*.05/(area*vacuum),
                nominal_bulk_bridge_resistance_ohm=rho*length/(math.pi*r*r),
                four_bridge_volume_nL=vol/1e-12,four_bridge_mass_microgram=vol*density*1e9,
                note="A transport suction capacity does not supply a retained-open test fixture under probe load")

def main():
    cases=[simulate(g,r) for g in (.0005,.001,.002,.005) for r in (.01,.1)]
    fine=simulate(.002,.01,.00005)
    ref=next(x for x in cases if x['contact_g_WK']==.002 and x['resistance_ohm']==.01)
    return dict(scope="INTRODUCED models only, no installed thermal cap, actual joint, reset, wetting, lifetime, novelty or manufacturing advantage",
                invariant="With positive passive heat flows, no internal device heat and the declared head control, every boundary at70C has nonpositive outward temperature derivative; latent enthalpy does not create heat. A real tool must establish this boundary condition.",
                thermal_cases=cases,refinement=dict(fine=fine,
                release_difference_s=abs(fine['model_95pct_melt_time_s']-ref['model_95pct_melt_time_s']),
                neighbour_peak_difference_C=abs(fine['peak_neighbour_C']-ref['peak_neighbour_C'])),
                force_and_geometry=force_and_geometry())
if __name__=="__main__":
    p=Path(__file__).with_suffix(".json");p.write_text(json.dumps(main(),indent=2,sort_keys=True)+"\n");print(str(p))

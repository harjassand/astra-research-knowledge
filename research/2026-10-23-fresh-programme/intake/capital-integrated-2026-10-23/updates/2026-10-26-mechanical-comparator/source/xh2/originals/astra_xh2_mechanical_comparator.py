"""ASTRA XH2: mechanical bridge as load-normalizing growth-feedback contract.

Independent theoretical construction, 26 Oct 2026. All rates and stiffness values are
illustrative nondimensional numbers. No empirical living mechanism implementing the
entire mechanofluidic valve/cellulose growth/repair loop is claimed.

Two reference springs a,b in series and two test springs c,d in series connect
common displaced nodes (bottom 0, top Delta). Midpoint nodes coupled by a probe
spring k>=0. The midpoint difference is a mechanical Wheatstone signal.
The test-bottom stiffness d increases when extracellular construction matures.
"""
import numpy as np
from math import erf, sqrt
from scipy.integrate import solve_ivp

def model(a=1.,b=1.,c=1.,d=.6,k=.1,Kbypass=.0,Delta=1.,force=None):
    M=np.array([[a+b+k,-k],[-k,c+d+k]])
    r=np.array([a,c])
    u=Delta*np.linalg.solve(M,r)
    Keq=a+c+Kbypass-r @ np.linalg.solve(M,r)
    if force is not None:
        Delta=force/Keq
        u=Delta*np.linalg.solve(M,r)
    direct=(c*b-a*d)*Delta/((a+b)*(c+d)+k*(a+b+c+d))
    return dict(Delta=Delta,u_ref=u[0],u_test=u[1],gap=u[1]-u[0],exact_gap=direct,K=Keq,
                threshold=c*b/a)

def normal_cdf(x):return .5*(1.+erf(x/sqrt(2.)))

def sign_error(a=1.,b=1.,c=1.,k=.1,damaged=.5,healed=1.2,Delta=.2,noise=.005):
    gd=model(a,b,c,damaged,k,Delta=Delta)['gap']
    gh=model(a,b,c,healed,k,Delta=Delta)['gap']
    return dict(Delta=Delta,g_damage=gd,g_healed=gh,miss_damaged=normal_cdf(-gd/noise),
                false_activate=normal_cdf(gh/noise))

def grow(d0=.4,qhi=.05,qlo=.008,tau=3.,hi_cut=.7,stop=.98,dt=.005,T=200.,mode='two',load_schedule=None,drive_min=0.):
    # z = unincorporated scaffold measured in ultimate stiffness units; d is matured stiffness
    d,z=float(d0),0.; series=[]; q_used=0.; t=0.; t_stop=None
    steps=int(T/dt)
    for j in range(steps):
        if load_schedule is None: amp=.2
        else: amp=load_schedule(t)
        # Compare to two mechanically coded thresholds using separate comparator arms;
        # a=b=1, c=hi_cut or stop, so zero occurs at d=hi_cut or stop.
        # Valve only receives reliable comparator signal under tensile probe excitation.
        good=amp>=drive_min
        if mode=='two':
            u=qhi if good and d<hi_cut else (qlo if good and d<stop else 0.)
        elif mode=='one':u=qhi if good and d<1.0 else 0.
        elif mode=='open':u=qhi if t<9 else 0.
        else:raise ValueError(mode)
        if u==0 and t_stop is None and d>= (1. if mode=='one' else stop):t_stop=t
        # exact discrete update for stock within step and integrated maturation
        decay=np.exp(-dt/tau)
        new_z=z*decay + u*tau*(1-decay)
        dd=z*(1-decay) + u*(dt-tau*(1-decay))
        d+=dd
        z=new_z
        q_used+=u*dt
        t+=dt
        if j % max(1,int(1.0/dt))==0:series.append((t,d,z,u))
        if t>100 and z<1.e-10 and u==0:break
    return dict(d0=d0,dfinal=d,stock=z,time=t,reactant=q_used,overshoot=d-stop,stop_time=t_stop,trace=series)

# Equilibrium fractional drift of reference and test-top stiffness shifts actual threshold.
def drift_thresholds(eps):
    return ((1-eps)**2/(1+eps), (1+eps)**2/(1-eps))

if __name__=='__main__':
    rng=np.random.default_rng(20261026)
    worst=0
    for _ in range(10000):
        a,b,c,d=rng.uniform(.2,3,4); k=rng.uniform(0,2)
        Delta=rng.uniform(.01,2)
        x=model(a,b,c,d,k,Delta=Delta)
        y=model(a,b,c,d,k,force=x['K']*Delta)
        worst=max(worst,abs(x['gap']-x['exact_gap']),abs(y['gap']-x['gap']))
        assert np.sign(x['gap'])==np.sign(c*b-a*d)
    print('mechanical bridge identity maximum residual',worst)
    for v in [.05,.1,.2,.5]:print('sensor noise',sign_error(Delta=v))
    for mode in ['one','two']:
        for d0 in [.4,.55,.7]:
            z=grow(d0=d0,mode=mode)
            print('growth',mode,d0,{k:round(v,5) if isinstance(v,float) else v for k,v in z.items() if k!='trace'})
    for e in [.01,.02,.05]:print('threshold with independent fractional drift',e,drift_thresholds(e))

# --- Further test: actual three-branch comparator and a physically motivated valve ---
from scipy.optimize import root

def dual_gaps(d, b1=.7,b2=.98, k1=.06,k2=.06,Delta=.2,a1=1.,a2=1.,c=1.):
    """A single growing test arm d observed by TWO finite-stiffness bridge comparators."""
    A=np.array([[a1+b1+k1,0.,-k1],
                [0.,a2+b2+k2,-k2],
                [-k1,-k2,c+d+k1+k2]])
    R=np.array([a1,a2,c])*Delta
    u=np.linalg.solve(A,R)
    return np.array([u[2]-u[0],u[2]-u[1]])


def fast_dual_gaps(d,b1=.7,b2=.98,k1=.06,k2=.06,Delta=.2,a1=1.,a2=1.,c=1.):
    A1=a1+b1+k1;A2=a2+b2+k2
    U=Delta*(c+k1*a1/A1+k2*a2/A2)/(c+d+k1+k2-k1*k1/A1-k2*k2/A2)
    return np.array([((a1+b1)*U-a1*Delta)/A1,((a2+b2)*U-a2*Delta)/A2])

def calibrate_dual(hi=.7,stop=.98,k1=.06,k2=.06):
    """Calibrate both mechanical reference ratios together; sensor probes interfere."""
    def residual(b):
        return [dual_gaps(hi,*b,k1,k2)[0], dual_gaps(stop,*b,k1,k2)[1]]
    sol=root(residual,[hi,stop],tol=1e-12)
    assert sol.success and np.max(np.abs(residual(sol.x)))<1e-10
    return tuple(sol.x)


def simulate_physical_growth(d0=.4,hi=.7,stop=.98,k=.06,
                             q_hi=.05,q_lo=.008,tau=3.,dt=.05,T=120,
                             eta=1.,growth_mode='snap',
                             load=None,minimum_signal=0.,reactant_budget=np.inf,
                             noise=0.,rng=None):
    """Gating determined only by physically modelled midpoint positions; d evolves
       from accumulated extracellular precursors z. External strain is NOT used to
       compute d. When load is zero, comparator has no information.
       See test scenarios below. No biology calibrated.
    """
    if rng is None:rng=np.random.default_rng(1)
    b1,b2=calibrate_dual(hi,stop,k,k)
    d,z,spent=float(d0),0.,0.
    trace=[];first_cut=None
    original_gap=dual_gaps(d0,b1,b2,k,k,Delta=.2)[1]
    for j in range(int(T/dt)):
        t=j*dt
        delta=.2 if load is None else load(t)
        hgap,fgap=fast_dual_gaps(d,b1,b2,k,k,Delta=delta)
        if noise:
            hgap+=rng.normal(0,noise);fgap+=rng.normal(0,noise)
        if growth_mode=='snap':
            if delta>0 and abs(delta)>minimum_signal:
                q=q_hi if hgap>0 else (q_lo if fgap>0 else 0.)
            else:q=0.
        elif growth_mode=='slit':
            # Poiseuille-like flow scales as third power of slit opening.
            # growth drops below maintenance at q<0.01*q_hi, setting q=0.
            g=max(0.,fgap)
            q=q_hi*min(1.,(g/max(original_gap,1e-12))**3)
            if q<.01*q_hi:q=0.
        else:raise ValueError(growth_mode)
        q=min(q,max(0.,reactant_budget-spent)/dt)
        E=np.exp(-dt/tau)
        # If eta<1, some synthesized precursor creates no useful stiffness;
        # stock z is measured in nutrient units, matured stiffness is eta*z/tau.
        dd=eta*(z*(1-E)+q*(dt-tau*(1-E)))
        z=z*E+q*tau*(1-E)
        d+=dd;spent+=q*dt
        if j%max(1,int(1/dt))==0:trace.append((t,d,z,spent,q,hgap,fgap))
    return dict(d0=d0,d=d,z=z,spent=spent,trace=trace,b1=b1,b2=b2)


def nonlinear_threshold(strain, c=1.,h=2.):
    """Reference a=b=1: u_ref=Delta/2. Test top is Hookean c;
       test bottom is d*u + h*u^3. At the neutral mechanical comparator,
       the probe spring is slack and force equality requires d=c-h*Delta^2/4.
    """
    return c-h*strain**2/4

if __name__=='__main__':
    b1,b2=calibrate_dual()
    print('two-probe calibrated reference lower stiffnesses',b1,b2)
    for d0 in [.4,.55,.7]:
        for mode in ['snap','slit']:
            out=simulate_physical_growth(d0=d0,growth_mode=mode)
            print('true mechanical valve', mode,d0, 'final',round(out['d'],6),
                  'materials',round(out['spent'],6), 'remaining stock',round(out['z'],7))
    for delta in [.1,.2,.4,.6]:
        print('nonlinear apparent threshold for h=2, Delta=',delta,nonlinear_threshold(delta))
    for eta in [1.,.7,.2,0.]:
        out=simulate_physical_growth(d0=.4,eta=eta,reactant_budget=1.)
        print('producer efficiency',eta,'d_final',round(out['d'],5),'material',round(out['spent'],5))

def stochastic_feedback(n=3000,seed=123,dt=.1,T=120,noise=.001,mode='continuous',
                        confirmations=8,drive=(.02,.30),start=(.4,.7),
                        latch_cut=.99,qhi=.05,qlo=.008,tau=3.,budget=np.inf,
                        miscalibrate=0.):
    """Vectorized population of independent damaged regions. Decision noise is
       ideal Gaussian midpoint-offset noise, not measured physical thermal noise.
       'continuous' keeps watching forever; 'latch' ceases feed after N successive
       decisions that indicate sufficient stiffness (physical latch hypothetical).
       All times/rates illustrative.
    """
    rng=np.random.default_rng(seed)
    d=rng.uniform(start[0],start[1],n)
    z=np.zeros(n);spent=np.zeros(n);sealed=np.zeros(n,dtype=bool)
    streak=np.zeros(n,dtype=int)
    b1,b2=calibrate_dual(.7,latch_cut)
    b1*=1+miscalibrate;b2*=1+miscalibrate
    E=np.exp(-dt/tau)
    for j in range(round(T/dt)):
        D=rng.uniform(drive[0],drive[1],n)
        A1=1.+b1+.06;A2=1.+b2+.06
        ut=D*(1+.06/A1+.06/A2)/(1+d+.12-2*.06**2/A1 if abs(A1-A2)<1e-14 else
                      1+d+.12-.06**2/A1-.06**2/A2)
        g1=( (1+b1)*ut-D)/A1 + rng.normal(0,noise,n)
        g2=( (1+b2)*ut-D)/A2 + rng.normal(0,noise,n)
        if mode=='latch':
            streak=np.where((g2<0)&~sealed,streak+1,0)
            sealed |= streak>=confirmations
        q=np.where((g1>0)&(~sealed),qhi,np.where((g2>0)&(~sealed),qlo,0.))
        q=np.minimum(q,np.maximum(0,budget-spent)/dt)
        d+=z*(1-E)+q*(dt-tau*(1-E))
        z=z*E+q*tau*(1-E)
        spent+=q*dt
    return dict(n=n,seed=seed,noise=noise,mode=mode,mean=float(d.mean()),
                p95=float(np.quantile(d,.95)),p05=float(np.quantile(d,.05)),
                within_90_110=float(np.mean((d>=.9)&(d<=1.1))),
                within_95_110=float(np.mean((d>=.95)&(d<=1.1))),
                over_110=float(np.mean(d>1.1)),under_95=float(np.mean(d<.95)),
                material=float(spent.mean()),sealed=float(sealed.mean()),
                minimum=float(d.min()),maximum=float(d.max()))

if __name__=='__main__':
    for noise in [0.,.0005,.001,.003]:
        for mode in ['continuous','latch']:
            z=stochastic_feedback(n=2500,noise=noise,mode=mode,confirmations=8,seed=15)
            print('stochastic',noise,mode, {k:round(v,4) if isinstance(v,float) else v for k,v in z.items() if k not in ['n','seed','mode','noise']})

def nonlinear_sensor_gap(d,Delta=.2,h=2.,k=.1):
    """Identical Hookean tops c=1; reference Hookean a=b=1;
       repair-bottom hardens as d*u + h*u^3. Bridge probe spring k.
    """
    from scipy.optimize import root
    def f(z):
        ur,ut=z
        return [ (2+k)*ur-k*ut-Delta,
                 -k*ur+(1+d+k)*ut+h*ut**3-Delta]
    rr=root(f,[Delta/2,Delta/(1+d)],tol=1e-12)
    assert rr.success or np.max(np.abs(f(rr.x)))<1e-10
    return float(rr.x[1]-rr.x[0])

if __name__=='__main__':
    for Delta in [.1,.2,.4,.6]:
        dthr=nonlinear_threshold(Delta,h=2)
        print('nonlinear exact comparator root',Delta,dthr,nonlinear_sensor_gap(dthr,Delta,h=2),
              'd=.9 gap',nonlinear_sensor_gap(.9,Delta,h=2))

# --- Follow-on: a mechanically hysteretic, resettable feedback switch ---
def calibrate_array(thresholds=(.7,.88,.98),k=.03):
    """Calibrate interacting gauge beams simultaneously, rather than assuming
       each reference is mechanically independent of the others."""
    thresholds=np.array(thresholds,dtype=float)
    m=len(thresholds)
    def gs(d,b,Delta=1.):
        A=1+b+k
        U=Delta*(1+np.sum(k/A))/(1+d+m*k-np.sum(k*k/A))
        return ((1+b)*U-Delta)/A
    def fun(b):return [gs(thresholds[j],b)[j] for j in range(m)]
    opt=root(fun,thresholds,tol=1e-11)
    assert opt.success or np.linalg.norm(fun(opt.x))<1e-9
    return opt.x


def run_multi_repair(n=3000,noise=.003,seed=102,dt=.1,T=240.,
                     events=((100.,.35),(185.,.12)),
                     reset=.88,hi=.7,stop=.98,confirmation=6,
                     qhi=.05,qlo=.008,tau=3.,max_material=np.inf):
    """One passive geometrical comparator per threshold, a bistable completion
       memory (not implemented in biological chemistry), hypothetical repair
       material and explicit damage events. Tensile excitation required.
    """
    rng=np.random.default_rng(seed)
    b=calibrate_array((hi,reset,stop));k=.03;m=3
    A=1+b+k
    d=rng.uniform(.4,.7,n);z=np.zeros(n);spent=np.zeros(n)
    on=np.ones(n,dtype=bool);stop_streak=np.zeros(n,dtype=int);reset_streak=np.zeros(n,dtype=int)
    E=np.exp(-dt/tau);event_idx=0;snapshots=[]
    for jj in range(round(T/dt)):
        t=jj*dt
        if event_idx<len(events) and t>=events[event_idx][0]-dt/2:
            d=np.maximum(.02,d-events[event_idx][1]);on_damage=d.copy()
            snapshots.append(('after damage',round(t,2),float(d.mean()),float((d>=.95).mean())))
            event_idx+=1
        D=rng.uniform(.02,.3,n)
        U=D*(1+k*np.sum(1/A))/(1+d+m*k-np.sum(k*k/A))
        g=((1+b[:,None])*U[None,:]-D[None,:])/A[:,None]+rng.normal(0,noise,(m,n))
        # Reset if new structural damage below threshold is corroborated.
        reset_streak=np.where((~on)&(g[1]>0),reset_streak+1,0)
        on |= reset_streak>=confirmation
        # Stop if construction is sufficiently complete with corroboration.
        stop_streak=np.where(on&(g[2]<0),stop_streak+1,0)
        on &= stop_streak<confirmation
        q=np.where(on,np.where(g[0]>0,qhi,qlo),0.)
        q=np.minimum(q,np.maximum(0,max_material-spent)/dt)
        d+=z*(1-E)+q*(dt-tau*(1-E));z=z*E+q*tau*(1-E);spent+=q*dt
        if jj and jj%round(40/dt)==0:
            snapshots.append(('sample',round(t,1),float(d.mean()),float((d>=.95).mean())))
    return dict(mean=float(d.mean()),p05=float(np.quantile(d,.05)),p95=float(np.quantile(d,.95)),
                within=float(np.mean((d>=.95)&(d<=1.1))),
                material=float(spent.mean()),on=float(on.mean()),snapshots=snapshots,calibration=b)

if __name__=='__main__':
    b=calibrate_array()
    print('joint three-comparator calibration',b)
    for sd in [0.,.001,.003,.006]:
        r=run_multi_repair(n=2500,noise=sd)
        print('regenerative material hysteron',sd,dict(mean=round(r['mean'],4),p05=round(r['p05'],4),p95=round(r['p95'],4),
                                                      within=round(r['within'],4),material=round(r['material'],4),on=round(r['on'],4)))
        if sd==.003: print('snapshots',r['snapshots'])

def viscoelastic_repair(n=4000,seed=42,noise=.003,T=240,dt=.1,
                       events=((100.,.35),(185.,.12)),
                       reset=.94,hi=.7,stop=.98,
                       tau_sensor=3.,theta_on=.0002,theta_off=.0002,
                       qhi=.05,qlo=.008,tau_material=3.,initial=(.4,.7)):
    """A physically interpretable alternative to digital consecutive counts:
       first-order viscoelastic filtering of displacement, and a bistable
       on/off valve (hydrodynamic hysteron). Full integration not demonstrated.
    """
    rng=np.random.default_rng(seed);k=.03;m=3
    b=calibrate_array((hi,reset,stop),k=k);A=1+b+k
    d=rng.uniform(initial[0],initial[1],n);stock=np.zeros(n);used=np.zeros(n)
    on=np.ones(n,dtype=bool);filtered=np.zeros((m,n))
    rat=1-np.exp(-dt/tau_sensor);E=np.exp(-dt/tau_material)
    ev_idx=0;records=[]
    for j in range(round(T/dt)):
        t=j*dt
        if ev_idx<len(events) and t>=events[ev_idx][0]-dt/2:
            d=np.maximum(.02,d-events[ev_idx][1]);ev_idx+=1
            records.append(('injury',round(t,1),float(d.mean()),float(((d>=.95)&(d<=1.1)).mean())))
        D=rng.uniform(.02,.3,n)
        U=D*(1+k*np.sum(1/A))/(1+d+m*k-np.sum(k*k/A))
        g=((1+b[:,None])*U[None,:]-D[None,:])/A[:,None]+rng.normal(0,noise,(m,n))
        filtered += rat*(g-filtered)
        # physical bistable switch with separate reset/closure thresholds
        reopen=(~on)&(filtered[1]>theta_on)
        close=on&(filtered[2]<-theta_off)
        on=(on|reopen)&(~close)
        q=np.where(on,np.where(filtered[0]>0,qhi,qlo),0.)
        d+=stock*(1-E)+q*(dt-tau_material*(1-E))
        stock=stock*E+q*tau_material*(1-E)
        used+=q*dt
        if j and j%round(40/dt)==0:
            records.append(('sample',round(t,1),float(d.mean()),float(((d>=.95)&(d<=1.1)).mean())))
    good=((d>=.95)&(d<=1.1))
    return dict(mean=float(d.mean()),p05=float(np.quantile(d,.05)),p95=float(np.quantile(d,.95)),
                good=float(good.mean()),used=float(used.mean()),on=float(on.mean()),records=records,
                thresholds=tuple(b))

if __name__=='__main__':
    for tau in [.4,1.,2.,4.,8.]:
        s=viscoelastic_repair(n=2200,tau_sensor=tau,reset=.94,seed=44)
        print('viscoelastic lag',tau,'good',round(s['good'],4),'mean',round(s['mean'],4),
              'used',round(s['used'],4),'on',round(s['on'],4))
    s=viscoelastic_repair(n=2200,tau_sensor=2.,reset=.94,seed=44)
    print('viscoelastic snaps',s['records'])

# --- Last physical interface: nutrient delivery by a previously grown hyphal route ---
def passive_feed_through_cylinder(diameter=88e-6,length=1e-3,
                                  D_glucose=7.294e-10,glucose_gradient=10.,
                                  D_oxygen=2e-9,oxygen_gradient=.258,
                                  cellulose_yield=.2):
    """Optimistic steady Fick transport through an unobstructed water cylinder.
       Fungus-filled nanofluidic channel in cited primary research is NOT this
       ideal fluid cylinder; ions/conductivity do NOT establish metabolite flux.
       Concentrations mol/m^3, D in m^2/s, molecular masses in g/mol.
    """
    from math import pi
    A=pi*(diameter/2.)**2;sec=86400.
    glucose_ug=D_glucose*A*glucose_gradient/length*sec*180.16*1e6
    oxygen_ug=D_oxygen*A*oxygen_gradient/length*sec*32.*1e6
    cellulose_ug=glucose_ug*(162.14/180.16)*cellulose_yield
    return {'area_m2':A,'glucose_ug_per_day':glucose_ug,
            'oxygen_ug_per_day':oxygen_ug,
            'cellulose_ug_per_day_at_yield':cellulose_ug,
            'channels_for_5ug_per_day':5./cellulose_ug}

if __name__=='__main__':
    for y in [1.,.2]:print('ideal water filled channel',y,passive_feed_through_cylinder(cellulose_yield=y))

def two_role_indistinguishability():
    """Two mutually indistinguishable functional states require opposite first
       interventions. A scalar completed-function readout min(A,B) is insufficient.
       Equal priors, one unit of A or B resources.
    """
    worlds=((0,1),(1,0))
    out={}
    for action in ('A','B'):
        final=[]
        for A,B in worlds:
            if action=='A':A+=1
            else:B+=1
            final.append(min(A,B))
        out[action]=dict(initial_signal=[0,0],completed=final,success=sum(x>0 for x in final)/2)
    return out

if __name__=='__main__':
    print('two-role partial-information no-go',two_role_indistinguishability())

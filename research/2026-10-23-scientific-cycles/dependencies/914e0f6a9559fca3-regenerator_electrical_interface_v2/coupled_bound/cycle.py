"""Whole-operation favorable limit: FE, separate optical gates, isolation C.

There is no water selector. Optical holds, direct LC exchange with both
finite OFF ports, and finite-time controlled endpoint correction alternate.
Optical transitions are adiabatic zero-duration limits with ALL charge/work
counted. Stiff rails and reversible gate/catch processors are BOUNDS, not
assigned attainable efficiencies. Their measured loss must fit the joint
budget. Source FE is one integrable G; every reversible state resets.
"""
from pathlib import Path
import sys,json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq,root
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'material'))
sys.path.insert(0,str(HERE.parent/'isolation'))
sys.path.insert(0,str(HERE.parent)) # portable calculation package fallbacks
sys.path.insert(0,str(HERE.parents[1]/'radiation_valve15/regeneration/geometry_scan'))
import source_envelope as fe
import gate_stack as gate
from te_analytic_check import te_at_power,te_max_power
TH=348.;TC=338.;VH=23.;VL=.1
HH=2111.152;HO=168.69;CH=4813.078;CO=264.262
EXTRA=.545+gate.CMASS
L0=2.443004509e-8
SHAPE=0.
# All extensive quantities below are per area A of ONE bank. Half-cycle
# pair work/(2*A*half-duration) is power per combined2A area.
MU_ON=np.array([[gate.MUH,gate.MUH],[gate.MUL,gate.MUL]])
MU_OFF=np.array([[gate.MUL,gate.MUH],[gate.MUL,gate.MUH]])
MU_END=MU_ON[::-1].copy()

def fp(T,V):return fe.props(float(T),float(np.clip(V,0,23.27)),SHAPE,EXTRA)

def thermal(T,mode,support):
    h,c=(HH,CO) if mode=='hot' else ((HO,CH) if mode=='cold' else (HO,CO))
    return h*(TH-T),(c+support)*(TC-T)

def at_fixed_dv(T,V,mus,mdots,Vdot,q):
    p=fp(T,V);fs=[gate.face(m,T,V) for m in mus]
    A=p['CV']+sum(f['CVmu'] for f in fs)
    Tdot=(q-T*p['alpha']*Vdot-T*sum(f['enT']*dm for f,dm in zip(fs,mdots)))/A
    I=(p['alpha']-gate.CI*sum(f['Vg_T'] for f in fs))*Tdot+(p['C']+2*gate.CI)*Vdot-gate.CI*sum(f['Vg_mu']*dm for f,dm in zip(fs,mdots))
    flows=[gate.face_flow(m,T,V,Tdot,Vdot,dm) for m,dm in zip(mus,mdots)]
    return Tdot,I,flows

def energy(T,V,mus):
    p=fp(T,V);fs=[gate.face(m,T,V) for m in mus]
    qfe=p['Q']+sum(f['Qfe_iso'] for f in fs)
    G=p['G']+sum(f['G'] for f in fs);S=p['S']+sum(f['entropy'] for f in fs)
    qr=sum(-gate.CGAP*(m-gate.PHIR) for m in mus)
    return G+T*S+V*qfe+sum(f['Vg']*f['Qg'] for f in fs)+gate.PHIR*qr

# y=TA,TB,VA,VB,j, Qh,Qc, W_FE_out,W_gate_out,
#    FE_abs,gate_abs,J2dt,Joule,chargeFE_A,chargeFE_B,
#    gate_I2,FE_I2,catch_FE_abs
NN=20 #18:heat into floating electrical assembly,19:its actual T
def integrate(initial,duration,rhs,max_step):
    return solve_ivp(rhs,[0,duration],initial,rtol=2e-9,atol=2e-10,max_step=max_step,dense_output=True)

def half(Tinit,hold=.003,tau=.001,catch_s=30e-6,support=409.,Rarea=0.,r_arms=None,r_coil=0.,theta=341.5,Cnode=1e6,dense=False):
    y=np.zeros(NN);y[:5]=[*Tinit,VH,VL,0]
    y[19]=theta
    if r_arms is not None:Rarea=r_arms+r_coil
    initial_energy=sum(energy(y[k],y[k+2],MU_ON[k]) for k in range(2))
    records=[]
    def rhs_general(mode,mus,mudots,Vdots=None,exchange=False,adiabatic=False,catch=False):
      def rhs(t,y):
        dy=np.zeros(NN);gp=0.;fa=0.;ga=0.;gi2=0.;fi2=0.
        for k in range(2):
          T,V=y[k],y[k+2];mm=mus(t)[k] if callable(mus) else mus[k];dm=mudots(t)[k] if callable(mudots) else mudots[k]
          qh,qc=(0.,0.) if adiabatic else thermal(T,mode[k],support)
          wireheat=0.
          if r_arms is not None and not adiabatic:
            # Four equal normal-metal arms: each r_arms/4. Wiedemann-Franz
            # integration uses k proportional to T, not independent G.
            wireheat=4*L0/r_arms*(y[19]**2-T*T)
            dy[18]-=wireheat
            if exchange:wireheat+=.25*r_arms*y[4]**2
          q=qh+qc+wireheat
          if exchange:
            I=(-1 if k==0 else 1)*y[4]
            Td,Vd,flows=gate.coupled_derivatives(T,V,mm,dm,I,q,fp(T,V))
          else:
            Vd=Vdots[k];Td,I,flows=at_fixed_dv(T,V,mm,dm,Vd,q)
          dy[k]=Td;dy[k+2]=Vd;dy[5]+=qh;dy[6]+=qc
          dy[7]-=V*I;dy[13+k]=I
          for f in flows:
            pp=f['gate_power']+f['reservoir_power'];gp-=pp;ga+=abs(pp);gi2+=f['Ig']**2
          fa+=abs(V*I);fi2+=I*I
        dy[8]=gp;dy[9]=fa;dy[10]=ga;dy[15]=gi2;dy[16]=fi2
        if catch:dy[17]=fa
        if exchange:
          LA=1.19709e-4*(tau/.01)**2
          dy[4]=(y[2]-y[3]-Rarea*y[4])/LA
          dy[11]=y[4]**2;dy[12]=Rarea*y[4]**2
          if r_arms is not None:dy[18]+=(.5*r_arms+r_coil)*y[4]**2
        if r_arms is not None:dy[19]=dy[18]/Cnode
        return dy
      return rhs
    zero=np.zeros((2,2))
    def add(label,sol,mus,mudots,modes,physical_duration):
      nonlocal y
      records.append((label,sol,mus,mudots,modes,physical_duration));y=sol.y[:,-1].copy()
    r=rhs_general(['hot','cold'],MU_ON,zero,[0.,0.])
    add('thermal_hold',integrate(y,hold,r,hold/25),MU_ON,zero,['hot','cold'],hold)
    def gate_flip(label,start,end):
      # Integrate over a dimensionless switching coordinate: no independent
      # finite-time heat law is fabricated for uncalculated intermediate mu.
      mus=lambda x:start+x*(end-start)
      md=lambda x:end-start
      rr=rhs_general(['off','off'],mus,md,[0.,0.],adiabatic=True)
      add(label,integrate(y,1.,rr,1/30),mus,md,['adiabatic_limit']*2,0.)
    gate_flip('gate_to_off',MU_ON,MU_OFF)
    rr=rhs_general(['off','off'],MU_OFF,zero,exchange=True)
    def stop(t,z):return z[4]
    stop.terminal=True;stop.direction=-1
    sol=solve_ivp(rr,[0,2*tau],y,rtol=2e-9,atol=2e-10,max_step=tau/100,events=stop,dense_output=True)
    if not len(sol.t_events[0]):raise ValueError('no zero-current endpoint')
    add('LC_exchange',sol,MU_OFF,zero,['off','off'],float(sol.t[-1]))
    endpoint=y[:5].copy();target=np.array([VL,VH]);vd=(target-y[2:4])/catch_s
    rr=rhs_general(['off','off'],MU_OFF,zero,vd,catch=True)
    add('endpoint_correction',integrate(y,catch_s,rr,catch_s/25),MU_OFF,zero,['off','off'],catch_s)
    gate_flip('gate_to_on',MU_OFF,MU_END)
    final_energy=sum(energy(y[k],y[k+2],MU_END[k]) for k in range(2))
    # During LC exchange terminal FE power supplies both magnetic energy and
    # resistor heating. Only its surplus AFTER Joule loss reaches the bus.
    W=y[7]+y[8]-y[12]
    # With a floating node all loop Joule heat stays inside the assembly.
    # Otherwise this favorable baseline dumps resistance heat at the sink.
    res=y[5]+y[6]-W-(y[12] if r_arms is None else y[18])-(final_energy-initial_energy)
    out=dict(Tnext=y[:2][::-1].tolist(),duration_s=hold+sol.t[-1]+catch_s,
       W_FE_terminal_out_J_m2=y[7],W_gate_out_J_m2=y[8],W_net_ideal_J_m2=W,
       hot_J_m2=y[5],cold_J_m2=y[6],FE_absolute_processed_J_m2=y[9],
       gate_absolute_processed_J_m2=y[10],J2dt=y[11],Joule_J_m2=y[12],
       charge_FE_A_C_m2=y[13],charge_FE_B_C_m2=y[14],gate_I2_coordinate=y[15],
       FE_I2_coordinate=y[16],catch_FE_absolute_J_m2=y[17],
       endpoint_before_correction=endpoint.tolist(),firstlaw_residual_J_m2=res,
       reversible_state_energy_change_J_m2=final_energy-initial_energy,
       floating_node_heat_J_m2=y[18],floating_node_T_end_K=y[19])
    if dense:out['_records']=records
    return out

def engine(**kw):
    pre_ts=None
    if kw.get('r_arms') is not None and 'theta' not in kw:
      def shoot(x):
        h=half(x[:2],**dict(kw,theta=x[2]))
        return [*(np.array(h['Tnext'])-x[:2]),h['floating_node_heat_J_m2']]
      rt=root(shoot,[342.75,340.02,341.41],tol=1e-8)
      if not rt.success or max(abs(np.array(shoot(rt.x))))>1e-6:raise ValueError('floating periodic shoot failed: '+rt.message)
      kw=dict(kw,theta=float(rt.x[2]));pre_ts=rt.x[:2]
    ts=np.array([343.,340.]) if pre_ts is None else pre_ts;err=1.
    for it in range(60 if pre_ts is None else 1):
      z=half(ts,**kw);n=np.array(z['Tnext']);err=max(abs(n-ts));ts=n
      if err<1e-8:break
    z=half(ts,dense=True,**kw);records=z.pop('_records');d=z['duration_s'];W=z['W_net_ideal_J_m2'];Q=z['hot_J_m2']
    P=W/(2*d);eta=W/Q;te=te_at_power(P);pmax=te_max_power()['Pmax_W_m2']
    def edge(loss):
      p=(W-loss)/(2*d)
      if p>pmax:return 1.
      inc=te_at_power(p)
      return (W-loss)/Q-inc['eta'] if inc else -1.
    allowance=brentq(edge,0,W*.999) if edge(0)>0 else 0.
    out=dict(scope=__doc__,parameters=kw,source_shape=SHAPE,extra_C_J_m2K=EXTRA,
      area_convention='EachbankareaA; reportedP=Whalf/(2A*half_duration)',
      period_s=2*d,initial_high_low_T=ts.tolist(),reset_error_K=err,
      power_ideal_W_m2=P,hot_W_m2=Q/(2*d),efficiency_ideal=eta,
      TE_same_power=te,TE_max=te_max_power(),
      joint_unallocated_loss_allowance_J_per_pair_half=allowance,halfcycle=z)
    return out,records

def export_voltage(records,path):
    # Material waveform is continuous in V through zero-time gate operations.
    # Save only physical-time segments; gate events have unchanged V.
    rows=[];now=0.
    for label,sol,mus,md,modes,duration in records:
      if duration==0:continue
      for tt in np.linspace(0,float(sol.t[-1]),161):
        if rows and abs(now+tt-rows[-1][0])<1e-12:continue
        y=sol.sol(tt);rows.append([now+tt,*y[:5]])
      now+=duration
    a=np.array(rows)
    # Second half exchanges bank labels; both V waveforms return exactly.
    second=a[1:].copy();second[:,0]+=now
    second[:,[1,2]]=second[:,[2,1]];second[:,[3,4]]=second[:,[4,3]];second[:,5]*=-1
    a=np.r_[a,second]
    np.savetxt(path,a,delimiter=',',comments='',header='time_s,TA_K,TB_K,VA_V,VB_V,j_A_m2')

if __name__=='__main__':
    z,records=engine();(HERE/'RESULTS.json').write_text(json.dumps(z,indent=2)+'\n')
    print(json.dumps(z,indent=2))
    export_voltage(records,HERE/'actual_voltage_path.csv')

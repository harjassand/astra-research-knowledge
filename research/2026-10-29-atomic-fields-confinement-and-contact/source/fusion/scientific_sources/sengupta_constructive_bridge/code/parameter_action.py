"""Fixed-iota, matched physical near-axis-volume, worst-well action tuning."""
from pathlib import Path
import sys,json,time
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'positive_current_operation/vendor'))
import numpy as np
from scipy.special import ellipk,ellipj
from scipy.optimize import brentq,minimize_scalar
from numpy.polynomial.legendre import leggauss
IOTA=1/np.sqrt(5);ALPHA=1e-4
nodes,weights=leggauss(128);zz=(nodes+1)*np.pi/4;ww=weights*np.pi/4

def params(sig):
 lm=brentq(lambda t:np.pi*ellipk(np.exp(t))/ellipk(1-np.exp(t))-sig,-35,-.01,xtol=1e-12)
 m=np.exp(lm);k=np.sqrt(m);K=ellipk(m);KP=ellipk(1-m);kap=2*KP/np.pi
 u=np.arccosh(1/(IOTA*np.cosh(sig)))
 return dict(sigma=float(sig),m=m,k=k,K=K,KP=KP,kappa=kap,u0=u,R=np.sinh(u),P=np.cosh(u))

def values(p,z,grad=False):
 sn,cn,dn,_=ellipj(p['kappa']*np.asarray(z),1-p['m']);D=p['P']**2-np.sin(2*z)**2
 A=1/dn+dn/p['k'];B=A/np.sqrt(D)
 T=1-(1-p['k'])*sn**2;hu=p['kappa']**2*(1-p['m'])*T/dn**2;hv=p['kappa']**2*(1-p['m'])*T/p['k']
 if not grad:return B,D,hu,hv
 dp=-(1-p['m'])*sn*cn;Az=p['kappa']*dp*(1/p['k']-1/dn**2);Dz=-4*np.sin(2*z)*np.cos(2*z)
 return (Az-A*Dz/(2*D))/np.sqrt(D)

def diagnostic(sig):
 p=params(sig);B,D,hu,hv=values(p,zz)
 length=4*np.sum(ww*np.sqrt(D));area_integral=4*np.sum(ww*p['P']*D/np.sqrt(hu*hv))
 q=ALPHA**2*length**3/(2*area_integral)
 xcap=np.arccos(1-q)/np.sqrt(1-p['m']);margin=p['u0']-2*xcap/p['kappa']
 roots=[0.,np.pi/4,np.pi/2];grid=np.linspace(1e-7,np.pi/2-1e-7,129);g=values(p,grid,True)
 for a,b,ga,gb in zip(grid[:-1],grid[1:],g[:-1],g[1:]):
  if ga*gb<0:
   rt=brentq(lambda t:values(p,t,True),a,b,xtol=1e-13)
   if all(abs(rt-v)>1e-7 for v in roots):roots.append(rt)
 roots=sorted(roots);mins=[];maxima=[]
 for rt in roots:
  ep=1e-4;sec=(values(p,rt+ep,True)-values(p,rt-ep,True))/(2*ep)
  if sec<0 and rt<np.pi/2-1e-7:maxima.append((rt,float(values(p,rt)[0])))
 for z in roots:
  if z>=np.pi/2-1e-7:continue
  eps=1e-4;second=(values(p,z+eps,True)-values(p,z-eps,True))/(2*eps)
  if second>1e-6:
   for j in range(4):
    phase=z+j*np.pi/2;bb,dd,hh,kk=values(p,phase)
    gu=-p['P']*p['R']/dd;gv=-p['R']*np.sin(2*phase)/dd
    norm=np.sqrt(gu*gu/hh+gv*gv/kk);S=np.sqrt(2)*norm
    du=np.sqrt(2)*gu/hh/norm;dv=np.sqrt(2)*gv/kk/norm
    left=max((mm for mm in [(zz+kk*np.pi/2,bm) for zz,bm in maxima for kk in [-1,0,1]] if mm[0]<z),key=lambda t:t[0])
    right=min((mm for mm in [(zz+kk*np.pi/2,bm) for zz,bm in maxima for kk in [-1,0,1]] if mm[0]>z),key=lambda t:t[0])
    barrier=(min(left[1],right[1])-float(bb))/float(bb)
    mins.append(dict(zeta=float(phase),B=float(bb),S=float(S),direction=[float(du),float(dv)],relative_barrier=barrier))
 guv=-p['P']*np.sin(2*zz);aa=2*p['P']**2/hu;cc=2*p['P']**2/hv;off=2*guv/np.sqrt(hu*hv)
 mid=(aa+cc)/2;rad=np.sqrt((aa-cc)**2/4+off**2);elong=np.sqrt((mid+rad)/(mid-rad))
 out={k:float(v) for k,v in p.items()};out.update(axis_length=float(length),near_axis_DeltaPsi=float(q),normalized_effective_minor_radius=ALPHA,complete_tube_margin_sufficient=float(margin),axis_minimum_count=len(mins),minimum_relative_barrier=min(v['relative_barrier'] for v in mins) if mins else 0,minima=mins,max_near_axis_elongation_diagnostic=float(elong.max()),normalized_axis_max_curvature=float(np.sqrt(p['R']**2+4)/p['R']**2*length))
 bar=out['minimum_relative_barrier'];out['isolated_well_isotropic_pitch_fraction_at_bottom']=float(np.sqrt(bar/(1+bar)))
 out['worst_linear_relative_half_action_variation_at1percent_depth']=max(v['S'] for v in mins)*np.sqrt(q)/.01 if mins else 1e9
 return out

if __name__=='__main__':
 start=time.time();ref=diagnostic(2*np.pi/5)
 def objective(sig):
  d=diagnostic(sig)
  return d['worst_linear_relative_half_action_variation_at1percent_depth'] if d['axis_minimum_count']==8 and d['complete_tube_margin_sufficient']>0 and d['minimum_relative_barrier']>=.02 else 1e3
 scan=[diagnostic(t) for t in np.linspace(.65,1.435,25)]
 valid=[v for v in scan if v['axis_minimum_count']==8 and v['complete_tube_margin_sufficient']>0 and v['minimum_relative_barrier']>=.02]
 best=min(valid,key=lambda v:v['worst_linear_relative_half_action_variation_at1percent_depth'])
 step=(1.435-.65)/24;opt=minimize_scalar(objective,bounds=(max(.65,best['sigma']-step),min(1.435,best['sigma']+step)),method='bounded',options={'xatol':1e-7})
 candidate=diagnostic(round(float(opt.x)-1e-6,6))
 assert candidate['axis_minimum_count']==8 and candidate['minimum_relative_barrier']>=.02
 matched=[v for v in scan+[ref] if v['axis_minimum_count']==8 and v['minimum_relative_barrier']>=ref['minimum_relative_barrier']-1e-10 and v['complete_tube_margin_sufficient']>0]
 matched_best=min(matched,key=lambda v:v['worst_linear_relative_half_action_variation_at1percent_depth'])
 out=dict(status='PASS',objective='Worst axis-well linear action half-spread at1% depth, matched physical near-axis V/Laxis³',iota_exact='1/sqrt5',alpha=ALPHA,reference=ref,candidate=candidate,reference_barrier_matched_control=matched_best,scan=[{k:v for k,v in d.items() if k!='minima'} for d in scan],seconds=time.time()-start,limits=['Near-axis volume matching, not finite-radius volume certificate.','No original four tube crossings removed or claimed repaired.','Every located minimum retained; no rigorous global critical-point enumeration.','Elongation and normalized curvature are reported costs, not engineering qualifications.'])
 Path('results/parameter_action.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='scan'},indent=2))

"""Read-only extraction of original model forcing, not a new gas trajectory."""
import os,sys,json,hashlib,time,resource
from pathlib import Path
import numpy as np
start=time.monotonic();root=Path(__file__).resolve().parents[2];os.environ['CELLS']='24';os.environ['HEATER_CELLS']='4'
sys.path.insert(0,str(root/'nitrogen_finite_cycle_20261021'));import reacting_heater_signed as m
p=root/'nitrogen_finite_cycle_20261021/heater_H4_signed_N24_T11_blow_10.npz';z=np.load(p)
# All non-end bed cells whose original solid AND gas stay in source table range.
TT=[];SS=[];HH=[];GG=[];area=6*(1-m.por)/m.dp
for t,s in zip(z['t'],z['state'].T):
 alpha=1-min(1,max(0,(t-10)/.02));d=m.evaluate(t,s,alpha,True);q,rho,U,r=m.props(s)
 G=.5*(abs(d['F'][:-1])+abs(d['F'][1:]));mu=r['viscosity'][m.ids];kg=r['conductivity'][m.ids];Pr=r['cp'][m.ids]*mu/kg
 h=(2+1.1*(G[m.ids]*m.dp/mu)**.6*Pr**(1/3))*kg/m.dp
 deriv=m.evaluate(t,s,alpha);other=m.CS*deriv[m.ngas:m.ngas+m.nsolid]*1000-area*h*(d['T'][m.ids]-d['Ts'])
 TT.append(d['T'][m.ids]);SS.append(d['Ts']);HH.append(h);GG.append(other/area)
T=np.array(TT);S=np.array(SS);h=np.array(HH);g=np.array(GG)
ids=np.flatnonzero((T.min(0)>=300)&(T.max(0)<=1700)&(S.min(0)>=300)&(S.max(0)<=1700));ids=ids[~np.isin(ids,[0,23,24,47])]
np.savez_compressed(Path(__file__).with_name('forcing.npz'),t=z['t']-z['t'][0],Tg=T[:,ids],Ts=S[:,ids],h=h[:,ids],g_other=g[:,ids],ids=ids,R=m.dp/2,cv=m.CS/(1-m.por))
out={'source':str(p.relative_to(root)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'model_sha256':hashlib.sha256((root/'nitrogen_finite_cycle_20261021/reacting_heater_signed.py').read_bytes()).hexdigest(),'selected_ids':ids.tolist(),'selection':'All non-end cells with original Tg and Ts in 300..1700K throughout saved one blow','scope':'Frozen gas film and frozen net interparticle heat flux applied at grain surface. No gas/neighbor feedback or periodic grain history; uniform initial grains are an explicit diagnostic assumption. cv is inherited assumed material capacity, not measurement. Table conductivity is Robold material input, not new measured property.','wall_s':time.monotonic()-start,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
Path(__file__).with_name('forcing_receipt.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))

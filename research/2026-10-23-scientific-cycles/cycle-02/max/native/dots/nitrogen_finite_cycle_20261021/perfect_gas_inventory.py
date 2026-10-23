"""Conservative fixed-volume gas/solid pressure-relaxation prototype.
Calorically perfect NONREACTING gas: no nitrogen-fixation prediction.
Darcy/Ergun quasi-static momentum; imposed fixed-temperature central heater.
Tests finite inventory, reverse flow, energy bookkeeping and valve switching.
"""
import numpy as np,json,time,resource,os
from pathlib import Path
from scipy.integrate import solve_ivp
from scipy.sparse import lil_matrix
R=Path(__file__).resolve().parent;N=int(os.environ.get('CELLS','12'));M=2*N+1;H=N
L=.1;dx=L/N;por=.4;dp=.009525;Rg=288.;cp=1230.;cv=cp-Rg;P0=101325.;TH=2700.;T0=300.;VH=.1
MU=6e-5;KG=.1;CS=2.5e6;KR=1.4161997074001969e-9*.2;sig=5.670374419e-8
vol=np.full(M,por*dx);vol[H]=VH;ids=np.r_[np.arange(N),np.arange(N+1,M)]
A=150*(1-por)**2/(por**3*dp**2);B=1.75*(1-por)/(por**3*dp)
dist=np.full(M+1,dx);dist[[0,N,N+1,M]]=dx/2
ledger_names=['heater_J_m2','boundary_enthalpy_J_m2','radiation_J_m2','boundary_mass_kg_m2']
def flux(dP,rho,d):
 a=A*MU/rho;b=B/rho;v=abs(dP)/d
 return np.sign(dP)*2*v/(a+np.sqrt(a*a+4*b*v))

def evaluate(t,s,alpha,with_details=False):
 rho=np.maximum(s[:M],1e-7);U=s[M:2*M];T=np.maximum(100,U/(rho*cv));T[H]=TH;Ts=np.maximum(100,s[2*M:2*M+2*N]);P=rho*Rg*T
 F=np.zeros(M+1);E=np.zeros(M+1)
 F[1:M]=flux(P[:-1]-P[1:],.5*(rho[:-1]+rho[1:]),dist[1:M]);E[1:M]=F[1:M]*cp*np.where(F[1:M]>=0,T[:-1],T[1:])
 gl=flux(P0-P[0],.5*(P0/(Rg*T0)+rho[0]),dist[0]);gr=flux(P[-1]-P0,.5*(P0/(Rg*T0)+rho[-1]),dist[-1])
 F[0]=(1-alpha)+alpha*gl;F[-1]=(1-alpha)*gr-alpha
 E[0]=(1-alpha)*cp*T0+alpha*gl*cp*(T0 if gl>=0 else T[0]);E[-1]=(1-alpha)*gr*cp*(T[-1] if gr>=0 else T0)-alpha*cp*T0
 dr=(F[:-1]-F[1:])/vol;dU=(E[:-1]-E[1:])/vol
 Gmid=.5*(abs(F[:-1])+abs(F[1:]));Nu=2+1.1*(Gmid[ids]*dp/MU)**.6*(cp*MU/KG)**(1/3);Uv=Nu*KG/dp*6*(1-por)/dp
 Q=Uv*(Ts-T[ids]);dU[ids]+=Q/por
 q=np.zeros(2*N+2);left=Ts[:N];right=Ts[N:]
 q[1:N]=-KR/4*(left[1:]**4-left[:-1]**4)/dx;q[0]=-sig*(left[0]**4-T0**4);q[N]=0
 q[N+2:2*N+1]=-KR/4*(right[1:]**4-right[:-1]**4)/dx;q[N+1]=0;q[-1]=sig*(right[-1]**4-T0**4)
 div=np.r_[np.diff(q[:N+1]),np.diff(q[N+1:])]/dx;dTs=(-Q-div)/CS
 heater=VH*cv*TH*dr[H]-(E[H]-E[H+1]);dU[H]=cv*TH*dr[H]
 out=np.r_[dr,dU,dTs,heater,E[0]-E[-1],q[-1]-q[0],F[0]-F[-1]]
 if with_details:return {'P':P,'T':T,'Ts':Ts,'F':F,'heater':heater,'instant_energy_ledger':float(np.dot(vol,dU)+CS*dx*dTs.sum()-heater-(E[0]-E[-1])+(q[-1]-q[0]))}
 return out

def initial():
 z=np.load(R.parent/'nitrogen_regenerator_20261021/radiating_2700_checkpoint.npz');xx=(np.arange(N)+.5)*dx;y=np.array([np.interp(xx,z['x'],v) for v in z['y']]);T=np.r_[y[11,::-1]*1000,TH,y[5]*1000];Ts=np.r_[y[12,::-1],y[12]]*1000;P=np.linspace(P0+2200,P0, M);rho=P/(Rg*T);return np.r_[rho,rho*cv*T,Ts,np.zeros(4)]

def sparsity():
 n=2*M+2*N+4;J=lil_matrix((n,n))
 for i in range(M):
  for j in range(max(0,i-1),min(M,i+2)):
   for a in [i,M+i]:J[a,j]=J[a,M+j]=1
  if i!=H:
   k=i if i<H else i-1
   for a in [i,M+i]:J[a,2*M+k]=1
 for k,i in enumerate(ids):
  row=2*M+k
  for j in range(max(0,i-1),min(M,i+2)):J[row,j]=J[row,M+j]=1
  for j in range(max(0,k-1),min(2*N,k+2)):J[row,2*M+j]=1
 J[-4:,:]=1
 return J.tocsr()

def main():
 t=time.monotonic();s=initial();s0=s.copy();records=[];elapsed=0.;duration=float(os.environ.get('DURATION','2'));dt=.02
 # Fixed one second blows with20ms smooth reversal; both valve components accounted.
 while elapsed<duration-1e-12:
  phase=int(round(elapsed));target=phase%2;startalpha=target if phase==0 else 1-target
  def alpha(u):return startalpha+(target-startalpha)*min(1,max(0,(u-elapsed)/dt))
  sol=solve_ivp(lambda u,v:evaluate(u,v,alpha(u)),[elapsed,min(duration,elapsed+1)],s,method='BDF',rtol=2e-6,atol=np.r_[np.full(M,1e-9),np.full(M,1e-2),np.full(2*N,1e-5),np.full(4,1e-4)],jac_sparsity=sparsity())
  s=sol.y[:,-1];elapsed=float(sol.t[-1]);d=evaluate(elapsed,s,target,True)
  rec={'t_s':elapsed,'success':sol.success,'message':sol.message,'steps':len(sol.t)-1,'nfev':sol.nfev,'nlu':sol.nlu,'pressure_range_Pa':[float(d['P'].min()),float(d['P'].max())],'T_range_K':[float(d['T'].min()),float(d['T'].max())],'Tsmax_K':float(d['Ts'].max()),'instant_energy_residual_W_m2':d['instant_energy_ledger'],'min_rho':float(s[:M].min())};records.append(rec);print(json.dumps(rec),flush=True)
  if not sol.success:break
 stored0=float(np.dot(vol,s0[M:2*M])+CS*dx*s0[2*M:2*M+2*N].sum());stored=float(np.dot(vol,s[M:2*M])+CS*dx*s[2*M:2*M+2*N].sum());led=s[-4:]
 result={'scope':__doc__,'N_per_bed':N,'completed_t_s':elapsed,'records':records,'ledger':dict(zip(ledger_names,map(float,led))),'energy_balance_residual_J_m2':stored-stored0-led[0]-led[1]+led[2],'mass_balance_residual_kg_m2':float(np.dot(vol,s[:M]-s0[:M])-led[3]),'wall_s':time.monotonic()-t,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'assumptions':{'solid_capacity_J_m3_K':CS,'gas_cp':cp,'gas_R':Rg,'heater_volume_m3_m2':VH,'switch_ramp_s':dt,'no_chemistry':True,'momentum':'quasi-static Ergun, not acoustic/inertial CFD','transport':'constant mu/k selected prototype values, not property-qualified model'}}
 (R/'perfect_gas_inventory_result.json').write_text(json.dumps(result,indent=2)+'\n');np.savez_compressed(R/'perfect_gas_inventory_checkpoint.npz',state=s,initial=s0,t=elapsed);print(json.dumps(result),flush=True)
if __name__=='__main__':main()

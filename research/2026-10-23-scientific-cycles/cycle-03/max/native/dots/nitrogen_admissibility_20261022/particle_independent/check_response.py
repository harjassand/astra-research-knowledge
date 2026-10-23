"""Independent shell-frequency and frozen-lumped checks, not a gas trajectory.
Uses full spherical volumes/areas instead of the normalized parent operator.
"""
from pathlib import Path
import json, os, sys, hashlib
import numpy as np
from scipy.linalg import solve_banded
from scipy.integrate import solve_ivp

P=Path(__file__).resolve().parent
ROOT=P.parents[1]
D=P.parent/'particle'
z=np.load(D/'forcing.npz'); t=z['t']; R=float(z['R']); cv=float(z['cv'])
KT=np.arange(300,1701,200); KV=np.array([2.04,1.97,1.90,1.84,1.79,1.74,1.68,1.62])
k=np.interp(z['Ts'].mean(0),KT,KV); h=z['h'].mean(0); omega=np.pi

def full_sphere_response(n,k,h):
    re=np.linspace(0.,R,n+1); rc=(re[:-1]+re[1:])/2
    V=4*np.pi/3*np.diff(re**3); area=4*np.pi*R**2
    G=4*np.pi*k*re[1:-1]**2/np.diff(rc)
    Gb=area/(1/h+(R-rc[-1])/k)
    diagonal=1j*omega*cv*V
    diagonal[:-1]+=G; diagonal[1:]+=G; diagonal[-1]+=Gb
    ab=np.zeros((3,n),complex); ab[0,1:]=-G; ab[1]=diagonal; ab[2,:-1]=-G
    b=np.zeros(n,complex); b[-1]=Gb
    theta=solve_banded((1,1),ab,b)
    Y=Gb/area*(1-theta[-1]); surface=theta[-1]+Y*(R-rc[-1])/k
    return Y,surface,theta@V/V.sum()

q=np.sqrt(1j*omega*cv/k)*R
Z=k/R*(q/np.tanh(q)-1)
Y=h*Z/(h+Z); S=h/(h+Z); M=3*Y/(1j*omega*cv*R)
Zl=1j*omega*cv*R/3; Yl=h*Zl/(h+Zl); Sl=h/(h+Zl)
convergence=[]
for n in [8,16,32,64,128,256]:
    got=np.array([full_sphere_response(n,ki,hi) for ki,hi in zip(k,h)])
    convergence.append({'n':n,'max_complex_relative_Y_error':float(max(abs(got[:,0]/Y-1))),
      'max_complex_relative_surface_error':float(max(abs(got[:,1]/S-1))),
      'max_complex_relative_mean_error':float(max(abs(got[:,2]/M-1))),
      'max_Y_phase_error_degrees':float(max(abs(np.angle(got[:,0]/Y)*180/np.pi)))})

# The parent uses arithmetic sample means on a highly nonuniform BDF time grid.
# Compare time means over the same one-blow history without changing the forcing.
timeavg=lambda a:np.trapezoid(a,t,axis=0)/(t[-1]-t[0])
kt=np.interp(timeavg(z['Ts']),KT,KV); ht=timeavg(z['h'])
qt=np.sqrt(1j*omega*cv/kt)*R; Zt=kt/R*(qt/np.tanh(qt)-1)
Yt=ht*Zt/(ht+Zt); Ylt=ht*Zl/(ht+Zl)

# Reconstruction control: all 18 grains remain lumped, but exactly the same
# piecewise-linear frozen histories are used. This isolates forcing interpolation
# from a genuine radial response, with no gas/neighbor re-solve.
def at(u):
    return [np.array([np.interp(u,t,a[:,j]) for j in range(a.shape[1])]) for a in [z['Tg'],z['h'],z['g_other']]]
def lumped_rhs(u,Ts):
    Tg,h,g=at(u);return 3*(h*(Tg-Ts)+g)/(cv*R)
lump=solve_ivp(lumped_rhs,(t[0],t[-1]),z['Ts'][0],method='DOP853',t_eval=t,rtol=1e-10,atol=1e-9,max_step=.002)
assert lump.success
rad=np.load(D/'radial_64.npz'); lumpT=lump.y.T
np.savez_compressed(P/'lumped_reconstruction_control.npz',t=t,ids=z['ids'],temperature=lumpT)
err=lumpT-z['Ts']; radial_delta=rad['mean']-lumpT
C=cv*R/3
ql=C*(lumpT[-1]-lumpT[0]); qr=rad['energy_J_m2_particle']

# Independently reproduce the original net bed-solid flux divergence directly
# from the original solid state, without borrowing evaluate()'s dTs expression.
source=ROOT/'nitrogen_finite_cycle_20261021/heater_H4_signed_N24_T11_blow_10.npz'
src=np.load(source); N=24; NH=4; MM=2*N+NH; ngas=7*MM
Ts_all=np.maximum(200,src['state'][ngas:ngas+2*N].T*1000)
dx=.1/N; por=.4; dp=.009525; area=6*(1-por)/dp
KR=1.4161997074001969e-9*.2; sig=5.670374419e-8
qs=np.zeros((len(t),2*N+2));left=Ts_all[:,:N];right=Ts_all[:,N:]
qs[:,1:N]=-KR/4*np.diff(left**4,axis=1)/dx;qs[:,0]=-sig*(left[:,0]**4-300**4)
qs[:,N+2:2*N+1]=-KR/4*np.diff(right**4,axis=1)/dx;qs[:,-1]=sig*(right[:,-1]**4-300**4)
div=np.concatenate([np.diff(qs[:,:N+1],axis=1),np.diff(qs[:,N+1:],axis=1)],axis=1)/dx
g_exact=-div[:,z['ids']]/area

ref32=np.load(D/'radial_32.npz');d=abs(rad['surface']-ref32['surface']);imax=np.unravel_index(d.argmax(),d.shape)
out={
 'scope':'Independent analytical/discrete frequency check plus one-second frozen-lumped reconstruction control, not coupled gas or periodic solve.',
 'inputs':{'forcing_sha256':hashlib.sha256((D/'forcing.npz').read_bytes()).hexdigest(),'R_m':R,'cv_J_m3_K':cv},
 'normalization':{'bed_surface_area_m2_per_m3':area,'grain_volume_to_area_m':R/3,'capacity_CS_over_a_J_m2_K':2.5e6/area,'capacity_cv_R_over_3_J_m2_K':cv*R/3,'max_g_source_difference_W_m2':float(max(abs(g_exact-z['g_other']).ravel()))},
 'frequency_grid_convergence':convergence,
 'harmonic_original_sample_mean':{'Bi_R': [float(min(h*R/k)),float(max(h*R/k))],'Bi_V_over_A':[float(min(h*R/(3*k))),float(max(h*R/(3*k)))],'heat_ratio':[float(min(abs(Y/Yl))),float(max(abs(Y/Yl)))],'phase_deg':[float(min(np.angle(Y/Yl)*180/np.pi)),float(max(np.angle(Y/Yl)*180/np.pi))],'surface_to_lumped_temperature_amplitude':[float(min(abs(S/Sl))),float(max(abs(S/Sl)))],'surface_to_mean_temperature_amplitude':[float(min(abs(S/M))),float(max(abs(S/M)))]},
 'sample_mean_bias':{'t_samples':len(t),'samples_at_t_le_0_02':int(sum(t<=.02)),'max_dt_s':float(max(np.diff(t))),'h_sample_mean_range':[float(min(h)),float(max(h))],'h_time_mean_range':[float(min(ht)),float(max(ht))],'max_relative_h_bias':float(max(abs(h/ht-1))),'harmonic_with_time_mean_heat_ratio':[float(min(abs(Yt/Ylt))),float(max(abs(Yt/Ylt)))],'harmonic_with_time_mean_phase_deg':[float(min(np.angle(Yt/Ylt)*180/np.pi)),float(max(np.angle(Yt/Ylt)*180/np.pi))]},
 'frozen_lumped_control':{'max_original_difference_K':float(max(abs(err).ravel())),'final_original_difference_K':err[-1].tolist(),'max_radial_mean_minus_control_K':float(max(abs(radial_delta).ravel())),'max_radial_mean_minus_original_K':float(max(abs(rad['mean']-z['Ts']).ravel())),'radial_over_lumped_net_heat_ratio_range':[float(min(qr/ql)),float(max(qr/ql))],'max_radial_minus_lumped_net_heat_abs_J_m2':float(max(abs(qr-ql)))},
 'initialization_and_refinement':{'max_surface_32_64_K':float(d[imax]),'max_location_time_s':float(t[imax[0]]),'max_location_solid_index':int(z['ids'][imax[1]]),'max_surface_32_64_at_t_ge_0_1_K':float(d[t>=.1].max()),'max_surface_32_64_at_final_K':float(d[-1].max()),'max_surface_minus_uniform_start_K':float(max(abs(rad['surface'][0]-z['Ts'][0]))),'max_surface_minus_mean_final_K':float(max(abs(rad['surface'][-1]-rad['mean'][-1])))}
}
(P/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

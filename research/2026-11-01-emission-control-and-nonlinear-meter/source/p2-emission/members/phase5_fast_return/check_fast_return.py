#!/usr/bin/env python3
"""Exact classical means and Gaussian covariance checkpoint for fast meter return.

No finite-Fock claim. Switching ramps and parasitic terms are not simulated.
Run: python phase5_fast_return/check_fast_return.py
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

root = Path(__file__).resolve().parent
g2, g3, gd, gu, alpha0, T = .125, .005, 10., .01, 4., 80.42477193
kappa = gd-gu
C = g3*kappa/(4*g2*g2)
base = np.sqrt(alpha0**2-C**2)
Astar = np.sqrt(alpha0**2-C**2/4)-.5j*C
Bstar = -g3*Astar.conjugate()/(2*g2)
D = np.diag([0.,0.,(gd+gu)/2,(gd+gu)/2])

def lin(c):
    return np.array([[c.real,-c.imag],[c.imag,c.real]])

def conj(c):
    return np.array([[c.real,c.imag],[c.imag,-c.real]])

def drift(A,B,offsum):
    M = np.zeros((4,4))
    M[:2,:2] = conj(-1j*(2*g2*B+offsum*g3*A.conjugate()))
    M[:2,2:] = lin(-2j*g2*A.conjugate())
    M[2:,:2] = lin(-2j*g2*A)
    M[2:,2:] = -.5*kappa*np.eye(2)
    return M

def rhs(t,y):
    A,B = y[0]+1j*y[1], y[2]+1j*y[3]
    dA = -2j*g2*A.conjugate()*B-1j*g3*A.conjugate()**2
    dB = -.5*kappa*B-1j*g2*(A*A-base*base)
    out = [dA.real,dA.imag,dB.real,dB.imag]
    for i,offsum in enumerate([2,-1]):
        start=4+32*i
        V=y[start:start+16].reshape(4,4)
        F=y[start+16:start+32].reshape(4,4)
        M=drift(A,B,offsum)
        out.extend((M@V+V@M.T+D).ravel())
        out.extend((M@F).ravel())
    return out

y0=[alpha0,0.,0.,0.]
for _ in range(2):
    y0.extend((.501*np.eye(4)).ravel())
    y0.extend(np.eye(4).ravel())
sol=solve_ivp(rhs,(0,T),y0,rtol=2e-10,atol=2e-12,dense_output=True)
assert sol.success
y=sol.y[:,-1]
A,B=y[0]+1j*y[1],y[2]+1j*y[3]
theta=-np.angle(A)
latency=.5  # declared example, not hardware measurement
detuning_bound=10.
buffer_drive_bound=2.
Bwait=B*np.exp(-kappa*latency/2)
tbuf=2/kappa*np.log1p(kappa*abs(Bwait)/(2*buffer_drive_bound))
tpulse=max(abs(theta)/detuning_bound,tbuf)
eps=-1j*kappa*Bwait/(2*np.expm1(kappa*tpulse/2))
Bend=Bwait*np.exp(-kappa*tpulse/2)-1j*eps*(1-np.exp(-kappa*tpulse/2))/(kappa/2)
Aend=A*np.exp(1j*theta)
R=np.eye(4); R[:2,:2]=lin(np.exp(1j*theta))
Freset=np.diag([1.,1.,np.exp(-kappa*(latency+tpulse)/2),np.exp(-kappa*(latency+tpulse)/2)])
Veqbuf=(gd+gu)/(2*kappa)
Qreset=np.diag([0.,0.,Veqbuf*(1-np.exp(-kappa*(latency+tpulse))),Veqbuf*(1-np.exp(-kappa*(latency+tpulse)))])
rows=[]
for i,kind in enumerate(['collective','difference_each_of_two']):
    start=4+32*i
    V=y[start:start+16].reshape(4,4)
    Fsense=y[start+16:start+32].reshape(4,4)
    Vend=R@(Freset@V@Freset.T+Qreset)@R.T
    Fcycle=R@Freset@Fsense
    rows.append({'mode':kind,'sensing_covariance':V.tolist(),'returned_covariance':Vend.tolist(),
      'returned_covariance_eigenvalues':np.linalg.eigvalsh(Vend).tolist(),
      'storage_gauge_occupation':float((np.trace(Vend[:2,:2])-1)/2),
      'buffer_fluctuation_occupation':float((np.trace(Vend[2:,2:])-1)/2),
      'cycle_mean_map_spectral_norm':float(np.linalg.norm(Fcycle,2)),
      'cycle_covariance_difference_contraction':float(np.linalg.norm(Fcycle,2)**2)})
Vmax=max(max(r['returned_covariance_eigenvalues']) for r in rows)
Vmin=min(min(r['returned_covariance_eigenvalues']) for r in rows)
k2=4*g2*g2/gd
k1=1e-4*k2
exposure=3*alpha0**2*(T+latency+tpulse)
old=3*alpha0**2*(T+60)
wrongA=A*np.exp(-1j*theta)
wrongBpre=-B.conjugate()*np.exp(-kappa*latency/2)
wrongeps=-1j*kappa*wrongBpre/(2*np.expm1(kappa*tpulse/2))
wrongB=Bwait*np.exp(-kappa*tpulse/2)-1j*wrongeps*(1-np.exp(-kappa*tpulse/2))/(kappa/2)
report={'parameters':{'g2':g2,'g3':g3,'gamma_down':gd,'gamma_up':gu,'net_damping':kappa,
  'stored_alpha':alpha0,'drive_alpha_base':float(base),'C':float(C),'sense_time':T},
 'classical':{'steady_A':[Astar.real,Astar.imag],'steady_B':[Bstar.real,Bstar.imag],
  'actual_A_at_stop':[A.real,A.imag],'actual_B_at_stop':[B.real,B.imag],
  'latency':latency,'rotation_angle':float(theta),'rotation_detuning_bound':detuning_bound,
  'drive_bound':buffer_drive_bound,'minimum_buffer_pulse':float(tbuf),'chosen_pulse':float(tpulse),
  'actual_buffer_drive_magnitude':float(abs(eps)),'buffer_mean_residual':float(abs(Bend)),
  'storage_radius_residual':float(abs(Aend-alpha0)),'total_fast_return':float(latency+tpulse),
  'wrong_record_storage_displacement_per_cat':float(abs(wrongA-alpha0)),
  'wrong_record_buffer_displacement_per_buffer':float(abs(wrongB)),
  'one_percent_rotation_area_error_displacement_per_cat':float(abs(Aend*(np.exp(1j*.01*theta)-1)))},
 'gaussian_modes':rows,'retained_covariance_min_eigenvalue':float(Vmin),
 'retained_covariance_max_eigenvalue':float(Vmax),
 'exposure':{'fast_total_photon_time_approx':float(exposure),'passive_total_photon_time_approx':float(old),
  'fast_single_photon_loss_probability_approx':float(1-np.exp(-k1*exposure)),
  'passive_single_photon_loss_probability_approx':float(1-np.exp(-k1*old))},
 'limitations':['Piecewise ideal switching; actual ramp waveforms and their disturbance not simulated.',
  'Gaussian Hessian only; no full cubic finite-Fock certificate.',
  'Final parity misassignment is a fault/outlier branch, not assumed corrected.',
  'No parasitic-control terms, detector likelihood, or readout-time optimization recomputed.',
  'Example feedforward latency .5/G is declared, not a verified hardware capability.',
  'Cycle contraction refers to the same calibrated native sensing trajectory and its Gaussian modes.']}
(root/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['classical','retained_covariance_min_eigenvalue','retained_covariance_max_eigenvalue','exposure']},indent=2))
print('Gaussian cycle contractions:',[r['cycle_covariance_difference_contraction'] for r in rows])

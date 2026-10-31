"""Actual three-cat/readout-buffer linear response and CD group modulation.

Uses the microscopic linearization of arXiv:2605.24262 Eq. (5),(7)-(10),
including its parity-dependent parametric terms. Not a full nonlinear device.
"""
from pathlib import Path
import json
import numpy as np


def transfer_real_force(s, G, gamma, delta):
    D=s*(s+gamma/2)+G*G
    return -G*(D+1j*delta*(s+gamma/2))/(D*D-delta*delta*(s+gamma/2)**2)


def matrix_transfer(s, G, gamma, delta):
    # Variables (c,c_dagger,b,b_dagger), source to c is -i F and to c† +i F.
    M=np.array([[0,-1j*delta,-1j*G,0],
                [1j*delta,0,0,1j*G],
                [-1j*G,0,-gamma/2,0],
                [0,1j*G,0,-gamma/2]], dtype=complex)
    src=np.array([-1j,1j,0,0])
    return np.linalg.solve(s*np.eye(4)-M,src)[2]


def modulated_power(f, G, gamma, delta, cycle):
    # H_R=epsilon (exp(-i theta_R) A_R + h.c.). Force on c is proportional
    # to f=exp(+i theta_R); c† receives f*. Keep both, not a scalar filter.
    nf=len(f)
    fw=np.fft.fft(f)/nf
    fcw=np.fft.fft(f.conj())/nf
    w=2*np.pi*np.fft.fftfreq(nf,d=cycle/nf)
    s=1j*w
    D=s*(s+gamma/2)+G*G
    bw=-G*(D*fw+1j*delta*(s+gamma/2)*fcw)/(D*D-delta**2*(s+gamma/2)**2)
    return float(np.sum(abs(bw)**2))


def main():
    G,gamma,n,nu=1.0,10.0,8.0,0.2
    kconf=2*G*G/gamma
    h=nu*G*G/gamma
    common_delta,dark_delta=2*h,-h
    max_res=0.0
    for delta in (0,common_delta,dark_delta,-common_delta):
        for omega in (0,.01,.2,1,3,10,100):
            max_res=max(max_res,abs(transfer_real_force(1j*omega,G,gamma,delta)-
                                    matrix_transfer(1j*omega,G,gamma,delta)))
    base={"n":n,"G":G,"gamma":gamma,"nu":nu,"confinement_amplitude_rate":kconf,
          "analytic_vs_matrix_transfer_residual":float(max_res)}
    freq=[]
    for ratio in (.05,.2,1,3,10,30,100):
        w=ratio*kconf
        freq.append({"omega_over_confinement":ratio,
                     "nu_zero_power_ratio":float(G**4/((G**2-w*w)**2+(gamma*w/2)**2)),
                     "common_mode_power_ratio_real_cosine":float(
                         (abs(transfer_real_force(1j*w,G,gamma,common_delta))**2+
                          abs(transfer_real_force(-1j*w,G,gamma,common_delta))**2)/
                         (2*abs(transfer_real_force(0,G,gamma,common_delta))**2))})
    # Eulerian circuit on G={I,X1X2,X1X3,X2X3}. Every vertex sees each
    # generator once. Each A rotates (1,2) by (+pi,-pi), B rotates (1,3).
    labels=["A","B","A","B","B","A","B","A"]
    samples_per_segment=1024
    step=np.arange(len(labels)*samples_per_segment)/samples_per_segment
    segment=step.astype(int)
    progress=step-segment
    theta=np.zeros((len(step),3))
    accum=np.zeros(3)
    for j,l in enumerate(labels):
        direction=np.array([1.,-1.,0.]) if l=="A" else np.array([1.,0.,-1.])
        mask=segment==j
        theta[mask]=accum+progress[mask,None]*np.pi*direction
        accum+=np.pi*direction
    modulation=[]
    for d_ratio in (.5,2,10,50,200):
        detuning=d_ratio*kconf
        cycle=8*np.pi/detuning
        cases={}
        for subset in ((0,),(1,),(2,),(0,1),(0,2),(1,2)):
            r=len(subset)
            f=np.exp(1j*np.sum(theta[:,subset],axis=1))
            common_weight=r*r/3
            dark_weight=r-common_weight
            new=common_weight*modulated_power(f,G,gamma,common_delta,cycle)+\
                dark_weight*modulated_power(f,G,gamma,dark_delta,cycle)
            old=common_weight*abs(transfer_real_force(0,G,gamma,common_delta))**2+\
                dark_weight*abs(transfer_real_force(0,G,gamma,dark_delta))**2
            cases["".join(str(j+1) for j in subset)]={
                "average_modulation_abs":float(abs(np.mean(f))),
                "leaked_power_relative_to_unmodulated":float(new/old)}
        modulation.append({"CD_detuning_over_confinement":d_ratio,
                           "cycle_duration":cycle,"paired_rotations_per_cycle":8,
                           "single_cat_rotations_per_cycle":16,
                           "cases":cases})
    balanced_labels=labels+labels[::-1]
    balanced_signs=[1.]*8+[-1.]*8
    balanced_step=np.arange(16*samples_per_segment)/samples_per_segment
    balanced_theta=np.zeros((len(balanced_step),3))
    accum=np.zeros(3)
    for j,(l,sign) in enumerate(zip(balanced_labels,balanced_signs)):
        direction=sign*(np.array([1.,-1.,0.]) if l=="A" else np.array([1.,0.,-1.]))
        mask=balanced_step.astype(int)==j
        progress=balanced_step[mask]-j
        balanced_theta[mask]=accum+progress[:,None]*np.pi*direction
        accum+=np.pi*direction
    balanced=[]
    for d_ratio in (10,50,200):
        cycle=16*np.pi/(d_ratio*kconf)
        cases={}
        for subset in ((0,),(1,),(2,),(0,1),(0,2),(1,2)):
            r=len(subset)
            f=np.exp(1j*np.sum(balanced_theta[:,subset],axis=1))
            wc,wd=r*r/3,r-r*r/3
            new=wc*modulated_power(f,G,gamma,common_delta,cycle)+wd*modulated_power(f,G,gamma,dark_delta,cycle)
            old=wc*abs(transfer_real_force(0,G,gamma,common_delta))**2+wd*abs(transfer_real_force(0,G,gamma,dark_delta))**2
            cases["".join(str(j+1) for j in subset)]={"average_modulation_abs":float(abs(np.mean(f))),
                "leaked_power_relative_to_unmodulated":float(new/old)}
        balanced.append({"CD_detuning_over_confinement":d_ratio,"cycle_duration":cycle,
                         "paired_rotations_per_cycle":16,"single_cat_rotations_per_cycle":32,
                         "cases":cases})
    out={"parameters":base,"single_frequency_response":freq,
         "Eulerian_counterrotation_modulation":modulation,
         "time_reverse_balanced_modulation":balanced,
         "underdamped_warning":{"gamma":0.5,"G":1.0,"omega":1.0,
                                  "power_ratio_at_omega":16.0},
         "limits":"Linearized model; ideal physical CD detunings and pump phase tracking. All rotation faults, finite pulse bandwidth and nonlinear cat leakage must be charged separately."}
    path=Path(__file__).with_name("actual_buffer_transfer_results.json")
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    main()

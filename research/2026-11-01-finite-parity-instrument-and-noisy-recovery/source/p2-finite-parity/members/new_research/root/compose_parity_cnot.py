"""Compose the exact finite-window parity instrument into a CNOT channel.

No parity bit is promoted to a projective oracle. The complete binned
homodyne Schur instrument, including residual cross-parity coherence,
internal losses and local phase corrections is used twice.

Circuit: a prepared |+>, measure Zc Za, measure Xa Xt, measure Za,
correct Zc**m2 Xt**(m1 xor m3). The output is on original c,t.
Physical basis changes and helper preparation/readout get explicit Pauli
noise. All prescribed error probabilities below are illustrative model
parameters, not claims about a physical device.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'finite_operation'))
from exact_cascade_parity import Model, solve, instrument_gram

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Z=np.diag([1,-1]).astype(complex)
Y=1j*X@Z
H=(X+Z)/np.sqrt(2)
PLUS=np.array([1,1],complex)/np.sqrt(2)
MINUS=Z@PLUS

def embed1(u,q):
    a=[I,I,I];a[q]=u
    return np.kron(np.kron(a[0],a[1]),a[2])

def evolve(rho,u): return u@rho@u.conj().T

def depol(rho,q,p):
    if p==0:return rho
    return (1-p)*rho+p/3*sum(evolve(rho,embed1(u,q)) for u in (X,Y,Z))

def schur2(rho,gram,q1,q2):
    ids=np.array([2*((i>>(2-q1))&1)+((i>>(2-q2))&1) for i in range(8)])
    return rho*gram[ids[:,None],ids[None,:]]

def prepare(rho,p):
    aux=(1-p)*np.outer(PLUS,PLUS.conj())+p*np.outer(MINUS,MINUS.conj())
    joint=np.zeros((8,8),complex)
    for c in range(2):
        for t in range(2):
            for cp in range(2):
                for tp in range(2):
                    for a in range(2):
                        for ap in range(2):
                            joint[4*c+2*a+t,4*cp+2*ap+tp]=rho[2*c+t,2*cp+tp]*aux[a,ap]
    return joint

def cnot_channel(rho,grams,prep=0.,read=0.,single=0.,phase=0., idle_dephase=0.):
    """Noise probabilities are per helper prep, final report, physical H or Z.

    'phase' models the two finite local phase-calibration operations;
    'idle_dephase' applies commuting local Z faults once per meter window.
    X/T1 faults *during* the meter are not reduced to this channel; their
    separate full-trajectory check and probability envelope are retained.
    """
    joint=prepare(rho,prep)
    out=np.zeros((4,4),complex)
    for m1 in range(2):
        r1=schur2(joint,grams[m1],0,1)
        r1=(1-phase)*r1+phase*evolve(r1,embed1(Z,0))
        for q in (0,1):r1=(1-idle_dephase)*r1+idle_dephase*evolve(r1,embed1(Z,q))
        for q in (1,2):r1=depol(evolve(r1,embed1(H,q)),q,single)
        for m2 in range(2):
            r2=schur2(r1,grams[m2],1,2)
            r2=(1-phase)*r2+phase*evolve(r2,embed1(Z,1))
            for q in (1,2):r2=(1-idle_dephase)*r2+idle_dephase*evolve(r2,embed1(Z,q))
            for q in (1,2):r2=depol(evolve(r2,embed1(H,q)),q,single)
            for actual in range(2):
                ids=[2*actual,2*actual+1,4+2*actual,5+2*actual]
                rr=r2[np.ix_(ids,ids)]
                for m3,prob in ((actual,1-read),(1-actual,read)):
                    cc=np.linalg.matrix_power(Z,m2)
                    tt=np.linalg.matrix_power(X,m1^m3)
                    corr=np.kron(cc,tt)
                    out+=prob*evolve(rr,corr)
    return out

CNOT=np.zeros((4,4),complex)
for c in range(2):
    for t in range(2):CNOT[2*c+(t^c),2*c+t]=1

def metrics(grams,**noise):
    # Normalized Choi is in (input,output) ordering.
    choi=np.zeros((16,16),complex)
    fe=0j
    trace_err=0.
    for i in range(4):
        for j in range(4):
            e=np.zeros((4,4),complex);e[i,j]=1
            out=cnot_channel(e,grams,**noise)
            choi[4*i:4*i+4,4*j:4*j+4]=out/4
            fe+=(CNOT.conj().T@out@CNOT)[i,j]/16
            trace_err=max(trace_err,abs(np.trace(out)-(1 if i==j else 0)))
    pure=CNOT.T.flatten()/2
    ideal=np.outer(pure,pure.conj())
    vals=np.linalg.eigvalsh((choi+choi.conj().T)/2)
    delta=np.linalg.eigvalsh(choi-ideal)
    dist=float(np.sum(abs(delta))/2)
    return dict(entanglement_infidelity=float(1-fe.real),
                average_gate_infidelity=float(4*(1-fe.real)/5),
                normalized_choi_trace_distance=dist,
                half_diamond_lower_from_choi=dist,
                half_diamond_upper_from_choi=min(1.,4*dist),
                min_choi_eigenvalue=float(vals.min()),
                trace_preservation_error=float(trace_err))

def main():
    ideal_grams=[]
    ss=np.array([1,-1,-1,1])
    for s in (1,-1):
        p=(ss==s).astype(float);ideal_grams.append(np.outer(p,p))
    result={'ideal_circuit_check':metrics(ideal_grams),'cases':[]}
    for loss in (0.,1e-5,1e-4,1e-3):
        m=Model(T=8,ke=1,kc=10,chi=5,eta=.5,assignment_error=1e-3,kb=loss,ki=10*loss)
        r,_,_=solve(m)
        grams=[instrument_gram(r,s) for s in (1,-1)]
        for name,noise in [
            ('meter_only',{}),
            ('helper_prep_and_read_0.001',{'prep':.001,'read':.001}),
            ('helper_and_each_H_0.001_and_phase_0.0001',{'prep':.001,'read':.001,'single':.001,'phase':.0001}),
            ('above_plus_commuting_Z_0.0001_per_meter_qubit',{'prep':.001,'read':.001,'single':.001,'phase':.0001,'idle_dephase':.0001})]:
            row={'loss_ratio_each':loss,'noise_model':name,'noise':noise,
                 'meter_assignment_error':r['assignment_error'],
                 'meter_same_sector_phase_flip_probability':r['same_sector_phase_flip_probability'],
                 **metrics(grams,**noise)}
            result['cases'].append(row)
            print(loss,name,row['entanglement_infidelity'])
    Path(__file__).with_name('cnot_composition_results.json').write_text(json.dumps(result,indent=2))
    print('ideal',result['ideal_circuit_check'])
    from finite_mediator_parity import Model as MediatorModel, solve as mediator_solve, instrument_gram as mediator_gram
    med={'ideal_circuit_check':result['ideal_circuit_check'],'cases':[]}
    for rate in (0.,1e-5,1e-4,1e-3):
        mm=MediatorModel(T=8,g=1,Gamma=4,chi=2,kb=rate,kc=rate)
        rr,_,_=mediator_solve(mm)
        grams=[mediator_gram(rr,s) for s in (1,-1)]
        for name,noise in [
            ('meter_only',{}),
            ('helper_prep_and_read_0.001',{'prep':.001,'read':.001}),
            ('helper_and_each_H_0.001_and_phase_0.0001',{'prep':.001,'read':.001,'single':.001,'phase':.0001}),
            ('above_plus_commuting_Z_0.0001_per_meter_qubit',{'prep':.001,'read':.001,'single':.001,'phase':.0001,'idle_dephase':.0001})]:
            row={'intrinsic_loss_rate_each_over_g':rate,'noise_model':name,'noise':noise,
                 'meter_assignment_error':rr['assignment_error'],'meter_same_sector_phase_flip_probability':rr['same_parity_pZ'],
                 **metrics(grams,**noise)}
            med['cases'].append(row)
            print('finite_mediator',rate,name,row['entanglement_infidelity'])
    med['thermal_initialization_envelope']=[{'nbar_each_of_six_modes':nb,
           'probability_outside_joint_vacuum':1-(1+nb)**-6,
           'half_diamond_additive_bound':1-(1+nb)**-6} for nb in (1e-5,1e-4,1e-3,.01)]
    med['scope']='Two complete meters; vacuum baths. Thermal initialization entry is a separate convex-mixture upper bound, not simulated finite-temperature gates. Noncommuting data faults during meters require full trajectories, or their total-probability bound; do not add their idealized postgate channels.'
    Path(__file__).with_name('finite_mediator_cnot_results.json').write_text(json.dumps(med,indent=2))

if __name__=='__main__':main()

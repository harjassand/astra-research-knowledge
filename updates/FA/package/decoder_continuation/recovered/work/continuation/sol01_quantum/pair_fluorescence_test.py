"""Substantively different transmon erasure-readout attempt.

Selective e<->h two-photon microwave drive and Floquet-assisted h->e emission
of two cavity photons. Preferred G106, source maximum frequency, all positive
frequency a/b output harmonics, finite cosine microwave ramps, photon-count
receiver, no terminal projector. Finite Floquet-RWA model only; the parent
pump waveform/bath and intrinsic higher-level rates remain unacquired.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import argparse
import json
import time
import numpy as np
from scipy import sparse as sp
from scipy.sparse.linalg import expm_multiply
SOURCE=Path('/Users/harjas/Documents/Codex/2026-10-13/astra-genesis-civilization-enabling-breakthrough-discovery')
sys.path.insert(0,str(SOURCE/'work/phase5/quantum_operation'))
import floquet_record_instrument as f
ROOT=Path(__file__).resolve().parent


def model(qdim=5,nf=6,epsilon=217.28013507543088):
    f.ecr.MEASURED_HALF_GE_CAVITY_SHIFT_MHZ=.5
    g=f.ecr.calibrate_g();f.f.G=g;f.f.DELTA=-2203.
    # Analytic sideband condition Delta+Omega=-3alpha/2=270MHz. Original JC
    # dispersive corrections move it, so inspect only a bounded local crossing.
    scan=[]
    for omega in np.arange(2463.,2484.,1.):
        block=f.f.floquet_block(3,epsilon,omega,sambe_half=5,ramp_steps=24)
        ee=block['values'][1]+omega;hh=block['values'][3]+3*omega
        scan.append({'omega_MHz':float(omega),'e2_h0_gap_MHz':float(abs(ee-hh))})
    omega=min(scan,key=lambda row:row['e2_h0_gap_MHz'])['omega_MHz']
    blocks={N:f.f.floquet_block(N,epsilon,omega,sambe_half=5,ramp_steps=24) for N in range(qdim+nf)}
    basis=[(q,n) for q in range(qdim) for n in range(nf)]
    idx={state:i for i,state in enumerate(basis)};dim=len(basis)
    energies=np.array([blocks[q+n]['values'][q]+q*omega for q,n in basis])
    rf_detuning=(energies[idx[(3,0)]]-energies[idx[(1,0)]])/2
    totals=np.array([q+n for q,n in basis])
    energies-=rf_detuning*totals
    calibration=f.static_vacuum_rates(g)
    collapse={'a':{},'b':{}};outside=np.zeros(dim);drive=np.zeros((dim,dim),complex)
    vacuum=[]
    for i,(qi,n) in enumerate(basis):
        N=qi+n
        if N==0:continue
        source,target=blocks[N],blocks[N-1]
        for qo in range(len(target['values'])):
            no=N-1-qo
            for bath,extractor in [('a',f.f.cavity_loss_harmonics),('b',f.bath_harmonics)]:
                harmonics=extractor(source,target,qi,qo)
                scale=f.KAPPA if bath=='a' else calibration[2 if qi>=2 else 1]['bath_scale']
                for ell,z in harmonics.items():
                    physical=7153.+source['values'][qi]-target['values'][qo]-ell*omega
                    if physical<=0 or abs(z)<1e-10:continue
                    k=ell+qi-qo
                    if (qo,no) in idx:
                        j=idx[(qo,no)]
                        if k not in collapse[bath]:collapse[bath][k]=np.zeros((dim,dim),complex)
                        collapse[bath][k][j,i]+=np.sqrt(scale)*z
                        # Qubit microwave carrier omega_r-Omega, represented
                        # by harmonic k=1 in this slow Floquet gauge.
                        if bath=='b' and k==1:drive[j,i]+=z
                    else:outside[i]+=scale*abs(z)**2
                    if n==0 and scale*abs(z)**2>1e-6:
                        vacuum.append({'input_q':qi,'output_q':qo,'output_n':no,'bath':bath,
                                       'harmonic_k':k,'frequency_MHz':float(physical),'rate_per_us':float(scale*abs(z)**2)})
    return {'dim':dim,'basis':basis,'energies':energies,'drive':drive,'collapse':collapse,'outside':outside,
            'diagnostics':{'G_MHz':g,'epsilon_MHz':epsilon,'omega_MHz':omega,
                           'frequency_range_MHz':[4950.-epsilon,4950.+epsilon],
                           'rf_frequency_MHz':7153.-omega+rf_detuning,
                           'rf_detuning_MHz':float(rf_detuning),'local_crossing_scan':scan,
                           'higher_level_b_bath_scale_per_us':calibration[2]['bath_scale'],
                           'vacuum_channels':vacuum,'maximum_unrepresented_loss_per_us':float(outside.max())}}


def generators(m,eta):
    d=m['dim'];I=sp.eye(d,format='csr')
    H0=sp.diags(2*np.pi*m['energies']);Hd=sp.csr_matrix(2*np.pi*(m['drive']+m['drive'].conj().T))
    L=-1j*(sp.kron(H0,I)-sp.kron(I,H0.T))
    Ld=-1j*(sp.kron(Hd,I)-sp.kron(I,Hd.T))
    J=sp.csr_matrix((d*d,d*d),dtype=complex)
    for bath,channels in m['collapse'].items():
        for a in channels.values():
            C=sp.csr_matrix(a);Q=C.conj().T@C
            recycle=sp.kron(C,C.conj())
            L+=recycle-.5*(sp.kron(Q,I)+sp.kron(I,Q.T))
            if bath=='a':J+=eta*recycle
    loss=sp.diags(m['outside'])
    L-=.5*(sp.kron(loss,I)+sp.kron(I,loss.T))
    return L.tocsr(),Ld.tocsr(),J.tocsr()


def run(m,eta,amplitude,flat,ramp,tail,segments,maxcount,modulation=0.,steps_per_period=12,legacy_count_phase=False,legacy_coarse_modulation=False):
    d=m['dim'];idx={state:i for i,state in enumerate(m['basis'])}
    z=np.zeros((d*d,4),complex)
    for col,(left,right) in enumerate([((0,0),(0,0)),((2,0),(2,0)),((1,0),(1,0)),((0,0),(2,0))]):
        z[idx[left]*d+idx[right],col]=1
    L,Ld,J=generators(m,eta)
    # Counts0..maxcount-1 are retained, all higher counts flag. No hidden
    # qutrit state is used in the receiver; every output branch remains present.
    bands=sp.diags(np.ones(maxcount-1),-1,shape=(maxcount,maxcount),format='csr')
    B0=sp.kron(sp.eye(maxcount),L-J)+sp.kron(bands,J)
    Bd=sp.kron(sp.eye(maxcount),Ld)
    values=np.zeros((maxcount*d*d,4),complex);values[:d*d]=z
    unconditional=z.copy();schedule=[]
    for j in range(segments):
        tmid=(j+.5)*ramp/segments
        schedule.append((ramp/segments,amplitude*(1-np.cos(np.pi*tmid/ramp))/2))
    schedule.append((flat,amplitude))
    for j in range(segments):
        tmid=(j+.5)*ramp/segments
        schedule.append((ramp/segments,amplitude*(1+np.cos(np.pi*tmid/ramp))/2))
    schedule.append((tail,0.))
    if modulation:
        refined=[]
        # Midpoint approximation to an explicit finite waveform. The cosine
        # modulation has zero linear carrier and a nonzero squared DC component.
        elapsed=0.
        components=schedule if legacy_coarse_modulation else [(ramp,None),(flat,None),(ramp,None)]
        for dt,coarse_u in components:
            if legacy_coarse_modulation and not coarse_u:
                refined.append((dt,0.));elapsed+=dt;continue
            steps=max(1,int(np.ceil(dt*modulation*steps_per_period)))
            sub=dt/steps
            for j in range(steps):
                t=elapsed+(j+.5)*sub
                envelope=(1-np.cos(np.pi*t/ramp))/2 if t<ramp else (1+np.cos(np.pi*(t-ramp-flat)/ramp))/2 if t>ramp+flat else 1.
                u=coarse_u if legacy_coarse_modulation else amplitude*envelope
                refined.append((sub,np.sqrt(2)*u*np.cos(2*np.pi*modulation*t)))
            elapsed+=dt
        if not legacy_coarse_modulation:refined.append((tail,0.))
        schedule=refined
    for j,(dt,u) in enumerate(schedule):
        G=(B0+u*Bd).tocsr()
        values=expm_multiply(G*dt,values,traceA=G.diagonal().sum()*dt)
        Gfree=(L+u*Ld).tocsr()
        unconditional=expm_multiply(Gfree*dt,unconditional,traceA=Gfree.diagonal().sum()*dt)
        if j%12==0 or j==len(schedule)-1:
            print(json.dumps({'segment':j,'drive_amplitude_MHz':u,'dt_us':dt}),flush=True)
    final=values.reshape(maxcount,d*d,4)
    cases=[]
    for cutoff in range(1,maxcount+1):
        accepted=final[:cutoff].sum(axis=0).T.reshape(4,d,d)
        populations=np.array([np.diag(mat).real for mat in accepted[:3]])
        totals=populations.sum(axis=1)
        gidx=[i for i,(q,n) in enumerate(m['basis']) if q==0]
        fidx=[i for i,(q,n) in enumerate(m['basis']) if q==2]
        # Physical photon count is retained, so a separate virtual Z may be
        # applied for each accepted count. This favorable feedforward cannot
        # restore logical information carried by missed photons.
        gfcoherence=0.
        for count in range(cutoff):
            cross=final[count,:,3].reshape(d,d)
            gfcoherence+=abs(sum(cross[idx[(0,n)],idx[(2,n)]] for n in range(max(n for q,n in m['basis'])+1)))
        if legacy_count_phase:
            gfcoherence=abs(sum(accepted[3,idx[(0,n)],idx[(2,n)]] for n in range(max(n for q,n in m['basis'])+1)))
        p=(totals[0]+totals[1])/2
        overlap=(populations[0,gidx].sum()+populations[1,fidx].sum()+2*gfcoherence)/4
        leakage=(totals[:2].sum()-populations[:2,gidx+fidx].sum())/2
        cases.append({'flag_if_detected_count_at_least':cutoff,'code_acceptance':float(p),
                      'accepted_Choi_infidelity':float(1-overlap/p),
                      'accepted_terminal_outside_GF_mass':float(leakage),
                      'prepared_e_flag_probability':float(1-totals[2]),
                      'initial_g_f_flag_probabilities':[float(1-totals[0]),float(1-totals[1])],
                      'accepted_cavity_mean_photons_mixed_code':float(sum(populations[i,j]*n for i in [0,1] for j,(q,n) in enumerate(m['basis']))/(2*p))})
    matrices=unconditional.T.reshape(4,d,d)
    return {'parameters':{'eta':eta,'qubit_drive_amplitude_MHz':amplitude,'flat_us':flat,
                           'ramp_us_each':ramp,'passive_tail_us':tail,'ramp_segments_each':segments,
                           'RF_sign_modulation_MHz':modulation,'modulation_steps_per_period':steps_per_period},
            'count_threshold_cases':cases,
            'represented_unconditional_traces_g_f_e':[float(np.trace(mat).real) for mat in matrices[:3]],
            'unconditional_cutoff_population_g_f_e':[float(sum(mat[i,i].real for i,(q,n) in enumerate(m['basis']) if n==max(nn for qq,nn in m['basis']))) for mat in matrices[:3]]}


def main():
    start=time.perf_counter();p=argparse.ArgumentParser()
    p.add_argument('--nf',type=int,default=6);p.add_argument('--qdim',type=int,default=5)
    p.add_argument('--amplitude',type=float,default=4.);p.add_argument('--flat',type=float,default=1.)
    p.add_argument('--modulation',type=float,default=0.);p.add_argument('--modulation-steps',type=int,default=12)
    p.add_argument('--legacy-count-phase',action='store_true',help='Replay initial pilot before per-count virtual-Z feedforward.')
    p.add_argument('--legacy-coarse-modulation',action='store_true',help='Replay historical RF modulation retaining coarse ramp-envelope samples.')
    p.add_argument('--segments',type=int,default=6);p.add_argument('--output',default='PAIR_FLUORESCENCE_RESULTS.json')
    args=p.parse_args();m=model(args.qdim,args.nf)
    r=run(m,.5,args.amplitude,args.flat,.1,.8,args.segments,4,args.modulation,args.modulation_steps,args.legacy_count_phase,args.legacy_coarse_modulation)
    result={'status':'NEW_ERASURE_FLUORESCENCE_MECHANISM_ATTEMPT_IN_FLOAT_FLOQUET_RWA_MODEL',
            'arguments':vars(args),'diagnostics':m['diagnostics'],'result':r,
            'runtime_seconds':time.perf_counter()-start,
            'limitations':['Floquet-RWA control projected to the commensurate RF harmonic; finite cosine RF ramps represented piecewise. Pump-on/off and real flux transfer remain separate gates.',
                           'Flat positive-frequency cavity and intrinsic-b baths; higher-level intrinsic rate continued from source FE calibration, not measured.',
                           'All cavity photon frequencies counted with eta .5 and no detector dark counts: extra receiver hardware is granted favorably.',
                           'Bath channels with equal harmonic are combined before secular averaging; full nonsecular driven model remains unvalidated.',
                           'No ideal terminal projector; code-only normalization is not used.']}
    (ROOT/args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

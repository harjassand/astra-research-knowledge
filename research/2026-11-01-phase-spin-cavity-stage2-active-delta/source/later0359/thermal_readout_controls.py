"""Reference-inclusive four-spin readout with actual thermal GKSL noise.

All rates are a declared finite Markov model, not measured hardware values.
There is no controller reset. The two receiver spins ARE fresh thermal inputs.
"""
import json,math,hashlib,itertools
from pathlib import Path
import numpy as np
from scipy.sparse import csc_matrix,eye,kron
from scipy.sparse.linalg import expm_multiply
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
def opnorm(a):return float(np.linalg.norm(a,2))
def main():
    sm=np.array([[0,1],[0,0]],complex);ss=[]
    for site in range(4):
        x=np.ones((1,1),complex)
        for j in range(4):x=np.kron(x,sm if j==site else np.eye(2))
        ss.append(x)
    ns=[x.conj().T@x for x in ss]
    X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.])
    delta=.1;T=math.pi/2;eta=.95;dark=1e-6;p_thermal=1e-5
    gamma_down=.002;dephase=.001;gamma_up=gamma_down*p_thermal/(1-p_thermal)
    H=np.kron(np.eye(16),17*X+.3*Z)
    for bit in (0,1):
        G=np.eye(2)+delta*(math.cos(.7+bit)*Z+math.sin(.7+bit)*Y)
        J=ss[bit].conj().T@ss[bit+2]+ss[bit+2].conj().T@ss[bit]
        H+=np.kron(J,G)
    d=32;I=eye(d,format='csc');Hs=csc_matrix(H)
    generator=-1j*(kron(I,Hs)-kron(Hs.T,I))
    for s,n in zip(ss,ns):
        for L in (math.sqrt(gamma_down)*s,math.sqrt(gamma_up)*s.conj().T,math.sqrt(2*dephase)*n):
            L=csc_matrix(np.kron(L,np.eye(2)));K=L.conj().T@L
            generator+=kron(L.conj(),L)-.5*kron(I,K)-.5*kron(K.T,I)
    generator=csc_matrix(generator)
    inputs=np.zeros((d*d,16),complex)
    for i,j in itertools.product(range(4),repeat=2):
        rho=np.zeros((d,d),complex)
        for r0,r1 in itertools.product((0,1),repeat=2):
            weight=p_thermal**(r0+r1)*(1-p_thermal)**(2-r0-r1)
            ai=((8 if i//2==0 else 4)+2*r0+r1)*2+i%2
            aj=((8 if j//2==0 else 4)+2*r0+r1)*2+j%2
            rho[ai,aj]=weight
        inputs[:,i+4*j]=rho.ravel(order='F')
    evolved=expm_multiply(T*generator,inputs,traceA=T*generator.diagonal().sum())
    choi=np.zeros((24,24),complex)
    for i,j in itertools.product(range(4),repeat=2):
        rho=evolved[:,i+4*j].reshape(d,d,order='F');out=np.zeros((6,6),complex)
        for s in range(16):
            c0=1-(1-dark)*(1-eta*((s>>1)&1));c1=1-(1-dark)*(1-eta*(s&1))
            weights=(c0*(1-c1),(1-c0)*c1,1-c0*(1-c1)-(1-c0)*c1)
            for label,w in enumerate(weights):out[label*2:label*2+2,label*2:label*2+2]+=w*rho[2*s:2*s+2,2*s:2*s+2]
        choi[i*6:(i+1)*6,j*6:(j+1)*6]=out
    partial=np.einsum('aiaj->ij',choi.reshape(6,4,6,4,order='F'))
    tp=opnorm(partial-np.eye(4));mineig=float(np.linalg.eigvalsh((choi+choi.conj().T)/2)[0])
    assert tp<2e-11 and mineig>-2e-11
    effects=[]
    for bit in (0,1):
        row=[]
        for label in (0,1,2):
            inds=[out+6*inp for inp in range(2*bit,2*bit+2) for out in range(2*label,2*label+2)]
            C=choi[np.ix_(inds,inds)].reshape(2,2,2,2,order='F')
            effect=np.einsum('aiaj->ij',C).T
            row.append(effect)
        effects.append(row)
    actual_correct=min(float(np.linalg.eigvalsh(effects[b][b])[0]) for b in (0,1))
    actual_wrong=max(opnorm(effects[b][1-b]) for b in (0,1))
    actual_flag=max(opnorm(effects[b][2]) for b in (0,1))
    cross=opnorm(choi[:12,12:])
    good_receiver=(1-p_thermal)**2
    no_jump=math.exp(-(gamma_down+2*dephase+3*gamma_up)*T)
    correct_lower=good_receiver*eta*(1-dark)**2*no_jump*math.cos(math.pi*delta/2)**2
    erasure_upper=1-correct_lower
    wrong_upper=2*p_thermal+4*gamma_up*T+2*dark
    assert actual_correct>=correct_lower-2e-11 and actual_wrong<=wrong_upper+2e-11
    assert actual_flag<=erasure_upper+2e-11 and cross<2e-11
    # Exhaustive decoder controls for every received 7-symbol string and
    # every valid codeword, including mixed errors and erasures.
    gens=(0b1111000,0b1100110,0b1010101)
    C0=sorted({a*gens[0]^b*gens[1]^c*gens[2] for a,b,c in itertools.product((0,1),repeat=3)})
    code=(C0,sorted(x^127 for x in C0));decoders=[]
    for received in itertools.product((0,1,2),repeat=7):
        known=sum(1<<j for j,v in enumerate(received) if v!=2)
        ones=sum(1<<j for j,v in enumerate(received) if v==1)
        scores=[min(((w^ones)&known).bit_count() for w in words) for words in code]
        label=scores.index(min(scores)) if scores[0]!=scores[1] else 2
        decoders.append((received,label))
    controls=0
    for logical,words in enumerate(code):
      for w in words:
       for rec,label in decoders:
        erased=[j for j,v in enumerate(rec) if v==2]
        wrong=[j for j,v in enumerate(rec) if v!=2 and v!=((w>>j)&1)]
        if not wrong:assert label==logical or label==2
        if len(erased)+2*len(wrong)<3:assert label==logical
        if label!=logical:
            bad_erasure=any(all(rec[j]==2 for j in range(7) if (t>>j)&1) for t in code[1] if t.bit_count()==3)
            assert bad_erasure or (len(erased)>=1 and len(wrong)>=1) or len(wrong)>=2
        controls+=1
    e,w=erasure_upper,wrong_upper;levels=[]
    for level in range(6):
        levels.append({'level':level,'physical_data_qubits':7**level,'fresh_thermal_receiver_spins':2*7**level,
                       'sequential_read_time':T*7**level,'erasure_upper':e,'wrong_label_upper':w})
        bad=42*e*w+21*w*w;e,w=min(1.,7*e**3+bad),min(1.,bad)
    result={'status':'PASS reference-inclusive finite thermal dynamics and decoder controls',
       'parameters':{'gain_relative_uncertainty':delta,'duration':T,'collection_efficiency':eta,
           'fresh_receiver_thermal_population':p_thermal,'gamma_down':gamma_down,'gamma_up':gamma_up,
           'dephasing_rate':dephase,'per_rail_detector_dark':dark,
           'detailed_balance_beta_energy':math.log((1-p_thermal)/p_thermal)},
       'full_source_Choi_TP_residual':tp,'full_source_Choi_minimum_eigenvalue':mineig,
       'logical_input_offdiagonal_source_channel_norm':cross,
       'actual_worst_source_correct_label_lower':actual_correct,'analytic_correct_label_lower':correct_lower,
       'actual_worst_source_wrong_label_upper':actual_wrong,'analytic_wrong_label_upper':wrong_upper,
       'actual_worst_source_erasure_upper':actual_flag,'analytic_erasure_upper':erasure_upper,
       'exhaustive_classical_decoder_cases':controls,'mixed_fault_recursive_bounds':levels,
       'scope':'four hard-core two-level sites per raw read plus arbitrary reused quantum controller; exact supplied Markov model; code encoder, source Hamiltonian engineering, and final detector qualification remain assumptions',
       'costs':'two fresh thermal receiver spins per physical read, four thermal local baths, finite timed exchange pulse, two detector ports, classical decoding; sequential storage during all reads is not qualified',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'thermal_readout_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

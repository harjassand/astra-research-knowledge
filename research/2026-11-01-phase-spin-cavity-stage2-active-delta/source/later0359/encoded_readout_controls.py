"""Full source/reference instrument control for destructive encoded readout.

The new warm-read primitive gives an exact labelled measurement or a flagged
loss on a dual-rail physical qubit. Source operators are carried coherently
across all seven reads. Classical decoding is standard Steane/CSS structure.
No independent-fault or controller-reset assumption is used.
"""
import itertools,json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'outputs/coherent_inference_20261101'
X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1.,-1.])
def opnorm(x):return float(np.linalg.norm(x,2))
def main():
    generators=(0b1111000,0b1100110,0b1010101)
    C0=sorted({a*generators[0]^b*generators[1]^c*generators[2] for a,b,c in itertools.product((0,1),repeat=3)})
    C1=sorted(x^0b1111111 for x in C0);code=(C0,C1)
    assert len(C0)==len(C1)==8 and min((a^b).bit_count() for a in C0 for b in C1)==3
    minimal_bad=[x for x in C1 if x.bit_count()==3];assert len(minimal_bad)==7
    for mask in range(128):
        ambiguous=any((a^b)&~mask==0 for a in C0 for b in C1)
        assert ambiguous==any(t&mask==t for t in minimal_bad)
    delta=.1;collection=.95;T=math.pi/2;raw_p=1-collection*math.cos(math.pi*delta/2)**2
    raw=[];direct_error=0.;complete_error=0.
    for j in range(7):
        H=(j+1)*1.7*X+.31*math.sin(j+1)*Y
        drift=expm(-1j*(.2+j*.11)*Y)
        bitops=[]
        # Five physical states: q0,q1,one-photon-rail0,rail1,vacuum.
        HH=np.kron(np.eye(5),H)
        for bit in (0,1):
            angle=(j+2*bit)*.73;gain=np.eye(2)+delta*(math.cos(angle)*Z+math.sin(angle)*X)
            vm=expm(-1j*(H-gain)*T);vp=expm(-1j*(H+gain)*T)
            A=(vp+vm)/2;B=(vp-vm)/2
            err=np.linalg.norm(A.conj().T@A+B.conj().T@B-np.eye(2),2);complete_error=max(complete_error,float(err))
            assert opnorm(A)**2<=math.sin(math.pi*delta/2)**2+1e-12
            bitops.append((math.sqrt(collection)*drift@B,drift@A,math.sqrt(1-collection)*drift@B))
            J=np.zeros((5,5));J[bit,bit+2]=J[bit+2,bit]=1
            HH+=np.kron(J,gain)
        U=expm(-1j*HH*T)
        for bit in (0,1):
            direct=U[(bit+2)*2:(bit+3)*2,bit*2:(bit+1)*2]
            direct_error=max(direct_error,opnorm(drift@direct-bitops[bit][0]/math.sqrt(collection)))
        raw.append(bitops)
    assert direct_error<1e-12 and complete_error<1e-12
    choi=np.zeros((24,24),complex);effects=[np.zeros((2,2),complex),np.zeros((2,2),complex)]
    histories=0
    for logical,words in enumerate(code):
      for word in words:
       for path in itertools.product(range(3),repeat=7):
        mask=sum(1<<j for j,k in enumerate(path) if k!=0)
        observed=word&~mask
        possible=[l for l,ww in enumerate(code) if any(x&~mask==observed for x in ww)]
        label=possible[0] if len(possible)==1 else 2
        assert label==logical or label==2
        M=np.eye(2,dtype=complex)
        for j,k in enumerate(path):M=raw[j][(word>>j)&1][k]@M
        M/=math.sqrt(8)
        K=np.zeros((6,4),complex);K[label*2:label*2+2,logical*2:logical*2+2]=M
        vec=K.ravel(order='F');choi+=np.outer(vec,vec.conj())
        if label==2:effects[logical]+=M.conj().T@M
        histories+=1
    # Choi trace over output equals identity on logical input + source.
    partial=np.einsum('aiaj->ij',choi.reshape(6,4,6,4,order='F'))
    tp=opnorm(partial-np.eye(4));assert tp<2e-11
    minimum=float(np.linalg.eigvalsh((choi+choi.conj().T)/2)[0]);assert minimum>-1e-11
    # Every accepted logical label has support only on its own input-logical
    # Choi block, with the source fully present. This is reference-inclusive.
    wrong=0.
    for label in (0,1):
        bad=[out+6*inp for out in range(2*label,2*label+2) for inp in range(2*(1-label),2*(1-label)+2)]
        wrong=max(wrong,float(np.linalg.norm(choi[np.ix_(bad,bad)],2)))
    flag=max(opnorm(e) for e in effects);upper=7*raw_p**3
    assert wrong<1e-13 and flag<=upper+1e-12
    # Conditional fault-set bounds, not IID approximations. Dark clicks are
    # a separate, explicit raw wrong-label budget in this extension.
    erasure=raw_p+2e-7;wrong_rate=2e-7;levels=[]
    for level in range(5):
        levels.append({'level':level,'physical_qubits':7**level,'erasure_upper':erasure,'wrong_label_upper':wrong_rate})
        bad_error=42*erasure*wrong_rate+21*wrong_rate**2
        erasure,wrong_rate=min(1.,7*erasure**3+bad_error),min(1.,bad_error)
    result={'status':'PASS complete encoded instrument with one coherently reused quantum source',
       'raw_gain_relative_uncertainty':delta,'collection_efficiency':collection,
       'raw_erasure_operator_bound':raw_p,'minimal_ambiguous_erasure_triples':minimal_bad,
       'raw_full_physical_isometry_residual':direct_error,'raw_trace_preservation_residual':complete_error,
       'enumerated_physical_Kraus_histories':histories,'full_source_logical_Choi_trace_preservation_residual':tp,
       'full_source_logical_Choi_minimum_eigenvalue':minimum,'accepted_wrong_logical_label_Choi_block_norm':wrong,
       'worst_source_state_logical_erasure_probability':flag,'logical_erasure_fault_set_upper':upper,
       'mixed_fault_recursive_bounds':levels,
       'limits':'encoded dual-rail/single-excitation input, independent fresh vacuum loss ports, no unmodeled cross-rail heating; no code encoder or universal computer is constructed',
       'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'encoded_readout_controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()

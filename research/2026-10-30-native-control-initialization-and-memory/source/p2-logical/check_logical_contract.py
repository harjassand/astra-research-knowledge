#!/usr/bin/env python3
"""Strong ordinary corrections under the same known-dilation permissions.

The goal is identity on L with arbitrary old-dirty/bath inputs and references.
It does not require retrieving the microscopic bath state. The original dirty
register is retained. These alternatives prevent an unfair full-state-retrieval
comparison from becoming a claimed logical-computing advantage.
"""
import json
from pathlib import Path
import numpy as np
from explore_rescue import cq_channel,choi
from check_information_rescue import (DIMS,L,OLD,B,FPROBE,S,ARCH,initial,
    apply,complete,rewrite,sqrt_psd,dirty_unitary,fidelity_lr)


def syndrome_inverse():
    # Registers L, OLD, S; S=2*g+a exposes the old bath's Z-syndrome a.
    u=np.zeros((16,16),complex)
    for l in range(2):
        for f in range(2):
            for s in range(4):
                lo=l^(f*(s%2))
                u[(lo*2+f)*4+s,(l*2+f)*4+s]=1
    return u


def upstream_kraus(ks):
    # Input L x OLD x B; inaccessible output B. Trace accessible L,OLD,S.
    out=[]
    for lo in range(2):
        for fo in range(2):
            for k in ks:
                a=np.zeros((2,8),complex)
                for l in range(2):
                    for f in range(2):
                        for b in range(2):
                            if fo==f and lo==(l^(f*b)):
                                a[:,(l*2+f)*2+b]=k[:,b]
                out.append(a)
    return out


def main():
    ks=cq_channel([.6,0,-.75],[.6,0,.5])
    source=complete(ks.reshape(8,2))
    rhos=[np.array([[.125,.3],[.3,.875]]),np.array([[.75,.3],[.3,.25]])]
    semantic=[]
    for g in range(2):
        for a in range(2):
            k=np.zeros((2,2),complex);k[:,a]=sqrt_psd(rhos[a])[:,g]
            semantic.append(k)
    basis_change=rewrite(ks,np.array(semantic))

    original=initial()
    damaged=apply(original,dirty_unitary(2),(L,OLD,B))

    def first_output(state):
        state=apply(state,dirty_unitary(4),(L,FPROBE,B))
        state=apply(state,source,(FPROBE,B))
        state=state.swapaxes(FPROBE,S)
        return apply(state,basis_change,(S,))

    outgoing=first_output(damaged)
    repaired=apply(outgoing,syndrome_inverse(),(L,OLD,S))
    expected=first_output(original)
    identity_error=float(np.linalg.norm(repaired-expected))
    assert identity_error<1e-12
    # Store the four-dimensional outgoing gauge in the existing archive. This
    # returns the real reused output S to blank without erasing it.
    repaired=repaired.swapaxes(S,ARCH)
    dirty_probe=float(np.sum(np.abs(repaired[:,:,:,:,:,:,1:,:,:])**2))
    dirty_output=float(np.sum(np.abs(repaired[:,:,:,:,:,:,:,1:,:])**2))
    assert dirty_probe<1e-20 and dirty_output<1e-20

    # A stronger permitted alternative when native dirty inputs can be chosen:
    # coherently copy OLD's control bit into the spare probe. The actual native
    # dirty completion then replays and cancels the original controlled X.
    copy=np.zeros((8,8),complex)
    for f in range(2):
        for r in range(4):copy[4*f+(r^f),4*f+r]=1
    replay=apply(damaged,copy,(OLD,FPROBE))
    replay=first_output(replay)
    assert abs(fidelity_lr(replay)-1)<1e-12

    # One real receiver fault flips the acquired syndrome before correction.
    flip=np.zeros((4,4),complex)
    for s in range(4):flip[s^1,s]=1
    wrong=apply(outgoing,flip,(S,))
    wrong=apply(wrong,syndrome_inverse(),(L,OLD,S))
    assert abs(fidelity_lr(wrong)-.5)<1e-12

    # Verify the logical-only minorant with p=1: the upstream channel is
    # H o Tr_L. H can retain dependence on OLD and B; it need not replace them.
    fks=upstream_kraus(ks)
    hks=[]
    for f in range(2):
        for k in ks:
            h=np.zeros((2,4),complex);h[:,2*f:2*f+2]=k;hks.append(h)
    target=[]
    for l in range(2):
        for h in hks:
            a=np.zeros((2,8),complex);a[:,4*l:4*l+4]=h;target.append(a)
    factor_error=float(np.max(np.abs(choi(fks)-choi(target))))
    trace_error=float(np.max(np.abs(sum(h.conj().T@h for h in hks)-np.eye(4))))
    assert max(factor_error,trace_error)<1e-12

    # Stronger logical-only implementation: the native source already labels
    # its Kraus operators by a=0,1 (S=2*a+g). Measure a and the retained OLD
    # gauge bit f, then apply the Pauli X**(f*a). No arbitrary output rotation,
    # coherent archive, or bath-state reconstruction is needed for this goal.
    def raw_output(v):
        v=apply(v,dirty_unitary(4),(L,FPROBE,B))
        v=apply(v,source,(FPROBE,B))
        return v.swapaxes(FPROBE,S)
    raw_bad=raw_output(damaged);raw_good=raw_output(original)
    measured=[]
    for f in range(2):
        for a in range(2):
            pold=np.diag([int(i==f) for i in range(2)])
            pout=np.diag([int(s//2==a) for s in range(4)])
            v=apply(apply(raw_bad,pold,(OLD,)),pout,(S,))
            target=apply(apply(raw_good,pold,(OLD,)),pout,(S,))
            if f*a:v=apply(v,np.array([[0,1],[1,0]]),(L,))
            err=float(np.linalg.norm(v-target));assert err<1e-12
            measured.append({'record':[f,a],'probability':float(np.vdot(v,v).real),
                             'logical_fidelity':fidelity_lr(v),'full_branch_vector_error':err})
    assert abs(sum(r['probability'] for r in measured)-1)<1e-12
    result={
        'scope':'Root full-isometry check of logical-only recovery and stronger ordinary alternatives; no independent review or native threshold.',
        'input_space':'L x OLD x B, each qubit maximally entangled with its own reference; checks the complete eight-dimensional input map.',
        'old_dirty_register_retained':True,
        'source_calls':1,
        'logical_fidelity_after_initial_excursion':fidelity_lr(damaged),
        'coherent_syndrome_recovery':{
            'logical_fidelity':fidelity_lr(repaired),'full_operator_vector_error':identity_error,
            'reused_probe_dirty_mass':dirty_probe,'reused_output_dirty_mass':dirty_output,
            'archive_dimension':4,'ideal_success_probability':1},
        'known_native_replay_cancellation':{'logical_fidelity':fidelity_lr(replay)},
        'logical_only_minorant':{'success_probability':1,'factorized_choi_error':factor_error,'gauge_map_trace_preservation_error':trace_error},
        'native_measurements_and_conditional_pauli':{
            'coherent_archive_dimension':1,'arbitrary_output_basis_change_required':False,
            'classical_record_bits':2,'branch_checks':measured,
            'entropy_contract':'Gauge measurements and their records are actual operations. Gauge retirement requires a real outlet after logical repair; it is not an ideal reset before reuse.'},
        'real_syndrome_fault_negative':{'logical_fidelity':fidelity_lr(wrong)},
        'comparison':'Full bath retrieval needs additional time in this source; it is a stronger task. It is not necessary for this logical correction.'
    }
    Path(__file__).with_name('logical_contract_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()

"""Finite-description local stabilization compiler and binary64 audit helpers.

The integer resource certificate is exact. The theorem assumes exactly unitary
one/two-qubit input gates. Matrix expansion and density-matrix audits below are
binary64 diagnostics, not certified native gate synthesis or physical runs.
Qubit 0 is the most significant tensor factor. A clock word is 1^t 0^(T-t).
"""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction
from pathlib import Path
import numpy as np


def ceil_log2(x: Fraction) -> int:
    x = Fraction(x)
    if x <= 1:
        return 0
    b = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    return b + ((1 << b) * x.denominator < x.numerator)


def resource_certificate(q: int, T: int, duty, mixing_error) -> dict:
    duty, mixing_error = Fraction(duty), Fraction(mixing_error)
    if q < 1 or T < 1 or not 0 < duty <= Fraction(1, 2):
        raise ValueError("q,T positive and 0 < duty <= 1/2 required")
    if not 0 < mixing_error < 1:
        raise ValueError("0 < mixing_error < 1 required")
    b = ceil_log2(T * (1-duty) / duty)
    K = 1 << b
    terms = q + 3*T - 1
    M = 1 << (2*terms - 1).bit_length()
    d = M * ceil_log2(3*T/mixing_error)
    c = M*T*(T-1)*ceil_log2(3/mixing_error)
    ell = M*(T+1)*(K+T)*ceil_log2(3*(q+1)*(K+T)/mixing_error)
    return {
        "work_qubits": q, "clock_qubits": T, "total_qubits": q+T,
        "nonidentity_channel_types": terms, "random_scan_slots": M,
        "selector_bits_per_event": M.bit_length()-1,
        "last_reverse_coin_bits": b, "last_reverse_probability": f"1/{K}",
        "early_clock_weight": f"1/{K+T}",
        "terminal_clock_weight": str(Fraction(K,K+T)),
        "actual_duty_error_bound": str(Fraction(T,K+T)),
        "requested_duty_error_bound": str(duty),
        "requested_complete_mixing_error": str(mixing_error),
        "killed_chain_gap_lower": f"1/{M*(T+1)*(K+T)}",
        "clock_dephasing_events_bound": d,
        "invalid_clock_cleanup_events_bound": c,
        "legal_history_mixing_events_bound": ell,
        "total_events_bound": d+c+ell,
        "event_support_qubits_max": 5,
        "event_cost_excludes": ["input circuit acquisition", "native synthesis",
            "routing", "reset and randomness production", "physical timing", "power"],
    }


def compile_description(source: dict, duty="1/16", mixing_error="1/16") -> dict:
    q, gates = int(source["work_qubits"]), source["gates"]
    if not gates:
        raise ValueError("Supply at least one gate; pad an empty circuit with identity")
    for g in gates:
        a = g["qubits"]
        if len(a) not in (1,2) or len(set(a)) != len(a) or not all(0 <= x < q for x in a):
            raise ValueError("Every input gate must act on one or two valid work qubits")
    T = len(gates)
    cert = resource_certificate(q,T,duty,mixing_error)
    channels = []
    for j in range(q):
        channels.append({"kind":"input_reset", "work_qubit":j,
            "clock_condition": {"index":0,"value":0}, "reset_state":"zero"})
    for t,g in enumerate(gates):
        channels.append({"kind":"history_edge", "clock_center":t,
            "left": {"index":t-1,"value":1} if t else {"fixed_boundary":1},
            "right": {"index":t+1,"value":0} if t+1<T else {"fixed_boundary":0},
            "dephase_clock_indices":list(range(max(0,t-1), min(T,t+2))),
            "forward_gate":g, "reverse_gate":"adjoint of forward gate",
            "forward_probability":"1",
            "reverse_probability":cert["last_reverse_probability"] if t==T-1 else "1"})
    for t in range(T):
        channels.append({"kind":"clock_dephase", "clock_index":t})
    for t in range(T-1):
        channels.append({"kind":"clock_cleanup", "clock_pair":[t,t+1],
            "transition":"01 -> 00; other classical patterns unchanged",
            "dephase_pair":True})
    return {"format":"P3_LOCAL_STABILIZER_V1", "source":source,
        "certificate":cert, "channels":channels,
        "padding_identity_slots":cert["random_scan_slots"]-len(channels),
        "semantics":"At every event choose a uniform slot; repeat this same channel forever.",
        "gate_contract":"Input gates are exact unitaries in the theorem. Floating matrices are diagnostics.",
        "noise_block_certificate":resource_certificate(q,T,duty,"1/4")}


def gate_matrix(g: dict) -> np.ndarray:
    kind = g["kind"].upper()
    if kind == "H": return np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
    if kind == "X": return np.array([[0,1],[1,0]],complex)
    if kind == "S": return np.diag([1,1j])
    if kind == "CNOT":
        return np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],complex)
    if kind == "RY":
        x=float(g["angle"])/2
        return np.array([[np.cos(x),-np.sin(x)],[np.sin(x),np.cos(x)]],complex)
    if kind == "RZ":
        x=float(g["angle"])/2
        return np.diag([np.exp(-1j*x),np.exp(1j*x)])
    if kind == "MATRIX":
        return np.array([[complex(*z) for z in row] for row in g["matrix"]],complex)
    raise ValueError(f"Unknown gate {kind}")


def embed(A, sites, n):
    sites=list(sites); d=1<<n
    out=np.zeros((d,d),complex)
    for col in range(d):
        local=0
        for site in sites: local=(local<<1)|((col>>(n-1-site))&1)
        for row_local in range(1<<len(sites)):
            val=A[row_local,local]
            if val==0: continue
            row=col
            for j,site in enumerate(sites):
                bit=(row_local>>(len(sites)-1-j))&1
                row=(row & ~(1<<(n-1-site))) | (bit<<(n-1-site))
            out[row,col]+=val
    return out


def word(s,T): return tuple((s>>(T-1-i))&1 for i in range(T))
def encode(w):
    ans=0
    for x in w: ans=(ans<<1)|x
    return ans


def potential(w):
    T=len(w)
    return sum(T-1-i for i in range(T-1) if w[i:i+2]==(0,1))


def edge_destination(w,t,reverse=False):
    T=len(w)
    if (t==0 or w[t-1]==1) and (t==T-1 or w[t+1]==0):
        z=list(w); z[t]=1-z[t]
        return tuple(z)
    return w


def reset_kraus(site,q):
    return [embed(np.array([[1,0],[0,0]],complex),[site],q),
            embed(np.array([[0,1],[0,0]],complex),[site],q)]


def stationary_history(source,cert):
    q=source["work_qubits"]; T=len(source["gates"]); d=1<<q
    a=float(Fraction(cert["early_clock_weight"]))
    terminal=float(Fraction(cert["terminal_clock_weight"]))
    states=[]; v=np.zeros(d,complex);v[0]=1
    states.append(np.outer(v,v.conj()))
    for g in source["gates"]:
        v=embed(gate_matrix(g),g["qubits"],q)@v
        states.append(np.outer(v,v.conj()))
    blocks=np.zeros((1<<T,d,d),complex)
    for t,rho in enumerate(states):
        s=encode((1,)*t+(0,)*(T-t))
        blocks[s]=(terminal if t==T else a)*rho
    return blocks, states


def apply_diagonal_clock(blocks,source,cert):
    q=source["work_qubits"];T=len(source["gates"])
    M=cert["random_scan_slots"];r=float(Fraction(cert["last_reverse_probability"]))
    out=(M-(q+3*T-1))*blocks.copy()
    for j in range(q):
        ops=reset_kraus(j,q)
        for s,B in enumerate(blocks):
            if word(s,T)[0]==0:
                out[s]+=sum(K@B@K.conj().T for K in ops)
            else: out[s]+=B
    for t,g in enumerate(source["gates"]):
        U=embed(gate_matrix(g),g["qubits"],q)
        for s,B in enumerate(blocks):
            w=word(s,T);dest=edge_destination(w,t)
            if dest==w: out[s]+=B;continue
            if w[t]==0: out[encode(dest)]+=U@B@U.conj().T
            else:
                p=r if t==T-1 else 1
                out[encode(dest)]+=p*U.conj().T@B@U
                out[s]+=(1-p)*B
    out+=T*blocks  # each clock dephaser is identity on these blocks
    for t in range(T-1):
        for s,B in enumerate(blocks):
            w=list(word(s,T))
            if w[t:t+2]==[0,1]: w[t+1]=0
            out[encode(w)]+=B
    return out/M


def full_kraus_channels(source,cert):
    """Small-system audit expansion; intentionally exponential, not the compiler."""
    q=source["work_qubits"];T=len(source["gates"]);n=q+T;D=1<<n
    Iw=np.eye(1<<q);Ic=np.eye(1<<T)
    P0=np.array([[1,0],[0,0]],complex);P1=np.diag([0,1])
    channels=[]
    for j in range(q):
        C0=embed(P0,[0],T);C1=embed(P1,[0],T)
        channels.append([np.kron(K,C0) for K in reset_kraus(j,q)]+[np.kron(Iw,C1)])
    r=float(Fraction(cert["last_reverse_probability"]))
    for t,g in enumerate(source["gates"]):
        U=embed(gate_matrix(g),g["qubits"],q);ks=[]
        # Dephase exactly the local clock patch, retaining identity on other bits.
        patch=list(range(max(0,t-1),min(T,t+2)))
        for mask in range(1<<len(patch)):
            localbits=word(mask,len(patch)); wdict=dict(zip(patch,localbits))
            P=np.zeros((1<<len(patch),1<<len(patch)),complex);P[mask,mask]=1
            Cp=embed(P,patch,T)
            allowed=(t==0 or wdict[t-1]==1) and (t==T-1 or wdict[t+1]==0)
            if not allowed: ks.append(np.kron(Iw,Cp));continue
            flip=embed(np.array([[0,1],[1,0]],complex),[t],T)@Cp
            if wdict[t]==0: ks.append(np.kron(U,flip))
            else:
                p=r if t==T-1 else 1
                ks.append(np.sqrt(p)*np.kron(U.conj().T,flip))
                if p<1: ks.append(np.sqrt(1-p)*np.kron(Iw,Cp))
        channels.append(ks)
    for t in range(T):
        channels.append([np.kron(Iw,embed(P,[t],T)) for P in (P0,P1)])
    for t in range(T-1):
        ks=[]
        for j in range(4):
            P=np.zeros((4,4),complex);P[0 if j==1 else j,j]=1
            ks.append(np.kron(Iw,embed(P,[t,t+1],T)))
        channels.append(ks)
    return channels


def superoperator(source,cert):
    D=1<<(source["work_qubits"]+len(source["gates"]))
    channels=full_kraus_channels(source,cert);M=cert["random_scan_slots"]
    S=(M-len(channels))*np.eye(D*D,dtype=complex)
    tp=[]
    for ops in channels:
        tp.append(float(np.linalg.norm(sum(K.conj().T@K for K in ops)-np.eye(D))))
        for K in ops:S+=np.kron(K.conj(),K)
    return S/M,tp


def blocks_to_density(blocks):
    C,d,_=blocks.shape
    rho=np.zeros((C*d,C*d),complex)
    for s,B in enumerate(blocks):rho[s::C,s::C]=B
    return rho


def trace_distance(A,B):
    D=(A-B + (A-B).conj().T)/2
    return float(np.abs(np.linalg.eigvalsh(D)).sum()/2)


def reduce_state(rho,keep,n):
    keep=list(keep); traced=[i for i in range(n) if i not in keep]
    perm=keep+traced+[n+i for i in keep]+[n+i for i in traced]
    a=rho.reshape((2,)*(2*n)).transpose(perm)
    d=1<<len(keep);e=1<<len(traced)
    return np.einsum('abcb->ac',a.reshape(d,e,d,e))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("source");p.add_argument("output")
    p.add_argument("--duty",default="1/16");p.add_argument("--mixing-error",default="1/16")
    a=p.parse_args()
    result=compile_description(json.loads(Path(a.source).read_text()),a.duty,a.mixing_error)
    Path(a.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["certificate"],indent=2))


if __name__=="__main__": main()

# Compressed moments do not supply the physical decoder: a paid orientation bridge

2026-10-28. Root candidate; independent review pending. This is an explicit acquisition example, not a general new Krylov recovery theorem or a claim of historical novelty.

## Primary comparison

Chowdhury, arXiv:2610.33607v1 (24 October 2026), sections 3.4 and 5.1, treats a known generator and encoder. Compressed moments determine the boundary cost without a full physical basis; the finite-angle robust optimization still uses physical spectral images. This note changes the interface to an unknown physical generator orientation. It does not contradict the known-generator theorem.

Primary source inspected: https://arxiv.org/html/2610.33607v1 , sections 3.4, 5.1, 7.5. No external formula is imported without the explicit elementary derivation below.

## Exact family and complete moment indistinguishability

Let physical output be a known flag qubit S and logical-size register L of dimension d. Encoder V|psi>=|0>_S|psi>. For any unknown unitary W on L, define

    H_W = |1><0| tensor W + |0><1| tensor W^dagger.

Then H_W^2=I, V^dagger H_W^(2j)V=I and V^dagger H_W^(2j+1)V=0 for ALL j>=0. Every compressed moment, not merely a finite prefix, is independent of W. The encoded spectrum and scalar angle distribution therefore do not locate the physical leakage decoder.

Apply e^(-i xi theta H_W) with independent xi=+1,-1 equally likely, theta fixed in [0,pi/2]. This yields the actual channel

    N_W(rho)=(1-p)|0><0| tensor rho + p|1><1| tensor W rho W^dagger,
    p=sin(theta)^2.                                               (1)

All generator powers are correctable for a KNOWN W: read flag S, apply I on flag0 and W^dagger on flag1. Oracle loss is exactly zero for every p. No environment access is necessary once the orientation is known.

If the receiver is given only p and all compressed moments, any common full CPTP recovery has worst-W entanglement loss at least p(1-1/d^2). Proof: average W over the d^2 Weyl unitaries. The leakage channel becomes the completely depolarizing channel, whose composition with any TP decoder has entanglement fidelity 1/d^2. The flag0 contribution is at most 1. The average loss lower-bounds a worst case. A decoder that preserves flag0 and replaces flag1 by the maximally mixed state attains this uniformly. Thus the exact minimax loss is p(1-1/d^2), despite the common moments and a zero informed optimum.

This is an operation-identifiability gap, not an inability to predict the informed optimal value. Physical orientation is required; moment-only zero optimal loss does not implement recovery. The source promises and known flag factorization are substantial inputs.

## Ordinary qubit acquisition without a rare-success oracle

Now d=2 and grant ordinary labelled single-qubit preparations, the known flag measurement, and local Pauli measurements. Noise is stationary and independently sampled across these calibration calls; this example does not inherit the retained-memory theorem. No entangled calibration reference, inverse source, or coherent generator query is used.

On each of exactly N calls choose input Pauli axis j uniformly from X,Y,Z, sign s uniformly, prepare its signed eigenstate, measure flag f, and measure output L in independent uniform Pauli axis a with sign b. Define

    F=9 f s b e_a e_j^T,    Mhat=N^(-1) sum F.

For the proper Bloch rotation R of W,

    E F=pR,     E||F||_F^2=81p,
    E||Mhat-pR||_F^2=(81p-3p^2)/N <=81p/N.             (2)

All failed/flag0 calls are counted. No division by observed success count or p is performed. Fit a proper rotation Rhat satisfying

    <Rhat,Mhat> >= max_(Q in SO(3))<Q,Mhat>-delta.

The finite rational quaternion fit from the received on-site construction supplies a physical unitary What with that objective gap, including zero/degenerate Mhat. Here ||Mhat||_F<=9 deterministically, so only the constant normalization of its 4x4 matrix changes. Apply What^dagger only on flag1; pass flag0 unchanged.

Let E=Mhat-pR and t=||Rhat-R||_F. For p>0, proper-rotation optimality gives

    (p/2)t^2 <=t||E||_F+delta,
    t^2 <=4||E||_F^2/p^2+4delta/p.

A unitary qubit error has Bell loss t^2/8, hence the ACTUAL total recovered-channel loss obeys

    ell <= ||E||_F^2/(2p)+delta/2,
    E ell <=81/(2N)+delta/2.                           (3)

For p=0 there is no leakage and actual loss is exactly zero, irrespective of the fitted rotation. With delta=1/N, expected loss is <=min(p,41/N). The min(p,...) bound follows because each physical flag1 decoder has loss at most one, not because data certified p. This is a distribution-free-in-p risk bound within the stationary flagged family, not a high-probability guarantee conditional on a realized record.

Finite fit precision is polynomial in log N, using rational counts and the already received gap-free quaternion fitting primitive. Preparation, flag detection, Pauli axes/readout, fit, controlled one-qubit inverse and flag discard are required; uniform whole-process implementation error nu adds nu to expected Bell loss. Count all N source calls, N preparations, N flag readouts and N Pauli readouts, then one payload call. The output register and flag are assumed known and measurable. No practical superiority over conventional process tomography is claimed: this IS a targeted conventional unitary-tomography fit that exploits the flag.

The scientific bridge is the cancellation of rare-event cost in the operational loss. Orientation estimation conditional on leakage requires inverse p resources, but leakage itself weighs the recovery objective by p. The resulting absolute-risk cap has no inverse p. It does not grant cheap relative estimation of W or a uniform recovery guarantee on the postselected leakage branch.

## Elementary necessity of paying the rare-event interface

Even granting more powerful calibration measurements cannot reveal W on a flag0-only calibration history: all such outputs are unchanged inputs. Restrict W to I and X, each with prior1/2. With N independent calls, the no-leakage event has probability (1-p)^N, independent of all calibration input/control choices. On that event the chosen decoder is common; averaging the leakage I/X channel has best Bell fidelity 1/2. The flag0 service can be perfect, so expected recovery regret is at least

    (p/2)(1-p)^N.                                    (4)

This is a lower bound even with coherent reference-assisted probes and adaptive control, provided each source call remains the channel (1), all N calls are counted, and no additional generator access is granted. For p=1/(N+1), this is order 1/N. Thus the worst-p 1/N risk scaling of (3) cannot be improved to a faster uniform order merely by assuming all compressed moments are known. Constant optimization and broader unknown nonflagged geometries remain open.

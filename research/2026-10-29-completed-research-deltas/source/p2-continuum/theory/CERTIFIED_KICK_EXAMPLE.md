# An evaluated, interval-enclosed continuum channel

This is a declared mathematical benchmark, not the P2 circuit. It closes evaluation for a small nonlinear continuum problem and tests full-input coherence and joint records. The separate oscillator example has stronger source-Hilbert scope but only floating compression diagnostics.

## Model and exact finite representation

Use dimensionless frequency/time, one source qubit, bath vacuum and rho(omega)=(21/10)exp(-omega) on omega>=0. With f_t=sqrt(rho)exp(i omega t), C(t,u)=(21/10)/(1-i(u-t)). Apply

    U1=exp[-i(1/2)X sin Phi(f_0)],
    U2=exp[-i(3/4)Z sin Phi(f_(3/5))].

These are specified finite-area kicks. They are not an uncharged approximation to a continuous waveform. Noncommuting source axes and field directions retain ordering and interference. Collection is explicitly E1=(3/5)I, E2=(1/4)I, with 3/20 unobserved. It is not inferred from rho.

For Pauli S, exp[-i theta S sin Phi(f)]=sum_n J_n(theta)(-S)^n W(inf). Keeping |n|<=8 in each kick gives 289 packets with alpha_nm=i(nf_0+mf_T), source matrix (-Z)^m(-X)^n, and coefficient J_n(1/2)J_m(3/4)exp[i nm Im C(0,T)].

The code replaces each J_n by the exact rational midpoint of 22 alternating Taylor terms and the next term. Terms decrease at these parameters, so half the next term bounds midpoint error. This error is charged.

For K, let a=theta²/[4(K+2)], q=theta/[2(K+2)]. A rational bound is

    tail_K(theta) <= 2(theta/2)^(K+1)/(K+1)! /[(1-a)(1-q)].

The absolute Bessel power series bounds J_n by (theta/2)^n/n! exp[theta²/(4(n+1))]. Use exp(a)<=1/(1-a), then a geometric factorial-tail bound. Adding retained midpoint errors gives e1,e2. The product map error is exactly bounded by

    epsilon=(1+e1)(1+e2)-1=8.734220304380286...e-10.

Its polar repair V(V†V)^(-1/2) is an isometric CPTP approximation with complete-output, arbitrary-reference half-diamond error <=2epsilon<1.747e-9. This uses a two-by-two input Gram, not the inverse of the 289-packet Gram. Record probabilities below directly enclose exact-model events from the unnormalized polynomial via the event-amplitude bound and do not use a floating polar inverse.

## Outward numerical evaluation

Packet norms, phases, signs, Bessel coefficients and exponents are exact rationals. Transcendentals use 48-digit Decimal intervals with directed basic arithmetic. Machin's formula and alternating arctangent remainders enclose pi. Range reduction modulo pi/2, with that enclosure, leaves arguments in [-1,1]. Horner-evaluated sine/cosine polynomials include rigorous factorial remainders. Correctly rounded Decimal.exp and Decimal.sqrt are enclosed with adjacent representable endpoints. Kernel sums and inclusion-exclusion therefore include arithmetic error.

For each physical record, transfer its polynomial probability interval p_V using

    max(0,sqrt(p_V)-epsilon)² <= p_exact
        <= min(1,(sqrt(p_V)+epsilon)²).

The receipt retains decimal-string endpoints and exact rational bounds. No quadrature convergence or Fock comparison certifies them.

## Results

For |0>, conservative rounded intervals are:

| Record | Exact-model probability interval |
|---|---|
| Neither | [0.6952296340,0.6952296371] |
| Only 1 | [0.1542934052,0.1542934066] |
| Only 2 | [0.0472082401,0.0472082409] |
| Both | [0.1032687175,0.1032687187] |

For (|0>+i|1>)/sqrt(2), neither-click becomes [0.5722791839,0.5722791866]. Basis-input probabilities alone would miss that coherence. Complete two-by-two effects and four input checks are saved. No physical bright/dark labels are assigned.

The first run took about 17 seconds in this environment. This is a small-instance observation, not a complexity theorem or a P2 solver cost. Larger action, continuous time and a full source oscillator can require many more packets.

Run `python code/certified_continuum_kicks.py` from the package root; only the Python standard library is needed. Its receipt hashes the source. The program asserts the conservative exact 2epsilon<2e-9; the tighter 1.747e-9 follows from the saved rational fraction and is separately checked in the independent review.

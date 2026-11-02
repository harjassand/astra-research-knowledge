# Exact full-sector one-photon rail channel

Fresh derivation, 2 Nov 2026. Analytic spectrum exact; numerical thresholds are diagnostics, not certified interval roots or exhaustive code optimization.

## Contract and failed escape

Input is the maximally mixed one-photon code across D identical thermal attenuators Phi_(eta,nu). It carries log2 D logical qubits per D physical channel uses with one photon total. ALL output total-photon sectors are retained. There is no postselection, backward success signal, sender amplification, or uncharged mixed seed.

Write G=1+(1-eta)nu, tau=eta/G, q=(G-1)/G, a=tau/(G-1), b=1-tau, and c_N=G^(-D)q^N. The loss-then-amplification Kraus representation gives, on total output photon N,

    Phi^tensor D(|i><j|)_N = c_N [a a_i^dagger a_j + b delta_ij I_N].

Let d_N=binom(N+D-1,D-1), d_(-1)=0. Bob's output has eigenvalue

    mu_N=c_N[b+a N/D], multiplicity d_N.

The reference-output state of the maximally entangled input has N-block

    J_N=c_N/D [b I_(D d_N)+a T_N],
    T_N=sum_ij |i><j| tensor a_i^dagger a_j.

Define V:R tensor Sym^N(C^D)->Sym^(N-1)(C^D),
V(|j> tensor psi)=a_j psi. Then T_N=V^dagger V and
VV^dagger=sum_i a_i a_i^dagger=(N+D-1)I.
Hence the complete eigenvalues are

    lambda_plus = c_N[b+a(N+D-1)]/D, multiplicity d_(N-1),
    lambda_zero = c_N b/D, multiplicity D d_N-d_(N-1).

At N=0 only the second eigenvalue occurs. This gives a positive, trace-preserving complete channel entropy calculation with no hidden erasure branch.

Set P_N=d_N mu_N and w_N=d_(N-1)lambda_plus/P_N. The block probability entropy cancels, leaving

    I_c = sum_N P_N { log2 d_N - h2(w_N)
                  -w_N log2 d_(N-1)
                  -(1-w_N)log2[D d_N-d_(N-1)] }.

Use the limiting convention w_0=0. Equivalent stable expression is used in full_rail.py.

## Diagnostics

For nu=1, zero crossings found numerically:

D=2: eta=.813953539505;
D=3: .817859102575;
D=4: .821245186753;
D=8: .830903130342;
D=16: .841571785554;
D=32: .852093444484;
D=64: .861806613931;
D=128: .870490557331.

These do not approach the primary certified non-Gaussian eta=.7841 result. Increasing D adds no demonstrated noise tolerance. This statement concerns this maximally mixed one-photon code only, not arbitrary inputs, higher photon shells, coherent superpositions of shells, or all-blocklength capacity.

For fixed G>1 and tau<1, concentration puts N approximately D(G-1), w_N approximately tau. The information has a negative contribution -(1-tau)log2D; the rest is O(1). Thus the large-D mechanism is asymptotically unfavorable even when all sectors, rather than only the one-photon sector, are retained.

## Primary channel representation and baseline

Mele et al., arxiv:2607.27449v1, Eqs15–18 give the loss/amplifier factorization and Kraus operators. Their appendix B supplies a finite-support, finite-cutoff certified witness at nu1,eta.7841 with I_c>=1.4312e-7. It is the relevant stronger direct thermal-link comparator, not the Gaussian hashing rate.

# Rare-sector recovery when experimental error is one fixed operator

Companion to `thermal_visibility.md`. Constructed 1 November 2026.

## 1. What changes, and what is credited

The lower bound in the companion uses a continuous but nonlinear action error. Here the experiment is separately qualified to implement ONE fixed real symmetric matrix B = H + E on every call, with ||E||op <= eta. Its linearity, reciprocity, stationarity and calibration bound are supplied instrument properties. Finite spot checks do not prove them globally. The result is useful only when such properties follow from the device architecture, a separately paid calibration, or a computational source. This note does not manufacture that qualification.

Polynomial spectral filtering, Gaussian range finding and singular-subspace perturbation are conventional machinery. The positive receiver below is explicitly credited to that machinery. The original synthesis in this investigation is its exact juxtaposition with the pinned Astra N1543 information bound and a thermodynamic task: error magnitude alone does not determine whether rare scientifically important sectors can be acquired.

Primary predecessor: Halko, Martinsson and Tropp, *Finding Structure with Randomness: Probabilistic Algorithms for Constructing Approximate Matrix Decompositions*, SIAM Review 53 (2011), 217--288, DOI https://doi.org/10.1137/090771806 ; public author version https://arxiv.org/abs/0909.4061 . Also compare Chen--Trogdon--Ubaru spectral quadrature and Amsel et al. structured learning cited in the companion. No claim of a new range-finding algorithm is made.

## 2. Exact source, input and output contract

Unknown H = 2 Delta I - Delta P on R^N, where P is an orthogonal projector of unknown rank r in {1,2}; N >= 3 and Delta > 0 are known. Each actual source call returns Bv exactly for the same symmetric B = H + E, where ||E||op <= eta <= Delta/4. An exact-action model for B is deliberate; independently noisy calls require the additional averaging budget in Section 8.

For failure budget delta in (0,1) and retained subspace tolerance epsilon in (0,1], the receiver returns the correct r and an explicit N-by-r orthonormal matrix Uhat. No later source call is needed for

    Z_r(b) = exp(-2b Delta) [N+r(exp(b Delta)-1)],
    U_r(b) = 2 Delta - Delta r exp(b Delta)/[N+r(exp(b Delta)-1)],
    rhohat_b = [I+(exp(b Delta)-1) Uhat Uhat*]
               / [N+r(exp(b Delta)-1)].

The first two formulas are exact when r is correct, because the two energies are a source promise. The third is a positive, normalized classical description of a density matrix. Delivering that description is not physical quantum-state preparation. Generic preparation from its explicitly stored vectors has O(Nr)-scale data and gate costs unless a separate state-preparation interface is available.

## 3. A fully explicit filter

By Weyl's inequality, B has exactly r eigenvalues in [Delta-eta, Delta+eta] and the remaining N-r in [2Delta-eta,2Delta+eta]. Define

    T = [(2Delta+eta)I-B]/(Delta+2eta),
    a = 2eta/(Delta+2eta) <= 1/3,
    h = 1/2-a >= 1/6.

The low-energy eigenspace of B has T spectrum in [1-a,1], while its orthogonal complement has T spectrum in [0,a]. Let PB be the low-energy spectral projector of B.

For odd m, define the binomial-majority polynomial

    q_m(t) = sum_{j=(m+1)/2}^m binom(m,j) t^j(1-t)^(m-j).

This is a degree-m polynomial with 0 <= q_m(t) <= 1 on [0,1]. Hoeffding's binomial tail bound gives

    ||q_m(T)-PB||op <= exp(-2m h^2).

All coefficients are rational when Delta and eta are rational. Applying q_m(T) to one vector takes m B-actions through ordinary polynomial evaluation. Integer coefficients in a power-basis expansion have O(m) bits, so the coefficient description itself is polynomial in m. Exact rational-action bit growth, vector arithmetic and evaluation precision are charged separately. The floating executable uses an equivalent Chebyshev representation and is a numerical diagnostic, not an interval-certified implementation theorem.

## 4. Random acquisition, including rank identification

Put t = sqrt(2 log(4/delta)). Choose integer s with

    a0 = sqrt(s)-sqrt(2)-t > 0,
    K = sqrt(N)+sqrt(s)+t.

Choose

    tau <= min(1/4, epsilon*a0/(4K)),
    m odd and m >= log(1/tau)/(2h^2).

Generate G with s independent standard real Gaussian columns and execute

    Y = q_m(T) G.

Perform a thin SVD of Y. Keep the left singular vectors whose singular values exceed 3a0/8; their number is rhat.

Standard Gaussian singular-value concentration gives, with probability at least 1-delta/2,

    sigma_min(PB G as an r-by-s matrix) >= a0,
    ||(I-PB)G||op <= K.

These follow respectively from sqrt(s)-sqrt(r)-t and sqrt(N-r)+sqrt(s)+t, each with failure at most exp(-t^2/2)=delta/4. The r <= 2 promise makes the displayed a0 uniform.

On this event write Y = M+W, with

    M = PB q_m(T)G,
    W = (I-PB)q_m(T)G.

The filter commutes with PB, so

    sigma_r(M) >= (1-tau)a0 >= 3a0/4,
    ||W||op <= tau K <= epsilon*a0/4 <= a0/4.

Weyl's singular-value inequalities give

    sigma_r(Y) >= a0/2,
    sigma_(r+1)(Y) <= a0/4.

The threshold 3a0/8 therefore identifies r exactly. Let Phat = Uhat Uhat* be the retained rank-r projector.

For completeness, a direct subspace proof avoids assuming a black-box perturbation theorem. The best rank-r approximation Y_r has residual at most ||W||, since M is a feasible rank-r approximation. Therefore

    ||(I-Phat) M|| <= ||(I-Phat)Y|| + ||W|| <= 2||W||.

The restriction of M to its row space maps onto ran(PB) with minimum singular value at least 3a0/4. Hence

    ||(I-Phat)PB|| <= 2||W||/(3a0/4) <= 2epsilon/3.

For equal-rank orthogonal projectors this is ||Phat-PB||op. In particular the simpler bound ||Phat-PB||op <= epsilon holds. This proves the whole acquisition event at probability at least 1-delta, with spare failure budget.

For fixed rmax=2 and chosen s = O(log(1/delta)), a0 is positive and the source-action cost is

    sm = O(log(1/delta) [log N + log(1/epsilon)
                        + log(1/delta)]),

at eta/Delta bounded by 1/4. More precisely use the displayed formulas; the simplified big-O is not a claim of sharp constants or confidence dependence.

Full-vector generation, readout and polynomial arithmetic cost O(Nsm), the thin SVD costs O(Ns^2+s^3), and retained output requires Nr numbers. Peak storage is O(Ns+s^2). The exact model does not hide these ambient-coordinate costs.

## 5. Calibration error and the actual true Gibbs state

The fixed calibration perturbation rotates the source subspace; its effect cannot be removed by more accurate numerical filtering.

Since B PB = PB B PB, multiplying H PB - PB B PB = -E PB by I-P gives

    (I-P)PB [2Delta I - B|ran(PB)] = -(I-P)E PB.

The bracket is positive with minimum eigenvalue at least Delta-eta. Therefore

    ||(I-P)PB|| <= eta/(Delta-eta).

The two projectors have equal rank, so

    ||P-PB||op <= eta/(Delta-eta),
    ||P-Phat||op <= eta/(Delta-eta)+epsilon.

Let x=exp(b Delta) and D=N+r(x-1). The true Gibbs state is rho_b=[I+(x-1)P]/D. Two rank-r projectors obey ||P-Phat||1 <= 2r||P-Phat||op. Consequently

    (1/2)||rho_b-rhohat_b||1
       <= r(x-1)/[N+r(x-1)] * [eta/(Delta-eta)+epsilon],

uniformly for every b >= 0 on the SAME acquired event. Cap the bound at one if necessary. For this exact two-energy family the calibration floor is independent of b after the thermal sector is occupied, because calibration changes the inferred vectors but the true energy levels are supplied exactly. It is not a general low-temperature stability theorem.

The exact half trace distance between two such represented states can be checked from principal angles: it equals (x-1)/D times the sum of the r sines of the principal angles between their subspaces.

## 6. Free energy, energy, Gibbs state and different temperature regimes

With F=-(1/b)log Z, compare ranks one and two from the companion. At x=N:

* The relative partition-function gap tends to 1/2.
* The absolute internal-energy gap tends to Delta/6.
* The free-energy gap is log(Z2/Z1)/b, asymptotic to Delta log(3/2)/log N, and therefore vanishes.
* The half trace distance between the rank-one and nested rank-two true Gibbs states is exactly x/[N+2(x-1)] - 1/[N+(x-1)], tending to 1/3.

For the last formula, the newly added vector u is the only positive eigenvalue of rho2-rho1: its probability increases from 1/(N-1+x) to x/(N-2+2x); all other probabilities decrease. At b=0 the state distance is zero. At b Delta=a log N, a<1, it is O(N^(a-1)); at a>1, it tends to 1/2. Partition functions retain a multiplicative degeneracy distinction at very low temperature, whereas the energy distinction goes back to zero and the state distinction survives.

Thus a constant-accuracy free-energy task does not inherit the companion's hard crossover claim. The intended precision must be stated. A state receiver and a scalar free-energy calculator require different information.

## 7. Robustness to a non-flat source and its unavoidable temperature bill

Suppose the actual H is Hc+R, Hc=2Delta I-Delta P, and ||R||op <= zeta. A fixed action bias of size eta gives total source-to-coarse perturbation eta+zeta, which must satisfy the filter separation condition. Rank still identifies the coarse sector, but exact thermodynamic formulas now describe Hc, not H.

Ordinary Gibbs variational inequalities give

    exp(-b zeta) Z_Hc <= Z_H <= exp(b zeta) Z_Hc,
    |F_H-F_Hc| <= zeta.

A dimension-independent state bound is

    T(rho_H,rho_Hc) <= min(1,b zeta/2).

Proof: quantum relative entropy satisfies

    D(rho_H||rho_Hc)+D(rho_Hc||rho_H)
        = b Tr[(rho_Hc-rho_H)R] <= 2b zeta T.

Quantum Pinsker gives each relative entropy at least 2T^2. For T>0, 4T^2 <= 2b zeta T, proving T <= b zeta/2; T=0 is immediate. The natural-log convention is used throughout. This is an ordinary entropy-continuity argument, not a new inequality claim.

It also gives

    |U_H-U_Hc| <= zeta + Delta min(1,b zeta/2),

because Hc centered at 3Delta/2 has norm Delta/2. A sharper tanh bound may follow from the optimal symmetrized-divergence/variation inequality; it is not needed or asserted here.

At the rare-sector crossover b Delta=log N, state or energy accuracy epsilon generally requires zeta=O(epsilon Delta/log N). Flatness protected by an actual symmetry could supply a stronger promise; generic small perturbations do not. The calibration and source-width terms must be kept separate.

## 8. Independent per-call errors: an explicit but more expensive fallback

If source calls instead give independent unbiased Gaussian vectors

    y(v)=Bv+xi,    xi ~ N(0, sigma^2 I_N/N),

then averaging M repeated calls to each of the N standard basis vectors constructs a matrix Btilde. Symmetrize it. Before symmetrization its noise entries are independent N(0,sigma^2/(NM)); symmetrization cannot increase the operator norm. A standard Gaussian matrix norm bound gives

    ||Btilde-B||op <= (sigma/sqrt(M))
                        [2+sqrt(2log(1/delta)/N)]

with probability at least 1-delta. Taking M at least the square of this bracket times sigma^2/eta_stat^2 earns a stationary symmetric representation within eta_stat. All NM native calls, O(N^2) readout/storage, and eigensolver arithmetic are paid. The positive filter can then be applied locally, but it does not erase this acquisition cost.

This fallback establishes a constructive iid-noise receiver without reusing the exponential lower bound outside its error model. Better matrix-free stochastic acquisition may exist; no optimal iid-noise complexity is claimed. If only scalar energy measurements are available, this full-vector construction does not apply.

## 9. Interpretation

The same pointwise budget eta||v|| permits exponentially hard acquisition when experimental errors can hide directions nonlinearly, while a qualified stationary symmetric perturbation admits conventional polynomial filtering with logarithmic-in-N source-call dependence for the promised rare-sector family. This is a precise information contrast, not proof that an invented learner outperforms an equally informed conventional method. In the positive model, the conventional receiver wins and is the construction we should use.

The surviving research question is broader: what experimentally checkable consistency, locality or conservation structure admits acquisition of rare task-relevant sectors without demanding whole-operator accuracy? The present note answers one finite explicit instance and marks exactly where source flatness, calibration and quantum output costs enter.

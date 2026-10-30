# Scoped independent review: centered-noise O(delta eta) refinement
2026-10-30. Reviewer: `challenge_live_busy_energy`.

## Verdict and binding source
**Scoped PASS** for section 6's refined noise bound

    +/- N_u*G_delta <= C delta eta N G_delta,

under the same bounded-body joint-cb incident budget and physical support convention as the accepted coarse theorem. This strengthens ONLY the noise sensitivity. The previously frozen coarse receipt is unchanged.

Exact author source, copied verbatim into `reviewed_sources/`:

`producer-workspace/SINGLETON_FULL_HILBERT_BUSY_MOMENT.md`

SHA-256 `4ef29910c0db77db185d052d27194a7b9441a6f87b7b564bda1f63855602708b`.

This receipt does not newly certify the permanent-program extension or the operational/readout composition in later sections. Those are unnecessary for the refinement and remain separately scoped.

## 1. Centering: exact condition and norm cost
Let N*=sum_Z N_Z* be the SAME physical perturbation being estimated, with HP local pieces on at most q system sites and the retained bath. The total must annihilate identity:

    sum_Z N_Z*(I)=N*(I)=0.

This holds for a perturbation which is the difference between two actual unital Heisenberg generators. The per-site absolute cb-norm budget implies absolute norm convergence of the nonempty-system-support sum for finite N. Define

    A_Z=N_Z*(I)=A_Z†,
    M_Z*(O)=N_Z*(O)-{A_Z,O}/2.

Then M_Z*(I)=0, M_Z* is HP, its system support remains Z, and

    ||M_Z*||_cb <=2||N_Z*||_cb.

The correction terms sum to zero, so sum_Z M_Z*=N*. Individual M_Z* need not be CP or generators; no such claim is required.

Bath-only terms must either be separately identity-annihilating, in which case they act as zero on the system observable, or be included consistently in the same zero-total-identity centering. One cannot exclude a nonunital bath-only contribution from an identity cancellation and still claim that the remaining centering preserves the total. The source's stated physical perturbation/nominal-bath convention has the required accounting; this sentence makes that condition explicit rather than extending the noise model. The author explicitly confirmed that nominal bath evolution is separately CPTP/identity-annihilating, all bounded pieces being centered form the same trace-preserving difference with an absolutely convergent incident-norm sum at fixed N, and no cancellation with an uncontrolled unbounded bath term is assumed.

## 2. Exact bounded cone, uniformly in delta
Let C_delta(O)=Y_delta† OY_delta, with the fixed-depth circuit of exp(delta X_h). Each X_h is a bounded system operator of fixed support; the overlap coloring has fixed depth and bounded incidence. For a centered local piece put

    Mtilde_Z(delta)=C_delta^{-1} M_Z* C_delta.

Disjoint system gates cancel by locality/bimodularity. After each layer only a bounded enlargement of the system support occurs, so the exact reduced expression contains at most K_q local congruence gates and their inverses, where K_q is independent of N and of the choice of distant partner sites. Choose the structural cone once, independently of delta. All bath factors are retained; the gates have no bath support, so sharing the same bath does not obstruct cancellation.

For one gate Q_h(delta)=exp(delta X_h), its congruence is exp(delta M_Xh), where M_Xh(O)=X_h O+OX_h and

    ||M_Xh||_cb<=2 C_X.

Both signs of the local congruence parameter obey the conservative bound exp(2delta C_X). Differentiating the finite reduced expression, with at most 2K_q factors around M_Z*, therefore gives, for 0<=delta<=delta0,

    ||d Mtilde_Z(delta)/d delta||_cb
      <= 4K_q C_X exp(4K_q delta0 C_X) ||M_Z*||_cb.  (1)

Harmless changes in K_q cover the fixed physical-to-forest support enlargement. Crucially (1) is a finite local-cone derivative, not a derivative of a global norm exp(O(delta N)). Its constant is independent of N, epsilon, and delta in the declared interval, with the apparatus and witness fixed.

## 3. Vanishing at zero and positive pullback
At delta=0, C_0=Id and Mtilde_Z(0)(I)=M_Z*(I)=0. Integrating (1) yields

    ||Mtilde_Z(delta)(I)||<=C_q delta ||M_Z*||_cb.

The output is Hermitian because each map in the expression is HP. Hence

    +/- Mtilde_Z(delta)(I)<=C_q delta ||M_Z*||_cb I.

Pull this inequality through the POSITIVE congruence C_delta. This gives exactly

    +/- M_Z*(G_delta)
       <=C_q delta ||M_Z*||_cb G_delta.            (2)

No identity-annihilation is asserted for Mtilde_Z at nonzero delta, and no unital-congruence lemma is used. The output vanishes only at delta=0; its derivative is what supplies the missing factor delta.

Summing (2), using the factor-two centering cost and

    sum_Z ||N_Z*||_cb
       <=sum_i sum_{Z containing i}||N_Z*||_cb
       <=n_system eta<=C_site N eta,

earns the stated O(delta eta) bound. Time-dependent partner choices are harmless because the argument is pointwise in time with uniform q and incident norm budget. It is representation-free and reference/common-bath stable under the joint cb convention.

## 4. Consequence and limits
Combining ONLY this refinement with the already accepted constant-singleton native drift changes its source coefficient from

    C_native delta epsilon^2+C_noise eta

to

    delta(C_native epsilon^2+C_noise eta).

The entropy contraction rate and maskwise barrier are unchanged. Thus the BUSY-tail source/barrier ratio becomes O(epsilon^2+eta), with a coefficient independent of delta in its allowed interval. This does not alter any hardware rate, imply all controllers are idle, or supply a physical output/readout interface.

I reran a local COPY of the author's 16-dimensional noncommuting-witness/shared-bath diagnostic. Its 20 drift checks and five noise-scaling checks pass. The centered relative noise norm divided by delta lies approximately between 2.944 and 3.062. These are supporting finite algebra diagnostics only; the proof is the exact centering, finite-cone derivative, and positive pullback above, not the chosen numerical bound.

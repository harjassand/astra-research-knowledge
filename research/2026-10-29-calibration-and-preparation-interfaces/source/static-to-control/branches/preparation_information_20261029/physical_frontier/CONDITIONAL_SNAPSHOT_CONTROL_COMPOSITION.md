# Arbitrary snapshot information and retained history: conditional TV composition

29 October 2026. New physical-frontier consequence theorem.

**Dependency update:** Section 7 instantiates this composition proof with
the completed, independently reviewed stronger transition theorem. Its
native snapshot-memory consequence is established at that theorem's
scope. Sections 1--6 retain the generic conditional argument and the
valid safe interpolation bound. The reviewed initial version is saved
as `reviewed_versions/CONDITIONAL_SNAPSHOT_CONTROL_47bee884.md`.

The analytic estimates in Section 1 are EXPLICIT ASSUMPTIONS for this
construction. This note does not prove the kinetic Schauder, paraproduct
or static-to-negative-norm estimates being developed elsewhere.

## 1. Transition and initial-preparation assumptions

For fixed native bath, dimension and torus, let F,G be position forces
bounded by A. Controls add through the same noisy momentum force port
and satisfy |u(t,z)|<=B. Assume the native transition kernels obey

    sup_(t,z,u: |u|<=B)
       TV(P_(F+u)(t,z;t+h),P_(G+u)(t,z;t+h))
                                      <=epsilon(h;eta). (T)

The SAME bounded Borel Markov field u is used on both sides. A currently
proposed estimate is epsilon(h;eta)<=min(1,C_tr eta h^(-5/8)) for
0<h<=h0, with eta the declared kinetic C^(-1/4) discrepancy. A stronger
verified estimate may be substituted. This theorem uses only (T).

Let the actual JOINT initial laws of physical state and retained history
be Lambda_F and Lambda_G, with TV discrepancy <=epsilon_init. Common
independent controller initialization reduces this to the state TV error.
A retained source-correlated calibration or warm-up record needs this
joint bound, not merely matching record marginals.

## 2. Current-state snapshot experiment

Fix 0=t0<t1<...<tm<=T. At snapshot i, draw a report from an arbitrary
common kernel

    K_i(da | H_(i-1),Z_(t_i))

into any standard Borel output space. The kernel may be noiseless,
discontinuous, arbitrarily sensitive, or vary with the compared source
family. It must be the SAME operation under the two hypotheses and use
only the current state and previously retained reports. Exact full-state
snapshots are included. Retaining all earlier reports is allowed.

On the next interval, the program selects a jointly Borel field
u_i(H_(i-1),t,z), bounded by B. Its dependence on current native state
is Markov during the interval. Histories and branch fields need not be
finite or countable. Their induced kernels must be measurable; an
arbitrary nonmeasurable selection is not a defined experiment.

No extra between-snapshot path record, accumulated force integral,
continuously reported command trace or hidden event-trigger time is
silently included. Those are different observation interfaces.

## 3. Augmented-kernel proof

Retain an augmented record R_i containing all exact snapshot states,
all reports and the initial history, even if the actual sensor reports
less. The program's available history is its prescribed projection.
Given a common previous record r with current state z and history h,
one step draws z' from the controlled transition with field u_i(h), then
draws a from K_i(.|h,z'), and appends both to the record. Call the resulting
kernels M_i^F,M_i^G. Data processing and (T) give

    sup_r TV(M_i^F(r,.),M_i^G(r,.))<=epsilon(Delta_i;eta),
    Delta_i=t_i-t_(i-1).

For any probability laws mu,nu and kernels M,N,

    TV(mu M,nu N)<=TV(mu,nu)+sup_r TV(M(r,.),N(r,.)).

This follows by inserting nu M and applying common-kernel contraction.
Iteration proves the complete joint discrete-record guarantee

    TV(Law_F R_m,Law_G R_m)
      <=min{1,epsilon_init+sum_i epsilon(Delta_i;eta)}.   (1)

Every observed transcript, retained memory, decision or randomized output
computed from this record satisfies the same bound. No alphabet size,
sensor continuity or enumeration of histories enters. The supremum over
all admitted programs may be taken AFTER choosing one candidate G.
The statement is joint DISCRETE-record TV, not continuous-path TV.

## 4. Time and observation budgets

For Delta_i<=h0 the proposed safe estimate gives

    TV<=epsilon_init+C_tr eta sum_i Delta_i^(-5/8).      (2)

Equal gaps T/m give C_tr eta T^(-5/8)m^(13/8). These are sufficient
error budgets, not optimal sampling-complexity or necessity claims.
If epsilon(h;eta)<=C_tr eta h^(1/16) is instead established, equal gaps
give C_tr eta T^(1/16)m^(15/16). Only verified analytic bounds may be used.

A longer interval can be divided into equal mathematical substeps of
length <=h0, applying transition composition before the actual sensor.
No physical observations are added at those analytical substeps.

An elementary supplement avoids a spurious small-gap divergence.
For the same start and same u, |F-G|<=2A gives full-segment path KL
<=A^2h/(gamma tau), hence endpoint TV<=C_short sqrt(h), where
C_short=A/sqrt(2gamma tau). Therefore the safe bound implies

    epsilon(h;eta)<=min{1,C_tr eta h^(-5/8),C_short sqrt(h)}
       <=min{1,(C_tr eta)^(4/9) C_short^(5/9)}=:epsilon_*.

The last inequality follows by a weighted geometric mean whose powers
of h cancel. With at most m observation intervals in total time T,
subdivision into pieces of length <=h0 requires at most m+T/h0 pieces.
Thus a sufficient uniform alternative is

    TV<=epsilon_init+(m+T/h0)epsilon_*,                  (3)

clipped at one. This is weaker in eta than (2) for fixed positive gaps,
but allows arbitrarily short gaps with a fixed finite snapshot budget.
At a zero gap the physical identity kernel is common and its error is zero.

The same argument allows the NEXT snapshot time to be chosen from the
already charged history at the previous snapshot: include current time
in the augmented state and use a uniform per-step ceiling. At most m
reports, total time T and (3) suffice. Stops use a common absorbing dummy
kernel. Timing triggered by continuously observing an unreported path
is excluded; its timestamp can itself carry additional information.

## 5. Conditional static-to-record corollary

If separately proved analytic bounds give

    eta<=C_stat(sqrt(s)+e^(1/4))^(1/[12(d+1)]),
    epsilon_init<=sqrt[s/(4gamma)]+C_init e^(1/4),

with true physical entropy upper bound s and full-position W1 fit e,
then substitution in (2) gives

    TV<=sqrt[s/(4gamma)]+C_init e^(1/4)
       +C_tr C_stat(sqrt(s)+e^(1/4))^(1/[12(d+1)])
                                      sum_i Delta_i^(-5/8).             (4)

The exact norm, domain and constants of those analytic hypotheses remain
obligations of their source proofs. Equation (3) offers the alternative
uniform per-piece exponent 1/[27(d+1)] after the same substitution.

## 6. Physical information and service preparation

This theorem permits exact snapshots as mathematical kernels; it does
not purchase instrument precision or implement noncomputable protocols.
It needs the same calibrated state-sensing operation on both models.
Measuring two different native force functions is not automatically one
common state kernel.

The static bridge needs an UPPER bound on actual physical entropy, the
specified bath/source domain, and adequate complete-configuration data.
Visible time symmetry or an entropy lower certificate is insufficient.
The finite entropy-upper acquisition contract is treated separately.

If U is selected from calibration data, genuinely fresh independent
baseline service preparation permits conditioning on that data and
using the population initial-state bound. Otherwise the actual joint
state/history approximation must be supplied. For a shared calibration
record with a good event of probability >=1-delta_cal, a uniform
conditional service bound epsilon yields joint record/service error
<=delta_cal+epsilon. This does not create a reset or independent samples.

The stronger analytic premise makes finite alphabet restrictions
unnecessary: arbitrary current-state snapshot information can be
retained and used causally. The one-bit fine-PATH classifier is outside
this interface because its information comes from an entire
between-snapshot trajectory, not one current state.

## 7. Established consequence of the reviewed stronger transition theorem

Completed dependencies, read at their new load-bearing statements:

    QUANTITATIVE_CONTROL_FROM_STATIC_INFORMATION.md
    c5bd15e499d750d85b56f3e26a52fe95626e74be6f1e0307c6da7afcafb1d3fc
    Section 7 equation (13), with source/norm definitions in Sections 1--2.

    alternative_frontier/QUANTITATIVE_CONTROL_INDEPENDENT_REVIEW_AND_STRENGTHENING.md
    905142e9aaa4dca0f7ce77efe65a0322064e6ede6bfb7304a75db7692900ef66
    Sections 3 and 6: bounded-Borel limits and endpoint extraction.

They establish, uniformly over start time, state and every common bounded
Borel Markov field u,

    TV(P_(F+u)(t,z;t+h),P_(G+u)(t,z;t+h))
       <=C_imp eta h^(1/16), 0<h<=h0<=1.                (12)

Here eta=||F-G||_(C_B^(-1/4)) uses the fixed kinetic anisotropic Besov
norm, momentum weight one and position weight three. C_imp,h0 are the
specified analytic constants; no control derivative ceiling is added.
This is a completed theorem dependency, not a proposed assumption.

Equation (1) proves the native snapshot-memory consequence:

    TV(complete joint discrete record)
      <=min{1,epsilon_init+C_imp eta sum_i Delta_i^(1/16)},
      for Delta_i<=h0.                                (13)

It holds for arbitrary common standard-Borel current-state sensor
kernels, including exact states and source-varying kernels, retaining
the full report history. Every history-selected bounded Markov branch
field is covered. One selected candidate serves the entire program
class; finite alphabets or a finite branch list are unnecessary.

Each short transition costs at most C_imp eta because h<=h0<=1.
Partition longer intervals as above. For at most m snapshot intervals
within time T, including report-driven scheduling with arbitrary
short gaps, this gives

    TV<=min{1,epsilon_init+(m+T/h0)C_imp eta}.            (14)

A factor h0^(1/16) may multiply the final term for a slightly stronger
bound. No minimum gap is required. Next times must still be chosen
from previously charged reports; continuously path-triggered timestamps
are a different interface. Growing snapshot counts pay the displayed
product even when the final retained state is small.

The completed force-information construction used by the root theorem
supplies E0<=sqrt[s/(4gamma)]+L(e)/2 and
eta<=C_force[sqrt(s)+L(e)]^(1/[12(d+1)]), with its explicit L1 density
bound L(e)=O(e^(1/4)). Under common independent service initialization,
epsilon_init=E0, so (14) becomes

    min{1, sqrt[s/(4gamma)]+L(e)/2
       +(m+T/h0)C_imp C_force
                          [sqrt(s)+L(e)]^(1/[12(d+1)])}. (15)

The joint-preparation qualification after data-dependent model selection
is unchanged. A finite physical entropy-upper acquisition contract is
provided in `FINITE_PHYSICAL_ENTROPY_UPPER_ACQUISITION.md`.

The analytic constants have not been instantiated numerically. These
are quantitative rates in specified finite constants, not an already
calibrated numerical stopping rule or executed physical acquisition.
Source entropy and position fit are bounded only after their warranted
acquisition contracts; no native source was sampled. The fine-PATH
one-bit counterexample remains outside this snapshot law.

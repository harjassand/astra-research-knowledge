# Independent audit: complementary actual infinite-composition trace

Reviewed 2026-10-30. **Pass, within the stated first-residual-exit scope.** Unlike the earlier controlled projected trace, this result uses the actual hard-network rates at every A/C composition. It supplies neither compactness of the residual target nor global recurrence by itself.

## Exact residual and head computation

For g(N)=4 floor(N/3)+(N mod 3), g(N)-g(N-3)=4. Thus clearing and fast conversion preserve s=B-g(N). The three residue cases give immigration increment -1 exactly at N=2 mod 3, and activation increment +1 exactly at N=0 mod 3; all other enabled increments are zero. Activation remains disabled at A=0, including N=0. The script respects all A/C enabling conditions, and B factors are positive for sufficiently large s.

Re-ran `check_composition_head_exit_degrees.py`; output matches `COMPOSITION_HEAD_EXIT_DEGREES.json` byte-for-byte. For K=8 there are 45 source probes; the maximal up degree is -1 and maximal neutral-tail degree is -3.

The underlying exact positive-Schur calculation is valid. Initial head rates have degrees 0, 1, or 4, with strictly positive leading coefficients precisely on the encoded enabled channels. Elimination uses positive sums and products divided by the sum of current outgoing rates, discards self returns, and reconstructs each denominator from its remaining outgoing rates. Consequently max-plus degree propagation has no hidden cancellation. Each source probe starts with a rate-one edge into its queried state, and its final edge rate to an absorbing label is exactly the corresponding absorption probability. Multiple original channels to the same target add positively.

Every head state reaches a down exit within at most three consecutive immigrations. At fixed head width total rates are at most C s^4 and immigration rate is exactly one. Conditional probability of the prescribed sequence is at least c s^-12; each holding mean is at most one. Repeated blocks therefore prove the stated O(s^12) stopping-time bound independently of the Schur exponent calculation.

## Exact infinite-composition descent

The full fast conversion rates are exactly (B)_4 times the conservative shell rates in the previously audited killed-shell theorem. Actual clearing is exactly (B)_4(A)_3. Thus time scaling gives

    sup_A E tau_clear <= C N^-9/4 /(B)_4

for N>=9, with no additional composition assumptions. The weaker statement for all N>=3 is also valid after covering finitely many small, transient shells.

Before a birth, N and B are fixed, and immigration plus activation intensity is 1+AB<=1+NB. One may construct the competing birth event as a state-dependent killing clock on the fast/clearing shell process. Its probability before clearing is bounded by its integrated hazard on that shell, hence by (1+NB) E tau_clear. Since B is large, this is <=C B^-3 N^-5/4. The actual stopped time is bounded by tau_clear, giving <=C B^-4 N^-9/4. No equilibrium, mixing, or independence of composition and the birth clock is assumed.

On paths with no birth, clearing sends (N,B) to (N-3,B-4) and leaves s fixed. At each successive stage the absorption bound is uniform in its random starting composition. Summing these conditional bounds over the decreasing N sequence, then bounding by the full convergent sums, proves the uniform O(s^-3) birth risk and O(s^-4) time to birth or head. This remains uniform even when the initial N is arbitrarily large.

For each finite initial N the no-birth descent visits only finitely many finite shells. A neutral birth restarts the same calculation at a finite new N and the same s; its conditional probability is bounded by p_s=C s^-3<1. Therefore the number of such restarts is geometrically bounded, even without independence. There is almost surely no infinite sequence of restarts, and no explosion inside an attempt. This closes the tail estimate without presupposing nonexplosion of the unrestricted physical chain.

## Renewal, factorial trace, and remaining scope

Head-to-tail probability is O(s^-3), tail-to-head probability is at most one, and each stopped piece has the established finite mean. The renewal inequalities consequently yield uniformly finite residual-exit time, O(s^12) mean, and O(s^-1) probability of an up exit. The same reasoning prevents explosion before that exit.

At exit the residual is precisely s+1 or s-1. For phi(s)=exp(ds) Gamma(s+1)^alpha, the exact two ratios are exp(d)(s+1)^alpha and exp(-d)s^-alpha. Therefore the stated contraction tends to zero for every fixed d and 0<alpha<1.

No A/N lower bound is used anywhere in this proof. The target s below a fixed threshold is nevertheless noncompact, and this trace alone does not establish global physical recurrence or compatibility with the other residual certificate. Those remain separate coupling obligations, correctly retained in the source.
380d315c69cb710b92137c3a601c8bc1a3907127335d08699a5d5ff72f810e15  chemical_joint_shell_20261030/COMPLEMENTARY_ACTUAL_COMPOSITION_TRACE.md
38ec73185f8cd4614d7e86e9a32e46ceba4716b0b3d5a099db50b34e703a6843  chemical_joint_shell_20261030/check_composition_head_exit_degrees.py
c2bcf271c89adc3de57f2aeb1666d3caf6ee4d5bcf18a99b4c7995b4504f3f95  chemical_joint_shell_20261030/COMPOSITION_HEAD_EXIT_DEGREES.json

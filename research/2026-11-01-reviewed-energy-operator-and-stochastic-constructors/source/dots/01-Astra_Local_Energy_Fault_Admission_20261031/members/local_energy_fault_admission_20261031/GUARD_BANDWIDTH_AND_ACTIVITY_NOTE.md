# Guard cooling bandwidth is not the same resource as emission activity

31 October 2026. Separate candidate cost note, not an amendment to the frozen admission theorem or compiler. Applies to the declared loss/injection model, including the proposed operator-valued shared-spectator extension. It does not identify excitation number with thermodynamic energy.

## 1. Exact balance

Let N=sum_i n_i, and let J_loss,J_inj count the actual canonical guard loss and injection jumps during [0,T]. All actual real occupation-controlled system/bath interactions, bath-only Hamiltonians and number-conserving hopping commute with N. Intended system-only gates and instruments also preserve N. The loss and injection adjoints give

  d E[N]/dt = -sum_i lambda_i E[n_i] + sum_i a_i E[1-n_i].

Integrating their actual jump intensities proves

  E[J_loss] = E[N(0)] - E[N(T)] + E[J_inj],
  E[J_inj] <= a n T,
  E[J_loss+J_inj] <= E[N(0)] + 2 a n T.

These are expectation identities/inequalities for arbitrary finite guard/system/spectator correlations and initialized Markov fields. They do not assert a classical occupation trajectory for a coherent guard state. The actual jump-record count is well defined in the specified dilation. If a_i vary, replace a n T by integral sum_i a_i(t) dt.

## 2. A full count MGF

For u>=0 let W=exp(uN), and tilt BOTH types of jump by exp(u). The Hamiltonian contribution to the tilted adjoint on W vanishes. At a loss jump, lowering N contributes exp(-u), exactly cancelling the counting tilt; hence its entire tilted dissipator contributes zero. At an injection jump, raising N contributes exp(u), so its tilted adjoint contribution is

  a_i (exp(2u)-1)(1-n_i) W
  <= a_i (exp(2u)-1) W.

Therefore the positive non-trace-preserving tilted evolution obeys

  E exp[u(J_loss+J_inj)]
   <= Tr[exp(uN) rho_G(0)]
      exp[a n T (exp(2u)-1)].

W>=I supplies the final count inequality. System/reference/spectator registers are included by identity. Exact prescribed system-only instruments preserve W; outcome records may be retained. A guard-creating operation or modified counting convention would require a new term and is not covered.

For n finite, Tr exp(uN)rho<=exp(un), so one may derive explicit Chernoff caps. The tighter initial moment is not automatically acquired from an unknown state. In particular cold N=0 removes the initial factor, but no cold assumption is inserted into the arbitrary-input theorem.

## 3. What this does and does not save

The mean and MGF do not grow with lambda when injection rates are held fixed. Thus a high guard cooling bandwidth need not entail lambda*T physical guard emissions per site in this MODEL. This is distinct from the all-selected fault-amplitude admission, and does not turn an expected jump count into a simulator gate count.

Loss engineering, control bandwidth, injection suppression, routing and observation costs remain physical resources. N is an occupation/charge operator, not a supplied energy Hamiltonian. The formulas are not heat, power or entropy-production bounds without an additional physical identification and bath model. An arbitrary spectator can exchange other forms of energy even when the counted guard activity is low.

At fixed nonzero thermal occupation, increasing a system-bath coupling often increases excitation and relaxation together. If a scales with lambda, both the above activity and the admission factor c g(1+a tau)/(gamma lambda) reflect that cost. In particular the latter contains a nonvanishing term when a/lambda stays fixed and c,tau stay fixed. Fixed a while lambda increases must be earned through the actual temperature, filtering or independent injection mechanism; it is not a free hardware rescaling.

No experimental mechanism or practical operating regime is supplied by this note.

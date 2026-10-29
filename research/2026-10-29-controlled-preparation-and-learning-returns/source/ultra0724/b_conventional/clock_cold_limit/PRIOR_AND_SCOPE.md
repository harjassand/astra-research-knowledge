# All-cold extension: comparator, costs and scientific boundary

29 October 2026. This is a NEW all-low-temperature continuation. The old
polynomial-window theorem is independently accepted/frozen and is not
retrospectively widened. The new proof and circuit also received root's
independent whole acceptance at their precise mathematical scope.
No quantum state, model case, parameter grid or trajectory is run.

## 1. What is different from raising a perturbative order

The new route uses the exact product-vacuum ground flow and a full operator
inequality. It retains all excitation sectors, rather than acquiring better
approximate number conservation. In the KMS parent, imaginary-time factors
cancel to a CP sech average. Order preservation gives a temperature-
UNIFORM lower bound by the excitation count, even though the averaged
parent can spread farther as t grows.

The new product-coercivity lemma pays that growing range: fixed-gap spectral
flow plus the vacuum-CP martingale turns its weak perturbation into a small
RELATIVE defect term with polynomial locality costs. Heated parent terms
are polynomial(t)exp(-t/4), so they pass one fixed all-real-T threshold.
The exact source Clifford/Pauli/clock symmetries are not required by this
new product-coercivity lemma; only its stated product vacuum, form bound
and spatial interaction hypotheses are used.

The resulting conditional sampler has a constant parent gap for all
sufficiently large t at ONE fixed sufficiently small lambda. Its conservative
mixing bound O(nt+log(1/epsilon)) is slower in volume than the old window's
O(log(n/epsilon)), but its full circuit work is still polynomial(n,t,1/epsilon).
There is no uniform-in-t finite SW order or an uncharged infinite-order
dressing. The physical temperature may tend to0 without retuning lambda.

## 2. Strongest controlling ordinary methods actually checked

The earlier packet's full primary intake of Ding--Li--Lin2404.05998,
Smid--Meister--Berta--Bondesan2510.04954, Zhan et al.2503.15827 and ADHH
remains applicable. Exact KMS completion, oscillator proofs, ground cooling,
local normal forms, filtered Hamiltonian simulation and quasilocality are
all strong established tools, not claimed inventions.

New primary checks for this wider question:

* [Yarotsky, math-ph/0412040](https://arxiv.org/pdf/math-ph/0412040),
  Theorems1--2, condition(6) and the start of Section3, supply strong
  relatively-bounded product/classical ground-state stability methods. The
  displayed setup is translation-invariant, finite-range, and even permits
  infinite-dimensional sites. The local Hilbert-space dimension is therefore
  not an excuse to assume poor constants. We do not import a finite-range
  theorem for the increasingly spread parent. Our actual all-cold gap proof
  spells out its quasilocal/spatial and polynomial-scale extension directly.
* [Rouze--Stilck Franca,2610.03578](https://arxiv.org/html/2610.03578),
  Theorem6.1 and Lemma6.2, already provide a powerful noncommuting block
  heat-bath/QBP perturbation theorem. Its displayed threshold is c/beta,
  with c itself allowed to depend on beta and fixed block data; its local
  comparison assumes beta delta<=1. On-site-field-uniform constants do not
  turn this into a fixed-lambda all-beta promise. Their one-dimensional
  any-finite-temperature result is broader in Hamiltonian class and faster
  in volume, but does not give a polynomial-beta any-dimension product-phase
  construction with this fixed-coupling contract. We read these governing
  scopes, not just their title/preview, and do not infer their general method
  cannot be improved with equally informed new estimates.

Ordinary BMNS exact spectral flow and NSY LR/quasilocal-map methods used in
the frozen stability package are explicitly the proof primitives. The
operator-order positivity of sech averaging is elementary Fourier analysis.
Our exact simulator implementation uses ordinary LCU, Hamiltonian simulation
and reset ancillas. An equally informed competitor given these new bounds
can use the same or better circuit primitives. No practical or quantum-vs-
classical advantage, or historical novelty, is certified.

## 3. Inputs and complete resource gates

The actual input is the native bounded-range local Hamiltonian list, its
known classical syndrome signs, fixed geometry bounds, and a qualified
small lambda. The exact ground-flow unitary is compiled from the supplied
uniformly gapped path; FLOW_CIRCUIT.md pays its filter, coefficient quadrature,
path discretization, real-time simulation and inverse. It is not an acquired
eigenbasis, assumed Gibbs state, uncomputed envelope or initial-overlap oracle.

The parent similarity and the parent bootstrap spectral flow are proof-only;
neither is simulated. The actual sampler keeps the exact KMS heating and
coherent correction, and uses the earlier explicit finite band/LCU/reset
receiver with its longer update time. No exponentially unlikely successful
postselection is used. Its slow stated work dependence is polynomial in t,
NOT in log(t) or merely the binary length of the inverse temperature.

The new lambda_prod and T0 are computable fixed constants from the stated
norm/filter majorants, but UNEVALUATED for the old literal clock recipe.
The native SW catalogue is no longer required. No numerical native gate,
actual quantum state, practical precision budget, quantum device, physical
bath or finite-coupling hardware realization is acquired. There is no new
measured computation time to report; this continuation is an analytical
construction. The old .03918s scalar receipt is neither rerun nor relabeled
as all-cold state preparation.

Full source-syndrome sampling remains separate. Its correct weights include
the ENTIRE excited-clock trace. The new theorem only prepares conditional
clocks once s is supplied. Any composition with root's full thermal-weight
initializer needs that initializer's independent admission and compatible
fixed gates. No native Davies memory lifetime, arbitrary Hamiltonian-error
finite-T stability, or hardware preparation follows from this packet alone.

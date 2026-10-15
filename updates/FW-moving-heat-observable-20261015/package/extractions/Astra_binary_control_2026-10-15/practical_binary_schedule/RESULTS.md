# Binary schedules: a sharp anchor obstruction and a conditional recovery primitive

Status: exact mathematical partial results and reproducible synthetic algebra. No complete polynomial-time acquisition algorithm, practical finite-noise guarantee, physical demonstration, or superiority to measured-model fitting is established.

Model: g(S)=f0-f(S)=a_Sᵀ(I+B_SS)^−1 1, B_ii=0. Baseline and singletons identify f0 and a. All subsequent ranks concern B with a held fixed. All generic statements exclude rational denominators and finitely many nonzero polynomial conditions. The ambiguity B ↦ diag(a)^−1 Bᵀ diag(a) preserves every response; full Jacobian rank does not remove this discrete ambiguity.

## 1. Exact five-node Jacobian witness

For S, write v=(I+B_SS)^−1 1 and u=(I+B_SS)^−T a_S. Then

∂g(S)/∂B_ij = −u_i v_j for i,j∈S, and zero otherwise.

Take two anchors {0,1}; measure every S containing at most two nonanchors. For five total nodes, the exact finite-field witness in rank_witness.json has a 20×20 Jacobian minor equal to 473745 modulo the prime 1000003. The file supplies a, B, the ordered row subsets, and the ordered directed-edge columns. certify_structure.py recomputes it using integer modular Gaussian elimination, including nonsingularity checks on the required inverses.

This is not merely a numerical rank estimate. Interpret the displayed integers as rational parameters. Because every modular denominator is nonzero, a nonzero minor modulo this prime proves that its rational-function numerator is not identically zero over Q or R. Therefore the two-anchor five-node schedule generically has full column rank 20.

## 2. Theorem: two anchors give generic local identifiability for every m≥5

Measure every S=T∪U where T⊆{0,1} and U⊆{2,…,m−1} has |U|≤2. There are

Q₂=4[1+(m−2)+C(m−2,2)]

settings, including baseline and singletons. This is O(m²).

For each three-element nonanchor set R, restrict to the five-node block {0,1}∪R. The schedule contains the full five-node schedule of section 1 for this block. The corresponding nonzero minor polynomial involves only that block's parameters. Their finite product is nonzero, so all block minors are simultaneously nonzero on a nonempty Zariski-open set.

If a tangent perturbation of B is in the kernel of the complete acquisition Jacobian, its restriction to each block must be zero by that block's full rank. Every directed edge occurs in at least one block for m≥5. Hence the complete kernel is zero. The acquisition Jacobian has rank m(m−1).

Consequences: the inverse-function theorem supplies local recovery near each generic true B; algebraic dimension theory gives a generically finite complex fiber. These are identifiability statements, NOT an efficient global inverse or a global branch-selection theorem. The finite number of candidate models can grow with m, and distinct candidates need not be response-equivalent. Weighted transpose already forces at least two candidates generically. The witness gives no useful conditioning margin.

## 3. Theorem: one anchor generically fails for every m≥5

The one-anchor version measures every S with at most two nonanchor controls. After baseline and singletons, it has exactly

q₁=C(m,2)+C(m−1,2)=(m−1)²

nontrivial scalar readings, versus n=m(m−1) unknown directed entries. This count alone is not the proof.

Section 2 proves that the COMPLETE response map has Jacobian rank n generically. The one-anchor acquisition map has rank r≤q₁<n. On its generic constant-rank locus, its real local fibers have dimension n−r≥m−1. The complete response map is locally injective there because it has an invertible n-row Jacobian submatrix. Consequently each such positive-dimensional acquisition fiber contains arbitrarily close models with different complete binary response tables. At least one unmeasured response changes, despite identical acquired responses. All required inverse matrices remain nonsingular in a sufficiently small neighborhood.

Thus one anchor plus at most two other active controls cannot generically identify even the binary response map, for any m≥5. This is a generic noiseless impossibility, stronger than an isolated disconnected-anchor example. It does not cover schedules collecting configurations from several different anchors, and says nothing against arbitrary O(m²) schedules. For m≤3 the one-anchor schedule already measures all states; no contrary claim is made for these sizes.

## 4. Conditional polynomial-time primitive: recover every remaining pair linearly

Suppose the directed entries among two anchors and between each anchor and every other node have already been acquired in one common representation, and a is known. For nonanchors i,j, set x=B_ij and y=B_ji. For any anchor context T⊆{0,1}, put M=I+B_TT and define

α=1−B_iT M^−1 B_Ti, δ=1−B_jT M^−1 B_Tj,
r=B_iT M^−1 B_Tj, s=B_jT M^−1 B_Ti,
p=1−B_iT M^−1 1, q=1−B_jT M^−1 1,
d=a_i−a_TᵀM^−1 B_Ti, e=a_j−a_TᵀM^−1 B_Tj.

Block inversion gives, with h=g(T∪{i,j})−g(T),

h=[dδp+eαq−d(x−r)q−e(y−s)p]/[αδ−(x−r)(y−s)].

Therefore each measured context supplies the LINEAR equation in (x,y,z), z=xy,

(hs+dq)x + (hr+ep)y − h z
 = dδp+eαq+drq+esp − h(αδ−rs).

Use T=∅,{0},{1}. Three actual binary readings solve a 3×3 linear system. Its determinant is a nonzero rational function: certify_structure.py gives an exact witness determinant 2381454404875/271492629518088 and reconstructs x=1/10, y=1/13, z=1/130. Thus generic pair recovery is unique once the anchor scaffold is known. Check z=xy and measured denominators for exact consistency. With uncertain data, neither this equality nor a nonzero floating-point determinant is a certificate; interval enclosures are required.

For all nonanchor pairs this costs 3 C(m−2,2) readings and O(m²) constant-sized arithmetic after the scaffold is known. It avoids quadratic per-edge orientation branching. It does NOT acquire the scaffold. Pair reconstruction remains subject to arbitrarily bad numerical conditioning. Exact-number bit complexity is not bounded merely by the arithmetic-operation count.

## 5. Scaffold-extension experiment: a useful remaining obstruction

For a known k-node anchor block, attach one new node with known singleton a*. Let u=B_new,T, v=B_T,new, W=uvᵀ. For every anchor subset T, use M=I+B_TT, p=M^−1 1, qᵀ=a_TᵀM^−1, and h=g(T∪{new})−g(T). Then

h=(a*−qᵀv)(1−u p)/(1−u M^−1v),

which supplies a linear lifted equation

a* u p + qᵀv − Σ_rs [h(M^−1)_rs+p_r q_s] W_rs = a*−h.

There are k²+2k lifted unknowns. The implemented modular samples at k=5,6,7,8 produced respective ranks 30,42,56,72, versus 35,48,63,80 unknowns. These are exact ranks at those points, not a proof that these ranks are generic upper bounds. They warn that naive unconstrained lifting does not immediately give recovery; the nonlinear rank-one constraints W=uvᵀ remain. A fixed k makes solving those equations constant-size, but multiplying finite candidate lists across m attached nodes can still yield exponentially many global branches. Neither unique extension from a calibrated generic anchor block nor a polynomial branch-alignment procedure is proved here.

## Reproduction and scope

Run with the existing Python environment (SymPy is used only by the exact pair witness):

python ../practical_binary_schedule/rank_probe.py
python ../practical_binary_schedule/certify_structure.py
python ../practical_binary_schedule/extension_probe.py

These scripts execute only locally written code. They query synthetic matrices, not hardware. rank_probe.py records exact modular ranks for m=2,…,8 and zero through four anchors; ranks.json is the receipt. All experiments precede no claim about physical precision, settling, drift, calibration lifetime, or total cost. The strongest defensible outcome is a generic impossibility for one efficient proposed schedule, generic local identifiability for two anchors, and an explicit conditional pair-recovery routine. The unresolved task is efficient acquisition and globally valid alignment of the anchor scaffold.

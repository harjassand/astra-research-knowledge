# Entropy comparison, decisions and paid exact replacement are different

Root independently reconstructed the new worker pair using exact SymPy
rationals, with no worker implementation imports. `check.py`/`RESULTS.json`
contain the matrices and certificates. This is a checked example and a useful
interface distinction, not a claim to invent general Blackwell comparison.

For the stated strictly positive 3x3 classical K,L, L has full rank but the
unique postprocessor K L^-1 contains -1/20, so K cannot be obtained by ordinary
stochastic postprocessing of L alone. K itself is singular, which the accepted
N1038 covariance formulation explicitly allows. Root whole-read the completed
N1038 `sources/PROOF.md` copied in the worker continuation, including its
denominator-only change of coordinates and subunit completed-square identity.
Independently rebuilding its three 2x2 matrices at c=3/4,z=(1/3,1/3) gives
positive diagonal entries and determinants221/144000,2201/144000,2201/144000.
By that accepted all-finite-quantum-reference criterion, conditional Umegaki
comparison is at most3/4. This reuses the accepted underlying reference formula
at its classical-input/equal-reference scope; it does not extend to arbitrary
coherent-input quantum channels.

Here is an explicit decision task. Use a uniform prior on the three input
states. Acting earns -6 in state1 and +1 in states2,3; declining earns0.
For L every observation has negative joint expected act reward, so its optimum
is0. For K, acting only at output1 earns1/180. Equivalently, shift and scale
both actions into utilities[0,1]: the advantage is1/1260. Thus even the stated
quantum-reference entropy order does not preserve this bounded decision task.

The optimal worst-input raw-read probability for a locally exact one-step
replacement is3/40. Root checked an explicit nonquery subchannel V>=0 with all
column sums37/40 and residual K-VL>=0 with every column sum3/40. For necessity,
let alpha=[[5/2,0,0],[0,1/2,1/2],[0,1/2,1/2]] and pi=(0,1/2,1/2). The matrix

    alpha L^T - ones(3,1) pi L^T = diag(3/2,0,0)

is entrywise nonnegative. Hence any feasible nonquery V satisfies
sum_x pi_x(1-q_x)<=sum_yx alpha_yx K_yx=37/40, proving max_x q_x>=3/40.
Together these establish the exact one-step optimum. The zero in pi is a
least-favorable COST weighting while all-input exactness constraints remain;
it is not a claim of positive read cost under a public support promise that
removes state1.

The worker's separate sequential theorem must retain its own local-history,
privacy and classical-raw-access assumptions. This root check does not infer
optimal hard-budget approximation error from a read-count tail. A physical
measurement to create raw X, a solver advantage, historical novelty and a
civilisation-level capability remain unestablished.

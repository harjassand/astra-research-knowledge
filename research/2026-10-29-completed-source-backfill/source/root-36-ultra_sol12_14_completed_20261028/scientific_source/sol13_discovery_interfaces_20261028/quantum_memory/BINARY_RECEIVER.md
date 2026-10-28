# Arbitrary noncommuting binary matrix weights are received

Let S,T be any two distinct Hesse SIC projectors and let A,B be arbitrary
PSD matrices on a finite memory L. Put C=A+B and M=S tensor A+T tensor B.
Then, with f(Z)=Tr Z log Z and f0=0,

`f(A)+f(B)+f(C)-2f(M)>=0`.

This is an ordinary unambiguous-state-discrimination operation applied
to the matrix-weight target. The operation is established science; no
new USD method, historical priority or physical instrument is claimed.
It is a global binary-label receiver for every memory dimension, without
a small perturbation, commutativity, faithful floor or condition number.

Normalize TrC1; the zero case is trivial and homogeneity restores scale.
Let P be the rank-two span projector of S,T. Since TrST=1/4, define the
three POVM effects
`E_s=(2/3)(P-T)`, `E_t=(2/3)(P-S)`, `E_?=I-E_s-E_t`.
The first two are PSD. S+T has eigenvalues3/2,1/2 on P, so E_? has
eigenvalues2/3,0 on P and one on its orthogonal complement. Thus all
effects are PSD and sum to I. Exactly
`Tr SE_s=Tr TE_t=1/2`, `Tr SE_t=Tr TE_s=0`, and both erasure
probabilities are1/2. This equal-success channel is valid for arbitrary
priors; optimality at unequal priors is neither needed nor asserted.

Introduce the actual classical-label state
`omega_IQL=|s><s| tensor S tensor A+|t><t| tensor T tensor B`.
Because the Q states are pure conditional on I,
`I(I:Q|L)=S(Q|L)=S(M)-S(C)`.
Measure Q with the displayed POVM, retaining all three outcomes J.
Conditional mutual-information data processing gives
`I(I:Q|L)>=I(I:J|L)`.
The erasure coin is independent of the input label and the memory. On a
success branch I is known; on the erasure branch the original IL state
is retained. Consequently
`H(I|JL)=H(I|L)/2`, and `I(I:J|L)=H(I|L)/2`.
Thus `2S(Q|L)>=H(I|L)`, which is exactly the displayed matrix inequality.
No classical label is assumed available after preparation: J is actually
generated from Q. Every failed/inconclusive outcome is retained. Finite
entropy continuity includes singular A,B and nonfaithful C on its support.

Primary comparator: Clarke, Chefles, Barnett and Riis, *Experimental
Demonstration of Optimal Unambiguous State Discrimination* (2000),
[arXiv:quant-ph/0007063v1](https://arxiv.org/pdf/quant-ph/0007063v1),
equation(2), gives failure probability equal to the overlap magnitude at
equal priors. The original operation is due to Ivanovic, Dieks and Peres;
[Dieks1988](https://doi.org/10.1016/0375-9601(88)90840-7).
Our explicit fixed effects above supply the required uniform success
probability directly, including arbitrary quantum-memory matrices.

## Literal strong source and interface

The acquired source uses labels00 and10 with
`A=[[4,1],[1,1]]/10`, `B=diag(1,4)/10` and
`C=[[5,1],[1,5]]/10`. Both weights are positive definite; their
commutator is `[[0,3/100],[-3/100,0]]`. The exact18-state Bell-block
source has trace1 and physical marginal I3/3. `acquire_binary.py`
checks324 literal Bell/SIC output entries and certifies
`CMI-log3=F>=1/4` using rational polynomial root intervals and
24-term atanh logs. The actual lower endpoint exceeds0.28925212207.
Reference dimension is6 and antisymmetric-isometry extension dimension54;
the isometry is `V|i>=sum_jk epsilon_ijk|jk>/sqrt2`. No extra flag is used.

The source is singular of rank4, so it does not meet condition-number24.
Reduction positivity would require both A<=C/3 and B<=C/3, impossible
for nonzero C. A logical-memory filter |0> succeeds with probability1/2
and produces Bell weights4/5,1/5; fidelity4/5>2/3 proves Schmidt number3.
The physical01 block has square `E02 tensor AB/9!=0`, excluding the
declared square-zero reset/bath package. Independent A,B cannot have
the common affine form p_i U+V with seven zero label weights, unless
they are proportional. Other alternative representations are unclassified.

## Costs and scientific boundary

The universal proof reads two supplied r-by-r PSD matrices and two known
SIC labels. Matrix input/PSD qualification costs are paid separately;
no tomography or source-support certificate is free. The receiver itself
has no spectral floor or precision-dependent radius. Our literal r2
source uses rational entries of denominator10 and the fixed rational
POVM; the exact replay took about0.119s including SymPy import/algebra,
excluding interpreter startup and source/literature retrieval. Its
entropy endpoints use at most9,292 rational bits. Exact polynomial root
isolation and interval logs are an equally informed ordinary method for
the strong numerical margin. No runtime separation is established.

If physically implemented, the operation needs calibrated qutrit
preparation and a three-outcome USD interface; success and erasure each
have probability1/2 for either label. All erasures enter the proof. Those
controls, the unknown memory matrices and their acquisition/readout have
not been acquired physically. The source and its entropy certificate are
synthetic mathematical inputs/outputs. The binary theorem does not prove
the nine-label matrix extension. It is a credited consequence of an
established operation, not a civilisation-level technology or new USD.

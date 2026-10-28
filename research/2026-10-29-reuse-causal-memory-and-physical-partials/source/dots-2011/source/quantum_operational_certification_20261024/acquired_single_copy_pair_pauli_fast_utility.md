# Actual single-copy pair-Pauli acquisition: fast utility with an explicit ambient-factor tradeoff

27 October2026. Local post-cutoff construction; independent receiving requested. This is an alternative to the collective-Keyl branch, which remains unchanged. No historical novelty or optimality claim.

## Statement and access

Use the same qutrit-source contrast H=J-3omega=4T-6omega and A=J+3omega=4T, on physical matrix dimension d=3s. Only the ACTUAL labelled states T and omega are supplied, one original source call per state copy. No physical J copies, unknown whitening operation, or collective source-copy measurement is used.

For known0<t<=1 and failure beta, the construction below acquires a classical Hermitian Hhat with

 Hhat-H=sqrt(A)Z+Z*sqrt(A)+R,
 ||Z||<=sqrt(9t/8), ||R||<=2sqrt(9/8)t,               (1)

with probability at least1-beta. If padding is used, (1) is understood on the known zero extension and then compressed to the physical space; the same decoder comparisons hold. Its deterministic source-call cap is

 O((d²/t) log(4d[1+log(4/t)]/beta))                     (2)

with harmless positive constants inside logarithms. Exact schedules below define the cap at all endpoints. This has an extra ambient factor compared with the received collective O(d/t) route, but requires only a single physical source output at a time and explicitly specified known-basis measurements.

The received deterministic localization then gives exact orthogonal-reset utility loss L<=140rt+2kappa, or overlapping-reset comparison L<=3L_*+300rt+2kappa. Here kappa is a charged feasible optimization gap, and the overlapping comparison still requires a separately constructed comparator. No entropy or structural-promise claim follows merely from acquisition.

## 1. Exact single-copy POVM and unbiased Hermitian estimator

Pad by a fixed known isometry to a power-of-two dimension D with d<=D<2d; the added levels have zero state population. This is a known register embedding, not a source-dependent isometry. Perform all estimation on the padded density matrices. At deployment compress the acquired Hhat back to the original d-dimensional physical space and use the original decoder feasible set.

Work in ANY known orthonormal basis, indexed1,...,D. For i<j define the supported Pauli matrices

 X_ij=|i><j|+|j><i|,
 Y_ij=-i|i><j|+i|j><i|.

Choose one of three settings with probability1/3:

 - Z: measure the basis. On outcome i, output the classical matrix Ysample=3|i><i|.
 - X: choose a uniformly random perfect matching of the D basis indices, and measure the X eigenbasis within every matched pair. On pair{i,j} and sign sigma in{+1,-1}, output Ysample=[3(D-1)/2] sigma X_ij.
 - Y: choose a uniformly random perfect matching and measure the Y eigenbasis within every pair. Output Ysample=[3(D-1)/2] sigma Y_ij.

These are ordinary orthonormal-basis measurements of ONE state copy. A uniform random permutation followed by adjacent pairing produces the matching; each specified pair appears with probability1/(D-1).

The Z expectation is the diagonal of rho. For either off-diagonal Pauli, the two outcome probabilities have difference Tr(rho Pauli_ij). Thus the matching probability and the estimator coefficient give contribution(1/2)Tr(rho Pauli_ij)Pauli_ij. Summing X and Y over all pairs reconstructs all off-diagonal entries, with their complex phases. Therefore

 E Ysample=rho.                                     (3)

No positivity or trace-one claim is made for an individual estimator.

## 2. Two exact second-moment calculations in a known pilot basis

Let G>0 be known and diagonal in the basis actually measured, with entries g_i and minimum g_min. Suppose rho<=cG. Put S=sqrtG and define the known Sylvester map T_G(M) by S T_G(M)+T_G(M)S=M. Its entries are M_ij/(sqrt(g_i)+sqrt(g_j)). Each filtered sample still has only one diagonal entry or one supported off-diagonal Pauli; its square is diagonal. Direct averaging gives

 [E T_G(Ysample)^2]_ii
 =3rho_ii/(4g_i)
  +[3(D-1)/2] sum_(j!=i) (rho_ii+rho_jj)/(sqrt(g_i)+sqrt(g_j))²
 <=(3c/2)D².                                       (4)

The last step uses rho_ii<=c g_i and (g_i+g_j)/(sqrt(g_i)+sqrt(g_j))²<=1. In particular c=2 gives the MATRIX second-moment bound3D²I. Centering subtracts the mean square, a PSD matrix.

For the full classical whitening map W_G(M)=G^-1/2 M G^-1/2, another exact calculation gives

 [E W_G(Ysample)^2]_ii
 =3rho_ii/g_i²
  +[3(D-1)/2] sum_(j!=i)(rho_ii+rho_jj)/(g_i g_j)
 <=3cD²/g_min.                                    (5)

These are actual matrix bounds because the displayed second moments are diagonal, not entrywise-to-operator estimates. No commutation of rho and G is needed; only the measurement basis is chosen from the KNOWN G.

## 3. A fully acquired constant-relative pilot without Keyl measurements

For a density rho, use scales u=1,1/2,... down to a supplied final u_*, appending u_* if necessary. Adjacent ratios are at most2. Let K be the known number of stages, and assign failure beta_p/K to each.

At the initial stage use G=I. At each later stage set G=rhohat_prev+uI. If the preceding estimate has relative error1/8 against rho+u_prev I, then

 (3/4)(rho+uI)<=G<=(5/4)(rho+uI).

Abort if G fails uI/2<=G<=4I; good histories never abort. On those histories rho<=2G and g_min>=u/2. Choose the KNOWN G eigenbasis for the pair-Pauli measurement, and acquire

 n_u=ceil[(4096D²/u) ln(2DK/beta_p)]

independent single-copy estimators. Their full-whitened second moment is at most12D²I/u by (5), and their raw whitened norm is at most6D/u. The centered norm is therefore at most12D/u.

For the whitened sample average, two-sided matrix Bernstein at deviation eta=1/10 has denominator at most25D²/u. The exponent is at least n_u u/(2500D²), so the stated count bounds stage failure by beta_p/K. Dewhitening the mean gives rhohat (equivalently the average of the unwhitened Ysample matrices) and

 -eta G<=rhohat-rho<=eta G.

Because G<=(5/4)(rho+uI), this is relative error at most1/8. At initialization G=I<=rho+I, so the same conclusion holds. The statement is conditional on successful histories with fresh copies; a union over first failures pays the total beta_p. No behavior following a failed history is assumed.

The sum of reciprocal scales is at most4/u_*, so the deterministic pilot cap is the explicit sum of n_u, of order(D²/u_*)log(2DK/beta_p). Every stage is a one-copy known-basis measurement; there is no hidden collective pilot primitive.

Apply this pilot to the ACTUAL state T with u_*=t/4 and beta_p=beta/2. Set

 G_A=4That+tI.

On success7(A+tI)/8<=G_A<=9(A+tI)/8. Abort if G_A fails tI/2<=G_A<=6I; successful histories pass. Padding simply replaces A by its zero extension and adds tI on the known extra levels.

## 4. Direct bounded single-copy estimation of the filtered contrast

Keep the acquired G_A fixed. Each observation uses TWO independent fresh state copies, one T and one omega, measured individually by the pair-Pauli POVM in the computed G_A eigenbasis. Store only the classical outcome before measuring the next copy. Form

 Zraw=4T_GA(Y_T)-6T_GA(Y_omega).

Its mean is M=T_GA(H), exactly. Since both true states obey rho<=A<=2G_A, (4), independence and the coefficients give

 E[(Zraw-M)^2]<=52*3D² I=156D² I.

Each individual Sylvester-filtered sample has norm at most3D/sqrt t because g_min>=t/2. Thus ||Zraw||<=30D/sqrt t and its centered norm is at most60D/sqrt t. Acquire

 n_c=ceil[(512D²/t) ln(4D/beta)]

independent contrast observations. Matrix Bernstein at deviation sqrt t has denominator at most312D²+40D<=352D². Hence their mean Mhat obeys ||Mhat-M||<=sqrt t except on probability at most beta/2. There is no clipping bias and no unbounded estimator in this step.

Set Hhat=sqrt(G_A)Mhat+Mhat sqrt(G_A). It estimates the ACTUAL H=4T-6omega. Douglas factorization from G_A<=9(A+tI)/8 gives exactly decomposition (1), as in the received deterministic square-root localization lemma. The total source cap is

 N_total=sum_pilot_stages n_u +2n_c,                 (6)

counting every T and omega preparation and every rejected/unused outcome. The first-failure and final-estimation union gives success probability at least1-beta. On failed histories the mathematical output may be arbitrary; a computed feasible decoder still remains CPTP.

## 5. Decoder rate and operation contract

Take, for example, t proportional to nu²p0/r with the same conservative constants as the received exact-source SDP or top-r-projector receiver. Equation(6) then gives

 O(s² r/(p0nu²) polylogs)

source calls and the received fast utility/recovery and fresh holdout guarantees. This is a constructive extra-ambient-factor alternative, not a claim to improve ordinary tomography in every regime (especially when r is large).

The quantum operation per sample is: a computed known basis rotation, then either a computational-basis measurement or direct-sum two-level Pauli measurements for a classically sampled matching. No source-dependent unknown unitary is supplied. A dense known D-dimensional basis rotation can be expressed using O(D²) known two-level rotations; the matching transformation adds O(D) two-level rotations. This is not efficient in log D or independent of ambient dimension. Quantum working storage contains one physical output and its known local-label/embedding registers plus implementation ancillas, NOT n0 stored source outputs for a collective Keyl measurement. Classical storage and matrix computations are ambient-sized.

All mathematical estimates above use ideal specified rotations/measurements and finite-dimensional classical arithmetic. Finite-precision basis synthesis, matrix arithmetic and decoder implementation must be assigned a separate error budget; no uncharged exact hardware or bit-complexity theorem is claimed. Unlike the collective branch, this construction does not invoke an unimplemented general-n covariant POVM: its measurement family is explicitly the single-copy pair-Pauli family above. The supplied regularization floors control all inverses in the statistical argument, not a least nonzero source eigenvalue.

The collective O(sr/(p0nu²)) branch and its resource limitations remain distinct. Neither branch establishes a matching coherent-adaptive accuracy lower or certifies the hidden source promise. Reuse and many-use confidence/error accounting are exactly as in the separately received receiver/holdout theorems.

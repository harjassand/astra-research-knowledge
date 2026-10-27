# A mixed-program filter for rare spectral subspaces

2026-10-27. Generalization of the received population method; independent receipt requested. This theorem is about an actual heralded quantum filter, not a classical eigenbasis description or a relative-whitening oracle.

## Access, promise, and result

Let sigma and rho be unknown density operators on an accessible finite register. The available resources are independent mixed copies of these two states, controlled full-register SWAPs, and known coherent ancilla operations. Define

 H=4sigma-6rho,
 P=1_(0,infinity)(H).

Suppose every positive eigenvalue of H is at least a supplied g0, where0<g0<=1. P may have arbitrary rank and the individual programs need NOT commute with P. Suppose also the supplied0<W<=1 bounds both target weights:

 Tr(Psigma)<=W, Tr(Prho)<=W.

For any0<xi<=1, there is an explicit consumed-program instrument with the following properties:

1. Its complete unhalved diamond distance from the ideal target projection with erased rejection,
   X -> PXP on acceptance, and erasure otherwise,
   is at most xi. Thus coherences WITHIN an arbitrary-rank target subspace are preserved to the same accuracy.
2. For every positive unit-trace input, including arbitrary auxiliary correlations, its acceptance probability is at most
   3 Tr(P input)+3W xi/16.
   In particular an input supported outside P is accepted with probability at most3W xi/16.

This simultaneously provides an ordinary quantum-instrument approximation and a much smaller false-acceptance bound when the target has small program weight W. It does not assert a relative diamond bound on arbitrary P/complement coherent superpositions, or preserve the rejected quantum state (rejection is erased).

## Explicit finite resources

Set

 L=max(1,ceil log_16[16/(W xi)]),
 eta=(xi/(100L))^2,
 M=2^m the least power of two with M>=1024/g0,
 r=ceil log_2(1/eta),
 S=Lr pi(M-1)/4.

The number of consumed program copies is at most

 n<=131072 S^2/xi+4Lrm.                               (1)

There is no raw register-dimension factor in this SAMPLE count; physical gate width and memory still depend on that dimension. The polylogarithmic W dependence replaces the naive extra factor1/W obtained by demanding uniform diamond error of order Wxi from each simulator. No optimal joint g0,W,xi complexity claim is made.

## 1. Coherent spectral classification with an arbitrary-rank target

Since -6I<=H<=4I, use QPE for

 U=exp[2pi i(H+6I)/16].

Its phases lie in[0,5/8]. Nonpositive eigenvalues have phase at most3/8; positive eigenvalues have phase at least3/8+g0/16. Accept estimated phases in

 [3/8+g0/32, 7/8).

Circular error less than g0/32 suffices, including wrap near zero. The same elementary finite QPE tail estimate used in the source receiver applies because M g0/32>=32. Repeating QPE r times and taking a reversible majority classification has spectral error at most eta.

Crucially, do not measure the phase registers and leave them behind: coherently compute the classification bit, then reverse the QPE circuits while retaining that bit. The reverse evolutions use fresh mixed programs and NEGATIVE collision angles, not an unavailable inverse state-preparation oracle. For exact evolutions, the resulting isometry differs from the ideal coherent P/complement flag isometry by at most2sqrt(eta) in operator norm. On each eigenvector the wrong-classification amplitude has norm at mostsqrt(eta), and computation/classification/uncomputation costs at most twice that norm. Orthogonality of the data eigenvectors makes this a uniform operator bound even when P has multiple distinct positive eigenvalues.

Measuring the classification bit, discarding its work registers, and retaining the data gives a complete nondestructive binary instrument within4sqrt(eta) in diamond norm of the ideal Lueders P measurement. Run L such classifiers with fresh samples, accept only if all L accept, and erase on any rejection. For exact evolution their complete instrument error is at most4Lsqrt(eta)<=.04xi by telescoping. This receives target-subspace coherences rather than only membership probabilities.

Forward QPE controlled H-times are t_a=pi 2^a/8, a=0,...,m-1. The reverse circuit has the opposite times; all Lr forward/reverse sums give the stated S. For each controlled time t, use

 N_t=ceil[65536 |t| S/xi]

signed rounds, each consuming one sigma and one rho copy with angles4t/N_t and-6t/N_t. The separately received signed-pair simulation bound is256 t^2/N_t. Hence total simulation error<=xi/256. Together with the ideal-filter error, this is less than xi. Counting two copies per round and both forward/reverse circuits gives(1).

## 2. Population receiving without code-sector measurements

The operator calculation in section3 of `noise_adapted_quadratic_training_receiver.md` uses only

 [P,4sigma-6rho]=0,
 Tr(Psigma),Tr(Prho)<=W,
 0<=sigma,rho<=I.

It does not use rank-one P. In particular sigma P sigma<=Tr(Psigma)sigma<=WI holds for arbitrary projector rank. For each controlled signed round with delta=t/N_t, the same proof gives

 K^*(I_control tensor P)
 <=(1+800delta^2)(I_control tensor P)+800delta^2 W I.   (2)

This is an operator inequality valid with arbitrary reference/ancilla systems and arbitrary coherences across P. All known control/work processing preserves I_control tensor P. No virtual sector pinching is used.

For one complete coherent classifier, including its reverse QPE, set

 v=800sum delta^2<=xi/(80L),
 a=exp(v), b=W(exp(v)-1)<=W xi/(40L).

If its input has total mass m and target population r0, its accepted branch has target population at most a r0+b m. Its accepted total mass is at most r0+beta m, where

 beta=eta+xi/(256L)<1/16.

The ideal coherent classification bit has the same membership probabilities as before uncomputation, so its outside acceptance remains at most eta. The simulation error supplies the additional term. These statements hold for arbitrary positive subnormalized inputs, not only diagonal mixtures.

## 3. Iterating actual accepted states

Write r_k for the P population and m_k for the total mass after k accepted classifiers. Then

 r_(k+1)<=a r_k+b m_k,
 m_(k+1)<=r_k+beta m_k.

The explicit positive-matrix recurrence proof in the received receiver gives

 m_L<=3r_0+5b+beta^L.

All its constants apply with p replaced by W: a^L<=80/79 and bL<=1/40. The chosen L gives beta^L<=Wxi/16, while5b<=Wxi/8. Therefore

 m_L<=3r_0+3Wxi/16,

which proves the claimed small false-acceptance guarantee. The accepted state can contain imported target population; that population is explicitly controlled by(2) and the recurrence, not assumed absent or removed by repetition.

## Consequences and restrictions

This is a reusable mixed-sample quantum filtering principle. It separates preservation of a target quantum subspace from suppression of false acceptance into a rare target. The target projector is specified implicitly by a signed contrast of unknown states; no classical tomography, unknown eigenbasis measurement, purified state preparation, or support oracle is introduced.

For an input ensemble that puts a small mass on the target and otherwise has small target population, the stronger acceptance estimate can improve an operational error budget beyond what uniform diamond simulation alone gives. Additional task-specific receiving is still necessary. In particular this theorem alone is not a decoder, a channel capacity result, a proof of a source promise, or a universal measurement of arbitrary relative eigenvalues.

## 4. Arbitrary known two-program contrast coefficients

The construction is not restricted to the numerical contrast4,-6. Let

 H=A sigma-B rho, A,B>0 known, ell=A+B,
 P=1_(0,infinity)(H), positive gap g0 with0<g0<=ell,
 Tr(Psigma),Tr(Prho)<=W.

Keep L,eta,r as above. Choose M=2^m>=128ell/g0 and use

 U=exp[pi i(H+B I)/ell],
 accepted phase interval[B/(2ell)+g0/(4ell),3/4).

The spectrum lies in[0,1/2]; the circular gap to the decision boundaries is at least g0/(4ell), except that the upper boundary has the larger gap1/4. The same QPE tail and coherent uncomputation argument applies. The complete forward/reverse time sum is now

 S=2Lr pi(M-1)/ell.

For each signed round use collision angles A delta,-B delta, with delta=t/N_t and

 N_t=ceil[65536 ell^2 |t|S/xi].

The total number of fresh program copies is at most

 n<=131072 ell^2 S^2/xi+4Lrm.

In particular its scale is O(ell^2/(g0^2 xi)) times the explicit logarithmic factors above. This is invariant under simultaneously rescaling H and g0.

Here are the coefficient bounds so this extension does not rely on rescaling the4,-6 theorem incorrectly. The simulation error per round is at most

 [4(A^2+B^2)+2AB]delta^2<=4ell^2 delta^2.

The first term is the sum of two controlled density-exponentiation errors; the second is the unitary product-formula commutator bound. For population, the two residual commutator coefficients sum to at most

 [(2/3)(A^3+B^3)+AB(A+B)]|delta|^3
 <=ell^3 |delta|^3.

The base identity coefficient is at most(A^2+B^2)W delta^2, the double commutator has coefficient at most AB delta^2 and operator bound P+3WI, and the scalar trace term is at most2A^2B W|delta|^3. Since ell|delta|<=1, their sum, dropping the negative P coefficient, yields conservatively

 K^*(P)<=(1+8ell^2 delta^2)P+8ell^2 delta^2 W I.

The chosen N_t ensures ell|delta|<=1 (indeed ell S>=2pi) and, per classifier, population exponent at most xi/(8192L), while simulation error is at most xi/(16384L). These are smaller than the budgets used in sections2-3. Thus BOTH conclusions hold unchanged: complete instrument error at most xi, and acceptance at most3Tr(P input)+3Wxi/16.

This section covers a two-state signed contrast with arbitrary known positive magnitudes. It does not silently claim an arbitrary many-term Hamiltonian extension. More terms require corresponding commutator and population bookkeeping.

## Promise consistency: rarity and gap are not independent

For the general two-program contrast, positivity on P gives

 g0 rank(P)<=Tr(PH)<=A Tr(Psigma)<=A W.

Thus a nonzero target with fixed coefficients cannot have arbitrarily small W at fixed positive gap. The logarithmic dependence on W means no EXTRA inverse-rarity penalty beyond the displayed gap dependence; it is not a claim of rarity-independent physical complexity. In the receiver application g0 and W are both of order p, so this distinction is exactly the quadratic-versus-naively-cubic signal cost. Supplied promises inconsistent with this inequality do not describe a nonempty target.

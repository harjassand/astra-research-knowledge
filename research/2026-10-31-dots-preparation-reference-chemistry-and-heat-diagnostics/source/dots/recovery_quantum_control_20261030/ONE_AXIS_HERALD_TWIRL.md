# Uniform herald probability from physical Z randomization
2026-10-30. Exact finite-operation lemma supporting, not completing, root's one-axis factory proposal.

Let H_X have rank r and let P_+=2^{-r} sum_{g in S_X}g project onto all +1 X-check outcomes. Define the actual physical product twirl T_Z=rho -> 2^{-n} sum_z Z^z rho Z^z. For arbitrary joint DATA/bath state rho,

 tr_DATA[(P_+ tensor I) T_Z(rho)] = 2^{-r} tr_DATA rho.

Proof: T_Z removes every off-diagonal computational matrix element. The diagonal of P_+ is uniformly 2^{-r}, since every nonidentity pure X stabilizer is a nonzero bit shift. Thus herald probability is exactly 2^{-r}, even with an entangled bath, and the herald effect is proportional to identity. This proves probability only, not logical harmlessness of the postselected Kraus map.

Every Z twirl branch commutes with all logical Z operators and all Z-checks. Hence it preserves an already proved known-logical-|0>, small-X-error module. More generally define M_X(t)=span{X^e Z^z |0bar> : |e|<=t, z arbitrary}, where |0bar> is the normalized projection of |0^n>. This module is Z-twirl invariant. Since X^e commutes with P_+, and P_+ Z^z|0bar> is either zero or a phase times |0bar>, the postselected support is contained in span{X^e|0bar> : |e|<=t}. Here a zero-X-syndrome Z^z acts as a Z stabilizer/logical Z, which fixes the all-logical-zero state. Thus arbitrary extensive Z phase is removed on success, without a mask. Native dirty-prefix/gauge sectors still require their actual module intertwiner; this DATA support proof does not supply it.

## Concrete one-axis projector
Let C_X=rowspan(H_X). The all-zero logical state is uniform on C_X. Its Z-Pauli orbit spans all computational basis vectors in C_X (characters of this binary group). Therefore

 M_X(t)=span{|x>: dist_Hamming(x,C_X)<=t}.

The module projector is computational-diagonal. Arbitrary physical Z payloads preserve it, as do completed X-stabilizers. Partial extraction/correction prefixes need actual BUSY/dirty credits; the diagonal identity does not assert they preserve the module. The distinction between H_Z syndrome and the coset x+C_X remains essential: low-weight error assumptions exclude an undetected logical X, not syndrome energy alone.

## No amplification of the incoming one-axis radius tail
Let Q_bad=I-Q_t for the diagonal one-axis projector. Since Q_t is a union of C_X cosets, it commutes with P_+. Thus T_Z^*(Q_bad P_+ Q_bad)=2^{-r}Q_bad. The conditional bad-radius population after an ideal true herald equals its incoming population exactly. This identity includes an untouched bath. Premeasurement one-axis tail estimates therefore do not automatically pay an exponential postselection penalty. Uncontrolled endpoint faults/false acceptance do not enjoy this identity without further proof.

## Finite imperfect randomness
For each i let E_i=(1-p_i)Id+p_i Ad_Zi with delta<=p_i<=1-delta. Then E_i=2delta T_i+(1-2delta)F_i for a CPTP Pauli channel F_i. Product expansion is CP-positive, so tensor_i E_i CP-dominates (2delta)^n T_Z. Consequently the all+ probability is at least (2delta)^n 2^{-r}, uniformly over input and bath. This CP domination is legitimate for the explicit stochastic randomizer, not a domination assertion about signed fault maps.

A local Z-jump Lindbladian of rate gamma for finite duration tau implements p=(1-exp(-2 gamma tau))/2, giving delta=p>0. An actual autonomous finite randomization window/commit is still required; externally switched duration is only an ordinary comparator.

## Why randomization is necessary for the proposed uniform bound
The one-axis module alone includes exact nonzero X-check syndrome states. Those have zero all+ probability. Merely waiting in a full memory for an unspecified duration does not establish a uniform lower bound. The physical twirl repairs this exact algebraic gap without learning a dense frame.

## Exponent and acceptance costs remain
If every completed physical attempt has success effect at least p I on its full input (p>=exp(-a n)), then M=ceil(exp(a n) log(1/epsilon)) attempts give no-success probability <=epsilon. Independence is NOT required: condition on each prior failure transcript; the normalized current state, including a retained bath and arbitrary intervening CPTP evolution, still has next success probability at least p. The ideal twirl instrument has exact effect p I, and the explicit biased randomizer has the uniform lower bound above. No such effect bound is presumed for faulty physical acceptance or an unfinished native attempt.

An unnormalized bad-herald norm bounded exp(-b n) becomes at best exp(-(b-a)n) after dividing by a success lower bound exp(-a n). Need b>a (including constants), or a direct conditional error proof; an exponential unnormalized numerator alone is insufficient. Faulty classical acceptance can admit a nonzero syndrome state, so a true protected all+ predicate and actual native endpoint/shared-prefix control remain missing. No autonomous factory or universal theorem follows.

# Exact entropy certificate for every physical 2+1 block-diagonal state

24 October 2026. Root's proposed extension, independently verified and expressed as a sum of three nonnegative information quantities. No separability premise or reference-dimension bound is needed.

## Theorem

Let ρ be a normalized state on C3 tensor R, with arbitrary finite R. Suppose a physical qutrit decomposition C3=C2 direct-sum C makes

ρ=B direct-sum C,

where B is a positive operator on C2 tensor R and C is positive on R. Then

2S((W3 tensor id)ρ)-S(ρ)-S(ρ_R)>=log 3.

Equality holds exactly when ρ=I3/3 tensor τ for some reference state τ. In particular every nonproduct state in this block-diagonal class has strict inequality, including states whose B block is entangled.

An arbitrary physical choice of the two-dimensional subspace reduces to this coordinate form by a unitary; WH covariance conjugates the output by the corresponding conjugate unitary and preserves all relevant entropies.

## 1. Exact output blocks and notation

Set P=Tr_A2 B, b=Tr B, c=Tr C, so b+c=1 and ρ_R=P+C. Use

u(X)=-Tr X log X

for UNNORMALIZED entropy, with zero eigenvalues contributing zero. This differs from the homogeneous normalized entropy (Tr X)S(X/Tr X) used in the principal-compression results; substituting that latter convention here would omit necessary mass terms.

The qubit reduction identity I2 tensor P-B^(T_A2)=(J tensor I)B(J-adjoint tensor I), with J the antisymmetric qubit unitary, gives

(W3 tensor id)ρ unitarily equivalent to
[(B+I2 tensor C)/2] direct-sum [P/2].

Put D=B+I2 tensor C, of trace 1+c. Since the total traces of D and P sum to two, direct entropy evaluation gives the exact target slack

G=2S(output)-S(ρ)-S(ρ_R)-log 3
 =u(D)+u(P)-u(B)-u(C)-u(P+C)+2 log 2-log 3.       (1)

## 2. First remainder: conditional-entropy concavity

Define

Delta_cond=u(D)-u(P+2C)-u(B)+u(P)-2c log 2.

This is nonnegative by homogeneous conditional-entropy concavity. Explicitly, D/(1+c) is the mixture with weights b/(1+c), 2c/(1+c) of B/b and (I2/2) tensor (C/c). Its reference is (P+2C)/(1+c). The second branch has conditional entropy log 2. Multiplying the conditional-entropy concavity inequality by 1+c gives precisely Delta_cond>=0.

Equivalently, Delta_cond=(1+c)I(A2:T|R) for the corresponding classical branch flag T. This remains valid by continuity when b or c vanishes.

## 3. Second remainder: ordinary entropy concavity

Define

Delta_mix=u(P+2C)-u(P+C)-u(C)-c log c+(1+c)log(1+c).

This is (1+c) times the Holevo information of the reference ensemble with states P+C and C/c, and weights 1/(1+c), c/(1+c). Hence Delta_mix>=0. The formula is interpreted continuously at c=0.

## 4. Third remainder: an explicit binary relative entropy

Define

g(c)=c log c-(1+c)log(1+c)+2(1+c)log 2-log 3.

It has the exact representation

g(c)=(1+c)D((c/(1+c),1/(1+c)) || (1/4,3/4))>=0.

Its unique zero on [0,1] is c=1/3. Alternatively g'(c)=log(4c/(1+c)) and g''(c)=1/[c(1+c)]>0 in the interior.

Direct cancellation in (1) now yields the exact certificate

G=Delta_cond+Delta_mix+g(c)>=0.                 (2)

Thus no optimizer, continuity conjecture, or comparison with a different channel is needed.

## 5. Equality

If G=0, all three nonnegative terms in (2) vanish. The scalar term forces c=1/3 and b=2/3, so both mixture weights are positive. Delta_mix=0 forces its two reference states to coincide:

C/c=P+C=:τ.

Consequently C=cτ and P=bτ. The two branches defining Delta_cond now have the SAME reference state τ. Its conditional-entropy Jensen gap therefore equals the ordinary entropy Jensen gap of B/b and (I2/2) tensor τ. Strict concavity of von Neumann entropy forces these two states to be equal. Hence

B=(I2/3) tensor τ, C=τ/3,

which is ρ=I3/3 tensor τ. Conversely these product states have equality by direct substitution. Singular τ causes no problem; all statements apply on its support.

## Scope

This proves the target for every state with a physical 2+1 block decomposition, for arbitrary finite reference and arbitrary entanglement in the two-dimensional block. It does not justify physically pinching a general state: the functional need not improve under that operation. It does not cover arbitrary coherence between the one-dimensional and two-dimensional physical sectors, and therefore does not settle the unrestricted entropy inequality.

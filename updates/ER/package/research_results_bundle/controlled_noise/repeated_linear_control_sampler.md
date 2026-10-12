# Binary repetition of a deterministic invertible control with polynomial faults

Scope extension, 2026-10-12. This is a compressed-control endpoint theorem, not a solution for random noncommuting gates. It uses the elementary commuting Fourier sampler after an exact interaction-picture reduction; the adaptive F_2 span sampler is an alternative.

## Exact model and ordering

Let C be an explicitly given invertible D by D matrix over a fixed prime field F_p. Let Z_t be independent, identically distributed fault-interval endpoints. Each interval has independent compound-Poisson types j with mean theta_j and fresh uniform Boolean inputs to explicit degree-at-most-k polynomial maps F_j. For a binary integer N, use the recurrence

    X_(t+1)=C X_t+Z_t,  t=0,...,N-1.

Then

    X_N=C^N x_0+sum_(t=0)^(N-1) C^(N-1-t) Z_t.

Superposing the independent interval Poisson streams gives an exact additive model: type j has total mean N theta_j, and a fresh jump is

    J_j=C^K F_j(U),

where K is uniform on {0,...,N-1}, independently of U. Compute C^N and C^K by repeated squaring; sample K with O(log N) bits and constant-success integer rejection. No repetition schedule is expanded.

If the intended recurrence is X_(t+1)=C(X_t+Z_t), the exponents are 1,...,N instead. Equivalently replace each F_j by C F_j. This phase convention must be fixed in the model.

## Acquired image span

Write c_(j,A) for the polynomial coefficient vectors. The image-generated additive subgroup of J_j is

    H_j=span{C^k c_(j,A): 0<=k<N}.

Cayley-Hamilton shows that k<min(N,D) suffices. This span and containment in any proposed W are computed with polynomially many matrix-vector products and Gaussian elimination. Boolean Mobius inversion identifies coefficient spans with image spans without input enumeration.

## Acquired nonzero-character/innovation bound

Suppose a linear functional ell is nonzero on H_j. Some coefficient vector c has a nonzero scalar sequence value

    s_k=ell(C^k c),  0<=k<N.

Because C is invertible, its characteristic-polynomial recurrence has nonzero constant term. A run of D consecutive zero s_k values would force all future and past values to be zero. Thus a nonzero sequence has no such run.

If N>=D, at least floor(N/D) indices in {0,...,N-1} have s_k nonzero, a fraction at least 1/(2D). If N<D, at least one does, a fraction at least 1/D. At every such index the Boolean scalar polynomial ell(C^k F_j(U)) is nonzero, and therefore is nonzero with probability at least 2^(-k_degree).

Consequently, uniformly over nontrivial ell and all horizons,

    P(ell(J_j)!=0)>=2^(-k_degree)/(2D).              (1)

For p=2 and a current acquired span W, choose ell annihilating W but not H_j. Equation (1) is precisely the active-mark innovation lower bound. The exact-real adaptive algorithm therefore uses at most O(D^2 2^k) expected proposals, with efficient containment and mark sampling as above.

## Simpler approximate endpoint implementation

The typewise Fourier method needs no adaptive waiting times. Let h_j=dim H_j and c_p=1-cos(2 pi/p). Its exact bound is

    TV(mu_j,Uniform(H_j))
      <=(1/2) sqrt(p^(h_j)-1)
         exp[-N theta_j c_p 2^(-k)/(2D)].

For per-type error delta, replace a type by Uniform(H_j) whenever

    N theta_j >= (2D 2^k/c_p)
                    [(h_j log p)/2+log(1/(2 delta))].

Otherwise its total Poisson mean is polynomial in D, 2^k and log(1/delta). Sample its bounded count, then each mark with a random K and repeated squaring. Sum type endpoints and add C^N x_0. Independent type convolution contracts TV. The positive Poisson truncation and rational-threshold method in commuting_polynomial_jump_sampler.md gives polynomial bit complexity and avoids continuous event times entirely.

Thus binary N costs polynomially in log N, not N. Degree O(log explicit input size) is still permitted. For a fixed extension field, regard outputs as a vector space over their prime field and use its additive dimension.

## Executed checks

repeated_control_checks.py checked every invertible 3 by 3 binary matrix (168 matrices), every nonzero input/output dual vector, and scalar prefixes of lengths 3 through 12: 82,320 cases. Every active prefix obeyed the recurrence density bound. The minimum observed active density was 1/5, consistent with the conservative 1/(2D)=1/6 bound.

It also compared direct control-then-noise iteration with the superposed interaction-picture compound-Poisson generator at N=1,2,3,7,12. Maximum endpoint residual was 1.0e-15. These numerical checks test orientation and finite examples; the argument above is the proof.

## Scope

This handles a binary number of repetitions of one deterministic invertible linear control, interleaved with identical independent polynomial-fault intervals. For Clifford controls it applies to the classical Pauli-frame labels with the supplied symplectic action; it does not simulate arbitrary quantum states.

It does not yet handle an arbitrary compressed straight-line program of varying controls and noises. In such a program, many suffix-transform contexts can appear, and an active transported fault type may have exponentially small global leaf mass. Nor does it handle random noncommuting gates whose response maps share inaccessible conditional paths.

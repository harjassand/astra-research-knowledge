# Exact boundaries and finite checks for the coherent extension

16 October 2026. These are exact small-matrix statements. They falsify proof
shortcuts, rather than establish an impossibility of coherent-error memory.
Run `python3 coherent_frontier/check_exact_coherent.py` from the campaign
directory. The rational/algebraic receipt is EXACT_CHECKS.json.

## 1. Hamiltonian drift is not a finite-rate channel proposal by itself

Let H=hX on one qubit, h>0. If -i[H,.]=r(N-Id), then necessarily

    N = Id - i(h/r)[X,.].

Write a=h/r. Compress its normalized Choi matrix to the orthonormal Bell
vectors |Phi> and (X tensor I)|Phi>. The compression is

    [ 1    i a ]
    [-i a   0  ],

with determinant -a^2<0. Therefore N is not completely positive for any
finite r. An argument that treats an arbitrary coherent generator as an
ordinary rare CPTP kick without adding a CP interior is invalid.

## 2. The same shortcut fails for a physical nonunitary Lindbladian

Let F=|0><1| and E=gamma D[F], gamma>0. If E=r(N-Id), then N=Id+aD[F] with
a=gamma/r. In output-first computational Choi order,

    J(N) = [ 1/2     0     0     1/2-a/4 ]
           [ 0       a/2   0       0     ]
           [ 0       0     0       0     ]
           [ 1/2-a/4 0     0     1/2-a/2 ].

The principal 00/11 minor is -a^2/16<0. Every finite-rate proposal fails
complete positivity, although exp(tE) is a valid amplitude-damping channel
for every t>=0. Complete positivity of the continuous semigroup does not
imply complete positivity of Id+E/r.

## 3. Completing correction proposals changes the quantum generator

Use a two-level syndrome toy with Pi_0=|0><0|, Pi_1=|1><1|, and active jump
J=X Pi_1=|0><1|. The original generator is D[J]. The completed proposal
uses Kraus Pi_0 and J, and has generator C-Id=D[J]+D[Pi_0].

On |0><1| the original derivative is -|0><1|/2, while the completed derivative
is -|0><1|. Their population equations agree exactly. Thus equality on
definite-syndrome Pauli densities cannot establish equality on coherent
cross-syndrome operators. The theorem deliberately uses a modified generator.

## 4. Positive Pauli-mixture closure fails, without implying a no-go

The rational unitary U=(3/5)I-(4i/5)X sends |0><0| to

    [ 9/25    12i/25 ]
    [-12i/25  16/25  ].

Every Pauli conjugate of |0><0| is diagonal, so no positive Pauli mixture
equals this output. The regularized theorem does not assert such a mixture:
it expands each Kraus operator coherently and uses exact correction of its
whole Pauli span on a common good proposal schedule.

## 5. Exact positive example of the floor identity

Take a one-qubit patch with nu=1,

    E = -i[(1/32)X,.] + (1/32)D[|0><1|],
    D(A) = Tr(A)I/2,
    N = D+E.

The sufficient diamond-norm estimate is

    ||E||_diamond <= 2/32+2/32 = 1/8 < nu/d^2 = 1/4.

The normalized Choi matrix of N is exactly

    [ 1/4    i/64    i/64   -1/128 ]
    [-i/64   17/64    0     -i/64  ]
    [-i/64    0       1/4   -i/64  ]
    [-1/128  i/64     i/64   15/64 ].

Its four leading principal minors are

    1/4, 271/4096, 4319/262144, 16039/4194304,

all strictly positive. The script also checks trace preservation and the
generator identity (D-Id)+E=N-Id on all matrix units. Thus this example
contains genuine continuous Hamiltonian and nonunitary drift, absorbed by an
actual depolarizing floor, with no small-time approximation.

## 6. Exact code/reference algebra and coherent cancellations

The executable constructs the [[5,1,3]] stabilizer code with generators
XZZXI, IXZZX, XIXZZ and ZXIXZ, its rank-two projector, a two-column encoding
isometry V, all 16 syndrome projectors and the perfect Pauli recovery.
For each recovered Kraus record A it checks the *operator* equality

    A V = c V,

and checks sum |c|^2=1, for a coherent one-qubit unitary, amplitude damping,
and their composition on the same support. This equality already includes
an arbitrary untouched reference. It is stronger than checking selected
logical input states, but remains a finite sanity check rather than a
verification of the asymptotic 4D proof.

For a stabilizer S, (I-S)V/2=0 exactly, whereas (I+S)V/2=V. Pauli summands
with identical syndrome can cancel or reinforce. The unitary

    U_S = (3/5)I-(4i/5)S

acts on the code as the scalar 3/5-4i/5 of modulus one. Summing absolute
Pauli coefficients gives 7/5 per step and (7/5)^n after n steps, despite
the actual operator norm remaining one. An absolute-weight proof can create
an artificial exponential normalization loss from perfectly harmless
coherent histories. The scalar-Kraus proof retains these sums until after
recovery, where trace preservation fixes their total squared weight.

## 7. Precise remaining frontier for the unregularized construction

This work proves an open local-generator neighborhood of the modified,
depolarization-regularized CPTP sweep. It leaves coherent stability of the
original generator, or of the completed sweep without a noise floor, open.

For the latter, there is a precise candidate missing estimate. Expand
exp[T(G_C+sum_x E_x)] by perturbation insertions between the completed
Poisson correction channels. For finite L,T this series is absolutely
convergent. Decompose every local insertion into Pauli left/right actions;
attach the same support-birth envelope to its location and keep all complex
coefficients and correction Kraus records. Group terms by whether that
common envelope reaches the first macroscopic escape. Every nonescaping
group recovers to a scalar multiple of the identity superoperator by the
same error-span proof. Let B_(L,T) be the sum of all escaping recovered
terms, without replacing their coefficients by absolute values.

The sufficient missing bound is

    ||B_(L,T)||_diamond
        <= C L^4(1+kappa T)exp(-cL)

uniformly for fixed local support and ||E_x||_diamond<=epsilon kappa, with
positive constants independent of L,T. Trace preservation would then imply
the desired decoded bound with at most a factor two. A raw absolute Dyson
estimate instead pays exp(T sum_x ||E_x||)=exp(O(epsilon kappa L^4 T)).
The original classical LSS/HT bound does not, by itself, remove this factor.

For the uncompleted original correction generator, the non-scalar no-jump
terms must additionally be included in such a bound. Neither the one-qubit
Choi obstructions nor the absence of a positive Pauli-mixture representation
falsifies a memory theorem for those generators. They only falsify the
specific uniformization shortcuts.

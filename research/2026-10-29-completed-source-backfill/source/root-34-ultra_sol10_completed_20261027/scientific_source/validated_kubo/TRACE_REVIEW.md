# Independent substantive review of the parent trace interface

Reviewed whole sources, read-only:

* `../parent/validated_twist_trace/PROOF.md`;
* `../parent/validated_twist_trace/certify.py`;
* `../parent/validated_twist_trace/TRACE_CERTIFICATE.json`.

**Disposition: ACCEPTED at the finite physical trace-enclosure scope.**
No mathematical correction to the claimed generic theorem or its literal
four-site source scope was needed. This is a review of the argument and
implementation contract; the separate Kubo extension has its own actual
physical calculation and exact-projector comparator in this directory.

## Generic argument

The condition ||V*V-I||<=epsilon<1 proves a full square V is invertible,
so its polar factor is a unitary on the entire physical block. The supplied
epsilon<=1/2 bound suffices for
||(V*V)^(-1/2)-I||<=epsilon: the worst lower-end deviation is
(1-epsilon)^(-1/2)-1, which is at most epsilon on this interval. The
upper-end deviation is smaller. Multiplication by ||V||<=3/2 gives the
advertised 3epsilon/2 bound.

The algebra H0U-U Lambda=R+H0(U-V)-(U-V)Lambda proves the claimed delta;
there is no missing factor ||V^-1|| on R, since R itself already has the
correct H0V-VLambda definition. Right multiplication by U* preserves
norm. The resulting Hermitian matrices H and U Lambda U* can be compared
by sorted Weyl eigenvalues. Summing their exponentials gives exactly the
reported two-sided e^(+/-beta delta) multiplicative trace bracket. No
eigenvector-gap, eigenvalue simplicity, eigenpair residual independence,
or Ritz completeness assumption is hidden.

Hermitian Gram/H0 row sums of |Re|+|Im| dominate their operator norms.
For the general residual, max(||R||1,||R||infinity) dominates
sqrt(||R||1 ||R||infinity), so the selected row/column bound is valid.
All exact matrix products are performed only after `.astype(object)`;
the Python integer products do not inherit an int64 or BLAS overflow
contract. The initial finite proposal storage is small enough for this
demonstration and is not itself an accuracy assertion. A bad solver
proposal gives a weak certificate or fails the Gram precondition.

The positive Taylor tail has the correct next term and geometric ratio.
Reduction to x<=1/2, outward squaring, and reciprocal endpoint reversal
enclose every scalar exponential. Integer floor/ceiling operations have
the correct direction. The lower trace divides by the **upper** bound
for e^(beta delta); the upper trace multiplies by that upper bound.
Only this upper growth bound is required for the reported bracket.

## Literal physical Hamiltonian

The product basis m_i=-2,...,2 has all 5^4=625 states. The listed
magnetization sectors -8,...,8 have dimensions

    1,4,10,20,35,52,68,80,85,80,68,52,35,20,10,4,1.

The Hamiltonian is the four-site **periodic spin-two** Heisenberg sum,
with a closing XY phase (3+4i)/5. Each undirected bond has SzSz diagonal
m_i m_j and both directed ladder terms. The 1/2 in the XY interaction
is present through division of the ladder-product radicand by 4.
Spin-two ladder factors are 2 or sqrt(6), so these hop amplitudes are
2, 3 or sqrt(6). The closing forward/reverse phases are conjugates and
have unit modulus exactly. The code verifies the rounded Hermitian
matrix, and the interval construction encloses the unrounded algebraic
matrix entry by entry. There is no physical approximation to sqrt(6).

The row sum of maximum absolute real/imaginary entry interval errors
dominates ||H-H0||. The exact full controls Tr H=0 and Tr H^2=30000 agree
with an independent physical bond calculation: a spin-two bond has
Tr[(S_i dot S_j)^2]=300 in dimension25, and the other two sites multiply
this by25. Four bond squares give 30000; distinct bond cross traces
vanish because a spin operator has trace0, and the unit closing phase
does not change the Hilbert-Schmidt bond norm. The actual code also
checks that the sqrt(6) coefficient in Tr H^2 is zero.

The parent JSON rational interval is the mathematical output. Displayed
decimals, relative width about2.66e-8, maximum delta about4.46e-9 and
about1.21 seconds are a finite-model report. No six-site cost or memory
estimate is established by those numbers.

## Independent replay and a proved strengthening

`review_controls.py` reuses only the producer's reviewed exact physical
builder, read-only. It supplies new solver proposals and recomputes the
Gram, residual, polar error and scalar enclosure using this directory's
independent validation implementation. The producer's `certify_block` is
never called, and its outputs are not written. Every original sector's
eta,epsilon,residual and delta is exactly reproduced. The complete
625-state trace and physical trace controls pass again.

`PROOF.md` Section1 additionally proves, by a positive Sylvester equation,
the stronger Hermitian bound

    ||H-U Lambda U*|| <= eta+residual/(1-epsilon).

On the same proposals, the resulting exact rational interval has displayed
endpoints [5.245258943309217e25,5.245258964625708e25], relative width about
4.063954145e-9 and maximum delta about7.019378456e-10. It is contained in
the parent interval and is about6.5498 times narrower. This changes the
error estimate without requiring an improved eigensolver proposal. The
replay, including both estimates, took about1.124 seconds; this is not a
timing advantage claim. Exact endpoints and all sectors are recorded in
`CONTROL_REPLAY.json`.

## Boundaries of acceptance

The full 625-state trace includes every magnetization sector explicitly;
there is no unverified negative-sector degeneracy multiplier. It is a
finite physical trace at one exact twist. Angular alias enclosures and
the source spin-character interpretation are separate upstream inputs;
the trace certificate does not validate either by itself. A plain trace
does not supply a Kubo correlation, a source higher form, a later
connected thermal input, a spectral gap, or a practical speed advantage.
The parent proof preserves these scope boundaries.

The Kubo extension in `PROOF.md` supplies the previously missing
observable transport and trace-weighted error operation. Its independent
dimer projector controls validate that implementation at a small actual
physical input; they do not upgrade the four-site trace into an unacquired
larger source family.

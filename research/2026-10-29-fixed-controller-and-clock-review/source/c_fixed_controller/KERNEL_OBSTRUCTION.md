# What finite dephasing fails to classicalize exactly

29 October 2026. An all-time analytic admission obstruction, not a memory
counterexample for the recursive family and not a finite-order Zeno model.

## 1. Exact local return kernel

For commuting H0 and one charged Hermitian Pauli P, fix a syndrome vector
|sigma,l>. The span of that vector and P|sigma,l> is invariant under H0+eps P
and stabilizer dephasing. Suppose P flips m checks and the two energies differ
by Delta. The block Hamiltonian is, up to a scalar,

    H_block=(Delta/2)Z+eps X.

If each flipped check dephases with Gamma D_S, the off-diagonal decay rate
is gamma=2Gamma m. Starting from one endpoint population, the Bloch equations
are EXACT:

    x'=-gamma x-Delta y,
    y'=Delta x-gamma y-2eps z,
    z'=2eps y,
    (x,y,z)(0)=(0,0,1).

Eliminating x,y gives the full Volterra equation and Laplace transform

    z'(t)=-4eps² integral_0^t e^[-gamma(t-s)]
                             cos[Delta(t-s)] z(s) ds,
    zhat(p)=1/{p+4eps²(p+gamma)/[(p+gamma)²+Delta²]}.        (1)

For Delta!=0 the kernel has negative lobes at every finite gamma. Even at
Delta=0 it has a finite memory width and z'(0)=0. A nonzero constant-rate
classical two-state Markov chain instead has a nonzero initial population
derivative. Thus this population evolution is not exactly the claimed
time-homogeneous Pauli jump semigroup. A low-frequency approximation would
give a z-decay rate 4eps²gamma/(gamma²+Delta²), but (1) retains the entire
frequency dependence and no such approximation is used as a theorem.
Neither negative projected kernels nor this initial derivative exclude all
larger hidden-state classical realizations; that stronger claim is not made.

## 2. CSS sector separation is a different additional condition

For two independent stabilizer flags s_X,s_Z in {+1,-1}, use unit-check
energy H0=(1-S_X)/2+(1-S_Z)/2 and a local Pauli flipping both. Then
Delta=s_X+s_Z, so (1) depends on the other sector even when one sector's
initial syndrome is fixed. In particular, for the flip probability p=(1-z)/2,

    p(t)=eps²t²-(gamma eps²/3)t³
          +[eps²(gamma²-Delta²)/12-eps^4/3]t^4+O(t^5).

The same-sign and opposite-sign flags have different Delta² (4 and 0),
and their probabilities differ by -eps²t^4/3+O(t^5), for EVERY finite Gamma.
Analyticity establishes a genuine mismatch for sufficiently small positive
t; this is an exact nonclosure result, not a truncated approximation.

Randomly changing the sign of eps does not change this probability. Even
ideal full Pauli-frame compilation which preserves the nominal H0 while
sign-randomizing this sole perturbation therefore does not remove the
joint-sector detuning. One must not call such a compiled channel a member
of the sector-separable class merely because its Kraus operators have the
form Pauli times a function of all stabilizers.

Drechsler--Oreg--Aharonov 2610.05589, Definition 2.35, additionally requires
each marginal sector-probability operator to belong to that sector's own
stabilizer algebra. The joint-dependent probability above fails that precise
condition. The local two-flag algebra is an admission counterexample to a
generic implication, not an asserted independently assignable sector pattern
inside every large code. Applying it to a specific constrained code requires
checking the relevant two valid syndrome patterns; that is not assumed here.

Importantly, the energy-neutral hopping in PROOF.md can itself couple sectors
and need not obey this separation condition, while remaining covered by the
fixed-stationary-state GNS argument. Sector separation is sufficient in that
primary framework, not necessary for quantum memory.

## 3. Adding a nominal thermal pair does not restore its Gibbs state

The same exact two-level analysis includes a genuine thermal recovery pair
with transfer rate b toward z=+1 and a toward z=-1. With the Hamiltonian
sign above, nominal Gibbs balance is b/a=exp(-beta Delta). Put r=a+b,
z_eq=(b-a)/(a+b), and let gamma include the extra coherence damping r/2. Then

    z'=-r(z-z_eq)-4eps² integral_0^t
                     e^[-gamma(t-s)]cos[Delta(t-s)]z(s)ds.

The exact stationary solution is

    z_infinity=r z_eq/[r+4eps²gamma/(gamma²+Delta²)].       (2)

At nonzero detuning and nonzero thermal polarization, this differs from the
nominal Gibbs value for every finite gamma and nonzero eps. This is an
all-orders local example of the nonequilibrium population change left by
charged coherent noise; it does not prove destruction of a many-body memory.
Its apparent symmetric heating term is not automatically a Gibbs perturbation
with a locally qualified effective temperature.

## 4. The surviving research question

Finite stabilizer dephasing may suppress coherent excursions and is a plausible
ingredient. Equations (1)--(2) show what it does not provide for free: an exact
Markov Pauli law, independent CSS-sector transition probabilities, or the
nominal/perturbed Gibbs stationary state. Kessler's dissipative SW expansion
and continuous-QEC Zeno estimates are ordinary predecessors; a finite-order
rate with an O(nt) remainder cannot establish an exp(c n^alpha) memory.

The unpaid resource is a dimension-uniform control of decoder-bad occupation
under the joint-syndrome nonequilibrium evolution, or a space-time excursion
bound that remains valid for the whole storage interval. Neither this local
obstruction nor the positive neutral theorem proves that such control is
impossible. The full arbitrary charged-error target remains NOT ACHIEVED.

# Preserved positive alternatives and receiving obstruction

## Exact free Gaussian-bath fast forwarding (earned subroutine, established machinery)

For a passive drift A=-iH-ell ell^dagger/2, F(t)=exp(At) is a contraction. The exact free auxiliary Lindblad channel has the passive vacuum dilation

    b_out=F(t)b_in+[I-F(t)F(t)^dagger]^(1/2) v_in,

with fresh vacuum modes v. An SVD of F implements this by passive mode rotations and M beam splitters; the complementary outputs are discarded. This is valid on arbitrary system-entangled, non-Gaussian auxiliary inputs, not merely on Gaussian states. Acquiring the M-by-M matrix and decomposition is an actual paid scalar/matrix computation, not an exponentially large Fock matrix. Implementing passive optics on binary encoded Fock registers still costs gate synthesis and a charged number cutoff. This is standard linear quantum systems machinery, not a novelty claim.

The unresolved operation is efficient composition with the simultaneous noncommuting Q(c b+b^dagger c^dagger) interaction. Exact free-bath macrosteps do not commute with this interaction. A naive splitting bound still pays the fast auxiliary rates and high-frequency scale. A Hamiltonian interaction picture removes the free H frequency but does not invert a dissipative channel as a CPTP map. A nonpositive inverse is not an available simulator.

The accepted Astra N1510 finite-bit retained-boson compiler has a distinct interface: independent strictly positively damped modes, diagonal known number frequencies and supplied bounded system insertion encodings. The new realization uses an off-diagonal number-preserving H and rank-one damping, with undamped individual coordinates coupled coherently to the loss port. A nonunitary diagonalization of A is not a canonical bosonic change of variables. Therefore its logarithmic microscopic-rate resource claim cannot be received unchanged. No correctness of N1510 or N675 is being reopened.

Promising next operation: a rate-robust retained-memory compiler that combines exact Gaussian free propagation with a bounded number of genuine interaction events, including all lost-field coherences and complete-isometry normalization. Dyson or LCU expressions alone have an exponential normalization unless this is earned. No such source/path oracle is supplied in the present construction.

## Finite-temperature one-frequency interpolation

The explicit two-mode spectrum has ratio

    S_1(-w)/S_1(w)=[(a-w)/(a+w)]^2.

At one desired w0>0 and beta>0, choose a=w0*coth(beta*w0/4). This gives the exact thermal ratio exp(-beta*w0), while retaining the same exact free-bath commutator. Its broad noise profile is not the target thermal bath. A multi-frequency rational majorant of w*coth(beta*w/2) with certified costs remains a possible extension; a truncated Matsubara expansion by itself may violate global positivity, and exact global KMS for finite rational spectra is impossible.

## Online causal bath rotations

The initially considered alternate mechanism was to rotate retained bath modes at time cuts, discard modes orthogonal to all future couplings, and admit fresh vacuum combinations. Exact orthogonality would justify discarding a past mode even when it is entangled with the system. Approximate low rank of the whole two-time kernel is not by itself a bound on operational past/future memory. Recent low-rank Gaussian kernel constructions already cover the basic finite-rank-to-physical-bath direction; see Chen-Cai arXiv:2610.29372. A causal memory guarantee or asymptotic advantage is not established here. Preserve this as an alternate mechanism rather than assert a second invention.

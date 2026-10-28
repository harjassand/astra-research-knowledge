# A new zero-time-frequency source message operation

Shift all event times of a history by tau modulo beta and re-sort cyclically,
keeping labels attached. This preserves the labelled simplex measure. Call
the unitary action V_tau. Simultaneous translation of both incident histories
cyclically permutes their merged word, so trace cyclicity proves

    k_beta(V_tau x,V_tau y)=k_beta(x,y), [J_beta,V_tau]=0.

The action commutes with rotations and event-count fugacities. Its average
P0=beta^-1 integral V_tau d tau is an orthogonal zero-frequency projection.
This acts on source trial functions, not on the physical Gibbs state.

The spin1 boundary message f_alpha=Tr[G_alpha times the history word] has
its insertion at time0 and is generally not time-invariant. Put g=P0f.
Idempotence and commutation imply

    <g,J^r g>=<f,J^r P0f>.

Only ONE relative-time integral remains. The open-chain contraction gives

    <g_z,J_beta^r g_z>=-1/(beta*5^r) integral_0^beta
      Tr[SzL exp(-tau H_open,r+2) SzR exp(-(beta-tau)H_open,r+2)]d tau.

The sign is i^2 from the two G insertions. For A_source=-J, power r adds
(-1)^r. This is a new source function, not another optimizer in the old
fixed16-vector span. Scalar vacuum/Krylov messages were already invariant,
so their improvement is not supplied for free.

For projected fugacity messages P0u_r and A_source P0u_r, a form power
p=d+e+q, q=0,1,2, requires an open p+2-site dimensionless Hamiltonian with
couplings(beta*r*s) ifp0, or(beta*r,beta,...,beta,beta*s) ifp>=1. Evaluate
the Kubo integral on[0,1]; there is NO extra beta factor after this rescaling.
Thus full Gram, Rayleigh and SECOND forms need at most six physical spins.
Every physical magnetization sector is included.

For H_eff eigenvectors and energies E, the exact spectral integral is

    C_H(A,B)=sum_ab A_ab B_ba L_ab,
    L_ab=(exp(-E_a)-exp(-E_b))/(E_b-E_a), L_aa=exp(-E_a).

The code uses the stable form exp[-(E_a+E_b)/2]sinhc[(E_a-E_b)/2]. Observables
are A=SzL,B=SzR with norm2 each. Source moments are -C_H/5^p, times(-1)^p.
Complete numerical eigensystems are used; no physical trace errors are
certified. Gram conditioning and all source costs are recorded.

All NONZERO time-frequency source modes remain in the FULL spin1 sixth
moment used for deflated tails. No unacquired zero-frequency moment or free
division by frequency degeneracy is assumed.

Uniform beta3 projected two-vector preview gives Rayleigh303807.73 and
variance2.019e9, versus equal-time277951.22 and8.195e9. Three fugacities
give308428.09 and8.732e8. One authorized wider nested five-fugacity family
gives308459.65 and8.597e8, with bounded minres8.420e8. Its Gram condition
is2.65e5. The identical ten-vector equal-time span, evaluated from the SAME
physical eigensystems, gives291895.26 and6.161e9. The gain from six to ten
projected vectors is only about1.018, so breadth is saturating.

A Hermitian trace-only acquisition interface also exists: if
Z(x,y)=Tr exp[-H_eff+xA+yB], then C_H=partial_x partial_y Z(0,0).
The central mixed difference from four traces(+/-h,+/-h), divided by4h^2,
has explicit remainder at most

    4 Z(0,0){[sinh(2h)/(2h)]^2-1}.

Dyson/Schatten Holder bounds each derivative by Z(0,0)2^(a+b); summing the
retained odd-odd terms excepta=b=1 proves this bound. Absolute trace errors
delta_j add sum delta_j/(4h^2). No such field acquisition was performed.
The separately owned validated-Kubo interface may give a sharper route.

These mathematical interfaces are acquired. Their recorded thermal values
are numerical previews; no later connected input or practical advantage is
claimed. Projection, Kubo response and Galerkin methods are ordinary tools;
no historical-priority claim is made for them.

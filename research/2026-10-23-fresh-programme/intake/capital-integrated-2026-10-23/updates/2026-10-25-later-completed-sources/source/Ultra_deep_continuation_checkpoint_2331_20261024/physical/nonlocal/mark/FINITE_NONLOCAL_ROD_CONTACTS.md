# Finite distributed-rod contacts for the positive nonlocal kernel

This note replaces each ideal point-spring link in `thermal/NONLOCAL_KERNEL_CONSTRUCTION.md` by a finite-inertia axial rod, attaches explicit local-rod leads, and gives the exact two-port transmission calculation. It is an ideal scalar elastic-network construction. Routing, crosshead mass, transverse modes, and fabrication are not included.

## Finite network and material assignment

Take $L\geq N$ backbone nodes, indexed $i=1,\ldots,L$, with spacing $a$ and point mass $M$ per node. For every pair $i<j$ with $n=j-i<N$, install one independent axial rod of length

\[
\ell_n=na,\qquad \kappa_n=c_N(N-n),\qquad
EA_n=\kappa_n\ell_n,
\]

where $c_N=12K/[N^2(N^2-1)]$, as in the point-kernel construction. The static axial stiffness of this rod is exactly $EA_n/\ell_n=\kappa_n$. Use common modulus $E$, density $\rho$, and wave speed $c=\sqrt{E/\rho}$, with area $A_n=EA_n/E$. Thus the line mass is $\rho A_n=EA_n/c^2$, and its full rod mass is

\[
m_n=\frac{EA_n\ell_n}{c^2}=\frac{\kappa_n n^2a^2}{c^2}.
\]

All rods meet at welded, scalar-displacement backbone nodes. This is a finite graph of distributed rods, rather than a massless realization of \(\kappa_n\). Geometrically routing many rods through common stations would require an actual crosshead/parallel-lane design; that hardware is not silently counted as zero here.

At each end attach a half local rod of length \(a/2\) and rigidity \(EA_0=Ka\). Attach its outer end directly to a semi-infinite local rod lead with the same \(E,\rho,A_0\). The half-rod and lead therefore have the same wave impedance

\[
Z_0=\frac{EA_0}{c}=\frac{Ka}{c}.
\]

There is no area or impedance step at the port plane. The two contact rods have total length \(a\), mass \(Ka^2/c^2\), and static stiffness \(2K\) each when their outer endpoint is clamped. Reflection from the finite sample remains and is calculated; “matched” describes only the contact-to-lead material transition.

## Exact finite dynamic-stiffness assembly

With time dependence \(e^{-i\omega t}\), a uniform rod of length \(\ell\), rigidity \(EA\), and speed \(c\) obeys \(u''+(\omega/c)^2u=0\). Eliminating its interior field gives the endpoint dynamic-stiffness matrix

\[
D_e(\omega)=\frac{EA(\omega/c)}{\sin(\omega\ell/c)}
\begin{pmatrix}
\cos(\omega\ell/c)&-1\\[-2pt]
-1&\cos(\omega\ell/c)
\end{pmatrix}.
\]

Its zero-frequency limit is \((EA/\ell)\bigl(\begin{smallmatrix}1&-1\\-1&1\end{smallmatrix}\bigr)\), so the prescribed static spring is recovered. The matrix is meromorphic: its apparent poles at \(\omega\ell/c\in\pi\mathbb Z\setminus\{0\}\) are internal standing-wave resonances of the eliminated rod, not missing frequency bands.

Use port nodes 0 and \(L+1\), and backbone nodes 1 through \(L\). Assemble one \(D_e\) for each rod (i,j), including the two half-rod contacts, into an \((L+2)\times(L+2)\) matrix \(D(\omega)\), then subtract \(M\omega^2\) from each backbone diagonal. Let \(P=(0,L+1)\), \(I=(1,\ldots,L)\). Away from element poles, eliminating the backbone displacements gives the exact two-port matrix

\[
D_{\rm port}=D_{PP}-D_{PI}D_{II}^{-1}D_{IP}.
\]

For the time and force convention above, an outgoing wave in either semi-infinite lead contributes the boundary dynamic stiffness \(D_{\rm lead}^{\rm out}=-i\omega Z_0\). Therefore

\[
D_{\rm eff}=D_{\rm port}+\operatorname{diag}(D_{\rm lead}^{\rm out},D_{\rm lead}^{\rm out})
=D_{\rm port}-i\omega Z_0 I_2,\qquad G=D_{\rm eff}^{-1}.
\]

The scalar energy-flux transmission is

\[
T(\omega)=\Gamma_L\Gamma_R|G_{0,L+1}|^2
=4\omega^2Z_0^2|G_{0,L+1}|^2,\qquad \Gamma_L=\Gamma_R=2\omega Z_0.
\]

Indeed, for unit incidence from the left, matching the incident plus reflected wave on the left and the outgoing wave on the right gives \(D_{\rm eff}u=-2i\omega Z_0(1,0)^T\). Thus \(u=-2i\omega Z_0G(1,0)^T\), and the right-going transmitted amplitude is \(t=u_{L+1}\). Identical leads give the stated flux ratio \(|t|^2\).

For this lossless one-channel sample, the corresponding reflected flux is \(1-T\), so \(0\leq T\leq1\). To retain rod poles, evaluate the assembled response by the retarded limit \(\omega\mapsto\omega+i0^+\), or use the nonsingular rod transfer matrix and take the same limit. Coincident rod poles may require the full interior-field/transfer formulation before taking the limit. No rod pole is deleted from a frequency integral.

## Material and static-resource ledger

For \(L\geq N\), the interior nonlocal rods have

\[
\begin{aligned}
\#\text{rods}&=\sum_{n=1}^{N-1}(L-n),\\
\text{total length}&=a\sum_{n=1}^{N-1}(L-n)n
=a\,\frac{N(N-1)(3L-2N+1)}6,\\
\sum_{\text{rods}}\text{static stiffness}
&=\sum_{n=1}^{N-1}(L-n)\kappa_n
=\frac{2K(3L-N-1)}{N(N+1)},\\
\text{rod mass}&=\frac{a^2}{c^2}\sum_{n=1}^{N-1}(L-n)n^2\kappa_n
=\frac{Ka^2}{c^2}\left(L-\frac{3N}{5}+\frac{2}{5N}\right).
\end{aligned}
\]

The mass uses the \(n^2\) rod-length factor. Counting only \(\sum\kappa_n\) would miss the distributed-connector material. Add the two contacts: total rod length increases by \(a\), rod mass by \(Ka^2/c^2\), and each contact has static stiffness \(2K\). The finite endpoint stiffness is a separate graph-compliance quantity, not the sum above.

The resource comparator is a local chain of \(L-1\) full rods, each length \(a\) and rigidity \(Ka\), with the same two half-rod contacts and the same semi-infinite leads. It spans the same distance \(La\), uses the same \(E,\rho,c\), and has total rod mass \(LKa^2/c^2\), including contacts. To match total mass exactly, set its \(L\) point masses to

\[
M_{\rm loc}=M-\frac{\Delta m}{L},\qquad
\Delta m=\frac{Ka^2}{c^2}\left(\frac{3N}{5}-1-\frac{2}{5N}\right),
\]

provided \(M_{\rm loc}>0\). If point masses are instead held equal to \(M\), the local comparator contains \(\Delta m\) more total mass. This matching is explicit; it does not match the point-mass distribution. The local chain's interior static-stiffness sum is \((L-1)K\), whereas the nonlocal sum is the expression above. Those are not equal resource budgets. Both infinite point-kernel models have the same long-wave stiffness \(\sum n^2\kappa_n=K\), but finite endpoint stiffnesses differ.

## Checked finite illustration

Set \(a=c=M=1\), \(K=0.1\), \(N=4\), and \(L=12\). Then \((\kappa_1,\kappa_2,\kappa_3)=(0.015,0.010,0.005)\), \(EA_n=(0.015,0.020,0.015)\), and \(Z_0=0.1\). There are 30 interior nonlocal rods and two contact rods. Their interior length is \(58a\), interior mass is \(0.97\), and interior stiffness sum is \(0.31\). Adding contacts gives total rod length \(59a\) and mass \(1.07\). The local chain has total rod length \(12a\) and rod mass \(1.20\); its mass-matched point masses are \(M_{\rm loc}=0.9891666667\), giving total sample mass \(13.07\) for either system.

Static elimination of the 12 backbone nodes gives finite end stiffnesses

\[
K_{\rm end,nl}=0.0665296065K,\qquad
K_{\rm end,loc}=K/12=0.0833333333K.
\]

These include the half-rod contacts. Thus the mass-matched local chain is statically stiffer in this fixture. The following values use the exact finite dynamic-stiffness assembly and matched leads; frequencies are in units \(c/a\):

| \(\omega a/c\) | Nonlocal \(T\) | Local \(T\) |
|---:|---:|---:|
| 0.001 | 0.9966681 | 0.9964918 |
| 0.05 | 0.3668843 | 0.3447427 |
| 0.10 | 0.6025443 | 0.4409750 |
| 0.20 | 0.9851446 | 0.2904517 |
| 0.50 | \(2.09\times10^{-13}\) | 0.3075145 |

The crossing values show why the point-model bulk bandwidth alone cannot stand in for a finite two-terminal conductance. This is a single idealized scalar fixture, not an integrated thermal-transport comparison or a fabricated-device result. Lead matching, finite-sample resonances, routing, extra polarizations, and contact hardware remain separate gates.

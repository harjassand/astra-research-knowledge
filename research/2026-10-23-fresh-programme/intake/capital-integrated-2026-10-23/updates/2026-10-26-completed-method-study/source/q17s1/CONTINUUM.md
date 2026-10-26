# An ordinary tapered conductor approaches the sharp limit

The exact finite-tree theorem is in PROOF.md. This note supplies a compatible continuum realization of its large-n extremizer, not a claim that exponential RC tapering is novel. For an inspected primary antecedent, El-Moursy and Friedman (2007), *Wire shaping of RLC interconnects*, DOI https://doi.org/10.1016/j.vlsi.2006.06.002, discuss optimized exponential RC/RLC shaping for propagation delay. That objective differs from the fixed total/source-capacity RMS release-width objective here. Ordinary RC line synthesis is a strong incumbent. Kelly and Ghausi's 1964 title also surfaced in a secondary catalogue, but its full primary report was not reviewed or used in this proof.

## Limiting component measure

Let C0 be the source lump capacity, R>1 the total/source capacity ratio, tau the desired mean release time, L=log R, and

    kappa=tau/(L+2).

Use log cumulative capacity u=log(S/C0) in [0,L]. The limiting delay-contribution measure a=S dr is

    a(du)=kappa [delta_0(du)+du+delta_L(du)].

It has total mass kappa(L+2)=tau. Its normalized variance is the kernel energy

    tau^(-2) integral integral exp(-|u-v|) a(du)a(dv).

For every u in [0,L],

    exp(-u)+exp(-(L-u))+integral_0^L exp(-|u-v|)dv = 2.

The energy is therefore 2/(L+2), precisely the n->infinity infimum. The two atoms correspond to ordinary finite contact resistances; omitting them does not implement the optimum.

## Physical geometry within the one-dimensional Fourier model

Let a homogeneous conductor have constant conductivity k>0, volumetric heat capacity c_v>0, and diffusivity alpha=k/c_v. Define

    ell=sqrt(alpha*kappa),     length d=ell*L,
    A(x)=C0/(c_v*ell) * exp(x/ell),     0<=x<=d.

The source reservoir C0 is joined to x=0 by resistance r_left=kappa/C0. Join x=d to the fixed-temperature bath by r_right=kappa/(R*C0). Insulate the sides. The rod's cumulative capacity, including the source, is

    S(x)=C0+integral_0^x c_v A(y)dy=C0 exp(x/ell).

Thus its capacity is (R-1)C0. Its differential axial resistance is

    dr=dx/[k A(x)]=kappa dS/S^2,

as required by the limiting measure. This construction needs ordinary reciprocal conduction, positive source/storage capacities, two fixed contact resistances, and the initial source-only preparation. It does not require a directed thermal transfer, a detector, a powered switch, or a threshold actuator.

The governing continuum equation is

    c_v A(x) T_t = [k A(x) T_x]_x,

with the source-lump balance and contact boundary conditions above. The one-dimensional approximation requires transverse thermal equilibration to be faster than axial evolution and negligible side leakage. A slender enough geometrically similar shape can approach that regime, but no device is fabricated or experimentally validated here. Contact resistances, radiation, variation of k and c_v, and initial heating of the rod would have to be measured. The mathematical limit is not evidence that these errors are negligible in any given material device.

The construction is a way of approaching the bound, not a route around its poor resource scaling. For R=100, even the continuum infimum has CV=sqrt[2/(2+log 100)] approximately 0.5503.

## Exact transfer function for further independent evaluation

For Laplace frequency z, put h=kappa*z and beta=sqrt(1/4+h). Solving the constant-coefficient boundary-value problem in u=x/ell gives normalized bath-flux transform

    F(z)=exp(L/2) /
      [(1+2h)cosh(beta L) + (h^2+2h+1/2)/beta*sinh(beta L)].

The zero-frequency limit is F(0)=1. Its first two logarithmic derivatives give tau=kappa(L+2) and sigma^2=2*kappa^2*(L+2), consistent with the measure argument. For beta=0 take the continuous sinh(beta L)/beta limit. The R=1,L=0 expression reduces to 1/(1+2*kappa*z), a single exponential with mean 2*kappa=tau, corresponding to zero rod length and two series contact resistances.

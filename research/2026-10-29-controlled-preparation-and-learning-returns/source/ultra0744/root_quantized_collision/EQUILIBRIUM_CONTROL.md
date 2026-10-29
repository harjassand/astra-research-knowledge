# A paid equilibrium alternative for the same finite collision kernel

29 October 2026. Root reconstruction, independent review pending. This is
an explicit ordinary comparator, not a claim of a new equilibrium principle.
Its output is an approximation at a displayed TV tolerance. It must not be
reported as the exact transient sample contract.

Let Sigma be the random Gaussian covariance, aI<=Sigma<=bI, and let
mu=Tr E(Sigma0)/3. Put D=Sigma-mu I, M=E D and V=E||D||_F^2. The collision
updates D to A D1 A^T+B D2 B^T with independent input copies, where
A=(I+R)/2,B=(I-R)/2 and R is uniform over the four x/y quarter-turns.

The mean evolves by dM/dt=(E_R R M R^T-M)/2. On real symmetric traceless
matrices this self-adjoint operator has eigenvalues -1/4,-1/2,-3/4; hence

    ||M_t||_F^2 <= exp(-t/2)||M_0||_F^2.

For a quarter-turn about x, P=A^T A=diag(1,1/2,1/2) and Q=B^T B=I-P;
about y, P=diag(1/2,1,1/2). The signs have the same P,Q. In the sum
E_R Tr(D P D P+D Q D Q), squared diagonal entries of x,y have coefficient
3/4, that of z coefficient1/2, and every squared off-diagonal contribution
coefficient1/2. It is therefore at most (3/4)||D||_F^2.
The cross term in the independent-copy update is bounded above by
2||A M A^T||_F ||B M B^T||_F <=2||M||_F^2. Consequently

    V'_t <= -V_t/4+2exp(-t/2)||M_0||_F^2,
    V_t <= exp(-t/4)[V_0+8||M_0||_F^2] <=9V_0 exp(-t/4).

For Sigma,mu I>=aI, the elementary Gaussian relative-entropy formula and
the Taylor bound on x-1-log x give

    D(N(0,Sigma)||N(0,mu I)) <=||Sigma-mu I||_F^2/(4a^2).

Pinsker, convexity of TV under mixing, and Cauchy--Schwarz yield

    TV(f_t,N(0,mu I)) <=3sqrt(V_0)/(2sqrt(2)a) exp(-t/8).   (E1)

Integer quantization cannot increase this bound. For the declared catalog,
mu=157/150 and V0 can be computed exactly from the two rational matrices;
the conservative V0<=3(b-a)^2=3/100 already suffices. Its prefactor is less
than 1/5. Thus for any epsilon>0, t>=8log[1/(5epsilon)] pays the requested
bin-law error by using an ordinary single Gaussian with covariance mu I.
For example t>=100 is safely enough for epsilon=10^-6. The Gaussian is
sampled/quantized by the same lazy-normal and strict-ball arithmetic, not
by a finite floating approximation whose TV error is silently ignored.

No convergence rate is assumed for arbitrary collision laws or arbitrary
initial distributions. The finite four-rotation kernel and bounded Gaussian
covariance source are used explicitly throughout. The physical hard-sphere
branch has a different rate and receives no conclusion from this bound.

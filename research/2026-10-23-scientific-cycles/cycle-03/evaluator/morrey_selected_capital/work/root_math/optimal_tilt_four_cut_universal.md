# Optimal trace tilt removes the four-cut calibration restriction

Root derivation, 22 October 2026. The decisive universal tilt identity
was obtained independently and simultaneously by root and WS05. This
note includes root's minimization and singular-boundary extension.
Independent audits requested. Historical novelty is unknown.

## Universal family statement

Retain (1),(2), the physical coordinates and parameters of
`nonminimal_four_cut_family_qc.md`: a0>0, k>1, p>q>0, gamma>0,
lambda0>0, k>=p/q, s0=1+lambda0, C symmetric with eigenvalues
alpha=c0+d0>0 and signed beta=c0-d0. Impose

    lambda0*(C^2/s0-I)-M=a0*[[1,k],[k,1]],
    M=gamma*[[p^2+q^2,2pq],[2pq,p^2+q^2]],
    0<=beta^2<=s0.

Define d1=(k^2-1)a0, O=gamma*(px+qy)_+^2+gamma*(qx+py)_+^2,
Phi=O+d1*(x_-^2+y_-^2), D=Phi-z^T Mz, and F=|w+Cz|^2+D.
Then F is globally QC, using the separately proved global QC of K.
The earlier uniform lower bound Phi>=mu|z|^2 and the extra mu/r
calibration inequalities are UNNECESSARY. The conclusion includes the
boundary beta^2=s0 and either sign of beta. It covers the original
stationary extreme member and the near-beta=1 member that defeats all
homogeneous graph-vanishing skew choices.

All PC supports and mixed-sector concavity in the earlier proof depend
only on the displayed structural identity and k>=p/q; they are unchanged.
For clarity, the new global K step and the complete routing are given below.

## 1. The optimal tilt, before using the structural identity

In the orthonormal plus/minus frame put

    P=(x+y)/sqrt(2), T=(x-y)/sqrt(2),
    U=(u1+u2)/sqrt(2), V=(u1-u2)/sqrt(2), u=w+Cz.

Thus C has eigenvalues alpha,beta and
D=Phi-Mplus*P^2-Mminus*T^2, where Mplus=gamma*(p+q)^2 and
Mminus=gamma*(p-q)^2.

For a fixed positive lambda and a tilt t, take

    tau^2=lambda/(1-t^2),
    h=tau*(w_minus+t*T)=tau*[V+(t-beta)T].

Its determinant-dual value is lambda. The active K quadratic is
Q=h^2+lambda*det A. Provided 1-(1+lambda)t^2>0, completion of the
free U,V variables gives the exact residual

    D+A_lambda*P^2-B(lambda,t)*T^2,
    A_lambda=lambda*(alpha^2-1-lambda)/(1+lambda),
    B(lambda,t)=lambda*(1-beta*t)^2/[1-(1+lambda)t^2]. (3)

When beta^2<1+lambda, the unique minimizing tilt is

    t*=beta/(1+lambda),
    Bmin=lambda*(1-beta^2/(1+lambda)).                (4)

One proof of optimality is the exact nonnegative difference

    B(lambda,t)-Bmin
      =lambda*((1+lambda)*t-beta)^2
        /[(1+lambda)*(1-(1+lambda)*t^2)].

Thus forcing h to vanish on the graph (the choice t=beta) can lose
the certificate even though the optimally tilted one works.

## 2. The structural cancellation at lambda=lambda0

Set xi=beta/s0 and tau^2=lambda0/(1-xi^2). Since beta^2<=s0<s0^2,
tau is real and positive. The physical left matrix is

    L=(tau/sqrt(2))*[[1-xi,1-xi],[1+xi,-1-xi]].

It has det L=-lambda0 and skew(LA)=+/-h. Its trace is

    tr(LA)=sqrt(2)*tau*[u1+u2-(alpha+xi)(x+y)].     (5)

The eigenvalue equations of the structural identity are

    A_lambda0=Mplus+a0*(1+k),
    Bmin=a0*(k-1)-Mminus.

For beta^2<s0, the exact residual from (3) is

    D+A_lambda0*P^2-Bmin*T^2
      =O(z)+psi_k(z),
    psi_k=a0*[x^2+2kxy+y^2+(k^2-1)*(x_-^2+y_-^2)]. (6)

There is also a simpler identity that is valid at the singular
endpoint without any quotient. Put rvec=w+Cz/s0. Then

    h=tau*rvec_minus,
    F-Q=s0*rvec_plus^2+(s0-tau^2)*rvec_minus^2+O+psi_k.

The coefficient s0-tau^2 is nonnegative exactly when beta^2<=s0.
This identity follows immediately from the existing completed form
F=lambda0*det+s0*|rvec|^2+O+psi_k. Thus both the strict and singular
cases share one direct global nonnegativity certificate.

The residual O+psi_k is globally nonnegative. In the positive quadrant every term
of the unhinged expression is nonnegative. In the two mixed quadrants
psi_k is a0*(kx+y)^2 or a0*(x+ky)^2. In the negative quadrant its
matrix a0*[[k^2,k],[k,k^2]] is positive semidefinite. Thus F>=Q
globally, without a lower estimate that replaces Phi by mu|z|^2.

## 3. The singular endpoint is valid, not an omitted limit

If beta^2<s0 the free-V square coefficient is

    M_V=s0-tau^2=(1-beta^2/s0)/(1-beta^2/s0^2)>0,

so the preceding ordinary square completion applies. If beta^2=s0,
then tau^2=s0 and M_V=0. Its mixed coefficient is exactly

    N_V=tau^2*xi*(1-beta*xi)=0.

The Moore--Penrose range condition is therefore satisfied. The
uncompleted T residual is zero, exactly Bmin=0. Formula (6) remains
the exact residual; U still has the strictly positive coefficient s0.
This proves the endpoint directly. No division by a vanishing square
coefficient or unsupported passage of parameters is used.

## 4. Inactive branch and positive-quadrant contact

The minus eigenvalue identity and beta^2<=s0 give

    Mminus<=a0*(k-1)<=d1.

Exactly as in the earlier mixed-quadrant calculation, D>=0 when
x+y>=0. The plus eigenvalue identity implies alpha^2>s0, so
alpha+xi>0 even when beta<0. Formula (5) shows that the graph-trace
halfspace pi(z)>=0 is precisely x+y>=0. The full linear-skew graph
criterion in `full_skew_graph_k_criterion.md` now gives F>=K(LA).
It can also be checked directly: if F<0, moving u continuously to zero
keeps F negative and Q<=F negative, hence Sym(LA) definite; at the
graph point its trace is positive, so it stays in the active component.

On graph backgrounds u=0,x,y>=0, D=0 and the trace is nonpositive;
F>=Q forces det Sym(LA)>=0. Thus Sym(LA)<=0 and K=F=0. The explicit
translation-plus-affine correction in the full-skew criterion gives
touching global QC minorants at every background with x,y>=0 and
arbitrary u, including boundary points.

## 5. All remaining backgrounds

The structural identity also gives exactly

    F=lambda0 det+s0|w+Cz/s0|^2+O+psi_k.

The global PC function obtained by replacing psi_k with
a0*(kx+y)_-^2 lies below F, because

    psi_k-a0*(kx+y)_-^2
      =a0*[(k^2-1)*(x_-^2+y_-^2-x^2)+(kx+y)_+^2]>=0.

For x<=0 this is immediate; for x>=0,y>=0 it is the positive
unhinged form; for -kx<=y<=0 it is (x+ky)^2; for y<=-kx it is
(k^2-1)*(y^2-x^2). This support touches throughout x<=0,y>=0,
kx+y<=0. The swapped support handles the reflected sector.

Every tangent of psi_k at a negative-quadrant point is a global
affine minorant: along any segment to a point outside the positive
quadrant the Hessians are PSD; at a point in the positive quadrant the
tangent is nonpositive, whereas psi_k is nonnegative. These tangents
give global PC touchers throughout the negative quadrant.

For fixed y>0 the only uncovered interval is -y/k<=x<=0. Its
three nonconstant cuts (-px-qy,x,-qx-py) are all nonpositive by
k>=p/q. Each fixed-test hinge Jensen defect is concave in x there;
the common quadratic defect is constant. The left endpoint has the
PC toucher and the right endpoint the K toucher. Concavity proves
every actual-test gap nonnegative between them. Reflection handles
the last mixed sector. This exhausts all backgrounds and proves QC.

This is a complete theorem for the stated structural family. It
does not cover every four-cut dictionary, arbitrary nonminimal
networks, all quartics, the sharp SC grid target, or full Morrey.

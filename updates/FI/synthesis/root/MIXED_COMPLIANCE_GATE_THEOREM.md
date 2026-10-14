# A sharp spatial control condition for a mixed local and shared compliance gate

Integration-derived calculation, 14 October 2026. Historical novelty and external
correctness remain UNKNOWN. This is a theorem about an explicitly supplied gate
functional. It does not establish that a compatible elastic device realizes it.
The incoming scalar Landau construction and its work accounting are retained.

## 1. The controlled model and the question left by homogeneous calculations

Let N sites carry real order parameters q_i, and set

    f0(q)=a q²/2−b q⁴/4+c q⁶/6,
    a=3b²/(16c), b,c>0, qB²=3b/(4c).

At coexistence, f0(q)=c q²(q²−qB²)²/6>=0. Define a mixed gate

    E(q;u,h)=sum_i[f0(q_i)−h q_i]
              +theta u sum_i q_i⁴/4
              +(1−theta)u (sum_i q_i²)²/(4N),             (1)

where 0<=theta<=1 and 0<=u<=b. The parameter theta specifies the coefficient
fraction of a genuinely sitewise quartic gate; the rest is a shared gate acting
on the mean squared order parameter. It is not an acquired modulus fraction
of a fabricated frame. Both gates are nonnegative, and every homogeneous state
q_i=v has exactly the source scalar energy f0(v)+u v⁴/4−hv, independently of theta.

The source shows that theta=0 fails a spatial linear-stability test. We determine
how much local control makes the entire chosen equilibrium path globally valid,
which is a stronger question than checking its homogeneous Hessian.

Use the source three-stage path: engage u from zero to b at v=h=0; traverse
0<=v<=qB at u=b and h_v=av+cv⁵; remove u at v=qB with h=u qB³.

## 2. Sharp threshold for global optimality of the complete middle path

Put beta=(1−theta)b. For any selected v>=0 define

    D_theta(q;v)=f0(q)−f0(v)+theta b(q⁴−v⁴)/4
                +beta v²(q²−v²)/2−h_v(q−v).

Direct expansion gives the exact decomposition

    E(q;b,h_v)−E(v1;b,h_v)
      =sum_i D_theta(q_i;v)
       +beta[sum_i q_i²−Nv²]²/(4N),                       (2)

and the scalar factorization

    D_theta(q;v)=(q−v)² K_theta(q,v),
    K_theta=a/2−beta(q+v)²/4
       +c(q⁴+2q³v+3q²v²+4qv³+5v⁴)/6.                   (3)

Let

    P(t)=t⁴+2t³+3t²+4t+5,
    alpha=the unique positive root of alpha³−3alpha−8=0,
    theta_* =1−sqrt[P(alpha)/(alpha+1)⁴]
            =0.167258048943982390... .                   (4)

**Theorem.** For the admitted class of all N, every homogeneous selected state
v1 on the middle path 0<=v<=qB is a global minimum of (1) if and only if
`theta>=theta_*`. For theta>theta_* the selected middle state is unique.
There is no requirement that E be convex at every unrelated configuration.

**Sufficiency.** The bias h_v is nonnegative and the remaining potential is even.
Replacing any negative q by |q| cannot increase its energy, so it suffices to
consider q>=0. For v>0 set t=q/v and z=v². Then

    K_theta=a/2−beta(t+1)² z/4+cP(t)z²/6.

This quadratic is nonnegative for all z>=0 whenever
`beta²(t+1)⁴<=b² P(t)`, using a=3b²/(16c). Moreover

    d[P(t)/(t+1)⁴]/dt=2(t³−3t−8)/(t+1)⁵.

There is precisely one positive critical point alpha; the ratio decreases to
it and then increases. Thus (4) makes (3) nonnegative for every q,v>=0.
Equation (2) proves the global comparison. At v=0 the same conclusion follows
directly from f0>=0 and the nonnegative gate. Strict theta gives strictly
positive K at q!=v, hence uniqueness. Endpoints with u=h=0 retain coexistence.

**Necessity for an all-N guarantee.** If theta<theta_*, choose t=alpha and

    v²=3 beta(alpha+1)²/[4cP(alpha)], q=alpha v.

Then K_theta(q,v)<0. This selected v lies inside the traversed interval:
`v²/qB²=(beta/b)(alpha+1)²/P(alpha)<1`. Put one site at q and the other N−1
sites at v. Its total energy difference is

    D_theta(q;v)+beta(q²−v²)²/(4N),                       (5)

which is negative for sufficiently large finite N. Therefore the selected
homogeneous state fails global optimality even though its scalar branch
continues to exist. This proves necessity within the stated admitted class.
It is not a theorem that every specific finite sample fails below (4).

## 3. Exact global engagement and removal

Gate engagement at q=0 is globally safe for every theta because both f0 and
the gate are nonnegative. During removal, set B=qB, h=uB³. The gate's tangent
remainder has the exact form

    theta u sum_i (q_i−B)²(q_i²+2Bq_i+3B²)/4
    +(1−theta)u[sum_i q_i²−NB²]²/(4N)
    +(1−theta)u B² sum_i(q_i−B)²/2 >=0.                   (6)

Adding sum_i f0(q_i)>=0 proves that B1 remains a global minimum. Thus (4)
provides the complete scalar-to-spatial path guarantee, using substantially
less sitewise control than theta=1 within this mathematical gate architecture.

Any additional quadratic gradient or graph coupling `kappa q^T L q/2`, with
kappa>=0, L>=0 and L1=0, preserves these sufficient global comparisons because
it vanishes at the selected homogeneous states and is nonnegative elsewhere.
Physical elastic compatibility does not automatically generate either gate in (1).

## 4. Three distinct spatial requirements

The full Hessian at a homogeneous middle-path state has a uniform eigenvalue
`a+5cv⁴` and N−1 transverse eigenvalues `a−2beta v²+5cv⁴`. Thus every
homogeneous middle-path Hessian is positive definite when

    theta > theta_lin=1−sqrt(15)/4
                     =0.0317541634481457787... .         (7)

This much weaker condition does not ensure global equilibrium. An exact
countermodel uses b=c=1, a=3/16, N=32, theta=1/10, selected v=1/4,
h_v=49/1024, and one alternative site q=5/8. All homogeneous Hessians have
margin at least51/2000>0, but

    D_theta(5/8;1/4)=−3969/2621440,
    E((5/8,1/4,...,1/4))−E((1/4,...,1/4))
        =−3969/5242880<0.                                (8)

This is a finite-amplitude failure of the selected equilibrium path despite
uniform local linear stability. It does not rely on a numerical optimizer.

For completeness, global convexity of the entire middle functional for all N
is a still stronger requirement. With M2=sum_i q_i²/N, its Hessian is

    diag[a−3beta q_i²+5c q_i⁴+beta M2]+(2beta/N)q q^T.

It is uniformly positive when `a−9beta²/(20c)>0`, equivalently

    theta > theta_conv=1−sqrt(15)/6
                      =0.354502775632097186... .         (9)

This threshold is sharp for an all-N convexity guarantee: with just one
nonzero site, its Hessian entry has minimum
`a−9beta²(1−1/N)²/(20c)`. Every theta below (9) therefore gives a negative
Hessian for sufficiently large N. At equality, the displayed general lower
bound is nonnegative. Hence

    homogeneous linear stability < selected global path < entire convexity.

Equation (4), rather than either outer criterion, answers the actual switching
question for the proposed mixed architecture. Circulated ideal work along
the homogeneous path is unchanged: the scalar control ports still exchange
`b qB⁴/4` in opposite directions. This theorem reduces a spatial requirement;
it does not manufacture an energy gain.

## 5. Physical implementation and evidence boundary

A general positive elastic kernel does not suffice. For
`G(q)=<q²,Jq²>/4`, the Hessian is `diag(Jq²)+2 diag(q)Jdiag(q)`.
The PSD matrix J=[[1,−1],[−1,1]] gives nonnegative energy but Hessian
`diag(3,−1)` at (1,0). Entrywise nonnegativity together with J>=0 is one
sufficient convexity condition; ordinary compatible elastic kernels need not
satisfy it. The mixed operator in (1) is a special explicit control ansatz.

The incoming material screen also uses a declared frozen Table-1 sextic
coefficient, not a validated temperature-dependent constitutive fit. Its primary
preprint contains an unresolved same-unit coefficient discrepancy. None of
(1)–(9) qualifies a BaTiO3 device, proves local shunt realizability, removes
finite-temperature state-selection/retention obligations, or establishes work
recovery efficiency, cooling performance or superiority to adaptive charge
control and multicaloric methods. The equal-free-energy stroke is not a full
thermodynamic cycle or an erasure of an unknown bit.

`mixed_compliance_gate.py` independently differentiates the functional,
checks the factorization and removal identity, isolates alpha, reconstructs
the exact32-site countermodel and verifies the homogeneous and full Hessians.
Its eight grouped checks are internal algebra only. The separate barrier
worker's delta audit reconstructs these claims rather than importing this code.

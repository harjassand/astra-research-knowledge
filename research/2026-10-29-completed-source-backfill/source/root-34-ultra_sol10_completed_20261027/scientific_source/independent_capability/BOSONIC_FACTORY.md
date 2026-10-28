# Coarse-detector photon factory: exact positive control and limits

This file develops the lossless-memory control for the supplied optical
model. The main acquired operation, including waiting loss and all failed
restarts, is in `WAITING_LOSS_PROOF.md`. No optical source, memory or useful
computational resource has been acquired physically.

## 1. Supplied source and literal operation

The raw state is number diagonal with probabilities

    (p0,p1,p2)=(99/500,4/5,1/500).

Take n independent copies in the same internal optical mode and apply a
passive interferometer whose retained output row has every entry 1/sqrt(n).
Condition each other output on a no-click result of a bucket detector with
efficiency D=19/20 and no dark clicks. Write t=1-D and let q_n(z) be the
unnormalized retained photon-number PGF. No photon-number resolving detector
is granted to this factory. The finite Fock cutoff, same-mode support and
source/detector law are supplied model inputs, not experimental findings.

Put

    F(t)=p0+p1 t+p2 t²,
    A=F(t), B=D F'(t), C=D² F''(t)/4,
    h(x)=A+Bx+Cx².

Then the exact operation is

    q_n(z)=integral_0^infinity exp(-s)
        [A+B ((z-t)/D)s/n+C ((z-t)/D)²(s/n)²]^n ds.          (1)

To see (1), the optical counting matrix is
M=t I+(z-t)ee*/n, with e the all-ones vector. Wick's Gaussian permanent
identity expresses each input Fock matrix element as a Gaussian moment.
For z>=t, realize the corresponding Gaussian variable as independent
variance-t noise plus a common variance-(z-t)/n component. Conditional on
the common component's squared modulus s, one mode contributes

    p0+p1(t+b)+p2(t²+2tb+b²/2)
       =F(t)+F'(t)b+F''(t)b²/4,
    b=(z-t)s/n.

The common squared modulus has density exp(-s). Independence of the n
remaining components gives (1). Both sides are polynomials in z, so equality
extends to all z, including z<t. This is a standard Gaussian/permanent
calculation applied to the stated circuit, not a claim of a new identity.

If c_k=[x^k]h(x)^n and T_k=c_k k!/n^k, then

    q_n(z)=sum_k T_k ((z-t)/D)^k, Z_n=q_n(1)=sum_k T_k.       (2)

All T_k are positive. With K distributed proportionally to T_k,

    E[N]=E[K]/D,
    E[N(N-1)]=E[K(K-1)]/D².                                (3)

`bucket_factory.py` computes these expressions using common-denominator
integer arithmetic. Its separate literal Fock-amplitude enumeration agrees
coefficient by coefficient at n2 with the full 0/1/2 source and at n4 with a
0/1 source. The latter fixture uses an explicit four-mode Hadamard matrix.
Those finite comparisons validate those circuits, not every asymptotic step.

## 2. Asymptotic control, and what it measures

For the admitted fixture,

    A=47601/200000, B=76019/100000, C=361/400000.

B>A and B²>2AC hold exactly. Thus f(x)=log h(x)-x is strictly concave for
x>=0, has one interior maximum x*, and tends to minus infinity. Its
stationarity condition h'(x*)=h(x*) gives

    C x*²+(B-2C)x*+(A-B)=0,
    17/25 < x* < 69/100.

Let v=(1-2C/h(x*))^(-1). Applying Laplace's method to
Z_n=n integral exp(n f(x))dx yields

    Z_n ~ sqrt(2 pi n v) exp(n[log h(x*)-x*]),
    E[N]/n -> x*/D,
    Var(N)/E[N] -> v/(D x*)-(2-D)/D.                         (4)

For completeness the moment limits follow by replacing h(x) by h(w x)
in the integral: the saddle y=w x obeys w h'(y)/h(y)=1. At w=1,
d y/d w=v, giving E[K]/n -> x* and Var(K)/n -> v-x*; (3) gives (4).
The numerical constants are mean/n -> .724195182271903 and Fano ->
.4283926022713. The code certifies the wider exact bounds

    68/95 < limiting mean/n < 69/95,
    21/50 < limiting Fano < 9/20.

For the same quadratic family under strict log concavity, B<A instead puts
the saddle at the endpoint and gives bounded thermal-limit mean
B/[D(A-B)]; B=A gives sqrt(n) scaling. For p2=0 these thresholds reduce to
p1 D=1/2 for macroscopic mean and p1 D>2/3 for limiting sub-Poisson Fano.
These results describe this analytic family, not a general optical
concentration theorem or an optimal source/detector threshold.

## 3. Retention costs and ordinary prior

For n=2m, prepare F_m on the left and retain it while independently preparing
F_m on the right. Fuse the two outputs on a balanced beamsplitter, retain
port0 only on a bucket no-click at port1, otherwise discard both and restart
F_n. A balanced binary tree has the same retained row as (1). Intermediate
herald modes are never used again, so conditioning all tree heralds gives
the same final state. The last fusion succeeds with

    s_n=Z_n/Z_m².

With one raw-source clock and one fusion clock, lossless memory gives

    C_1=T_1=1, J_1=0,
    C_n=2 C_m/s_n,
    J_n=(2 J_m+1)/s_n, T_n=C_n+J_n=(2 T_m+1)/s_n.            (5)

C counts every raw source attempt and J every fusion, including failures.
The non-recycled retention speedup is established prior:
[Motes et al., PRA94,012344 (2016), Secs.IV–V.2,
Eqs.26–29](https://arxiv.org/html/1603.00533v2) already derives the
quasipolynomial non-recycled Fock-fusion cost. Its number-resolved recycling
policy is a stronger distinct comparator. Neither ordinary protocol is
defeated here; the source model, detector and policy must match before
comparing cost. Coarse-herald Gaussification also has direct prior in
[Browne, Eisert, Scheel and Plenio,
PRA67,062320 (2003)](https://arxiv.org/abs/quant-ph/0211173).

For illustration, at n32 the ideal model gives mean 23.17549356886293,
Fano .4284230341, expected sources about 20,308 and expected clocks about
33,745. At n128 the corresponding source cost is about 11.6 million.
These are model costs, without a physical clock duration or measured
throughput. A source-attempt count is not a delivered multi-photon rate.

The ideal expected photon-clock occupation A_n obeys

    A_1=0,
    A_n=(2 A_m+E[N_m] T_m+2 E[N_m])/s_n.                    (6)

The first retained child waits through the whole second preparation; both
children then wait one fusion clock. Coupling a memory with per-clock loss
1-lambda to this ideal process gives output total-variation/trace-distance
at most (1-lambda)A_n, capped at one. This is a sufficient perturbation
bound, never a necessary lifetime threshold. At n32, A_n is about 401,721;
the crude bound is weak for lambda=.999. The separate waiting-loss compiler
calculates the actual supplied lossy model without using that bound.

## 4. Resource-quality control

For normalized output probabilities q_k the radial Wigner function is

    W(alpha)=(2/pi) exp(-t/2) P(t),
    P(t)=sum_k q_k (-1)^k L_k(t), t=4|alpha|².

`bucket_wigner.py` constructs P with exact rational coefficients, uses
Sturm root isolation and produces exact negative-point witnesses. The n2,
n4, n8 and n16 factories have 1, 2, 3 and 4 negative radial intervals,
respectively. However, 80-digit quadrature gives negative volumes

    one raw source: .1000507257127923
    n2:             .09067985502926865
    n4:             .04326599756204792
    n8:             .004847756818844198
    n16:            .0000699589252800668.

The areas are numerical diagnostics without directed integration
certification; the root counts and sign witnesses are exact. More negative
rings, higher mean and a nonzero tiny top Fock tail do not certify a useful
approximate stellar, GKP, cubic-phase or fault-tolerant resource. The
multi-copy Fock-capability benchmark itself is prior in
[Zapletal et al. (2020)](https://arxiv.org/html/2012.08544v1); its supplied
experimental input states are followed by a computational multi-copy
interference analysis. This does not qualify our physical factory.

The result retained from this direction is the fully costed model-side
waiting-loss acquisition. Historical priority, a better physical factory,
a robust quantum-computing resource and the original civilisation-changing
capability are UNKNOWN or NOT_ACHIEVED.

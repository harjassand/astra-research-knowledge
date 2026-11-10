# Endpoint-matched full-parameter construction: status and invariant reduction

9 November2026. Author construction, not an independent intermediate audit. No all-k positivity or global J_r theorem is claimed here.

## 1. Fixed path and preserved outcome

The translator is

    Lambda=2j_A+ell[ku_A-v_A+3(k+1)j_A/2]/(3k+1).

Its endpoint coefficient2 is supported by the complete determinant-null-face proof, and its k1 coefficient3 is the reviewed adapted-Hessian translator. The separate near-face absorption proof gives an existential small-positive-r interval for this path without depending on this full-parameter construction.

The single exact full-parameter child completed in3.565180082 seconds, rc0, external cap20seconds, no optimizer, field search or parameter sample. Source SHA2565f5ea6864add01cb168f6c1916c544c16cc2ba5bf65a77e237fb90c10f0dbe25. MATRIX.json contains the complete affine3x3 quadratic Q, cubic C and quartic E for8(k+1)(3k+1) times the support remainder. The full augmented determinant has ell^3 factor and90 binary coefficient forms in powers of ell and V^2.

The ell^0 forms are exactly the paid endpoint forms. Some higher individual ell coefficients are signed; that is not a negative matrix or field, and it prevents merely claiming coefficientwise positivity. All forms, including signed ones, remain in M4.json. No coefficient was changed within the run.

## 2. A useful exact all-k quadratic identity

The common selector gives the quadratic support metric

    Q_A(X)=(1/2)A:P(X)A
              +ell*j_X[ku_A-v_A-ell*j_A]/[2(3k+1)].

This follows from qS(A)/2-Lambda=ell(ku_A-v_A-ell j_A)/(2m). The second term is signed; no separate positive-metric claim follows from this identity alone.

## 3. The diagonal perturbation Schur in determinant/strain coordinates

For V=0 put X=diag(x,y), A=diag(alpha,delta),

    d=kx^2-y^2, j=xy, E2=d^2+4kj^2=(kx^2+y^2)^2,
    s=k alpha x-delta y, t=alpha y+delta x,
    ell=3k-1,n=k+1,m=3k+1,
    a=ell/(8n), b=ell/(2n), c=(3k^2+12k+1)/(4n),
    L=ell(d+3kj)/m.

The exact support remainder is Q(s,t)+C1*s+C2*t+f, with

    Qss=6a-L*j/E2,
    Qst=ell(7k+1)/(4nm)+L*d/(2E2),
    Qtt=(13k+1)/(4n)+L*k*j/E2,
    C1=4ad+2bj, C2=bd+2cj,
    f=a d^2+b dj+c j^2.

Here Q(s,t)=Qss*s^2+2Qst*s*t+Qtt*t^2. The only zero denominator is X=0, whose remainder is trivially zero.

The derivation uses the exact identities

    (k alpha^2-delta^2)j+(alpha delta)d=s*t,
    alpha delta=(-j s^2+d s t+kj t^2)/E2,
    8ak+2c-Lambda_j=3ell*k/m.

Thus this is a coupled invariant reduction of the complete fixed diagonal Schur, not an estimate by independent coefficient norms.

## 4. Exact scalar quartic target

Let Mdiag be the augmented matrix of Q,C/2,f in(s,t,1). Then

    E2 det(Mdiag)=ell^2 P(d,j)/(64n^2m^2),

    P=2m^2 d^4-2m(6k^2-7k-1)d^3j
        +ell(9k^3-23k^2-7k+1)d^2j^2
        +4kell(9k^2+4k-1)dj^3
        +4kn(33k^2-1)j^4.

The exact Q determinant is

    ell[3m^2 d^2-m(18k^2+7k+1)dj
             +k(54k^3+69k^2+16k+1)j^2]/(4E2 n m^2).

Its numerator quadratic has positive d^2 coefficient; its discriminant after removal of m^2 is

    -324k^4-576k^3-107k^2+2k+1<0, k>=1/3.

The inequality follows, for example, by expanding about k=1/3, whose constant is negative and all subsequent coefficients are negative. Hence detQ>0. A positive leading Q entry, and the quartic P payment, still have to be retained for a full diagonal support. The lead has taken a structural Gram construction for P; no result from that construction is silently presumed here.

The invariant extraction source f4ef9bdf852268a4b26ff3e0d53a4bf7530bfebf85bd0f009dce919d92be0e62 completed in0.293945074 seconds, rc0, external cap5seconds. It performs exact algebra only, with no candidate search. DIAGONAL_INVARIANTS.json contains the literal rational forms.

## 5. Remaining full target

Even a positive diagonal quartic would cover only V=0 in this current pointwise proof. All nonzero-V affine cross terms are retained in MATRIX.json and must be paid with the same resources. The all-r acoustic projection is independently available, but its full mixed cubic/quartic remainder is still unproved. Neither a signed parameter coefficient nor a successful restricted support is a genuine negative/positive full-gradient Jensen conclusion.

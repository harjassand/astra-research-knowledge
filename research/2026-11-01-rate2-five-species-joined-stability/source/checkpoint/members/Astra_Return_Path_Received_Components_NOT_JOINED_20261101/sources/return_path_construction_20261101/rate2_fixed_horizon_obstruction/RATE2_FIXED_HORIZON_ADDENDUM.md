# Rate-2 fixed-horizon obstruction: exact transfer, separate from stability

**New author addendum, pending independent review.** The original rate-1 source
SHA256 0f6a4405e9566b070100322606f004ea1f58dda08fd7ea46d03cec1da8d3e478
and its independent receipt SHA256
4321f9200831c54d5b33f5e430fad8ede9759b5d7392ccd18115fa46ef020590
are unchanged. That receipt was for the all-unit model. The present addendum
actually performs the finite-constant transfer to CD->AE coefficient two;
it does NOT transfer the product-Poisson stationary law or positive recurrence.

## Actual rate-2 model and dominant process

Take the port 0<->A and internal pairs 2A<->AC, 2A<->AD, 2A<->AE,
AE<->CD and CD<->AB, all coefficients one except CD->AE has coefficient two.
Start at x_N=(0,N,1,1,0). Call every A-dependent reaction except AB->CD bad.
The dominant chain keeps immigration, AB->CD, CD->AB and CD->AE. Coupling uses
the same actual channel clocks up to the first bad event.

The retained jumps preserve exactly

    A+C=A+D=1+I,
    B=N-I+A-E.

E is the monotone count of retained CD->AE jumps, now of intensity 2CD.
Stopping at immigration number m+1 therefore dominates this count by a Poisson
variable of mean `2T(1+m)^2`. No future-intensity conditioning is used.

For nonnegative integers m,ell, let K=3+2m+ell and N>2K. The dominant process
outside the two counter-tail events has A+C+D+E<K and B>N/2. The EXACT full
rate-2 generator and bad intensity are

    LA=1-A-3A(A-1)+A(C+D)+3CD-AB,
    q_bad=A+3A(A-1)+A(C+D+2E).

On the stated stopped region, these imply

    LA<=1+3K^2-(N/2-K)A,
    q_bad<=(1+5K)A.

Stop the actual process at the first bad event or first region exit. The actual
and dominant paths coincide before a bad event. Stopped Dynkin, A(0)=0 and
nonnegative terminal A give

    E integral_0^stop A(s)ds <=(1+3K^2)T/(N/2-K).

The compensator for the first bad mark then proves

    P_xN(any bad event by T)
      <=P(Pois(T)>m)+P(Pois(2T(1+m)^2)>ell)
          +(1+5K)(1+3K^2)T/(N/2-K).                    (1)

The counter exit is covered by the dominant tails; the last term pays all
remaining actual competing channels. Unit immigration bounds total count and
proves nonexplosion; ordinary localization validates all stopped expectations.
For fixed T, first choose m,ell, then N. Equation (1) yields

    P_xN(any A death by T) ->0.                           (2)

This does not assert convergence of unrestricted expected A-occupation.

## Count growth and the representation consequence

For every fixed T and r>1, write D_A for actual death count. Pathwise
`S(T)=N+2+I(T)-D_A(T)`. The difference between `E r^I(T)` and
`E r^[S(T)-(N+2)]` is at most

    (E r^(2I(T)))^(1/2) P(D_A(T)>0)^(1/2).

Thus (2), with no independence assumption, proves

    E_xN r^[S(T)-(N+2)] -> exp[T(r-1)].                  (3)

Suppose a finite nonnegative W, constants c,C,zeta>0 and finite K0 obeyed
`c r^S<=W<=C r^S` and `LW<=-zeta W+K0` on all states. Nonnegative localized
integrating-factor Dynkin and Fatou give
`E W(X(T))<=exp(-zeta T)W(x)+K0/zeta`. Divide by r^(N+2), use (3), then N->infinity:

    c exp[T(r-1)] <= C exp(-zeta T).

Choosing a sufficiently large fixed T contradicts this inequality. Therefore
**the actual rate-2 non-complex-balanced model also has no geometric Foster
function uniformly comparable to r^S.** This is solely a representation
obstruction. The rate-1 product-Poisson stability fact is not used and is not
asserted for the rate-2 chain. No recurrence, stationary tail, scaled-time
limit, N^(1/5) quantitative strengthening or absolute-occupation conclusion
is supplied by this addendum.

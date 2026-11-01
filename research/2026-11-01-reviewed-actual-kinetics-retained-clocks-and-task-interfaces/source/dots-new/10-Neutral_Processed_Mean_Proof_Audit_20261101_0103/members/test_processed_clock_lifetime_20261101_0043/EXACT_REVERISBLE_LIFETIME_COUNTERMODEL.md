# Fixed trial a,q do not bound actual lifetime: exact reversible chain

Status: exact construction, 2026-11-01 UTC; independent review pending.
This settles actual lifetime from a,q,rho alone. It does NOT settle a uniform
bound on the integrated trial correlation, nor a theorem that additionally
assumes a uniform inverse-form certificate for the whole-domain source 1_D.
No physical acquisition, feedback, or quantum claim is made.

## 1. Three actual live states and one cemetery

Fix delta>0 and rho>0. Let 0<r<1. The live-state reference measure is

    m(0)=1-r,  m(1)=r,  m(2)=rho.

The basin is A_set={0,1}, the slab S={2}, so M=1 and slab ratio rho is fixed.
Take h=(1,1,0), N=1, e=h. State 0 is killed at rate 1. State 1 is killed at
rate k=r/(delta+r). Its only live transition is to state 2 at rate
p=delta/(delta+r). State 2 jumps to state 1 at rate

    b=r delta/[rho(delta+r)].

There are no other live transitions. The shared edge conductance is

    c=m(1)p=m(2)b=r delta/(delta+r).

Thus the reference killed generator A on functions is

    A = [[1, 0, 0],
         [0, 1, -p],
         [0, -b, b]].

This is an actual finite nonexplosive positive killed Markov chain. It is
self-adjoint in L2(m) by the conductance identity. Its quadratic form is

    E(f,f)=(1-r)|f0|^2 + r k |f1|^2 + c |f1-f2|^2.

It is positive definite for every r>0. The killed transition operators are
positive and contractive in L2(m); one can obtain them by killing the
m-invariant conservative chain at rates 1,k,0. All domains are finite-
dimensional. There is no uniform lower spectral gap as r tends to zero.

## 2. Exactly fixed a=1 and q=1+delta

Since h=(1,1,0),

    a=E(h,h)=(1-r)+r k+c=1.

Solving A v=h gives v0=1 and v1=v2=1/k. Consequently

    q=<h,A^(-1)h>_m=(1-r)+r/k=1+delta.

These are identities, not limiting approximations. The Schur defect aq-1 is
exactly the arbitrarily small fixed delta. M=N=1 and rho are also exactly
fixed. The common measure's three atom weights vary with r, while its total
mass 1+rho is fixed. The reference matrix itself varies with r.

## 3. The actual mean diverges

Let t_i be expected killing time from state i. Solving A t=1_D gives

    t0=1,
    t2=t1+rho/c,
    t1=(1+rho/r)/k.

For the exact initial law m(.|A_set),

    E[tau]=(1-r)t0+r t1
          =1+delta+rho+delta rho/r -> infinity as r downarrow 0.

Every member has finite mean; the family has no finite upper bound determined
by a,q,rho. No processing is required: the zero processing term is neutral on
both sides and is admissible. If genuinely time-dependent nonzero processing
is desired, split state 2 into two states of mass rho/2 with identical
conductances c/2 to state 1, and add arbitrary predetermined locally bounded
symmetric exchange rates between those two slab states. This processing
preserves the same measure, annihilates h on both sides, is dissipative, is a
nonexplosive actual chain on every finite horizon, and leaves the displayed
three-state lumped law unchanged. It therefore gives exactly the same mean
counterexample under genuinely time-dependent neutral Markov processing.

## 4. Absolute CDF accuracy is even stronger than the port bound

The exact basin start is a mixture: weight 1-r in state 0, whose lifetime is
Exp(1), and weight r in state 1. Writing S_1(t) for survival from state 1,

    S(t)=(1-r) exp(-t)+r S_1(t),
    sup_t |S(t)-exp(-t)| <= r.

Hence the survival error tends to zero while the actual mean diverges. This
is not an arbitrary spectral-mixture example: all conductances, killing
rates, invariant reference measure, common form, trial neutrality and actual
positive propagation have been explicitly realized.

## 5. Precisely what this does and does not refute

The integrated trial correlation remains exactly

    int_0^infinity <h,exp(-tA)h>_m dt =q=1+delta.

Its smallness does not control long occupation of the slab, where h=0. The
whole-domain source inverse form is NOT uniformly bounded. In fact

    B_A=<1_A,A^(-1)1_A>=1+delta,
    <1_A,A^(-1)1_S>=rho/k=rho+delta rho/r,
    B_S=<1_S,A^(-1)1_S>
       =rho^2/(r k)+rho^2/c
       =rho^2(delta+r)^2/(delta r^2).

Thus a separately uniform B_S or B_total derived from both source currents
would exclude this family. In particular the existing stronger reversible
MFPT theorem is not contradicted. The counterexample only rejects a uniform
actual mean conclusion from the root's trial data a,q and slab ratio rho.

The harder open question remains: when the output is the trial itself
(e.g. h=1_D), or when a genuinely uniform whole-domain source certificate is
added, can arbitrary predetermined common-measure neutral processing make
integrated survival unbounded? A generic passive L2-gain argument or this
slab-occupation construction does not decide that stronger question.

## 6. Costs and provenance

All calculations above are exact finite-dimensional linear algebra. The
reference sources read were PASSIVE_PORT_CLOCK_ROOT.md and
PASSIVE_PORT_CLOCK_ROOT_V2.md in neutral_processing_clock_pending_20261101,
and audit_neutral_processing_process_20261101_0034/CONCRETE_PROCESS_RECEIPT.md
and AUDIT.md. Source originals were not edited.

The time-dependent add-on has finitely many states and locally bounded rates,
so no finite-time explosion/Zeno issue arises. Its strength can be any
predetermined locally bounded function. Neutrality is mathematical only; it
assigns no free control, acquisition, or thermodynamic operation.

No external retrieval or external state change was needed. No blocker or
authorization denial occurred in this construction.

# Energy drift alone does not give Poisson-small repeated-jump faults

Status: root construction, independent review pending. Ordinary quantum-jump
calculus; no novelty claim. This concerns actual counted jumps, not automatically
logical faults. It explains a remaining gap in interpreting energy/count bounds.

Use a three-level source |0>,|1>,|2>, lambda=1, and

  H=diag(0,1,2), L1=sqrt(2)|0><1|, L2=2|1><2|,
  G=D[L1]+D[L2], V=g(|2><0|+|0><2|), 0<g<=1.

Then sum L_j*L_j=2H, G*H=-2H, h=kappa=2, C=||sqrt(H)V||=sqrt(2)g.
Initialize in |0>. All premises of the source-energy estimate and finite-ceiling
MGF hold. A rare excitation can nevertheless produce TWO successive emitted
jumps; it need not pay two independent coherent excitations.

Before the first count, the unnormalized no-jump state is a(t)|0>-i x(t)|2>,
with real amplitudes satisfying

  a'=-g x, x'=g a-2x, a(0)=1, x(0)=0.

For 0<=t<=1, positivity until a could first reach1/2 gives x(t)<=g t and
a(t)>=1-g^2 t^2/2>=1/2. A first-crossing argument therefore gives these bounds
through the whole interval (the endpoint equality causes no issue). Consequently

  x(t)>=g(1-exp(-2t))/4.

The first jump density is4 x(t)^2. On t in[1/2,1] it is at least
g^2(1-exp(-1))^2/4. At this jump the state becomes exactly |1>; the Hamiltonian
does not act there, and the next jump waiting time is Exp(2). Thus

  P(N_2>=2) >= g^2(1-exp(-1))^2(1-exp(-2))/8.        (B)

In particular this is a fixed positive constant times C^2, not O(C^4).
No uniform Poisson domination with mean K C^2 T, for any fixed K independent
of g, can follow from these energy premises: at T=2 its two-count probability
would be O(g^4), contradicting (B) for sufficiently small g.

The example has a finite-dimensional source with the standard formal monitored
Markov dilation and an initialized dark source. This is not a finite-bath or
acquired physical detector construction. It does not exploit warm initial energy
or unbounded H. Additional
assumptions such as complete reset after EACH count would change the example.
Independent detection thinning would charge eta^2 for missing BOTH emissions,
but it would not turn their underlying source-generation probability into g^4.

The finite-tilt MGF is consistent with this burst. It is not a claim that the
number of emitted photons obeys an independent low-rate Poisson model. Nor is
this a lower bound on any logical error: the receiver may observe/correct the
burst, parity may cancel it, or both emissions may lie in one correction window.
Such actual consumer structure is exactly what must be constructed before a
source-count certificate becomes an all-selected fault service.

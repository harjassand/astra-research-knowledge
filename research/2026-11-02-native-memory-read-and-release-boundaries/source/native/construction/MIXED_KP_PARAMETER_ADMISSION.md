# Fixed-parameter room for doubled-charge mixed KP

Supporting calculation for the scalar auditor; not a replacement for their final inequalities.

The mixed-source representation allows arbitrarily small fixed q as microscopic epsilon_d tends to zero, at any fixed admissible native r=t/Delta and beta. The exponential factor exp(2 beta t b_c) is severe but volume independent.

For strict doubled-charge rod KP choose charges of the form

 a_rod(l)=a0+b l, a0=128 Dbar r², b=64 Dbar t²/Delta,

and strengthen native constraints so that exp(2a0)<=2 and d2=Delta-2t-2b>=Delta/2; for example 2r+128Dbar r²<=1/2 suffices for the latter. Choose beta large enough that wraps remain strictly within the endpoint budget even after exp(2a_wrap). The same path-integral calculation as the audited rod theorem then has substantial fractional slack relative to these enlarged charges. These are stronger conditions than the old rod theorem; do not claim the entire old parameter region without recalculation.

For compound source with m distinct labels take a_source=A m. Its interaction with ordinary rods is bounded by a constant times

 b_c m * beta * t²/Delta

plus the full-time wrapping contribution. Choose A finite and at least several times that coefficient. The positive fixed a0 pays source activity seen by short rods: every full-time source meeting a fixed rod is anchored near its clock, irrespective of the rod's duration. Bounded-degree source-animal counting gives an upper bound C sum_(m>=1) m [C_V q exp(2A)]^m. This can be made <=delta a0 for any fixed delta>0 by taking fixed epsilon_d sufficiently small. A source of m labels sees at most C m times this anchored sum, similarly <=delta A m.

Hence there is no parameter-scale obstruction to simultaneous

 integral (mu_rod+nu_source)|f(x,y)| exp[2a(y)] <= theta a(x), theta<1,

and a source-only marked bound proportional to epsilon_d a(x), provided the refined rod-only inequalities and the scalar auditor's source-anchor bookkeeping are enforced. All choices occur once, independent of n and bath volume. No spectral resolution or interaction penalty grows with system size.

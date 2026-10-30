# Autonomous preset-bank transfer: a simpler comparator to request semantics
30 October 2026. Root new whole-composition candidate, unreviewed. This is on-chip transfer/storage into a predetermined bank, not LOCC, requested on-demand handoff, or universal computation.

## 1. The actual changed task
An unknown state is supplied ALREADY ENCODED on Q at startup, with ready native memory apparatus and every routing clock initialized to0. This small but real clean routing initialization is required: bare encoded Q with arbitrary unknown routing labels is not canonical encoded Q under G. B is an arbitrary logical-independent spare, possibly correlated with the retained bath. The task is to put the state in physical bank B after a finite startup interval and keep it recoverable there. Transfer may begin immediately. There is no promise of remaining in Q until a later request.

This change matters: a hardwired B attractor has no finite unprotected target bit to forget. It directly avoids the allowed local replacement counterexample in REQUEST_DRIVEN_SUBSYSTEM_ROUTER_AND_MODE_OBSTRUCTION.md. It does not solve that counterexample under its original strict request semantics.

## 2. Exact physical hardware and canonical frame
Use the three-state (0,e,1) router in producer-workspace/REQUEST_DRIVEN_SUBSYSTEM_ROUTER_AND_MODE_OBSTRUCTION.md, but REMOVE the request register and its projector. The Hamiltonian drive is permanently enabled:

 H_i=Omega SWAP(Q_i,B_i) tensor (|e><0|+|0><e|),
 J_i=sqrt(kappa) I_QB tensor |1><e|.

Define onsite G_i=I_QB tensor P0 + SWAP(Q_i,B_i) tensor (Pe+P1). G=product G_i. The actual native memory generator is G (L_memory on Q tensor id_B,clock) G^dagger, with its full actual controls, losses and reset monitors. Paired cells are fixed-dimensional sites. All original hub-resource couplings remain two-site; the routing Hamiltonian/reset are onsite. This pays genuine quantum access to both banks at every column. It is not remote teleportation.

Optional vacant-bank resets are separately phase-resolved actual jumps

 K_(c,b)=sqrt(mu) G_i[I_Q tensor |0><b|_B tensor Pc]G_i^dagger.

In the fixed G frame all router, terminal and vacant-bank channels act as identity on canonical Q. Native correction acts only on canonical Q and its existing apparatus. Thus the SAME native memory theorem applies under the same bounded-body incident joint-cb noise contract, with constants adjusted for the larger onsite dimension. Conjugation is onsite and does not grow physical noise support. Logical-independent auxiliary dynamics may be retained as bath. No retuning based on a record occurs.

## 3. Explicit routing density under continuous correlated noise
Let B_i^r=P0+Pe (counting e as unfinished is conservative). On this two-dimensional subspace define

 R_i=[[2/kappa+(kappa+2mu)/(4Omega^2), -i/(2Omega)],
      [i/(2Omega),                         2/kappa]],

and R_i=0 on state1. The actual complete clock generator including phase-resolved spare-reset dephasing satisfies L_i^*R_i=-B_i^r. Let Rmax and Rmin be its positive extremal eigenvalues, A_i=R_i/Rmax, a=Rmin/Rmax, r=1/Rmax. Then a B_i^r<=A_i<=B_i^r, [A_i,B_i^r]=0, and L_i^*A_i=-r B_i^r<=-r A_i.

For fixed u>0 put V=product_i(I+u A_i), M_r=sum_i B_i^r, ell=log(1+u a). All factors are disjoint and commute. V is written in the fixed G frame; the actual physical witness is G V G^dagger, which need not be clock-only. M_r and its cutoffs commute G and are the same physical and canonical projectors. Native memory annihilates V in the G frame. Directly,

 L_nom^* V <= -r V sum_i [u A_i/(I+u A_i)]
             <= -k V log V,  k=r/(1+u),

using z/(1+z)>=log(1+z)/(1+u) on 0<=z<=u. This is exact, not a Taylor/service approximation.

The existing finite-system-leg relative-norm estimate gives E_t^*V<=C_u eta N V for admitted bounded-body joint noise (including moving distant partners and arbitrary retained bath). Constants depend on the finite grouped dimension and u, not N or bath dimension. For x=Tr V rho,

 log x(t)<=e^(-kt) log x(0)+(C_u eta N/k)(1-e^(-kt)).

Initially x(0)<=(1+u)^N, hence

 Pr{M_r>=b_r N}<=exp{N[-ell b_r+e^(-kt)log(1+u)+C_u eta/k]}.

Choose t_star so e^(-k t_star)log(1+u)<=ell b_r/4 and eta so C_u eta/k<=ell b_r/4. For EVERY fixed t>=t_star the routing density tail is <=exp(-ell b_r N/2). t_star is a fixed physical duration independent of block size at fixed code allowance; it can be large and is not a measured engineering estimate. All clocks are noisy throughout. A local replacement of DONE by0 now has an actual enabled repair path.

This is a time-uniform family of pointwise bounds, not an event that no bad density ever occurs, not an anytime selected-output result, and not a global DONE detector.

## 4. Composition with the actual memory and bare-bank output
Import the exact unified idempotent native memory and strong-BUSY contracts, not the nonidempotent AB rollback memory. Receiving sources:

 producer-workspace/Q_AND_RECEIVER_GLOBAL_MEMORY_CONTRACT.md;
 producer-workspace/GLOBAL_EXPONENTIAL_COMPILER.md;
 producer-workspace/DIRECT_SINGLETON_DERIVATION_V1.md.

Their reviewed scope supplies: a positive canonical-killed comparison preserving the unknown logical module with error epsilon_C(t)=poly(N)(1+t) exp(-cN); and a pointwise exponentially small physical strong-BUSY density after selecting the small first LOAD amplitude/noise budget. G commutes all BUSY predicates, because it changes only paired DATA and routing clocks, not native workspace/tags. Routing projectors commute the physical native forest, since the latter is G F_Q G^dagger and G is diagonal in routing labels.

Transfer the actual physical BUSY and routing tail masses to the positive canonical comparison by trace-norm closeness; then apply their commuting physical cutoffs to that comparison. Gentle compression gives error at most epsilon_C+2 sqrt(epsilon_BUSY+epsilon_route+epsilon_C), up to a harmless trace-deficit term. No product of memory and routing witnesses or drift restriction is inferred. No tail is conditioned on an adaptively selected time.

In every kept coefficient, relative to full SWAP of all Q/B columns, G differs only on at most b_r N columns. A native forest with at most b_b N BUSY owners touches at most s b_b N columns for a fixed footprint constant s. The admitted canonical memory error has radius at most r0 N. Expanding arbitrary operators on the union into physical Pauli legs gives a common B-code correctable span once

 r0 + 2 s b_b + 2 b_r < r_decode

in the source's sum-of-two-CSS-sector radius convention, with any fixed native grouping factors included in s. The factor2 converts one physical DATA support into at most two sector weights. All arbitrary spare/old-Q/bath coefficients are retained and independent of the unknown logical input. A single SAME ordinary B zero-code decoder corrects this entire linear span, not a decoder chosen after seeing a routing pattern. No routing clock measurement or frame inversion is part of that decoder.

Therefore the candidate conclusion is an exponentially accurate fixed-time logical B-output benchmark after t_star, for horizons where the inherited poly(N)(1+t) exp(-cN) error is small. Q need not be initialized again or retired; correction continues across both banks through the covariant hardware. B is not a separately autonomous standalone receiver disconnected from Q: the paired correction apparatus remains available.

## 5. Costs, limitations and strongest alternative
Paid resources: already-encoded Q; admitted ready native startup; fixed paired multi-level sites; permanent quantum SWAP access across each pair; full conjugated memory controls; continuous resets/entropy export; specified small joint noise; ideal final ordinary DATA decoder as a benchmark. No elementary-qubit compilation, physical final decoder, raw input encoder, practical threshold, latency advantage, or low power is proved.

This is a stronger simple comparator for PRESET transfer than the raw-Bell/LOCC endpoint: no raw Bell resource, waveform shutoff or target latch is needed, at the price of direct quantum couplers and continued paired apparatus. It does not replace that endpoint under its LOCC resource contract. Likewise a conventional fault-tolerant SWAP followed by ordinary QEC is a strong comparator; no practical advantage over it is claimed.

Established primary context (checked 30 October): Verstraete, Wolf and Cirac, arXiv:0803.1447, already formulate time-independent local dissipative universal computation; Kastoryano, Wolf and Eisert, arXiv:1205.0985, construct dissipative timing/trigger gadgets. Their existence prevents claiming that an autonomous clock or dissipation-driven transfer is itself a new principle. The intended increment here is the explicit continuous-noise/native-memory/fixed-bank interface, pending whole review. Historical novelty of that combination is unverified.

The real hard remaining problem is logically correct causal commands and gates under noisy distributed control. This comparator narrows that problem; it does not bypass it by calling preset routing universal computation.

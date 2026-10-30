# Full-state absorbing receiver rail and its noisy completion moment

30 October 2026. V2 construction. Preserves the table and freshness limits of ABSORBING_RECEIVER_RAIL.md. This variant removes V1's stationary garbage sectors by actual two-site Hamiltonians. No encoded composition or late-arrival theorem is asserted.

## 1. Replace the actual Hamiltonian, retain the onsite jump

Use exactly the full 18-state table V in V1. In canonical gauge let

    u_v=s, u_0=f0, u_1=f1,
    h = Omega sum_(a=v,0,1) (|e_a><u_a|+|u_a><e_a|),
    j = sqrt(kappa) sum_(a=v,0,1) |d_a><e_a|.

The actual H is V(I_L tensor h)V*, a two-site A/B operator. In addition to V1's source-transfer terms it contains, for b=0,1, the coherent couplings

    |v,v> <-> |0,e0>,      |v,x> <-> |0,e1>,
    |0,x> <-> |1,e0>,      |1,x> <-> |1,e1>,

each with coefficient Omega. These are explicit nonlocal A/B Hamiltonian terms of the allowed two-site kind, not fictitious classical transitions. The actual receiver-onsite jump remains

    J = sqrt(kappa) I_A tensor (|d0><e0|+|d1><e1|).

Thus V*HV=I_L tensor h and V*JV=I_L tensor j exactly on every physical state. The gauge dynamics is the direct sum of three identical source/intermediate/done chains. There is no dark garbage subspace outside the physical B-done sector.

The source loading sector s evolves exactly as in V1. The two extra couplings do not act on that nominal trajectory. They repair the completion geometry of dirty gauge states; they do NOT make an arbitrary initial receiver encode A's unknown input.

## 2. One full-state Gramian

Let B_act=I_g-sum_a |d_a><d_a|. Put the V1 positive 2x2 Gramian R on each ordered pair (u_a,e_a), and zero on done gauges, obtaining R_all. Set

    A=R_all/||R||,  a0=lambda_min(R)/||R||,  r=1/||R||.

Then

    a0 B_act <= A <= B_act,
    L_gauge* A = -r B_act <= -r A.

This is a full-Hilbert operator inequality. Consequently the nominal probability of receiver-not-done at t is at most a0^(-1) exp(-rt) for every joint initial state, including an arbitrary logical/gauge/reference/bath correlation. 'Receiver done' identifies an output LOCATION, not the provenance/correctness of the logical value stored there.

For k independent nominal pairs, conjugated canonical memory acts on logical DATA/controllers and as identity on their gauge factors. It commutes every A_i and does not change this drift. Any arbitrary bath-only evolution likewise annihilates the tests.

## 3. Continuous local-noise hierarchy

Assume the complete joint physical generator is CPTP, and its perturbation is decomposed into Hermiticity-preserving identity-annihilating local terms N_Z, with joint cb norms, at most q rail gauges touched per term, and summed per-gauge incident norm at most eta. The bath may be common and retained. These are the same kinds of full-joint hypotheses used in the earlier reviewed program-clock lemma; no reduced Markov clock law is presumed.

For M_S=product_(i in S) A_i, a term with K=S intersect Z satisfies

    N_Z* M_S <= ||N_Z*||cb M_(S minus K)

when K is nonempty, and vanishes when K is empty. Untouched positive factors commute and can be pulled out; the touched product has norm at most one. Therefore the positive moment hierarchy is dominated by p(t)^|S|, where

    p'=-r p+eta p^(1-q),        p(0)=1,
    p(t)^q=e^(-qr t)+(eta/r)(1-e^(-qr t)),

for eta<r. The induction uses |K|<=q and p<=1. It applies to arbitrary initial joint states. Since product B_act,i <= a0^(-|S|) M_S,

    Pr[all receivers in S not done at t] <= (p(t)/a0)^|S|.

Choose a desired small inclusion strength, then a fixed finite startup dwell and sufficiently small eta. The late-time bound is uniform; it has no exp(eta t) degradation. The new gauge rates, local dimension, grouping and q/eta constants must be used. This is an elementary application of the established clock-moment method to the new physical full-state table, not a new general noise theorem.

If a memory killed-basin projection is canonically independent of these rail gauges, it commutes the tests. The usual complete-loss conditional-positivity argument retains the same inequality for the subnormalized killed state. This condition must be checked for the actual composed memory; a bare appeal to a memory theorem is insufficient.

## 4. Preserved exact firewall and remaining costs

Every new H term and J still annihilates P_D=I_A tensor P_(B,done). Source-only operators preserve this subspace and act only on its A gauge. Hence V1's exact post-done source firewall is unchanged. Source-only noise of arbitrarily large strength can be harmless AFTER a perfectly done output, but the hierarchy above only covers source terms while bounded by its stated incident norm. Arbitrary strong source processing during incomplete/noise-reopened transfer needs a separate defect-supported argument or rate bound; do not infer it here.

The moment establishes output-location concentration under noise. Original unknown-state protection still needs the canonical code/memory theorem, valid initialization A-encoded/B-vacant, full endpoint correctable span, and paid extraction/controller resources. Dormant false-done poisoning remains exactly as in V1. All-state completion is not all-state correct input acquisition.

## 5. Exact unloaded-bank failure, even without noise

V2 deliberately completes from every gauge state. In particular the physically unloaded state |v_A,v_B> is canonical |0,f0>. Its nominal f0->e_0->d_0 chain ends at |0_A,d0_B>. Thus an empty source/receiver pair becomes an occupied done receiver WITHOUT any incoming unknown qubit and WITHOUT noise. If a genuine source qubit arrives later, the exact done firewall blocks its transfer. This is a direct deterministic consequence of the all-state completion design, not merely a small perturbation issue.

V1 does leave the empty pair stationary. But during a dormant interval T, the admissible receiver-local poison jump sqrt(epsilon)|d0><v| produces false done with probability 1-exp(-epsilon T), after which V1 also refuses arrival. The jump's generator has cb norm at most 2 epsilon, so arbitrarily weak allowed continuous local noise still ruins an unprotected one-use terminal rail over sufficiently long dormant time. This is only the specified finite rail/control architecture; protected redundant arrival/history records are not excluded.

The choice is therefore explicit: V2 supplies a full-state completion/repair witness after a qualified loaded-source start, while V1 avoids spontaneous unloaded completion. Neither substitutes for a fresh late-arrival interface.

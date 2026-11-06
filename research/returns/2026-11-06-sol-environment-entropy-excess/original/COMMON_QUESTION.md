# Common full question: computability of ordinary quantum communication capacity

For every valid finite-dimensional memoryless quantum channel N:A->B given by an explicit finite rational-complex Choi matrix J_N, determine whether there exists a total algorithm T which returns a rational q satisfying

    |q-Q(N)|<=1/4 bit,
    Q(N)=sup_{n>=1} (1/n) max_rho I_c(rho,N^{tensor n}),
    I_c(rho,N)=S(N(rho))-S(N^c(rho)).

Dimensions vary over finite inputs and are part of the description. The Choi convention is normalized: J_N>=0, Tr_B J_N=I_A/d_A. Inputs are promised valid. Entropies are in bits. All encoders and decoders allowed by the ordinary unassisted coding theorem are allowed. No shared entanglement, free identity wire, symmetric helper, backward communication or postselection is added to that capacity definition.

Resolve the whole question: construct a terminating evaluator with its mathematical error guarantee, or prove that no such total evaluator exists. There is no running-time promise. Include the actual acquisition, dimension, precision, channel-description and execution costs required by your claim. A fixed1/4 evaluator yields arbitrary precision by finite tensor amplification Q(N^{tensor k})=kQ(N); efficient evaluation is a separate stronger claim. A proof of finite-block nonadditivity, QMA hardness, positive-versus-zero behavior with an uncomputably small gap, an assisted-resource result, or a failed proposed evaluator does not settle this question.

The consequence sought is a complete computational boundary for the operational rate of arbitrary finite quantum communication, rather than another restricted channel formula. No numerical impact grade, practical quantum device or historical-priority claim is a supplied premise.

## Exact sources and factual boundaries

- Bhattacharyya--Mehta--Zhao, arXiv:2601.22471v3, https://arxiv.org/html/2601.22471v3 : their ordinary-capacity promise Q>=3/4 versus Q<=1/4 is QMA-hard for succinct channel circuits, including degradable constructions. Their undecidability result concerns a restricted maximally-entangled-assisted one-shot zero-error classical resource. Neither proves the ordinary total evaluator impossible. Read governing original passages if using its construction.
- Cubitt et al., Unbounded number of channel uses may be required to detect quantum capacity, Nature Communications6,6739(2015), https://doi.org/10.1038/ncomms7739 : arbitrary fixed detection blocks are insufficient. Do not replace this by noncomputability or a noncomputable convergence modulus without proof.
- Accepted Astra N675 supplies complete-order/reference-dimension and source-defined entropy-defect undecidability at its actual generic variable-dimensional rational POVM scope. The standing human acceptance supersedes historical unreviewed labels; do not re-audit it. Original: REPO/updates/DG/package/channel_order_undecidability/channel_order_undecidability.pdf ; searchable derived extraction: REPO/updates/DG/package/channel_order_undecidability/EXTRACTED_TEXT.txt . Current acceptance is recorded in REPO/knowledge/current/packets/N675.json under current_acceptance. Read the governing quantified statement before using it.
- Existing Astra N1677 and its stronger ordinary-resource successor N1680 retain the distinction between assisted and ordinary rates. Complete available scientific originals are REPO/research/2026-11-03-p1-symmetric-assistance-return/source/p1/COMPLETE_VISIBLE_RESPONSE.txt and REPO/research/2026-11-03-p1-ordinary-capacity-resource-interface/source/p1/COMPLETE_VISIBLE_RESPONSE.txt . They include constructed interfaces and scoped failures. The ordinary evaluator remains unresolved. Their offered PDF/ZIP packages are unavailable under existing transfer holds: do not retry, recover by an alternative route, or assume missing code/proofs were acquired.

REPO=/Users/harjas/Documents/ChatGPT/coordination/work/astra-capital-successor-20261030/repo . Its generated retrieval currently reports stale input membership. Read the existing exact originals in place; do not rebuild or edit the integration checkout. Search/fetch, where otherwise available, remains a source menu rather than a theorem. Existing public primary sources remain available. These are useful prior facts, not a prescribed method or decomposition.

Direct Zenodo discovery by the lead found Stefano Pirandola's record22922992(v2), https://zenodo.org/records/22922992 , concerning explicit amplitude-damping formulas in the degradable regime. Its record was readable, while the original PDF timed out and its newer-record route was unavailable. Metadata is not imported as a theorem. That discovery helps distinguish a restricted evaluated formula from the present unrestricted question; no bypass of that source failure is authorised.

## Scientific and resource contract

Invent your own full construction and representation. A solution need not pass through any Astra predecessor. Do not deliberately access other pilot constructors' or the lead's developing outputs before your initial full attempt is completed. Public retrieval/Personal Context can create incidental exposure; this is not a blind trial. Preserve material incidental exposure honestly.

Use only existing permitted source access and bounded local mathematics. No packages, services, API billing, installations, hardware, outreach, access/transfer bypass, shared integration/predecessor writes, goals, automations or onward spawning. Your role directory is the only write destination. This is one human-authorised bounded pilot, with at most two research turns per whole constructor and an account-wide coarse usage guard managed by the lead. An operational resource stop does not resolve the scientific question.

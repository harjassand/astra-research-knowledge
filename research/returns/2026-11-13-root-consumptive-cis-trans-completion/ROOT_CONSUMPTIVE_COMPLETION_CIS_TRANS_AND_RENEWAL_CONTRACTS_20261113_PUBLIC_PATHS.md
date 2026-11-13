ROOT SCIENCE CONTRACT: CONSUMPTIVE COMPLETION KEYS, CIS/TRANS DELIVERY AND RENEWAL
13 November 2026 Brisbane. This note contains independently derived introduced models and exact source-exposure limits. It supplies neither qualified chemistry nor a working manufacturing system.

1. Physical operation and useful partial construction

A proposed abiotic oligomer factory can attach an instruction-activating key to the protecting group of a reagent packet. Successful covalent extension retains that group on the growing product; unsuccessful packets can, in principle, be physically cleared before instruction activation. A retained key can then enable cleavage of a clip blocking the next selection. Recoverable noncoupling can leave the original reactive terminus available for another attempt.

This organisation makes product retention relevant to progression. It does not by itself authenticate the intended bond or make instruction delivery local. Wrong strong covalent products can retain the same key. Residual unsuccessful packets can make the same enzyme substrate. A used key that survives cleavage may activate several neighbouring clips. A future blocker duplex can itself be an unintended substrate. Product-to-key connectivity, reagent removal, cleavage topology, cis delivery and useful end-group regeneration therefore remain separate physical operations.

One alternative is a continuation key that is itself consumed during its first instruction transition. Cutting both the instruction clip and the activating strand could change a reusable catalytic signal into a one-use event. This is a hypothesis about an actual covalent and geometrical organisation. The key fragments must really lose function, avoid reassembly or cooperative rescue, and leave the chemical chain and subsequent instruction accessible. A claim of one-use delivery is not supplied by calling a strand a key, by observing one fluorescent event, or by the existence of a double-strand-cutting enzyme. A key can still make its first cut on the wrong neighbour.

2. Actual independent primary and maker exposures

NEB BbvCI product main:
https://www.neb.com/en/products/r0601-bbvci
The first current ROOT open succeeded. Actual main lines 0-112 and the remaining returned main were read. The maker describes a restriction enzyme with two-strand cutting coordinates, a 37 C assay and an activity unit based on digestion of a particular DNA substrate over one hour. Heat inactivation is unavailable; the maker identifies cleanup alternatives and possible star activity under some conditions. These are manufacturer assay and handling claims, not kinetics on a branched, product-bound instruction clip, compatibility with oligomer chemistry, or autonomous reset. The displayed pack prices do not determine enzyme consumption per extension. No linked protocol, lot certificate, image, cleanup product or cited original was followed.

NEB Nicking Endonucleases main:
https://www.neb.com/en/products/restriction-endonucleases/hf-nicking-master-mix-time-saver-other/nicking-endonucleases
The first current ROOT open succeeded; actual main lines 0-36 and returned table description were read. The maker distinguishes ordinary two-strand cleavage from engineered one-strand nicking and identifies Nb.BbvCI and Nt.BbvCI as variants with one working catalytic site. This supports the physical distinction between destroying a duplex and nicking one partner, not the proposed single-use molecular gate. References, products, amplification applications and protocols were not followed. No sequence, cloning, genetic engineering or biological production construction is supplied here.

Liu--Liu--Deng, ATP-fueled autonomous pathway-selective signal transduction on DNA-nanostructure tracks, 2026, DOI 10.1038/s41467-026-76957-8:
https://www.nature.com/articles/s41467-026-76957-8
Before first navigation ROOT completed local identity/alias/hold checks. The first tool-rendered main through line 150 was actually read. It was marked as a rewritten summary and redirected to an error=cookies_not_supported query URL; this is its artifact scope, not independently checked publisher bytes. The exposed construction couples covalent DNA ligation to hairpin opening and uses nicking/refolding for dissipation and reset. It distinguishes geometrical propagation on a track from free-hairpin fragmentation. Reported multi-station propagation and finite fuel-restart demonstrations do not establish intended abiotic product-bond authentication, heterogeneous monomer synthesis, long-life renewal or manufacturing advantage. The FIRST governing followup at line 151 returned 500/nonretryable identity-provider redirect. The SAME identity, including PMC13590496, is now HELD against retry, challenge, alternate provider/version/author/title/PDF/SI/data/export recovery. Later main, Methods, input clearance and supplementary mechanisms were not read or imported. Search-rendered later text is not governing evidence. This is distinct from already-held Bath--Turberfield 2026 and Meng 2016; neither held identity was recovered.

He--Wang et al., Enhanced screening via a pure DNA-encoded peptide library enabled by an Fmoc modification, 2026, DOI 10.1073/pnas.2524999123:
https://pmc.ncbi.nlm.nih.gov/articles/PMC12933050/
The FIRST current ROOT open exposed browser-check/reCAPTCHA only. SAME identity HELD against challenge/reload/redirect/PNAS/author/repository/provider/version/title/PDF/SI/export recovery. No governing modification, capture, sequence, yield or preparation passage was read. Producer-reported capture exposure remains producer exposure, not a ROOT read. The present abiotic-control model imports no biological assay or application.

All earlier known and unknown source/access/transfer holds remain. Failed access is an observation limit, not scientific negative evidence. These distinct maker and primary exposures do not recover any held paper.

3. Independent coupled key calculation

Artifact:
ROOT_CONSUMPTIVE_COMPLETION_KEY_AND_TRANS_ACTIVATION_SCREEN_20261113.py
with its same-stem JSON in this directory. ROOT authored and executed this standard-library calculation. It does not execute or recover producer code or linked artifacts.

Every numerical rate, concentration, geometry, stock loss and molecular-weight approximation below is INTRODUCED. None is fitted to NEB, the track paper, a chemical experiment or a force law.

States per initially correct product are U (not yet progressed), C (correctly progressed, used key still locally sequestered), F (used key accessible), T (quenched used key), X (premature trap loss). Rates:
U -> C at k_cis;
U -> X at alpha*c;
C -> F at b;
F -> T at c.
An accessible used key remains catalytic at effective rate mu. In the declared well-mixed macroscopic model, bad-site hazard is [g/(1-g)]*mu*F(t), where g is the initially correct fraction. Thus
q_bad = 1-exp(-[g/(1-g)]*mu*integral(F(t),0,W)).
This is not a general physical lower bound: spatial restriction, enzyme geometry or other reaction organisations can change the model.

The script integrates the finite-state linear system by uniformization, in subintervals with q*dt <= 10, including an augmented occupation reward. It checks probability mass and the independent exact intended-progression formula:
P_cis = k_cis/(k_cis+alpha*c) *
        [1-exp(-(k_cis+alpha*c)*W)].
The zero-release limit gives zero transfer. Tiny numerical mass drift is normalized at each analytically unit-mass step. An initial conservation check exposed about 2.1e-12 accumulated floating-point drift at the largest quench case; the normalization corrected that numerical issue. It was not chemistry or a failed physical design.

At k_cis=.1/s, b=.01/s, mu=1/s, W=60 s and g=.1:
- no quench: intended progression .997521, bad-site progression .704649;
- c=1/s with perfect prior protection: .997521 and .0418071;
- c=100/s with perfect prior protection: .997521 and .000433710;
- c=100/s with alpha=1e-6: .996540 and .000433350;
- c=100/s with alpha=1e-4: .907854 and .000400307;
- c=1000/s with alpha=1e-4: .499997 and .0000234607.
The small bad-site number in the last case comes with loss of about half of the intended transitions. Fast indiscriminate quenching is not a free selective operation. Conversely, b=1e-6/s with no quench gives .997521 intended and .000144404 bad progression in this introduced finite window; an actually sufficiently stable sequestered key could avoid the problem without destruction. Neither selective quench nor long-lived sequestration is qualified here.

4. Single-use alternative and its remaining geometry

Under the additional unconstructed assumption that the activating key is permanently destroyed by its FIRST cut, only two first-event hazards are considered: k_cis and total k_trans. The exact first-hit probabilities are k_i/(k_cis+k_trans) * [1-exp(-(k_cis+k_trans)*W)]. A key cannot then catalyse many later transitions in THIS model. At most [g/(1-g)]*P_trans of initially bad sites can be advanced by those keys, before separate false-substrate, wrong-bond and fragment-reassembly paths. This count bound does not assume a unique target. The script also reports a distinct random-target mean-field occupancy.

For an introduced uniformly sampled sphere, one tethered molecule has effective molarity
1/[N_A*(4*pi*r^3/3)*1000],
with r in metres and the volume in litres. At r=10,20,30 nm this is .396425,.0495531,.0146824 mM. These are geometrical averages, not actual intramolecular rate constants or accessible conformations.

If a 1 micromolar competitor has an equal association rate constant, k_cis=.1/s and W=60 s, the conditional one-use model gives:
- 10 nm: intended .995048, wrong first hit .00251006, bad-site count bound .000278895;
- 20 nm: intended .978066, wrong first hit .0197378, bound .00219308;
- 30 nm: intended .934692, wrong first hit .0636608, bound .00707342.
A long tether that reaches an entire register can therefore lose the local delivery advantage in this declared geometry. More elaborate organisation, different rate constants or paid physical isolation can change the result. A fixed short tether plus motion, a transferred program, a steric guard or a consumptive clip are candidate operations, not provided parts. Short reach must remain compatible with actual growth, docking, washing and product release.

Destructive delivery removes repeated transfer only. It does not authenticate intended covalent chemistry, prevent a preformed duplex from cutting, ensure the first cut is correct, remove unsuccessful donors, regenerate a protected chemical terminus, or make all fragments inert. No molecular sequence or completed common operating window is constructed by this calculation.

5. Stock, fidelity and whole-operation limits

For introduced 32 nmol initiator sites, 20 extensions and a 25-nucleotide key at an average 330 g/mol per nucleotide, one consumed key for every successful extension is 640 nmol or 5.28 mg per library. Three attempts at every site use 15.84 mg. These are counts within this organisation, not universal lower bounds: other materials, smaller keys and successful retry schedules can change them. They exclude program scaffold, conjugate preparation and purification, enzyme, protecting groups and waste.

Reusing a small codon alphabet could reduce the number of separately customised packet species only if past signals really cannot act again and the program advances without losing sequence specificity. The recognition chemistry, position/state control, repeats and all consumed molecules remain paid. Smaller alphabet is a hypothesis, not an acquired reusable molecular factory or cost saving.

At .003 independent critical-stock loss per damaging event, 600 events leave .164852 functional stock; 95% after 600 events permits at most 8.54852e-5 loss per event if there is no paid replenishment. This differs from .003 loss per entire production cycle. The two must not be interchanged. For independent hidden errors, 90% correct full 20-step sequences permits per-step error at most .00525417; errors from retention, wrong chemistry, transfer, cleavage, reset and release must share the actual budget, with correlation treated explicitly.

The full useful operation still requires 16 genuinely different 20-step abiotic products, authenticated released output, repeatable preparation/production/reset, a useful physical material response, renewable critical stocks and a matched whole-operation advantage over competent parallel synthesis. A product barcode, a pooled fragment spectrum or favourable isolated transfer probability cannot supply those outputs. Sequence-resolving standards, per-program product recovery and minority-error sensitivity remain physical analytical operations.

No working molecular machine, joint chemistry, material function, measured reliability, whole-cost advantage, algorithmic novelty or all-design obstruction is established. No source recovery, producer execution, physical experiment, purchase, installation, new worker or retrieval/index probe occurred.

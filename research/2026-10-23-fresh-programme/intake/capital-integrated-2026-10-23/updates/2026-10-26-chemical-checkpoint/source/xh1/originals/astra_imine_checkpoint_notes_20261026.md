# Astra Chemistry: reversible precursor checkpoint and amide-reset obstruction
26 October 2026. Working scientific calculations, not measured PNA chemical kinetics or an integrated device.

## Corrected primary benchmark
- Rosenbaum & Liu, JACS 2003, DOI 10.1021/ja038058b: DNA-templated polymerization of PNA aldehydes; up to ten consecutive reductive-aminations yielding 40-unit PNA.
- Liu group, JACS 2008, DOI 10.1021/ja0753997: functionalized PNA tetramer/pentamer aldehydes, multiple lysine side chains and 40-unit products.
- Brudno, Birnbaum, Kleiner & Liu, Nat Chem Biol 2010 (online Dec 2009), DOI 10.1038/nchembio.280: 12 codons, 4.3 x 10^8 template library, six translation-selection-amplification cycles and >10^6-fold model enrichment for a biotinylated PNA.
- Joshi, Romanens & Winssinger JACS 2025, DOI 10.1021/jacs.5c00708: 256 PNA 4mer sequences in primer-extension assay; two s-NHS incorporation/PMe3 reduction cycles with a masked incoming terminus, reported inactive immobilized primer fraction, not a demonstrated 100-step molecular factory. 4mer off-rates from earlier sources ~0.3-1.5/s; substrate/buffer dependence matters.
- He & Liu Nat Nanotechnol 2010 DOI 10.1038/nnano.2010.190: single-solution autonomous DNA walker making oligoamides. Neither DNA-directed polymer growth nor translation-selection is Astra novel by itself.

## Decisive difference of amide versus imine->amine
An activated ester, Parent-NH2 + maskedPNA-COOSu -> Parent-NH-CO-maskedPNA, consumes old primary amine to a low-reactivity amide. Thus masking the new amino head prevents duplication during feed retries (provided no other accessible nucleophiles). An aldehyde, Parent-NH2 + maskedPNA-CHO -> imine -> NaBH3CN -> Parent-NH-CH2-maskedPNA, leaves the old nitrogen a secondary amine; secondary amines can reductively alkylate further, especially with many aldehydes and reducing agent. Terminal masking ALONE is therefore insufficient to prove no double alkylation, site error or branching. Original one-pot aldehyde polymerization works but doesn't establish a masked 100-step fault-tolerant architecture.

A Ugi four-component reaction instead takes the imine from a primary amine/aldehyde to an N-acylated bisamide product, consuming the old reactive amine. The standard model methylamine + acetaldehyde + acetic acid + methyl isocyanide -> CH3-CO-N(CH3)-CH(CH3)-CO-NH-CH3 + water is atom-balanced by RDKit. The carbon derived from acetaldehyde is an unassigned stereocentre (different four substituents), so generic PNA-aldehyde donor-based Ugi would add up to one new stereochemical choice per coupling, introducing 2^L states if racemic and independently selected in an L-step synthesis. Ugi DNA-conjugate chemistry DOI 10.1021/acsomega.3c07136 generally uses concentrated reagents/organic solvent (dry THF, methanol) and doesn't validate near-micromolar donor/template dynamics; site-selective protein Ugi in PBS doi 10.1002/chem.202303242 is closer solvent-wise but requires high substrate, long exposures and demonstrates competing off-target sites. An aqueous vesicle-based Ugi paper DOI 10.1039/C7RA03376A measured 19% isolated product in PBS after 48h with small molecules at ~100 mM; not a demonstration of templated-PNA Ugi. Therefore Ugi is a conceptual *amide-reset* route, not demonstrated synthesis. Oxidative imine-to-amide approaches on aromatic aldehydes (DOI 10.1021/acs.joc.5b01922) likewise do not validate PNA/DNA aqueous oxidative commitment.

## A reversible checkpoint model
Unreduced, parent-connected imine intermediate survives in one of three nonabsorbed states: I_B (DNA-hybridized covalent imine), I_F (DNA-detached covalent imine), H_B (hydrolyzed donor still hybridized noncovalently to DNA with competent parent restored). LOST is a cleared donor plus competent unreacted parent. Rates are I_B->I_F=u_i, I_F->I_B=a_i, I_B->H_B=r_B, I_F->LOST=r_F, H_B->I_B=c and H_B->LOST=u_H. During chase (no reductant), transient generator

Q = [[-(u_i+r_B),u_i,r_B],[a_i,-(a_i+r_F),0],[c,0,-(c+u_H)]].

Starting I_B, state distribution at time t is e_B^T exp(Qt). Adding reductant gives reduction traps of the imine states at k_R, so Q_R=Q-diag(k_R,k_R,0). Probability of irreversible conversion during reduction for time T is

P_commit(t,T)= e_B^T exp(Qt) [-Q_R]^-1 (I-exp(Q_R T)) (k_R,k_R,0)^T.

Mass balance: any non-committed imine or bound hydrolyzed donor can survive the finite reduction window; chemistry must actually clear them before a second step. Rate values are unknown on the intended substrates. The working script tests positivity and computes numerical outcomes.

Conditional comparison: initial imine fractions correct 0.50, wrong 0.05; I_B <-> I_F rebind=.02/s, bound hydrolysis=.005/s, detached imine hydrolysis=.05/s, bound hydrolyzed reformation c=.2/s; 20s reduction at k_R=.2/s; per feed permanent damage d=1e-5. With u_match=.003/s and u_wrong=.3/s, optimal t_chase~246.46s, per attempt correct~.2940, wrong~4.81e-7, F_100~.99644 conditional on unlimited cycles, with ~3.40 attempts per stage. The 100-step expected time lower bound from chase+reduction phases alone is ~25.2 hours. If u_match=.3/s and u_wrong=3/s, same model achieves at best F_100~.00181 after optimization: registered fourmer contact that dissociates quickly is not sufficiently selective. EVERY rate here except the separate reported fourmer-off range is a hypothetical stress-test parameter; the favourable u_match is 100x slower than earlier fourmer examples. This demonstrates a stringent discriminator, not experimental feasibility.

## An exact limit for hydrolysis/reformation proofreading
For the simpler I->H at r; H->I at c; H->LOST at u process, the slow exponential loss rate is
 gamma(u) = ((r+c+u)-sqrt((r+c+u)^2-4*r*u))/2
          = 2*r*u / [r+c+u+sqrt((r+c+u)^2-4*r*u)].
For fixed r,c>0, gamma(u)/u is nonincreasing because its denominator is increasing with u. Hence if u_wrong>=u_right>0,
  1 <= gamma(u_wrong)/gamma(u_right) <= u_wrong/u_right.
This is EXACT for the slow eigenvalue, with no approximation. At r << c+u, gamma ~= r u/(c+u). Long-time single-exponential separation m=gamma_w/gamma_c has the conditional retention-versus-enrichment law: suppress wrong/right odds by a factor E while keeping fraction Y of correct intermediate => Y=E^(-1/(m-1)). For E=1000, if m=2 Y=.001; if m=10 Y=.464; if m=20 Y=.695; if m=100 Y=.933. 50% retention requires m >= 1+ln(1000)/ln(2) ~10.97. The exact matrix model need not obey a single exponential at short times, so this curve is a long-time / effective-hazard criterion, not a universal bound for all multistate networks.

## Optimal checkpoint duration with irreversible damage
If per fresh feed fractions q_c and q_w form correct and wrong imines, chase keeps e^-gamma_i*t, irreversible reduction efficiency eta, and every attempt also has independent irreparable damage probability d (exclusive probabilities), then with recoverable misses and infinitely repeated attempts:
 p=eta q_c exp(-gamma_c*t); w=eta q_w exp(-gamma_w*t);
 F_stage(t)=p/(p+w+d).
Equivalently 1/F -1=(q_w/q_c)exp(-(gamma_w-gamma_c)t)+(d/(eta*q_c))exp(gamma_c*t).
If gamma_w>gamma_c>0 and d>0, the optimal delay is
 t* = max(0, [ln((gamma_w-gamma_c)*eta*q_w/(gamma_c*d))]/gamma_w).
Too short commits wrong intermediates; too long loses productive material and creates more opportunities for irreversible damage. Numerical minimization independently matches the algebra in the script. At q_c=.45,q_w=.045,gamma_c=.002/min,gamma_w=.2/min,eta=.9,d=1e-5: t*=64.51 min, ideal eventual F_100=.99717, but requiring long recovery time. These gamma values are not measured and the simple model neglects reactor aging, shared donor inhibition, heterogeneity and chemical competition.

## Readout ambiguity
For plain canonical PNA tetramers, a full molecule mass reports base composition, not nucleotide order. 4^4=256 sequences fall into only binomial(7,3)=35 compositions, with degeneracy histogram (class size:number of classes) 1:4, 4:12, 6:6, 12:12, 24:1. For example, ACGT has 23 other sequence permutations of identical canonical PNA mass. A full-length MALDI or correct polymer mass does not certify bond site or correct sequence. This does NOT refute targeted MALDI ladders or other established sequencing methods that use additional sequence-dependent experiments. Verification of an Astra factory requires junction/sequence-resolving and end-group functional tests in addition to length/mass.

## Reasoned current selection
Retain Joshi-style terminal-azide masked NHS-amidation with multiple donor feeds before global PMe3 unmasking as the BEST CHEMICALLY GROUNDED near-term way to recover missed reactions; unresolved are the chance of stable wrong amides, waste removal, spatial register, completely stalled strands, pool background and cumulative side chemistry. Maintain a genuinely alternative invention of reversible template-sensitive intermediates irreversibly committed to NON-NUCLEOPHILIC amides (e.g. Ugi or oxidative imine amidation) but do not label it integrated until aqueous templating, stereochemical fidelity and reaction orthogonality are demonstrated. Most decisive interface: can an actual incorrect intermediate dissociate/reverse while a correct one is retained long enough for an amide-forming commitment, with retained competent failed parent? Test both site-specific products and double-functionalization, with true vs wrong donor at same stoichiometry and buffer; site-specificity not just disappearance of a reactive group. No wet lab operation performed.

# Task B — output entropy of a quantum amplifier

All scientific sources below were read publicly at Git revision **6360a39d9488a041f259181e38c37e638b83c609**. The unavailable live library was not silently replaced with a different revision.

**Usable result.** At this revision Astra accepts the amplifier entropy photon-number inequality internally, at the exact reviewed manuscript version described below. Write
\[
S(\rho)=-\operatorname{Tr}\rho\ln\rho,\qquad
g(x)=(x+1)\ln(x+1)-x\ln x,\quad g(0)=0,
\qquad n_\rho=g^{-1}(S(\rho)/m).
\]
The inverse is the increasing inverse on \([0,\infty)\). For the retained state \(C\),
\[
\boxed{\quad S(C)\ \ge\
m\,g\!\left(\kappa\,g^{-1}(S(A)/m)
+(\kappa-1)\big[g^{-1}(S(B)/m)+1\big]\right).\quad}
\]
Equivalently, \(n_C\ge\kappa n_A+(\kappa-1)(n_B+1)\). This is sharp as a bound using only the two entropies: independent product thermal states realize every nonnegative finite entropy pair and attain equality. [Governing statement, manuscript lines 39–64][Mstatement]

The exact class is: the same finite integer \(m\ge1\) in both groups, finite gain \(\kappa>1\), normal states (positive trace-class operators of trace one) on the bosonic Fock space \(\ell^2(\mathbb N_0^m)\), finite mean total photon number \(\operatorname{Tr}\rho N<\infty\), \(N=\sum_j a_j^\dagger a_j\), and the joint input **\(\rho_A\otimes\rho_B\)**. The canonical bosonic annihilators obey the stated ideal two-mode-squeezing transformation; the other output is traced out. Each group may contain arbitrary internal correlations or entanglement. Gaussianity, thermality, and independence of the modes within a group are unnecessary. Entropies above are in nats; use \(S_{\rm nats}=(\ln2)S_{\rm bits}\) when inserting bit entropies. The finite-energy entropy bound \(S(\rho)\le m g(E/m)\) ensures the quantities are finite. [Definitions and energy/domain passage, lines 39–99][Mdefs]

**Requested one-mode calculation.** For independent thermal inputs of mean photon numbers \(1\) and \(2\),
\[
S(A)=g(1)=2\ln2\approx1.3862943611,\qquad
S(B)=g(2)=3\ln3-2\ln2\approx1.9095425049.
\]
At \(\kappa=2\),
\[
n_C\ge2(1)+(2-1)(2+1)=5,\qquad
S(C)\ge g(5)=6\ln6-5\ln5
\approx\mathbf{2.7033672532\ {\rm nats}}
=\mathbf{3.9001345299\ {\rm bits}}.
\]
Equality is warranted. Thermal inputs are centered Gaussian states, and the Gaussian unitary followed by a partial trace yields a centered Gaussian marginal. Independence eliminates cross moments:
\(\langle c^\dagger c\rangle=2\langle a^\dagger a\rangle+\langle bb^\dagger\rangle=2+3=5\), while \(\langle cc\rangle=0\). Its marginal is therefore the thermal state of mean \(5\), whose entropy is exactly \(g(5)\). The manuscript explicitly states thermal attainment and identifies the thermal output through its Weyl Gaussian covariance. [Lines 57–64][Mstatement], [thermal limit and covariance, lines 462–496][Mlimit] These arithmetic values were computed directly with ordinary JavaScript logarithms. A general input need not be thermal: the theorem is an entropy inequality, and the thermal states are extremizers, rather than a prescribed physical form of every output.

**Load-bearing argument actually inspected.** I read the main manuscript through line 522 and the interpolation appendix through line 620. The proof starts from a strict entropy violation, passes to number cutoffs using finite-energy continuity, and constructs a regularized negative minimum. At that minimum the Hessian supplies four form comparisons. The creation port uses the reversed metric \(F_B^\uparrow(v)=F_B^\downarrow(-v)\), with interpolation parameter \(y_B=+h_B/2\), while \(y_A=-h_A/2\); this exchanges the creation port's \(r_B\) and \(r_B+1\) weights. [Signed metric, lines 243–318][Mmetric]

The corrected theorem requires a test space with finite parameter support that is invariant under parameter-dependent scalar multipliers. Four numerical comparisons by themselves do not suffice. Centered finite spectral blocks meet the repaired hypothesis: the diagonal identity tail has frequency zero and receives one common multiplier, preserving centering. In the appendix's parallel-sum proof the minimizing split multiplies the source test by \(Y/(X+Y)\) and \(X/(X+Y)\), which explains why that invariance matters. [Repair, lines 286–318][Mrepair], [appendix theorem and parallel sums, lines 556–608][Mappendix]

The argument then combines the squared-defect entropy-production identity with signed centered-energy cancellation, forces defects and means to vanish, and identifies the limiting product geometric state by a number-basis recurrence. This contradicts the fixed negative witness. Seventh-moment regularity is obtained at the auxiliary minimizers; it is not an extra assumption on the original finite-energy inputs. [Regularity, lines 221–240][Mregularity], [entropy production and final cancellation, lines 421–485][Mcancellation] This was source inspection and reasoning, not a new full proof audit or formal build.

**Actual internal acceptance and correction scope.** The current version-bound decision is **accepted_internally_verified**, review ID **A557-completed-internal-cfdb**, dated 27 October 2026, recognizing the completed 10 October Sol 2/3/4 mathematical reviews. It binds the theorem to manuscript SHA256 **cfdbb6a0ca85861788d39c8843ce7533a641633c4cabab8070ac09b9d41d170d**. I read all three final review files, not just the packet labels. They contain end-to-end reconstructions and exact final-delta checks; after the repairs they report no remaining required mathematical fix. The repairs include graph-domain composition, the centered dual norm, half-integer weighted exponents, individual interpolation parameter indices, and cutting off a discarded operator in its own discarded number basis so it still commutes with retained observables. [Sol 2, lines 1–171][R2], [Sol 3, lines 1–91][R3], [Sol 4, lines 1–44][R4]

The current recognition explicitly says these substantive internal reviews suffice for Astra acceptance at this version and scope; external specialist review and formal verification are not prerequisites for that acceptance. Older “candidate,” “unreviewed,” or next-external-gate language remains historical source text. The acceptance neither supplies external/formal verification nor expands the theorem's domain. [Recognition, lines 3–31][Recognition], [version-bound review][Acceptance]

I also inspected the later **W49 heated logarithmic-tail audit**, including its verdict, shift argument, explicit counterexample, and boundaries. Its target is another manuscript, SHA256 **2167da8029a740a937b5ae477a1bf984fd34d4f9b6c02ce001ee02c8bc191e6e**, concerning actual heat applied to a specified thermal-mixture tail class. Its correction replaces an unjustified \(O(1/r)\) assertion about the total relative density change under fixed shifts with preservation of the two-term expansion and an \(o(1/\log r)\) remainder. The oscillatory density counterexample directly refutes only the stronger sentence. [W49, lines 1–39][Wverdict], [lines 298–346][Wshift], [lines 404–458][Wcounter]

W49 also states general unheated EPnI is NOT_ACHIEVED. That contrary programme-status sentence remains visible; it is not an audit or identified defect of the cfdb manuscript. The current recognition expressly separates the two scopes. Thus W49 neither supplies the unrestricted proof nor cancels the completed cfdb review chain. [Recognition, lines 33–47][Recognition]

**Independence and broader classes.** Removing cross-group independence actually invalidates the displayed bound, even for a separable joint input. The manuscript takes a circular complex Gaussian \(z\) of variance \(v>0\) and mixes coherent product pairs with amplitudes \(\sqrt{\kappa-1}z\) and \(-\sqrt\kappa\,\bar z\). Their retained displacement cancels. The marginal inputs are thermal with means \((\kappa-1)v,\kappa v\), but the retained output is thermal with mean \(\kappa-1\). The putative bound without independence would require entropy photon number at least \((\kappa-1)+2\kappa(\kappa-1)v\). In particular, \(\kappa=2,v=1\) has the same thermal marginals of means \(1,2\) as the requested example, yet output entropy \(g(1)<g(5)\). [Explicit independence counterexample, lines 498–506][Mindependence]

Infinite mode count, infinite mean energy or a merely finite-entropy broader class, correlated/shared-reference versions, and equality uniqueness are outside this accepted statement; no extension follows from the present limit argument. The general theorem does not require a measured state, an acquired tail law, or a thermal output. It establishes no working apparatus, entropy-estimation procedure, communication capacity advantage, efficiency guarantee, or historical priority. [Manuscript, lines 498–519][Mresources], [acceptance boundaries][Acceptance]

**Actual route and initial exposure.** The only local source read was TASK_B.txt. The public GitHub connector successfully read the pinned entry point, pinned knowledge/index.html, no-script browse index, EPnI/bosonic topic pages, LA102 packet, N557 packet, governing manuscript, exact review overlay/recognition, three final reviews, and W49 audit. The live library URL returned an inaccessible/Internal Error response from the web reader. GitHub code searches for “amplifier entropy” and “EPnI” returned no results. Those failures were overcome through the pinned no-script browse → LA102 source/update links → N557 packet → exact theorem and reviews. No absence-of-science conclusion was drawn from a failed URL or search. [Entry point][Entry], [static browse route][Browse], [LA102][LA102], [N557][N557]

Initial product context supplied a general Astra memory summary, including evidence-gating practices and the user's preference that substantive completed internal audits count at their actual scope. That is prior exposure to a status preference and possible cold-start bias. It did not supply this amplifier theorem, card ID, proof/version facts, or the example's answer. I opened no memory registry, other chat, prior experiment report, protocol, expected-scope file, local corpus/cache, or other experiment worker's output. I used no local retrieval/search runtime, clone, browser/CUA control, paid API, research-script execution, hardware, or publication action. The only filesystem write was this report.

[Mstatement]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L39-L64
[Mdefs]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L39-L99
[Mmetric]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L243-L318
[Mrepair]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L286-L318
[Mappendix]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L556-L608
[Mregularity]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L221-L240
[Mcancellation]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L421-L485
[Mlimit]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L462-L496
[Mindependence]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L498-L506
[Mresources]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/amplifier_proof_candidate.tex#L498-L519
[R2]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/work/reports/final_review_sol2.txt#L1-L171
[R3]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/work/reports/final_review_sol3.txt#L1-L91
[R4]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/updates/BY/package/astra_ultra_campaign/work/reports/final_review_sol4.txt#L1-L44
[Recognition]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/knowledge/audits/2026-10-27-amplifier-review-recognition.md#L1-L47
[Acceptance]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/knowledge/reviews/A557-completed-internal-cfdb.json
[Wverdict]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-24-run-closeout/evidence/checkpoints/v10/w49__log_tail_entropy_audit__FULL_FRESH_LOG_TAIL_AUDIT_V1.md#L1-L39
[Wshift]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-24-run-closeout/evidence/checkpoints/v10/w49__log_tail_entropy_audit__FULL_FRESH_LOG_TAIL_AUDIT_V1.md#L298-L346
[Wcounter]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-24-run-closeout/evidence/checkpoints/v10/w49__log_tail_entropy_audit__FULL_FRESH_LOG_TAIL_AUDIT_V1.md#L404-L458
[Entry]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/00_START_HERE.txt
[Browse]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/knowledge/current/browse/epni.tsv
[LA102]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/knowledge/current/packets/LA102-signed-four-weight-transfer.json
[N557]: https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/knowledge/current/packets/N557.json


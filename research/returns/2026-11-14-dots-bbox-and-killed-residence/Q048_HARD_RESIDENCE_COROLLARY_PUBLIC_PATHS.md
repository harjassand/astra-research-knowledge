# Hard all-minus residence numerator: integrated finite-volume corollary

## Statement
For the1600×1600 periodic nearest-neighbor Ising heatbath chain with energy E(S)=8P(S)−|S|/25 and independent rate-one site clocks, let a be all-minus and B={|S|≥1280000}. Normalize w(a)=1. Let h(x)=P_x(τ_a<τ_B), with h(a)=1,h(B)=0, and let C=cap(a,B) use native conductances w(x)q(x,y). Then the computer-assisted construction assembled in COMPLETE_KILLED_PATH_PROOF.md and its listed directed static certificates gives

1 ≤ N := Σ_x w(x)h(x) <1+1.087×10^-7.

Consequently the exact mean first-passage identity yields

1/C ≤ E_a τ_B < (1+1.087×10^-7)/C.

This closes the hard-source RESIDENCE NUMERATOR, not the capacity or an efficient trajectory sampler. For separately valid hard-capacity bounds C_lo≤C≤C_hi, one may conclude
1/C_hi ≤E_aτ_B <(1+1.087×10^-7)/C_lo.
No equality with a soft-source capacity or numerator is assumed.

## Proof chain
1. After leaving a, the native exit law is uniform singleton, with λ_a=n/(1+e^31.96)<10^-7. Regenerative occupation and reversibility give
   N=1+λ_a E_singleton τ_{a∪B}.
2. Inside analytical box164 core, exact raw-face/polymer bounds give an occupation contribution beyond a at most Γ/(1−Γ), with Γ<1.087×10^-7. Its sharper rational value is retained in renewal_box164_raw_faces.py.
3. The same exact scalar certificate gives a first departure probability p below10^-450; it includes all gate multiplicities, full companion gas, and native λ division. No claim that these rare departures are automatically short is used.
4. The global canonical construction, with original-component history and overwrite reconstruction, has occurrence-counted congestionρ<e1000. This uses the independently reviewed hull, critical-strip and full-cylinder partition bounds, all actual phase records, and native inverse rates. See creative's complete proof and GLOBAL_KILLED_PROOF_REVIEW.md.
5. Killed spectral contraction yields a UNIFORM mean time M<22000000 e1000 from every state outside a/B, including every possible first-departure configuration and arbitrary winding/thermal companions.
6. Strong Markov at first core departure bounds all subsequent outside occupation by pM, even with repeated returns and departures. The exact rational script conditional_duration_numerator.py proves, using e<87/32, that λ_a pM<6.571×10^-21 and the total numerator excess is below1.087×10^-7.

The script's historical filename records that its scalar implication was developed before the global proof. Its congestion input is now supplied by that proof, not by finite tests. It remains useful as a modular conditional check if an input certificate is changed.

## Evidence and limitations
The general argument is analytic plus explicit finite directed arithmetic. Exhaustive/random small-system tests support implementations but do not establish the large-system theorem. Keep the saved upward moment tables, positive-recurrence source, scalar scripts, proofs and reproduction instructions together.

The bound M is enormous. This theorem does not say native or guided trajectories can finish practically, does not prove controlled sampler variance/work, is not uniform in system size, and does not imply a new engineering capability. The physical first-passage target is unchanged throughout.

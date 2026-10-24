# Donor-OH checkpoint: scoped causal audit

## Chemical event and observable

Write the upstream donor as \(D{-}O{-}C(O){-}P\), where \(P\) is the growing chain, and the bound downstream aminoacyl adaptor as \(H_2N{-}B{-}C(O){-}O{-}A\). The intended transfer and the competing hydrolysis are
\[
\begin{aligned}
D{-}O{-}C(O){-}P + H_2N{-}B{-}C(O){-}O{-}A
&\longrightarrow D{-}OH + P{-}C(O){-}NH{-}B{-}C(O){-}O{-}A,\\
D{-}O{-}C(O){-}P + H_2O
&\longrightarrow D{-}OH + P{-}C(O){-}OH.
\end{aligned}
\]
In the second branch, the bound downstream adaptor remains \(H_2N{-}B{-}C(O){-}O{-}A\). Both branches produce the same donor-DNA 3'-OH and preserve its DNA control sequence; they differ in where the organic chain resides. Therefore the donor-OH checkpoint alone does not logically witness transfer to the intended acceptor. This is an event-alias, not a claim that the full physical states are identical: chain attachment, charge, sterics, and geometry can change subsequent binding or enzyme access and might provide a discriminator if independently acquired.

Conditioning on the same downstream adaptor being bound and the blocker site exposed removes the trivial distinction that one branch has not yet admitted \(A\). It does not remove the alias: hydrolysis can release \(P{-}C(O){-}OH\) while the still-aminoacylated \(A\) performs its DNA competition step. A DNA progression record may then advance without the intended peptide bond. If hydrolysis occurs earlier, downstream-adaptor binding is still a separate necessary event before this DNA gate opens.

## What polymerase advancement actually requires

A free 3'-OH is necessary but not sufficient for extension. In the cited Bath–Turberfield design, the spent upstream adaptor's 3' end must hybridize to the displaced 3' end of the blocking strand to provide the primer/template duplex; polymerase and nucleotide substrate are also required. Since either chemistry branch gives the same donor adaptor with a 3'-OH, this DNA priming route can in principle report the same advancement in both branches. The primary reports polymerase/blocker operation and use of hydrolyzed adaptors as primers, while the aminoacyl-transfer step itself remains future work; it does not demonstrate that transfer product and hydrolysis product have matched extension kinetics. [Bath and Turberfield, *Nanoscale Horizons* (2026), DOI:10.1039/D5NH00505A](https://doi.org/10.1039/D5NH00505A).

## Minimal condition for interpreting an advancement rate

For a minimal two-branch ledger conditioned on bound \(A\), let \(p=\Pr(T)\) be the probability of correct transfer, \(q_T=\Pr(O\mid T)\), and \(q_H=\Pr(O\mid H)\), where \(O\) is observed DNA advancement. Then
\[
\Pr(O)=p q_T+(1-p)q_H.
\]
Advancement identifies transfer only if hydrolysis cannot advance (\(q_H=0\)) and the other assumptions of this two-branch conditioning hold. More generally, an acquired bound \(q_H\le\eta<1\) would give the conservative implication
\[
p\ge \max\!\left\{0,\frac{\Pr(O)-\eta}{1-\eta}\right\},
\]
using only \(q_T\le1\); without a hydrolysis-advance bound, the DNA record alone gives no nontrivial lower bound on transfer. A product/acceptor-sensitive measurement or a validated chemical selectivity gate is needed to certify the bond.

This is a scoped causal objection to using donor-OH/blocker progression as a transfer witness. It does not imply transfer is impossible, that hydrolysis dominates, or that payload-dependent physical discrimination cannot be engineered. No hazard rates, transfer yields, or full-assembler capability are inferred here.

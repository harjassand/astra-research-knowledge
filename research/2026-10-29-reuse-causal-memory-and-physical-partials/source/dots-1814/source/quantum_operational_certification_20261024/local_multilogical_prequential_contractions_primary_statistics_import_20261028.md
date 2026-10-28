# Primary statistics import for local retained memory recovery

28 October 2026. Independent reviewer `producer-workspace/audit_count_pilot_fresh`. This is a source-disabled primary-text check, not an acquisition result.

## Matrix martingale concentration

I independently read Joel A. Tropp, *Freedman's Inequality for Matrix Martingales*, Electronic Communications in Probability **16** (2011), 262–270, Theorem 1.2 on printed page 264 (PDF page index 2). The inspected primary PDF reports submission on 15 January 2011 and final acceptance on 25 March 2011. [Primary paper](https://tropp.caltech.edu/papers/Tro11-Freedmans-Inequality.pdf).

For a self-adjoint dimension-d martingale with differences X_t satisfying lambda_max(X_t)<=R almost surely, its predictable quadratic variation is W_t=sum_(s<=t) E_(s-1) X_s^2. The theorem bounds the event that, at some time, lambda_max of the martingale is at least a threshold t and ||W|| is at most v by

`d exp[-t^2/(2(v+Rt/3))]`.

Applying the theorem separately to X and -X, and restricting to a fixed deterministic number N of increments, gives the two-sided norm probability

`2d exp[-N a^2/(2(v0+R a/3))]`

when each conditional second moment is at most v0 I. No independent-increments or identical-state assumption is required. The current source application uses R=2d, v0=3^w and a=kappa/(8d). Correlations between different learners' martingales do not enter a union bound.

This note imports only that established concentration inequality; it does not claim a new proof of the matrix exponential theorem. The filtration, current-record law, predictable variance and finite parameter substitution are checked independently in the accompanying statistics audit.

## Local Pauli measurement representation

I independently read Huang, Kueng and Preskill, *Predicting Many Properties of a Quantum System from Very Few Measurements*, arXiv:2002.08953v2 (22 April 2020), Proposition 2 and equation (S44), printed page 25 (PDF page index 24). The source identifies the one-copy inverse-measurement representation as the tensor product of the single-qubit matrices 3 Pi-I. [Primary manuscript](https://arxiv.org/pdf/2002.08953v2).

The audited construction uses only that one-copy linear representation. Its explicit direct Born-law calculation of first and second moments is independent of the manuscript's iid shadow-estimation guarantees. Neither an iid concentration theorem nor a reset assumption is imported.

## Evidence limits

The primary PDFs were read through the web tool's parsed text. No visual page-inspection or downloaded PDF byte-hash verification is claimed. There were no source calls, random draws, quantum experiments or modifications to previously received material.

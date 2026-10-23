# Continuation of coherent recurrent communication

## Current question

At the one fixed `beta=1/512`, `alpha=sqrt(1-beta^2)`, and the actual one fixed normal initializer `tau_pi`, can reliable unassisted communication exceed `3/2` qubits per counted forward qutrit call? Or is there a capacity plateau? The feedback equality question at nonzero beta is also open. The current operation does not answer either.

## What this checkpoint changed

The intended high-entropy iid coherent seed cannot make the bath tight. The exact root-retaining corrector proves exponential depth escape. For the actual bath, charge conservation proves linear entropy growth and an exponential rank requirement for every asymptotically lossless final-bath projection. This is not merely failure of a coordinate cutoff.

The stronger new benchmark is exact: the optimized iid/tensor-power coherent information is `3/2` asymptotically for every fixed beta<=1/8, even if the marginal is chosen anew at each horizon. A general code, nonidentical independent products, or feedback can fall outside this input family. The result should not be promoted to a capacity converse.

## Objects to retain

The entire bath is `C^2_seed tensor F(C^2)`, with creation isometries S1,S2 and a vacuum exchange R. `U=[[R,S1,S2],[S1*,0,0],[S2*,0,0]]`; no boundary may be deleted. `tau_pi` has each depth-l vertex eigenvalue `(1/3)6^(-l)`, multiplicity `2^(l+1)`. Actual initializer, device, angle and no-return capacity contract stay fixed. All calls and all outcomes count. No bath access, reset, fresh bath, free entanglement or timing channel is available.

The exact algebra and root relations are in `representation/exact_representation.py`. The prior whole-bath Dyck identity, exact two-call erasure interface and finite-error-set coding proof are preserved in the unchanged Cycle2 ZIP. Do not infer a reusable coding operation from the bath average alone.

## Selected next operation

Use a minimally correlated two-call input on the full nine-dimensional port space:

`varrho = x |00><00| + z sum_(a,b=1,2) |ab><ab| + sum_(a=1,2) [ y(|a0><a0|+|0a><0a|) + c(|a0><0a|+|0a><a0|) ]`.

Take real `x,z>=0`, `y>=|c|`, `x+4y+4z=1`. Its eigenvalues are x, z four times, and y+c and y-c twice each. Both marginals are diagonal with zero probability `q=x+2y` and colored entries `y+2z`. At `(x,y,z,c)=(1/4,1/8,1/16,0)` it equals the critical product input and has entropy 3 bits per block. Negative c favors antisymmetric zero/color order; this is motivated by the actual prior dark-pair identity, not a claim that a dark vector carries a high rate.

First derive the EXACT two-call bath map and its charge/corrected-depth identities, retaining all final-bath overlaps and the root exchange. Decide whether parameters with entropy above 3 per block can have subextensive complementary information from the actual tau_pi. If the single-site obstruction extends, prove its actual block version and use it to revise the family. If it fails, identify a specific surviving cancellation, an honest entropy/overflow estimate and a whole-block arbitrary-reference coding consequence.

The relevant comparison is the tensor-power theorem, whose fixed single-site bath map is absent here. Merely increasing finite-block Kraus rank or input entropy will not count as reliable communication. If blocks are repeated, they share the same evolving bath; no iid channel uses or free bath replacement may be assumed.

## Evidence that would change the route

A bounded corrected-drift operator for this exact correlated map, together with an appropriate entropy-flow inequality, could close its stabilization mechanism. Conversely, a demonstrated cancellation with a provable long-time bath entropy or smooth-rank bound could reopen a controlled compression construction. Either result must include the actual initializer or a charged preparation/reachability argument; a formal invariant state alone is insufficient.

The family is a selected next starting point, not a candidate already proved to beat 3/2. The angle never scales with n. No new correlation theorem or compiler has been run during this checkpoint.

## Routes to retain as failures

Do not reopen balanced-only rate gain, biased diagonal sublinear-depth compression, exact product stationarity, or finite reflecting-cutoff stationarity. The current theorem additionally closes high-entropy SINGLE-SITE IID stabilization and asymptotically lossless subexponential-rank bath compression. Positive drift alone does not imply exponential escape; growing entropy alone does not imply exponential smooth rank. The actual proof supplies both missing controls.

## Source and ownership

Read `COHERENT_INPUT_ESCAPE.tex` and its three included sections, then the focused reviews. `preserved/Astra_Amplification_Cycle2_PRO1_20261022.zip` is unchanged. Max integrates; the evaluator studies methods/transfer. Source delivery does not imply their acceptance. R1, hidden-entropy, N33, N557, IQM, Morrey and closed material/guide operations retain their prior owners and boundaries.

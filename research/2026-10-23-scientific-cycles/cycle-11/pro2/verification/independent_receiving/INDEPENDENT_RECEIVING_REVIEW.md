# Independent Cycle11 original-action receiving verification

## Verdict and scope

**PASS on the first checker execution.** Both saved native receiving operations and the separate three-isolated-vertex direct-sum check pass exact verification. The checker imports only Python standard-library modules. It does not import or execute producer code, any earlier closure engine, or an old scientific suite.

The verification certifies the two saved graph/design pairs and their actual full-original-action records. The exact incidence-Gram certificates additionally establish the squared inverse bound 18 for **all action noise on each of these two fixed designs**. This is not an independent proof that every graph in the theorem class admits the producer's construction. Universal local-family coverage and all-depth existence are separate proof obligations handled elsewhere.

Checked receiving source:

- `results/RECEIVING.json`, SHA256 `4d883f8ba015cacdb3dcd3725b372a5c421bc95a9290e05fe2dfb6fa366db7be`.
- The two native original input files are checked against the saved byte counts and SHA256 values, then read directly. Construction-provenance metadata is not used as a graph oracle.
- The saved producer source hashes are compared with source bytes. Those source files are never imported or executed by this checker.

## What was reconstructed independently

1. The simple original graph, its maximum degree, all bridges, the components remaining after deleting bridges, and all biconnected edge blocks inside those modules.
2. A treewidth-at-most-two certificate, recorded as a degree-at-most-two elimination order with fill. A degree-two fill edge is paid in the certificate; it does not change the action support.
3. Chordlessness of the original graph. For each original edge uv, the checker verifies that G-uv has no two internally vertex-disjoint u-v paths. Bridges and degree-at-most-two endpoints give immediate certificates; the remaining edges use an integral vertex-capacitated maxflow stopped at value two. The 49-vertex graph requires six nontrivial flow checks, all with value one.
4. Proper coordinate colors and their unit whole-row norm; every nontrivial bichromatic component is reconstructed and checked to be a tree. All saved component inventories are compared against the original graph.
5. Actual atom edge sets and local star colorings, including actual neighbor multiplicities and far-repeat flags. Atom colors are checked through the recorded permutation to the final original vertex colors. The observed degree-three family labels are 24, 26 and 4; this verifies their supplied realizations, not every member of those families.
6. Actual bridge orientation, specified child entry, module entry degree, missing incoming channel, and the outgoing color prohibition when another bridge leaves that same entry vertex. Every child endpoint is directly verified to have degree one in its incoming bichromatic component of the full original graph.
7. Every bichromatic component has at most one nontrivial original module core. That core is directly checked to be a spider with arms of length at most two; every vertex outside it is a pendant connected to the core. Components having no nontrivial core are directly checked to be bridge stars. No diameter-only surrogate is used.
8. Original coefficients, the full original D X, added rational noise, saved observations, exact least-squares output, exact projected action and raw residual. Zero-valued coefficients on allowed edges remain in the supported input class and do not remove those graph edges.

## Separate exact inverse

For a color pair (a,b), multiply its observations at color-a vertices by +1 and at color-b vertices by -1. Subtract the mean of this signed divergence over the actual tree component. The checker then repeatedly removes a leaf, recovers its edge coefficient from its remaining divergence, and subtracts that edge's contribution from the neighboring vertex. The final divergence is exactly zero.

The diagonal is recovered from each row's own-color observation. Each action coordinate not used by the diagonal or a nontrivial pair component is projected to zero. Thus the checker obtains the canonical orthogonal projection independently of the saved decoded output.

It separately verifies the normal equations: each own-color residual is zero, and for every original edge uv the two corresponding residual entries sum to zero. The decoded full action equals the independently projected observation exactly. The raw noise residual need not vanish; its exact norm is checked against the saved value.

## All-noise certificate for the saved designs

For each nontrivial tree component, let Q be its unsigned vertex-by-edge incidence matrix. The checker constructs the exact integer matrix

    9 Q^T Q - I

and performs rational LDL elimination. Every pivot is strictly positive. The ordered original edges and exact pivots are saved in the result. This proves that the smallest eigenvalue of Q^T Q exceeds 1/9 and therefore that the edge-coefficient least-squares inverse has Euclidean norm at most 3.

Each off-diagonal coefficient contributes twice to the reconstructed symmetric matrix's squared Frobenius norm. Hence each pair block has squared Frobenius-output gain at most 18. Diagonal gain is one. The pair/diagonal observation coordinates are disjoint, so summing these inequalities gives

    ||Dhat-D||_op^2 <= ||Dhat-D||_F^2 <= 18 ||E||_F^2.

This exact Gram check is an independent certificate of the asserted fixed-design norm bound; a floating eigensolver status or just the two observed error ratios is not used for that purpose.

## Observed receiving records

| Operation | Vertices / edges | Modules / atoms | Pair trees | Bridge resets | Squared error/noise ratio | Cut balance |
|---|---:|---:|---:|---:|---:|---:|
| Mixed native bridge entries | 49 / 61 | 16 / 8 | 38 | 8 | 581947/884700 | 1 |
| Same-graph entry-reset chain | 27 / 35 | 9 / 9 | 27 | 7 | 35897/58194 | 2/3 |

The mixed receiver's actual degree-three entries are vertices 1, 17 and 38. Their internal neighbor-color multiplicities are respectively [0,0,1,2], [0,3,0,0] and [0,3,0,0]. Each has a real missing incoming channel on its original support.

The noiseless reconstruction is exact in both cases; the projected numerical residual is exactly zero in both. The nonzero raw residual norms squared are 48051/204020 and 9539/61206, respectively. Three isolated vertices are checked separately by their own-color diagonal observations.

**Unexercised inherited branch:** both native receiving records have zero internal block stop messages. The checker confirms this count. These inputs therefore do not newly exercise a nonzero stop-message branch inherited from Cycle10. No input was changed to inflate branch coverage.

## Replay and costs

From the source archive root, use an appropriate relative path to the checker:

```text
python independent_receiving.py --root PATH_TO_CYCLE11_SOURCE --output NEW_RESULT.json
```

The first complete checking body, including native input/source hash reads but excluding final JSON serialization, took 0.015028567999252118 seconds wall and 0.014992446999999999 seconds CPU. Peak process RSS was 14,127,104 bytes. Per-operation bodies were approximately 0.007997 and 0.004688 seconds. These measurements do not include checker authoring, reading, research, inference, proof review, process startup, or source integration; those totals remain unknown. This is verification cost, not discovery cost or a practical application comparison.

Checker source: `independent_receiving.py`, 26,060 bytes, SHA256 `023d4823124d9acec35fde94cda09dbc5339a2a35bb026efa91caa5cb712ed06`.

Saved result: `INDEPENDENT_RECEIVING_RESULT.json`, 56,961 bytes, SHA256 `a75e5792dd1edd4d014a8313dc699ccd420de1a348b857a969a91ec11c2bb68b`.

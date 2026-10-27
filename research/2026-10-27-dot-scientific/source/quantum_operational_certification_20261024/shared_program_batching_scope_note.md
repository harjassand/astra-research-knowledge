# Shared-program batching: current mechanism and access boundary

2026-10-27. No reusable-decoder or amortization theorem established.

The consumed-program receiver charges a fresh bank for every data attempt. Simply sharing a DME bank across K systems is not an automatic saving: a generic collective simulation estimate depends quadratically on the total evolution time Kt. At fixed complete-batch error, this has the same K² scaling as splitting the error budget over K fresh simulations. This compares two straightforward constructions; it is not a batching lower bound.

A concrete reference-recycling precedent is [Bartlett, Rudolph, Spekkens and Turner, Degradation of a quantum reference frame](https://arxiv.org/html/quant-ph/0602069). Their directional-reference longevity scales quadratically with the number of aligned spins. However, the degrading test sequence consists of independent maximally mixed spins, previous measurement outcomes are averaged, and quality is an average orientation-test criterion. Those assumptions do not supply a worst-case correlated multi-data recovery guarantee or a mixed-sample preparation method for this task.

Thus this paper suggests a collective-reference mechanism worth testing, not an available amortization theorem. A valid extension here must account for program preparation from ordinary channel outputs, back-action, retained outcomes, correlations among future outputs, and complete instrument error across the stated batch. Equally informed classical tomography can yield a reusable description at dimension-dependent one-off cost; it is not excluded by the dimension-independent consumed-sample results.

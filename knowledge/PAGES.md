# Bounded public navigation

The complete source repository includes originals, historical site payloads,
native retrieval indexes and model assets. Publishing that entire tree produced
a roughly1.8GBartifact and two10minute file-synchronization timeouts. The
browser's actual navigation closure is about351MBbefore compression, with all
current packets. The existing GitHub Pages publisher can serve that generated
view after its one-time source selection; exact original/history/source bytes
remain in the public Git tree.
GitHub documents a1GBpublished-site limit and10minute deployments:
https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

`knowledge/current/records.jsonl` remains the sole canonical normalized corpus.
The Pages branch is a generated projection, never another authoring source.
Search rankings, scientific statements, review status, conditions and IDs do not
change during publication. Packet/catalog/posting bytes are copied from one
committed manifest; every canonical record must have its packet. Original code
is evidence and is not executed by publication.

Ordinary intake follows `knowledge/INTAKE.md`: preserve originals, update the
existing authoring formats, build/check, relevant source-use checks, reviewed PR,
required CI and verified main merge. Then run:

```
python3 knowledge/pages.py publish --revision <verified-main-merge-SHA>
```

The command stages privately, validates exact canonical view hashes and a
500MBtotal budget, and pushes only `codex/astra-pages`. It refuses a superseded
main, an unowned publication branch, missing support/views, incomplete packet
coverage and mixed source metadata. It leaves main, the active index and unrelated
work unchanged. Existing publication-branch history is retained; an identical
source view needs no new commit. A push is not a successful Pages deployment.

For a local reviewable artifact, outside the source checkout:

```
python3 knowledge/pages.py stage --revision <full-SHA> --output <new-private-directory>
python3 knowledge/pages.py check --output <same-private-directory>
```

The existing Pages site is configured once to use branch `codex/astra-pages`,
folder `/`, with its current legacy publisher. No workflow, recurring task,
credential, permission, paid endpoint or additional service is introduced.
Public visibility and HTTPS stay unchanged. Subsequent publication-branch pushes
use that same existing Pages deployment. Keep its previous source setting in the
private deployment receipt until actual new-site verification succeeds.

`publication.json` binds the web view to an immutable source revision and the
normalizer's input version. The same binding is embedded in the search page and
checked against the exact search-manifest bytes. Source, full-review and transfer
links lead directly to that public Git revision, so a later main change cannot
silently redirect a governing proof. A mixed page/data version fails visibly and
asks for a reload. The old full-tree site remains readable during migration.

Full archives, old site assets and frozen interfaces are not copied into the
bounded Pages artifact. They remain unchanged and public in GitHub. The site's
history page links the pinned complete tree and original historical entry.
An old non-navigation Pages path shows an explicit archived-source pointer when
that exact path exists in the pinned tree; it does not impersonate the original
file's bytes or return a fabricated theorem. Agents should use the immutable raw
base in `agent/ACCESS.txt`, or the actual source URL returned by current search.

Before release closeout, verify the actual Pages build, current search/packet,
rendered source link and the supporting passage. Check that source revision and
input version match the verified main merge, and retain failed deployments.
Publication fidelity does not replace the source's actual scientific review.

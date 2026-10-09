#!/usr/bin/env python3
"""Pin sources actually read: two spin versions plus reused primary interfaces."""
from pathlib import Path
import urllib.request, hashlib, json, shutil
ROOT=Path(__file__).resolve().parent
OWNED_PREVIOUS=ROOT.parent/"cycle06_record_transfer"/"primary"
PRIMARY=ROOT/"primary";PRIMARY.mkdir(exist_ok=True)
entries=[]
for version,date,scope in [
 ("quant-ph/0212114v1","2002-12-19","Live SectionIII-equivalent Eq3 and projector/threshold passages; historical v1 only. Its older Eq6 differs from corrected v3; not imported into the derivation."),
 ("quant-ph/0212114v3","2003-07-12","Live SectionIII Eq3 and Eq9-10, separability threshold and coherent-product twirl. Familiar spin-qubit state/threshold are known prior art; whole paper proof not independently reconstructed.")]:
 url="https://arxiv.org/html/"+version
 filename=version.replace("/","-")+".html"
 req=urllib.request.Request(url,headers={"User-Agent":"Codex scoped source cache"})
 with urllib.request.urlopen(req,timeout=30) as r: data=r.read()
 (PRIMARY/filename).write_bytes(data)
 entries.append(dict(id=version,version_date=date,url=url,path="primary/"+filename,
                     bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),
                     read_status="LIVE_EXACT_PRIMARY",scope=scope,
                     date_note="Arxiv version header and submission history determine version date; rendered document date is an HTML conversion artifact."))
for filename,version,date,scope in [
 ("1506.06377v2.html","1506.06377v2","2015-08-13","Shirokov Theorem2/C3 extended-CMI and local-unconditioned-system monotonicity, checked live Cycle06; immutable primary interface reused for finite theorem."),
 ("2601.09995v1.html","2601.09995v1","2026-01-15","Hayashi-Zhao Theorem1 exact double-Markov PVM structure, read live after Cycle06 baseline; exact known endpoint only, no approximate consequence imported.")]:
 data=(OWNED_PREVIOUS/filename).read_bytes()
 (PRIMARY/filename).write_bytes(data)
 entries.append(dict(id=version,version_date=date,url="https://arxiv.org/html/"+version,
                     path="primary/"+filename,bytes=len(data),
                     sha256=hashlib.sha256(data).hexdigest(),
                     read_status="PINNED_ACTUALLY_READ_PREVIOUS_CYCLE_REUSED",scope=scope))
registry={"schema":1,"date":"2026-10-09","sources":entries,
 "search_queries": [
  "quantum approximate double Markov conditional mutual information separable stability",
  "quantum two conditional mutual informations I(A:B|C) I(A:C|B) entanglement bound",
  "k extendible trace distance mutual information logarithm dimension lower bound entangled states",
  "relative entropy coherence conditional mutual information classical marginal tripartite dephasing inequality",
  "SU(2) invariant state spin one half spin S entanglement projector J minus half Schliemann",
  "relative entropy of entanglement trace distance dimension-independent regularized",
  "approximate double Markov quantum",
  "broadcast conditional mutual information entanglement separable"
 ],
 "search_cost":"8 queries in 3 batched web calls; focused primary opening Schliemann v1/v3 and abstract/version history. Search snippets and nonprimary pages are not proof premises.",
 "novelty_status":"UNKNOWN. These bounded searches do not certify historical priority or exhaustive coverage.",
 "mathematical_imports":"Finite SSA, relative-entropy data processing, CMI monotonicity, Pinsker. Marginal repair is a separately audited Cycle05 lemma, re-stated in origin baseline.",
 "cache_scope":"Exact source bytes; integrity is not theorem validation."}
(ROOT/"PRIMARY_SOURCE_REGISTRY.json").write_text(json.dumps(registry,indent=2)+"\n")
print(json.dumps({"source_cache":"PASS","sources":len(entries),"new_live_versions":2,"reused_pinned_interfaces":2}))


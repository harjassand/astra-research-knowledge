"""Floating diagnostic only; no rare-probability or convergence certificate."""
import json,numpy as np
from pathlib import Path
from scipy.sparse import csr_matrix
p=Path(__file__).parent/'d13_r13_p1_1000_graph.json';G=json.loads(p.read_text());edges=G['edges'];nd=G['internal_vertices'];n=max(max(e) for e in edges)+1
probs=np.array([e['p_float'] for e in G['errors']]);costs=np.array(G['costs']);g=(1-probs)*2.**(-costs)+probs*2.**costs
states=[];adj=[[] for _ in range(n)]
for i,(u,v) in enumerate(edges):states.extend([(u,v,i),(v,u,i)]);adj[u].append((v,i));adj[v].append((u,i))
sid={(u,v):i for i,(u,v,e) in enumerate(states)};row=[];col=[];vals=[]
for i,(u,v,e) in enumerate(states):
 if v>=nd:continue
 for w,f in adj[v]:
  if w!=u:row.append(i);col.append(sid[v,w]);vals.append(g[f])
T=csr_matrix((vals,(row,col)),shape=(len(states),len(states)));right=set(G['right']);b=np.array([float(v in right) for u,v,e in states]);starts=[sid[u,adj[u][0][0]] for u in G['left']];first=np.array([g[states[i][2]] for i in starts]);h=b.copy();weights=[]
for length in range(1,501):
 weights.append(float(first@h[starts]));h=T@h
Z=sum(weights);mom=sum((i+1)*x for i,x in enumerate(weights))/Z
out={'scope':'floating weighted-walk envelope diagnostic only','Z_500':Z,'mean_proposed_length':mom,'mass_first_30':sum(weights[:30])/Z,'mass_first_150':sum(weights[:150])/Z,'length_weights_first_50':weights[:50]}
Path(__file__).with_name('weighted_envelope_screen.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

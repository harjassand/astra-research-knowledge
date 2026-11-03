import numpy as np,itertools,json
D='producer-workspace/chiral_hamiltonian_interface_20261102'
# All generic 4-vertex chambers modulo common phase shifts.
counts=set()
for bits in itertools.product([0,1],repeat=3):
 for ranks in itertools.permutations(range(1,4)):
  p=np.array([0]+[r/8+b/2 for r,b in zip(ranks,bits)])
  ns=[]
  for a,b,c in itertools.combinations(range(4),3):
   ns.append(round(p[c]-p[b])-round(p[c]-p[a])+round(p[b]-p[a]))
  counts.add(sum(x!=0 for x in ns))
print('all 48 tetra rotor chambers pierced-face counts',counts)
# Actual cubic geometry and endpoint configurations from previous test.
z=np.load(D+'cubic_move.npz',allow_pickle=True);T=[(tuple(t),int(s)) for t,s in z['T']]
records=[]
for label,p in [('a',z['phi_a']),('b',z['phi_b'])]:
 edges=sorted({e for t,s in T for e in itertools.combinations(t,2)});m={e:int(np.floor(p[e[1]]-p[e[0]]+.5)) for e in edges}
 n=lambda f:m[f[1],f[2]]-m[f[0],f[2]]+m[f[0],f[1]]
 q=sum(s*m[a,b]*n((b,c,d)) for (a,b,c,d),s in T)
 winding=0.;arcs=[]
 for t,s in T:
  flux=[]
  for i in range(4):
   face=t[:i]+t[i+1:];v=-s*(-1)**i*n(face) # Actual z vortex is -n.
   if v:flux.append((face,v))
  assert len(flux) in [0,2]
  if not flux:continue
  incoming=[f for f,v in flux if v==-1][0];outgoing=[f for f,v in flux if v==1][0]
  x=p[outgoing[0]]-p[incoming[0]];dx=x-np.floor(x+.5)
  winding+=dx;arcs.append({'tet':t,'in_face':incoming,'out_face':outgoing,'phase_turns':float(dx)})
 record={'endpoint':label,'selflink':int(q),'core_phase_winding':float(winding),'arcs':arcs};records.append(record)
 print(label,'s',q,'core winding',winding,'number arcs',len(arcs))
json.dump(records,open(D+'core_phase_rule_results.json','w'),indent=2)

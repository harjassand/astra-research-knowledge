"""Exact central-cube syndrome cleanup for flat §6 ell=8 blue doubling.
Six central faces: bottom, top, west, east, south, north.
Eight distinct exterior sheet faces, one beyond each horizontal cube edge.
Each allowed repetition-sheaf edge generator flips its two cube faces and
one exterior face. This script checks all 32 metacheck-admissible patterns.
Not a certificate for boundary gadgets or a complete RG decoder.
"""
import json
G=[]
for layer in range(2):
 for side in range(4):
  G.append((1<<layer)|(1<<(2+side))|(1<<(6+4*layer+side)))
rows=[]
for syndrome in range(64):
 if syndrome.bit_count()%2: continue
 candidates=[]
 for correction in range(256):
  image=0
  for j,g in enumerate(G):
   if correction>>j&1: image^=g
  if image&63==syndrome:
   candidates.append(((image>>6).bit_count(), correction.bit_count(),correction,image>>6))
 best=min(candidates)
 assert best[0]<=syndrome.bit_count()
 rows.append(dict(input=syndrome,input_weight=syndrome.bit_count(),output=best[3],output_weight=best[0],edge_correction=best[2]))
# Any arbitrary outside syndrome eta can only make the bound easier:
# |eta xor output| <= |eta| + |output| <= |eta| + |input|.
report=dict(scope='flat central cube only; not full recursive decoder',patterns=len(rows),generators=G,rows=rows,passed=True)
print(json.dumps(report,indent=2))

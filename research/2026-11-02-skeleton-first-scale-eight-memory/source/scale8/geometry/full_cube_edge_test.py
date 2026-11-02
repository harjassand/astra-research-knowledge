"""Test all 12 physical blue cube edges, not only constructive 8-edge subset.
Scope: central cube boundary plus first exterior incident faces. No collar
transport/correction generators are included. Hence the optimum is a local
edge-star optimum, not a global decoding lower bound.
"""
import json
G=[]
for layer in range(2):
 for side in range(4):
  G.append((1<<layer)|(1<<(2+side))|(1<<(6+4*layer+side)))
# Four sides indexed in cyclic order. Each vertical edge has four incident
# ribbon faces, two central and two different outward arms.
for side in range(4):
 G.append((1<<(2+side))|(1<<(2+(side+1)%4))|(1<<(14+2*side))|(1<<(15+2*side)))
mins={x:1000 for x in range(64) if x.bit_count()%2==0}
for correction in range(4096):
 image=0
 for j,g in enumerate(G):
  if correction>>j&1:image^=g
 syndrome=image&63
 mins[syndrome]=min(mins[syndrome],(image>>6).bit_count())
assert mins[60]==4
assert mins[63]==4
print(json.dumps(dict(scope=__doc__,generators=G,all_optima=mins,four_side_input_weight=4,four_side_min_output_weight=4,all_six_input_weight=6,all_six_min_output_weight=4),indent=2))

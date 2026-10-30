import itertools,json
# Exhaust all length-six event strings for 3-bit repetition checks.
H=(0b011,0b110); n=3; w=2; s=1; degree=2
syn=lambda e:sum(((e&h).bit_count()%2)<<j for j,h in enumerate(H))
S=lambda e:syn(e).bit_count()
traces=0
for e0 in range(8):
 stack=[(e0,e0,0,0,0)] # error, union support, faults, corrections, depth
 while stack:
  e,u,m,k,d=stack.pop(); traces+=1
  assert k<=S(e0)+degree*s*m
  assert u.bit_count()<=e0.bit_count()+s*m+w*(S(e0)+degree*s*m)
  if d==6:continue
  for f in range(1,8):
   if f.bit_count()<=w and S(e^f)<S(e):stack.append((e^f,u|f,m,k+1,d+1))
  for f in (1,2,4):stack.append((e^f,u|f,m+1,k,d+1))
# Disjoint writes are insufficient for serializability: stale reads increase energy.
H=(0b111,0b111,0b001,0b010)
e0=4; f=1; g=2
assert f&g==0 and S(e0^f)<S(e0) and S(e0^g)<S(e0)
assert S(e0^f^g)>S(e0)
print(json.dumps({'exhaustive_prefixes':traces,'depth':6,'work_budget':'PASS','stale_read_example':{'initial':e0,'disjoint_flips':[f,g],'syndrome_weights':[S(e0),S(e0^f),S(e0^g),S(e0^f^g)]}},indent=2))

import json
out=[]
for N in (4,8,16,32,64):
 edges=[(i,i+1) if i%2==0 else (i+1,i) for i in range(N-1)]
 def valid(h):return all(h[a]-h[b] in (0,1) for a,b in edges)
 base=[i//2 for i in range(N)]
 shifted=base.copy();shifted[0]+=1
 assert valid(base) and valid(shifted)
 results=[]
 for start in (base,shifted):
  h=start.copy();accepted=[]
  for i in range(1,N):
   proposal=h.copy();proposal[i]+=1
   if valid(proposal):h=proposal;accepted.append(i)
  results.append((h,accepted))
 assert not results[0][1] and results[1][1]==list(range(1,N))
 out.append({'N':N,'root_support':1,'valid_both_branches':True,'unshifted_accepted':0,'shifted_accepted':len(results[1][1]),'different_outside_event_vertices':N-1})
print(json.dumps({'fixture':'one valid local root and a fixed clean attempt sequence; fixed physical-time output frontiers differ at arbitrarily many outside sites','results':out},indent=2))

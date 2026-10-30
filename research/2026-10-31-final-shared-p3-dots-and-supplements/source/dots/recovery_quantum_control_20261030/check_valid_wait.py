import json
rows=[]
for m in (1,2,4,8,16,32):
 n=[m-(i+1)//2 for i in range(2*m+1)]
 edges=[(i,i+1) if i%2==0 else (i+1,i) for i in range(2*m)]
 def valid(n):return all(n[a]-n[b] in (0,1) for a,b in edges)
 def enabled(i):
  h=n.copy();h[i]+=1
  return valid(h)
 assert valid(n)
 # Construct the cut from clean flat initialization, stopping immediately before
 # the production at vertex 0. This establishes reachability, not probability.
 target=n.copy();target[0]-=1
 h=[0]*(2*m+1);steps=0
 while h!=target:
  for j in range(2*m+1):
   if h[j]<target[j]:
    hh=h.copy();hh[j]+=1
    if valid(hh):h=hh;steps+=1;break
  else:raise AssertionError("No enabled path to valid target")
 h[0]+=1;assert h==n
 actual=[]
 # Execute the exact mandatory backwards chain once. At each step all vertices
 # before the selected site are disabled, independently of extra later updates.
 for i in range(2*m,0,-1):
  assert all(not enabled(j) for j in range(i))
  assert enabled(i)
  n[i]+=1;actual.append(i)
 assert actual==list(range(2*m,0,-1))
 rows.append({'m':m,'vertices':2*m+1,'necessary_serial_completions_before_consumption':len(actual),'mean_delay_at_unit_ideal_rate':2*m,'clean_prefix_events_before_wire_production':steps})
print(json.dumps({'cases':rows,'scope':'Exact deterministic dependency checks; Erlang result is proved analytically, not Monte Carlo.'},indent=2))

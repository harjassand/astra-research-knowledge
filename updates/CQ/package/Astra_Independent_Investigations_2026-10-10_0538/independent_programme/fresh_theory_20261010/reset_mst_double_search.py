from reset_potential_search import *
import sys,time

def ph(S,d):return 2*mst(S,d)-len(S)+1

def main():
 rng=random.Random(20261012);out={'max_mst_ratio':0,'max_reset_ratio':0,'tested':0,'failures':[]};start=time.time()
 for n in range(3,11):
  for t in range(4000):
   A=[tuple(rng.randrange(n) for _ in range(n)) for _ in range(2)]
   d,words=pair_dist(A)
   if any(v is None for v in d.values()):continue
   out['tested']+=1;Q=tuple(range(n));p=ph(Q,d);w,_=reset_bfs(A)
   if mst(Q,d)>n*(n-1)//2 or len(w)>p:
    r={'n':n,'A':A,'mst':mst(Q,d),'reset_length':len(w),'reset_word':w,'pair_dist':{'%d,%d'%pair:v for pair,v in d.items()},'failure':'quadratic initial bound' if mst(Q,d)>n*(n-1)//2 else 'doubled MST reset bound'}
    out['failures'].append(r);print(json.dumps(r,indent=2),flush=True)
    json.dump(out,open('independent_programme/fresh_theory_20261010/reset_mst_double_results.json','w'),indent=2);return
   out['max_mst_ratio']=max(out['max_mst_ratio'],mst(Q,d)/(n*(n-1)/2))
   out['max_reset_ratio']=max(out['max_reset_ratio'],len(w)/p)
  print('passed',n,out['tested'],round(time.time()-start,1),flush=True)
 json.dump(out,open('independent_programme/fresh_theory_20261010/reset_mst_double_results.json','w'),indent=2)
if __name__=='__main__':main()

"""Seeded falsification of coordinatewise upward injections in union-closed families."""
import random,json,sys,time
from collections import deque

def closure(gens):
 f={0}
 for g in gens:
  f|={a|g for a in f}
 return sorted(f)

def matching(F,e,witness=False):
 L=[a for a in F if not a&e]; R=[b for b in F if b&e]
 adj=[[j for j,b in enumerate(R) if a|b==b] for a in L]
 rm=[-1]*len(R);lm=[-1]*len(L)
 def dfs(i,seen):
  for j in adj[i]:
   if j in seen:continue
   seen.add(j)
   if rm[j]<0 or dfs(rm[j],seen):
    rm[j]=i;lm[i]=j;return True
  return False
 for i in sorted(range(len(L)), key=lambda i:len(adj[i])):dfs(i,set())
 k=sum(x>=0 for x in lm)
 if not witness:return k,len(L)
 q=deque(i for i in range(len(L)) if lm[i]<0);visL=set(q);visR=set()
 while q:
  i=q.popleft()
  for j in adj[i]:
   if j in visR:continue
   visR.add(j)
   if rm[j]>=0 and rm[j] not in visL:
    visL.add(rm[j]);q.append(rm[j])
 return {'matched':k,'left_size':len(L),'right_size':len(R),'hall_L':[L[i] for i in sorted(visL)],'hall_N':[R[j] for j in sorted(visR)]}

def allfail(F,n):
 return all(matching(F,1<<i)[0]<matching(F,1<<i)[1] for i in range(n))

def main():
 rng=random.Random(20261010);start=time.time();count=0
 for n in range(3,13):
  for trial in range(3000):
   gens=rng.sample(range(1,1<<n),rng.randint(2,min(5*n,(1<<n)-1)))
   F=closure(gens);count+=1
   if allfail(F,n):
    result={'n':n,'family':F,'generators':gens,'trial':trial,'checked':count,'witnesses':[matching(F,1<<i,True) for i in range(n)]}
    print(json.dumps(result,indent=2),flush=True)
    json.dump(result,open('independent_programme/fresh_theory_20261010/counterexample_raw.json','w'),indent=2)
    return
  print('passed',n,count,'elapsed',round(time.time()-start,2),flush=True)
if __name__=='__main__':main()

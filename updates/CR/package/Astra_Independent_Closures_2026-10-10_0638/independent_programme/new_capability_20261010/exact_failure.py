from exact_verify import F,inv,mm,mv,tr,top,ROOT
from itertools import combinations
import json

def weighted(n,es,w,p):
 A=[[F((i==a)-(i==b))for a,b in es]for i in range(n-1)];AW=[[A[i][j]*w[j]for j in range(len(es))]for i in range(n-1)];K=mm(AW,tr(A));Z=inv(K);T=mm(tr(AW),mm(Z,A));f=mv(tr(AW),mv(Z,p[:-1]));return A,K,T,f

if __name__=='__main__':
 n=5;es=list(combinations(range(n),2));w=list(map(F,[5,1,10,1,10,50,2,50,5,50]));p=list(map(F,[3,3,3,0,-9]));A,K,T,f=weighted(n,es,w,p);m=len(es);d=[1-T[i][i]for i in range(m)];S=[4,5,7];v=[F(1),F(3),F(3)]
 # Width necessary condition: d_i h_i >= sum_{j in S-i}|T_ij|h_j.
 # This v proves its comparison operator expands every coordinate.
 slacks=[sum(abs(T[i][j])*v[b] for b,j in enumerate(S) if j!=i)-d[i]*v[a]for a,i in enumerate(S)]
 assert all(s>0 for s in slacks)
 i,j=S[:2];single=f[i]/d[i];pair=(d[j]*f[i]+T[i][j]*f[j])/(d[i]*d[j]-T[i][j]*T[j][i]);assert pair!=single
 caps=list(map(F,['31/10','31/10','6','91/10','9/2','8','91/10','7','91/10','91/10']))
 maxes=[F(0)]*m;count=0
 for kk in range(4):
  for SS in combinations(range(m),kk):
   KS=[[K[a][b]-sum(w[s]*A[a][s]*A[b][s]for s in SS)for b in range(n-1)]for a in range(n-1)]
   theta=mv(inv(KS),p[:-1]);ff=[w[e]*sum(A[a][e]*theta[a]for a in range(n-1))for e in range(m)];count+=1
   for e in range(m):
    if e not in SS:maxes[e]=max(maxes[e],abs(ff[e]));assert abs(ff[e])<caps[e]
 out={'graph':'complete K5 with positive integer edge weights','edges':es,'weights':list(map(str,w)),'injections':list(map(str,p)),'k':3,'caps':list(map(str,caps)),'all_exact_outage_cases_including_empty':count,'all_flows_strictly_below_caps':True,'minimum_exact_thermal_slack':str(min(caps[i]-maxes[i] for i in range(m))),'max_exact_flow_per_edge':list(map(str,maxes)),'comparison_triangle_edge_indices':S,'comparison_triangle_edges':[es[s]for s in S],'expanding_vector':list(map(str,v)),'strict_positive_expansion_slacks':list(map(str,slacks)),'incompatible_singleton_compensation':str(single),'incompatible_pair_compensation':str(pair),'compensation_difference':str(pair-single),'conclusion':'No finite common signed interval supersolution exists, although all modeled outages are safe at the supplied limits. This is exact row/sign relaxation loss, not a floating-point or iteration failure.'}
 (ROOT/'exact_intrinsic_failure.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

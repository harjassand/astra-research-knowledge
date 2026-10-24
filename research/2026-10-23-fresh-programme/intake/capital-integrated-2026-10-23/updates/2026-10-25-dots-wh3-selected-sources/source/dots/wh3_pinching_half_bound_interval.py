import mpmath as m,json
m.iv.dps=60;i=m.iv;e=i.mpf(1)/100
A=2*i.log((1+e)/e)
B=i.log((i.mpf(1)/2+e)/(i.mpf(1)/4+e))/2+3*i.log((i.mpf(1)/4+e)/e)/2
assert (B-A/2).a>0
r={'epsilon':'1/100','input_metric':str(A),'output_metric':str(B),'ratio':str(B/A),'half_bound_excess':str(B-A/2),'scope':'Strict BKM counterexample to physical-pinching half-contraction; not an entropy-conjecture counterexample.'}
print(json.dumps(r,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(r,indent=2)+'\n')

# Stronger faithful example with both marginals exactly uniform.
A2=6/(1-e)*i.log((6-5*e)/(3-2*e));B2=9/(3-e)
assert (B2-A2/2).a>0
r2={"epsilon":"1/100","input_metric":str(A2),"output_metric":str(B2),"ratio":str(B2/A2),"half_bound_excess":str(B2-A2/2),"both_marginals":"I3/3","scope":"Pinching-coherence proof counterexample only"}
open(__file__.replace(".py","_uniform.json"),"w").write(json.dumps(r2,indent=2)+"\n");print(json.dumps(r2,indent=2))

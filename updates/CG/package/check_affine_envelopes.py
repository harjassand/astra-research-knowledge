from fractions import Fraction
from math import comb
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent

def all_linear_subspaces(m):
    layers=[{frozenset([0])}]
    for d in range(m):
        nxt=set()
        for U in layers[-1]:
            for v in range(1<<m):
                if v not in U:nxt.add(U|frozenset(x^v for x in U))
        layers.append(nxt)
    return layers

def run():
    reports=[]
    for m in range(1,7):
        total=0;tight=0;linear=0
        for d,layer in enumerate(all_linear_subspaces(m)):
            linear+=len(layer)
            for U in layer:
                unseen=set(range(1<<m))
                while unseen:
                    v=min(unseen);L={x^v for x in U};unseen-=L
                    w=min(x.bit_count() for x in L)
                    assert w<=m-d
                    total+=1;tight+=w==m-d
        reports.append({'m':m,'linear_subspaces':linear,'affine_subspaces':total,'tight_minweight_bounds':tight,'all_minweight_bounds_verified':True})
    examples=[]
    for m in (8,16,32,64):
        for k in (0,m//4,m//2,m):
            K=2**k;Z=Fraction(3,2)**m;C=2**(m-k)*Fraction(3,2)**k
            assert C/Z==Fraction(4,3)**(m-k)
            assert C>=Fraction(2**m,K)
            examples.append({'m':m,'fixed_prefix':k,'pieces':K,'C':str(C),'Z':str(Z),'overhead':str(C/Z),'general_lower_bound':str(Fraction(4,3)**m/K)})
    # Coupled diagonal factors lambda_1, lambda_2, lambda_1+lambda_2.
    weights={(a,b):Fraction(1,2**(a+b+(a^b))) for a in range(2) for b in range(2)}
    Z=sum(weights.values());law={str(k):str(v/Z) for k,v in weights.items()}
    assert law=={'(0, 0)':'4/7','(0, 1)':'1/7','(1, 0)':'1/7','(1, 1)':'1/7'}
    # Exact finite bound for unrestricted positive mixtures of uniform affine distributions.
    mixture=[]
    for m,K in [(100,100),(250,62500),(500,250000)]:
        best=Fraction(0);bestdata=None
        # Search parameters with exact rational binomial tails, not a probabilistic simulation.
        for D in range(m//2,m):
            smallmass=K*Fraction(2,3)**(m-D)
            if smallmass>=1:continue
            for t in range(m//3,(D+1)//2):
                P=sum(Fraction(comb(m,w)*2**(m-w),3**m) for w in range(t+1))
                numerator=P-smallmass
                if numerator<=0:continue
                Q=Fraction(sum(comb(D+1,w) for w in range(t+1)),2**(D+1))
                bound=numerator/Q
                if bound>best:best=bound;bestdata=(D,t)
        mixture.append({'m':m,'K':K,'D':bestdata[0],'weight_threshold':bestdata[1],'exact_overhead_lower_bound':str(best),'float_for_display':float(best)})
    out={'all_checks_passed':True,'affine_exhaustion':reports,'coordinate_partition_examples':examples,'coupled_three_factor_law':law,'general_affine_mixture_bounds':mixture}
    (ROOT/'AFFINE_ENVELOPE_RESULTS.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({'affine_exhaustion':reports,'general_affine_mixture_bounds':[dict(m=x['m'],K=x['K'],D=x['D'],t=x['weight_threshold'],bound=x['float_for_display']) for x in mixture]},indent=2))
if __name__=='__main__':run()

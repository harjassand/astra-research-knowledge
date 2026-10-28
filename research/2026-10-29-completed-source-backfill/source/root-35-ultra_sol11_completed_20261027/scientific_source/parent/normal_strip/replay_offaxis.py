"""Independent exact consumer of the producer's two rational Newton proposals.

Uses root's independent input-polynomial code; never imports the producer.
Reconstructs coefficient corrections and their PSD proof from literal inputs.
"""
from certify import Q, OUT, SRC, mon, ae, add, sc, mul, sq, bs, zero, gp, ma, diagT, outer, liftT, ldl, serial, inputs
from pathlib import Path
from itertools import product
import hashlib,json,math,time
WAVE=OUT.parents[1]
ROOT=WAVE.parents[1]
def diff(p,i):
    o={}
    for e,c in p.items():
        if e[i]:
            f=list(e);f[i]-=1;o[tuple(f)]=c*e[i]
    return o
def value(p,a):return sum((c*math.prod(t**n for t,n in zip(a,e)) for e,c in p.items()),Q(0))
def translate(p,a):
    out={}
    for ex,c in p.items():
        for yy in product(*(range(n+1) for n in ex)):
            v=c*math.prod(math.comb(n,j)*a[i]**(n-j) for i,(n,j) in enumerate(zip(ex,yy)))
            out[yy]=out.get(yy,Q(0))+v
    return {ex:c for ex,c in out.items() if c}
def main():
    start=time.perf_counter();F,p,q,T=inputs();one={(0,0,0,0):Q(1)}
    k,e,sigma=Q(1,20000000),Q(199999,20000000),Q(1,34)
    H=add(F,sc(-k,sq(q)));ph=add(p,sc(-2*k,mul(q,sq(T))));D=sq(add(T,sc(sigma,one)))
    baseN=add(mul(D,add(sc(-3,H),sc(-e,T))),mul(ph,q))
    cof=[{mon((i,)):Q(s)} for i,s in [(3,1),(2,-1),(1,-1),(0,1)]]
    NB=[add(mul(D,add(diff(H,i),{mon((i,)):2*e})),sc(-1,mul(ph,cof[i]))) for i in range(4)]
    r=json.loads((WAVE/'smooth_conic_interface/LOCAL_EVALUATION.json').read_text())
    oldpath=ROOT/'work/sol8_opportunity_selection_20261027/rational_selector/EXACT_RATIONAL_SUPPORT.json'
    old=json.loads(oldpath.read_text());den=int(old['gram_denominator'])
    # Independently reconstruct the producer's baseline, using its declared
    # exact old principal block rather than root's stronger new GF block.
    gf=[[Q(old['gram_integer_matrix'][80+i][80+j],den) for j in range(10)] for i in range(10)]
    assert gp(gf,bs(2))==F
    gfh=ma((1,gf),(-k,outer(q,2)))
    raw35=json.loads((SRC/'EXACT35_LEADING_GRAM.json').read_text())
    g35=[[Q(v,int(raw35['gram_denominator'])) for v in row] for row in raw35['gram_numerators']]
    blocks=[ma((e*sigma*sigma,diagT(1))),ma((3*sigma*sigma,gfh),(2*e*sigma,diagT(2))),
            ma((6*sigma,liftT(gfh,2)),(e,diagT(3))),ma((1,g35),(-k,outer(mul(T,q),4)))]
    scales=list(map(Q,r['feature_scales_by_degree']));features=sum([bs(d) for d in range(1,5)],[])
    ds=[scales[sum(ex)-1] for ex in features];G=zero(69);offset=0
    for j,block in enumerate(blocks):
        ldl(block,scales[j]**2)
        for i,row in enumerate(block):
            for h,v in enumerate(row):G[offset+i][offset+h]=v
        offset+=len(block)
    assert gp(G,features)==sc(-1,baseN)
    pairs={}
    for i,ex in enumerate(features):
        for j in range(i,69):pairs.setdefault(ae(ex,features[j]),[]).append((i,j))
    for ex,ijs in list(pairs.items()):
        best=max(ds[i]*ds[j] for i,j in ijs);pairs[ex]=[(i,j) for i,j in ijs if ds[i]*ds[j]==best]
    rows=[]
    for example in r['examples']:
        zz=list(map(Q,example['query']));c=example['certificate'];a=list(map(Q,c['anchor']))
        N=add(baseN,*[sc(zz[i],NB[i]) for i in range(4)],sc(zz[4],ph))
        t0=value(N,a)/value(D,a);cleared=add(sc(t0,D),sc(-1,N));shift=translate(cleared,a)
        assert shift.get((0,0,0,0),Q(0))==0
        l=[shift.get(mon((i,)),Q(0))/2 for i in range(4)]
        assert l==list(map(Q,c['linear_residual']))
        target={ex:v for ex,v in shift.items() if sum(ex)>=2};baseline=sc(-1,baseN)
        g=[row[:] for row in G]
        for ex,ijs in pairs.items():
            corr=target.get(ex,Q(0))-baseline.get(ex,Q(0))
            for i,j in ijs:
                t=corr/(len(ijs)*(1 if i==j else 2));g[i][j]+=t
                if i!=j:g[j][i]+=t
        assert gp(g,features)==target
        rho=max(sum(abs(g[i][j]-G[i][j])/(ds[i]*ds[j]) for j in range(69)) for i in range(69))
        assert rho==Q(c['scaled_Gram_row_norm']) and rho<1
        b=(1-rho)*ds[0]**2/2;assert b==Q(c['b'])
        eta=2*sum(v*v for v in l)/(sigma*sigma*b);assert eta==Q(c['completion_eta'])
        # Literal square completion and the actual bound for D-sigma²/2.
        assert sum(v*v for v in a)<=sigma/4
        shiftD=translate(D,a)
        completed=add(target,sc(-b,T),sc(b,add(T,*[{mon((i,)):2*l[i]/b} for i in range(4)],sc(sum(v*v for v in l)/(b*b),one))),sc(eta,add(shiftD,sc(-sigma*sigma/2,one))))
        assert completed==add(shift,sc(eta,shiftD))
        off=k*sum(v*v for v in zz)
        assert t0+off==Q(c['lower']) and t0+off+eta==Q(c['upper'])
        assert Q(c['lower'])<=Q(c['upper'])
        rows.append({'query':example['query'],'lower':c['lower'],'upper':c['upper'],'width_display':float(eta),'row_bound_display':float(rho),'all_coefficients':'PASSED','square_completion':'PASSED','point_evaluation_dual':'PASSED','baseline_PSD_and_scaled_row_perturbation':'PASSED','reconstructed_Gram_sha256':hashlib.sha256(json.dumps(serial(g)).encode()).hexdigest()})
    result={'status':'INDEPENDENT_OFFAXIS_LITERAL_REPLAY_PASSED','examples':rows,'seconds':time.perf_counter()-start,'producer_receipt_sha256':hashlib.sha256((WAVE/'smooth_conic_interface/LOCAL_EVALUATION.json').read_bytes()).hexdigest(),'scope':'Two actual off-axis70-SOS query certificates. Independent literal polynomial translation, exact block LDL, coefficient correction, scaled row bound, square completion and dual lower. General open-box bounds and theorem are separate proof reviews.'}
    (OUT/'OFFAXIS_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'widths':[v['width_display'] for v in rows],'seconds':result['seconds']},indent=2))
if __name__=='__main__':main()

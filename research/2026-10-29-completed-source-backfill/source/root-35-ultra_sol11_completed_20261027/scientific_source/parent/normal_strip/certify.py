"""Exact normal-strip consumer. No producer code or scientific libraries."""
from fractions import Fraction as Q
from itertools import combinations_with_replacement as cwr
from pathlib import Path
import hashlib, json, math, time
OUT=Path(__file__).resolve().parent
SRC=OUT.parents[1]/'support_gram_compiler'
def mon(ii):return tuple(ii.count(i) for i in range(4))
def ae(e,f):return tuple(a+b for a,b in zip(e,f))
def add(*ps):
    o={}
    for p in ps:
        for e,c in p.items():o[e]=o.get(e,Q(0))+c
    return {e:c for e,c in o.items() if c}
def sc(c,p):return {e:c*v for e,v in p.items() if c*v}
def mul(p,r):
    o={}
    for e,c in p.items():
        for f,d in r.items():
            k=ae(e,f);o[k]=o.get(k,Q(0))+c*d
    return {e:c for e,c in o.items() if c}
def sq(p):return mul(p,p)
def bs(d):return [mon(ii) for ii in cwr(range(4),d)]
def zero(n):return [[Q(0) for _ in range(n)] for _ in range(n)]
def gp(g,b):
    o={}
    for i,e in enumerate(b):
        for j,f in enumerate(b):
            k=ae(e,f);o[k]=o.get(k,Q(0))+g[i][j]
    return {e:c for e,c in o.items() if c}
def ma(*cg):
    n=len(cg[0][1]);return [[sum((c*g[i][j] for c,g in cg),Q(0)) for j in range(n)] for i in range(n)]
def diagT(d):
    g=zero(len(bs(d)))
    for i,e in enumerate(bs(d)):g[i][i]=Q(math.factorial(d),math.prod(math.factorial(a) for a in e))
    return g
def outer(p,d):
    v=[p.get(e,Q(0)) for e in bs(d)];return [[a*b for b in v] for a in v]
def liftT(g,d):
    b,c=bs(d),bs(d+1);ix={e:i for i,e in enumerate(c)};o=zero(len(c))
    for k in range(4):
        ii=[ix[ae(e,mon((k,)))] for e in b]
        for i in range(len(b)):
            for j in range(len(b)):o[ii[i]][ii[j]]+=g[i][j]
    return o
def canonical(p,d):
    b=bs(d);pairs={};o=zero(len(b))
    for i,e in enumerate(b):
        for j in range(i,len(b)):pairs.setdefault(ae(e,b[j]),(i,j))
    for e,c in p.items():
        i,j=pairs[e]
        if i==j:o[i][j]+=c
        else:o[i][j]+=c/2;o[j][i]+=c/2
    assert gp(o,b)==p
    return o
def ldl(g,margin):
    n=len(g);l=zero(n);p=[]
    for i in range(n):
        t=g[i][i]-margin-sum((l[i][k]**2*p[k] for k in range(i)),Q(0));assert t>0,(i,t);p.append(t)
        for j in range(i+1,n):
            assert g[i][j]==g[j][i]
            l[j][i]=(g[j][i]-sum((l[j][k]*p[k]*l[i][k] for k in range(i)),Q(0)))/t
    return min(p)
def serial(g):return [[str(v) for v in row] for row in g]
def inputs():
    a,b,c,d=[{mon((i,)):Q(1)} for i in range(4)]
    u,v=add(sq(a),sq(c)),add(sq(b),sq(d));w=add(mul(a,b),mul(c,d));q=add(mul(a,d),sc(-1,mul(b,c)))
    T=add(u,v);x,y,z=add(u,sc(-1,v)),sc(2,w),sc(2,q)
    p0=Q(55220381,10**10);p2=Q(114430029,625000000)
    F=add(sc(p0,add(sq(u),sq(v))),sc(p2,mul(u,v)),sc(-Q(801761987,5000000000),sq(w)),sc(Q(118849817,4000000000),mul(q,x)))
    p=add(sc(Q(6222019,200000000),mul(sq(x),x)),sc(Q(1686519911,10**10),mul(sq(x),z)),sc(Q(81172813,2000000000),mul(x,sq(z))),sc(Q(1726116771,10**10),mul(sq(z),z)),sc(Q(128626163,5000000000),mul(x,sq(y))),sc(Q(373321239,2000000000),mul(sq(y),z)))
    return F,p,q,T
def main():
    start=time.perf_counter()
    F,p,q,T=inputs()
    p0=Q(55220381,10**10);p2=Q(114430029,625000000)
    k,e,sigma=Q(1,20000000),Q(1,100)-Q(1,20000000),Q(1,34)
    H=add(F,sc(-k,sq(q)));ph=add(p,sc(-2*k,mul(q,sq(T))))
    P=sum(map(abs,p.values()),Q(0));assert P==Q(1976430361,156250000)
    assert sum(map(abs,mul(q,sq(T)).values()),Q(0))==32
    Pbar=P+64*k;assert sum(map(abs,ph.values()),Q(0))<=Pbar
    width=e/(2*Pbar)
    r26=json.loads((SRC/'EXACT26_SUPPORT_GRAM.json').read_text());r35=json.loads((SRC/'EXACT35_LEADING_GRAM.json').read_text())
    g26=[[Q(v,int(r26['gram_denominator'])) for v in row] for row in r26['gram_numerators']]
    g35=[[Q(v,int(r35['gram_denominator'])) for v in row] for row in r35['gram_numerators']]
    assert [tuple(z) for z in r35['features']]==bs(4)
    assert [tuple(z)[4:] for z in r26['features'][16:]]==bs(2)
    gf=[row[16:] for row in g26[16:]]
    assert gp(gf,bs(2))==F
    assert gp(g35,bs(4))==add(sc(3,mul(sq(T),F)),sc(-1,mul(p,q)))
    gfh=ma((1,gf),(-k,outer(q,2)));g8=ma((1,g35),(-k,outer(mul(T,q),4)))
    assert sum(q.get(z,0)**2 for z in bs(2))==2
    assert sum(mul(T,q).get(z,0)**2 for z in bs(4))==8
    fF=Q(1,25000)-2*k;f8=Q(1,200000)-8*k
    ldl(gfh,fF);ldl(g8,f8)
    assert gp(gfh,bs(2))==H
    assert gp(g8,bs(4))==add(sc(3,mul(sq(T),H)),sc(-1,mul(ph,q)))
    gph=canonical(ph,3);rb=max(sum(map(abs,row),Q(0)) for row in gph);assert rb<=Pbar
    tgh=liftT(gfh,2);assert gp(tgh,bs(3))==mul(T,H)
    g4=ma((3*sigma*sigma,gfh),(2*e*sigma,diagT(2)))
    g2=ma((e*sigma*sigma,diagT(1)))
    g60=ma((6*sigma,tgh),(e,diagT(3)))
    floors=[e*sigma*sigma,2*e*sigma,e/2,f8];margin=Q(1,250000);assert min(floors)>margin
    D=sq(add(T,{(0,0,0,0):sigma}));rows=[];blocks={}
    for s in [-width,-Q(1,10000),Q(0),Q(1,10000),width]:
        g6=ma((1,g60),(-s,gph))
        poly=add(gp(g2,bs(1)),gp(g4,bs(2)),gp(g6,bs(3)),gp(g8,bs(4)))
        target=add(mul(D,add(sc(3,H),sc(e,T))),sc(-1,mul(ph,add(q,{(0,0,0,0):s}))))
        assert poly==target
        if abs(s)==width:ldl(g6,margin)
        lower=2*e*abs(s)+k*s*s;upper=lower+(2*p0+p2-k)*s*s
        rows.append({'s':str(s),'calibrated_exact_value':str(k*s*s),'all_support_15_lower':str(lower),'all_support_15_feasible_upper':str(upper),'literal_coefficients_checked':len(target)})
        if s==Q(1,10000):blocks={str(d):serial(g) for d,g in [(1,g2),(2,g4),(3,g6),(4,g8)]}
    cert={'schema':'calibrated_normal_strip_blocks_v1','basis':{str(d):bs(d) for d in range(1,5)},'query_s':'1/10000','blocks':blocks,'uniform69_Gram_margin':str(margin)}
    cp=OUT/'EXACT69_QUERY_BLOCKS.json';cp.write_text(json.dumps(cert,indent=2)+'\n')
    out={'status':'LITERAL_NORMAL_STRIP_CERTIFIED','kappa':str(k),'epsilon_original':'1/100','epsilon_compensated':str(e),'sigma':str(sigma),'p6_coefficient_l1':str(P),'pH_coefficient_bound':str(Pbar),'canonical_pH_Gram_row_bound':str(rb),'normal_halfwidth':str(width),'normal_halfwidth_decimal':float(width),'block_PD_margins':list(map(str,floors)),'uniform69_Gram_margin':str(margin),'queries':rows,'input_hashes':{n:hashlib.sha256((SRC/n).read_bytes()).hexdigest() for n in ['EXACT26_SUPPORT_GRAM.json','EXACT35_LEADING_GRAM.json']},'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'seconds_including_source_load_and_exact_LDL':time.perf_counter()-start,'scope':'Exact rational homogeneous-block construction; global calibrated operation is a separate theorem. No70 SDP acquisition, physical capability, novelty, or global smoothness claim.'}
    (OUT/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({z:out[z] for z in ['status','normal_halfwidth','normal_halfwidth_decimal','uniform69_Gram_margin','seconds_including_source_load_and_exact_LDL']},indent=2))
if __name__=='__main__':main()

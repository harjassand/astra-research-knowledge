"""Known operation blocks with physically executable reversed adjoints.
Extends the scalar certificate to nonsymmetric products. The reviewed
primitive compiler is kept unchanged, at its original reviewed hashes.
"""
from fractions import Fraction as F
from echo_compiler import (EchoCompiler, Interval, canonical, echo_word,
    bilinear_expr, add_expr, matvec, interval_expr, sqrt_upper)

class BlockEchoCompiler(EchoCompiler):
    def __init__(self,dictionary,blocks,records,maps,dual_maps):
        self.dictionary=[tuple(w) for w in dictionary]
        self.blocks=[tuple(w) for w in blocks]
        self.q,self.r=len(blocks),len(dictionary)
        self.records={canonical(w):v for w,v in records.items()}
        self.maps,self.dual_maps=maps,dual_maps
        if self.dictionary[0]!=():raise ValueError('Missing reset dictionary word')
        self.initial=[F(1)]+[F(0)]*(self.r-1)
        missing=self.required_block_words(dictionary,blocks)-self.records.keys()
        if missing:raise ValueError(f'Missing {len(missing)} block records')

    @staticmethod
    def required_block_words(dictionary,blocks):
        out=set()
        for a in dictionary:
            for b in dictionary:
                out.add(echo_word(a,(),b))
                for v in blocks:
                    v=tuple(v);rv=v[::-1]
                    for middle in [v,rv,v+rv,rv+v]:
                        out.add(echo_word(a,middle,b))
        return out

    def defect_expr(self,i,left,right):
        out=bilinear_expr(self.dictionary,left,self.blocks[i],right)
        return add_expr(out,bilinear_expr(self.dictionary,left,(),
                        matvec(self.maps[i],right)),F(-1))

    def residual_expr(self,i,left,right,dual=False):
        v=self.blocks[i][::-1] if dual else self.blocks[i]
        t=self.dual_maps[i] if dual else self.maps[i]
        tl,tr=matvec(t,left),matvec(t,right)
        out=bilinear_expr(self.dictionary,left,v+v[::-1],right)
        add_expr(out,bilinear_expr(self.dictionary,left,v[::-1],tr),F(-1))
        add_expr(out,bilinear_expr(self.dictionary,tl,v,right),F(-1))
        add_expr(out,bilinear_expr(self.dictionary,tl,(),tr))
        return out

    def certificate(self,word,sqrt_bits=72):
        w=tuple(word);h=len(w)
        f=[self.initial]
        for i in w:f.append(matvec(self.maps[i],f[-1]))
        b=[None]*(h+1);b[h]=self.initial
        for s in range(h-1,-1,-1):b[s]=matvec(self.dual_maps[w[s]],b[s+1])
        expr=bilinear_expr(self.dictionary,self.initial,(),f[h])
        uncorrected=interval_expr(expr,self.records)
        a,d=[],[]
        for s,i in enumerate(w):
            add_expr(expr,self.defect_expr(i,b[s+1],f[s]))
            af=interval_expr(self.residual_expr(i,f[s],f[s]),self.records)
            ab=interval_expr(self.residual_expr(i,b[s+1],b[s+1],dual=True),self.records)
            a.append(sqrt_upper(af.hi,sqrt_bits));d.append(sqrt_upper(ab.hi,sqrt_bits))
        point=interval_expr(expr,self.records)
        rem,acc=F(0),F(0)
        for x,y in zip(a,d):rem+=acc*y;acc+=x
        cap=self.records[()].hi
        return {'interval':Interval(max(-cap,point.lo-rem),min(cap,point.hi+rem)),
                'corrected_prediction':point,'uncorrected_prediction':uncorrected,
                'remainder':rem,'native_length':sum(len(self.blocks[i]) for i in w),
                'native_coefficient_l1':sum(map(abs,expr.values()),F(0))}

def propose_block_maps(dictionary,blocks,records,quantum=10**10):
    import numpy as np
    g=np.array([[float(records[echo_word(a,(),b)].center) for b in dictionary]
                for a in dictionary])
    forward,dual=[],[]
    for block in blocks:
        for target,v in [(forward,block),(dual,tuple(block)[::-1])]:
            m=np.array([[float(records[echo_word(a,v,b)].center) for b in dictionary]
                        for a in dictionary])
            t=np.linalg.solve(g,m)
            target.append([[F(int(round(float(x)*quantum)),quantum) for x in row]
                           for row in t])
    return forward,dual

def uniform_block_certificate(compiler,rho=F(7,10),metric=None):
    from uniform_certificate import (psd,sub,scale,mm,transpose,dominate,diagonal)
    from echo_compiler import dot
    w=metric if metric is not None else compiler.gram_centers()
    if not psd(w,strict=True):raise ValueError('Computational metric not SPD')
    if not 0<=rho<1:raise ValueError('Invalid contraction factor')
    for t in compiler.maps+compiler.dual_maps:
        if not psd(sub(scale(w,rho*rho),mm(transpose(t),mm(w,t)))):
            raise ValueError('Forward/adjoint block contraction check failed')
    r=compiler.r
    eye=[[F(int(j==k)) for k in range(r)] for j in range(r)]
    eps,uppers=[],[]
    for dual in [False,True]:
        for i in range(compiler.q):
            a=[[interval_expr(compiler.residual_expr(i,x,y,dual),compiler.records)
                for y in eye] for x in eye]
            radii=[sum((z.radius for z in row),F(0)) for row in a]
            upper=[[a[j][k].center+(radii[j] if j==k else 0)
                    for k in range(r)] for j in range(r)]
            uppers.append(upper);eps.append(dominate(w,upper))
    def noise(middle):
        a=[[compiler.records[echo_word(x,middle,y)].radius
            for y in compiler.dictionary] for x in compiler.dictionary]
        rows=[sum(row,F(0)) for row in a]
        cols=[sum((a[j][k] for j in range(r)),F(0)) for k in range(r)]
        return dominate(w,diagonal([max(x,y) for x,y in zip(rows,cols)]))
    gg=noise(())
    gm=max(noise(v) for v in compiler.blocks)
    eps2=max(eps)
    cn=dot(compiler.initial,matvec(w,compiler.initial))
    res=cn*eps2/(1-rho)**2
    meas=cn*(gg+(gm+rho*gg)/(1-rho))
    return {'rho':rho,'metric':w,'residual_uppers':uppers,'eps2':eps2,
            'per_map_eps2':eps,'gamma_g':gg,'gamma_m':gm,
            'initial_metric_norm_squared':cn,'all_word_residual_bound':res,
            'all_word_measurement_bound':meas,'all_word_total_bound':res+meas,
            'exact_psd_checks_passed':True}

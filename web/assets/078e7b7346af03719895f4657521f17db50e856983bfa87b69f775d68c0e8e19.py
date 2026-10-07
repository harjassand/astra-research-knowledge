"""Exact cut-rank sampler for canonical coordinate-source vector-pair systems.

Each colored line is (e_source, vector), with a nonnegative rational activity.
Original hard-BCS lines and arbitrary coordinate-pair additions are covered.
Site blocks contain one row mode per source color plus one common column mode;
local occupancy permits at most one mode. Transfers skip all site modes as a
block, so no uncharged within-site rank blowup is hidden.
"""
from rank_frontier_sampler import rref,linear,wedge,add,scale,parity,ZERO,ONE,clean
from pathlib import Path
from fractions import Fraction
import sys,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from frontier_sampler import qr,ga,gm,gc,gs

class ColorRankParity:
    def __init__(self,lines,n):
        # line entries: (source, vector length n, activity)
        self.n=n;self.lines=[(int(i),list(map(qr,v)),Fraction(a)) for i,v,a in lines]
        if any(i<0 or i>=n or len(v)!=n or a<0 for i,v,a in self.lines):raise ValueError('bad canonical line')
        self.local_rows=[[] for _ in range(n)];self.mode_line={};self.mode_site={};self.col_modes=[];self.cuts=[0]
        p=0
        for i in range(n):
            for line_id,(source,v,a) in enumerate(self.lines):
                if source==i:
                    self.local_rows[i].append((p,line_id));self.mode_line[p]=line_id;self.mode_site[p]=i;p+=1
            self.col_modes.append(p);self.mode_site[p]=i;p+=1;self.cuts.append(p)
        self.m=p;K=[[ZERO for _ in range(p)] for _ in range(p)]
        for mode,line_id in self.mode_line.items():
            source,v,a=self.lines[line_id]
            for j,c in enumerate(v):
                col=self.col_modes[j];K[mode][col]=c;K[col][mode]=gs(c,-1)
        self.K=K;self.bases=[];self.pivots=[]
        for p in self.cuts:
            B,cols=rref([row[p:] for row in K[:p]],self.m-p)
            self.bases.append(B);self.pivots.append(cols)
        self.ranks=list(map(len,self.bases));self.tensors=[]
        for i in range(n):
            left,right=self.cuts[i:i+2];site_modes=right-left
            B=self.bases[i];C=self.bases[i+1];pivs=self.pivots[i+1]
            T=[[row[site_modes+j] for j in pivs] for row in B]
            beta=[[row[s] for s in range(site_modes)] for row in B]
            ell=[[K[left+s][right+j] for j in pivs] for s in range(site_modes)]
            # New row span includes old tail forms and every current-site
            # future edge form. Verify coordinates exactly.
            for row,coords in [(row[site_modes:],T[a]) for a,row in enumerate(B)]+[(K[left+s][right:],ell[s]) for s in range(site_modes)]:
                rr=[]
                for j in range(self.m-right):
                    z=ZERO
                    for x,b in zip(coords,C):z=ga(z,gm(x,b[j]))
                    rr.append(z)
                if rr!=row:raise AssertionError('block cross-form reconstruction')
            tensors={'empty':[]}
            for s in range(site_modes):tensors[s]=[]
            for mask in range(1<<len(B)):
                p0={0:ONE};p1=[{} for _ in range(site_modes)];old_degree=0
                for a in range(len(B)):
                    if not(mask>>a&1):continue
                    tpoly=linear(T[a])
                    p1=[add(wedge(p1[s],tpoly),scale(p0,gs(beta[a][s],-1 if old_degree%2 else 1))) for s in range(site_modes)]
                    p0=wedge(p0,tpoly);old_degree+=1
                tensors['empty'].append(p0)
                for s in range(site_modes):tensors[s].append(add(p1[s],wedge(parity(p0),linear(ell[s]))))
            self.tensors.append(tensors)
        self.stats={}

    def local_options(self,i):
        left=self.cuts[i]
        options=[('empty',Fraction(1),0,None),(self.col_modes[i]-left,Fraction(1),0,None)]
        options += [(mode-left,self.lines[line_id][2],1,line_id) for mode,line_id in self.local_rows[i]]
        return options

    def partition(self,k,allowed=None):
        if k<0 or 2*k>self.n:return Fraction(0)
        allowed={} if allowed is None else allowed
        current={(0,0,0):ONE};peak=1;steps=0
        for i in range(self.n):
            nxt={}
            for (a,b,q),v in current.items():
                for label,weight,increment,line_id in self.local_options(i):
                    if label not in allowed.get(i,tuple(self.tensors[i])):continue
                    qq=q+increment
                    if qq>k:continue
                    for aa,c in self.tensors[i][label][a].items():
                        for bb,d in self.tensors[i][label][b].items():
                            key=(aa,bb,qq);term=gs(gm(v,gm(c,gc(d))),weight)
                            nxt[key]=ga(nxt.get(key,ZERO),term);steps+=1
            current=clean(nxt);peak=max(peak,len(current))
        ans=current.get((0,0,k),ZERO)
        if ans[1] or ans[0]<0:raise ArithmeticError(ans)
        self.stats={'modes':self.m,'lines':len(self.lines),'max_site_cross_rank':max(self.ranks,default=0),'peak_states':peak,'norm_transitions':steps}
        return ans[0]

    def sample(self,k,rng=None,max_bit_trials=None):
        rng=random.SystemRandom() if rng is None else rng
        fixed={};total=self.partition(k)
        if not total:raise ValueError('zero sector')
        labels=[];selected_lines=[];column_sites=[];fallback=0;bits=0
        from math import lcm
        for i in range(self.n):
            options=[]
            for label,activity,increment,line_id in self.local_options(i):
                child={**fixed,i:(label,)};mass=self.partition(k,child)
                options.append((label,line_id,mass))
            if sum(z for label,line_id,z in options)!=total:raise AssertionError('prefix mass')
            den=1
            for label,line_id,z in options:den=lcm(den,z.denominator)
            mass=int(total*den)
            if max_bit_trials is None:draw=rng.randrange(mass)
            else:
                if max_bit_trials<1:raise ValueError('positive bit cap required')
                nb=(mass-1).bit_length();draw=None
                for _ in range(max_bit_trials):
                    candidate=rng.getrandbits(nb);bits+=nb
                    if candidate<mass:draw=candidate;break
                if draw is None:draw=0;fallback+=1
            for label,line_id,z in options:
                weight=int(z*den)
                if draw<weight:break
                draw-=weight
            labels.append(label);fixed[i]=(label,);total=z
            if line_id is not None:selected_lines.append(line_id)
            elif label!='empty':column_sites.append(i)
        return {'local_labels':tuple(labels),'selected_lines':tuple(selected_lines),'J':tuple(column_sites),'fallback_events':fallback,'charged_random_bits':bits if max_bit_trials is not None else 'UNKNOWN'}

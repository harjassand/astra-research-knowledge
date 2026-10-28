"""Finite internal-relative-time source, complete time-ordered contractions.

B_delta/i=(S+(delta)S-(0)-S-(delta)S+(0))/2. Global time averaging leaves
one relative-center integral. All intermediate magnetization sectors and
ladder transitions are retained. Numerical Gauss preview, not validation.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','1')
from pathlib import Path
import sys,time,json,functools,itertools,hashlib
import numpy as np
import scipy.linalg as la
import scipy.sparse as ss
from numpy.polynomial.legendre import leggauss

ROOT=Path(__file__).resolve().parents[1];WORK=ROOT.parents[1]
OLD=WORK/'sol10_constructive_frontier_20261028/thermal_spin_projection'
sys.path.insert(0,str(OLD/'code'))
from angular_spin_projection import sector_parts
from projected_fugacity_preview import all_mode_count
from contact_jet_preview import analyze,boundary_bond

class Physical:
    def __init__(self,n,beta=3.,edges=None):
        self.n=n;self.beta=beta;self.edges=edges;self.sectors={};self.opcache={};self.trace_calls=0
        for mag in range(-2*n,2*n+1):
            states,parts=sector_parts(n,mag)
            if not states:continue
            d0,d1,_,_=parts;l=np.array([w[0]for w in states]);r=np.array([w[-1]for w in states])
            if edges is None:
                h=(d0+np.sqrt(6)*d1).toarray();h[np.diag_indices_from(h)]-=l*r;h*=beta
            else:
                assert len(edges)==n-1
                h=sum(c*boundary_bond(states,k)for k,c in enumerate(edges)).toarray()
            e,u=la.eigh(h,check_finite=False,overwrite_a=True)
            self.sectors[mag]=(states,{w:i for i,w in enumerate(states)},e,u)
        assert sum(len(x[0])for x in self.sectors.values())==5**n
    def operator(self,side,step,mag):
        key=(side,step,mag)
        if key in self.opcache:return self.opcache[key]
        target=mag+step
        if mag not in self.sectors or target not in self.sectors:
            self.opcache[key]=None;return None
        source=self.sectors[mag];dest=self.sectors[target]
        site=0 if side=='L'else self.n-1
        if step==0:out=dest[3].T@(np.array([w[site]for w in source[0]])[:,None]*source[3])
        else:
            rows=[];cols=[];vals=[]
            for col,w in enumerate(source[0]):
                m=w[site]
                if -2<=m+step<=2:
                    v=list(w);v[site]+=step
                    rows.append(dest[1][tuple(v)]);cols.append(col);vals.append(np.sqrt(6-m*(m+step)))
            raw=ss.csr_matrix((vals,(rows,cols)),shape=(len(dest[0]),len(source[0])))
            out=dest[3].T@(raw@source[3])
        self.opcache[key]=out;return out
    def event_trace(self,events):
        events=sorted(events,key=lambda x:x[0]);assert abs(events[0][0])<1e-12
        self.trace_calls+=1;answer=0.
        for mag,(_,_,e0,_)in self.sectors.items():
            current=mag;product=None;valid=True
            for index,(t,side,step)in enumerate(events):
                op=self.operator(side,step,current)
                if op is None:valid=False;break
                current+=step
                product=op if product is None else op@product
                nexttime=events[index+1][0]if index+1<len(events)else 1.
                if nexttime>t:product=np.exp(-(nexttime-t)*self.sectors[current][2])[:,None]*product
            if valid:
                assert current==mag
                answer+=float(np.trace(product))
        return answer
    def source_trace(self,left,right,tau):
        def terms(side,delta,offset):
            if delta is None:return [(1.,[(offset,side,0)])]
            return [(sign/2,[(offset,side,-sign),((offset+delta)%1,side,sign)])for sign in (-1,1)]
        return sum(a*b*self.event_trace(e+f)for a,e in terms('L',left,0.)for b,f in terms('R',right,tau))
    def source_integral(self,left,right,degree):
        breaks={0.,1.}
        if left is not None:breaks.add(left)
        if right is not None:
            breaks.add(1-right)
            if left is not None:breaks.add((left-right)%1)
        breaks=sorted(breaks);xs,ws=leggauss(degree);out=0.
        for a,b in zip(breaks,breaks[1:]):
            for x,w in zip(xs,ws):out+=(b-a)/2*w*self.source_trace(left,right,(a+b)/2+(b-a)/2*x)
        return out,len(breaks)-1

def main():
    start=time.monotonic();deltas=(.125,.25);messages=[(None,0),(None,1),(.125,0),(.25,0)]
    uniform=json.loads((ROOT/'results/contact_jet_trace_preview.json').read_text())
    control={r['n']:r for r in uniform};values={};report=[];physical={}
    def value(n,left,right):
        if left is None and right is None:
            return control[n]['C'][0][0],control[n]['equal_time_C'][0][0]
        key=(n,left,right)
        if key in values:return values[key]
        model=physical.setdefault(n,None)
        if model is None:model=physical[n]=Physical(n)
        before=model.trace_calls
        v8,pieces=model.source_integral(left,right,8)
        v16,_=model.source_integral(left,right,16)
        equal=model.source_trace(left,right,0.)
        diff=abs(v16-v8)/max(1.,abs(v16))
        row={'n':n,'left_delta':left,'right_delta':right,'C_projected_degree8':v8,
             'C_projected_degree16':v16,'C_equal_time':equal,'quadrature_pieces':pieces,
             'degree8_vs16_relative_difference':diff,'time_ordered_trace_calls':model.trace_calls-before}
        assert diff<5e-8,row
        report.append(row);values[key]=(v16,equal)
        print('CORRELATION',row,'seconds',time.monotonic()-start,flush=True)
        (ROOT/'results/bilocal_time_source_inputs.json').write_text(json.dumps(report,indent=2)+'\n')
        return values[key]
    matrices=[[],[]]
    for shift in range(3):
        mats=[np.zeros((4,4))for _ in range(2)]
        for i,(left,d)in enumerate(messages):
            for j,(right,e)in enumerate(messages[:i+1]):
                p=d+e+shift
                # Reflect endpoints so a sole bilocal is always the right source.
                a,b=(left,right)if left is None or right is not None else(right,left)
                v=value(p+2,a,b)
                for channel in range(2):mats[channel][i,j]=mats[channel][j,i]=(-1)**(p+1)*v[channel]/5**p
        for channel in range(2):matrices[channel].append(mats[channel])
    source=json.loads((OLD/'results/spin_projection_preview.json').read_text())
    source=next(x for x in source['rows']if x['beta']==3 and x['angle_samples']==64)
    a5=json.loads((WORK/'sol9_frontier_20261028/thermal/results/a5_preview.json').read_text())
    a5=next(x for x in a5['rows']if x['beta']==3)
    rows=[]
    for channel,name in enumerate(('P0_projected','matched_unprojected')):
        for size in (2,3,4):
            rows.append(analyze([m[:size,:size]for m in matrices[channel]],source,a5,f'{name}_rank{size}'))
    controls=[]
    model=physical[2]
    for left,right in ((None,None),(None,.5),(None,.875),(.125,.25),(.25,.125)):
        v16,_=model.source_integral(left,right,16)
        controls.append({'n':2,'left_delta':left,'right_delta':right,'integral':v16})
    assert abs(controls[0]['integral']/control[2]['C'][0][0]-1)<2e-12
    assert abs(controls[1]['integral']/control[2]['C'][0][0])<2e-12
    assert abs((controls[2]['integral']+values[(2,None,.125)][0])/control[2]['C'][0][0])<2e-12
    assert abs((controls[3]['integral']-controls[4]['integral'])/max(1.,abs(controls[3]['integral'])))<2e-12
    result={'status':'FINITE_INTERNAL_TIME_BILOCAL_SPIN1_NUMERICAL_PREVIEW','beta':3.,
      'messages':messages,'rows':rows,'controls':controls,'distinct_new_time_integrals':len(values),
      'physical_source_sizes':sorted(physical),'all_physical_states_per_size':{n:5**n for n in physical},
      'time_ordered_trace_calls':sum(x.trace_calls for x in physical.values()),
      'source_operator_cache_entries':sum(len(x.opcache)for x in physical.values()),
      'seconds':time.monotonic()-start,'new_validated_source_acquisition':False,
      'scope':'Finite δ raw bilocal messages, two Gauss degrees, all signed-M/intermediate ladder sectors. Not certified source/roundoff/quadrature enclosures; scalar reference unchanged.'}
    np.savez(ROOT/'results/bilocal_time_matrices.npz',G0=matrices[0][0],H0=matrices[0][1],M20=matrices[0][2],
             G1=matrices[1][0],H1=matrices[1][1],M21=matrices[1][2])
    (ROOT/'results/bilocal_time_preview.json').write_text(json.dumps(result,indent=2)+'\n')
    for row in rows:print('SUMMARY',row['name'],row['rows'][0],flush=True)

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Exact fixed-N conditional photon-affinity reader. No timestamps or floats.
Source/readout/IID/coding/precommitment contracts remain supplied, not inferred.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import hashlib,json
from math import isqrt
from pathlib import Path
import sys
SCHEMA='conditional-photon-affinity-v1'
COORDS=('ReM1','ImM1','ReM2','ImM2','W11','W22','ReW12','ImW12')
RANGES=(2,2,2,2,1,1,2,2)
GOVERNING={'photon_confidence_sha256':'25bfdb4e5ccab5499fe568491d1a5d2f77c833e2623ec7c355dfd35be49d15ba','spectral_affinity_sha256':'8334d1121be4d34b28492d9789daa7e4654f448ac3f5aae1bd197c776efd5e18'}
class InputError(ValueError):pass

def require(ok,message):
    if not ok:raise InputError(message)

def rational(v,path):
    require(type(v) in (int,str),f'{path}: integer or rational string required, no floats/bools')
    try:return F(v)
    except (ValueError,ZeroDivisionError,OverflowError):raise InputError(f'{path}: invalid finite rational') from None

def integer(v,path,minimum=0):
    require(type(v) is int and v>=minimum,f'{path}: integer >={minimum} required')
    return v

def text(v,path):
    require(isinstance(v,str) and bool(v.strip()),f'{path}: nonempty reference/text required')
    return v

def exact_keys(d,keys,path):
    require(isinstance(d,dict),f'{path}: object required')
    require(set(d)==set(keys),f'{path}: fields must be exactly {sorted(keys)}')

def parse_json(raw,path):
    def pairs(items):
        out={}
        for key,value in items:
            require(key not in out,f'{path}: duplicate key {key!r}');out[key]=value
        return out
    def no_float(s):raise InputError(f'{path}: floating/nonfinite JSON number forbidden ({s})')
    try:
        if isinstance(raw,bytes):raw=raw.decode('utf-8')
        require(bool(raw.strip()),f'{path}: blank line is not a record')
        return json.loads(raw,object_pairs_hook=pairs,parse_float=no_float,parse_constant=no_float)
    except InputError:raise
    except (UnicodeError,ValueError) as e:raise InputError(f'{path}: invalid UTF-8 JSON: {e}') from None

def parse_header(d):
    exact_keys(d,('schema','kind','data_kind','N','cutoffs','lambda_on','lambda_dark','alpha_stat','alpha_other_total','budget_scope','eta','analysis','contract_ref','sqrt_bits'),'header')
    require(d['schema']==SCHEMA,'unsupported header schema');require(d['kind']=='header','first record must be header')
    require(d['data_kind'] in ('SUPPLIED_RECORD_STREAM','NONPHYSICAL_SOFTWARE_TEST'),'unsupported data_kind')
    n=integer(d['N'],'header.N',2)
    require(isinstance(d['cutoffs'],list) and len(d['cutoffs'])==2,'cutoffs: two required')
    ks=[integer(v,f'cutoffs[{i}]',1) for i,v in enumerate(d['cutoffs'])];caps=[]
    for key in ('lambda_on','lambda_dark'):
        require(isinstance(d[key],list) and len(d[key])==2,f'{key}: two required')
        row=[rational(v,f'{key}[{i}]') for i,v in enumerate(d[key])];require(all(v>=0 for v in row),f'{key}: negative cap');caps.append(row)
    alpha=rational(d['alpha_stat'],'alpha_stat');require(0<alpha<1,'require0<alpha_stat<1')
    require(d['budget_scope']=='TOTAL_DATASET','budget_scope must be TOTAL_DATASET')
    require(isinstance(d['alpha_other_total'],dict),'alpha_other_total: named TOTAL-dataset budgets required')
    other={text(k,'budget name'):rational(v,'alpha_other_total.'+k) for k,v in d['alpha_other_total'].items()}
    require(all(v>=0 for v in other.values()),'negative other budget');require(alpha+sum(other.values())<1,'total failure budget must be<1')
    eta=rational(d['eta'],'eta');require(eta>=0,'negative eta')
    exact_keys(d['analysis'],('frequency_cycles_per_time','time_unit','common_gate_ref','capture_ref','phasor_coder_ref','precommitment_ref'),'analysis')
    analysis=dict(d['analysis']);freq=rational(analysis['frequency_cycles_per_time'],'frequency_cycles_per_time');require(freq>=0,'negative frequency');analysis['frequency_cycles_per_time']=str(freq)
    for key in analysis:
        if key!='frequency_cycles_per_time':text(analysis[key],'analysis.'+key)
    return {'schema':SCHEMA,'kind':'header','data_kind':d['data_kind'],'N':n,'cutoffs':ks,'lambda_on':list(map(str,caps[0])),'lambda_dark':list(map(str,caps[1])),'alpha_stat':str(alpha),'alpha_other_total':{k:str(v) for k,v in other.items()},'budget_scope':'TOTAL_DATASET','eta':str(eta),'analysis':analysis,'contract_ref':text(d['contract_ref'],'contract_ref'),'sqrt_bits':integer(d['sqrt_bits'],'sqrt_bits',1)}

# Rational complex arithmetic, never Python complex binary floats.
def cadd(a,b):return (a[0]+b[0],a[1]+b[1])
def csub(a,b):return (a[0]-b[0],a[1]-b[1])
def cmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
def cscale(a,s):return (a[0]*s,a[1]*s)
def norm2(a):return a[0]**2+a[1]**2
def l1(a):return abs(a[0])+abs(a[1])

def record(d,path):
    exact_keys(d,('count','phasors'),path);count=integer(d['count'],path+'.count')
    require(isinstance(d['phasors'],list) and len(d['phasors'])==count,path+': count/phasor-length mismatch')
    total=(F(0),F(0))
    for j,pair in enumerate(d['phasors']):
        require(isinstance(pair,list) and len(pair)==2,f'{path}.phasors[{j}]: [re,im] required')
        z=(rational(pair[0],path+'.re'),rational(pair[1],path+'.im'));require(norm2(z)<=1,f'{path}.phasors[{j}]: norm>1');total=cadd(total,z)
    return count,total

def block(d,index,ks):
    exact_keys(d,('kind','index','bright_a','bright_b','dark'),f'block[{index}]');require(d['kind']=='block','block kind required');require(type(d['index']) is int and d['index']==index,'indices must be consecutive from0')
    counts=[];ys=[]
    for key in ('bright_a','bright_b','dark'):
        require(isinstance(d[key],list) and len(d[key])==2,f'{key}: exactly two channels required')
        pairs=[record(rec,f'block[{index}].{key}[{i}]') for i,rec in enumerate(d[key])];counts.append([p[0] for p in pairs]);ys.append([p[1] for p in pairs])
    totals=[sum(row[i] for row in counts) for i in range(2)];cut=any(totals[i]>ks[i] for i in range(2))
    if cut:return [F(0)]*8,counts,totals,True
    delta=[csub(ys[0][i],ys[1][i]) for i in range(2)]
    means=[cscale(csub(cscale(cadd(ys[0][i],ys[1][i]),F(1,2)),ys[2][i]),F(1,ks[i])) for i in range(2)]
    off=cscale(cmul(delta[0],conj(delta[1])),F(1,ks[0]*ks[1]))
    f=[*means[0],*means[1],norm2(delta[0])/ks[0]**2,norm2(delta[1])/ks[1]**2,*off]
    require(all(0<=f[j]<=1 if j in (4,5) else -1<=f[j]<=1 for j in range(8)),'internal bounded-feature identity failed')
    return f,counts,totals,False

def sqrt_bounds(x,bits):
    """Rational enclosure on a relative dyadic grid, verified by squaring."""
    x=F(x);require(x>=0,'negative sqrt argument')
    if not x:return F(0),F(0)
    e=(x.numerator.bit_length()-x.denominator.bit_length())//2-bits
    if e>=0:step=F(1<<e);a=x.numerator;b=x.denominator*(1<<(2*e))
    else:step=F(1,1<<(-e));a=x.numerator*(1<<(-2*e));b=x.denominator
    k=isqrt(a//b);lo=k*step;hi=lo if k*k*b==a else (k+1)*step
    if not (0<lo<=hi and lo*lo<=x<=hi*hi):raise ArithmeticError('sqrt enclosure failed')
    return lo,hi

def log_upper(x):
    """Natural log(x)<=ceil(log2 x), since e>2. Exact integer comparisons."""
    x=F(x);require(x>=1,'log bound requires x>=1');h=max(0,x.numerator.bit_length()-x.denominator.bit_length())
    while (1<<h)*x.denominator<x.numerator:h+=1
    while h and (1<<(h-1))*x.denominator>=x.numerator:h-=1
    return F(h)

def poisson_tails(ell,K):
    """Upper tails at K+1,K,K-1. Fixed Taylor degree J=K+1."""
    ell=F(ell);terms=[F(1)]
    for j in range(1,K+2):terms.append(terms[-1]*ell/j)
    lower_exp=sum(terms);ans={}
    for k in (K+1,K,K-1):
        if k<=0:v=F(1)
        elif not ell:v=F(0)
        elif k<=ell:v=F(1)
        else:v=min(F(1),terms[k]/((1-ell/F(k+1))*lower_exp))
        ans[k]=v
    return ans,lower_exp

def bias_bounds(h):
    ks=h['cutoffs'];on=list(map(F,h['lambda_on']));dark=list(map(F,h['lambda_dark']));ell=[2*on[i]+dark[i] for i in range(2)];ts=[];receipts=[]
    for i in range(2):
        tails,explo=poisson_tails(ell[i],ks[i]);k=ks[i];p0=tails[k+1];p1=ell[i]*tails[k];p2=ell[i]**2*tails[k-1]+ell[i]*tails[k];ts.append((p0,p1,p2))
        receipts.append({'ell':str(ell[i]),'K':k,'exp_taylor_degree':k+1,'exp_taylor_lower':str(explo),'tail_ge_Kplus1':str(tails[k+1]),'tail_ge_K':str(tails[k]),'tail_ge_Kminus1':str(tails[k-1]),'p0':str(p0),'p1':str(p1),'p2':str(p2)})
    mean=[(ts[i][1]+ell[i]*ts[1-i][0])/ks[i] for i in range(2)]
    diag=[(ts[i][2]+(ell[i]**2+ell[i])*ts[1-i][0])/ks[i]**2 for i in range(2)]
    off=(ts[0][1]*ell[1]+ell[0]*ts[1][1])/(ks[0]*ks[1])
    return mean,diag,off,receipts

def confidence(h,sums,squares):
    n=h['N'];bits=h['sqrt_bits'];alpha=F(h['alpha_stat']);eta=F(h['eta']);hats=[v/n for v in sums]
    variance=[(squares[j]-sums[j]**2/n)/(n-1) for j in range(8)]
    if any(v<0 for v in variance):raise ArithmeticError('negative exact empirical variance')
    lu=log_upper(32/alpha);stat=[];roots=[]
    for j in range(8):
        rad=2*variance[j]*lu/n;_,hi=sqrt_bounds(rad,bits);stat.append(hi+F(7*RANGES[j])*lu/(3*(n-1)));roots.append({'coordinate':COORDS[j],'radicand':str(rad),'sqrt_upper':str(hi)})
    tm,td,to,poisson=bias_bounds(h)
    em=[sqrt_bounds(stat[2*i]**2+stat[2*i+1]**2,bits)[1]+tm[i]+eta for i in range(2)]
    ed=[stat[4+i]+td[i]+2*eta for i in range(2)];eo=sqrt_bounds(stat[6]**2+stat[7]**2,bits)[1]+to+2*eta
    return {'empirical_means':list(map(str,hats)),'unbiased_variances':list(map(str,variance)),'statistical_coordinate_radii':list(map(str,stat)),'log_argument':str(32/alpha),'natural_log_upper':str(lu),'log_method':'ceil-log2 upper; e>2','statistical_sqrt_enclosures':roots,'poisson_receipts':poisson,'clipping_mean_bias':list(map(str,tm)),'clipping_diagonal_bias':list(map(str,td)),'clipping_offdiagonal_bias':str(to),'mean_disk_radii':list(map(str,em)),'diagonal_total_radii':list(map(str,ed)),'offdiagonal_disk_radius':str(eo),'coding_mean_bias':str(eta),'coding_covariance_bias':str(2*eta)}

def affinity_geometry(means,mean_radii,off,off_radius,diag,diag_radii,bits):
    reasons=[]
    if any(norm2(means[i])<=mean_radii[i]**2 for i in range(2)):reasons.append('mean_disk_contains_zero')
    lowers=[diag[i]-diag_radii[i] for i in range(2)];uppers=[diag[i]+diag_radii[i] for i in range(2)]
    if any(v<=0 for v in lowers):reasons.append('diagonal_lower_guard_not_positive')
    a=off;b=conj(means[0]);c=means[1];ea=off_radius;eb,ec=mean_radii;ua,ub,uc=map(l1,(a,b,c))
    err=(ua+ea)*(ub+eb)*(uc+ec)-ua*ub*uc;im=abs(cmul(cmul(a,b),c)[1]);L=max(F(0),im-err)
    detail={'product_imaginary_abs':str(im),'product_error_upper':str(err),'product_imaginary_lower':str(L),'L1_upper_magnitudes':list(map(str,(ua,ub,uc))),'diagonal_lower_guards':list(map(str,lowers)),'diagonal_upper_bounds':list(map(str,uppers))}
    def unknown(why):return {'status':'UNKNOWN','reasons':why,'affinity_lower':None,'affinity_squared_lower':None,'geometry':detail}
    if not L:reasons.append('imaginary_product_not_resolved')
    if reasons:return unknown(reasons)
    denom=(ub+eb)**2*(uc+ec)**2*uppers[0]*uppers[1]
    if denom<=0:return unknown(['nonpositive_denominator'])
    r2=L**2/denom;detail['radius_squared_lower']=str(r2)
    if r2>=1:return unknown(['inconsistent_radius_squared_ge_one'])
    A2=36*r2/(1-r2);Alo,Ahi=sqrt_bounds(A2,bits);detail['affinity_display_sqrt_upper']=str(Ahi)
    return {'status':'CONDITIONAL_LOWER_BOUND','reasons':[],'affinity_lower':str(Alo),'affinity_squared_lower':str(A2),'radius_squared_lower':str(r2),'geometry':detail,'inequality':'Amax^2>=36*rlo_squared/(1-rlo_squared) since pi>3; affinity_lower^2<=affinity_squared_lower'}

def certify(stream):
    it=iter(stream);digest=hashlib.sha256();bytecount=0;EOF=object()
    def line():
        nonlocal bytecount
        raw=next(it,EOF)
        if raw is EOF:return EOF
        if isinstance(raw,str):
            try:raw=raw.encode('utf-8')
            except UnicodeError as e:raise InputError(f'invalid UTF-8 text line: {e}') from None
        require(isinstance(raw,bytes),'stream must yield bytes/text lines');digest.update(raw);bytecount+=len(raw);return raw
    first=line();require(first is not EOF,'missing header');h=parse_header(parse_json(first,'line1'))
    sums=[F(0)]*8;squares=[F(0)]*8;clipped=0;photons=[[0,0] for _ in range(3)];max_counts=[0,0]
    for i in range(h['N']):
        raw=line();require(raw is not EOF,f'missing block: expected{h["N"]}, received{i}')
        f,counts,totals,cut=block(parse_json(raw,f'line{i+2}'),i,h['cutoffs'])
        for j in range(8):sums[j]+=f[j];squares[j]+=f[j]**2
        clipped+=int(cut)
        for r in range(3):
            for ch in range(2):photons[r][ch]+=counts[r][ch]
        max_counts=[max(max_counts[ch],totals[ch]) for ch in range(2)]
    require(line() is EOF,f'extra data after fixed N={h["N"]}; no prefix certificate')
    conf=confidence(h,sums,squares);hat=list(map(F,conf['empirical_means']))
    result=affinity_geometry([(hat[0],hat[1]),(hat[2],hat[3])],list(map(F,conf['mean_disk_radii'])),(hat[6],hat[7]),F(conf['offdiagonal_disk_radius']),[hat[4],hat[5]],list(map(F,conf['diagonal_total_radii'])),h['sqrt_bits'])
    total=F(h['alpha_stat'])+sum(map(F,h['alpha_other_total'].values()))
    result.update({'schema':SCHEMA,'qualification':'CONDITIONAL_ON_SUPPLIED_CONTRACTS','physical_experiment_acquired_or_qualified':False,'data_kind':h['data_kind'],'confidence_lower':str(1-total),'failure_total':str(total),'failure_budget_scope':'TOTAL_DATASET','header':h,'header_sha256':hashlib.sha256(json.dumps(h,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'received_stream_sha256':digest.hexdigest(),'received_bytes':bytecount,'blocks':{'expected':h['N'],'processed':h['N'],'clipped_whole':clipped,'retained':h['N']-clipped},'photon_counts_by_record_and_channel':dict(zip(('bright_a','bright_b','dark'),photons)),'observed_max_block_counts_diagnostic_only':max_counts,'observed_maxima_were_used_as_caps':False,'coordinates':list(COORDS),'exact_sums':list(map(str,sums)),'exact_squared_sums':list(map(str,squares)),'confidence_construction':conf,'governing_math':dict(GOVERNING),
       'supplied_not_inferred':['stationary finite-state all-even bidirectional source; real nonnegative emissions','passive common prefilter gate; fixed causal responses; repeated deterministic background','complete capture/reset or charged TOTAL-dataset failure bounds','a,b,d independence and IID fixed-coded blocks, or acquired paid coupling/preparation bounds','conditional independent Poisson readout and externally acquired conditional count-mean ceilings','uniform per-photon coding error eta with a fixed code and norm<=1 rational codes','frequency/gate/coder/N/cutoffs chosen before records; all other budgets are TOTAL-dataset bounds'],
       'precommitment_verified':False,'historical_precommitment_caveat':'The reader freezes the supplied header for one complete file. References/hashes do not prove choices predated human data access or protect repeated post-data reruns.',
       'interpretation':'Dimensionless maximum simple-cycle LOG RATE RATIO under supplied contracts. Thermodynamic entropy per cycle additionally needs supplied local detailed balance. Not entropy-production rate, source qualification, IID test or physical discovery.'})
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',nargs='?',default='-');p.add_argument('-o','--output');args=p.parse_args()
    try:
        if args.input=='-':answer=certify(sys.stdin.buffer)
        else:
            with open(args.input,'rb') as src:answer=certify(src)
        code=0
    except (InputError,OSError,OverflowError,RecursionError) as e:
        answer={'schema':SCHEMA,'status':'INVALID_INPUT','qualification':'NO_CERTIFICATE','affinity_lower':None,'affinity_squared_lower':None,'error':str(e)};code=2
    encoded=json.dumps(answer,indent=2,sort_keys=True)+'\n'
    if args.output:Path(args.output).write_text(encoded)
    else:sys.stdout.write(encoded)
    return code
if __name__=='__main__':raise SystemExit(main())

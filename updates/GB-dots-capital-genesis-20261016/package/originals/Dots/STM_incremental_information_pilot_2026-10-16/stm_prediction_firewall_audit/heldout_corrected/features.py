"""Frozen v1.1 whitelist feature map. Never accepts state/info objects as features.

Unknown keys are ignored intentionally: the sole reads are the documented whitelist.
Input currents are source amperes, converted numerically to nA (gain unverified).
"""
import hashlib
import json
import numpy as np

STAT_NAMES = ['first','last','mean','std','min','max','q10','median','q90','mean_abs_diff','max_abs_diff']

def finite(v, shape=None):
    a = np.asarray(v, dtype=np.float64)
    if shape is not None and a.shape != shape:
        raise ValueError(f'Expected shape {shape}, got {a.shape}')
    if not np.isfinite(a).all():
        raise ValueError('Nonfinite authorized input')
    return a

def trace(v):
    a = finite(v)
    if a.ndim != 1 or len(a) < 2:
        raise ValueError('Trace must be 1-D and length >=2')
    return a

def S(v):
    a = finite(v)
    if a.ndim != 1 or not len(a):
        raise ValueError('S requires nonempty vector')
    d = np.abs(np.diff(a))
    return np.array([a[0],a[-1],a.mean(),a.std(ddof=0),a.min(),a.max(),*np.quantile(a,[.1,.5,.9],method='linear'),d.mean() if len(d) else 0.,d.max() if len(d) else 0.], dtype=np.float64)

def B(v, n=32):
    a = finite(v)
    if a.ndim != 1 or not len(a):
        raise ValueError('B requires nonempty vector')
    return np.interp(np.linspace(0,1,n),np.linspace(0,1,len(a)),a)

def MAD(v):
    return np.median(np.abs(v-np.median(v)))

def current_summary(a):
    d = np.diff(a)
    scale = max(float(MAD(d)),1e-6)
    # Counts normalized by trace length n, as frozen "length-normalized counts".
    return np.r_[S(a),np.count_nonzero(np.abs(d)>3*scale)/len(a),np.count_nonzero(np.abs(d)>6*scale)/len(a),np.median(a[len(a)//2:])-np.median(a[:len(a)//2]),np.max(np.abs(a-np.median(a)))/max(float(MAD(a)),1e-6)]

def _aggregate(a, include_sum):
    parts = [a[-1]]
    if include_sum:
        parts.append(a.sum(axis=0))
    parts.extend([a.mean(axis=0),a.std(axis=0,ddof=0),a.min(axis=0),a.max(axis=0)])
    return np.concatenate(parts)

def feature_maps(record):
    p = finite(record['p'],(2,))
    gp = finite(record['g_minus_p'],(2,))
    prior = finite(record['prior_disagreement'],())
    if prior < 0: raise ValueError('Negative measured disagreement')
    h = record['history']
    if not isinstance(h,list) or not h: raise ValueError('Empty history')
    actions=[]; ds=[]; currents=[]
    for item in h:
        action=finite(item['action'],(6,)); start=finite(item['start_nm'],(2,)); end=finite(item['end_nm'],(2,))
        d=trace(item['d']); current=trace(item['current'])*1e9
        if len(d)!=len(current) or (d<0).any() or abs(d[0])>1e-9: raise ValueError('Incompatible current/d')
        if not np.isfinite(current).all(): raise ValueError('Current conversion overflow')
        actions.append(np.r_[action,start,end]); ds.append(d); currents.append(current)
    av=np.array(actions)
    request=av[-1,8:10]-av[-1,6:8]
    dv=np.array([np.r_[S(d),len(d),np.abs(np.diff(d)).sum()] for d in ds])
    A=np.r_[p,gp,np.linalg.norm(gp),prior,len(h),av[0],_aggregate(av,True),np.concatenate([B(av[:,j],16) for j in range(10)]),request,np.linalg.norm(request),_aggregate(dv,True),B(ds[-1]),B(np.concatenate(ds))]
    C=_aggregate(np.array([current_summary(a) for a in currents]),False)
    normalized=[(a-np.median(a))/max(float(MAD(a)),1e-6) for a in currents]
    F=np.r_[C,B(currents[-1]),B(np.concatenate(currents)),B(normalized[-1]),B(np.concatenate(normalized))]
    result={'A':A,'A+C':np.r_[A,C],'A+F':np.r_[A,F]}
    for a in result.values():
        if not np.isfinite(a).all(): raise ValueError('Nonfinite resulting features')
    return result

def schema():
    names=['p_x','p_y','g_minus_p_x','g_minus_p_y','goal_radius','prior_disagreement','history_count']
    act=['action_'+str(i) for i in range(6)]+['request_start_x','request_start_y','request_end_x','request_end_y']
    for stat in ['first','latest','sum','mean','std','min','max']:
        names.extend('action_'+stat+'_'+c for c in act)
    names.extend('action_B16_'+c+'_'+str(i) for c in act for i in range(16))
    names.extend(['latest_request_difference_x','latest_request_difference_y','latest_request_difference_norm'])
    dnames=STAT_NAMES+['length','total_absolute_difference']
    for stat in ['latest','sum','mean','std','min','max']:
        names.extend('d_'+stat+'_'+c for c in dnames)
    names.extend('d_B32_'+which+'_'+str(i) for which in ['latest','concatenated'] for i in range(32))
    cnames=STAT_NAMES+['spikes3_per_n','spikes6_per_n','half_median_difference','max_abs_deviation_per_MAD']
    C=['current_'+stat+'_'+c for stat in ['latest','mean','std','min','max'] for c in cnames]
    F=C+['current_B32_'+which+'_'+str(i) for which in ['latest','concatenated','latest_MADnormalized','concatenated_pertrace_MADnormalized'] for i in range(32)]
    return {'version':'STM-v1.1','dtype':'float64','quantiles':'linear','std_ddof':0,'current_source_to_nA':1e9,'spike_denominator':'trace_length','arms':{'A':names,'A+C':names+C,'A+F':names+F}}

def schema_hash():
    return hashlib.sha256(json.dumps(schema(),sort_keys=True,separators=(',',':')).encode()).hexdigest()

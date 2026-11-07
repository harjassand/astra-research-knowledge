"""CPU replay of author pulsed coincidence baseline on acquired Figshare SPC data.
No simulated observations. Source algorithm: Israel et al Nat Commun 8:14786,
2017 supplementary software; BSD licensed. Independent NumPy implementation.
"""
from pathlib import Path
import argparse, hashlib, io, json, math, time, zipfile
import numpy as np
from scipy.io import loadmat
from scipy.stats import chi2

HERE = Path(__file__).resolve().parent
CHANNELS = np.r_[np.arange(13,21), np.arange(3,11)]
REL = np.array([0,10,-3,12,-18,27,12,-15,35,67,21,22,-26,400,16,3])
DARK = np.array([368.654,469.644,340.002,501.489,336.291,694.435,
                 420.647,379.020,1591.010,686.283,173.411,249.130,
                 448.907,0,369.273,331.315])
TPB = .164610e-9
LASER_HZ = 10e6 # exact source Run_TimeTraceCalc uses10MHz; source paper Methods20MHz
TRIGGER_DIVIDER = 20
TRIGGER_INDEX = 13 # zero-based index in CHANNELS, actual channel8
FORBIDDEN = {(0,1),(1,0),(2,3),(3,2)}

def decode(buf, high_rule='author', drop_last=True):
    w=np.frombuffer(buf,dtype='<u4'); kind=w>>30
    hi=kind==1; event=kind==0
    hi_vals=(w[hi]&((1<<30)-1)).astype(np.int64)
    hi_num=np.cumsum(hi)-1; hi_num=np.maximum(hi_num,0)
    high=hi_vals[hi_num].copy()
    if high_rule=='manual':
        # The manual says a high word applies starting at PREVIOUS event.
        # That interpretation is explicitly compared to observed ordering.
        for i,v in zip(np.flatnonzero(hi),hi_vals):
            prior=np.flatnonzero(event[:i])
            if len(prior): high[prior[-1]]=v
    times=(w[event]&((1<<24)-1)).astype(np.int64)+(high[event]<<24)
    channels=((w[event]>>24)&31).astype(np.int64)
    gaps=((w[event]>>29)&1).astype(bool)
    desc=int(w[0]);raw=(desc>>26)&1
    receipt=dict(records=len(w),events=len(times),high_records=int(hi.sum()),
                 raw_bit=raw,tpb_femtoseconds=desc&((1<<24)-1),gap_bits=int(gaps.sum()),
                 negative_increments_all=int((np.diff(times)<0).sum()),
                 negative_increments_without_last=int((np.diff(times[:-1])<0).sum()),
                 final_jump_ns=float((times[-1]-times[-2])*TPB*1e9))
    if drop_last: times,channels=times[:-1],channels[:-1]
    return times,channels,receipt

def prepare(buf, rel=REL):
    times,chs,receipt=decode(buf)
    dt=(times[-1]-times[0])*TPB
    lookup=np.full(32,-1,dtype=int);lookup[CHANNELS]=np.arange(16)
    ix=lookup[chs]
    if np.any(ix<0): raise ValueError('Unknown channel')
    # Source rates use unshifted absolute timestamps and dT, without subtracting
    # first timestamp. Retain that behavior for a literal replay.
    bins_unshift=np.ceil(times*TPB*4/dt).astype(int)-1
    rates=np.zeros((4,16),dtype=int)
    for k in range(4): rates[k]=np.bincount(ix[np.minimum(bins_unshift,3)==k],minlength=16)
    corrected=times+rel[ix]; order=np.argsort(corrected,kind='stable')
    corrected,ix=corrected[order],ix[order]
    trig=ix==TRIGGER_INDEX;trigt=corrected[trig]
    ntrig=np.cumsum(trig)
    pt=corrected[~trig];pix=ix[~trig]; ti=ntrig[~trig]
    delay=pt-np.where(ti>0,trigt[np.maximum(ti-1,0)],0)
    time_div=(trigt[-1]-trigt[0])/(len(trigt)-1)/TRIGGER_DIVIDER
    pulse=ti*TRIGGER_DIVIDER+np.floor(delay/time_div).astype(int)
    within=np.mod(delay,time_div)
    frame=np.ceil(pt*TPB*4/dt).astype(int)-1
    receipt.update(duration_seconds=float(dt),trigger_events=len(trigt),
      inferred_trigger_hz=float((len(trigt)-1)/((trigt[-1]-trigt[0])*TPB)),
      inferred_laser_hz=float(1/(time_div*TPB)),photon_events=len(pt),
      trigger_interval_bins_minmax=[int(np.diff(trigt).min()),int(np.diff(trigt).max())],
      photon_counts_per_detector=np.bincount(pix,minlength=16).tolist(),
      author_delay_vector_bins=rel.tolist())
    deadtime=[]
    for j in range(16):
      if j==TRIGGER_INDEX:continue
      intervals=np.diff(pt[pix==j])*TPB*1e9
      deadtime.append(dict(channel=int(CHANNELS[j]),min_ns=float(intervals.min()),
        intervals_below10ns=int((intervals<10).sum()),
        intervals_below50ns=int((intervals<50).sum()),
        intervals_below100ns=int((intervals<100).sum()),
        total_intervals=len(intervals)))
    pairs=np.column_stack([pulse,pix]); _,multip=np.unique(pairs,axis=0,return_counts=True)
    receipt.update(same_detector_reconstructed_pulse_multiclick_bins=int((multip>1).sum()),
      same_detector_reconstructed_pulse_extra_clicks=int(np.maximum(multip-1,0).sum()),
      same_detector_interarrival=deadtime,
      photon_phase_hist_100bins=np.histogram(within/time_div,bins=np.linspace(0,1,101))[0].tolist())
    return pulse,pix,within,frame,rates,receipt

def correlations(pulse,pix,range_=50):
    out=np.zeros(range_+1,dtype=np.int64)
    # Author checks prior20 photons. Here every pair within50 pulses is counted
    # by shifting until all remaining lag values exceed50; verifies offset20.
    maxoffset=0
    for offset in range(1,len(pulse)):
        d=pulse[offset:]-pulse[:-offset]
        if np.all(d>range_):break
        valid=(d>=0)&(d<=range_)&(pix[offset:]!=pix[:-offset])
        for a,b in FORBIDDEN: valid &= ~((pix[offset:]==a)&(pix[:-offset]==b))
        out+=np.bincount(d[valid],minlength=range_+1)[:range_+1]
        maxoffset=offset
        if offset>2000:raise RuntimeError('Pathological pulse alignment')
    return out,maxoffset

def dark_pairs(rate,dt,scale=1):
    d=DARK.copy()*scale;d=np.delete(d,TRIGGER_INDEX)
    r=np.delete(rate,TRIGGER_INDEX)
    g=0.
    for i in range(14):
      for j in range(i+1,15):
        if (i,j) in FORBIDDEN:continue
        g+=(d[i]*r[j]+d[j]*r[i]-d[i]*d[j])*dt/LASER_HZ
    return g

def summarize_g2(counts,rates,dt,darkscale=1):
    g0=float(counts[0]);mean=float(counts[6:50].mean())
    dk=dark_pairs(rates/(dt/4),dt/4,darkscale)
    denom=mean-2*dk
    g=2*(g0-dk)/denom if denom>0 else math.nan
    # Literal source uncertainty and threshold; source uses M=44, dark count
    # calibration treated as Poisson based on duration of science frame.
    G0=max(2*g0,.1*mean);B=2*dk;dc=DARK.sum()*darkscale*dt/4
    if mean<15 or denom<=0 or dc<=0:err=198.
    else:
      err=math.sqrt(((G0-mean)/denom**2*B/math.sqrt(dc))**2+
          G0/denom**2+((G0-B)/denom**2*math.sqrt(mean/44))**2)
    return dict(zero_pairs=int(g0),side_mean=mean,dark_pairs=dk,g2=g,
                source_error=err,source_dominance_pass=bool(g<.375-1.96*err))

def raw_multiplicity(pulse,pix):
    # Counts distinct detectors in each reconstructed excitation bin. At15
    # channels with dead time, this is NOT true photon-number resolution.
    unique=np.unique(np.column_stack([pulse,pix]),axis=0)
    pp,n=np.unique(unique[:,0],return_counts=True)
    hist=np.bincount(n,minlength=7)
    exposures=int(pulse.max()-pulse.min()+1)
    hist[0]=exposures-len(pp)
    triples=int(sum(int(math.comb(int(x),3)) for x in n if x>=3))
    # A triple is accepted only if all3 detector pairs meet source exclusions.
    validtriple=0
    for p in pp[n>=3]:
      ids=unique[unique[:,0]==p,1]
      import itertools
      validtriple+=sum(all((int(a),int(b)) not in FORBIDDEN for a,b in itertools.combinations(c,2)) for c in itertools.combinations(ids,3))
    return dict(reconstructed_pulses=exposures,distinct_detector_hist=hist.tolist(),
                all_distinct_triple_combinations=triples,source_allowed_triples=int(validtriple))

def saved_rows(cycle):
    # Source MAT summarizes221 cycles1835..2000,1..55. Verify via rates+g2.
    k=cycle-1835 if cycle>=1835 else 166+cycle-1
    return np.arange(k*4,(k+1)*4)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',default='/tmp/astra_premise_quantum_data.zip');ap.add_argument('--all',action='store_true');args=ap.parse_args()
 start=time.perf_counter();z=zipfile.ZipFile(args.archive)
 mat=loadmat(io.BytesIO(z.read('ExampleData2/analysisG2/analysisG2_threshold.mat')))
 names=[x for x in z.namelist() if x.endswith('.spc')]
 if not args.all:names=[x for x in names if any(x.endswith('_c'+str(c).zfill(4)+'.spc') for c in [1,2,1857,1881,1950])]
 results=[]
 for name in names:
  buf=z.read(name);cycle=int(name[-8:-4]);pulse,pix,within,frame,rates,meta=prepare(buf)
  _,_,manual=decode(buf,'manual');meta['manual_previous_event_decode']=manual
  rows=saved_rows(cycle);frames=[]
  for k in range(4):
   take=frame==k;g,maxoffset=correlations(pulse[take],pix[take]);s=summarize_g2(g,rates[k],meta['duration_seconds'])
   mr=int(rows[k]);expected=mat['g2TrigMat'][mr].astype(int)
   s.update(frame=k+1,g2_counts=g.tolist(),max_neighbor_offset=maxoffset,
            zero_rounded_phase_fraction=float(np.mean(np.rint(within[take])==0)),
            source_phase_valid=bool(np.mean(np.rint(within[take])==0)<=.01),
            saved_mat_row_1based=mr+1,saved_g2=float(mat['g2_pulsed_minus_dk_cycle'][0,mr]),
            saved_rate=float(mat['Rs_sum'][0,mr]),saved_pass=bool(mat['thrs_single_emitters'][0,mr]),
            saved_g2_counts_max_abs_difference=int(np.max(np.abs(g-expected))),
            raw_multiplicity=raw_multiplicity(pulse[take],pix[take]),
            sensitivity_dark_half=summarize_g2(g,rates[k],meta['duration_seconds'],.5)['g2'],
            sensitivity_dark_double=summarize_g2(g,rates[k],meta['duration_seconds'],2)['g2'])
   frames.append(s)
  results.append(dict(file=name,bytes=len(buf),sha256=hashlib.sha256(buf).hexdigest(),meta=meta,frames=frames))
  print(name,'g2',*[round(f['g2'],4) for f in frames],'match',*[f['saved_g2_counts_max_abs_difference'] for f in frames],flush=True)
 archive=Path(args.archive);b=archive.read_bytes()
 out=dict(source='https://doi.org/10.6084/m9.figshare.4588723.v1',archive=dict(path=str(archive),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),md5=hashlib.md5(b).hexdigest()),
    implementation='Independent CPU NumPy replay of source cross-detector coincidence with exact full neighbor scan',
    calibration_scope='Source supplied calibration vectors; calibration exposures unacquired',
    data_selection='all63SPC' if args.all else 'five files selected by fixed cycle numbers for low/high-g2 replay',
    total_spc_files_in_archive=63,mat_rows=884,mat_passes=int(mat['thrs_single_emitters'].sum()),
    elapsed_seconds=time.perf_counter()-start,results=results)
 HERE.joinpath('BASELINE_ALL.json' if args.all else 'BASELINE_SUBSET.json').write_text(json.dumps(out,indent=2,allow_nan=False))
 print('elapsed_seconds',out['elapsed_seconds'],flush=True)

if __name__=='__main__':main()

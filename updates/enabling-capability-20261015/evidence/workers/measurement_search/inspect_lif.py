from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import h5py,numpy as np
start=time.perf_counter()
p=ROOT/'data'/'transient_LiF_nirlinpol_run6_scan_000_2024_05_07_16_29_09.hdf5'
with h5py.File(p) as f:
 on=f['data/res0/on'][()].astype(float);off=f['data/res0/off'][()].astype(float)
 bon=f['data/bg0/on'][()].mean(0);boff=f['data/bg0/off'][()].mean(0)
on=on.mean(2)-bon;off=off.mean(2)-boff
pixel=np.array([577,635,655,666,1035.5,1119,1137.5]);lamb=np.array([27.2,26.31,25.99,25.85,20.7,19.5,19.2])
coef=np.polyfit(pixel,lamb,1);energy=1239.843/np.polyval(coef,np.arange(1340))
time_fs=-(np.arange(100)*0.1+3-11.1)*6.6
reports=[];maps=[]
for pol in range(2):
 a=on[:,pol,:1300];b=off[:,pol,:1300]
 dod=-np.log10(a/b)
 # Same source off-only adjacent delay calibration. Direct SVD least-squares
 # avoids squaring its condition number, but is NOT claimed bitwise source replay.
 cal=-np.log10(b[::2]/b[1::2]);edge=cal[:,:1025]
 beta,res,rank,s=np.linalg.lstsq(edge,cal,rcond=1e-12)
 referenced=dod-dod[:,:1025]@beta
 # Source heat offset window, explicitly script-derived rather than measured axis metadata.
 referenced=referenced-referenced[30:40].mean(0)
 maps.append(referenced)
 details={'polarization_index':pol,'source_waveplate_degrees':[0,45][pol],'dOD_shape':list(dod.shape),'on_positive_fraction':float(np.mean(a>0)),'off_positive_fraction':float(np.mean(b>0)),'edge_calibration_rows':int(edge.shape[0]),'edge_calibration_columns':int(edge.shape[1]),'edge_rank':int(rank),'retained_singular_min':float(s[rank-1]),'retained_singular_max':float(s[0]),'reference_band_energy_eV':[float(energy[0]),float(energy[1024])],'feature_summaries':[]}
 for center in [59.2,61.2,61.7,62.5]:
  reg=(energy[:1300]>=center-.1)&(energy[:1300]<=center+.1)
  zero=(time_fs>=-.7)&(time_fs<=.7)
  details['feature_summaries'].append({'energy_center_eV':center,'n_spectral_pixels':int(reg.sum()),'n_time_points':int(zero.sum()),'raw_mean_mOD':float(1000*dod[np.ix_(zero,reg)].mean()),'referenced_heat_subtracted_mean_mOD':float(1000*referenced[np.ix_(zero,reg)].mean())})
 reports.append(details)
np.savez_compressed(ROOT/'data'/'single_scan_processed.npz',energy_eV=energy[:1300],time_fs=time_fs,parallel=maps[0],perpendicular=maps[1])
model={}
for q in (ROOT/'data').glob('DeltaOD*.npy'):
 v=np.load(q);model[q.name]={'shape':list(v.shape),'min':float(v.min()),'max':float(v.max()),'finite_fraction':float(np.isfinite(v).mean())}
out={'raw_file':p.name,'purpose':'Access and nuisance inspection only; one scan, not full source replication or independent mechanism validation.','delay_axis':'Hardcoded source script: -(3+0.1*j-11.1)*6.6 fs; j=0,...,99','energy_axis':'Least-squares linear wavelength calibration from seven source script line positions; energy 1239.843/lambda_nm','polarization_maps':reports,'model_arrays':model,'wall_seconds_measured':time.perf_counter()-start,'novelty':'NOT_ESTABLISHED','comparative_advantage':'NOT_TESTED','physical_validation':'SOURCE_REPORTED_ONLY'}
(ROOT/'RAW_INSPECTION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

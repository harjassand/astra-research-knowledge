"""Extract public primary measurements without filling missing samples.
Run with the primary Python runtime; source provenance is in data_manifest.json.
"""
import csv,hashlib,json,math,pathlib,collections
import numpy as np
import openpyxl
P=pathlib.Path(__file__).parent
summary={}
def write_csv(name,header,rows):
 with (P/name).open('w',newline='') as f:
  w=csv.writer(f);w.writerow(header);w.writerows(rows)
w7=openpyxl.load_workbook(P/'source_data_fig_7.xlsx',read_only=True,data_only=True)
r7b=list(w7['panel b'].iter_rows(min_row=3,values_only=True))
ireland=[]
for label,col in [('2016-12',5),('2021-12',6)]:
 y=np.array([r[col] for r in r7b if isinstance(r[col],(int,float))]);
 summary['Ireland_'+label]={'n':len(y),'min_mHz':float(y.min()),'max_mHz':float(y.max()),'half_peak_to_trough_mHz':float(np.ptp(y)/2),'initial_peak_to_min_drop_mHz':float(y[0]-y.min()),'fundamental_amplitude_mHz':float(2*abs(np.fft.rfft(y-y.mean())[1])/len(y))}
 for k,a in enumerate(y):ireland.append((label,k,a))
write_csv('ireland_measured_minute_waveforms.csv',['month','second','frequency_deviation_mHz'],ireland)
r7f=list(w7['panel f'].iter_rows(min_row=3,values_only=True));out=[]
for label,col,tcol in [('before_Current_1',1,0),('before_Current_3',2,0),('after_Current_3',5,4),('after_Current_1',6,4)]:
 rows=[r for r in r7f if hasattr(r[tcol],'second')];
 t=np.array([(r[tcol]-rows[0][tcol]).total_seconds() for r in rows]);y=np.array([float(r[col]) if isinstance(r[col],(int,float)) else np.nan for r in rows]);
 for r,tt,yy in zip(rows,t,y):out.append((label,r[tcol].isoformat(),tt,'' if not np.isfinite(yy) else yy))
 threshold=float(np.nanmax(y)/2);hit=t[y>threshold]
 starts=[float(hit[0])] if len(hit) else []
 for i in range(1,len(hit)):
  if hit[i]-hit[i-1]>1.5:starts.append(float(hit[i]))
 R=float(abs(np.mean(np.exp(2j*np.pi*np.array(starts)/60)))) if starts else None
 summary[label]={'timestamp_count':len(t),'finite_count':int(np.isfinite(y).sum()),'missing_timestamps_seconds':sorted(set(range(601))-set(map(int,t))),'missing_values_seconds':t[~np.isfinite(y)].tolist(),'maximum_A':float(np.nanmax(y)),'event_threshold_A':threshold,'event_starts_seconds':starts,'event_start_phases_mod_60_s':[float(x%60) for x in starts],'start_phase_resultant_60s':R}
write_csv('ups_fig7f_measured_current.csv',['channel_as_labelled_in_source','timestamp','elapsed_seconds','current_A'],out)
w6=openpyxl.load_workbook(P/'source_data_fig_6.xlsx',read_only=True,data_only=True);r6=list(w6['Panel a'].iter_rows(values_only=True));out=[]
for c in [0,18,36]:
 channel=r6[0][c].strip()
 for j in range(1,17):
  date=r6[1][c+j]
  for row in r6[2:]:out.append((channel,date,row[c],row[c+j]))
write_csv('building_measured_minute_waveforms.csv',['meter','week','second','periodic_active_power_W'],out)
r6b=list(w6['Tabelle3'].iter_rows(min_row=2,values_only=True));out=[];d=collections.defaultdict(list)
for r in r6b:
 out.append((r[1].date().isoformat(),r[2],r[3]));d[r[1].date().isoformat()].append(r[3])
write_csv('ups_hourly_phase_indices.csv',['day','hour_UTC','argmax_diff_sample_index'],out)
summary['phase_index_interpretation']='Indices are from 20 samples per 60-second waveform (3-second sampling); a two-index daily progression corresponds to six seconds. No phase unwrapping or imputation performed in CSV.'
summary['daily_mode_phase_indices']={k:collections.Counter(v).most_common(1)[0][0] for k,v in d.items()}
w3=openpyxl.load_workbook(P/'source_data_fig_3.xlsx',read_only=True,data_only=True);r3=list(w3['Panel a'].iter_rows(values_only=True));out=[]
for c in range(1,25):
 for row in r3[2:]:out.append((r3[1][c],row[0],row[c]))
write_csv('continental_europe_hourly_minute_waveforms.csv',['hour_CET_or_CEST','second','frequency_deviation_mHz'],out)
(P/'measurement_summary.json').write_text(json.dumps(summary,indent=2))
static='https://static-content.springer.com/esm/art%3A10.1038%2Fs41560-026-02144-0/MediaObjects/'
mapping={'source_data_fig_3.xlsx':static+'41560_2026_2144_MOESM5_ESM.xlsx','source_data_fig_5.xlsx':static+'41560_2026_2144_MOESM7_ESM.xlsx','source_data_fig_6.xlsx':static+'41560_2026_2144_MOESM8_ESM.xlsx','source_data_fig_7.xlsx':static+'41560_2026_2144_MOESM9_ESM.xlsx','supplement_published.pdf':static+'41560_2026_2144_MOESM1_ESM.pdf','Smart_Household_Devices.zip':'https://zenodo.org/api/records/21997337/files/Smart%20Household%20Devices.zip/content'}
manifest={'paper_doi':'10.1038/s41560-026-02144-0','dataset_version_doi':'10.5281/zenodo.21997337','dataset_concept_doi':'10.5281/zenodo.17366692','source_archives':'source_data_fig_5/6/7.xlsx extracted via HTTP byte ranges from Source Data Figures.zip; ZIP member CRC verified by Python zipfile. Fig3 and supplement downloaded directly from publisher.','files':[],'warnings':['Raw UPS_DC_#.csv files require multiplication by 0.1 to convert manufacturer MODBUS values to ampere. This does not authorize blanket rescaling of already-labelled ampere source-data sheets.','Fig7 panel f has missing timestamps/values before update; do not drop missing samples and treat remaining observations as uniformly sampled.','Paper Supplementary Note9 refers to updated battery block1, whereas the changed trace appears in source workbook columns labelled Current3. Preserve literal channel labels; do not infer a one-to-one physical-block mapping.','Source Fig6 waveforms are averaged at 3-second resolution, not measurements of subsecond pulse shapes.','The 2025 arXiv v1 and 2026 final paper differ materially, including Mallorca interpretation and amplitude conventions; use final paper and final supplement.']}
for fn,url in mapping.items():
 b=(P/fn).read_bytes();manifest['files'].append({'file':fn,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'source_url':url})
(P/'data_manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps(summary,indent=2))

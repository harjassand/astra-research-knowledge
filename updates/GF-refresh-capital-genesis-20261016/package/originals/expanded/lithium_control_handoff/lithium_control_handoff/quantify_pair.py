from recover_mpr_pair import *
out={}
for label,f in FILES.items():
 a=parse(BASE/f);t=a['time_s'];v=a['Ewe_V'].astype(float);q=a['Q_mAh'];dq=a['dq_mAh'];mode=a['flags']&3
 first=int(np.flatnonzero(a['Ns']==2)[0]);last=len(a)-1
 stages={'whole_acquisition':(0,last),'negative_protocol':(first,last)}
 if label=='CC':
  cv=int(np.flatnonzero((a['Ns']==2)&(mode==2))[0]);stages.update(galvanostatic_negative=(first,cv-1),negative_voltage_hold=(cv-1,last))
 else:stages['preparation']=(0,first)
 res={'file':str((BASE/f).relative_to(ROOT)),'sha256':hashlib.sha256((BASE/f).read_bytes()).hexdigest(),'n':len(a),'stages':{}}
 for name,(start,end) in stages.items():
  d=np.diff(q[start:end+1]);vl=v[start:end];vr=v[start+1:end+1];neg=np.maximum(-d,0);pos=np.maximum(d,0);span=float(t[end]-t[start]);
  res['stages'][name]={'start_index':start,'end_index':end,'start_s':float(t[start]),'end_s':float(t[end]),'elapsed_s':span,'negative_mAh':float(neg.sum()),'negative_C':float(neg.sum()*3.6),'positive_mAh':float(pos.sum()),'net_negative_mAh':float(-d.sum()),'mean_negative_mA':float(neg.sum()*3600/span),'signed_Ewe_work_mWh_left':float((d*vl).sum()),'signed_Ewe_work_mWh_right':float((d*vr).sum()),'absolute_Ewe_work_mWh_left':float((abs(d*vl)).sum()),'absolute_Ewe_work_mWh_right':float((abs(d*vr)).sum())}
 res['sum_negative_dq_mAh']=float(-np.minimum(dq,0).sum());res['charge_delta_minus_dq_max_abs_mAh']=float(abs(np.diff(q)-dq[1:]).max())
 if label=='P4-8':
  res['number_negative_pulse_starts']=int(np.count_nonzero((a['Ns'][1:]==2)&(a['Ns'][:-1]!=2)))
  pulse_starts=np.flatnonzero((a['Ns'][1:]==2)&(a['Ns'][:-1]!=2))+1
  pulse_ends=pulse_starts+1
  res['sum_between_pulse_start_end_s']=float(np.sum(t[pulse_ends]-t[pulse_starts]));res['firstpulse_start_s']=float(t[first]);res['lastpulse_end_s']=float(t[pulse_ends[-1]])
 out[label]=res
(ROOT/'verified_pair_metrics.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))

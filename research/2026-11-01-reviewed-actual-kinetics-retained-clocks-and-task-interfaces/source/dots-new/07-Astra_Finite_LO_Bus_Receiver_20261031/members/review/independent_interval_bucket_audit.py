"""Independent high precision enclosures, exact table receiving and bucket POVMs."""
from pathlib import Path
from fractions import Fraction as F
import json,math
import mpmath as mp
import numpy as np
root=Path(__file__).resolve().parent;mp.mp.dps=130;j=json.loads((root/'finite_lo_certificates.json').read_text());results=[]
def mf(s):
 f=F(s);return mp.mpf(f.numerator)/f.denominator
def inside(name,v,r):
 lo,hi=map(mf,r['interval']);assert lo<=v<=hi,(name,mp.nstr(v,60));results.append(dict(name=name,value=mp.nstr(v,60),width=mp.nstr(hi-lo,8)))
T=2*mp.pi;beta=mp.mpf(8);D=beta*beta+1;r=mp.exp(-beta*T);Fw=(T*(1+beta*beta/(2*D))-(1-r)/(beta*D*D))/24-(1-r)**2*mp.exp(-2)/(48*beta*D*D)
S=mp.mpf(999)/5000*Fw;ell=mp.pi/40-S;table_checks=0;overflow_checks=[]
for row in j['rows']:
 n=mf(row['parameters']['observed_LO_mean']);v=mp.exp(-(mp.sqrt(n+4*S)-mp.sqrt(n))**2/2);t=mp.exp(-2*ell)*v;d=mp.exp(-8*ell);w=1-t;q=1-d;margin=2*t-1-d
 dm=q if margin>=0 else 4*w*w/(4*w-q);lam=n+4*S;po=mp.exp(-lam)*lam**21/mp.factorial(21)/(1-lam/22);data=mp.mpf(4)/10000*(T+mp.mpf(1)/8+mp.mpf(1)/100+1);cor=mp.mpf(4)/10**6;total=dm+2*po+data+cor+mp.mpf(1)/1000;theta=mp.atan(2*mp.sqrt(S/n))/2
 vals={'source_beta8_collected_energy':S,'source_beta8_lost_energy':ell,'LO_adjacent_factor':v,'minimax_condition_margin':margin,'exact_bus_receiver_diamond':dm,'maximum_total_count_mean':lam,'uniform_overflow_probability_upper':po,'continuing_data_error_upper':data,'finite_correction_error_upper':cor,'total_complete_error_upper':total,'theta_interval':theta}
 for name,value in vals.items():inside(str(n)+'_'+name,value,row[name])
 actual=1-mp.exp(-lam)*mp.fsum(lam**k/mp.factorial(k) for k in range(21));assert actual<=po
 overflow_checks.append(dict(nlo=str(n),actual_tail=mp.nstr(actual,50),certified_upper=mp.nstr(po,50)))
 for item in row['finite_correction_table']:
  raw=item['count_difference']*theta;wrapped=raw-mp.nint(raw/mp.pi)*mp.pi;cmd=mf(item['local_Z_coefficient_angle']);err=mf(item['computation_error_upper']);assert abs(cmd-wrapped)<=err;assert err<mp.mpf('1e-8');table_checks+=1
 assert row['meets_0_01']==(total<mp.mpf('.01'))
inside('average_system_efficiency_lower',1-mp.exp(-8*(mp.pi/40-mp.mpf('.314')*S/mp.mpf('.999'))),j['average_efficiency_0_314_extreme_pair_lower'])

# Direct on/off POVM evaluation from coherent amplitudes, then independent bin product.
ss=float(S);el=float(ell);b=np.array([-2,0,2]);nlo=4;theta=.5*np.arctan(2*np.sqrt(ss/nlo));bucket=[]
for N in [1,8,512,1024,4096]:
 K=np.ones((3,3),complex)
 for sign in [1,-1]:
  z=(b*np.sqrt(ss)+sign*1j*np.sqrt(nlo))/np.sqrt(2*N)
  # Each field inner product sums all unresolved photon sectors; click = I-|0><0|.
  alloverlap=np.exp(-abs(z)[:,None]**2/2-abs(z)[None,:]**2/2+z[:,None]*z.conj()[None,:]);zero=np.exp(-abs(z)**2/2);K0=np.outer(zero,zero);K1=alloverlap-K0
  phase=np.exp(sign*1j*theta*(b[:,None]-b[None,:]));K*=K0+phase*K1
 K=K**N*np.exp(-el*(b[:,None]-b[None,:])**2/2)
 assert np.linalg.norm(K.imag)<1e-11;w=1-K[0,1].real;q=1-K[0,2].real;dm=q if q>=2*w else 4*w*w/(4*w-q)
 bucket.append(dict(bins=N,bus_diamond=dm,adjacent=K[0,1].real,extreme=K[0,2].real))
ideal=float(mf(j['rows'][3]['exact_bus_receiver_diamond']['interval'][0]));assert all(x['bus_diamond']>ideal for x in bucket);assert all(bucket[i]['bus_diamond']>bucket[i+1]['bus_diamond'] for i in range(len(bucket)-1))
other=float(mf(j['rows'][3]['continuing_data_error_upper']['interval'][1])+mf(j['rows'][3]['finite_correction_error_upper']['interval'][1])+mp.mpf('.001'))
assert bucket[2]['bus_diamond']+other>.01 and bucket[3]['bus_diamond']+other<.01
out={'high_precision_interval_checks':len(results),'finite_table_checks':table_checks,'interval_results':results,'overflow_comparisons':overflow_checks,'direct_onoff_POVM_checks':bucket,'scope':'High precision checks diagnostic; exact interval implementation, coherent sums and CP bounds reviewed analytically. Bucket comparisons do not acquire binning/rearming services.'}
(root/'independent_interval_bucket_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='interval_results'},indent=2))

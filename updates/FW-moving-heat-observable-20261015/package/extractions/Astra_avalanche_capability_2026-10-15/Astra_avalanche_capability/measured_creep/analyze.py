import numpy as np,json,hashlib
from scipy.stats import weibull_min,chi2
from scipy.optimize import brentq
from pathlib import Path
P=Path(__file__).parent
x87=np.array([.03,.04,.07,.08,.08,.09,.15,.15,.20,.28,.28,.30,.38,.41,.50,.51,.57,.70,.72,.82,.84,1.05,1.13,1.19,1.32,1.35,1.35,1.36,1.39,1.40,1.48,1.55,1.56,1.57,1.59,1.80,1.85,1.86,1.92,2.00,2.08,2.27,2.38,2.46,2.49,2.61,2.61,2.62,2.74,2.79,2.80,2.89,2.91,2.91,3.10,3.11,3.42,3.47,3.50,3.64,3.67,3.68,3.75,4.39,4.50,4.53,4.53,4.65,4.65,4.69,4.70,4.75,4.84,5.01,5.71,5.92,6.19,6.33,6.59,6.62,6.94,7.16,7.29,7.36,7.38,7.42,8.09,8.88,9.05,9.25,9.26,9.47,10.50,10.57,11.25,13.49,13.78,16.15,16.59,18.16])
x80=np.array([1.80,3.10,4.20,6,7.50,8.20,8.50,10.30,10.60,24.20,29.60,31.70,41.90,44.10,49.50,50.10,59.70,61.70,64.40,69.70,70,77.80,80.50,82.30,83.50,84.20,87.10,87.30,93.20,103.40,104.60,105.50,108.80,112.60,116.80,118,122,123.50,124.40,125.40,129.50,130.40,131.60,132.80,133.80,137,140.20,140.90,148.50,149.20,152.20,152.80,157.70,160,163.60,166.90,170.50,174.90,177.70,179.20,183.60,183.80,194.30,195.10,195.30,202.60,220.20,221.30,227.20,251,266.50,267.90,269.20,270.40,272.50,285.90,292.60,295.10,301.10,304.30,316.80,329.80,334.10,346.20,351.20,353.30,369.30,372.30,381.30,393.50,451.30,461.50,574.20,653.30,663,669.80,739.70,759.60,894.70,974.90])
x84=np.array([.25,.31,.44,.45,.57,.65,.73,.89,1.06,1.22,1.37,1.83,1.96,2.15,2.40,2.51,2.77,4.05,4.07,4.34,4.98,5.86,5.90,6.18,6.30,7.14,7.32,7.45,7.92,7.99,8.22,8.35,8.38,8.39,8.45,8.53,8.55,8.64,8.68,8.92,8.93,9.45,9.57,9.80,9.83,10.60,10.82,10.83,11.03,11.12,11.13,12.52,12.94,16.42,16.47,17.68,17.79,18.45,18.95,19.07,19.40,19.62,19.86,20.76,21.38,23.03,23.10,23.83,24.46,24.81,25.15,25.18,26.96,27.53,27.86,29.89,32.55,33.95,34.51,34.74,35.63,36.84,36.97,39.17,41.54,42.32,42.53,43.61,48.54,49.02,55.20,55.99,61.37,63.17,66.48,67.06,74.01,74.61,76.46,84.26,89.87,97.37,119.09])
# Values checked against rotated source image; source ranks are preserved.
def fit(x):
 z=np.log(x);n=len(x)
 def score(b):
  w=np.exp(b*(z-z.max())); return 1/b+z.mean()-(w*z).sum()/w.sum()
 b=brentq(score,.05,20)
 a=np.exp((np.log(np.exp(b*(z-z.max())).mean())+b*z.max())/b)
 ll=n*np.log(b)-n*b*np.log(a)+(b-1)*z.sum()-np.sum((x/a)**b)
 ll0=-n*np.log(x.mean())-n
 return b,a,2*(ll-ll0)
def ks(x):
 n=len(x);f=-np.expm1(-np.sort(x)/x.mean());return max(np.max(np.arange(1,n+1)/n-f),np.max(f-np.arange(n)/n))
rng=np.random.default_rng(82976);B=20000
null=np.array([(*fit(y),ks(y)) for y in rng.exponential(size=(B,100))])
out={}
for label,x in [('440ksi_R087',x87),('404.6ksi_R080',x80),('424.8ksi_R084',x84)]:
 n=len(x)
 if n!=100: null=np.array([(*fit(y),ks(y)) for y in rng.exponential(size=(B,n))])
 b,a,lr=fit(x);D=ks(x)
 np.savetxt(P/(label+'.csv'),np.column_stack([np.arange(1,n+1),x,np.ones(n)]),delimiter=',',header='source_rank,time_hours,event_observed',comments='',fmt=['%d','%.2f','%d'])
 boots=np.array([fit(rng.choice(x,n,replace=True))[0] for _ in range(5000)])
 out[label]={'n':n,'failures':n,'censored':0,'mean_hours':x.mean(),'median_hours':np.median(x),'weibull_shape':b,'weibull_scale_hours':a,'shape_percentile_bootstrap_95CI':np.quantile(boots,[.025,.975]).tolist(),'LR_exp_vs_weibull':lr,'LR_null_bootstrap_p':(1+sum(null[:,2]>=lr))/(B+1),'KS_exp_fitted':D,'KS_null_refit_bootstrap_p':(1+sum(null[:,3]>=D))/(B+1)}
out['bootstrap']={'null_replicates':B,'shape_CI_replicates':5000,'seed':82976,'method':'Parametric iid exponential simulation with scale and Weibull refit; scale invariant for complete samples. Separate nonparametric percentile CI for shape.'}
out['source_sha256']=hashlib.sha256((P/'nasa1995.pdf').read_bytes()).hexdigest()
(P/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
from scipy.stats import f
ratio=x80.mean()/x87.mean();q=440/404.6
# Under independent exponential cohorts, mean ratio divided by true mean ratio is F(200,200).
ci=[ratio/f.ppf(.975,200,200),ratio/f.ppf(.025,200,200)]
nullratio=q**2
z=ratio/nullratio
p=2*min(f.cdf(z,200,200),f.sf(z,200,200))
bootratio=np.mean(rng.choice(x80,size=(20000,100)),axis=1)/np.mean(rng.choice(x87,size=(20000,100)),axis=1)
out['two_cohort_load_sensitivity']={'mean_lifetime_ratio_low_to_high_load':ratio,'stress_ratio':q,'rho_from_two_means':np.log(ratio)/np.log(q),'ratio_F95CI_under_exponential':ci,'rho_F95CI_under_exponential':(np.log(ci)/np.log(q)).tolist(),'rho_nonparametric_bootstrap95CI':np.quantile(np.log(bootratio)/np.log(q),[.025,.975]).tolist(),'specimen_rho2_predicted_ratio':nullratio,'specimen_rho2_two_sided_F_p':p,'scope':'Tests specimen mean-life power-law scaling at just two loads conditional on cohort comparability; NOT elementary fiber rate identification or broad constitutive law validation.'}
(P/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out['two_cohort_load_sensitivity'],indent=2))
# Interior cohort is a held-out check of two endpoint-anchored aggregate mean laws.
alpha_linear=(440-424.8)/(440-404.6)
alpha_log=np.log(440/424.8)/np.log(440/404.6)
preds={}
for name,alpha in [('log_mean_linear_stress',alpha_linear),('log_mean_linear_log_stress',alpha_log)]:
 pred=x87.mean()**(1-alpha)*x80.mean()**alpha
 m87=rng.choice(x87,(20000,len(x87))).mean(axis=1)
 m80=rng.choice(x80,(20000,len(x80))).mean(axis=1)
 m84=rng.choice(x84,(20000,len(x84))).mean(axis=1)
 rr=m84/(m87**(1-alpha)*m80**alpha)
 preds[name]={'endpoint_interpolation_weight':alpha,'heldout_predicted_mean_hours':pred,'heldout_observed_mean_hours':x84.mean(),'observed_to_predicted_ratio':x84.mean()/pred,'ratio_bootstrap95CI':np.quantile(rr,[.025,.975]).tolist()}
out['heldout_middle_cohort']=preds
out['bootstrap']['note']='103-sample null simulations generated separately for middle cohort; three cohorts and two test statistics are exploratory multiplicity, not one preselected confirmatory test.'
(P/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(preds,indent=2))

import math,json
beta=1.0; Delta=1.0; t=1.0
rows=[]
for d in [0.1,0.01,0.001,1e-6,1e-12]:
    pe=math.exp(-beta*Delta)*math.cosh(beta*d)/(1+math.exp(-beta*Delta)*math.cosh(beta*d))
    upavg=math.exp(-beta*Delta)*math.cosh(beta*d)
    cg=(1-pe)*math.exp(-upavg*t)
    ce=pe*math.exp(-t)
    real=cg+ce; imag=0.0
    rows.append({'delta':d,'rescaled_time':t,'logical_coherence_real':real,'logical_coherence_imag':imag,'distance_lower_bound_from_X':1-real})
out={'beta':beta,'Delta':Delta,'downward_rates':1.0,'delta_exactly_zero_coherence':1.0,'nonzero_delta_results':rows,'scope':'Exact dissipative interaction-picture formulas in Davies rescaled time; not a native-code counterexample or finite-coupling simulation.'}
print(json.dumps(out,indent=2))

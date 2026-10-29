from quartic_sos_oracle import *
f={e:Q(0) for e in exps}
for e in [(2,2,0,0),(0,2,2,0),(2,0,2,0),(0,0,0,4)]:f[e]=Q(1)
f[(1,1,1,1)]=Q(-4)
g0,gq,ns=gram_param(f);start=time.time();xx,trace=barrier_search(g0,gq,ns);lower,ys,G,piv,tries=rational_certificate(g0,gq,ns,xx);verify_identity(f,lower,G)
q=[Q(1,2)]*4;upper=exact_eval(f,q);assert upper==0 and lower<0
result=dict(quartic='x²y²+y²z²+z²x²+w⁴−4xyzw (coordinate names arbitrary)',known_exact_global_minimum='0 by AM-GM, attained at (1/2,1/2,1/2,1/2)',SOS_lower=str(lower),SOS_gap=float(-lower),fails_target_1e_6=(-lower>Q(1,10**6)),seconds=time.time()-start,scope='Explicit nonnegative non-SOS obstruction: a fast Gram certificate need not attain the true minimum. No false oracle success is permitted.')
print(json.dumps(result,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')

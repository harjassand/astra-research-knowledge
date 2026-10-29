"""Mean bounds BETWEEN whole regions from the frozen acquired record.

Uses conventional robust row inequalities, with exact rational release
checks. No source or private model is imported. Policy iteration only
proposes vectors; the row certificates are the guarantee.
"""
from pathlib import Path
from fractions import Fraction as F
import json,time
from consume_excursion_record import solve,stringify

ROOT=Path(__file__).resolve().parent

def extreme_matrix(Slo,Shi,R,h,minimize):
    n=len(Slo);A=[i for i in range(n) if i not in R]
    K=[[F(0) for _ in R] for _ in R]
    for x,i in enumerate(R):
        ground=sum((-Slo[i][j] if minimize else -Shi[i][j]) for j in A)
        K[x][x]=ground
        for y,j in enumerate(R):
            if i==j:continue
            use_lower=(h[x]>=h[y]) if minimize else (h[x]<h[y])
            edge=-Slo[i][j] if use_lower else -Shi[i][j]
            K[x][x]+=edge;K[x][y]-=edge
    return K

def envelope(Slo,Shi,R,load,minimize):
    # Every policy contains the connected lower graph and grounding;
    # candidates are ordinary positive nonsingular M-matrix solves.
    h=solve([[Slo[i][j] for j in R] for i in R],load)
    seen=set()
    for iteration in range(1,101):
        K=extreme_matrix(Slo,Shi,R,h,minimize)
        hnew=solve(K,load)
        Knew=extreme_matrix(Slo,Shi,R,hnew,minimize)
        residual=[sum(Knew[i][j]*hnew[j] for j in range(len(R)))-load[i] for i in range(len(R))]
        # Upper: true K*h >= minimum >= b_upper.
        # Lower: true K*h <= maximum <= b_lower.
        passed=all(v>=0 for v in residual) if minimize else all(v<=0 for v in residual)
        if passed:
            assert min(hnew)>=0
            return hnew,{'iterations':iteration,'extreme_residual':residual,'release_verified':True}
        key=tuple(hnew)
        if key in seen:raise RuntimeError('policy cycle: no certificate released')
        seen.add(key);h=hnew
    raise RuntimeError('policy cap: no certificate released')

def main():
    started=time.perf_counter();p=ROOT/'macro_run'
    cert=json.loads((p/'NATIVE_EXCURSION_CERTIFICATE.json').read_text())
    groups=cert['input_contracts']['module_ports'];m=sum(map(len,groups))
    Slo=[[F(x) for x in r] for r in cert['S_lower']]
    Shi=[[F(x) for x in r] for r in cert['S_upper']]
    blo=list(map(F,cert['b_lower']));bhi=list(map(F,cert['b_upper']))
    slo=list(map(F,cert['stationary_event_lower']));shi=list(map(F,cert['stationary_event_upper']))
    vlo=list(map(F,cert['v_lower']));vhi=list(map(F,cert['v_upper']))
    queries=[];vectors=[]
    for amask in range(1,(1<<len(groups))-1):
        A=[j for j in range(len(groups)) if amask>>j&1]
        R=[i for j,g in enumerate(groups) if j not in A for i in g]
        hu,ru=envelope(Slo,Shi,R,[bhi[i] for i in R],True)
        hl,rl=envelope(Slo,Shi,R,[blo[i] for i in R],False)
        assert all(0<=hl[k]<=hu[k] for k in range(len(R)))
        vectors.append({'target_modules':A,'live_ports':R,'lower':hl,'upper':hu,'lower_check':rl,'upper_check':ru})
        for cmask in range(1,1<<len(groups)):
            if cmask&amask:continue
            C=[j for j in range(len(groups)) if cmask>>j&1]
            Cp=[i for j in C for i in groups[j]]
            cl=sum(slo[i]*vlo[i] for i in Cp)/2
            cu=sum(shi[i]*vhi[i] for i in Cp)/2
            nl=cl+sum(blo[i]*hl[R.index(i)] for i in Cp)
            nu=cu+sum(bhi[i]*hu[R.index(i)] for i in Cp)
            dl=sum(blo[i] for i in Cp);du=sum(bhi[i] for i in Cp)
            tl=nl/du;tu=nu/dl
            queries.append({'source_modules':C,'target_modules':A,
                'lower':tl,'upper':tu,'factor':tu/tl,
                'display':[float(tl),float(tu)],'factor_display':float(tu/tl)})
    out={'schema':'astra.between_region_mean_certificate.v1',
        'initial_law':'true stationary law conditioned on the specified source union',
        'same_acquisition_event':True,'failure_probability_upper':cert['failure_probability_upper'],
        'new_source_observations':0,'source_model_reads':0,
        'vectors':vectors,'queries':queries,'query_count':len(queries),
        'max_factor_display':max(q['factor_display'] for q in queries),
        'max_policy_iterations':max(max(x['upper_check']['iterations'],x['lower_check']['iterations']) for x in vectors),
        'wall_seconds':time.perf_counter()-started,
        'scope':'exact verified row inequalities; rectangular relaxation may be nonreversible; no claim that it is the true source',
    }
    (p/'BETWEEN_REGION_CERTIFICATE.json').write_text(json.dumps(stringify(out),indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['query_count','max_factor_display','max_policy_iterations','wall_seconds','new_source_observations']},indent=2))

if __name__=='__main__':main()

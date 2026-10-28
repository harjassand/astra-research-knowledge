"""Independent finite replay for nonsymmetric block echo certificates.

No root compiler or PSD checker is imported. Starts from saved decoded
intervals and checks the new block/adjoint expressions, common contractions,
row/column uncertainty bounds, and final uniform error arithmetic.
"""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from review_uniform_certificate import (ROOT,decode,tr,mm,sub,scale,diag,all_principal_psd,ew,interval)

def main():
    payload=decode(json.loads((ROOT/'results/BLOCK_EXPERIMENT.json').read_text()))
    dictionary=payload['dictionary'];blocks=[tuple(x) for x in payload['blocks']]
    r=len(dictionary);maps=payload['forward_maps'];duals=payload['dual_maps']
    records={tuple(e['word']):(e['interval']['lo'],e['interval']['hi']) for e in payload['decoded_records']}
    C=payload['uniform_certificate'];W=C['metric'];rho=C['rho']
    all_principal_psd(W,strict=True)
    assert F(0)<=rho<1
    for T in maps+duals:all_principal_psd(sub(scale(rho*rho,W),mm(mm(tr(T),W),T)))
    checks=[]
    for dual in [False,True]:
        for i in range(len(blocks)):
            v=blocks[i][::-1] if dual else blocks[i]
            L=duals[i] if dual else maps[i]
            data=[]
            for j in range(r):
                row=[]
                for k in range(r):
                    coeff={}
                    def term(a,mid,b,c):
                        word=ew(dictionary[a],mid,dictionary[b]);coeff[word]=coeff.get(word,F(0))+c
                    term(j,v+v[::-1],k,F(1))
                    for l in range(r):
                        term(j,v[::-1],l,-L[l][k])
                        term(l,v,k,-L[l][j])
                        for m in range(r):term(l,(),m,L[l][j]*L[m][k])
                    row.append(interval(coeff,records))
                data.append(row)
            mid=[[(a+b)/2 for a,b in row] for row in data]
            rows=[sum(((b-a)/2 for a,b in row),F(0)) for row in data]
            upper=[[mid[j][k]+(rows[j] if j==k else 0) for k in range(r)] for j in range(r)]
            index=i+(len(blocks) if dual else 0)
            assert upper==C['residual_uppers'][index]
            all_principal_psd(sub(scale(C['per_map_eps2'][index],W),upper))
            checks.append({'block':list(blocks[i]),'dual':dual,'residual_upper_rebuilt':True,'domination_verified':True})
    for middle,gamma in [((),C['gamma_g'])]+[(v,C['gamma_m']) for v in blocks]:
        radii=[[(records[ew(a,middle,b)][1]-records[ew(a,middle,b)][0])/2 for b in dictionary] for a in dictionary]
        rows=[sum(row,F(0)) for row in radii]
        cols=[sum((radii[j][k] for j in range(r)),F(0)) for k in range(r)]
        D=diag([max(a,b) for a,b in zip(rows,cols)])
        all_principal_psd(sub(scale(gamma,W),D))
    eps=max(C['per_map_eps2']);cn=W[0][0]
    residual=cn*eps/(1-rho)**2
    noise=cn*(C['gamma_g']+(C['gamma_m']+rho*C['gamma_g'])/(1-rho))
    assert C['eps2']==eps
    assert C['all_word_residual_bound']==residual
    assert C['all_word_measurement_bound']==noise
    assert C['all_word_total_bound']==residual+noise
    assert len(records)==payload['records']==32
    assert sum(map(len,records))==payload['native_primitive_executions']==122
    assert payload['total_readings']==payload['records']+payload['calibration_standards']==34
    # Recompute exact block norms for the declared physical interpretation.
    n0=[F(3,5),0,F(4,5)];n1=[0,F(3,5),F(4,5)]
    inner=sum((a*b for a,b in zip(n0,n1)),F(0))
    assert inner==F(16,25)
    sources={}
    for p in [ROOT/'core/block_echo_compiler.py',ROOT/'core/run_block_experiment.py',ROOT/'results/BLOCK_EXPERIMENT.json']:
        sources[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    out={'scope':'Independent exact replay from decoded intervals of the new block/adjoint matrix witnesses; no shot execution or physical audit.',
         'source_hashes':sources,'residual_checks':checks,
         'all_common_contractions_verified':True,'row_column_noise_bounds_verified':True,
         'all_word_bound':str(residual+noise),'all_word_bound_float':float(residual+noise),
         'source_words':len(records),'standards':payload['calibration_standards'],'primitive_executions':sum(map(len,records)),
         'declared_block_operator_norm':str(inner),
         'quantum_shot_count_is_illustration_only':payload['quantum_interpretation_only']['assumed_IID_shots_not_executed']}
    Path(__file__).with_name('BLOCK_CERTIFICATE_REVIEW_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

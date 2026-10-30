from pathlib import Path
import sympy as S,json
root=Path(__file__).resolve().parents[1];out=root/'outputs/rotational_faces';out.mkdir(exist_ok=True)
raw=json.loads((root/'work/rotational_face_family.json').read_text());z=S.Symbol('z')
def pack(p):return [[pw[0],int(co.p),int(co.q)] for pw,co in S.Poly(S.sympify(p,locals={'z':z}),z).terms() if co]
cert={'cubic_powers':raw['cubic_powers'],'quartic_powers':raw['quartic_powers'],
 'cubic_matrix':[[pack(p) for p in row] for row in raw['cubic_matrix']],
 'quartic_matrix':[[pack(p) for p in row] for row in raw['quartic_matrix']],
 'translation_cubics':[[pack(p) for p in col] for col in raw['translation_cubics']],
 'F':[pack(p) for p in raw['F']],
 'exceptional_ranks':raw['exceptional_ranks'],
 'parameter_scope':'-1<z<1, z not equal to -1/3 or 1/3',
 'source_QC_primitive':'https://arxiv.org/html/2608.06367v1#A1.E4',
 'scope':'Full-space exposure, exact cubic rigidity and entire degree<=4 polynomial face classification. The leading quartic primitive is primary-source mathematics, replayed symbolically here.'}
for name in ('cubic_minor','quartic_minor','translation_minor'):
    cert[name]={'rows':raw[name]['rows'],'columns':raw[name]['columns'],'polynomial':pack(raw[name]['determinant'])}
(out/'certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
print('written',out/'certificate.json')

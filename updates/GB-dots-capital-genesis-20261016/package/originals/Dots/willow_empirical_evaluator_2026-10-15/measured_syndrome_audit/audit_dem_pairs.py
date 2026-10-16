import pathlib,re,json,hashlib
O=pathlib.Path(__file__).parent;D=(pathlib.Path(__file__).resolve().parent.parent / 'measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X/r50')
f=(pathlib.Path(__file__).resolve().parent.parent / 'measured_noise_independence/frozen_family.json');family=json.loads(f.read_text())['pairs']
coords=[]
for line in (D/'circuit_ideal.stim').read_text().splitlines():
 if line.startswith('DETECTOR('):coords.append(tuple(map(float,line.split('(')[1].split(')')[0].split(',')))[:3])
expected={(i,j) for i,a in enumerate(coords) for j,b in enumerate(coords) if a[:2]==b[:2] and 1<=a[2]<=49 and 1<=b[2]<=49 and 2<=b[2]-a[2]<=10}
assert len(expected)==9288 and {(p['d1'],p['d2']) for p in family}==expected
results={}
for label in ['si1000','rl_optimized']:
 path=D/f'decoding_results/correlated_matching_decoder_with_{label}_prior/error_model.dem';incident=[set() for _ in coords];modelcoords={};errors=0
 for line in path.read_text().splitlines():
  if line.startswith('error('):
   support=set()
   for word in line.split(') ',1)[1].split():
    if word=='^' or word.startswith('L'):continue
    assert re.fullmatch('D[0-9]+',word);d=int(word[1:])
    if d in support:support.remove(d)
    else:support.add(d)
   for d in support:incident[d].add(errors)
   errors+=1
  elif line.startswith('detector('):
   c,target=line.split(') ');modelcoords[int(target[1:])]=tuple(map(float,c.split('(')[1].split(',')))[:3]
  elif line.strip():raise ValueError(line)
 assert modelcoords==dict(enumerate(coords))
 overlaps=[len(incident[a]&incident[b]) for a,b in sorted(expected)]
 assert not any(overlaps)
 results[label]={'model_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'error_instructions':errors,'pairs':len(overlaps),'max_shared_mechanisms':max(overlaps),'coordinate_match':True}
(O/'independent_dem_pair_audit.json').write_text(json.dumps({'family_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'models':results},indent=2));print(results)

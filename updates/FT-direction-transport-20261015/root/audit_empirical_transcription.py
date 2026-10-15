from pathlib import Path
import json,hashlib,csv,importlib.util
R=Path(__file__).resolve().parents[1];p=R/'sources/closure/empirical_analysis.py';spec=importlib.util.spec_from_file_location('producer_empirical',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
items=[]
for key,name,md5 in [('CPA','fig2CPA(in-situ).csv','9024841d1f015c294ccaa52b89bc57ed'),('TMT','fig2TMT(in-situ).csv','99cce4f39f6fd0b6691b6e4bcb8f713d'),('Invisibility','fig2Invis(in-situ).csv','869fb11199cef5354f5d6bd7854531cc')]:
 f=R/'acquired/empirical'/name;b=f.read_bytes();assert hashlib.md5(b).hexdigest()==md5
 rows=list(csv.reader(b.decode().splitlines()));values=[float(x[1]) for x in rows[1:] if x];expected=m.DATA[key];assert len(values)==len(expected) and values==expected
 items.append(dict(objective=key,path=str(f.relative_to(R)),source_md5=md5,sha256=hashlib.sha256(b).hexdigest(),rows=len(values),all_transcribed_objective_values_equal=True,maximum_absolute_difference=0.,column=rows[0][1],source='Zenodo17314682v1 primary CSV'))
r=dict(status='PASS',scope='All110 producer-transcribed objective values match independently fetched raw third-party experimental CSVs exactly; this verifies transcription only, not new adjoint physics, noise calibration, causality or performance superiority.',files=items,source_script_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(R/'root/EMPIRICAL_TRANSCRIPTION_AUDIT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))

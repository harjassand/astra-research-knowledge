"""Preserve the Phase7 archive by content and add the complete Phase8 research."""
from pathlib import Path
import ast, hashlib, json, zipfile, sys

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'Astra_Retained_Memory_Parity_and_Repeated_Operations_20261101.zip'
BASE_SHA='1173f0342352c28859393ed11510085b0d5bbca849a14a5b547f578c768bf221'
OUT=ROOT/'Astra_Causal_Memory_Closure_and_Physical_Noise_Admission_20261101.zip'
MANIFEST=ROOT/'PHASE8_PRESERVATION.json'
REPORT=ROOT/'Astra_P8_Causal_Memory_and_Physical_Admission_Report_20261101.txt'

def digest(data):return hashlib.sha256(data).hexdigest()

def selected_files():
    return sorted([p for p in (ROOT/'phase8').rglob('*')
        if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ['.pyc','.pyo']]
        +[REPORT,ROOT/'PHASE8_START_HERE.txt'])

def main():
    if not BASE.exists():
        raise SystemExit('Place the unchanged Phase7 base archive next to the extracted Phase8 files to rebuild.')
    assert digest(BASE.read_bytes())==BASE_SHA
    files=selected_files();py_count=json_count=0
    for p in files:
        if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p));py_count+=1
        if p.suffix=='.json':json.loads(p.read_text());json_count+=1
    validation={'python_programs_parsed':py_count,'json_documents_parsed':json_count,
        'method':'Syntax/data validation plus the saved analytic and independent scientific checks. No unperformed experiment is inferred.'}
    validation_path=ROOT/'phase8/root/FINAL_VALIDATION.json'
    validation_path.write_text(json.dumps(validation,indent=2)+'\n')
    files=selected_files()
    with zipfile.ZipFile(BASE) as base:
        names=base.namelist()
        assert len(names)==337 and len(set(names))==337
        assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
        inherited={n:digest(base.read(n)) for n in names}
        new={p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in files}
        assert not set(inherited).intersection(new)
        manifest={'base_archive':BASE.name,'base_sha256':BASE_SHA,
            'inherited_entries':337,'inherited_content_sha256':inherited,
            'new_entries_excluding_manifest':len(new),'new_content_sha256':new,
            'manifest_self_hash_excluded':True,
            'preservation':'Every inherited entry is copied with byte-identical uncompressed contents. New caches/private transfer helpers excluded.'}
        MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n')
        with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as out:
            for info in base.infolist():out.writestr(info,base.read(info.filename))
            for p in files:out.write(p,p.relative_to(ROOT).as_posix())
            out.write(MANIFEST,MANIFEST.name)
    with zipfile.ZipFile(OUT) as out:
        assert out.testzip() is None
        assert len(out.namelist())==337+len(new)+1
        for n,h in inherited.items():assert digest(out.read(n))==h
        for n,h in new.items():assert digest(out.read(n))==h
        assert out.read(MANIFEST.name)==MANIFEST.read_bytes()
    result={'archive':str(OUT),'bytes':OUT.stat().st_size,'sha256':digest(OUT.read_bytes()),
        'inherited_entries_unchanged':337,'new_entries_including_manifest':len(new)+1,
        'total_entries':337+len(new)+1,'crc_check':'passed','content_hash_comparison':'passed',
        'validation':validation}
    (ROOT/'PHASE8_ARCHIVE_VERIFIED.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()

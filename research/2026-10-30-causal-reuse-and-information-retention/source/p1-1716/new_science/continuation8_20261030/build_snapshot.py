#!/usr/bin/env python3
"""Package this continuation and verify byte preservation of its predecessor.
This is an artifact-integrity check, not a scientific validation rerun.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime, timezone
import hashlib, json


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root=Path(__file__).resolve().parents[2]
    workspace=root.parent
    predecessor=workspace/'Astra_P1_Controlled_Transport_Action_20261029.zip'
    expected='9417699671e19c196831100b54eddd219ed6924ae959c62a7c31f2dfb9ac5705'
    assert digest(predecessor.read_bytes())==expected
    with ZipFile(predecessor) as old:
        names=[x.filename for x in old.infolist() if not x.is_dir()]
        assert len(names)==472
        for name in names:
            p=root/name
            assert p.is_file(), ('missing predecessor file',name)
            assert p.read_bytes()==old.read(name), ('changed predecessor file',name)
    inherited=set(names)
    manifest_name='EIGHTH_CONTINUATION_MANIFEST.json'
    files=[]
    for p in sorted(root.rglob('*')):
        if not p.is_file(): continue
        name=p.relative_to(root).as_posix()
        if name==manifest_name: continue
        if name not in inherited and ('__pycache__' in p.parts or p.suffix=='.pyc'):
            continue
        files.append(p)
    entries=[{'path':p.relative_to(root).as_posix(),'size_bytes':p.stat().st_size,
              'sha256':digest(p.read_bytes()),
              'preserved_predecessor':p.relative_to(root).as_posix() in inherited}
             for p in files]
    manifest={'created_utc':datetime.now(timezone.utc).isoformat(),
              'role':'Astra P1, same role and two existing complementary roles',
              'predecessor_archive':predecessor.name,
              'predecessor_sha256':expected,
              'predecessor_files_byte_identical':len(names),
              'total_archive_files':len(entries)+1,
              'new_archive_files':len(entries)+1-len(names),
              'manifest_self_hash_omitted':True,
              'entries':entries}
    manifest_path=root/manifest_name
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    files.append(manifest_path)
    destination=workspace/'Astra_P1_Designed_Transport_and_Event_Memory_20261030.zip'
    with ZipFile(destination,'w',compression=ZIP_DEFLATED,compresslevel=6) as out:
        for p in sorted(files): out.write(p,p.relative_to(root).as_posix())
    with ZipFile(destination) as out:
        assert out.testzip() is None
        assert len(out.namelist())==len(entries)+1
        with ZipFile(predecessor) as old:
            for name in names: assert out.read(name)==old.read(name)
        for e in entries: assert digest(out.read(e['path']))==e['sha256']
    print(json.dumps({'archive':str(destination),'size_bytes':destination.stat().st_size,
                      'sha256':digest(destination.read_bytes()),
                      'files':len(entries)+1,'unchanged_predecessor_files':len(names),
                      'new_files':len(entries)+1-len(names)},indent=2))


if __name__=='__main__': main()

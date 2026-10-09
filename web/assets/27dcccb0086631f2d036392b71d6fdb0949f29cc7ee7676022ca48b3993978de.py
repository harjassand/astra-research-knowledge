#!/usr/bin/env python3
"""Restore verified original paths from the ASTRA content-addressed checkpoint.
Standard-library only. A fresh destination directory is required.
"""
import argparse, hashlib, json, os, pathlib, shutil, stat, zipfile

def admitted(path, profile):
    if profile == 'all': return True
    if profile == 'sources': return path.startswith('work/sources/')
    if profile == 'research': return not path.startswith('work/sources/')
    if profile == 'handoff': return path.startswith('outputs/final-research-handoff/')
    if profile == 'square':
        # Include the entire non-cache agent tree, so inherited square premises
        # cannot be dropped merely because their directory has a generic name.
        return path.startswith(('work/agents/', 'work/state/', 'work/handoff/', 'outputs/'))
    return False

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive'); p.add_argument('destination')
    p.add_argument('--profile', choices=['handoff','square','research','sources','all'], default='handoff')
    p.add_argument('--path', action='append', default=[], help='Exact original path or directory prefix; overrides profile')
    p.add_argument('--allow-internal-symlinks', action='store_true')
    a=p.parse_args(); dst=pathlib.Path(a.destination).absolute()
    if dst.exists() and any(dst.iterdir()): raise SystemExit('Destination must be absent or empty.')
    dst.mkdir(parents=True,exist_ok=True)
    count=0; skipped=[]
    with zipfile.ZipFile(a.archive) as z:
        rows=[json.loads(x) for x in z.read('PATH_INDEX.jsonl').splitlines()]
        selected=[r for r in rows if (any(r['path']==x.rstrip('/') or r['path'].startswith(x.rstrip('/')+'/') for x in a.path) if a.path else admitted(r['path'], a.profile))]
        for r in selected:
            rel=pathlib.PurePosixPath(r['path'])
            if rel.is_absolute() or '..' in rel.parts: raise ValueError('Unsafe archive path')
            out=dst.joinpath(*rel.parts)
            if not out.resolve().is_relative_to(dst.resolve()): raise ValueError('Unsafe destination path')
            out.parent.mkdir(parents=True,exist_ok=True)
            if r['kind']=='symlink':
                target=r['target']
                safe=not os.path.isabs(target) and (out.parent/target).resolve().is_relative_to(dst.resolve())
                if a.allow_internal_symlinks and safe: out.symlink_to(target)
                else: skipped.append({'path':r['path'],'target':target})
                continue
            h=hashlib.sha256()
            with z.open('blobs/'+r['sha256']) as source, out.open('xb') as f:
                while block:=source.read(1024*1024): h.update(block); f.write(block)
            if h.hexdigest()!=r['sha256']: raise ValueError('Digest mismatch: '+r['path'])
            os.chmod(out, r['mode'] & 0o777)
            os.utime(out, ns=(r['mtime_ns'],r['mtime_ns']))
            count+=1
    receipt={'profile':a.profile,'paths':a.path,'files_restored_and_verified':count,'symlinks_not_restored':skipped}
    (dst/'RESTORE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__=='__main__': main()

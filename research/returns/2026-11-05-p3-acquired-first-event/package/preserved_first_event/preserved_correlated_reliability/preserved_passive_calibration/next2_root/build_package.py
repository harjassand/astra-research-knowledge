"""Assemble reproducible research files and preserve the previous package."""
from pathlib import Path
import hashlib, json, platform, shutil, sys, zipfile
import numpy, scipy, mpmath, matplotlib, PIL

root=Path(__file__).resolve().parent.parent
dest=root/'passive_calibration_package'
dest.mkdir(exist_ok=True)
for folder in ['next2_root','next2_continuous_quantum','next2_reliability','next2_alternatives']:
    shutil.copytree(root/folder,dest/folder,dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
shutil.copy2(root/'next2_root/README_FOR_PACKAGE.txt',dest/'README.txt')
shutil.copy2(root/'next2_root/SOURCE_REGISTER.txt',dest/'SOURCE_REGISTER.txt')
prior=root/'deferred_calibration_package'
old=dest/'preserved_deferred_calibration'
shutil.copytree(prior,old,dirs_exist_ok=True)
preserved=[]
for p in sorted(prior.rglob('*')):
    if p.is_file():
        q=old/p.relative_to(prior)
        assert p.read_bytes()==q.read_bytes(),str(p)
        preserved.append(str(p.relative_to(prior)))
assert len(preserved)==47
report=root/'output/pdf/Astra_Passive_Hamiltonian_Calibration.pdf'
shutil.copy2(root/'output/pdf/passive_calibration_report.pdf',report)
shutil.copy2(report,dest/report.name)
# Resolve a source-navigation path in NEW files only. Preserved files are untouched.
newnote=dest/'next2_reliability/CALIBRATION_AND_PHYSICAL_SCOPE.md'
s=newnote.read_text()
s=s.replace('../next_rare_interventions/COMPLETED_RESULTS.txt',
 '../preserved_deferred_calibration/independent_routes/reliability/COMPLETED_RESULTS.txt')
newnote.write_text(s)
env={'python':sys.version,'platform':platform.platform(),'numpy':numpy.__version__,
     'scipy':scipy.__version__,'mpmath':mpmath.__version__,
     'matplotlib':matplotlib.__version__,'pillow':PIL.__version__,
     'evidence':'Synthetic model simulations and mathematical constructions, not laboratory data.'}
(dest/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
(dest/'PRESERVATION_RECEIPT.json').write_text(json.dumps({
 'prior_file_count':len(preserved),'comparison':'Exact byte equality for every prior file',
 'paths':preserved},indent=2)+'\n')
manifest=[]
for p in sorted(dest.rglob('*')):
    if p.is_file() and p!=dest/'SHA256SUMS.txt':
        manifest.append(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(dest)))
(dest/'SHA256SUMS.txt').write_text('\n'.join(manifest)+'\n')
archive=root/'output/Astra_Passive_Calibration_Research_Package.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(dest.rglob('*')):
        if p.is_file():z.write(p,Path(dest.name)/p.relative_to(dest))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps({'files':len(manifest)+1,'prior_files_preserved':len(preserved),
 'report':str(report),'report_bytes':report.stat().st_size,
 'archive':str(archive),'archive_bytes':archive.stat().st_size,
 'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),
 'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()},indent=2))

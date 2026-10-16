"""Hash retained artifacts and record source locations. Does not access the network."""
from pathlib import Path
import json,hashlib
p=Path(__file__).parent
ware='https://raw.githubusercontent.com/matthewware/RGST-analysis/9afedca174dbcb14d52c245cf7504a834816fc39/'
qgl='https://raw.githubusercontent.com/BBN-Q/QGL.jl/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/'
pygst='https://raw.githubusercontent.com/pyGSTio/pyGSTi/v0.9.3/'
edd=json.loads((p/'source/download_urls.json').read_text())
extract=json.loads((p/'edd_subset/extraction_manifest.json').read_text())
archive_members={Path(m).name:m for m in extract['selected_members']}
files=[]
for f in sorted(p.rglob('*')):
 if not f.is_file() or f.name=='provenance.json':continue
 rel=f.relative_to(p).as_posix();entry={'path':rel,'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'kind':'newly authored or derived artifact'}
 if rel.startswith('rgst/'):
  entry.update(kind='unaltered upstream file',source_url=ware+rel[5:],license='Apache-2.0')
 elif rel.startswith('qgl_source/') and f.suffix!='.csv':
  entry.update(kind='unaltered upstream file',source_url=qgl+rel[len('qgl_source/'):],license='Apache-2.0')
 elif rel.startswith('edd_subset/') and f.name in archive_members:
  entry.update(kind='unaltered archive member',source_url=extract['archive_url'],archive_member=archive_members[f.name],archive_sha256=extract['archive_sha256'],license='Apache-2.0')
 elif rel.startswith('source/') and f.name in edd:
  entry.update(kind='unaltered upstream file',source_url=edd[f.name],license='Apache-2.0')
 elif f.name.startswith('pygsti_v093_'):
  x=f.name[len('pygsti_v093_'):]
  x=x[:-4] if x.endswith('.py.txt') else x
  source='license.txt' if x=='license.txt' else 'packages/pygsti/construction/'+x
  entry.update(kind='unaltered upstream file',source_url=pygst+source,license='GPL-3.0-or-later')
 elif f.name=='GPL-3.0-or-later.txt':
  entry.update(kind='license text',source_url='https://raw.githubusercontent.com/spdx/license-list-data/main/text/GPL-3.0-or-later.txt')
 elif f.name=='Randomize_notebook_text.txt':
  entry.update(kind='notebook cell sources concatenated as plain text',derived_from='rgst/notebooks/Randomize.ipynb',source_url=ware+'notebooks/Randomize.ipynb',license='Apache-2.0')
 elif f.name=='submit_HaarDelayArmonk.txt':
  entry.update(kind='notebook cell sources concatenated as plain text',derived_from='edd_subset/submit_HaarDelayArmonk.ipynb',source_url=extract['archive_url'],license='Apache-2.0')
 elif f.name=='rgst_repository_tree.json':
  entry.update(kind='GitHub API tree metadata',source_url='https://api.github.com/repos/matthewware/RGST-analysis/git/trees/9afedca174dbcb14d52c245cf7504a834816fc39?recursive=1')
 elif f.name=='qgl_current_tree.json':
  entry.update(kind='GitHub API tree metadata',source_url='https://api.github.com/repos/BBN-Q/QGL.jl/git/trees/70e66d76f2e5f518ff2d8b78bc93b65779182c9f?recursive=1')
 files.append(entry)
result={'retrieved_date_utc':'2026-10-15','method':'Public read-only HTTPS; raw text/JSON/zip members; no author code executed or installed. Original clocks/mtimes not used as scientific timestamps.','primary_dataset_release':'https://zenodo.org/records/4609459','primary_data_repository_commit':'9afedca174dbcb14d52c245cf7504a834816fc39','additional_edd_archive':extract,'files':files}
(p/'provenance.json').write_text(json.dumps(result,indent=2))
print(len(files),'retained files;',sum(x['bytes'] for x in files),'bytes excluding this manifest')

"""Run the unchanged detyping enumeration without requiring omitted source copies.
Only the source-copy statement is guarded; every mathematical assertion is unchanged.
Primary source version/hashes remain in the original report and source ledger.
This replay does not reacquire or independently validate that primary source.
"""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"agents/detyping_blind/enumerate_game.py"
s=p.read_text()
old="        shutil.copyfile(source_dir / filename, SOURCES / filename)"
new="        if (source_dir / filename).is_file():\n            shutil.copyfile(source_dir / filename, SOURCES / filename)"
assert s.count(old)==1, "Expected archival-copy statement changed; re-audit adapter."
s=s.replace(old,new)
exec(compile(s,str(p),"exec"),{"__name__":"__main__","__file__":str(p)})
print("Portable replay: omitted third-party source copying was optional; mathematical enumeration unchanged.")

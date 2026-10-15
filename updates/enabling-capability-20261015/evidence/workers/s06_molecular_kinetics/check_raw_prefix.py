"""Check acquired raw coordinate frames against the compact reference labels."""
from pathlib import Path
import json
import argparse
import time
import numpy as np
import mdtraj as md
from scipy.special import expit
from replay_kinetics import load_reference

p = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--frames",type=int,default=10000)
args = parser.parse_args()
raw = p / "acquired/data/chignolin/equilibrium/run0.xtc"
complete = raw.exists()
if not complete:
    raw = raw.with_suffix(".xtc.partial")
started = time.perf_counter()
with md.formats.XTCTrajectoryFile(str(raw)) as f:
    xyz, times, steps, box = f.read(n_frames=args.frames)
top = md.load_pdb(str(p / "acquired/data/chignolin/mol.pdb")).topology
traj = md.Trajectory(xyz, top, time=times)
traj.unitcell_vectors = box
pairs = np.load(p / "acquired/data/chignolin/signature.npy")
r0 = np.load(p / "acquired/data/chignolin/r0.npy")
dist = md.compute_distances(traj, pairs, periodic=True)
q = np.mean(expit(-50*(dist-1.8*r0)), axis=1)
states = np.full(len(q), "R")
states[q >= .99] = "A"
states[q <= .01] = "B"
# New dataset run0 is old dataset equilibrium1; archive byte sizes confirm map.
reference = load_reference()[1]["states"][:len(states)]
assert len(states) == args.frames, "Coordinate prefix is shorter than requested"
assert np.array_equal(reference,states), "Raw coordinates disagree with supplied state labels"
assert float(np.median(np.diff(times))) == 100.0, "Physical frame spacing differs from source setting"
unique, counts = np.unique(states,return_counts=True)
result = {"scope": f"First {len(states)} coordinate frames only; all remaining compact labels remain source-derived.",
          "raw_complete_archive_entry_crc_verified": complete,
          "frames":len(states),"atoms":xyz.shape[1],"contacts":len(pairs),
          "frame_dt_ps":float(np.median(np.diff(times))),
          "time_interval_ps":[float(times[0]),float(times[-1])],
          "states":dict(zip(unique.tolist(),counts.tolist())),
          "mismatches":int(np.sum(reference!=states)),
          "first_mismatch_frames":np.flatnonzero(reference!=states)[:30].tolist(),
          "compute_seconds":time.perf_counter()-started}
(p / "RAW_PREFIX_CHECK.json").write_text(json.dumps(result,indent=2))
(p / f"RAW_PREFIX_CHECK_{len(states)}.json").write_text(json.dumps(result,indent=2))
np.savez_compressed(p / f"raw_prefix_{len(states)}frames.npz",Q=q,states=states,time_ps=times)

# Save actual atomistic transitions for pathway-level follow-up. Two distances
# are published visualization coordinates; they are not by themselves a proven
# classification of all molecular mechanisms.
from replay_kinetics import skeleton
arrivals,basins=skeleton(states)
cv_pairs=np.array([[top.select("resid 2 and name O")[0],top.select("resid 6 and name CA")[0]],
                   [top.select("resid 1 and name CA")[0],top.select("resid 7 and name O")[0]]])
cvs=md.compute_distances(traj,cv_pairs,periodic=True)
paths=[]
for j in range(1,len(arrivals)):
    end=arrivals[j]
    previous=basins[j-1]
    begin=np.flatnonzero(states[:end]==previous)[-1]
    name=f"transition_{j:02d}_{previous}_to_{basins[j]}"
    np.savez_compressed(p/(name+".npz"),xyz_nm=xyz[begin:end+1],
                        time_ps=times[begin:end+1],Q=q[begin:end+1],
                        d37_d28_nm=cvs[begin:end+1],atom_pairs=cv_pairs)
    paths.append({"file":name+".npz","from":previous,"to":basins[j],
                  "start_frame":int(begin),"end_frame":int(end),
                  "duration_ns":float((times[end]-times[begin])/1000),
                  "d37_d28_start_nm":cvs[begin].tolist(),
                  "d37_d28_end_nm":cvs[end].tolist(),
                  "scope":"Observed transition in supplied atomistic MD; no complete mechanism classification or experimental validation."})
(p/"ACQUIRED_ATOMISTIC_PATHS.json").write_text(json.dumps(paths,indent=2))
print(json.dumps(result,indent=2))
print(json.dumps(paths,indent=2))

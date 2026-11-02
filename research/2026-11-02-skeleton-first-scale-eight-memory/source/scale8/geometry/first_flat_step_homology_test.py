"""Topological first-step reduced mapping-cylinder realization of actual seed boundary colors.
Uses the specified abstract hashtag cylinder, with source-compatible boundary incidence.
Not a full raw-coordinate gadget atlas or weight-preserving map certificate.
"""
import contextlib,io,json
with contextlib.redirect_stdout(io.StringIO()):
 from flat_parent_face_fiber_test import faces,inc
from sheaf_incidence_compiler import compile_sheaf
colors={}
for e,fs in inc.items():
 if len(fs)==2:continue
 a,b=e
 # Outer y boundaries are blue, x boundaries red (seed opposite sides).
 if a[1]==b[1] and a[1] in [0,3]:color='blue'
 elif a[0]==b[0] and a[0] in [0,3]:color='red'
 else:color='blue'
 colors[e]=color
r=compile_sheaf(faces,colors,True)
print(json.dumps(dict(scope=__doc__,**r),indent=2))

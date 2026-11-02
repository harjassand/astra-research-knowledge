from pathlib import Path
import subprocess,sys,os
ROOT=Path(__file__).resolve().parent
SCRIPTS=['geometry/central_cube_certificate.py', 'geometry/full_cube_edge_test.py', 'geometry/t_star_joint_certificate.py', 'geometry/t_subcomplex_certificate.py', 'geometry/two_rib_transfer_certificate.py', 'geometry/degree4_packet_projection.py', 'geometry/aligned_tree_basis_test.py', 'geometry/packet_matching_certificate.py', 'geometry/flat_parent_face_fiber_test.py', 'geometry/flat_red_face_fiber_test.py', 'geometry/flat_fiber_boundary_projection.py', 'geometry/flat_fiber_flow_metric.py', 'geometry/first_flat_step_homology_test.py', 'geometry/first_red_step_projection_test.py', 'geometry/recursive_t_polygon_certificate.py', 'geometry/parent_face_subdivision_certificate.py', 'geometry/rep4_aux_packet_test.py', 'geometry/root_product_syndrome_check.py', 'geometry/edge_fiber_template_test.py', 'cochains/boxed_relative_certificate.py', 'cochains/red_seed_projection_test.py', 'duality/verify_torus.py', 'duality/audit_checks.py', 'duality/audit_trace_prepass.py']
env=os.environ.copy();env['PYTHONPATH']=os.pathsep.join(str(ROOT/x) for x in ['replay_site','geometry','cochains','duality'])
(ROOT/'replay_logs').mkdir(exist_ok=True)
for rel in SCRIPTS:
 p=ROOT/rel;r=subprocess.run([sys.executable,str(p)],cwd=p.parent,env=env,text=True,capture_output=True)
 (ROOT/'replay_logs'/(rel.replace('/','__')+'.txt')).write_text(r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(rel+'\n'+r.stderr)
 print(rel,'CLEAN_COPY_PASS',flush=True)
print(len(SCRIPTS),'CHECKS_PASS',flush=True)

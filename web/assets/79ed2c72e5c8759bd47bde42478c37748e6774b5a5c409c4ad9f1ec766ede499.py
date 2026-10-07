"""Read-only research snapshot. No worker files changed; per-file capture times."""
from pathlib import Path
import datetime, hashlib, json, zipfile, shutil

root = Path(__file__).resolve().parents[3]
out = root / 'outputs/round6'
now = datetime.datetime.now(datetime.timezone.utc)
selected = {
    'EXACT_FULL_SEPARABILITY.txt': 'c04_s01/revisions/EXACT_FULL_SEPARABILITY.txt',
    'FULL_RANK_STOPPING.txt': 'c04_s01/revisions/FULL_RANK_STOPPING.txt',
    'INDEPENDENT_QUDIT_PROOF.txt': 'c04_s02/revisions/QUDIT_POSITIVITY_LOCALIZATION.txt',
    'HIGHER_SPIN_EXACT_SEPARABILITY.txt': 'c05_s02/revisions/EXACT_FULL_SEPARABILITY.txt',
    'LOW_PARTICLE_COUNT_SAMPLE_PROOF.txt': 'c03_s02/audit_c03_l10/AUDIT_REPORT.txt',
    'AXIAL_UNIFORM_SEPARABILITY.txt': 'c07_s02/phase2/AXIAL_UNIFORM_SEPARABILITY.txt',
    'AXIAL_HALF_EXTENSION.txt': 'c07_s02/phase2/AXIAL_HALF_EXTENSION.txt',
    'AXIAL_ONE_CERTIFICATE.txt': 'c07_s02/phase2/AXIAL_ONE_CERTIFICATE.txt',
    'AXIAL_ONE_INDEPENDENT_AUDIT.txt': 'c05_s03/revisions/11_axial_one_fresh_math_and_code_audit.txt',
    'INDEPENDENT_DELTA1_CERTIFICATE_VERIFY.json': 'c02_s01/axial/INDEPENDENT_DELTA1_CERTIFICATE_VERIFY.json',
    'AXIAL_FIVE_FOURTHS_JOIN.txt': 'c07_s02/phase2/AXIAL_FIVE_FOURTHS_JOIN.txt',
    'AXIAL_FIVE_FOURTHS_ANALYTIC_PROOF.txt': 'c05_s03/revisions/12_axial_five_fourths_analytic_tail.txt',
    'AXIAL_FIVE_FOURTHS_INDEPENDENT_AUDIT.txt': 'c05_s03/revisions/13_axial_five_fourths_joined_certificate.txt',
    'OPTIMAL_JOIN.txt': 'c07_s02/phase2/OPTIMAL_JOIN.txt',
    'OPTIMAL_ANALYTIC_TAIL.txt': 'c07_s02/phase2/OPTIMAL_ANALYTIC_TAIL.txt',
    'OPTIMAL_AUDIT_CLOSED.json': 'c07_s02/phase2/OPTIMAL_AUDIT_CLOSED.json',
    'OPTIMAL_FULL_INDEPENDENT_AUDIT.txt': 'c05_s03/revisions/18_optimal_uniform_axial_joined_certificate.txt',
    'OPTIMAL_FINITE_INDEPENDENT_AUDIT.txt': 'c05_s03/revisions/17_optimal_endpoint_independent_finite_prefix_audit.txt',
    'OPTIMAL_INDEPENDENT_VERIFICATION.json': 'c05_s03/revisions/optimal_prefix_independent_complete_manifest_check.json',
    'OPTIMAL_THIRD_ANALYTIC_AUDIT.txt': 'c07_s01/revisions/AXIAL_OPTIMAL_ANALYTIC_FRESH_AUDIT.txt',
    'NEGATIVE_AXIAL_COROLLARY.txt': 'c07_s02/phase2/NEGATIVE_AXIAL_COROLLARY.txt',
    'QUANTITATIVE_VERTICAL_GAP.txt': 'c07_s02/phase2/QUANTITATIVE_VERTICAL_GAP.txt',
    'NEWTON_EXPLOSIVE_BIRTH_LEMMA.txt': 'c05_s03/revisions/14_newton_explosive_birth_checked_lemma.txt',
    'AXIAL_FINITE_BIT_COMPILER.txt': 'c01_s03/axial_compiler/AXIAL_FINITE_BIT_COMPILER.txt',
    'REUSABLE_ZERO_FIELD_COMPILER.txt': 'c01_s03/axial_compiler/REUSABLE_ZERO_FIELD_COMPILER.txt',
    'DICKE_QUADRATURE_BIT_COMPLEXITY.txt': 'c02_s03/quadrature/BIT_COMPLEXITY_PROOF.txt',
    'DICKE_FINITE_PREFIX_COMPONENT.txt': 'c02_s03/quadrature/FINITE_PREFIX_COMPONENT.txt',
    'DIRECT_FILTERED_COMPILER.txt': 'c01_s03/axial_compiler/DIRECT_FILTERED_COMPILER.txt',
    'OPTIMAL_DOMAIN_COMPILER.txt': 'c01_s03/axial_compiler/OPTIMAL_DOMAIN_COROLLARY.txt',
    'WHOLE_AXIAL_COMPILER_AUDIT.txt': 'c08_s03/revisions/axial_compiler_audit/WHOLE_AXIAL_AUDIT.txt',
    'DIRECT_FILTERED_COMPILER_AUDIT.txt': 'c08_s03/revisions/axial_compiler_audit/DIRECT_FILTERED_AUDIT.txt',
    'IMPLEMENTATION_POSTERIOR_AUDIT.txt': 'c02_s01/axial/algorithm_review/IMPLEMENTATION_POSTERIOR_AUDIT.txt',
    'FILTERED_N32_N64_VERIFY.json': 'c02_s01/axial/filtered_review/FILTERED_N32_N64_VERIFY.json',
    'SAMPLER_REPLAY_README.txt': 'c03_s01/implementation/README.txt',
    'N64_BUDGET_OVERRUN.json': 'c03_s01/implementation/SCALING_BUDGET_OVERRUN_04.json',
    'LUNA_N72_COUNTEREXAMPLE.txt': 'c07_l02/revisions/AXIAL_HANKEL_N72_COUNTEREXAMPLE.txt',
    'LUNA_N72_FRESH_AUDIT.txt': 'c07_s01/revisions/LUNA_N72_COUNTEREXAMPLE_FRESH_AUDIT.txt',
    'PHASE_MODULUS_COUNTEREXAMPLE.json': 'c02_s01/axial/algorithm_review/PHASE_MODULUS_COUNTEREXAMPLE.json',
    'AXIAL_HALF_INDEPENDENT_AUDIT.txt': 'c05_s03/revisions/08_axial_half_fresh_audit.txt',
    'BERNSTEIN_COMPLETION_PRINCIPLE.txt': 'c07_s02/phase2/BERNSTEIN_COMPLETION_PRINCIPLE.txt',
    'AXIAL_EXACT_SIX_QUBIT_COUNTER.txt': 'c05_s03/revisions/05_axial_exact_six_qubit_counter.txt',
    'FIXED_VARIABLE_ORACLE_COMPILER.txt': 'c01_s01/spin_bridge/FIXED_VARIABLE_ORACLE_COMPILER.txt',
    'IID_ORACLE_RECOVERY_AUDIT.txt': 'c07_s01/revisions/IID_ORACLE_RECOVERY_AUDIT.txt',
    'SYMMETRY_COMPRESSED_WHITE_REPAIR.txt': 'c01_s01/spin_bridge/SYMMETRY_COMPRESSED_WHITE_REPAIR.txt',
    'SYMMETRIC_CORRECTION_AUDIT.txt': 'c08_s03/revisions/separability_fallback/SYMMETRIC_CORRECTION_AUDIT.txt',
    'MULTISPECIES_EXACT_SEPARABILITY.txt': 'c04_s03/revisions/phase2/MULTISPECIES_EXACT_SEPARABILITY.txt',
    'MULTISPECIES_INDEPENDENT_AUDIT.txt': 'c05_s01/revisions/06_multispecies_exact_audit.txt',
    'UNIFORM_ANISOTROPY_LITERATURE_AUDIT.txt': 'c07_l03/revisions/UNIFORM_ANISOTROPY_LITERATURE_AUDIT.txt',
    'CLASSICALITY_COMPILER_PRIORITY.md': 'c07_l01/revisions/CLASSICALITY_COMPILER_PRIORITY.md',
    'LUNA_COMPARISON_LEDGER.txt': 'c01_l01/revisions/LUNA_COMPARISON_LEDGER.txt',
    'LUNA_COMPARISON_LEDGER.json': 'c01_l01/revisions/LUNA_COMPARISON_LEDGER.json',
    'OPTIMAL_DOMAIN_COMPILER_AUDIT.txt': 'c08_s03/revisions/axial_compiler_audit/OPTIMAL_DOMAIN_AUDIT.txt',
    'FILTERED_SAMPLER_REPLAY.json': 'c02_s01/axial/filtered_review/OWNED_FILTERED_SAMPLER_REPLAY.json',
    'FILTERED_NEGATIVE_CONTROLS.json': 'c02_s01/axial/filtered_review/FILTERED_NEGATIVE_CONTROLS.json',
    'SCALING_SECOND_SCALAR_VERIFY.json': 'c01_s03/axial_compiler/scaling_model_checks.json',
    'FAST_SCALAR_ENCLOSURE.txt': 'c01_s03/axial_compiler/FAST_SCALAR_ENCLOSURE.txt',
    'AXIAL_SPIN_TRANSFER.txt': 'c05_s02/phase3_axial/AXIAL_SPIN_TRANSFER.txt',
    'PROJECTION_DP_COMPILER.txt': 'c05_s02/phase3_axial/PROJECTION_DP_COMPILER.txt',
    'COMPRESSED_POSTERIOR_AUDIT.txt': 'c02_s01/axial/filtered_review/COMPRESSED_POSTERIOR_AUDIT.txt',
    'FILTERED_FINAL_ALL4_VERIFY.json': 'c02_s01/axial/filtered_review/FILTERED_FINAL_ALL4_VERIFY.json',
    'FILTERED_FINAL_MANIFEST.json': 'c02_s01/axial/filtered_review/FINAL_CHECKS_MANIFEST.json',
    'PI_PRODUCT_MEASUREMENT_COMPARATOR.md': 'c07_l01/revisions/PI_PRODUCT_MEASUREMENT_COMPARATOR.md',
    'UNIVERSAL_REGULARIZED_COMPILER.txt': 'c02_s03/quadrature/regularization/UNIVERSAL_REGULARIZED_COMPILER.txt',
    'REGULARIZED_OPTIMAL_DOMAIN.txt': 'c02_s03/quadrature/regularization/OPTIMAL_DOMAIN_EXTENSION.txt',
    'REGULARIZED_SIGNED_DOMAIN.txt': 'c02_s03/quadrature/regularization/SIGNED_DOMAIN_COMPOSITION.txt',
    'REGULARIZED_ATOMIC_FIXTURES.json': 'c02_s03/quadrature/regularization/atomic_fixture.json',
    'PROMISED_DICKE_COMPILER_PRIORITY.txt': 'c07_l03/revisions/PROMISED_DICKE_SEP_COMPILER_PRIORITY_ADDENDUM.txt',
    'SPIN_PROJECTION_DP_FRESH_AUDIT.txt': 'c07_s01/revisions/SPIN_PROJECTION_DP_FRESH_AUDIT.txt',
    'SPIN_SIGNED_COMPILER_COMPOSITION.txt': 'c05_s02/phase3_axial/ALL_SIGNED_COMPOSITION.txt',
    'ELEMENTARY_COMPILER_COMPOSITION.txt': 'control/ELEMENTARY_COMPILER_COMPOSITION.txt',
    'COLLECTIVE_DECAY_ENTANGLEMENT.txt': 'c07_s02/phase2/COLLECTIVE_DECAY_ENTANGLEMENT.txt',
    'COLLECTIVE_DECAY_FRESH_AUDIT.txt': 'c05_s03/revisions/19_collective_decay_fresh_proof_audit.txt',
    'COLLECTIVE_ZERO_T_AUDIT_CLOSED.json': 'c05_s03/COLLECTIVE_ZERO_T_AUDIT_CLOSED.json',
    'COLLECTIVE_DARK_SECTOR_PRIORITY.txt': 'c07_l03/revisions/COLLECTIVE_DARK_SECTOR_PRIORITY_AUDIT.txt',
    'THERMAL_COLLECTIVE_BATH_PRIORITY.txt': 'c07_l03/revisions/THERMAL_COLLECTIVE_BATH_PRIORITY_AUDIT.txt',
    'UNIVERSAL_REGULARIZATION_AUDIT.txt': 'c08_s03/revisions/regularization_audit/REGULARIZATION_AUDIT.txt',
    'UNIVERSAL_REGULARIZATION_END.json': 'c08_s03/revisions/regularization_audit/END.json',
    'COLLECTIVE_THERMAL_BATH_ENTANGLEMENT.txt': 'c07_s02/phase2/COLLECTIVE_THERMAL_BATH_ENTANGLEMENT.txt',
    'COLLECTIVE_THERMAL_FRESH_AUDIT.txt': 'c05_s03/revisions/20_collective_thermal_bath_fresh_audit.txt',
    'COLLECTIVE_THERMAL_AUDIT_CLOSED.json': 'c05_s03/COLLECTIVE_THERMAL_AUDIT_CLOSED.json',
    'STATIONARY_DEPTH_TWO_FRESH_AUDIT.txt': 'c05_s03/revisions/21_stationary_collective_bath_depth_two_audit.txt',
    'STATIONARY_DEPTH_AUDIT_CLOSED.json': 'c05_s03/COLLECTIVE_STATIONARY_DEPTH_AUDIT_CLOSED.json',
    'SCHUR_CENTRAL_EXACT_DEPTH.txt': 'c04_s02/revisions/SCHUR_CENTRAL_EXACT_DEPTH.txt',
    'SCHUR_FILTER_ENVELOPE_AND_PRIORITY.txt': 'c04_s02/revisions/SCHUR_FILTER_ENVELOPE_AND_PRIORITY_ADDENDUM.txt',
    'SCHUR_DEPTH_INDEPENDENT_PROOF.txt': 'c04_s03/revisions/representation/CENTRAL_SCHUR_DEPTH.txt',
    'PI_THERMAL_CENTRAL_PRIOR_ART.txt': 'c07_l04/revisions/PI_THERMAL_AND_CENTRAL_WERNER_PRIOR_ART.txt',
    'REGULARIZATION_FINAL_RECEIPT.json': 'c02_s03/quadrature/regularization/REGULARIZATION_END.json',
    'COMPILED_N64_ONSET_NOTE.txt': 'c02_s01/axial/downstream/COMPILED_N64_ONSET_NOTE.txt',
    'COMPILED_N64_ONSET_CERTIFICATE.json': 'c02_s01/axial/downstream/COMPILED_N64_ONSET_CERTIFICATE.json',
    'COMPILED_N64_MEASUREMENT_INTERFACE.json': 'c02_s01/axial/downstream/CONDITIONAL_MEASUREMENT_INTERFACE.json',
    'SCHUR_FINAL_RECEIPT.json': 'c04_s02/revisions/SCHUR_CENTRAL_FINAL.json',
    'SCHUR_THERMALIZER_SCOPE.txt': 'c04_s02/revisions/SCHUR_THERMALIZER_SCOPE_ADDENDUM.txt',
    'THERMAL_DICKE_PRESERVATION_PRIORITY.txt': 'c07_l03/revisions/THERMAL_DICKE_SEPARABILITY_PRIORITY_ADDENDUM.txt',
    'SYMMETRIC_BIRTH_DEATH_SEP_PRESERVATION.txt': 'c07_s02/phase2/SYMMETRIC_BIRTH_DEATH_SEP_PRESERVATION.txt',
    'COLLECTIVE_PAIR_REPRESENTATION.txt': 'c07_s02/phase2/COLLECTIVE_STATIONARY_PAIR_REPRESENTATION.txt',
    'ALL_TIME_THERMAL_DEPTH_AUDIT.txt': 'c08_s03/revisions/thermal_depth_audit/THERMAL_DEPTH_AUDIT.txt',
    'ELEMENTARY_COMPOSITION_AUDIT.txt': 'c08_s03/revisions/thermal_depth_audit/ELEMENTARY_COMPOSITION_AUDIT.txt',
    'STATIONARY_TWO_PRODUCIBLE.txt': 'c04_s03/revisions/representation/STATIONARY_TWO_PRODUCIBLE.txt',
    'ALL_TIME_THERMAL_END.json': 'c08_s03/revisions/thermal_depth_audit/END.json',
    'STATIONARY_SAMPLER_INTERFACE_AUDIT.txt': 'c05_s03/revisions/22_stationary_finite_bit_sampler_interface_audit.txt',
    'STATIONARY_SAMPLER_CHECKS.json': 'c04_s03/revisions/representation/charged_qubit_sampler_check.json',
    'SCHUR_CORE_FINITE_BIT_COMPILER.txt': 'c01_s01/central_bridge/CORE_SUPPLIED_WEIGHTS.txt',
    'SCHUR_CORE_WORDING_ADDENDUM.txt': 'c01_s01/central_bridge/CORE_WORDING_ADDENDUM.txt',
    'SCHUR_FILTERED_FINITE_BIT_DRAFT.txt': 'c01_s01/central_bridge/FILTERED_SUPPLIED_RATIONAL_G_DRAFT.txt',
    'COLLECTIVE_FOLLOWON_FINAL.txt': 'c07_s02/phase2/COLLECTIVE_FOLLOWON_FINAL.txt',
    'COLLECTIVE_AUDIT_CLOSED.json': 'c07_s02/phase2/COLLECTIVE_AUDIT_CLOSED.json',
    'STATIONARY_SAMPLER_AUDIT_CLOSED.json': 'c05_s03/STATIONARY_SAMPLER_INTERFACE_AUDIT_CLOSED.json',
    'SCHUR_FILTERED_AUDIT_ADDENDUM.txt': 'c01_s01/central_bridge/FILTERED_AUDIT_ADDENDUM.txt',
    'SCHUR_ACCURACY_ENCODING_ADDENDUM.txt': 'c01_s01/central_bridge/ACCURACY_ENCODING_ADDENDUM.txt',
    'SCHUR_GIBBS_WEIGHT_ACQUISITION.txt': 'c01_s01/central_bridge/OPTIONAL_CENTRAL_GIBBS_WEIGHT_ACQUISITION.txt',
    'SCHUR_FINITE_BIT_FINAL_AUDIT.txt': 'c04_s02/reviews/CENTRAL_FINITE_BIT_FINAL_AUDIT.txt',
    'SCHUR_FINITE_BIT_AUDIT_RECEIPT.json': 'c04_s02/reviews/CENTRAL_FINITE_BIT_FINAL_AUDIT.json',
    'SCHUR_COMPILER_FINAL.txt': 'c01_s01/central_bridge/REPORT.txt',
    'SCHUR_COMPILER_FROZEN_MANIFEST.json': 'c01_s01/central_bridge/FROZEN_MANIFEST.json',
    'ROOT_RESEARCH.txt': 'control/ROOT_RESEARCH.txt',
    'FILTERED_SECTOR_POSTERIOR.txt': 'control/FILTERED_SECTOR_POSTERIOR.txt',
}
for name, relative in selected.items():
    src = root / 'work/cycle6' / relative
    if src.exists():
        shutil.copy2(src, out / name)

manifest = {'snapshot_started_utc': now.isoformat(),
            'atomic_across_files': False,
            'scope': 'Round 6 research artifacts only. Excludes caches; each file copied as captured.',
            'files': []}
# Preserve downloaded manuscripts locally, with hashes and source-acquisition
# records in the shareable packet, rather than redistributing their full text.
external_text_roots = {
    'work/cycle6/c05_s01/sources',
    'work/cycle6/c08_l03/sources',
    'work/cycle6/c08_s02/sources',
    'work/cycle6/c09_s01/phase2_sources',
    'work/cycle6/c09_s01/priority_schur_20261008/sources',
}
external_tex = {
    'work/cycle6/c09_s01/06-matrices.tex',
    'work/cycle6/c09_s01/glyph-mappings.tex',
    'work/cycle6/c09_s01/03-critical.tex',
    'work/cycle6/c09_s01/main.tex',
    'work/cycle6/c09_s01/07-observations.tex',
    'work/cycle6/c09_s01/02-calculus.tex',
    'work/cycle6/c09_s02/reviews/family093_observations.tex',
}
def external_manuscript(p):
    rel = p.relative_to(root).as_posix()
    return (p.suffix.lower() == '.pdf' or rel in external_tex or
            (p.parent.relative_to(root).as_posix() in external_text_roots and
             p.suffix.lower() in {'.txt', '.html', '.htm', '.png'}))
omissions = []
for p in (root / 'work/cycle6').rglob('*'):
    if p.is_file() and not p.is_symlink() and external_manuscript(p):
        data = p.read_bytes()
        omissions.append({'path': p.relative_to(root).as_posix(),
                          'bytes': len(data),
                          'sha256': hashlib.sha256(data).hexdigest(),
                          'retained_locally': True})
(out / 'SOURCE_OMISSIONS.json').write_text(json.dumps({
    'reason': 'Third-party full manuscripts remain local. Source URLs/acquisition records and exact hashes are retained in the research packet.',
    'files': omissions}, indent=2)+'\n')
archive = out / 'ROUND6_EVIDENCE.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    paths = list((root / 'work/cycle6').rglob('*'))
    paths += [p for p in out.rglob('*') if p.is_file() and p.suffix in ('.json', '.txt', '.md')
              and p not in {out / 'SNAPSHOT_MANIFEST.json', out / 'ARCHIVE_VERIFICATION.json'}]
    for p in sorted(set(paths)):
        if not p.is_file() or p.is_symlink() or '__pycache__' in p.parts or p.suffix == '.pyc':
            continue
        if external_manuscript(p):
            continue
        data = p.read_bytes()
        rel = p.relative_to(root).as_posix()
        entry = {'path': rel, 'bytes': len(data),
                 'sha256': hashlib.sha256(data).hexdigest(),
                 'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
        manifest['files'].append(entry)
        z.writestr(rel, data)
    z.writestr('SNAPSHOT_MANIFEST.json', json.dumps(manifest, indent=2)+'\n')
manifest['archive_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
manifest['archive_bytes'] = archive.stat().st_size
manifest['snapshot_finished_utc'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
(out / 'SNAPSHOT_MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k != 'files'}))
print('files_captured', len(manifest['files']))

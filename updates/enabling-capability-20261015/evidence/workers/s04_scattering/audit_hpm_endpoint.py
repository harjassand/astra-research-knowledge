#!/usr/bin/env python3
"""Bounded provenance audit of acquired, reference-linked HPM-1 measurements.

This decodes supplied TIFFs and audits exact deterministic fills. It does not
integrate diffraction peaks, solve an atomic structure or run dynamic refinement.
"""
from pathlib import Path
import hashlib
import io
import json
import re
import shlex
import time
import zipfile

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent


def main():
    started = time.perf_counter()
    archive = BASE / 'data/HPM-1_RT.zip'
    frames = []
    fills = []
    with zipfile.ZipFile(archive) as z:
        names = [x.filename for x in z.infolist() if x.filename.endswith('.tiff')]
        cache = {}

        def pixels(name):
            if name not in cache:
                im = Image.open(io.BytesIO(z.read(name)))
                cache[name] = np.asarray(im).astype(np.int32)
            return cache[name]

        for name in names:
            blob = z.read(name)
            im = Image.open(io.BytesIO(blob))
            a = np.asarray(im)
            frames.append({'path': name, 'source_file_sha256': hashlib.sha256(blob).hexdigest(),
                           'size_wh': list(im.size), 'mode': im.mode, 'source_dtype': str(a.dtype),
                           'tiff_software': str(im.tag_v2.get(305, '')),
                           'tiff_description': str(im.tag_v2.get(270, '')),
                           'min': int(a.min()), 'max': int(a.max()),
                           'pixels_equal_65535': int((a == 65535).sum()),
                           'pixel_sum': int(a.astype(np.uint64).sum())})
            if name.endswith('i.tiff'):
                n = int(Path(name).stem[:-1])
                previous = f'HPM-1_RT/tiff/{n - 1:05d}.tiff'
                following = f'HPM-1_RT/tiff/{n + 1:05d}.tiff'
                mid = pixels(name)
                expected = (pixels(previous) + pixels(following) + 1) // 2
                equal = np.array_equal(mid, expected)
                fills.append({'path': name, 'parents': [previous, following],
                              'exact_pixelwise_ceil_neighbor_mean': bool(equal),
                              'pixels_tested': int(mid.size),
                              'different_pixels': int((mid != expected).sum())})
                cache.clear()
        pts = z.read('HPM-1_RT/crs3.pts2').decode()
        lines = pts.splitlines()
        image_start = lines.index('imagelist') + 1
        image_stop = lines.index('endimagelist', image_start)
        listed = [line.split() for line in lines[image_start:image_stop] if line.strip()]
        listed_names = ['HPM-1_RT/' + row[0].replace('\\', '/') for row in listed]
        assert set(listed_names) == set(names)
        geometry = {}
        for key in ['lambda', 'aperpixel', 'geometry', 'centermode', 'dstarmax',
                    'integrationmode', 'intensitymethod', 'integrationparams',
                    'intkinematical', 'intdynamical', 'phi', 'omega',
                    'cellrefinemode', 'referencecell', 'virtualframes']:
            geometry[key] = next(line[len(key):].strip() for line in lines if line.startswith(key + ' '))
    reference = BASE / 'sources/STW_HPM1_Xray_reference.cif'
    cif = reference.read_text()
    embedded = {}
    for tag, name in [('_shelx_hkl_file', 'STW_HPM1_Xray_reference.hkl'),
                      ('_shelx_res_file', 'STW_HPM1_Xray_reference.res')]:
        match = re.search(re.escape(tag) + r'\s*\n;\s*\n(.*?)\n;', cif, re.S)
        assert match
        blob = (match.group(1) + '\n').encode()
        destination = BASE / 'data' / name
        destination.write_bytes(blob)
        embedded[tag] = {'path': str(destination.relative_to(BASE)), 'bytes': len(blob),
                         'sha256': hashlib.sha256(blob).hexdigest(),
                         'lines': len(match.group(1).splitlines())}
    selected_tags = {}
    for tag in ['_chemical_formula_sum', '_space_group_IT_number', '_space_group_name_H-M_alt',
                '_cell_measurement_temperature', '_cell_length_a', '_cell_length_b', '_cell_length_c',
                '_diffrn_reflns_number', '_diffrn_radiation_wavelength',
                '_reflns_number_total', '_refine_ls_abs_structure_Flack',
                '_refine_ls_R_factor_all', '_refine_ls_R_factor_gt']:
        line = next(line for line in cif.splitlines() if line.startswith(tag + ' '))
        selected_tags[tag] = line[len(tag):].strip()
    result = {
        'status': 'REFERENCE_INTERFACE_ACQUIRED; ATOMIC_HAND_REPLAY_NOT_RUN',
        'archive': {'path': str(archive.relative_to(BASE)), 'bytes': archive.stat().st_size,
                    'sha256': hashlib.sha256(archive.read_bytes()).hexdigest()},
        'source_tiff_files': len(frames),
        'exact_neighbor_mean_fills': len(fills),
        'all_i_files_exact_neighbor_mean_fills': all(r['exact_pixelwise_ceil_neighbor_mean'] for r in fills),
        'non_i_supplied_detector_files': len(frames) - len(fills),
        'raw_boundary': '429 non-i supplied instamatic detector TIFFs, 22 deterministically filled ImageJ TIFFs. These 22 files are exactly ceil((previous+following)/2) pixelwise. The 429 files are not certified untouched detector bytes; the Timepix detector-gap expansion and upstream calibration provenance still require documentation.',
        'dimensions_wh': sorted({tuple(f['size_wh']) for f in frames}),
        'all_source_files_nonempty_signal': all(f['pixel_sum'] > 0 for f in frames),
        'frames_with_pixel_equal_65535': sum(f['pixels_equal_65535'] > 0 for f in frames),
        'PETS_source_geometry': geometry,
        'PETS_imagelist': {'listed_files': len(listed), 'all_exist_in_archive': True,
                          'all_use_flags': sorted({int(row[8]) for row in listed}),
                          'original_alpha_range_deg': [float(listed[0][9]), float(listed[-1][9])],
                          'refined_alpha_range_deg': [float(listed[0][1]), float(listed[-1][1])],
                          'frame_scale_range': [min(float(row[4]) for row in listed),
                                                max(float(row[4]) for row in listed)],
                          'interpolated_files_included_as_use_1': sum(row[0].endswith('i.tiff') and int(row[8]) == 1 for row in listed)},
        'reference_CIF': {'path': str(reference.relative_to(BASE)), 'bytes': reference.stat().st_size,
                          'sha256': hashlib.sha256(reference.read_bytes()).hexdigest(),
                          'selected_tags': selected_tags, 'embedded_inputs': embedded},
        'scientific_endpoint': 'STW_HPM-1 framework P 65 2 2 versus P 61 2 2, linked by inversion. Source reports room-temperature 3D ED wR_all 0.234 versus 0.306, and original-crystal CuKa Flack x=0.06(2), based on 828 quotients. These are source results, not independently rerun results.',
        'reference_scope': 'Same-parent-crystal cross-modality reference, per paper provenance; XRD sampled the parent and ED a crushed fragment. Source assumes each parent is a single enantiomorph. CIF x=0.06(2) establishes a dominant hand under its model; it is not a fragment-by-fragment independent homogeneity measurement.',
        'cost_scope': {'source_ED_conditions': '200kV JEOL JEM-2100, Timepix detector, Instamatic; 0.46 deg/s, 0.5s exposure nominally 0.23 deg/frame',
                       '451_file_exposure_sum_s_if_all_were_measured': 451 * .5,
                       '429_nonfill_file_exposure_sum_s': (len(frames) - len(fills)) * .5,
                       'warning': 'The first exposure sum overcounts independent measured files because 22 are deterministic fills. The second is nominal measured-frame integration time, not full beam-on dose or acquisition wall time. Tracking/dead time and dose unreported for this RT control.',
                       'physical_cost_energy_hardware_time': 'UNKNOWN beyond quoted source parameters'},
        'execution_elapsed_s': time.perf_counter() - started,
        'inference_tokens': 'UNKNOWN', 'inference_cost': 'UNKNOWN', 'inference_energy': 'UNKNOWN',
    }
    (BASE / 'HPM_endpoint_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    (BASE / 'sources/HPM_frame_audit.json').write_text(json.dumps({'frames': frames, 'fills': fills}, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['status', 'source_tiff_files', 'exact_neighbor_mean_fills',
                                             'all_i_files_exact_neighbor_mean_fills', 'non_i_supplied_detector_files',
                                             'dimensions_wh', 'PETS_imagelist', 'execution_elapsed_s']}, indent=2))


if __name__ == '__main__':
    main()

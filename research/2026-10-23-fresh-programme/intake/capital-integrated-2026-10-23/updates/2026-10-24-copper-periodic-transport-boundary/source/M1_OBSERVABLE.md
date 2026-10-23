# M1 movie: bounded front observable and extraction QA

## Result

The public M1 AVI supports a reproducible **pixel-space front track** over a fixed region before the ramified front leaves the chosen search window. A one-valued interface graph is visually and numerically stable through encoded frame 11 (about 2.2 s). From frame 12 onward the tracker begins to hit the search-window boundary; by frame 15 (about 3.0 s) the overlay is visibly unreliable as the interface develops protrusions/overhangs. This is a bounded image observable, not a reconstruction of Cu volume, local current, or concentration.

The object is Schneider et al., “Nanoscale evolution of interface morphology during electrodeposition,” *Nature Communications* 8, 2174 (2017), [article DOI](https://doi.org/10.1038/s41467-017-02364-9), specifically supplementary movie M1 (`41467_2017_2364_MOESM3_ESM.avi`). The source and bath details are in [DATA_INTERFACE.md](DATA_INTERFACE.md).

## Time and image crosswalk

Independent `ffprobe` inspection of the retained AVI gives MJPEG, 720×480 pixels, 10 frames/s, 93 frames, and 9.3 s encoded duration. The article supplement describes M1 as 2× playback with an 18 s run. The upside-down camera clock visible in the movie is approximately 17:00:00 at frame 0, 17:00:03 at frame 15, 17:00:09 at frame 45, and 17:00:18 at frame 90. These checks support a movie-to-experiment time conversion of roughly 0.2 s per encoded frame; the script records `frame × 0.2 s` as an approximate overlay time, not a precision acquisition timestamp. This places frame 15 near the paper’s reported onset of strong ramification around 3.1 s.

The paper gives a 1.85×1.4 µm field of view, whereas the AVI raster is 720×480 (3:2). The physical-axis calibration/crop is not resolved by the public movie, so all extracted distances and areas below stay in pixels.

## Front operator and outputs

`m1_front_extract.py` decodes the first 16 frames to a temporary directory without changing the source AVI. In each frame it searches a fixed ROI `x=220…679`, `y=240…419` for the Cu/electrolyte boundary. The local image is smoothed with Pillow `GaussianBlur(radius=0.8 px)`. For each x it chooses the y maximizing the vertically differenced grayscale score `I(y−d)−I(y+d)` with `d=4 px`, after a three-pixel lateral average; a three-point median filter is then applied along x. Bright electrolyte above and darker Cu-rich contrast below define the sign. The ROI and resulting line are drawn in green/red, respectively, in [M1_EARLY_FRONT_QA.png](M1_EARLY_FRONT_QA.png). The later frame-15 panel is included to expose failure, not to endorse that track.

The exported [M1_FRONT_PROFILES_FRAMES_0_11.csv](M1_FRONT_PROFILES_FRAMES_0_11.csv) contains 5,520 point records: `frame`, approximate `time_s_from_overlay`, x pixel, tracked y pixel, and local edge strength. It contains every x=220…679 for frames 0…11. [M1_EARLY_METRICS.csv](M1_EARLY_METRICS.csv) contains one row for each of the first 16 frames at d=4 px, including:

- mean and median upward advance relative to the frame-0 profile, plus the first-difference interval mean upward velocity in px/s (using the approximate 0.2 s/frame crosswalk);
- `projected_swept_area_px2 = Σₓ(y₀(x)−yₜ(x))`, a 2-D pixel-space front-displacement proxy;
- detrended RMS of y(x), after subtracting a fitted straight-line slope;
- the fraction of tracked x positions at the top/bottom search boundary, used as an operator-failure flag.

At frame 5 (~1.0 s), mean advance is 5.14 px, the pixel-space swept proxy is 2,363 px², and detrended RMS is 3.93 px (2.90 px at frame 0). At frame 10 (~2.0 s), mean advance is 37.53 px, the proxy is 17,265 px², RMS is 5.58 px, and no positions are at the search boundary. The frame-0-to-10 average is 18.77 px/s in the image's upward direction; the local first-difference interval velocities are also in the CSV. At frame 11 (~2.2 s), the boundary-hit fraction remains zero. It rises to 3.3% at frame 12 (~2.4 s), then to 13.9% at frame 14 and 13.7% at frame 15. The frame-15 profile also visibly clips and follows an increasingly branched boundary, so it is excluded from the primary profile export.

Sensitivity to the vertical contrast span is acceptable for gross position after the front has clearly advanced: at frame 10 the mean advance is 36.95, 37.53, and 37.40 px for `d=2,4,6`, respectively. At frame 5 the corresponding estimates are 3.69, 5.14, and 4.35 px, so the very early small displacement is less stable. Absolute roughness is operator-dependent: `d=2` tracks image texture at frame 0 (10.65 px detrended RMS, versus 2.90 and 2.81 px for `d=4` and `d=6`). The primary roughness series therefore uses `d=4` and should be read as an algorithm-defined projected roughness measure, not as a calibrated material roughness.

## Physical boundary of this observation

The extracted `h(x,t)` is the location of a grayscale transition in a compressed, rendered transmission image. The swept proxy sums vertical displacement over a selected image interval; it is not a segmented Cu footprint or a volume. Overhangs can place several interfaces on the same x column, and a maximum-gradient operator then chooses one branch or clips. Contrast can also depend on thickness, diffraction, beam conditions, and overlapping material along the line of sight. The movie provides no public thickness-resolved reconstruction, contrast-to-Cu calibration, porosity/density calibration, or local electrochemical current map. Thus the data support projected pixel position, slope/envelope, and algorithm-specific RMS before failure only; they do not support converting that proxy to deposited Cu mass/current or fitting a concentration-transport law.

The article’s quoted 55 nm/s front-growth estimate is source-reported and uses its own calibration/analysis. As a consistency check only, applying the nominal vertical scale `1.4 µm / 480 px` to the extracted 37.53 px advance over about 2 s gives 54.7 nm/s. The numerical agreement does not establish that the rendered movie uses the full stated field of view or the same front-position definition, so I do not treat this as a calibrated reproduction. A physical velocity comparison would need the active image crop and axis calibration reconciled with the 720×480 movie. A local flux/volume analysis would additionally need front thickness/gap and a density/porosity or independent mass calibration. The existing public AVI is therefore useful for a limited front-shape reanalysis, while the requested flux-versus-morphology inference remains blocked at the observation operator.

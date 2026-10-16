# Acquisition and replay manifest

Frozen 16 October 2026. No numerical hardware qualification has been established.

Originals are retained at `/workspace/shared/refresh_qualification_route`; small reports/audits suffice for delivery.

## Replay and safety

`python check_public_data.py` validates count structure, pinned Git blob identity and static frequency-data opcodes. No downloaded notebook, compiler, or pickle code was executed.

## What remains uncalibrated

- Actual Astra refresh pulses and their simultaneous neighborhood
- Full-joint Hamiltonian residual and bath/truncation norms
- Seed isolation and no-return condition
- Spatial/temporal noisy footprint before recovery
- Confidence-bounded operational or diamond residual for a performed refresh

## Public source files

- `sources/hellings2025.pdf` (1949364 bytes): [source](https://arxiv.org/pdf/2503.04610); SHA256 `e0bbd70d107e8818080f586ecfd5caae86e06bab6019a965b35b14b96f343d3b`
- `sources/hellings2025.txt` (105094 bytes): [source](https://arxiv.org/pdf/2503.04610); SHA256 `a7eb25668d333c38ecc973670798ac4815a803740462dc8846bab4d1d10d4fe2`
- `sources/giarmatzi2024.html` (207352 bytes): [source](https://arxiv.org/html/2308.00750v2); SHA256 `f4a2f2634dc53488b1e5bb6cf0c426f2c5f9ad922d0d6a509b0b9f11db66dec0`
- `sources/white2025.html` (758613 bytes): [source](https://arxiv.org/html/2312.08454v2); SHA256 `c0f7c2187bf3b5aca34250a5300caf15ee646e67ad795b569a1ebc46ca0a06b7`
- `sources/white_repo_tree.json` (59556 bytes): [source](https://api.github.com/repos/gwhitequantum/process-tensor-network-tomography/git/trees/e3f01b011f28c1497f7ebb3dc4f98a782a75095f?recursive=1); SHA256 `a7b26d7eeb234d5045bb839fd59903bf3efba028724d09ec58752d34d288076c`
- `sources/giarmatzi_repo_tree.json` (2688 bytes): [source](https://api.github.com/repos/Christina-Giar/NMN-tomo/git/trees/154235f8bbf5e70eb71c325370a67b1894490452?recursive=1); SHA256 `f8d1a87dc7cb5c660afa32c6dffd6fa709102710bdf7047f5bc1096f323ed2ca`
- `sources/NMN_README.md` (904 bytes): [source](https://github.com/Christina-Giar/NMN-tomo/blob/154235f8bbf5e70eb71c325370a67b1894490452/README.md); SHA256 `fcd27b514890614b03a26f7ec84a879962feccdb846fd00de103b9631c46a593`
- `sources/NMN_lab_rslts.json` (20177 bytes): [source](https://github.com/Christina-Giar/NMN-tomo/blob/154235f8bbf5e70eb71c325370a67b1894490452/NMN_lab_rslts.json); SHA256 `b52afa57cced174839059e6438e17dc49ead33ae6687c44f58f6f2c664dcdc43`
- `sources/NMN_tomog_rerun.json` (176825 bytes): [source](https://github.com/Christina-Giar/NMN-tomo/blob/154235f8bbf5e70eb71c325370a67b1894490452/NMN_tomog_rerun.json); SHA256 `450db9360fbd162fd12e5be13655e45e1d19f29049f96c9fdb2ab6616b00c657`
- `sources/NMN_All_codes.ipynb` (1399666 bytes): [source](https://github.com/Christina-Giar/NMN-tomo/blob/154235f8bbf5e70eb71c325370a67b1894490452/All%20codes.ipynb); SHA256 `b0a2e041ef1616f8c0cff8e2536a892a260820d16fbd8343d22e898b0441c2a1`
- `sources/NMN_notebook_source.txt` (31174 bytes): [source](https://github.com/Christina-Giar/NMN-tomo/blob/154235f8bbf5e70eb71c325370a67b1894490452/All%20codes.ipynb); SHA256 `34cdb30a1598768626e4f65cb396b1d6a965224ee249f78242e340d7ae1c7aae`
- `sources/white_cairo_SU4_results.pickle` (108038 bytes): [source](https://github.com/gwhitequantum/process-tensor-network-tomography/blob/e3f01b011f28c1497f7ebb3dc4f98a782a75095f/data/SU4_opt/Job_data/cairo_SU4_job_dict_cnot_03_10_results.pickle); SHA256 `9920ef3abe36088cdc4f1f505881def92df73d628c903860cbbf8433f09962af`
- `sources/white_preprocess.py` (8283 bytes): [source](https://github.com/gwhitequantum/process-tensor-network-tomography/blob/e3f01b011f28c1497f7ebb3dc4f98a782a75095f/src/preprocess.py); SHA256 `718c8564078a145910ac3a0bdd560407d29c938e4e36af825a731fafb652b550`
- `rgst_1.gst` (91424 bytes): [source](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/data/rgst_1.gst); SHA256 `1151a751d81f9949a99030a3604f4070aa0acd721169be0ad2153408708a0389`
- `ware_data_gst_1.gst` (91424 bytes): [source](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/data/gst_1.gst); SHA256 `32243ffc1be44877a4c07164683e773df623dcfb52a7e6b09daad30be8a17958`
- `ware_notebooks_Randomize.ipynb` (52789 bytes): [source](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/notebooks/Randomize.ipynb); SHA256 `5caf50b3f0c85341cfa19227b3b8adc9cd2dd51666c494f3e6721def6b6f3c0a`
- `ware_scripts_rand_README.md` (1109 bytes): [source](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/scripts/rand/README.md); SHA256 `563de2987aa9abf257e768e400153b5e70213288aace1243f9c334ef0060e908`
- `ware_scripts_rand_randomize.jl` (3336 bytes): [source](https://github.com/matthewware/RGST-analysis/blob/9afedca174dbcb14d52c245cf7504a834816fc39/scripts/rand/randomize.jl); SHA256 `fe71c1b0aef7448fb846666ceca9ee3f440516f597b4464618c1c9a3793097d3`
- `ware_repo_tree.json` (16878 bytes): [source](https://api.github.com/repos/matthewware/RGST-analysis/git/trees/9afedca174dbcb14d52c245cf7504a834816fc39?recursive=1); SHA256 `5d809d910483dd623e94305e391511c2e476f519b6df66f24cfd5b0805b3239a`
- `RGST-analysis_head.json` (5163 bytes): [source](https://api.github.com/repos/matthewware/RGST-analysis/commits/9afedca174dbcb14d52c245cf7504a834816fc39); SHA256 `ff8ce635e1390f853b73e1b3dc48f94f95f2aa7f85094e8056d40b6d2ff92030`
- `qgl_APS2.jl` (11133 bytes): [source](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/APS2.jl); SHA256 `a2d26ee7a08df4408e57a491be3f0ff45bcceb2d6d972e0dd26b100e95a369ed`
- `qgl_GSTsequences.jl` (3176 bytes): [source](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/GSTsequences.jl); SHA256 `9475d1c7f1759a4e44ec6fa766e00dfbce4b64f357a8497cc56dbfdd51c6e46e`
- `qgl_compiler.jl` (8450 bytes): [source](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/compiler.jl); SHA256 `c7c6a06314592002323aaeaa1485715f441052eda5d60826de1f2f267e51ea2c`
- `qgl_pulses.jl` (10344 bytes): [source](https://github.com/BBN-Q/QGL.jl/blob/70e66d76f2e5f518ff2d8b78bc93b65779182c9f/src/pulses.jl); SHA256 `e0c72541348535b26e0ae562ee6dec1e244de6aace26c9c65f17a9fd8e6fd753`
- `qgl_repo_tree.json` (5619 bytes): [source](https://api.github.com/repos/BBN-Q/QGL.jl/git/trees/70e66d76f2e5f518ff2d8b78bc93b65779182c9f?recursive=1); SHA256 `eeca00c480de9b096150143bf7e4964d2c1d87456f66f76d36fe52fa342c4408`
- `QGL.jl_head.json` (2661 bytes): [source](https://api.github.com/repos/BBN-Q/QGL.jl/commits/70e66d76f2e5f518ff2d8b78bc93b65779182c9f); SHA256 `1030ddf0f8d7f654156cdeca9d2034ca7088e61854f4136e31d98e3756f9e397`
- `winick_source.html` (229239 bytes): [source](https://arxiv.org/html/2212.07500v1); SHA256 `b3d185f2f13efa12fee2dd99ad04cb886e40e59428a66608f46e6998a77de20b`

## Acquisition limits

- ETH flux-data DOI exists in the published paper, but its landing page returned HTTP 429. Raw flux-data contents were not acquired.
- Giarmatzi records are grouped counts: paired opposite second-preparations total exactly 16,000 (IBM) or 18,432 (in-house), rather than the preprint’s nominal 16,384. Grouping is consistent with the described postprocessing, but the nominal-count discrepancy is unresolved.
- White representative file contains processed frequencies; required setting/outcome metadata must be matched before reanalysis.
- Ware public compiler revision is not proven identical to the build used in the archived experiment.

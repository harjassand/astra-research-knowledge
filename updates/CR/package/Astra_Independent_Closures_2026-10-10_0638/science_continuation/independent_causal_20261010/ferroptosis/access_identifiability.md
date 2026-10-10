# Ferroptotic-wave candidate: no newly identified mechanism

## Access verified
Primary article: Co et al., Nature 631, 654–662 (2024), https://doi.org/10.1038/s41586-024-07623-6.
Raw/source image deposit: https://doi.org/10.6084/m9.figshare.25762806; downloaded Figure 2a.7z (15,933,731 bytes; published MD5 e5d5d01837162250d2c1627bda717c21).
Code and supporting processed data: https://github.com/imb-lcd/ftw2024, frozen tree SHA 01cab80eb0e365f975962ea4c49fde4f553cd555.

The downloaded gap archive contains four examples, gaps labelled 35, 118, 156, and 224 micrometres, each with ROS and nuclear-dye TIFF stacks. Every stack is 1,587 × 201 pixels × 7 frames, 16-bit. The source-data workbook contains four smoothed, spatially averaged, differential-ROS profiles and a separate table of gap-crossing outcomes. Upstream code calculates ROS frame differences before plotting the profiles; they are not direct extracellular mediator concentrations. The full acquisition and donor emission history are not included in these cropped stacks. Upstream scripts refer to earlier global frames and a separate preprocessing/alignment pipeline.

No microscopy pixel arrays or tabulated numerical gap outcomes were opened. The specified 118/224 micrometre validation sequences are still untouched; indeed the 35/156 discovery pixel sequences also remain unexamined. Their published qualitative crossing categories were already known and were expressly excluded as fresh validation targets.

## Identification boundary
The proposed new question was whether extracellular destruction (rate k) sets the gap-crossing cutoff. For a carrier m satisfying m_t = D*m_xx - k*m + s, a finite source duration with k=0 can also cause an apparent finite transmission range over a finite observation period. The data measure cellular reporter responses, not source flux s or the extracellular field m. Intracellular amplification/integration and fluorescent reporter integration add unknown kernels. Therefore the cutoff and intracellular spatial/temporal signal alone do not uniquely determine extracellular destruction versus finite emission.

A useful formal statement is y_L = H_cell * H_reporter * G_(D,k,L) * s. Observing y_L while s and the two response kernels are unmeasured does not identify k just by fitting G. Multiple gap widths can help only with justified, shared source/response restrictions; the four selected movies, heterogeneous donor histories, and missing pre-window histories do not establish those restrictions. No k estimate, molecular species, or new pathway is claimed.

The attractive inference that propagation occurs before cell rupture is prior art, not a discovery here: Riegman et al., Nature Cell Biology 22, 1042–1048 (2020), https://pmc.ncbi.nlm.nih.gov/articles/PMC7644276/, demonstrated propagation with osmoprotection suppressing lysis.

The pass stops before consuming the reserved numerical validation data. No new wet-lab action or contact was attempted.

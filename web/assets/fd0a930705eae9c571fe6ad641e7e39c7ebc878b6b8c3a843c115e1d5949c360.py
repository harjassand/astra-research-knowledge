#!/usr/bin/env python3
"""Reconstruct relative 2-kb position-code ChIP profiles for GSE287042.

The public GEO text files are samtools idxstats tables (PC, reference length,
mapped reads, unmapped reads). This script normalizes ChIP PC read fractions by
the matching genomic-DNA PC read fractions. It intentionally reports *relative*
per-code enrichment only: GEO lacks the independent qPCR recovery scale used in
the paper, so these outputs are not absolute ChIP recovery or per-cell occupancy.

Run from repository root:
  python3 work/agents/c8_genome_engineering/code/analyze_pc_profiles.py
"""
from __future__ import annotations

import csv
import gzip
import json
import math
import re
from pathlib import Path

ROOT = Path("work/agents/c8_genome_engineering")
RAW = ROOT / "sources/raw"
SUP = ROOT / "sources/supplement"
OUT = ROOT / "sources/derived"


def read_idxstats(path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    with gzip.open(path, "rt") as fh:
        for line in fh:
            fields = line.rstrip("\n").split("\t")
            if len(fields) >= 4 and re.fullmatch(r"T\d{3}", fields[0]):
                counts[fields[0]] = int(fields[2])
    return counts


def parse_fasta(path: Path):
    current = None
    parts: list[str] = []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current is not None:
                    yield current, "".join(parts).upper()
                current = line[1:].split()[0]
                parts = []
            else:
                parts.append(line)
        if current is not None:
            yield current, "".join(parts).upper()


def reverse_complement(seq: str) -> str:
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def read_pc_sequences() -> dict[str, str]:
    out: dict[str, str] = {}
    with (ROOT / "sources/CenU_position_codes.tsv").open() as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            out[row["code"]] = row["sequence"].upper()
    return out


def sequence_map(pc: dict[str, str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    files = [
        ("HAC120", SUP / "Supplementary Contigs 1.fasta"),
        ("HAC465", SUP / "Supplementay Contigs 2.fasta"),
    ]
    for hac, fasta in files:
        for contig, sequence in parse_fasta(fasta):
            for code, motif in pc.items():
                for strand, needle in (("+", motif), ("-", reverse_complement(motif))):
                    start = 0
                    while True:
                        pos = sequence.find(needle, start)
                        if pos < 0:
                            break
                        rows.append({
                            "hac": hac,
                            "contig": contig,
                            "position0": pos,
                            "position1": pos + 1,
                            "code": code,
                            "strand": strand,
                        })
                        start = pos + 1
    return sorted(rows, key=lambda x: (str(x["hac"]), str(x["contig"]), int(x["position0"])))


def relative_enrichment(chip: dict[str, int], dna: dict[str, int], codes: list[str]):
    chip_total = sum(chip.get(code, 0) for code in codes)
    dna_total = sum(dna.get(code, 0) for code in codes)
    out = {}
    for code in codes:
        # Jeffreys pseudocount is used only to make the descriptive log ratio
        # finite at sparse/zero-read codes. Raw counts are preserved separately.
        p_chip = (chip.get(code, 0) + 0.5) / (chip_total + 0.5 * len(codes))
        p_dna = (dna.get(code, 0) + 0.5) / (dna_total + 0.5 * len(codes))
        out[code] = p_chip / p_dna
    return out, chip_total, dna_total


def write_tsv(path: Path, rows: list[dict[str, object]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pc = read_pc_sequences()
    codes = sorted(pc, key=lambda c: int(c[1:]))
    assert len(codes) == 128, len(codes)

    dna_by_hac = {}
    dna_paths = {}
    for hac, file_tag in (("HAC120", "120"), ("HAC465", "465")):
        hits = sorted((RAW / "GSE287040").glob(f"*HAC{file_tag}_GD.txt.gz"))
        assert len(hits) == 1, hits
        dna_by_hac[hac] = read_idxstats(hits[0])
        dna_paths[hac] = str(hits[0])

    # Sample basename encodes the condition, antibody and HAC line.
    rx = re.compile(
        r"GSM(\d+)_HAC(120|465)_ChIP(?:_(THYM|COL|CR3|siC|siK7|siHJ))?_(CA|K4D|K14A|K8A|K20M|K36D|K9T)\.txt\.gz$"
    )
    profile_rows: list[dict[str, object]] = []
    sample_profiles: dict[tuple[str, str, str], dict[str, float]] = {}
    sample_meta: list[dict[str, object]] = []
    for path in sorted((RAW / "GSE287042").glob("*.gz")):
        match = rx.fullmatch(path.name)
        if not match:
            continue
        gsm, line, cond, antibody = match.groups()
        hac = "HAC" + line
        condition = cond or "ASYNC"
        chip = read_idxstats(path)
        rel, chip_total, dna_total = relative_enrichment(chip, dna_by_hac[hac], codes)
        key = (hac, condition, antibody)
        sample_profiles[key] = rel
        sample_meta.append({
            "gsm": "GSM" + gsm,
            "hac": hac,
            "condition": condition,
            "antibody_code": antibody,
            "chip_reads_T_codes": chip_total,
            "gd_reads_T_codes": dna_total,
            "file": str(path),
        })
        for code in codes:
            profile_rows.append({
                "gsm": "GSM" + gsm,
                "hac": hac,
                "condition": condition,
                "antibody_code": antibody,
                "code": code,
                "chip_mapped_reads": chip.get(code, 0),
                "gd_mapped_reads": dna_by_hac[hac].get(code, 0),
                "relative_enrichment": f"{rel[code]:.8g}",
                "log2_relative_enrichment": f"{math.log2(rel[code]):.8g}",
            })

    # Within-sample spatial profiles are compositional because the qPCR recovery
    # multiplier is not in GEO. Compare phase shapes only; do not call these
    # absolute phase-change estimates.
    fold_rows: list[dict[str, object]] = []
    for hac in ("HAC120", "HAC465"):
        for antibody in ("CA", "K9T"):
            ref = sample_profiles.get((hac, "THYM", antibody))
            if ref is None:
                continue
            for condition in ("COL", "CR3", "siC", "siK7", "siHJ"):
                profile = sample_profiles.get((hac, condition, antibody))
                if profile is None:
                    continue
                for code in codes:
                    fold = profile[code] / ref[code]
                    fold_rows.append({
                        "hac": hac,
                        "antibody_code": antibody,
                        "reference_condition": "THYM",
                        "condition": condition,
                        "code": code,
                        "relative_profile_fold": f"{fold:.8g}",
                        "log2_relative_profile_fold": f"{math.log2(fold):.8g}",
                        "interpretation": "compositional shape ratio; not absolute ChIP recovery",
                    })

    map_rows = sequence_map(pc)
    write_tsv(OUT / "relative_profiles.tsv", profile_rows)
    write_tsv(OUT / "relative_shape_folds_vs_THYM.tsv", fold_rows)
    write_tsv(OUT / "assembled_pc_positions.tsv", map_rows)
    write_tsv(OUT / "sample_manifest.tsv", sample_meta)

    summary = {
        "source": "GSE287040/GSE287042 raw idxstats tables and Ohzeki et al. 2026 Supplementary Contigs/Table S1",
        "n_cenu_codes": len(codes),
        "n_chip_sample_files_parsed": len(sample_meta),
        "samples_per_hac_condition_antibody": "one PC-sequencing sample per listed combination; qPCR replicates in paper are separate",
        "dna_inputs": dna_paths,
        "hac120_zero_read_gd_codes": [c for c in codes if dna_by_hac["HAC120"].get(c, 0) == 0],
        "hac465_zero_read_gd_codes": [c for c in codes if dna_by_hac["HAC465"].get(c, 0) == 0],
        "n_assembled_pc_hits_by_hac": {
            hac: sum(row["hac"] == hac for row in map_rows) for hac in ("HAC120", "HAC465")
        },
        "limitations": [
            "Counts are sequencing read counts, not independent biological replicate values.",
            "GEO omits the per-sample qPCR recovery multiplier used by the paper; normalization yields relative PC distributions only.",
            "A PC tag duplicated in the assembled HAC cannot identify the mark state of each individual physical copy.",
            "Bulk ChIP profiles do not give same-cell CENP-A/H3K9me3 joint distributions or lineage transitions.",
        ],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

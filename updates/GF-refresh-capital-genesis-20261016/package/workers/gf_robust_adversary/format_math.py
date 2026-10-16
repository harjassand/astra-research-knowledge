#!/usr/bin/env python3
"""Repair inline math delimiters lost in the initial local text write."""
from pathlib import Path
import re

path = Path(__file__).with_name("DERIVATION.md")
lines = path.read_text().splitlines(keepends=True)
out = []
display = False
for line in lines:
    if line.strip() == r"\[":
        display = True
    if display:
        out.append(line)
        if line.strip() == r"\]":
            display = False
        continue
    protected = []

    def protect(match):
        protected.append(match.group())
        return f"@@MATH{len(protected)-1}@@"

    line = re.sub(r"\\\(.*?\\\)", protect, line)
    result, index = [], 0
    while index < len(line):
        if line[index] != "(":
            result.append(line[index])
            index += 1
            continue
        end, depth = index + 1, 1
        while end < len(line) and depth:
            depth += (line[end] == "(") - (line[end] == ")")
            end += 1
        if depth:
            result.append(line[index:])
            break
        inner = line[index + 1:end - 1].rstrip("\\")
        is_math = ("\\" in inner or "_" in inner
                   or re.fullmatch(r"[A-Za-z](?:[,= +<>0-9A-Za-z]*)", inner)
                   or re.fullmatch(r"[0-9]+/[0-9]+", inner))
        result.append(r"\(" + inner + r"\)" if is_math else line[index:end])
        index = end
    line = "".join(result)
    for index, value in enumerate(protected):
        line = line.replace(f"@@MATH{index}@@", value)
    out.append(line)
path.write_text("".join(out))
print("Repaired inline delimiters in DERIVATION.md")

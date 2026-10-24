"""Shared normalization, evidence resolution and deterministic lexical scoring."""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import html
import json
import math
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
STOP = frozenset((
    "a an the and or but if then as at by for from in into of on to with under "
    "this that these those is are was were be been being do does did can could "
    "should would will may might describe find want need using use"
).split())
TRANSFER_STATES = {
    "PROVEN LOGICAL DEPENDENCY", "ESTABLISHED COMPATIBLE INTERFACE",
    "CANDIDATE CONNECTION", "INCOMPATIBLE ASSUMPTIONS", "REFUTED TRANSFER",
}


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def local(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Path escapes repository: " + name)
    return path


def flatten(value):
    if isinstance(value, dict):
        return " ".join(flatten(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten(item) for item in value)
    return str(value) if value is not None else ""


def scientific_text(text):
    try:
        value = json.loads(text)
    except (ValueError, TypeError):
        return text, "unchanged_utf8"
    if isinstance(value, dict) and isinstance(value.get("answer"), dict):
        for key in ("text", "innerText"):
            if isinstance(value["answer"].get(key), str):
                return value["answer"][key], "JSON /answer/" + key + "; raw JSON remains authoritative"
    if isinstance(value, dict) and isinstance(value.get("cells"), list):
        return "\n\n".join("".join(cell.get("source", [])) for cell in value["cells"]), "notebook cell sources; outputs not indexed"
    def clean(item):
        if isinstance(item, dict):
            return {key: clean(child) for key, child in item.items() if key not in ("html", "image", "data", "base64")}
        if isinstance(item, list):
            return [clean(child) for child in item]
        return item
    return flatten(clean(value)), "JSON values excluding HTML/binary payloads; raw JSON remains authoritative"


def tokens(text):
    text = unicodedata.normalize("NFKC", text).lower().replace("_", " ")
    words = re.findall(r"[^\W_]+", text, re.UNICODE)
    return [word for word in words if word not in STOP and len(word) > 1]


def route_id(identifier):
    return identifier.split("-", 1)[0] if re.match(r"^[NL]\d+(?:-|$)", identifier) else identifier


def unique(rows, key):
    result = {}
    for row in rows:
        identifier = row[key]
        if identifier in result:
            raise ValueError("Duplicate " + key + ": " + identifier)
        result[identifier] = row
    return result


class Inputs:
    def __init__(self, root):
        self.root = Path(root)
        self.hashes = {}
        self.sources = {}

    def read(self, name):
        data = local(self.root, name).read_bytes()
        self.hashes[name] = digest(data)
        return data

    def json(self, name):
        return json.loads(self.read(name))

    def rows(self, name, shards=None):
        result = [json.loads(line) for line in self.read(name).splitlines() if line.strip()]
        if shards:
            for path in sorted((self.root / shards).glob("*.jsonl")):
                result.extend(self.rows(path.relative_to(self.root).as_posix()))
        return result

    def source(self, reference):
        expected = reference["sha256"]
        key = (reference["path"], expected, reference.get("read_path"))
        if key not in self.sources:
            found = None
            for name in dict.fromkeys([reference["path"], reference.get("read_path", "")]):
                if not name or not local(self.root, name).is_file():
                    continue
                data = self.read(name)
                if digest(data) == expected:
                    found = data.decode("utf-8")
                    break
                if name.endswith(".html"):
                    for block in re.findall(r"<pre(?:\s[^>]*)?>(.*?)</pre>", data.decode("utf-8"), re.S):
                        text = html.unescape(block)
                        if digest(text.encode()) == expected:
                            found = text
                            break
                if found is not None:
                    break
            if found is None:
                raise ValueError("INGESTION FAILED: required source bytes missing/mismatched: " + str(key))
            self.sources[key] = found
        text = self.sources[key]
        start, end = reference["lines"] if reference.get("lines") is not None else (1, len(text.splitlines()))
        if type(start) is not int or type(end) is not int or not 1 <= start <= end <= len(text.splitlines()):
            raise ValueError("Invalid source range: " + str(reference))
        passage = "".join(text.splitlines(keepends=True)[start - 1:end])
        if reference.get("quote") and reference["quote"] not in passage:
            raise ValueError("Wrong supporting passage/quote: " + reference["path"])
        return text, passage


def evidence_refs(value):
    if isinstance(value, dict):
        if {"path", "sha256", "lines"} <= value.keys():
            yield value
        for child in value.values():
            yield from evidence_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from evidence_refs(child)


def compact_ref(reference):
    fields = ("path", "sha256", "lines", "read_path", "hash_kind", "original_sha256",
              "source_revision", "range_scope", "quote", "doc_id", "web_page", "locator_scope")
    return {key: reference[key] for key in fields if key in reference}


def field_index(documents):
    """BM25 per field, combined additively; identical postings power CLI and web."""
    weights = {"title": 2.5, "statement": 1.5, "contract": 1.4, "aliases": 1.2,
               "body": 1.0, "notices": 0.7}
    postings = defaultdict(lambda: defaultdict(float))
    count = len(documents)
    for field, weight in weights.items():
        terms = [Counter(tokens(flatten(document.get(field, "")))) for document in documents]
        lengths = [sum(frequency.values()) for frequency in terms]
        average = sum(lengths) / max(count, 1) or 1
        frequency = Counter(term for document in terms for term in document)
        for index, document in enumerate(terms):
            normalizer = 1.2 * (0.25 + 0.75 * lengths[index] / average)
            for term, occurrences in document.items():
                inverse = math.log(1 + (count - frequency[term] + 0.5) / (frequency[term] + 0.5))
                postings[term][index] += weight * inverse * occurrences * 2.2 / (occurrences + normalizer)
    return {term: [[index, round(score, 6)] for index, score in sorted(values.items())]
            for term, values in sorted(postings.items())}


def query_terms(query, concepts):
    original = set(tokens(query))
    terms = {term: 1.0 for term in original}
    expansions = []
    for concept in concepts:
        triggers = [set(tokens(phrase)) for phrase in concept["phrases"]]
        if any(trigger and trigger <= original for trigger in triggers):
            added = []
            for term in tokens(" ".join(concept["terms"])):
                if term not in terms:
                    terms[term] = 0.35
                    added.append(term)
            if added:
                expansions.append({"concept": concept["id"], "terms": added})
    return terms, expansions


def score_query(postings, terms):
    scores = defaultdict(float)
    matched = defaultdict(set)
    for term, weight in terms.items():
        for index, score in postings.get(term, []):
            scores[index] += weight * score
            matched[index].add(term)
    return sorted(scores, key=lambda index: (-scores[index], index)), scores, matched

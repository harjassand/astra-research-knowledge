"""Lossless operation views and conservative premise inspection; no inferred proofs."""
import re

from knowledge.model import digest, flatten, tokens, route_id

CURRENT_CONSUMER_LAYOUT = "explicit-current-acceptance-v1"


def compile_current_consumers(records):
    """Project explicit, version-bound authority without rewriting its sources.

    A curator may restate a current consumer contract in the same acceptance
    notice. No prose classifier guesses which historical qualifications to
    delete; the full original record and its scientific identity remain intact.
    """
    by_id = {record["id"]: record for record in records}
    projections, known_authorities = {}, set()
    for record in records:
        for outer in record.get("notices", []):
            notice = outer.get("notice", outer)
            if (notice.get("kind") == "human_acceptance_instruction"
                    and notice.get("current_programme_status") == "CORRECT_AND_ACCEPTED"):
                known_authorities.add(notice["notice_id"])
            if notice.get("kind") == "current_consumer_projection":
                item = {key: notice.get(key) for key in ("notice_id", "authority_notice_id", "consumer_views")}
                if item["notice_id"] in projections and projections[item["notice_id"]] != item:
                    raise ValueError("INGESTION FAILED: conflicting consumer projection notice")
                projections[item["notice_id"]] = item
    for item in projections.values():
        if item["authority_notice_id"] not in known_authorities or not item["consumer_views"]:
            raise ValueError("INGESTION FAILED: consumer projection has no existing current authority/views")
    for record in records:
        record.pop("current_acceptance", None)
        record.pop("current_consumer", None)
        authorities, selected = {}, None
        for outer in record.get("notices", []):
            notice = outer.get("notice", outer)
            if notice.get("kind") == "current_consumer_projection":
                continue
            views = notice.get("consumer_views", [])
            if (notice.get("kind") != "human_acceptance_instruction"
                    or notice.get("current_programme_status") != "CORRECT_AND_ACCEPTED"):
                if views:
                    raise ValueError("INGESTION FAILED: consumer view needs explicit current acceptance")
                continue
            views = views + [view for item in projections.values()
                             if item["authority_notice_id"] == notice["notice_id"]
                             for view in item["consumer_views"]]
            subjects = {subject["id"]: subject["content_version"]
                        for subject in notice.get("accepted_subjects", [])}
            for view in views:
                subject = view.get("subject", {})
                if subject.get("id") not in by_id or subjects.get(subject.get("id")) != subject.get("content_version"):
                    raise ValueError("INGESTION FAILED: consumer view has no accepted subject/version")
                if by_id[subject["id"]]["content_version"] != subject["content_version"]:
                    raise ValueError("INGESTION FAILED: stale current consumer subject/version")
            if subjects.get(record["id"]) != record["content_version"]:
                continue
            if not notice.get("source_refs") or not notice.get("clarification"):
                raise ValueError("INGESTION FAILED: current acceptance needs its actual source and scope")
            authority = {"notice_id": notice["notice_id"], "kind": notice["kind"],
                "status": notice["current_programme_status"], "new_audit": notice.get("new_audit", False),
                "subject": {"id": record["id"], "content_version": record["content_version"]},
                "scope": notice["clarification"], "source_refs": notice["source_refs"],
                "legacy_status_fields_are_historical": bool(notice.get("legacy_status_fields_are_historical"))}
            authorities[notice["notice_id"]] = authority
            for view in views:
                subject = view.get("subject", {})
                if subject.get("id") not in by_id or subjects.get(subject.get("id")) != subject.get("content_version"):
                    raise ValueError("INGESTION FAILED: consumer view has no accepted subject/version")
                if by_id[subject["id"]]["content_version"] != subject["content_version"]:
                    raise ValueError("INGESTION FAILED: stale current consumer subject/version")
                if subject["id"] != record["id"]:
                    continue
                contract = view.get("contract", {})
                if (not view.get("statement") or not view.get("scope")
                        or any(not contract.get(field) for field in
                               ("requires", "provides", "assumptions", "costs", "units", "obstruction"))):
                    raise ValueError("INGESTION FAILED: incomplete current consumer statement/contract/scope")
                value = {"subject": subject, "authority_notice": notice["notice_id"],
                         "statement": view["statement"], "contract": contract, "scope": view["scope"],
                         "original_contract_context": "Preserved source-reported contract; superseded review/status wording is historical. Original scientific conditions and authority remain available at the record's source/history routes."}
                if selected is not None and selected != value:
                    raise ValueError("INGESTION FAILED: conflicting current consumer views")
                selected = value
        if authorities:
            record["current_acceptance"] = list(authorities.values())
        if selected:
            record["current_consumer"] = selected
    compile_input_contract_corrections(records)


def compile_input_contract_corrections(records):
    """Repair a cited input-field transcription while preserving pinned history.

    This permits only an explicit requires correction at an exact version. It
    cannot change a statement, output, review, acceptance or other conditions.
    Source hashes/ranges/quotes are checked by the ordinary build input reader.
    """
    by_id = {record["id"]: record for record in records}
    corrections = {}
    for record in records:
        for outer in record.get("notices", []):
            notice = outer.get("notice", outer)
            if notice.get("kind") != "source_input_contract_correction":
                continue
            notice = {key: notice.get(key) for key in
                      ("notice_id", "subject", "field", "value", "clarification", "source_refs")}
            subject = notice.get("subject", {})
            target = by_id.get(subject.get("id"))
            sources = notice.get("source_refs") or []
            supported = any(isinstance(ref, dict) and ref.get("path")
                            and isinstance(ref.get("sha256"), str)
                            and re.fullmatch(r"[0-9a-f]{64}", ref["sha256"])
                            and isinstance(ref.get("lines"), list) and len(ref["lines"]) == 2
                            and ref.get("quote") for ref in sources)
            value = notice.get("value")
            valid_value = isinstance(value, str) or (isinstance(value, list)
                            and all(isinstance(item, str) for item in value))
            if (target is None or subject.get("content_version") != target["content_version"]
                    or not notice.get("notice_id") or notice.get("field") != "requires"
                    or not valid_value or not flatten(value).strip()
                    or not supported or not notice.get("clarification")):
                raise ValueError("INGESTION FAILED: input correction needs exact subject, requires and source support")
            key = subject["id"]
            if key in corrections and corrections[key] != notice:
                raise ValueError("INGESTION FAILED: conflicting source input corrections")
            corrections[key] = notice
    for identifier, notice in corrections.items():
        record = by_id[identifier]
        if record.get("current_consumer"):
            raise ValueError("INGESTION FAILED: input correction conflicts with another current consumer view")
        visible_statement = statement_view(record, operation_frame(record))["statement"]
        record["current_consumer"] = {
            "subject": notice["subject"], "source_correction_notice": notice["notice_id"],
            "authority_notice": notice["notice_id"],
            "statement": visible_statement,
            "contract": dict(record["contract"], requires=notice["value"]),
            "scope": notice["clarification"],
            "original_contract_context": "Pinned source-reported input field remains in the original record/history. This source-supported input transcription correction changes no output, condition, scientific identity, review or acceptance.",
        }


def consumer_contract(record):
    return record.get("current_consumer", {}).get("contract", record["contract"])


def consumer_notice_view(value):
    """Link an authoring restatement once; keep every notice and source scope."""
    if isinstance(value, list):
        return [consumer_notice_view(item) for item in value]
    if not isinstance(value, dict):
        return value
    return {key: ([{"subject": view["subject"], "current_packet":
                    "knowledge/current/packets/" + route_id(view["subject"]["id"]) + ".json",
                    "scope": "Explicit current consumer restatement appears once in that packet; original notice authoring bytes remain in manifest inputs."}
                   for view in data] if key == "consumer_views" else consumer_notice_view(data))
            for key, data in value.items()}


def acceptance_view(record, preview=False):
    """Compact preview; the complete authority and exact sources stay in packets."""
    result = [{key: value for key, value in authority.items()
             if key in ("notice_id", "kind", "status", "new_audit", "subject", "scope",
                        "legacy_status_fields_are_historical")}
            for authority in record.get("current_acceptance", [])]
    if preview:
        for item in result:
            text = item["scope"]
            item["scope"] = text[:240]
            item["scope_omitted_characters"] = max(0, len(text) - 240)
    return result

CARD_LABEL = re.compile(r"(?i)^\s*(?:source-reported\s+)?(exact claim|claim|theorem|interface(?: and assumptions)?|assumptions|boundaries|boundary|costs?(?: and information boundary)?|proof spine|proof|construction|next obligation|evidence|references)\s*(?:\([^\n]*?\))?\s*(?:\||:|\.|$)")


def card_sections(record):
    """Locate existing prose; never synthesize a theorem from a status label."""
    if record["kind"] != "result":
        return []
    lines = record["body"].splitlines(keepends=True)
    label = CARD_LABEL
    # Skip the header/status block, or begin at an explicit scientific label
    # when a compact card has no separating blank line.
    begins = next((i + 1 for i, line in enumerate(lines) if not line.strip()), len(lines))
    first_label = next((i for i, line in enumerate(lines[1:], 1) if label.match(line)), len(lines))
    begins = min(begins, first_label)
    result, block, start, role = [], [], begins + 1, "unlabelled_card_passage"

    def flush():
        while block and not block[-1].strip():
            block.pop()
        if block and role not in ("evidence", "references"):
            result.append({"role": role, "text": "".join(block).rstrip("\r\n"), "lines": [start, start + len(block) - 1]})
        block.clear()

    for number, line in enumerate(lines[begins:], begins + 1):
        if re.match(r"(?i)^(?:status=|notation local\.?$|symbols .*local)", line.strip()):
            flush()
            role = "unlabelled_card_passage"
            continue
        match = label.match(line)
        if match:
            flush()
            role, start = match[1].lower(), number
        elif not line.strip() and role == "unlabelled_card_passage":
            flush()
            continue
        if not block:
            start = number
        block.append(line)
    flush()
    return result


def operation_frame(record):
    contract = consumer_contract(record)
    frame = {
        "id": record["id"], "content_version": record["content_version"],
        "operation": record["title"], "statement": record.get("current_consumer", {}).get("statement", record["statement"]),
        "construction": record["body"] if record["kind"] != "result" else "Read the card and cited construction",
        "requires": contract.get("requires", "UNKNOWN"),
        "returns": contract.get("provides", "UNKNOWN"),
        "conditions": contract.get("assumptions", "UNKNOWN"),
        "costs": contract.get("costs", "UNKNOWN"), "units": contract.get("units", "UNKNOWN"),
        "obstruction": contract.get("obstruction", "UNKNOWN"),
        "scope": "Verbatim normalized fields. Objects/types remain source-local; this view does not infer an interface or acceptance.",
    }
    if record.get("current_acceptance"):
        frame["acceptance"] = acceptance_view(record)
    if record.get("current_consumer"):
        frame["scope"] = "Explicit version-bound current consumer projection; its original source contract is preserved separately. No new audit or scientific scope inferred."
        frame["consumer_origin"] = {key: value for key, value in record["current_consumer"].items()
                                    if key not in ("statement", "contract")}
    passages = card_sections(record)
    if passages:
        labelled = [p for p in passages if p["role"] in ("claim", "exact claim", "theorem")]
        frame["scientific_excerpt"] = (labelled or passages)[0]
        frame["card_roles"] = [p for p in passages if p["role"] != "unlabelled_card_passage"]
        frame["card_reference"] = {"authority": record["authority"], "sha256": digest(record["body"].encode()),
                                   "read": ["card", record["id"]]}
        frame["card_scope"] = "Verbatim historical card passages, not a new theorem, inferred premise, or acceptance. Reported status is kept separately in the canonical record; current review overlays and corrections govern. Unlabelled excerpts have no inferred role."
    return frame


def historical_summary(record):
    statement = record["statement"]
    header_lines = re.split(r"\r?\n\s*\r?\n", record["body"], maxsplit=1)[0].splitlines()
    metadata = []
    for line in header_lines:
        if CARD_LABEL.match(line):
            break
        metadata.append(line)
    header = "\n".join(metadata)
    return record["kind"] == "result" and isinstance(statement, str) and bool(statement.strip()) and (
        statement.startswith("status=") or statement.strip() in header)


def statement_view(record, frame):
    if record.get("current_consumer"):
        return {"statement": record["current_consumer"]["statement"],
                "acceptance": acceptance_view(record),
                "statement_origin": {"kind": "explicit_current_consumer",
                    **{key: value for key, value in record["current_consumer"].items()
                       if key not in ("statement", "contract")}}}
    excerpt = frame.get("scientific_excerpt")
    if historical_summary(record) and excerpt:
        result = {"statement": excerpt["text"], "statement_origin": {"kind": "verbatim_card_excerpt",
                    "role": excerpt["role"], "lines": excerpt["lines"], "reference": frame["card_reference"],
                    "scope": "An unlabelled excerpt has no inferred theorem role; current proof/review/conditions govern."},
                "historical_reported_status": record["statement"]}
        if record.get("current_acceptance"):
            result["acceptance"] = acceptance_view(record)
        return result
    result = {"statement": record["statement"], "statement_origin": {"kind": "canonical_statement"}}
    if record.get("current_acceptance"):
        result["acceptance"] = acceptance_view(record)
    return result


def premise_check(frame, available=(), unavailable=()):
    """Surface literal overlaps with requirements, without treating absence as falsity.

    Negation, quantifiers and units require the full passage. In particular a
    match against 'without X' is not evidence that X is a required input.
    """
    fields = {key: flatten(frame[key]) for key in ("requires", "conditions", "costs", "units", "obstruction")}
    for passage in frame.get("card_roles", []):
        if passage["role"].startswith(("interface", "assumption", "boundar", "cost")):
            fields["verbatim_card_" + passage["role"]] = passage["text"]
    checks = []
    for role, phrases in (("available", available), ("unavailable", unavailable)):
        for phrase in phrases:
            wanted = set(tokens(phrase))
            spans = []
            for field, text in fields.items():
                for clause in re.split(r"(?<=[.;\n])\s+", text):
                    overlap = sorted(wanted & set(tokens(clause)))
                    if overlap:
                        spans.append({"field": field, "text": clause, "overlap": overlap})
            checks.append({"role": role, "input": phrase, "literal_spans": spans,
                           "state": "INSPECT POTENTIAL CONFLICT" if role == "unavailable" and spans else "NOT DISCHARGED"})
    return {"checks": checks, "compatibility": "NOT ESTABLISHED",
            "scope": "Literal premise triage only, including possible negated mentions. Available facts are not verified and no requirement is automatically discharged. Inspect full conditions, units, notices and governing source; use bridge for documented transfers."}


def exact_excerpt(value, query, budget):
    """Select bounded relevance fragments; never replace the complete field."""
    text = flatten(value)
    if len(text) <= budget:
        return text
    clauses = [x for x in re.split(r"(?<=[.;\n])\s+", text) if x]
    wanted = set(tokens(query))
    scored = sorted(enumerate(clauses),
                    key=lambda pair: (-len(wanted & set(tokens(pair[1]))), pair[0]))
    chosen, used = [], 0
    for index, clause in scored:
        take = clause[:max(0, budget - used)]
        if take:
            chosen.append((index, take))
            used += len(take) + 1
        if used >= budget:
            break
    return " ".join(text for _, text in sorted(chosen))


def qualified_views(record, frame, task):
    """Current, source-local relevance views; never inferred premises.

    Fields and notice prose stay separate from the statement/source views.
    Complete contracts, units and corrections remain in the operation packet.
    """
    header = record["title"] + "\n"
    names = ("requires", "returns", "conditions", "costs", "units", "obstruction")
    fields = [(name, frame[name]) for name in names]
    if any(not flatten(value).startswith(("UNKNOWN", "source-local;")) for _, value in fields):
        text = header + "\n".join(name + ": " + exact_excerpt(value, task, 192)
                                    for name, value in fields)
        yield "qualified_operation", text, None
    notices = record.get("notices", [])
    if notices:
        def notice_text(notice):
            return flatten({key: value for key, value in notice.items()
                            if key not in ("source_refs", "card_ids", "schema_version", "notice_id")})
        wanted = set(tokens(task))
        index, notice = max(enumerate(notices), key=lambda pair: (
            len(wanted & set(tokens(notice_text(pair[1])))), -pair[0]))
        yield "current_notice", header + exact_excerpt(notice_text(notice), task, 1400), index

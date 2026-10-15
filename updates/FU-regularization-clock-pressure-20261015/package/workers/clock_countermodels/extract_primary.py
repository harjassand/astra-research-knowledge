#!/usr/bin/env python3
"""Text extraction only. Preserve fetched bytes; record any MIME extraction."""
from email.parser import BytesParser
from email.policy import default
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
from pypdf import PdfReader

OUT = Path(__file__).resolve().parent


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style"]:
            self.skip += 1
        if tag in ["p", "h1", "h2", "h3", "h4", "div", "li", "tr", "section"]:
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in ["script", "style"] and self.skip:
            self.skip -= 1
        if tag in ["p", "h1", "h2", "h3", "h4", "div", "li", "tr", "section"]:
            self.parts.append("\n")
    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


rows = []
for path in sorted((OUT/"primary").iterdir()):
    if path.suffix not in [".pdf", ".html"] or path.stem.endswith("_extracted"):
        continue
    data = path.read_bytes()
    row = {"input": str(path), "input_sha256": hashlib.sha256(data).hexdigest()}
    if path.suffix == ".pdf":
        readpath = path
        if not data.startswith(b"%PDF"):
            first_line = data.split(b"\r\n", 1)[0]
            boundary = first_line[2:].decode("ascii")
            message = BytesParser(policy=default).parsebytes((f"Content-Type: multipart/form-data; boundary={boundary}\r\nMIME-Version: 1.0\r\n\r\n").encode()+data)
            parts = [p for p in message.iter_parts() if p.get_content_type() == "application/pdf"]
            assert len(parts) == 1
            pdfdata = parts[0].get_payload(decode=True)
            assert pdfdata.startswith(b"%PDF")
            readpath = path.with_name(path.stem+"_extracted.pdf")
            readpath.write_bytes(pdfdata)
            row.update({"mime_extracted_pdf": str(readpath), "mime_extracted_pdf_sha256": hashlib.sha256(pdfdata).hexdigest()})
        reader = PdfReader(readpath)
        text = "\n".join(f"\nPAGE {i+1}\n"+page.extract_text() for i,page in enumerate(reader.pages))
        row["pages"] = len(reader.pages)
    else:
        parser = TextParser()
        parser.feed(data.decode("utf-8", errors="replace"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines() if line.strip())
    txtpath = path.with_suffix(".txt")
    txtpath.write_text(text)
    row.update({"text_path": str(txtpath), "text_sha256": hashlib.sha256(txtpath.read_bytes()).hexdigest(), "text_chars": len(text)})
    rows.append(row)
(OUT/"primary_extraction_receipts.json").write_text(json.dumps(rows, indent=2)+"\n")
print(json.dumps(rows, indent=2))

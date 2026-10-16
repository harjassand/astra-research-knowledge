"""Validate source identity and acquire a primary-deposit prior-art copy if public."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

R=Path(__file__).resolve().parent
original=json.loads((R/"source_acquisition.json").read_text())
validated=[]
for row in original:
    item=row.copy()
    if row.get("path"):
        payload=(R/row["path"]).read_bytes()
        if row["name"]=="Lim2021_PMC.html" and b"Non-Faradaic Promotion of Ethylene Hydrogenation" not in payload:
            item["status"]="FAILED_OR_WRONG_CONTENT"
            item["validation_reason"]="HTTP 200 browser challenge, not article fulltext. Original acquisition receipt classified generic HTML too permissively; this content check supersedes it."
        elif row["name"]=="nature_landing.html":
            item["content_scope"]="Article title, abstract, references and source links only; subscription main text NOT acquired."
    validated.append(item)

url="https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8395646/fullTextXML"
entry={"name":"Lim2021_primary_deposit.xml","requested_url":url,"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
    response=urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Astra-scientific-source-audit/1.0"}),timeout=40)
except urllib.error.HTTPError as exc:
    response=exc
except Exception as exc:
    response=None
    entry.update(status="NETWORK_ERROR",error=repr(exc))
if response is not None:
    with response:
        payload=response.read()
        valid=(response.status==200 and b"Non-Faradaic Promotion of Ethylene Hydrogenation" in payload and b"jacsau.1c00044" in payload)
        path=R/"external_excluded_from_publication"/(entry["name"] if valid else entry["name"]+".failed_response")
        path.write_bytes(payload)
        entry.update(status="ACQUIRED_PRIMARY_FULLTEXT" if valid else "FAILED_OR_WRONG_CONTENT",status_code=response.status,bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest(),path=str(path.relative_to(R)))
        if valid:
            xml=ET.fromstring(payload)
            fragments=[]
            for node in xml.iter():
                if node.tag in {"article-title","title","p","table-wrap","supplementary-material"}:
                    fragments.append("".join(node.itertext()))
            path.with_suffix(".txt").write_text("\n\n".join(fragments))
validated.append(entry)
(R/"validated_source_acquisition.json").write_text(json.dumps(validated,indent=2)+"\n")
print(json.dumps(validated,indent=2))

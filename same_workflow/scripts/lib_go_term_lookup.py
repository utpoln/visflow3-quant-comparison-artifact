# Verbatim copy of the registered VisFlow library "go_term_lookup"
# (visflow-backend `libraries` table, Python, source fetched directly from
# the database — not reimplemented) so the computation this workflow
# performs is identical in every system it's ported to, not merely similar.
import requests, time

def run(input):
    terms = input if isinstance(input, list) else [input]
    results = []
    for go_id in terms:
        r = requests.get(f"https://api.geneontology.org/api/ontology/term/{go_id}", timeout=10)
        data = r.json() if r.ok else {}
        results.append({"go_id": go_id, "label": data.get("label",""),
                        "namespace": data.get("aspect",""), "definition": data.get("definition","")[:200] if data.get("definition") else ""})
        time.sleep(0.05)
    return results

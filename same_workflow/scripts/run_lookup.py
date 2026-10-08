#!/usr/bin/env python3
"""Pipeline step 1 (= the 'GO Term Lookup' Library node): read the GO ID
list, call the real library function, write its output."""
import argparse, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib_go_term_lookup import run

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

with open(args.input) as fh:
    go_ids = json.load(fh)

result = run(go_ids)
with open(args.out, "w") as fh:
    json.dump(result, fh, indent=2)
print(f"[run_lookup] {len(result)} rows -> {args.out}")

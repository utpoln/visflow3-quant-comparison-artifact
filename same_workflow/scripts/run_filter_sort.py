#!/usr/bin/env python3
"""Pipeline step 2 (= the 'Filter & Sort' Library node, via the Adapter
contract that wraps upstream rows as {"data": [...]} ): read step 1's
output, call the real library function, write the final result — this
file IS the workflow's RETURN value / Terminal output."""
import argparse, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib_filter_and_sort import run

ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

with open(args.input) as fh:
    go_details = json.load(fh)

result = run({"data": go_details})
with open(args.out, "w") as fh:
    json.dump(result, fh, indent=2)
print(f"[run_filter_sort] {len(result)} rows -> {args.out}")

#!/usr/bin/env python3
"""Step 1 of the naive-integration pipeline: load the raw negative/positive
case tables and flatten them into a plain correspondence-edge list — a
(source_id, target_gene_id) table. This is the single artifact a scientist
with no identity-mediation tool would naturally build first: "join the
bridge/alias table to the gene table." Snakemake, Nextflow, and CWL all
provide dataflow orchestration, not identifier semantics, so this step
looks the same in all three — the file exists so each tool's pipeline can
call the identical code rather than re-implementing it three times (the
measured outcome must be a property of the join strategy, not of which
tool happened to invoke it).

Input:  negative_cases.csv (bridge_id, bridge_type, target_ids, target_symbols)
        positive_cases.csv (old_id, true_gene_id, true_symbol)
Output: edges.csv (source, target) — one row per correspondence, exactly
        mirroring MapBasePlanner's own _build_snapshot() (table5_safety.py),
        since this experiment's whole point is to run the *same* benchmark
        through a different system's naive join, not a different benchmark.
"""
import argparse
import csv


def build_edges(negative_path, positive_path, out_path):
    edges = []
    with open(negative_path, newline="") as fh:
        for row in csv.DictReader(fh):
            for target_id in row["target_ids"].split("|"):
                edges.append((row["bridge_id"], target_id))
    with open(positive_path, newline="") as fh:
        for row in csv.DictReader(fh):
            edges.append((row["old_id"], row["true_gene_id"]))

    with open(out_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["source", "target"])
        w.writerows(edges)
    return len(edges)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--negative", required=True)
    ap.add_argument("--positive", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    n = build_edges(args.negative, args.positive, args.out)
    print(f"[build_edges] wrote {n} edges to {args.out}")

#!/usr/bin/env python3
"""Step 3: score a join's conclusions against the same two questions
MapBasePlanner's table5_safety.py asks of its own three semantics:

  false_merges  — of the 116 negative (over-merge) cases, how many pairs
                  of genuinely distinct target genes did this join
                  conclude are "the same" (same concluded_group)?
  recovered     — of the 100 positive (true-match) cases, how many old
                  identifiers did this join correctly place in the same
                  group as their one true current gene?

A negative case with target_ids [g1, g2, ..., gk] contributes a false
merge if ANY two of those k genuinely-distinct genes end up concluded
equal — matching MapBasePlanner's own pairwise check (it compares
target_ids[0] vs target_ids[1] per case; this script checks all pairs,
which is at least as strict, so it cannot under-count a result that
would otherwise look favourable to the naive join).
"""
import argparse
import csv
import itertools
import json


def load_groups(path):
    with open(path, newline="") as fh:
        return {row["node"]: row["concluded_group"] for row in csv.DictReader(fh)}


def evaluate(negative_path, positive_path, groups_path, mode, out_path):
    groups = load_groups(groups_path)

    false_merges = 0
    for row in csv.DictReader(open(negative_path, newline="")):
        target_ids = row["target_ids"].split("|")
        if any(
            groups.get(a) is not None and groups.get(a) == groups.get(b)
            for a, b in itertools.combinations(target_ids, 2)
        ):
            false_merges += 1

    recovered = 0
    for row in csv.DictReader(open(positive_path, newline="")):
        old_id, true_gene_id = row["old_id"], row["true_gene_id"]
        if groups.get(old_id) is not None and groups.get(old_id) == groups.get(true_gene_id):
            recovered += 1

    n_negative = sum(1 for _ in csv.DictReader(open(negative_path, newline="")))
    n_positive = sum(1 for _ in csv.DictReader(open(positive_path, newline="")))

    result = {
        "mode": mode,
        "false_merges": false_merges,
        "n_negative": n_negative,
        "recovered": recovered,
        "n_positive": n_positive,
    }
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=2)
    print(f"[evaluate:{mode}] false_merges={false_merges}/{n_negative}  "
          f"recovered={recovered}/{n_positive}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--negative", required=True)
    ap.add_argument("--positive", required=True)
    ap.add_argument("--groups", required=True)
    ap.add_argument("--mode", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    evaluate(args.negative, args.positive, args.groups, args.mode, args.out)

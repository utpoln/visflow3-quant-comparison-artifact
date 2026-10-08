#!/usr/bin/env python3
"""Step 2: the actual join. Two modes, both the ordinary, idiomatic way
anyone would write this in a Snakemake `script:`, a Nextflow process, or a
CWL CommandLineTool's base command — none of Snakemake, Nextflow, or CWL
provide an identifier-mediation primitive, so whichever of these two a
scientist reaches for is genuinely representative of what such a pipeline
does today, not a strawman built to lose:

  --mode exact        Join only on byte-identical string equality
                       (pandas `merge(..., how='inner')` on raw ids, or
                       equivalently `JOIN target.id = source.id` in SQL).
                       This is the most defensive thing to write.

  --mode transitive    Union-find over the edge table: if A and B are both
                       linked to the same bridge/alias, conclude A and B
                       are "the same" (transitively). This is what you get
                       the moment a pipeline chains more than one join
                       through a shared synonym/alias column — the single
                       most natural way to resolve old identifiers against
                       a current reference when nothing stops two
                       unrelated genes from sharing one historical alias.

Both are exactly the two baselines MapBasePlanner's own table5_safety.py
evaluates (`_syntactic_same` / `_transitive_closure_groups`) — this script
re-implements them standalone so a Snakemake/Nextflow/CWL pipeline can
run them without importing anything from that project, while remaining
answerable to the same corpus and the same question.

Output: concluded.csv (node, concluded_group) — the equivalence class each
node was placed in, consumed by evaluate.py.
"""
import argparse
import csv


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry


def load_edges(path):
    with open(path, newline="") as fh:
        return [(row["source"], row["target"]) for row in csv.DictReader(fh)]


def run_exact(edges):
    """Each node is its own group under byte-identical equality — i.e. two
    nodes are "the same" only if they are literally the same string."""
    nodes = {n for e in edges for n in e}
    return {n: n for n in nodes}


def run_transitive(edges):
    uf = UnionFind()
    for a, b in edges:
        uf.union(a, b)
    nodes = {n for e in edges for n in e}
    return {n: uf.find(n) for n in nodes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--edges", required=True)
    ap.add_argument("--mode", required=True, choices=["exact", "transitive"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    edges = load_edges(args.edges)
    groups = run_exact(edges) if args.mode == "exact" else run_transitive(edges)

    with open(args.out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["node", "concluded_group"])
        for node, group in sorted(groups.items()):
            w.writerow([node, group])
    print(f"[naive_join:{args.mode}] wrote {len(groups)} node assignments to {args.out}")


if __name__ == "__main__":
    main()

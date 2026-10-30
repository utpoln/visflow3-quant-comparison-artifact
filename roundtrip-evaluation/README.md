# VisFlow 3.0 Φ/Ψ Round-Trip Evaluation

**This is a separate evaluation from the rest of this repository.** The rest
of this repo backs dissertation §7.4 (the Nextflow/Snakemake/CWL
comparison). This subfolder backs a different claim entirely — Chapter 6's
"Empirical Support for the Projection" section, which tests whether the
VisFlow 3.0 reference implementation's `Φ` (`translateGraphToAst` +
`printProgram`) and `Ψ` (`parseProgram`) functions round-trip exactly
(`Ψ(Φ(G)) = G`) over the real VisFlow 2.0 workflow corpus. It lives here
rather than in its own repository as a pragmatic choice, not because the two
evaluations are related.

## What this is

`verify_roundtrip.mjs` is a standalone script that re-runs this claim
end to end: given a restored copy of the real production database, it
attempts to translate every workflow's canvas graph to an AST, print that
AST to Necto text, parse the text back to an AST, and checks the result is
structurally identical to the original (ignoring `LAYOUT`, which is
presentational). It calls the application's own, unmodified
`src/necto/translator.js`, `printer.js`, and `parser.js` — it does not
reimplement or approximate any part of Φ or Ψ.

It is not runnable standalone: it depends on the VisFlow backend
application's own `src/necto/` modules and `pg` driver, and on a Postgres
instance holding the real workflow corpus. The application source is not
distributed here (same scope boundary as the rest of this repo and its
sibling evaluation repos — see the main README's "Related artifacts").

## How to reproduce

1. Copy `verify_roundtrip.mjs` into the root of a checkout of the VisFlow
   backend application.
2. Restore a copy of the production database dump into a disposable
   Postgres instance.
3. Run:
   ```bash
   DB_HOST=localhost DB_PORT=5432 DB_NAME=<restored-db> \
   DB_USER=<user> DB_PASSWORD=<password> node verify_roundtrip.mjs
   ```
4. The script only ever issues `SELECT` queries — nothing in the database is
   modified.

## Results

See `results.json` for the full machine-readable output. Summary:

| | Count |
|---|---|
| Total corpus | 449 (106 Taverna-seeded, 5 paper examples, 338 developer/user-created) |
| Excluded (empty / no valid version) | 3 |
| Sampled | 446 |
| Filtered (unsupported construct) | 57 |
| In scope | 389 |
| Round-tripped exactly (`Ψ(Φ(G)) = G`) | **389 / 389 = 100%** |

**Why 57 were filtered**, broken down in `results.json`'s
`unsupported_reasons`:

- 27 use a control-flow node type the translator does not attempt (`If`,
  `Repeat`, `Procedure`, `IO`, `Wait On`, `Connect`) — composite control flow
  the scheduler can run but the canvas has no node type to draw yet.
- 16 have a `Data` node bound to a resource type the translator does not yet
  recognize (`ftp`, `excel`, `xml`, `database`, `web_wrapper`,
  `web_scraper`) — it currently only handles `rest_api` and `static`
  resources.
- 7 have more than one sink node (`Terminal`/`Printer`) — the translator
  only represents a single `RETURN`.
- 4 `Combine` and 1 `Fusion` node have no explicit, translator-inspectable
  join key (the key is only auto-detected at runtime by VisFlow 2.0's own
  executor, which this offline translator does not call).
- 1 `Adapter` node has no resolvable function; 1 sink has an unexpected
  input-arity shape.

None of these 57 are a counterexample to the bijection theorem itself — the
theorem is about the notation (what a well-formed `Φ`-domain program
satisfies), not about this specific, intentionally offline reference
implementation's current coverage of VisFlow 2.0's full node-type surface.
The 100% round-trip rate is over every workflow the implementation
*attempts*, exactly as Chapter 6 states.

## Provenance note

This evaluation was re-run in full against a restored copy of the real
production database as part of a pre-submission accuracy pass. An earlier
draft of Chapter 6 reported different sub-counts (429 sampled / 33 filtered
/ 396 in-scope) from an evaluation run whose exact filtering criteria were
not preserved; this script and `results.json` are the current, reproducible
source of truth, and the dissertation text was updated to match.

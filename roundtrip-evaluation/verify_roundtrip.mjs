// VisFlow 3.0 Phi/Psi round-trip verification.
//
// Re-runs the dissertation's Chapter 6 empirical-support claim
// (Section "Empirical Support for the Projection") against a restored copy
// of the real VisFlow 2.0 production database: for every workflow in the
// corpus, attempt translateGraphToAst (Phi), then printProgram + parseProgram
// (Psi), and check that the round trip is exact.
//
// Run from a checkout of the VisFlow backend (github.com/utpoln — private
// application repo), with this script copied into its root, against a
// Postgres instance holding a restored copy of the production dump:
//
//   DB_HOST=localhost DB_PORT=5432 DB_NAME=visflow_check \
//   DB_USER=check DB_PASSWORD=check node verify_roundtrip.mjs
//
// Only depends on the application's own src/necto/{translator,printer,parser}.js
// and the `pg` driver — no other application code is touched, and nothing in
// the database is mutated (every query here is a SELECT).
import pg from 'pg';
import { translateGraphToAst, UnsupportedWorkflowError } from './src/necto/translator.js';
import { printProgram } from './src/necto/printer.js';
import { parseProgram } from './src/necto/parser.js';

const pool = new pg.Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'visflow',
  user: process.env.DB_USER || 'postgres',
  password: process.env.DB_PASSWORD || '',
});

function sortDeep(x) {
  if (Array.isArray(x)) return x.map(sortDeep);
  if (x && typeof x === 'object') {
    return Object.fromEntries(Object.keys(x).sort().map(k => [k, sortDeep(x[k])]));
  }
  return x;
}
function roundTripsExactly(astBack, ast) {
  const { layout: la, ...ca } = ast;
  const { layout: lb, ...cb } = astBack;
  return JSON.stringify(sortDeep(ca)) === JSON.stringify(sortDeep(cb));
}

const { rows: workflows } = await pool.query(
  `SELECT id, user_id, name, current_version FROM workflows ORDER BY created_at ASC`
);
console.log('total workflows in corpus:', workflows.length);

const userIds = [...new Set(workflows.map(w => w.user_id))];
const resourcesByUser = {}, librariesByUser = {};
for (const uid of userIds) {
  const { rows: res } = await pool.query(`SELECT id, name, type, config FROM resources WHERE user_id=$1`, [uid]);
  const { rows: libs } = await pool.query(`SELECT id, name FROM libraries WHERE user_id=$1`, [uid]);
  resourcesByUser[uid] = res;
  librariesByUser[uid] = libs;
}

let nEmpty = 0, nUnsupported = 0, nOtherError = 0, nTranslated = 0, nRoundTripExact = 0, nRoundTripMismatch = 0;
const unsupportedReasons = {};

for (const wf of workflows) {
  const { rows: vrows } = await pool.query(
    `SELECT nodes, edges FROM workflow_versions WHERE workflow_id=$1 AND version=$2`,
    [wf.id, wf.current_version]
  );
  const nodes = vrows[0]?.nodes || [];
  const edges = vrows[0]?.edges || [];
  if (!vrows.length || !nodes.length) { nEmpty++; continue; }

  let ast;
  try {
    ast = translateGraphToAst(nodes, edges, wf.name, resourcesByUser[wf.user_id] || [], librariesByUser[wf.user_id] || []);
  } catch (e) {
    if (e instanceof UnsupportedWorkflowError) {
      nUnsupported++;
      const reason = e.message.split(':')[0].trim();
      unsupportedReasons[reason] = (unsupportedReasons[reason] || 0) + 1;
    } else {
      nOtherError++;
    }
    continue;
  }
  nTranslated++;

  try {
    const text = printProgram(ast);
    const astBack = parseProgram(text);
    if (roundTripsExactly(astBack, ast)) nRoundTripExact++;
    else nRoundTripMismatch++;
  } catch {
    nRoundTripMismatch++;
  }
}

console.log(JSON.stringify({
  total_corpus: workflows.length,
  excluded_empty_or_versionless: nEmpty,
  sampled: workflows.length - nEmpty,
  filtered_unsupported_construct: nUnsupported,
  other_translate_error: nOtherError,
  in_scope: nTranslated,
  round_trip_exact: nRoundTripExact,
  round_trip_mismatch: nRoundTripMismatch,
  unsupported_reasons: unsupportedReasons,
}, null, 2));

await pool.end();

const assert = require('node:assert/strict');
const {createHash, webcrypto} = require('node:crypto');
const {readFileSync} = require('node:fs');
const {join} = require('node:path');
const vm = require('node:vm');

const hash = text => createHash('sha256').update(text).digest('hex');
const script = readFileSync(join(__dirname, 'search.js'), 'utf8');
const shard = hash('mechanism').slice(0, 2);

function epoch(label, score) {
  const files = {
    'current/catalog.json': JSON.stringify({concepts: [], shards: [shard], lexical_shards: [],
      documents: [[0, false]], records: [{record_id: 'U-fixture', title: `Epoch ${label}`,
        kind: 'mechanism', parents: []}]}),
    [`current/postings/${shard}.json`]: JSON.stringify({mechanism: [[0, score]]}),
    'current/packets/U-fixture.json': JSON.stringify({id: 'U-fixture', title: `Epoch ${label}`, statement: `Premise ${label}`,
      contract: {assumptions: `Conditions ${label}`}, review_overlays: [], review: {}, notices: [], evidence: []}),
  };
  return {files, manifest: {input_version: hash(label),
    outputs: Object.fromEntries(Object.entries(files).map(([path, text]) => [`knowledge/${path}`, hash(text)]))}};
}

class Element {
  constructor(tag) {
    this.tag = tag;
    this.children = [];
    this.listeners = new Map();
    this.textContent = '';
    this.value = '';
    this.disabled = false;
  }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children = children; }
  addEventListener(name, callback) { this.listeners.set(name, callback); }
}

function harness(initial, cached = initial) {
  let server = initial;
  let paused;
  const requests = [];
  const cache = new Map(Object.entries(cached.files));
  const elements = Object.fromEntries(['status', 'results', 'query', 'search'].map(name => [name, new Element(name)]));
  const document = {querySelector: selector => elements[selector.slice(1)], createElement: tag => new Element(tag),
    createTextNode: text => Object.assign(new Element('#text'), {textContent: text})};
  const fetch = async (url, options = {}) => {
    const path = url.split('?')[0];
    requests.push({url, cache: options.cache});
    const available = path === 'current/search_manifest.json' ? JSON.stringify(server.manifest) : server.files[path];
    const body = options.cache !== 'no-store' && cache.has(url) ? cache.get(url) : available;
    if (paused && paused.path === path) {
      const gate = paused;
      paused = undefined;
      gate.reached();
      await gate.release;
    }
    if (body !== undefined && options.cache !== 'no-store') cache.set(url, body);
    return {ok: body !== undefined, text: async () => body, json: async () => JSON.parse(body)};
  };
  vm.runInNewContext(script, {document, fetch, TextEncoder, crypto: webcrypto});
  return {
    elements, requests,
    setEpoch: next => { server = next; },
    submit: async (query = 'mechanism') => {
      elements.query.value = query;
      await elements.search.listeners.get('submit')({preventDefault() {}});
    },
    pauseNext: path => {
      let reached;
      let release;
      const arrived = new Promise(resolve => { reached = resolve; });
      const gate = new Promise(resolve => { release = resolve; });
      paused = {path, reached, release: gate};
      return {arrived, release};
    },
  };
}

const descendants = element => [element, ...element.children.flatMap(descendants)];
const heading = browser => browser.elements.results.children[0]?.children.find(element => element.tag === 'h2')?.textContent;
const button = browser => browser.elements.results.children[0].children.find(element => element.tag === 'button');

async function updateWithoutReload() {
  const first = epoch('first', 1);
  const second = epoch('second', 2);
  const browser = harness(first);
  await browser.submit();
  assert.equal(heading(browser), 'Epoch first');
  const oldButton = button(browser);
  browser.setEpoch(second);
  await oldButton.listeners.get('click')();
  assert.match(oldButton.textContent, /Mixed or changed dataset/);
  assert.match(oldButton.textContent, /Search again/);
  assert.equal(oldButton.disabled, false);
  await browser.submit();
  assert.equal(heading(browser), 'Epoch second');
  assert.match(browser.elements.status.textContent, new RegExp(second.manifest.input_version.slice(0, 12)));
  await button(browser).listeners.get('click')();
  const article = browser.elements.results.children[0];
  assert.match(descendants(article).find(element => element.tag === 'pre').textContent, /Premise second/);
  assert.match(article.children.find(element => element.tag === 'a').href, /\?sha256=[0-9a-f]{64}$/);
  assert.equal(browser.requests.filter(request => request.url === 'current/search_manifest.json').length, 2);
  assert.ok(browser.requests.every(request => request.cache === 'no-store'));
  assert.ok(browser.requests.filter(request => request.url !== 'current/search_manifest.json')
    .every(request => /\?sha256=[0-9a-f]{64}$/.test(request.url)));
  const reloaded = harness(second, first);
  await reloaded.submit();
  assert.equal(heading(reloaded), 'Epoch second');
}

async function rejectAndRecover() {
  const current = epoch('recoverable', 3);
  const path = `current/postings/${shard}.json`;
  const original = current.files[path];
  current.files[path] = JSON.stringify({mechanism: [[0, 99]]});
  const browser = harness(current);
  await browser.submit();
  assert.match(browser.elements.status.textContent, /Mixed or changed dataset/);
  assert.equal(browser.elements.results.children.length, 0);
  current.files[path] = original;
  await browser.submit();
  assert.equal(heading(browser), 'Epoch recoverable');
}

async function olderRequestCannotPublish() {
  const browser = harness(epoch('old-request', 1));
  const pause = browser.pauseNext('current/catalog.json');
  const older = browser.submit();
  await pause.arrived;
  browser.setEpoch(epoch('latest-request', 2));
  await browser.submit();
  assert.equal(heading(browser), 'Epoch latest-request');
  const latestStatus = browser.elements.status.textContent;
  pause.release();
  await older;
  assert.equal(heading(browser), 'Epoch latest-request');
  assert.equal(browser.elements.status.textContent, latestStatus);
}


async function intermediateCorrectionRoute() {
  const current = epoch('intermediate-route', 4);
  const parent = JSON.parse(current.files['current/packets/U-fixture.json']);
  parent.related_units = [{id: 'U-step', title: 'Full residual', packet: 'knowledge/current/packets/U-step.json'}];
  const edge = {id: 'B-route', from: 'U-step', to: 'U-replacement', state: 'REFUTED TRANSFER',
    scope: 'A reversible lower bound does not transfer to circulation.',
    remaining_obligations: 'Supply the weighted adjoint and both full residuals.', authority: 'knowledge/transfers/B-route.json'};
  const step = {id: 'U-step', title: 'Full residual', statement: 'A conditional premise', contract: {},
    review_overlays: [], review: {}, notices: [{notice_id: 'SN-failure', clarification: 'One-sided bound fails.'}], evidence: [], transfers: [edge]};
  const replacement = {...step, id: 'U-replacement', title: 'Primal and dual', statement: 'Two-sided replacement'};
  for (const [name, packet] of [['U-fixture', parent], ['U-step', step], ['U-replacement', replacement]]) {
    const path = `current/packets/${name}.json`;
    current.files[path] = JSON.stringify(packet);
    current.manifest.outputs[`knowledge/${path}`] = hash(current.files[path]);
  }
  const browser = harness(current);
  const findButton = label => descendants(browser.elements.results).find(element => element.tag === 'button' && element.textContent.startsWith(label));
  await browser.submit();
  await button(browser).listeners.get('click')();
  const intermediate = findButton('Read intermediate operation');
  assert.ok(intermediate);
  const path = 'current/packets/U-step.json';
  const original = current.files[path];
  current.files[path] = JSON.stringify({...step, statement: 'Unregistered changed premise'});
  await intermediate.listeners.get('click')();
  assert.match(intermediate.textContent, /Mixed or changed dataset/);
  current.files[path] = original;
  await intermediate.listeners.get('click')();
  assert.ok(descendants(browser.elements.results).some(element => element.textContent.includes('One-sided bound fails.')));
  assert.ok(descendants(browser.elements.results).some(element => element.tag === 'strong' && element.textContent === 'REFUTED TRANSFER: '));
  const connected = findButton('Read connected operation');
  assert.ok(connected);
  await connected.listeners.get('click')();
  assert.ok(descendants(browser.elements.results).some(element => element.tag === 'pre' && element.textContent.includes('Two-sided replacement')));
  assert.equal(descendants(browser.elements.results).filter(element => element.tag === 'button' && element.textContent === 'Read connected operation: U-step').length, 0);
  assert.ok(browser.requests.filter(request => request.url.includes('/packets/')).every(request => /\?sha256=[0-9a-f]{64}$/.test(request.url)));
}

async function identifierRoutes() {
  const records = [
    {record_id: 'N120-parent', title: 'Broad high-scoring parent', kind: 'result', parents: []},
    ...Array.from({length: 7}, (_, index) => ({record_id: `U120-step-${index}`, title: `Buried step ${index}`,
      kind: 'mechanism', parents: ['N120-parent']})),
    {record_id: 'LA012-conditioned', title: 'Atlas premise', kind: 'lemma', parents: ['N120-parent']},
    {record_id: 'P-checks', title: 'Named protocol', kind: 'protocol', parents: []},
  ];
  const current = epoch('identifier-routes', 1);
  current.files['current/catalog.json'] = JSON.stringify({concepts: [], shards: [shard], lexical_shards: [],
    documents: records.map((_, index) => [index, false]), records});
  current.files[`current/postings/${shard}.json`] = JSON.stringify({mechanism: [[0, 100], [1, 1]]});
  for (const record of records) {
    const route = record.record_id.replace(/^([NL]\d+)-.*$/, '$1');
    current.files[`current/packets/${route}.json`] = JSON.stringify({id: record.record_id, title: record.title,
      statement: `Exact ${record.record_id} premise`, contract: {assumptions: 'Supplied interface required'},
      review_overlays: [], review: {}, notices: [{notice_id: 'SN-scope', clarification: 'No acquired device evidence.'}], evidence: []});
  }
  current.manifest.outputs = Object.fromEntries(Object.entries(current.files).map(([path, text]) => [`knowledge/${path}`, hash(text)]));
  const browser = harness(current);
  const ids = () => browser.elements.results.children.map(article => article.children.find(element => element.tag === 'a').textContent.split(' — ')[0]);
  await browser.submit();
  assert.equal(heading(browser), 'Broad high-scoring parent');
  await browser.submit('  u120-STEP-0  ');
  assert.deepEqual(ids(), ['U120-step-0']);
  assert.match(browser.elements.status.textContent, /1 identifier match/);
  await button(browser).listeners.get('click')();
  assert.ok(descendants(browser.elements.results).some(element => element.tag === 'pre' && element.textContent.includes('Exact U120-step-0 premise') && element.textContent.includes('No acquired device evidence.')));
  await browser.submit('U120');
  assert.equal(ids().length, 7); // Ambiguity is not silently cut to five ranked hits.
  assert.deepEqual(ids(), records.slice(1, 8).map(record => record.record_id));
  assert.match(browser.elements.status.textContent, /7 records share this identifier prefix/);
  for (const missing of ['U999', 'U120-step', 'U120-step-99']) {
    await browser.submit(missing);
    assert.equal(browser.elements.results.children.length, 0);
    assert.match(browser.elements.status.textContent, /No current record matches this identifier/);
  }
  await browser.submit('n120');
  assert.deepEqual(ids(), ['N120-parent']);
  assert.match(browser.elements.results.children[0].children.find(element => element.tag === 'a').href, /\/N120.json\?sha256=/);
  await browser.submit('la012');
  assert.deepEqual(ids(), ['LA012-conditioned']);
  await browser.submit('p-checks');
  assert.deepEqual(ids(), ['P-checks']);
  await browser.submit('T2 relaxation mechanism');
  assert.equal(heading(browser), 'Broad high-scoring parent');
  // Exact lookup still uses the current manifest and packet byte guards.
  await browser.submit('U120-step-0');
  current.files['current/packets/U120-step-0.json'] += ' ';
  await button(browser).listeners.get('click')();
  assert.match(button(browser).textContent, /Mixed or changed dataset/);
  assert.ok(browser.requests.every(request => request.cache === 'no-store'));
}

async function currentAuthorityPriority() {
  const current = epoch('current-authority', 1);
  const acceptance = [{status: 'CORRECT_AND_ACCEPTED', kind: 'human_acceptance_instruction',
    subject: {id: 'U-fixture', content_version: 'a'.repeat(64)}, new_audit: false,
    legacy_status_fields_are_historical: true, scope: 'The same finite conditional source.'}];
  const catalog = JSON.parse(current.files['current/catalog.json']);
  catalog.records[0].acceptance = acceptance;
  current.files['current/catalog.json'] = JSON.stringify(catalog);
  const packet = JSON.parse(current.files['current/packets/U-fixture.json']);
  packet.current_acceptance = acceptance;
  packet.current_consumer = {scope: 'Current accepted scope; original source retained.'};
  packet.statement = 'The same accepted conditional premise';
  packet.scientific_card_excerpt = {text: 'Historical unreviewed source claim', scope: 'Historical'};
  packet.contract = {requires: 'Actual finite input', assumptions: 'Independent noise remains required', units: 'seconds'};
  packet.review = {acceptance: 'historical_unreviewed'};
  current.files['current/packets/U-fixture.json'] = JSON.stringify(packet);
  current.manifest.outputs = Object.fromEntries(Object.entries(current.files).map(([path, text]) => [`knowledge/${path}`, hash(text)]));
  const browser = harness(current);
  await browser.submit();
  assert(descendants(browser.elements.results).some(e => e.tag === 'strong' && e.textContent.includes('CORRECT_AND_ACCEPTED')));
  await button(browser).listeners.get('click')();
  const rendered = JSON.parse(descendants(browser.elements.results).find(e => e.tag === 'pre').textContent);
  assert.equal(rendered.statement, packet.statement);
  assert.equal(rendered.acceptance[0].new_audit, false);
  assert.equal(rendered.contract.assumptions, 'Independent noise remains required');
  assert(!rendered.historical_reported_status);
  assert(!rendered.review.acceptance);
  assert.match(rendered.review.context, /not a new audit/);
}

(async () => {
  await updateWithoutReload();
  await rejectAndRecover();
  await olderRequestCannotPublish();
  await intermediateCorrectionRoute();
  await identifierRoutes();
  await currentAuthorityPriority();
  process.stdout.write('6 static web cache/epoch/interface/identifier/authority scenarios passed\n');
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });

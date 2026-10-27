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
    submit: async () => {
      elements.query.value = 'mechanism';
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

(async () => {
  await updateWithoutReload();
  await rejectAndRecover();
  await olderRequestCannotPublish();
  await intermediateCorrectionRoute();
  process.stdout.write('4 static web cache/epoch/interface scenarios passed\n');
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exitCode = 1; });

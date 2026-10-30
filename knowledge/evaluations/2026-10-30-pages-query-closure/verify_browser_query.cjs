// Real staged/public browser code, including natural-query shard fetches.
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const assert = require('node:assert/strict'), {webcrypto} = require('node:crypto');
const location = process.argv[2], output = process.argv[3];
const remote = /^https:\/\//.test(location), requests = [];
const load = async name => {
  if (remote) {
    const response = await fetch(new URL(name, location), {cache: 'no-store', signal: AbortSignal.timeout(45000)});
    requests.push({path: name, status: response.status}); assert(response.ok, name);
    return response.text();
  }
  requests.push({path: name, transport: 'actual staged file'});
  return fs.readFileSync(path.join(location, name.split('?')[0]), 'utf8');
};
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.listeners = new Map(); this.textContent = ''; this.value = ''; }
  append(...items) { this.children.push(...items); }
  replaceChildren(...items) { this.children = items; }
  addEventListener(name, callback) { this.listeners.set(name, callback); }
}
const all = element => [element, ...element.children.flatMap(all)];
(async () => {
  const html = await load('knowledge/index.html'), code = await load('knowledge/search.js');
  const marker = JSON.parse(html.match(/<script id="publication" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  const elements = Object.fromEntries(['status', 'results', 'query', 'search', 'publication'].map(id => [id, new Element(id)]));
  elements.publication.textContent = JSON.stringify(marker);
  const document = {querySelector: selector => elements[selector.slice(1)], createElement: tag => new Element(tag), createTextNode: text => Object.assign(new Element('#text'), {textContent: text})};
  vm.runInNewContext(code, {document, fetch: async name => ({ok: true, text: async () => load('knowledge/' + name)}), TextEncoder, crypto: webcrypto});
  const results = [];
  for (const [query, family] of [
    ['finite bandwidth covariance outside envelope sensor floor', /[NU]1338(?:-|\.json)/],
    ['ordered word inverse Jordan compiler', /[NU]675(?:-|\.json)/]
  ]) {
    const start = requests.length;
    elements.query.value = query;
    await elements.search.listeners.get('submit')({preventDefault() {}});
    assert(elements.status.textContent.includes('ranked candidates'), elements.status.textContent);
    assert(elements.status.textContent.includes(marker.input_version.slice(0, 12)));
    const article = elements.results.children.find(article => all(article).some(element => element.tag === 'a' && family.test(element.textContent)));
    assert(article, query);
    await article.children.find(element => element.tag === 'button').listeners.get('click')();
    const packet = all(article).find(element => element.tag === 'pre'); assert(packet, query);
    const sourceLinks = all(article).filter(element => element.tag === 'a' && element.href?.startsWith('https://raw.githubusercontent.com/'));
    assert(sourceLinks.length && sourceLinks.every(element => element.href.includes('/' + marker.source_revision + '/')));
    const reads = requests.slice(start);
    results.push({query, status: elements.status.textContent, packet: JSON.parse(packet.textContent), source_urls: sourceLinks.map(element => element.href), requests: reads});
  }
  for (const folder of ['postings', 'lexical']) assert(requests.some(request => request.path.startsWith('knowledge/current/' + folder + '/')));
  const result = {result: 'pass', source_revision: marker.source_revision, input_version: marker.input_version, transport: remote ? 'actual anonymous HTTP' : 'actual staged files', results, scope: 'Exposed source-informed browser-query regressions, not held-out retrieval or scientific acceptance. Actual source HTTP/ranges are checked separately.'};
  if (output) fs.writeFileSync(output, JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify({result: result.result, source_revision: marker.source_revision, input_version: marker.input_version, queries: results.map(result => result.query), transport: result.transport}));
})().catch(error => {console.error(error); process.exitCode = 1;});

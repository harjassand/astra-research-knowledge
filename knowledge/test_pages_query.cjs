// Execute a real staged natural-language query; exact IDs bypass both shards.
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const assert = require('node:assert/strict'), {webcrypto} = require('node:crypto');
const root = process.argv[2];
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.listeners = new Map(); this.textContent = ''; this.value = ''; }
  append(...items) { this.children.push(...items); }
  replaceChildren(...items) { this.children = items; }
  addEventListener(name, callback) { this.listeners.set(name, callback); }
}
const all = element => [element, ...element.children.flatMap(all)];
(async () => {
  const elements = Object.fromEntries(['status', 'results', 'query', 'search', 'publication'].map(id => [id, new Element(id)]));
  elements.publication.textContent = fs.readFileSync(path.join(root, 'knowledge/index.html'), 'utf8').match(/<script id="publication" type="application\/json">([\s\S]*?)<\/script>/)[1];
  const requests = [];
  const fetch = async request => {
    const name = request.split('?')[0]; requests.push(name);
    const file = path.join(root, 'knowledge', name);
    return {ok: fs.existsSync(file), text: async () => fs.readFileSync(file, 'utf8')};
  };
  const document = {querySelector: selector => elements[selector.slice(1)], createElement: tag => new Element(tag), createTextNode: text => Object.assign(new Element('#text'), {textContent: text})};
  vm.runInNewContext(fs.readFileSync(path.join(root, 'knowledge/search.js'), 'utf8'), {document, fetch, TextEncoder, crypto: webcrypto});
  elements.query.value = 'probe mechanism';
  await elements.search.listeners.get('submit')({preventDefault() {}});
  assert(elements.status.textContent.includes('1 ranked candidates'), elements.status.textContent);
  assert(requests.some(name => name.startsWith('current/postings/')));
  assert(requests.some(name => name.startsWith('current/lexical/')));
  const article = elements.results.children[0]; assert(article);
  await article.children.find(element => element.tag === 'button').listeners.get('click')();
  assert(all(article).some(element => element.tag === 'pre' && element.textContent.includes('Conditional result')));
  assert(all(article).some(element => element.tag === 'a' && element.href.startsWith('https://raw.githubusercontent.com/')));
  console.log('Staged natural query, both shard lanes, compact packet and pinned source route pass.');
})().catch(error => {console.error(error); process.exitCode = 1;});

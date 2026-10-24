const status = document.querySelector('#status');
const results = document.querySelector('#results');
const stop = new Set(('a an the and or but if then as at by for from in into of on to with under this that these those is are was were be been being do does did can could should would will may might describe find want need using use').split(' '));
const tokenize = text => (text.normalize('NFKC').toLowerCase().replaceAll('_', ' ').match(/[\p{L}\p{N}]+/gu) || []).filter(word => word.length > 1 && !stop.has(word));
const bytes = new TextEncoder();
const sha = async text => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes.encode(text)))].map(value => value.toString(16).padStart(2, '0')).join('');
const searchManifest = fetch('current/search_manifest.json', {cache: 'no-store'}).then(response => { if (!response.ok) throw Error('Search manifest unavailable'); return response.json(); });
const readJSON = async path => {
  const manifest = await searchManifest;
  const response = await fetch(path);
  if (!response.ok) throw Error(`${path} unavailable`);
  const text = await response.text();
  if (await sha(text) !== manifest.outputs[`knowledge/${path}`]) throw Error(`Mixed or changed dataset: ${path}`);
  return JSON.parse(text);
};
const catalog = readJSON('current/catalog.json');
const shards = new Map();
const loadShard = (shard, folder = 'postings') => {
  const key = `${folder}/${shard}`;
  if (!shards.has(key)) shards.set(key, readJSON(`current/${key}.json`));
  return shards.get(key);
};
let generation = 0;
document.querySelector('#search').addEventListener('submit', async event => {
  event.preventDefault();
  const request = ++generation;
  results.replaceChildren();
  status.textContent = 'Searching cited content and operation contracts…';
  try {
    const data = await catalog;
    const original = new Set(tokenize(document.querySelector('#query').value));
    const terms = new Map([...original].map(term => [term, 1]));
    const expanded = [];
    for (const concept of data.concepts) {
      if (concept.phrases.some(phrase => { const trigger = tokenize(phrase); return trigger.length && trigger.every(term => original.has(term)); })) {
        for (const term of tokenize(concept.terms.join(' '))) if (!terms.has(term)) { terms.set(term, .35); expanded.push(term); }
      }
    }
    const scores = new Map();
    const lexicalScores = new Map();
    for (const [term, weight] of terms) {
      const shard = (await sha(term)).slice(0, 2);
      const postings = data.shards.includes(shard) ? await loadShard(shard) : {};
      for (const [index, score] of postings[term] || []) scores.set(index, (scores.get(index) || 0) + weight * score);
      if (original.has(term) && data.lexical_shards.includes(shard)) {
        const lexical = await loadShard(shard, 'lexical');
        for (const [index, score] of lexical[term] || []) lexicalScores.set(index, (lexicalScores.get(index) || 0) + score);
      }
    }
    if (request !== generation) return;
    const seen = new Set();
    const selected = [];
    for (const [index, score] of [...scores].sort((left, right) => right[1] - left[1] || left[0] - right[0])) {
      const [recordIndex, isSource] = data.documents[index];
      const match = {...data.records[recordIndex], kind: isSource ? 'source_window' : data.records[recordIndex].kind};
      const group = match.parents[0] || match.record_id;
      if (seen.has(group)) continue;
      seen.add(group);
      selected.push({...match, score});
      if (selected.length === 5) break;
    }
    const lexicalWinner = [...lexicalScores].sort((left, right) => right[1] - left[1] || left[0] - right[0])[0];
    if (lexicalWinner) {
      const match = data.records[data.documents[lexicalWinner[0]][0]];
      if (!seen.has(match.record_id)) {
        if (selected.length === 5) selected.pop();
        selected.push({...match, score: lexicalWinner[1], safety: true});
      }
    }
    const manifest = await searchManifest;
    status.textContent = `${selected.length} ranked candidates, not applicability verdicts. Dataset ${manifest.input_version.slice(0, 12)}. ${expanded.length ? 'Expanded terms: ' + [...new Set(expanded)].join(', ') : ''}`;
    for (const candidate of selected) {
      const article = document.createElement('article');
      const heading = document.createElement('h2');
      heading.textContent = candidate.title;
      const link = document.createElement('a');
      const short = candidate.record_id.replace(/^([NL]\d+)-.*$/, '$1');
      link.href = `current/packets/${encodeURIComponent(short)}.json`;
      link.textContent = `${candidate.record_id} — exact packet, conditions, notices and sources`;
      const note = document.createElement('p');
      note.className = 'note';
      note.textContent = `${candidate.kind}; ${candidate.safety ? 'full-card lexical safety lane, independent score scale' : 'content/contract lane'}; score ${candidate.score.toFixed(2)}. Similar wording does not establish composition.`;
      const expand = document.createElement('button');
      expand.textContent = 'Read compact packet';
      expand.addEventListener('click', async () => {
        expand.disabled = true;
        try {
          const packet = await readJSON(`current/packets/${encodeURIComponent(short)}.json`);
          const text = document.createElement('pre');
          text.textContent = JSON.stringify({statement: packet.statement, contract: packet.contract, review: packet.review_overlays.length ? packet.review_overlays : packet.review, notices: packet.notices, evidence: packet.evidence}, null, 2);
          article.append(text);
          for (const reference of packet.evidence) {
            const source = document.createElement('a');
            source.href = '../' + (reference.read_path || reference.path).split('/').map(encodeURIComponent).join('/');
            source.textContent = `Read source: ${reference.path} — lines ${JSON.stringify(reference.lines)}, SHA ${reference.sha256}`;
            const paragraph = document.createElement('p');
            paragraph.append(source);
            article.append(paragraph);
          }
        } catch (error) { expand.textContent = error.message; expand.disabled = false; }
      });
      article.append(heading, link, note, expand);
      results.append(article);
    }
  } catch (error) { if (request === generation) status.textContent = `Access failure: ${error.message}. Use the pinned raw packet route in README.md.`; }
});

const status = document.querySelector('#status');
const results = document.querySelector('#results');
const stop = new Set(('a an the and or but if then as at by for from in into of on to with under this that these those is are was were be been being do does did can could should would will may might describe find want need using use').split(' '));
const tokenize = text => (text.normalize('NFKC').toLowerCase().replaceAll('_', ' ').match(/[\p{L}\p{N}]+/gu) || []).filter(word => word.length > 1 && !stop.has(word));
const bytes = new TextEncoder();
const sha = async text => [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes.encode(text)))].map(value => value.toString(16).padStart(2, '0')).join('');
const packetButton = (dataset, container, packetPath, label = 'Read compact packet', ancestors = new Set()) => {
  const button = document.createElement('button');
  button.textContent = label;
  button.addEventListener('click', async () => {
    button.disabled = true;
    try {
      const packet = await dataset.readJSON(packetPath);
      const section = document.createElement('section');
      const heading = document.createElement('h3');
      heading.textContent = packet.title;
      const text = document.createElement('pre');
      const contract = {...packet.contract};
      if (contract.provides?.length === 1 && contract.provides[0] === packet.statement) delete contract.provides;
      const reviews = packet.review_overlays.map(({id, decision, reviewer, scope, remaining_gaps, authority}) =>
        ({id, decision, reviewer, scope, remaining_gaps, authority}));
      const notices = packet.notices.map(({notice_id, status, clarification, whole_claim_invalidated, affected_units, context_only_notice, parent_context_card}) =>
        ({notice_id, status, clarification, whole_claim_invalidated, affected_units, context_only_notice, parent_context_card}));
      text.textContent = JSON.stringify({statement: packet.scientific_card_excerpt?.text ?? packet.statement,
        statement_scope: packet.scientific_card_excerpt?.scope,
        card_source: packet.scientific_card_excerpt?.source,
        historical_reported_status: packet.scientific_card_excerpt ? packet.statement : undefined,
        contract, review: reviews.length ? reviews : packet.review, notices}, null, 2);
      const fullPacket = document.createElement('a');
      fullPacket.href = dataset.url(packetPath);
      fullPacket.textContent = 'Complete packet, exact evidence and version identities';
      section.append(heading, fullPacket, text);
      for (const review of reviews) {
        const fullReview = document.createElement('a');
        fullReview.href = '../' + review.authority;
        fullReview.textContent = `Full scoped review: ${review.id}`;
        section.append(fullReview);
      }
      for (const reference of packet.evidence) {
        const source = document.createElement('a');
        source.href = '../' + (reference.read_path || reference.path).split('/').map(encodeURIComponent).join('/');
        source.textContent = `Read source: ${reference.path} — lines ${JSON.stringify(reference.lines)}, SHA ${reference.sha256}`;
        const paragraph = document.createElement('p');
        paragraph.append(source);
        section.append(paragraph);
      }
      const seen = new Set([...ancestors, packet.id]);
      for (const unit of packet.related_units || []) {
        if (seen.has(unit.id)) continue;
        const paragraph = document.createElement('div');
        paragraph.append(packetButton(dataset, paragraph, unit.packet.replace(/^knowledge\//, ''), `Read intermediate operation: ${unit.title}`, seen));
        section.append(paragraph);
      }
      for (const transfer of packet.transfers || []) {
        const paragraph = document.createElement('div');
        const state = document.createElement('strong');
        state.textContent = `${transfer.state}: `;
        paragraph.append(state, document.createTextNode(transfer.scope));
        const obligation = document.createElement('p');
        obligation.textContent = transfer.remaining_obligations;
        const other = transfer.from === packet.id ? transfer.to : transfer.from;
        if (!seen.has(other)) {
          const short = other.replace(/^([NL]\d+)-.*$/, '$1');
          paragraph.append(packetButton(dataset, paragraph, `current/packets/${encodeURIComponent(short)}.json`, `Read connected operation: ${other}`, seen));
        }
        const full = document.createElement('a');
        full.href = '../' + transfer.authority;
        full.textContent = `Full version-bound connection: ${transfer.id}`;
        section.append(paragraph, obligation, full);
      }
      container.append(section);
    } catch (error) { button.textContent = error.message; button.disabled = false; }
  });
  return button;
};
const createDataset = manifest => {
  const expectedHash = path => {
    const expected = manifest.outputs?.[`knowledge/${path}`];
    if (!/^[0-9a-f]{64}$/.test(expected || '')) throw Error(`Unregistered dataset file: ${path}`);
    return expected;
  };
  const url = path => `${path}?sha256=${expectedHash(path)}`;
  const readJSON = async path => {
    const response = await fetch(url(path), {cache: 'no-store'});
    if (!response.ok) throw Error(`${path} unavailable`);
    const text = await response.text();
    if (await sha(text) !== expectedHash(path)) throw Error(`Mixed or changed dataset: ${path}. Search again for the current version.`);
    return JSON.parse(text);
  };
  let catalog;
  const readCatalog = () => {
    if (!catalog) catalog = readJSON('current/catalog.json').catch(error => { catalog = undefined; throw error; });
    return catalog;
  };
  const shards = new Map();
  const loadShard = (shard, folder = 'postings') => {
    const key = `${folder}/${shard}`;
    if (!shards.has(key)) shards.set(key, readJSON(`current/${key}.json`).catch(error => { shards.delete(key); throw error; }));
    return shards.get(key);
  };
  return {manifest, url, readJSON, readCatalog, loadShard};
};
let activeDataset;
const loadDataset = async () => {
  const response = await fetch('current/search_manifest.json', {cache: 'no-store'});
  if (!response.ok) throw Error('Search manifest unavailable');
  const manifest = await response.json();
  if (!/^[0-9a-f]{64}$/.test(manifest.input_version || '')) throw Error('Search manifest version invalid');
  if (!activeDataset || activeDataset.manifest.input_version !== manifest.input_version) activeDataset = createDataset(manifest);
  return activeDataset;
};
let generation = 0;
document.querySelector('#search').addEventListener('submit', async event => {
  event.preventDefault();
  const request = ++generation;
  const query = document.querySelector('#query').value;
  results.replaceChildren();
  status.textContent = 'Searching cited content and operation contracts…';
  try {
    const dataset = await loadDataset();
    const data = await dataset.readCatalog();
    const original = new Set(tokenize(query));
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
      const postings = data.shards.includes(shard) ? await dataset.loadShard(shard) : {};
      for (const [index, score] of postings[term] || []) scores.set(index, (scores.get(index) || 0) + weight * score);
      if (original.has(term) && data.lexical_shards.includes(shard)) {
        const lexical = await dataset.loadShard(shard, 'lexical');
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
    const manifest = dataset.manifest;
    status.textContent = `${selected.length} ranked candidates, not applicability verdicts. Dataset ${manifest.input_version.slice(0, 12)}. ${expanded.length ? 'Expanded terms: ' + [...new Set(expanded)].join(', ') : ''}`;
    for (const candidate of selected) {
      const article = document.createElement('article');
      const heading = document.createElement('h2');
      heading.textContent = candidate.title;
      const link = document.createElement('a');
      const short = candidate.record_id.replace(/^([NL]\d+)-.*$/, '$1');
      const packetPath = `current/packets/${encodeURIComponent(short)}.json`;
      link.href = dataset.url(packetPath);
      link.textContent = `${candidate.record_id} — exact packet, conditions, notices and sources`;
      const note = document.createElement('p');
      note.className = 'note';
      note.textContent = `${candidate.kind}; ${candidate.safety ? 'full-card lexical safety lane, independent score scale' : 'content/contract lane'}; score ${candidate.score.toFixed(2)}. Similar wording does not establish composition.`;
      const expand = packetButton(dataset, article, packetPath);
      article.append(heading, link, note, expand);
      results.append(article);
    }
  } catch (error) { if (request === generation) status.textContent = `Access failure: ${error.message}. Use the pinned raw packet route in README.md.`; }
});

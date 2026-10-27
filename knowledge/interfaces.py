"""Linear-size, version-bound common-consumer navigation; no inferred transfer."""
RELATION = 'COMMON CONSUMER; NAVIGATION ONLY'
SCOPE = ('Each candidate can feed its OWN qualified task bound to this abstract consumer. '
         'No provider-to-provider transfer, shared physical assumptions, unit conversion, '
         'confidence conversion or inherited acceptance is established.')


def compile_navigation(records, transfers):
    current = {r['id']: r for r in records}
    navigation = {id: dict(routes=[], bindings=[], consumers=[]) for id in current}
    for transfer in transfers:
        binding = transfer.get('slot_binding')
        if binding is None:
            continue
        if transfer['state'] != 'ESTABLISHED COMPATIBLE INTERFACE':
            raise ValueError('Only an established compatible interface can bind a consumer slot')
        if not isinstance(binding, dict) or not isinstance(binding.get('slot'), str) or not binding['slot'].strip():
            raise ValueError('Consumer binding requires an explicit declared slot')
        source, target = current[transfer['from']], current[transfer['to']]
        if source['id'] == target['id']:
            raise ValueError('A consumer slot cannot bind itself')
        for endpoint, record in (('from', source), ('to', target)):
            if transfer[endpoint+'_version'] != record['content_version']:
                raise ValueError('Stale consumer binding endpoint version')
        slots = target['contract'].get('input_slots', [])
        declared = [s for s in slots if isinstance(s, dict) and s.get('id') == binding['slot']]
        if len(declared) != 1:
            raise ValueError('Unknown or ambiguous declared consumer input slot')
        fields = declared[0].get('required_binding_fields')
        if (not isinstance(fields, list) or not fields
                or any(not isinstance(k, str) or not k.strip() or k == 'slot' for k in fields)
                or len(set(fields)) != len(fields)
                or not {'units', 'qualification'} <= set(fields)):
            raise ValueError('Consumer slot must declare its required fields, units and qualification')
        if any(not isinstance(binding.get(k), str) or not binding[k].strip() for k in fields):
            raise ValueError('Consumer binding must supply every explicit declared field, including units and qualification')
        item = dict(provider=source['id'], provider_version=source['content_version'],
                    consumer=target['id'], consumer_version=target['content_version'],
                    slot=binding['slot'], transfer=transfer['id'], binding=binding)
        navigation[target['id']]['bindings'].append(item)
        route = {k: v for k, v in item.items() if k != 'binding'}
        for context in [source['id']] + source.get('parents', []):
            navigation[context]['routes'].append(route)
    for identifier, record in current.items():
        slots = {item['slot'] for item in navigation[identifier]['bindings']}
        for parent in record.get('parents', []):
            for slot in sorted(slots):
                navigation[parent]['consumers'].append(dict(consumer=identifier,
                    consumer_version=record['content_version'], slot=slot))
    for nav in navigation.values():
        for key in ('routes', 'bindings'):
            nav[key].sort(key=lambda x: (x['consumer'], x['slot'], x['provider'], x['transfer']))
        nav['consumers'].sort(key=lambda x: (x['consumer'], x['slot']))
    return {id: nav for id, nav in navigation.items() if any(nav.values())}


def packet_navigation(navigation, transfers):
    """Avoid repeating an identical mapping already retained in full on a transfer."""
    by_id = {t['id']: t for t in transfers}
    bindings = []
    for item in navigation.get('bindings', []):
        transfer = by_id.get(item['transfer'], {})
        if (transfer.get('slot_binding') == item['binding']
                and transfer.get('from_version') == item['provider_version']
                and transfer.get('to_version') == item['consumer_version']):
            item = {key: value for key, value in item.items() if key != 'binding'}
            item['binding_ref'] = dict(field='transfers', id=transfer['id'], mapping_field='slot_binding')
        bindings.append(item)
    return dict(navigation, bindings=bindings)


def peers(records, identifier, offset=0, limit=8):
    if type(offset) is not int or type(limit) is not int or offset < 0 or not 1 <= limit <= 50:
        raise ValueError('Use a nonnegative offset and limit in 1..50')
    record = records[identifier]
    nav = record.get('interface_navigation', {})
    routes = nav.get('routes', [])
    for route in routes:
        if (route['provider_version'] != records[route['provider']]['content_version']
                or route['consumer_version'] != records[route['consumer']]['content_version']):
            raise ValueError('Stale common-consumer local route; rebuild current views')
    contexts = {(r['consumer'], r['slot']) for r in routes}
    for consumer in nav.get('consumers', []):
        if consumer['consumer_version'] != records[consumer['consumer']]['content_version']:
            raise ValueError('Stale common-consumer parent route; rebuild current views')
        contexts.add((consumer['consumer'], consumer['slot']))
    contexts.update((r['consumer'], r['slot']) for r in nav.get('bindings', []))
    local = {r['provider'] for r in routes}
    candidates = {}
    for consumer, slot in sorted(contexts):
        target = records[consumer]
        for item in target.get('interface_navigation', {}).get('bindings', []):
            if item['slot'] != slot or item['provider'] in local:
                continue
            source = records[item['provider']]
            if item['provider_version'] != source['content_version'] or item['consumer_version'] != target['content_version']:
                raise ValueError('Stale common-consumer navigation; rebuild current views')
            key = (consumer, slot, item['provider'], item['transfer'])
            candidates[key] = dict(item, title=source['title'], parents=source.get('parents', []),
                                   notice_count=len(source.get('notices', [])),
                                   review_decisions=[r['decision'] for r in source.get('review_overlays', [])],
                                   next=['packet', source['id']], consumer_next=['packet', consumer])
    ordered = [candidates[key] for key in sorted(candidates)]
    end = offset + limit
    return dict(relation=RELATION, context=identifier, routes=routes, consumers=nav.get('consumers', []), total_candidates=len(ordered),
                offset=offset, limit=limit, next_offset=end if end < len(ordered) else None,
                candidates=ordered[offset:end], scope=SCOPE)

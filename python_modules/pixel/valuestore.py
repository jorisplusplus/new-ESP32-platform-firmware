## These functions allow you to easily load and save Python objects as json files in /cache/.

def load(namespace='system', keyname=''):
    import ujson
    if namespace == '' or keyname is None:
        print('nvs.load() called with empty namespace')
        return None
    if keyname == '' or keyname is None:
        print('nvs.load() called with empty keyname')
        return None

    try:
        with open('/cache/%s-%s.json' % (namespace, keyname), 'r') as file:
            return ujson.load(file)
    except BaseException as error:
        # Ignore error if file does not yet exist
        if 'ENODEV' not in str(error):
            print('Error reading cache file for %s-%s: %s' % (namespace, keyname, error))
        return None

def save(namespace='system', keyname='', value=None):
    import ujson
    if namespace == '' or keyname is None:
        print('nvs.save() called with empty namespace')
        return None
    if keyname == '' or keyname is None:
        print('nvs.save() called with empty keyname')
        return None
    if value == None:
        print('nvs.save() called with empty value')
        return None

    try:
        with open('/cache/%s-%s.json' % (namespace, keyname), 'w') as file:
            return ujson.dump(value, file)
    except Exception as error:
        print('Error writing cache file for %s-%s: %s' % (namespace, keyname, error))
        return None

def nvs_get(namespace, key):
    nvs = load('nvs', namespace)
    item = nvs[key] if nvs is not None and key in nvs else None
    return item

def nvs_set(namespace, key, value):
    nvs = load('nvs', namespace) or {}
    nvs[key] = value
    save('nvs', namespace, nvs)
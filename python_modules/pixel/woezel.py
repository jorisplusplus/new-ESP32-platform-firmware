import sys, gc, uos as os, uerrno as errno, ujson as json, uzlib, urequests, upip_utarfile as tarfile, time, wifi, machine
import consts, rtc
gc.collect()

debug = False
install_path = None
_progress_callback = None
cleanup_files = []
gzdict_sz = 16 + 15

cache_path = '/cache/woezel'
woezel_domain = consts.WOEZEL_WEB_SERVER
device_name = consts.INFO_HARDWARE_WOEZEL_NAME

file_buf = bytearray(100)

class NotFoundError(Exception):
    pass

class LatestInstalledError(Exception):
    pass

def _op_split(path):
    if path == "":
        return ("", "")
    r = path.rsplit("/", 1)
    if len(r) == 1:
        return ("", path)
    head = r[0]
    if not head:
        head = "/"
    return (head, r[1])

def op_basename(path):
    return _op_split(path)[1]

# Expects *file* name
def _makedirs(name, mode=0o777):
    ret = False
    s = ""
    comps = name.rstrip("/").split("/")[:-1]
    if comps[0] == "":
        s = "/"
    for c in comps:
        if s and s[-1] != "/":
            s += "/"
        s += c
        try:
            os.mkdir(s)
            ret = True
        except OSError as e:
            if e.args[0] != errno.EEXIST and e.args[0] != errno.EISDIR:
                raise
            ret = False
    return ret


def _save_file(fname, subf):
    global file_buf
    with open(fname, "wb") as outf:
        while True:
            sz = subf.readinto(file_buf)
            if not sz:
                break
            outf.write(file_buf, sz)

def _install_tar(f, prefix):
    meta = {}
    for info in f:
        #print(info)
        fname = info.name
        try:
            fname = fname[fname.index("/") + 1:]
        except ValueError:
            fname = ""

        save = True
        for p in ("setup.", "PKG-INFO", "README"):
                #print(fname, p)
                if fname.startswith(p) or ".egg-info" in fname:
                    if fname.endswith("/requires.txt"):
                        meta["deps"] = f.extractfile(info).read()
                    save = False
                    if debug:
                        print("Skipping", fname)
                    break

        if save:
            outfname = prefix + fname
            if info.type != tarfile.DIRTYPE:
                if debug:
                    print("Extracting " + outfname)
                _makedirs(outfname)
                subf = f.extractfile(info)
                _save_file(outfname, subf)
    return meta

def _expandhome(s):
    if "~/" in s:
        h = os.getenv("HOME")
        s = s.replace("~/", h + "/")
    return s


def _fatal(msg, exc=None):
    print("Error:", msg)
    if exc and debug:
        raise exc
    sys.exit(1)

def set_progress_callback(callback):
    global _progress_callback
    _progress_callback = callback

def _show_progress(text, error=False):
    if error:
        machine.nvs_setint('system', 'lastUpdate', 0)

    if callable(_progress_callback):
        _progress_callback(text, error)

def _get_last_updated():
    last_updated = -1
    return machine.nvs_getint('system', 'lastUpdate') or last_updated

def _set_last_updated():
    try:
        return machine.nvs_setint('system', 'lastUpdate', int(time.time()))
    except:
        pass

def _slug_to_name(slug):
    if len(slug) < 2:
        return slug.upper()

    slug = slug.replace('_', ' ')
    return slug[0].upper() + slug[1:]

def update_cache():
    # Check if RTC has been synced over NTP
    if not rtc.isSet():
        _show_progress("Connecting to WiFi...", False)
        wifi.connect()
        if not wifi.wait():
            _show_progress("Failed to connect to WiFi.", True)
            return False

        while wifi.status() and (time.time() < 1482192000):
            wifi.ntp()

    last_update = _get_last_updated()
    if last_update > 0 and time.time() < last_update + (600):
        return True

    if not wifi.status():
        _show_progress("Connecting to WiFi...", False)
        wifi.connect()
        if not wifi.wait():
            _show_progress("Failed to connect to WiFi.", True)
            return False

    print('Updating woezel cache..')

    _show_progress("Downloading package list...")
    packages = get_pkg_list()
    categories = set(item['category'] for item in packages)

    with open(cache_path + '/categories.json', 'w') as categories_file:
        categories_file.write(json.dumps([{'name': _slug_to_name(cat), 'slug': cat} for cat in categories]))

    _show_progress("Saving lists...")
    for cat in categories:
        gc.collect()
        with open(cache_path + '/' + cat + '.json', 'w') as category_file:
            category_file.write(json.dumps([app for app in packages if app['category'] == cat]))

    gc.collect()
    _set_last_updated()

    _show_progress("Done!")
    gc.collect()
    return True


def get_categories():
    if not update_cache():
        return []

    active_categories = []

    with open(cache_path + '/categories.json', 'r') as categories_file:
        categories = json.load(categories_file)

    for category in categories:
        slug = category['slug']
        with open(cache_path + '/' + slug + '.json', 'r') as file:
            contents = json.load(file)
            if len(contents) > 0:
                category['eggs'] = len(contents)
                active_categories.append(category)
    gc.collect()
    return active_categories


def get_category(category_name):
    if not update_cache():
        return []

    with open(cache_path + '/%s.json' % category_name, 'r') as category_file:
        return json.load(category_file)

def get_pkg_metadata(name):
    import gc
    gc.collect()
    try:
        response = urequests.get('http://%s/eggs/get/%s/json' % (woezel_domain, name))
    except BaseException as e:
        import sys
        sys.print_exception(e)
        print('Exception getting package metadata')
        return None


    return response.json()

def get_pkg_list():
    import dumbstreamjson
    return list(dumbstreamjson.from_url('http://%s/basket/%s/list/json' % (woezel_domain, device_name),
                                   keys=['name', 'slug', 'category', 'revision']))

def search_pkg_list(query):
    import dumbstreamjson
    return list(dumbstreamjson.from_url('http://%s/basket/%s/search/%s/json' % (woezel_domain, device_name, query),
                                        keys=['name', 'slug', 'category', 'revision']))
    response = urequests.get()
    return response.json()

def is_installed(app_name, path=None):
    if path == None:
        path = get_install_path()
    if path[-1] != '/':
        path += '/'
    already_installed = False
    print(app_name, path)
    try:
        os.stat("%s%s/" % (path, app_name))
    except OSError as e:
        if e.args[0] == errno.EINVAL:
            print("Package %s already installed" % (app_name))
            already_installed = True
        else:
            print("Package %s not yet installed" % (app_name))
    else:
        # fallback for unix version
        print("Package %s already installed" % (app_name))
        already_installed = True

    return already_installed

def install_pkg(pkg_spec, install_path, force_reinstall):
    data = get_pkg_metadata(pkg_spec)
    if data is None:
        return None
    already_installed = is_installed(pkg_spec, install_path)
    latest_ver = data["info"]["version"]
    verf = "%s%s/version" % (install_path, pkg_spec)
    if already_installed:
        try:
            with open(verf, "r") as fver:
                old_ver = fver.read()
        except:
            print("No version file found")
        else:
            if old_ver == latest_ver:
                if not force_reinstall:
                    raise LatestInstalledError("Latest version installed")
            else:
                print("Removing previous rev. %s" % old_ver)
                for rm_file in os.listdir("%s%s" % (install_path, pkg_spec)):
                    os.remove("%s%s/%s" % (install_path, pkg_spec, rm_file))
    packages = data["releases"][latest_ver]
    del data
    gc.collect()
    assert len(packages) == 1
    package_url = packages[0]["url"].replace('https', 'http')
    print("Installing %s rev. %s from %s" % (pkg_spec, latest_ver, package_url))
    package_fname = op_basename(package_url)
    f1 = urequests.get(package_url).raw
    try:
        gc.collect()
        print('mem_free:', gc.mem_free())
        f2 = uzlib.DecompIO(f1, gzdict_sz)
        f3 = tarfile.TarFile(fileobj=f2)
        meta = _install_tar(f3, "%s%s/" % (install_path, pkg_spec))
    finally:
        f1.close()
        del f1
    del f3
    del f2
    with open(verf, "w") as fver:
        fver.write(latest_ver)
    del fver
    gc.collect()
    return meta

def install(to_install, install_path=None, force_reinstall=False):
    # Calculate gzip dictionary size to use
    global gzdict_sz
    # Perform a collect before installing
    gc.collect()
    sz = gc.mem_free() + gc.mem_alloc()
    if sz <= 65536:
        # this will probably give errors with some packages, but we
        # just don't have enough memory.
        gzdict_sz = 16 + 8

    if install_path is None:
        install_path = get_install_path()
    if install_path[-1] != "/":
        install_path += "/"
    if not isinstance(to_install, list):
        to_install = [to_install]
    print("Installing to: " + install_path)
    _show_progress('Installing...', False)
    # sets would be perfect here, but don't depend on them
    installed = []
    try:
        while to_install:
            if debug:
                print("Queue:", to_install)
            pkg_spec = to_install.pop(0)
            if pkg_spec in installed:
                continue
            meta = install_pkg(pkg_spec, install_path, force_reinstall)
            installed.append(pkg_spec)
            if debug:
                print(meta)
            deps = meta.get("deps", "").rstrip()
            if deps:
                deps = deps.decode("utf-8").split("\n")
                to_install.extend(deps)
        return True
    except Exception as e:
        import sys
        sys.print_exception(e)
        print("Error installing '{}': {}, packages may be partially installed".format(
                pkg_spec, e),
            file=sys.stderr)
        return False

def display_pkg(packages):
    for package in packages:
        print(package["name"])
        print("  Slug:        " + package["slug"])
        print("  Version:     " + package["revision"])
        print("  Description: " + package["description"])


def search(query="*"):
    if query == "*":
        packages = get_pkg_list()
    else:
        packages = search_pkg_list(query)
    display_pkg(packages)

def get_install_path():
    global install_path
    if install_path is None:
        install_path = 'apps'
    install_path = _expandhome(install_path)
    return install_path

def cleanup():
    for fname in cleanup_files:
        try:
            os.unlink(fname)
        except OSError:
            print("Warning: Cannot delete " + fname)

def help():
    print("""\
woezel - Clone of the Simple PyPI package manager for MicroPython
Usage: micropython -m woezel install [-p <path>] <package>... | -r <requirements.txt>

import woezel
woezel.install(package_or_list, [<path>])
woezel.search([query])

If <path> is not given, packages will be installed into sys.path[1]
(can be set from MICROPYPATH environment variable, if current system
supports that).""")
    print("Current value of sys.path[1]:", sys.path[1])
    print("""\

Note: only MicroPython packages are supported for installation,
woezel, like upip does not support arbitrary code in setup.py.
""")

def main():
    global debug
    global install_path
    install_path = None

    if len(sys.argv) < 2 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        help()
        return

    if sys.argv[1] != "install":
        _fatal("Only 'install' command supported")

    to_install = []

    i = 2
    while i < len(sys.argv) and sys.argv[i][0] == "-":
        opt = sys.argv[i]
        i += 1
        if opt == "-h" or opt == "--help":
            help()
            return
        elif opt == "-p":
            install_path = sys.argv[i]
            i += 1
        elif opt == "-r":
            list_file = sys.argv[i]
            i += 1
            with open(list_file) as f:
                while True:
                    l = f.readline()
                    if not l:
                        break
                    if l[0] == "#":
                        continue
                    to_install.append(l.rstrip())
        elif opt == "--debug":
            debug = True
        else:
            _fatal("Unknown/unsupported option: " + opt)

    to_install.extend(sys.argv[i:])
    if not to_install:
        help()
        return

    install(to_install)

    if not debug:
        cleanup()


if __name__ == "__main__":
    main()

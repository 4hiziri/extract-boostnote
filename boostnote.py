import os


def read_json_str(filename):
    import json
    with open(filename) as file:
        return json.loads(file.read())


def folder_names_boostnote(json):
    return list(map(lambda x: x['name'], json['folders']))


def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return


def files_boostnote(dir):
    import cson

    ret = []

    files = os.listdir(dir)
    for file in files:
        path = os.path.join(dir, file)
        with open(path) as f:
            cdict = cson.loads(f.read())
            cdict['name'] = file
            ret.append(cdict)

    return ret


def cp_boostnotes(csons, jsons, src, trg):
    import shutil
    jsons = jsons['folders']
    for cson in csons:
        srcpath = os.path.join(src, cson['name'])
        dir_name = list(
            filter(lambda x: x['key'] == cson['folder'], jsons)).pop()['name']
        trgpath = os.path.join(trg, dir_name, cson['title'] + '.md')
        shutil.copyfile(srcpath, trgpath)


def main(dir):
    os.chdir(dir)

    root = '_notes'
    mkdir_if_not_exists(root)

    jsons = read_json_str('boostnote.json')
    dir_names = folder_names_boostnote(jsons)
    for dir_name in dir_names:
        mkdir_if_not_exists(os.path.join(root, dir_name))

    csons = files_boostnote('notes')
    cp_boostnotes(csons, jsons, 'notes', root)
    return

from io import BytesIO
from PIL import Image
from pathlib import Path
from flask import Flask, render_template, request, make_response, redirect
import numpy as np
import magic
import datetime
import h5py
import glob

app = Flask(__name__)

thumbnail_db = h5py.File('thumbnail.h5', 'a')

icons_db = h5py.File('icons.h5', 'a')


magic_man = magic.Magic()

@app.route('/')
def list_dbs():
    return render_template("list.html", url='/', list=[key for key in glob.glob("*.h5")], show=True)



@app.route('/<string:db>')
@app.route('/<string:db>/')
def root_index(db):
    if db.endswith('.h5'):
        db = db[:-3]
    
    return index(db, "/")


@app.route('/<string:db>/<path:path>')
def index(db, path):

    if db.endswith('/'):
        db = db[:-1]

    if db.endswith('.h5'):
        db = db[:-3]

    if db in 'thumbnail' or db in 'icons':
        return render_template('errors/nope.html')

    print('db path:' + db)
    print('file Path:' + path)
    if_db = Path(db + ".h5")

    if if_db.is_file() is False:
        return render_template('errors/404.html', msg='no DB with the name "' + db + '"')

    try:
        file = h5py.File(db + ".h5")[path]
    except:
        return render_template('errors/404.html', msg="there was an error i think it was just a 404 error")

    is_dataset = isinstance(file, h5py.Dataset)

    do_resize = request.args.get('thumb')


    if is_dataset or do_resize is not None:

        if do_resize is None:

            response = make_response(file[0].tobytes())
            response.headers.set('Content-Type', get_mime_type(file[0].tobytes()) )
            return response

        else:
            return get_thumnail(file ,db, path)

    else:

        do_show_img = request.args.get('i')

        if do_show_img is None:
            show_img = False
        else:
            show_img = True

        link = request.path

        print('Link:' + request.path)

        if link.endswith('/') is False:
            link += "/"

        return render_template("list.html", url=link, list=[key for key in file.keys()], show=show_img)


def get_mime_type(buffer):
    return magic_man.from_buffer(buffer)

def make_thumbnail(name, buffer):
    size = 160, 160
    im = Image.open(BytesIO(buffer))
    im.thumbnail(size)

    imgByteArr = BytesIO()
    im.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()

    try:
        dt = h5py.special_dtype(vlen=np.dtype('uint8'))
        temp = thumbnail_db.create_dataset(name, (1,), dtype=dt)
    except:
        temp = thumbnail_db[name]

    temp[0] = np.fromstring(imgByteArr, dtype='uint8')


def get_thumnail(db_file, db, path):
    thumbnail_path = db + '/' + path
    try:
        if "image" not in get_mime_type(db_file[0].tobytes()):
            try:
                print(get_mime_type(db_file[0].tobytes()))
                output = thumbnail_db[get_mime_type(db_file[0].tobytes())][0].tobytes()
                response = make_response(output)
                response.headers.set('Content-Type', get_mime_type(output))
                return response
            except:
                return redirect("http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/file-text-icon.png", code=302)

    except:
        #this will be a folder
        return redirect("http://icons.iconarchive.com/icons/dtafalonso/yosemite-flat/512/Folder-icon.png", code=302)

    try:
        output = thumbnail_db[thumbnail_path][0].tobytes()
    except:
        print('Making thumb nail')
        make_thumbnail(thumbnail_path, db_file[0].tobytes())
        output = thumbnail_db[thumbnail_path][0].tobytes()

    print(thumbnail_path)
    thumbnail_db[thumbnail_path].attrs['last'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = make_response(output)
    response.headers.set('Content-Type', get_mime_type(output))
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0")

from flask import *
import numpy as np
import h5py
from PIL import Image
from io import BytesIO
import datetime


app = Flask(__name__)


thumbnail_db = h5py.File('thumbnail.h5', 'a')


@app.route('/<string:db>')
@app.route('/<string:db>/')
def root_index(db):
    if db is not 'favicon.ico':
        return index(db, "/")


@app.route('/<string:db>/<path:path>')
def index(db, path):

    file = h5py.File(db + ".h5")[path]

    is_dataset = isinstance(file, h5py.Dataset)

    if is_dataset:

        do_resize = request.args.get('thumb')

        if do_resize is None:

            response = make_response(file[0].tobytes())
            response.headers.set('Content-Type', 'image/jpeg')
            return response

        else:

            print('do resize')
            thumbnail_path = db + '/' + path

            try:
                output = thumbnail_db[thumbnail_path][0].tobytes()
            except:
                print('Making thumb nail')
                make_thumbnail(thumbnail_path, file[0].tobytes())
                output = thumbnail_db[thumbnail_path][0].tobytes()

            thumbnail_db[thumbnail_path].attrs['last'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            response = make_response(output)
            response.headers.set('Content-Type', 'image/jpeg')
            return response

    else:

        do_show_img = request.args.get('i')

        if do_show_img is None:
            show_img = False
        else:
            show_img = True

        link = request.path

        if link.endswith('/') is False:
            link += "/"

        return render_template("list.html", url=link, list=[key for key in file.keys()], show=show_img)


def make_thumbnail(name, buffer):
    size = 300, 300
    im = Image.open( BytesIO(buffer))
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


if __name__ == '__main__':
    app.run()

from flask import *
from hdf5helper import *
import h5py

app = Flask(__name__)

f = FileHelper('test.h5')

f.store_from_folder('data/', '/a_place/')
f.store_file('im1.jpg', '/cats/im1.jpg')
f.store_file('im2.jpg', '/cats/im2.jpg')
f.store_file('im3.jpg', '/cats/im3.jpg')

icon_db = FileHelper('icons.h5')

@app.route('/<string:db>')
@app.route('/<string:db>/')
def root_index(db):
    return index(db, "/")


@app.route('/<string:db>/<path:path>')
def index(db, path):

    file = h5py.File(db + ".h5")[path]

    is_dataset = isinstance(file, h5py.Dataset)
    do_show_img = request.args.get('i')
    do_resize = request.args.get('r')

    if is_dataset:

        if do_resize:
            icon_Path = db + '/' + path

            need_make = icon_Path in icon_db.get()
            if need_make is False:
                pass

            response = make_response(icon_db.get(icon_Path)[0].tobytes())
            response.headers.set('Content-Type', 'image/jpeg')
            return response

        else:
            response = make_response(file[0].tobytes())
            response.headers.set('Content-Type', 'image/jpeg')
            return response

    else:

        if do_show_img is None:
            show_img = False
        else:
            show_img = True

        link = request.path

        if link.endswith('/') is False:
            link += "/"

        return render_template("list.html", url=link, list=[key for key in file.keys()], show=show_img)


if __name__ == '__main__':
    app.run()

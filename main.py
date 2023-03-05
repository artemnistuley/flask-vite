from flask import Flask, render_template, send_from_directory
from flask_vite import Vite

class FlaskVue(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='<%',
        block_end_string='%>',
        variable_start_string='[[',
        variable_end_string=']]',
        comment_start_string='<#',
        comment_end_string='#>',
    ))

app = FlaskVue(__name__, static_folder='static')
app.config['VITE_DEV_MODE'] = app.config.get('DEBUG')

Vite(app)

@app.route('/src/assets/<path:path>')
def serve_vite_assets(path):
    print(path)
    if app.config.get('DEBUG'):
        return send_from_directory('./src/assets/', path)
    else:
        return ('Missing resource', 404)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/library')
def library():
    return render_template('library.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True,)

from flask import Flask, render_template, url_for, request, \
    jsonify, g, redirect, session
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Thisisasecret'

def connect_db():
    # amend as appropriate
    path_to_db = '/home/seraphina/Documents/TRAINING/training_2019/JOB_APPLICATIONS/brandworkz/page-generator/'
    sql = sqlite3.connect(path_to_db + 'form.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/data', methods=['POST', 'GET'])
def process_data():
    if request.method == 'POST':
        db = get_db()
        data = {}

        template_name = request.form['template_name']
        background_colour = request.form['background_colour']
        background_image = request.form['background_image']
        height = request.form['height']
        content_bg_clr = request.form['content_bg_clr']
        border_radius = request.form['border_radius']
        content_body = request.form['content_body']

        data['template_name'] = template_name
        data['background_colour'] = background_colour
        data['background_image'] = background_image
        data['height'] = height
        data['content_bg_colour'] = content_bg_clr
        data['border_radius'] = border_radius
        data['content_body'] = content_body

        temp_name = template_name

        data = jsonify(data)
        session['temp_name'] = temp_name
        
        cur = db.execute('select id from form1 where template_name = ?', [template_name])
        existing_template = cur.fetchone()
        if existing_template:
            message = "Template name {} already exists, please try again!".format(template_name)
            return render_template('data.html', message=message)
        db.execute('insert into form1 (template_name, background_colour, background_image, height, content_bg_clr, border_radius, content_body) values (?, ?, ?, ?, ?, ?, ?)', [template_name, background_colour, background_image, height, content_bg_clr, border_radius, content_body])
        db.commit()
        
        message = ''
        return redirect(url_for('output', message=message))
    return render_template('data.html')

@app.route('/output', methods=['POST', 'GET'])
def output():
    db = get_db()
    if 'template_name' in session:
        name = session['temp_name']
    else:
        name = 'Default Name'
    cur = db.execute('select template_name, background_colour, background_image, height, content_bg_clr, border_radius, content_body from form1 where template_name = ?', [name])
    result = cur.fetchone()
    return render_template('output.html', result=result, name=name)



if __name__ == '__main__':
    app.run(debug=True)

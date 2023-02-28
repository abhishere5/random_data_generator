
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_pymongo import PyMongo


app = Flask(__name__, template_folder='template')
app.secret_key = 'super secret key'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/admin'
mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        if request.form.get('signup') == 'Submit':
            users = mongo.db.user
            signup_user = users.find_one({'username': request.form['username']})
            if signup_user:
                flash('User Already Exists')
                render_template('login.html')
            else:
                mongo.db.user.insert_one(
                    {
                        'name': request.form['name'],
                        'username': request.form['username'],
                        'password': request.form['password']
                    }
                )
                flash('You were successfully signed in now login to see about distributions')
                return render_template('login.html')
        return "wtf"


# login page code
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form.get('login') == 'Submit':
            users = mongo.db.user
            login_user = users.find_one({'username': request.form['username']})

            if login_user is None:
                flash("Username Not Found")

            if login_user:
                if request.form['password'] == login_user['password']:
                    return redirect('/front')
                else:
                    flash("Invalid Password")
            return render_template('/login.html')
        if request.form.get('signup') == 'Signup':
            return render_template('signup.html')


@app.route('/front')
def front():
    return render_template('front.html')


@app.route('/uniform')
def uniform():
    return render_template('uniform.html')


@app.route('/normal')
def normal():
    return render_template('normal.html')


@app.route('/binomial')
def binomial():
    return render_template('binomial.html')


@app.route('/geometric')
def geometric():
    return render_template('geometric.html')


@app.route('/poisson')
def poisson():
    return render_template('poisson.html')


@app.route('/graph_comp')
def graph_comp():
    return render_template('comp.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000, use_reloader=False)




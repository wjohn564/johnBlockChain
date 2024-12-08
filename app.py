from flask import Flask, render_template
from logic.routes import routes

app = Flask(__name__)

app.register_blueprint(routes, url_prefix='/logic')

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/home')
def homepage():
    return render_template('home.html')

@app.route('/create_course')
def create_course():
    return render_template('create_course.html')

@app.route('/enroll')
def enroll():
    return render_template('enroll.html')

@app.route('/course_details')
def course_details():
    return render_template('course_details.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from logic.routes import routes

app = Flask(__name__)

# Register the routes blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)

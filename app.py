from flask import Flask, request, render_template, send_from_directory
import os

from src.routes.api import api_blueprint


app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api_blueprint)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
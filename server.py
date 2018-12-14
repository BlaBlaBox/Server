import os

from flask import Flask, session
from flask import Blueprint, render_template
from handlers import site
     

def create_app():
    app = Flask(__name__)
    app.register_blueprint(site)
    return app

    
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)

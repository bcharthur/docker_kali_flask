# app.py
from flask import Flask
from Controller.docker_controller import docker_bp
from Controller.chocolatey_controller import choco_bp
from Controller.kali_controller import kali_bp
from Controller.ssh_controller import ssh_bp
from Controller.console_controller import console_bp
from Controller.home_controller import home_bp

def create_app():

    app = Flask(__name__)
    app.secret_key = "SECRET_KEY"

    # Register blueprints
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(docker_bp, url_prefix='/')
    app.register_blueprint(choco_bp, url_prefix='/')
    app.register_blueprint(kali_bp, url_prefix='/')
    app.register_blueprint(ssh_bp, url_prefix='/')
    app.register_blueprint(console_bp, url_prefix='/')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)

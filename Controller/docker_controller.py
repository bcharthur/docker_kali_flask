# Controller/docker_controller.py
from flask import Blueprint, redirect, url_for
from Service.docker_service import DockerService

docker_bp = Blueprint('docker_bp', __name__)
docker_service = DockerService()

@docker_bp.route('/docker/install', methods=['POST'])
def install_docker():
    docker_service.install_docker()
    return redirect(url_for('home_bp.index'))

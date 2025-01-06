# Controller/docker_controller.py
from flask import Blueprint, redirect, url_for
from Service.docker_service import DockerService

docker_bp = Blueprint('docker_bp', __name__)
docker_service = DockerService()

@docker_bp.route('/docker/install', methods=['POST'])
def install_docker():
    docker_service.install_docker()
    return redirect(url_for('home_bp.index'))

@docker_bp.route('/docker/uninstall', methods=['POST'])
def uninstall_docker():
    docker_service.uninstall_docker()
    return redirect(url_for('home_bp.index'))

@docker_bp.route('/docker/start', methods=['POST'])
def start_docker():
    docker_service.start_docker()
    return redirect(url_for('home_bp.index'))

@docker_bp.route('/docker/stop', methods=['POST'])
def stop_docker():
    docker_service.stop_docker()
    return redirect(url_for('home_bp.index'))

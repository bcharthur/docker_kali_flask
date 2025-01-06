# Controller/home_controller.py
from flask import Blueprint, render_template
from Service.docker_service import DockerService
from Service.chocolatey_service import ChocolateyService
from Service.kali_service import KaliService

home_bp = Blueprint('home_bp', __name__)

docker_service = DockerService()
choco_service = ChocolateyService()
kali_service = KaliService()

@home_bp.route('/', methods=['GET'])
def index():
    docker_status = docker_service.check_docker()
    choco_status = choco_service.check_chocolatey()
    kali_status = kali_service.check_kali()
    return render_template(
        'home/index.html',
        docker_status=docker_status,
        choco_status=choco_status,
        kali_status=kali_status
    )

# Controller/console_controller.py
from flask import Blueprint, request, render_template
from Service.console_service import ConsoleService
from Service.docker_service import DockerService
from Service.chocolatey_service import ChocolateyService
from Service.kali_service import KaliService
from Service.ssh_service import SSHService

console_bp = Blueprint('console_bp', __name__)
console_service = ConsoleService()

docker_service = DockerService()
choco_service = ChocolateyService()
kali_service = KaliService()
ssh_service = SSHService()

@console_bp.route('/console/execute', methods=['POST'])
def console_execute():
    command = request.form.get('command', '')
    console_service.execute_command_in_container("my_kali_container", command)

    # On recharge tout pour la page home
    docker_status = docker_service.check_docker()
    choco_status = choco_service.check_chocolatey()
    kali_status = kali_service.check_kali()
    ssh_status = ssh_service.check_ssh()

    console_logs = console_service.get_logs()

    return render_template('home/index.html',
                           docker_status=docker_status,
                           choco_status=choco_status,
                           kali_status=kali_status,
                           ssh_status=ssh_status,
                           console_logs=console_logs)

# Controller/ssh_controller.py
from flask import Blueprint, redirect, url_for
from Service.ssh_service import SSHService

ssh_bp = Blueprint('ssh_bp', __name__)
ssh_service = SSHService()

@ssh_bp.route('/ssh/enable', methods=['POST'])
def enable_ssh():
    ssh_service.enable_ssh_in_kali()
    return redirect(url_for('home_bp.index'))

@ssh_bp.route('/ssh/disable', methods=['POST'])
def disable_ssh():
    ssh_service.disable_ssh_in_kali()
    return redirect(url_for('home_bp.index'))

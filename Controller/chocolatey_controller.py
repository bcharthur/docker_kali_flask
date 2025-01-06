# Controller/chocolatey_controller.py
from flask import Blueprint, redirect, url_for
from Service.chocolatey_service import ChocolateyService

choco_bp = Blueprint('choco_bp', __name__)
choco_service = ChocolateyService()

@choco_bp.route('/choco/install', methods=['POST'])
def install_chocolatey():
    choco_service.install_chocolatey()
    return redirect(url_for('home_bp.index'))

@choco_bp.route('/choco/uninstall', methods=['POST'])
def uninstall_chocolatey():
    choco_service.uninstall_chocolatey()
    return redirect(url_for('home_bp.index'))

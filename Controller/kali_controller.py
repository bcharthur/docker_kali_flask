# Controller/kali_controller.py
from flask import Blueprint, redirect, url_for
from Service.kali_service import KaliService

kali_bp = Blueprint('kali_bp', __name__)
kali_service = KaliService()

@kali_bp.route('/kali/build', methods=['POST'])
def build_kali():
    kali_service.build_kali_image()
    return redirect(url_for('home_bp.index'))

@kali_bp.route('/kali/run', methods=['POST'])
def run_kali():
    kali_service.run_kali_container()
    return redirect(url_for('home_bp.index'))

@kali_bp.route('/kali/stop', methods=['POST'])
def stop_kali():
    kali_service.stop_kali_container()
    return redirect(url_for('home_bp.index'))

@kali_bp.route('/kali/uninstall', methods=['POST'])
def uninstall_kali():
    kali_service.uninstall_kali()
    return redirect(url_for('home_bp.index'))

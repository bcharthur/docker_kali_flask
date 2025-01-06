# Controller/kali_controller.py
from flask import Blueprint, redirect, url_for
from Service.kali_service import KaliService

kali_bp = Blueprint('kali_bp', __name__)
kali_service = KaliService()

@kali_bp.route('/kali/install', methods=['POST'])
def install_kali():
    kali_service.install_kali()
    return redirect(url_for('home_bp.index'))

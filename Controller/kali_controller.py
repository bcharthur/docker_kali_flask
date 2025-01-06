# Controller/kali_controller.py
from flask import Blueprint, redirect, url_for, request, render_template, flash
from Service.kali_service import KaliService

kali_bp = Blueprint('kali_bp', __name__)
kali_service = KaliService()


@kali_bp.route('/kali/install', methods=['POST'])
def install_kali():
    kali_service.install_kali()
    flash("Installation de Kali lancée. Vérifiez les logs pour plus de détails.", "info")
    return redirect(url_for('home_bp.index'))


@kali_bp.route('/kali/execute', methods=['POST'])
def execute_kali_command():
    # Récupérer la commande depuis le formulaire
    command = request.form.get('command')
    if not command:
        flash("Aucune commande fournie.", "danger")
        return redirect(url_for('home_bp.index'))

    # Exécuter la commande via SSH
    output = kali_service.execute_command(command)

    # Ajouter la sortie aux logs
    flash(f"Résultat de la commande : <pre>{output}</pre>", "success")
    return redirect(url_for('home_bp.index'))

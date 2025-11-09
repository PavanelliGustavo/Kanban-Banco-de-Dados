from flask import Blueprint, render_template, request, redirect, url_for, render_template, flash, session



user_bp = Blueprint("user_bp", __name__)

@user_bp.route('/')
def login():
    return render_template('login.html')

@user_bp.route('/login_request', methods=["POST"])
def login_request():

        parameters = request.form
        user_type = parameters.get("user-type")

        if user_type == "civil":
            #logica para redirecionar o usuario civil
            pass
        else:
            user = parameters.get("user_input")
            password = parameters.get("password_input")
            #logica para verificar usuario e senha
            flash("ERRO: usuário ou senha incorretos", "info")
            return redirect(url_for('user_bp.login'))
             
        



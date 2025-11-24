from flask import Blueprint, render_template, request, redirect, url_for, render_template, flash, session
import json


home_corp_bp = Blueprint("home_corp_bp", __name__)


@home_corp_bp.route("/home_corp")
def home():

    with open("example_corp.json", 'r', encoding='utf-8') as arquivo:
        example_corp = json.load(arquivo)

    with open("example_fields_of_activity.json", 'r', encoding='utf-8') as arquivo:
        example_fields_of_activity = json.load(arquivo)

    return render_template("home_corp.html", corp=example_corp)


@home_corp_bp.route("/edit_profile", methods=["POST"])
def edit_profile():
    flash("Perfil atualizado com sucesso!", category="info")
    return redirect(url_for("home_corp_bp.home"))

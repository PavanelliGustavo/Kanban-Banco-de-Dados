from flask import Blueprint, render_template, request, redirect, url_for, render_template, flash, session


home_corp_bp = Blueprint("home_corp_bp", __name__)


@home_corp_bp.route("/home_corp")
def home():
    example_corp = {"name": "Odebrecht Engenharia e Construção"}
    return render_template("home_corp.html", corp=example_corp)

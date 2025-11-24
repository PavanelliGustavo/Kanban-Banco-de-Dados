from flask import Blueprint, render_template, request, redirect, url_for, render_template, flash

home_gov_bp = Blueprint("home_gov_bp", __name__)

@home_gov_bp.route("/home_gov")
def home():
    return render_template("home_gov.html")
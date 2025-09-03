from flask import Blueprint, redirect, render_template, url_for
from src.forms.user_forms import RegistrationForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/contact")
def contact():
    return render_template("contact.html")

@main_bp.route("/login")
def login():
    return redirect(url_for("api.login"))

@main_bp.route("/register")
def register():
    form = RegistrationForm()
    return redirect(url_for("api.register"))






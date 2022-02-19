from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user

settings = Blueprint('settings', __name__)


@settings.route('/settings')
@login_required
def settings_get():
    return render_template('settings.html')

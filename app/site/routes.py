from app.site import bp
from app.site.dall_e import AIArtGenerator
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request

@bp.route('/', methods=['GET'])
def home():

    return render_template('site/home.html', this_user=current_user)

@bp.route('/app/generate_art/', methods=['GET', 'POST'])
def generate_art():

    return render_template(
        'site/app/generate_art.html',
        this_user=current_user
    )

@bp.route('/app/photo_to_image/', methods=['GET', 'POST'])
def photo_to_image():

    return render_template(
        'site/app/photo_to_image.html',
        this_user=current_user
    )

@bp.route('/app/edit_image/', methods=['GET', 'POST'])
def edit_image():

    return render_template(
        'site/app/edit_image.html',
        this_user=current_user
    )
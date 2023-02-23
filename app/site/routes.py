from app.site import bp
from app.site.dall_e import AIArtGenerator
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request

@bp.route('/', methods=['GET'])
def home():

    return render_template('site/home.html', this_user=current_user)

response = {}

@bp.route('/app/generate_art/', methods=['GET', 'POST'])
def generate_art():

    if request.method == 'POST':

        style = request.form.get('style')
        text_prompt = request.form.get('text_prompt')
        number = request.form.get('number')
        size = request.form.get('size')

        prompt = f"style: {style}. Description: {text_prompt}"

        image_object = AIArtGenerator(
            prompt=prompt,
            n=int(number),
            size=size
        )

        response.update({"data": image_object.generate_art()})
        
        print(response['data'])

        return redirect(url_for('site.generate_art'))

    return render_template(
        'site/app/generate_art.html',
        this_user=current_user,
        generated_response=response
    )

@bp.route('/app/photo_to_art/', methods=['GET', 'POST'])
def photo_to_art():

    return render_template(
        'site/app/photo_to_art.html',
        this_user=current_user
    )

@bp.route('/app/edit_image/', methods=['GET', 'POST'])
def edit_image():

    return render_template(
        'site/app/edit_image.html',
        this_user=current_user
    )

@bp.route('/app/image_variation/', methods=['GET', 'POST'])
def image_variation():

    return render_template(
        'site/app/image_variation.html',
        this_user=current_user
    )
from app.site import bp
from app.extensions import db
from app.site.dall_e import AIArtGenerator
from app.models.subscription import Account
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash, request

response = {"data": []}

ACCOUNT_MANAGEMENT = {
    "free_account": {
        "tier": "Free",
        "max_count": 4,
        "max_images": 1,
        "quality": "256x256"
    },
    "basic_account": {
        "tier": "Basic",
        "max_count": 10,
        "max_images": 2,
        "quality": "512x512"
    },
    "standard_account": {
        "tier": "Standard",
        "max_count": 20,
        "max_images": 3,
        "quality": "512x512"
    },
    "pro_account": {
        "tier": "Pro",
        "max_count": 50,
        "max_images": 5,
        "quality": "1024x1024"
    }
}

@bp.route('/', methods=['GET'])
def home():

    user_account = Account.query.filter_by(user_id=current_user.id)\
                    .first() if current_user.is_authenticated else None

    return render_template(
        'site/home.html',
        this_user=current_user,
        this_account = user_account,
    )

@bp.route('/app/generate_art/', methods=['GET', 'POST'])
@login_required
def generate_art():

    user_account = Account.query.filter_by(user_id=current_user.id).first()
    current_count = int(user_account.generation_count)

    if user_account.subscription == ACCOUNT_MANAGEMENT['free_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['free_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['free_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['free_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['basic_account']['tier']:
        
        max_count = ACCOUNT_MANAGEMENT['basic_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['basic_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['basic_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['standard_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['standard_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['standard_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['standard_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['pro_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['pro_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['pro_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['pro_account']['quality']

    if request.method == 'POST':

        if current_count <= max_count:

            style = request.form.get('style')
            text_prompt = request.form.get('text_prompt')

            prompt = f"style: {style}. Description: {text_prompt}"

            image_object = AIArtGenerator(
                prompt=prompt,
                n=max_images,
                size=quality
            )

            response.update({"data": image_object.generate_art()})

            user_account.generation_count += 1

            try:

                db.session.commit()

            except Exception as e:

                flash(f"Error: {str(e)}", "error")
                return None

        else:

            flash("you have reached the limit of your current subscription.", "error")

        return redirect(url_for('site.generate_art'))

    return render_template(
        'site/app/generate_art.html',
        this_user=current_user,
        this_account=user_account,
        generated_response=response['data']
    )

@bp.route('/app/photo_to_art/', methods=['GET', 'POST'])
@login_required
def photo_to_art():

    user_account = Account.query.filter_by(user_id=current_user.id).first()
    current_count = int(user_account.generation_count)

    if user_account.subscription == ACCOUNT_MANAGEMENT['free_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['free_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['free_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['free_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['basic_account']['tier']:
        
        max_count = ACCOUNT_MANAGEMENT['basic_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['basic_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['basic_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['standard_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['standard_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['standard_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['standard_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['pro_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['pro_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['pro_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['pro_account']['quality']

    if request.method == 'POST':
            
        if current_count <= max_count:

            style = request.form.get('style')
            text_prompt = request.form.get('text_prompt')
            image = request.files['image'].stream.read()

            prompt = f"style: {style}. Description: {text_prompt}"

            image_object = AIArtGenerator(
                prompt=prompt,
                n=max_images,
                size=quality
            )

            response.update({"data": image_object.photo_to_art(image=image)})

            user_account.generation_count += 1

            try:

                db.session.commit()

            except Exception as e:

                flash(f"Error: {str(e)}", "error")
                return None

        else:

            flash("you have reached the limit of your current subscription.", "error")

        return redirect(url_for('site.photo_to_art'))

    return render_template(
        'site/app/photo_to_art.html',
        this_user=current_user,
        this_account=user_account,
        generated_response=response['data']
    )

@bp.route('/app/image_variation/', methods=['GET', 'POST'])
@login_required
def image_variation():

    user_account = Account.query.filter_by(user_id=current_user.id).first()
    current_count = int(user_account.generation_count)

    if user_account.subscription == ACCOUNT_MANAGEMENT['free_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['free_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['free_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['free_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['basic_account']['tier']:
        
        max_count = ACCOUNT_MANAGEMENT['basic_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['basic_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['basic_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['standard_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['standard_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['standard_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['standard_account']['quality']

    elif user_account.subscription == ACCOUNT_MANAGEMENT['pro_account']['tier']:

        max_count = ACCOUNT_MANAGEMENT['pro_account']['max_count']
        max_images = ACCOUNT_MANAGEMENT['pro_account']['max_images']
        quality = ACCOUNT_MANAGEMENT['pro_account']['quality']

    if request.method == 'POST':
            
        if current_count <= max_count:

            image = request.files['image'].stream.read()

            image_object = AIArtGenerator(
                prompt='',
                n=max_images,
                size=quality
            )

            response.update({"data": image_object.image_variation(image=image)})

            user_account.generation_count += 1

            try:

                db.session.commit()

            except Exception as e:

                flash(f"Error: {str(e)}", "error")
                return None

        else:

            flash("you have reached the limit of your current subscription.", "error")

        return redirect(url_for('site.image_variation'))

    return render_template(
        'site/app/image_variation.html',
        this_user=current_user,
        this_account=user_account,
        generated_response=response['data']
    )

@bp.route('/app/upload_image/', methods=['POST'])
def upload_image():

    pass

@bp.route('/app/delete_image/', methods=['POST'])
def delete_image():

    pass
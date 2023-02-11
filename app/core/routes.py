from app.core import bp

@bp.route('/')
def home():

    return 'This is the main blueprint.'
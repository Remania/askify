from flask import current_app
import os
import secrets
from PIL import Image

def save_avatar(form_avatar):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_avatar.filename)
    avatar_filename = rand_hex + f_ext
    avatar_path = os.path.join(current_app.root_path, "static/avatars", avatar_filename)

    output_size=(250, 250)
    i = Image.open(form_avatar)
    i.thumbnail(output_size)

    i.save(avatar_path)
    return avatar_filename
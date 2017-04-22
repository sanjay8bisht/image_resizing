import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = os.environ.get(
    'PROPAGATE_EXCEPTIONS', False
)
app.config['DEBUG'] = os.environ.get('DEBUG_VALUE', False)

from controller.image_resize import ImageResize  # noqa

view = ImageResize()

app.add_url_rule('/', methods=["POST"], view_func=view.image_resize)  # noqa

if __name__ == '__main__':
    app.run()


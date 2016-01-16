
""" Микро-сервис для обработки изображений

"""

from envi import Application
from controllers import Controller

application = Application()
application.route("/<action>/", Controller)
application.route("/v1/<action>/", Controller)
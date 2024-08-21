from flask import Flask
from app.controllers.main_controller import main_controller

app = Flask(__name__)

# Registrar o controlador
app.register_blueprint(main_controller)

if __name__ == '__main__':
    app.run(debug=True)
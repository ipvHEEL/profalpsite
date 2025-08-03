import os
import logging
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from flask import session, url_for, flash
from functools import wraps
from flask_admin.contrib.sqla import ModelView
from flask import abort, redirect, url_for

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://andrew:@localhost/alp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db = SQLAlchemy(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Для доступа в админку необходимо войти.')
            return redirect(url_for('login'))  # будет маршрут ниже
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Простая проверка (в реальном приложении используй хэширование и БД)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect('/admin')
        else:
            flash('Неверный логин или пароль')

    return render_template('login.html')


class SecureModelView(ModelView):
    def is_accessible(self):
        return 'logged_in' in session

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user doesn't have access
        return redirect(url_for('login'))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300), nullable=True)
    subdescription = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f'<Service {self.name}>'


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FIO = db.Column(db.String(200), nullable=False)
    Number = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return f'<Application {self.FIO} - {self.Number}>'


admin = Admin(app, name='Админ панель', template_mode='bootstrap3')
admin.add_view(ModelView(Application, db.session))
admin.add_view(ModelView(Service, db.session))


@app.route('/', methods=['GET', 'POST'])
def index():
    services = Service.query.all()

    if request.method == 'POST':
        try:
            fio = request.form['fio']
            number = request.form['number']
            logging.debug(f"Received form data: FIO={fio}, Number={number}")

            new_application = Application(FIO=fio, Number=number)
            db.session.add(new_application)
            db.session.commit()

            logging.info("Application successfully submitted!")
            # Используем render_template вместо redirect для передачи success
            return render_template('index.html',
                                   services=services,
                                   success="Ваша заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.")
        except Exception as e:
            logging.error(f"Error processing form submission: {e}", exc_info=True)
            return render_template('index.html',
                                   error="Произошла ошибка. Попробуйте снова.",
                                   services=services)

    return render_template('index.html', services=services)


@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            file = request.files['image']

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                image_url = f'/static/img/{filename}'
                new_service = Service(name=name, description=description, image_url=image_url)
                db.session.add(new_service)
                db.session.commit()
                logging.info(f"Service '{name}' added successfully with image {filename}")
                return redirect('/')
            else:
                logging.warning("Неверный формат файла.")
                return "Недопустимый формат изображения"
        except Exception as e:
            db.session.rollback()
            logging.error(f"Ошибка при добавлении услуги: {e}", exc_info=True)
            return "Произошла ошибка при добавлении услуги"
    return render_template('add_service.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

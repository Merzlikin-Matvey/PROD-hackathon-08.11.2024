import json

from loguru import logger
from flask import Flask, flash, redirect, render_template, request, url_for, jsonify, make_response, send_from_directory
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, get_jwt
import os
from dotenv import load_dotenv

from src.logic.adapter import Adapter
from src.logic.event import EventDate, EventType, Event
from src.logic.tour import Tour
from src.server.auth import handle_login, handle_registration
from flask_swagger_ui import get_swaggerui_blueprint
from src.logic.user import User

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


log_file = os.path.join(log_dir, "server_{time}.log")
logger.add(log_file, format="{time} {level} {message}", level="INFO", rotation="10 MB", compression="zip")

load_dotenv(dotenv_path='./.env', verbose=True)

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yaml'

jwt = JWTManager(app)


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

@app.route('/')
def index():
    logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token, error = handle_login(data)
    print("my token", token)
    if token:
        return jsonify(access_token_cookie=token), 200
    return jsonify(error=error), 401

@app.route('/registration', methods=['POST'])
def registration():
    print("Я ТУТ")
    data = request.get_json()
    error = handle_registration(data)
    if error:
        logger.warning(f'Registration failed: {error}')
        return jsonify(error=error), 400
    else:
        logger.info('User registered successfully')
        return '', 200

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    logger.info('Expired token detected, redirecting to login')
    return redirect(url_for('login'))


@app.route('/activate', methods=['GET'])
def activate_account():
    email = request.args.get('email')
    activation_key = request.args.get('key')
    print(email, activation_key)
    if not email or not activation_key:
        return jsonify(error='Email or activation key not provided'), 400

    db = Adapter()
    user = db.sel_userdata_by_activation_key(email, activation_key)
    if not user:
        return jsonify(error='Invalid email or activation key'), 400

    if user['is_active']:
        return jsonify(error='Account has already been activated'), 400

    db.update('users_2', 'is_active = TRUE', user['uuid'])
    return jsonify(message='Success'), 200

@app.route('/ping', methods=['GET'])
def ping():
    logger.info('Ping request received')
    return jsonify(ping='pong')


@app.route('/jwt_ping', methods=['GET'])
@jwt_required()
def jwt_ping():
    logger.info('Ping request received')
    return jsonify(ping='pong')


@app.route('/add_tour', methods=['POST'])
@jwt_required()
def add_tour():
    print("СОЗДАНИЕ ТУРА")
    data = request.get_json()
    user_email = get_jwt_identity()
    user = User(email=user_email)
    tour = Tour(name=data['name'], country=data['country']).save_to_repository()
    user.add_tour(tour.get_uuid())
    return jsonify(
        message='Tour added',
        uuid=tour.get_uuid()
    ), 200

@app.route('/delete_tour', methods=['POST'])
@jwt_required()
def delete_tour():
    data = request.get_json()
    user_email = get_jwt_identity()
    user = User(email=user_email)
    user.remove_tour(data['uuid'])
    return jsonify(message='Tour deleted'), 200


@app.route('/user_tours', methods=['GET'])
@jwt_required()
def get_user_tours():
    user_email = get_jwt_identity()
    print(user_email)
    user = User(email=user_email)
    tours = user.get_all_tours()
    return jsonify(tours=tours), 200


@app.route('/add_event', methods=['POST'])
@jwt_required()
def add_event():
    data = request.get_json()
    user_email = get_jwt_identity()
    user = User(email=user_email)
    tour_uuid = data['tour_uuid']

    if tour_uuid not in user.get_all_tours():
        return jsonify(error='Tour does not belong to the user'), 403

    event_data = data.get('event_data', {})


    event = Event(
        name=data['name'],
        event_type=EventType(data['event_type']),
        event_date=EventDate(data['start_date'], data['end_date']),
        event_data=event_data
    )
    event.save_to_repository()

    tour = Tour.get_tour_by_uuid(tour_uuid)
    tour.add_event(event.get_uuid())
    tour.save_to_repository()
    return jsonify(message='Event added'), 200

@app.route('/events', methods=['GET'])
@jwt_required()
def get_all_events():
    tour_uuid = request.args.get('tour_uuid')
    if not tour_uuid:
        return jsonify(error='Tour UUID is required'), 400

    tour = Tour.get_tour_by_uuid(tour_uuid)
    if not tour:
        return jsonify(error='Tour not found'), 404

    events = tour.get_events()
    info = []

    for event in events:
        event_info = event.get_event_info()
        info.append(event_info)
    return jsonify(events=info), 200

@app.route('/delete_event', methods=['POST'])
@jwt_required()
def delete_event():
    data = request.get_json()
    user_email = get_jwt_identity()
    user = User(email=user_email)
    tour_uuid = data['tour_uuid']
    event_uuid = data['event_uuid']

    if tour_uuid not in user.get_all_tours():
        return jsonify(error='Tour does not belong to the user'), 403

    tour = Tour.get_tour_by_uuid(tour_uuid)
    tour.remove_event(event_uuid)
    return jsonify(message='Event deleted'), 200

@app.route('/update_event', methods=['POST'])
@jwt_required()
def update_event():
    data = request.get_json()
    print(data)
    user_email = get_jwt_identity()
    user = User(email=user_email)
    tour_uuid = data.get('tour_uuid')
    event_uuid = data.get('event_uuid')

    if not tour_uuid or not event_uuid:
        return jsonify(error='Tour UUID and Event UUID are required'), 400

    if tour_uuid not in user.get_all_tours():
        return jsonify(error='Tour does not belong to the user'), 403

    tour = Tour.get_tour_by_uuid(tour_uuid)
    event = Event.get_event_by_uuid(event_uuid)
    if not event:
        return jsonify(error='Event not found'), 404

    if 'name' in data:
        event.name = data['name']
    if 'event_type' in data:
        event.event_type = EventType(data['event_type'])
    if 'start_date' in data and 'end_date' in data:
        event.event_date = EventDate(data['start_date'], data['end_date'])
    if 'event_data' in data:
        event.event_data = data['event_data']

    print(event.get_event_info())
    event.save_to_repository()

    return jsonify(message='Event updated'), 200

@app.route('/tours', methods=['GET'])
@jwt_required()
def get_all_tours():
    user_email = get_jwt_identity()
    user = User(email=user_email)
    tours = user.get_all_tours()

    tour_objects = [Tour.get_tour_by_uuid(tour_uuid) for tour_uuid in tours]
    tour_objects = [tour for tour in tour_objects if tour]
    sorted_tours = sorted(tour_objects, key=lambda tour: tour.get_start() or datetime.max)

    tour_info = []
    for tour in sorted_tours:
        tour_info.append({
            'uuid': tour.get_uuid(),
            'name': tour.name,
            'country': tour.country,
            'events': tour.events,
            'planned_budget': tour.planned_budget,
            'start_date': tour.get_start(),
            'end_date': tour.get_end()
        })

    return jsonify(tours=tour_info), 200


@app.route('/change_airline', methods=['POST'])
@jwt_required()
def change_airline():
    data = request.get_json()
    user_email = get_jwt_identity()
    user = User(email=user_email)

    flight_number = data.get('flight_number')
    new_start_time = data.get('new_start_   time')
    new_end_time = data.get('new_end_time')

    if not user.airline:
        return jsonify(error='User is not allowed to change airline events'), 403

    if not flight_number:
        return jsonify(error='Flight number is required'), 400

    db = Adapter()
    all_events = db.sel_all_events()
    print(new_start_time, new_end_time)
    for event in all_events:
        event_data = event[3]  # Assuming event_data is the 6th column in the events table
        try:
            if isinstance(event_data, str):
                event_data = json.loads(event_data)
            print(event_data)
            if event_data.get('flight_number') == str(flight_number):
                event_uuid = event[5]  # Assuming uuid is the 1st column in the events table
                event_obj = Event.get_event_by_uuid(event_uuid)
                print('win')
                print(event_obj.event_data)
                event_obj.event_date = EventDate(new_start_time, new_end_time)
                event_obj.save_to_repository()
        except:
            pass

    return jsonify(message='Airline events updated'), 200

@app.route('/set_airline', methods=['POST'])
def set_airline():
    data = request.get_json()
    user_uuid = data.get('user_uuid')
    admin_key = data.get('admin_key')

    if not user_uuid or not admin_key:
        return jsonify(error='User UUID and Admin Key are required'), 400

    if admin_key != os.getenv('ADMIN_KEY'):
        return jsonify(error='Invalid Admin Key'), 403

    db = Adapter()
    user_data = db.select_sth_by_uuid('*', 'users_2', user_uuid)
    if not user_data:
        return jsonify(error='User not found'), 404

    db.update('users_2', "airline = TRUE", user_uuid)
    return jsonify(message='User airline status updated'), 200



swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API вашего сервера"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    logger.info('Starting server')
    app.run(debug=True)
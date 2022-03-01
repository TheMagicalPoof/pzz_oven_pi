from flask import Blueprint, request, render_template, jsonify
from .models import Schedule, Mode
from sqlalchemy import desc, asc
from . import db, socketio
from flask_login import login_required, current_user
from datetime import datetime, time
from flask_socketio import emit

import sys

schedule = Blueprint('schedule', __name__)

@schedule.route('/schedule')
@login_required
def schedule_handle():
    return render_template("schedule.html")

@socketio.on('remove')
def handle_my_custom_event(id):
    if not current_user.is_authenticated:
        return
    Schedule.query.filter(Schedule.id == id).delete()
    db.session.commit()
    # print(id, file=sys.stdout)

@socketio.on('add')
def add_schedule_elem(data):
    if not current_user.is_authenticated:
        return
    time_obj = datetime.strptime(data["time"], "%H:%M")
    schedule = Schedule.query.filter_by(weekday=data["weekday"], hour=time_obj.hour, minute=time_obj.minute).first()
    if schedule:
        return
    new_schedule_elem = Schedule(weekday=data["weekday"], hour=time_obj.hour, minute=time_obj.minute, mode=data["mode"])
    db.session.add(new_schedule_elem)
    db.session.commit()

    get_schedule()

@lru_cache(maxsize=10)
def get_mode_data(mode: int):
    mode_data = Mode.query.filter_by(id=mode).first()
    return mode_data if mode_data else None

@socketio.on('get_all_modes')
def emit_all_modes():
    if not current_user.is_authenticated:
        return
    modes = {}
    for elem in Mode.query.all():
        modes.update({elem.id: elem.name})
    emit("all_modes", modes)

@socketio.on('get_schedule')
def get_schedule():
    if not current_user.is_authenticated:
        return
    schedule = Schedule.query.order_by(asc(Schedule.hour))
    data = {1: {"name": "Понедельник", "value": "mon", "schedule": []},
            2: {"name": "Вторник", "value": "tue", "schedule": []},
            3: {"name": "Среда", "value": "wed", "schedule": []},
            4: {"name": "Четверг", "value": "thu", "schedule": []},
            5: {"name": "Пятница", "value": "fri", "schedule": []},
            6: {"name": "Суббота", "value": "sat", "schedule": []},
            7: {"name": "Воскресенье", "value": "sun", "schedule": []}}

    for elem in schedule:
        minute = "0" + str(elem.minute) if elem.minute < 10 else str(elem.minute)
        data_elem = {"id": str(elem.id),
                     "type": get_mode_data(elem.mode).name,
                     "time": str(elem.hour) + ":" + minute,
                     "red": get_mode_data(elem.mode).red,
                     "green": get_mode_data(elem.mode).green,
                     "blue": get_mode_data(elem.mode).blue}

        data[elem.weekday]["schedule"].append(data_elem)

    emit("get_schedule", data)


# emit("telemetry", {"conv": "666", "fan": "1488", "heater": "9999", "light": "blue"})
# emit("status", {"current": "MODE2", "time_now": "14:88", "ending": "16:28", "next": "IDLE"})

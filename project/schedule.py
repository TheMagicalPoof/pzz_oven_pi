from flask import Blueprint, request, render_template, jsonify
from .models import Schedule
from . import db, socketio
from flask_login import login_required
from datetime import datetime, time
from flask_socketio import SocketIO

import sys

schedule = Blueprint('schedule', __name__)

@schedule.route('/schedule')
@login_required
def main():

    schedule = Schedule.query.all()
    print(schedule, file=sys.stderr)
    print(schedule[0], file=sys.stderr)
    data = {"Понедельник": [],
            "Вторник": [],
            "Среда": [],
            "Четверг": [],
            "Пятница": [],
            "Суббота": [],
            "Воскресенье": []}

    for elem in schedule:
        data_elem = {"id": str(elem.id), "type": str(elem.mode), "time": str(elem.hour) + ":" + str(elem.minute)}
        if elem.weekday == 1:
            data["Понедельник"].append(data_elem)
        elif elem.weekday == 2:
            data["Вторник"].append(data_elem)
        elif elem.weekday == 3:
            data["Среда"].append(data_elem)
        elif elem.weekday == 4:
            data["Четверг"].append(data_elem)
        elif elem.weekday == 5:
            data["Пятница"].append(data_elem)
        elif elem.weekday == 6:
            data["Суббота"].append(data_elem)
        elif elem.weekday == 7:
            data["Воскресенье"].append(data_elem)

    return render_template("schedule.html", schedule=data)

@schedule.route('/addschedule', methods=['POST'])
def add():
    weekday = request.form.get("weekday")
    mode = request.form.get("mode")
    time = request.form.get("time")
    time_obj = datetime.strptime(time, "%H:%M")
    schedule = Schedule.query.filter_by(weekday=weekday, hour=time_obj.hour, minute=time_obj.minute).first()
    if schedule:
        return jsonify("Elem already exist")
    new_schedule_elem = Schedule(weekday=weekday, hour=time_obj.hour, minute=time_obj.minute, mode=mode)
    db.session.add(new_schedule_elem)
    db.session.commit()
    return jsonify("element created")


# @socketio.on("web", namespace="/sock")
@socketio.on("web", namespace="/sock")
def on_connect(message):
    print(message, file=sys.stdout)
    print("o4ko", file=sys.stdout)


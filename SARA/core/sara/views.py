"""
add button
setting button
if no users add user
setting
"""
import threading
from uuid import UUID

import validators
from socketio import BaseManager

async_mode = None

import os

from django.http import HttpResponse
import socketio

basedir = os.path.dirname(os.path.realpath(__file__))


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    if uuid_to_test == None:
        return False
    else:
        try:
            uuid_obj = UUID(uuid_to_test).version
            return True
        except ValueError:
            return False


class Cm(BaseManager):
    def leave_room(self, sid, namespace, room):
        """Remove a client from a room."""
        try:
            if is_valid_uuid(room):
                print(room)
                r = Rooms.objects.filter(room_id=room)
                if not (r.count() == 0):
                    r = r[0]
                    r.count_s -= 1
                    r.upd()
            del self.rooms[namespace][room][sid]
            if len(self.rooms[namespace][room]) == 0:
                del self.rooms[namespace][room]
                if len(self.rooms[namespace]) == 0:
                    del self.rooms[namespace]
        except KeyError:
            pass


sio = socketio.Server(async_mode=async_mode, client_manager=Cm())
thread = None

import random

from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import Records, Rooms


# add_widget(main)
# handles calculation and levels
def calc(request):
    return render(request, "index.html")


""" print(request.GET.keys())
calculation_l = request.GET["Calc"]"""
"""    r = Rooms()
    r.save()
    print(r.room_id)"""
def ii(request):
    return render(request,"ii.html")

def scav(request):
    return render(request, "scav.html", {"cond": "scav"})


def operate(request):
    level = request.user.level

    answer = 1
    remainder = 1

    level = int(level / 2.1)
    if level <= 1:
        level = 1
    print("Level", level)
    addition = False
    subtraction = False
    multiplication = False
    division = False
    rand = random.randint(1, 4)
    num1 = 0
    num2 = 0

    print("operate")
    if rand == 1:
        addition = True
    elif rand == 2:
        subtraction = True
    elif rand == 3:
        multiplication = True
    elif rand == 4:
        division = True

    if addition:
        num1 = random.randint(
            1 * level, 7 * level)
        num2 = random.randint(
            1 * level, 7 * level)
        answer = num1 + num2
        remainder = 0
        print("Add:", num1, "+", num2)
        calculation = f"Add: {num1} + {num2}"
    if subtraction:
        num1 = random.randint(
            3 * level, 7 * level)
        num2 = random.randint(
            0 * level, 3 * level)
        answer = num1 - num2
        remainder = 0
        print("Subtract:", num1, "-", num2)
        calculation = f"Subtract: {num1} - {num2}"
    if multiplication:
        num1 = random.randint(
            0 + level, 7 * level)
        num2 = random.randint(
            0 + level, 7 + level)
        answer = num1 * num2
        remainder = 0
        print("Multiply:", num1, "*", num2)
        calculation = f"Multiply:{num1} * {num2}"
    if division and level <= 30:
        answer = 0
        while not (int(remainder) == 0 and int(answer) >> 0):
            num1 = random.randint(
                4 + level, 7 + level)
            num2 = random.randint(
                1 + level, 4 + level)
            answer = num1 // num2
            remainder = num1 % num2
            print("Divide:", num1, "/", num2)
            print(answer, remainder)
        calculation = f"Divide: {num1} / {num2}"
        # print("Find only the divisor and ignore the remainder")
    elif division and not level >> 30:
        num1 = random.randint(
            4 * level, 7 * level)
        num2 = random.randint(
            1 + level, 4 + level)
        answer = num1 // num2
        remainder = num1 % num2
        print("Divide:", num1, "/", num2)
        print(answer, remainder)
        calculation = f"Divide: {num1} / {num2}"

    return JsonResponse({"question": calculation, "answer": answer, "remainder": remainder})


def record(request):
    r = Records(user=request.user, score=float(request.POST["PERF"]) * 100)
    r.save()

    user = request.user
    percen_tage = float(request.POST["PERF"]) * 100
    print(percen_tage)
    if percen_tage >= 84:
        user.level += 1
        print("here")
        user.save()
        return HttpResponse(f"Nice Work ,new level is,{user.level}")
    elif percen_tage <= 35:
        user.level -= 1
        user.save()
        if user.level <= 1:
            user.level = 1
        user.save()
        return HttpResponse(f"Try harder {user.level}")
    else:
        return HttpResponse("Level_____up")


# set async_mode to 'threading', 'eventlet', 'gevent' or 'gevent_uwsgi' to
# force a mode else, the best mode is selected automatically from what's
# installed


def index(request):
    global thread
    if thread is None:
        thread = sio.start_background_task(background_thread)
    return HttpResponse(open(os.path.join(basedir, 'static/index.html')))


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'},
                 namespace='/test')


@sio.event
def lobby(sid, message):
    r_inc = Rooms.objects.filter(condition=message["condition"], empty=False, full=False, in_session=True)
    if not r_inc:
        r_empty = Rooms.objects.filter(condition=message["condition"], empty=True, full=False, in_session=True)
        if not r_empty:

            r = Rooms.objects.create(condition=message["condition"], in_session=True)
            if message["condition"] == "scav":
                r.max_users = 5
            elif message["condition"] == "2vs2":
                r.max_users = 4
            else:
                r.max_users = 2
        else:
            r = r_empty[0]
    else:
        r = r_inc[0]
    print(r.room_id)
    sio.emit('lobby', {'data': str(r.room_id)}, room=sid)


@sio.event
def confirm(sid, message):
    sio.emit("confirm", {"data": ""}, room=message["room"])


@sio.event
def my_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=sid)


@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', {'data': message['data']})


@sio.event
def join(sid, message):
    r = Rooms.objects.filter(room_id=message["room"])[0]
    r.count_s += 1
    r.upd()
    sio.enter_room(sid, message['room'])
    sio.emit('clear', {"data": "free"}, room=message['room'])
    if r.full:
        sio.emit("full", {}, room=message["room"])


@sio.event
def audio(sid, message):
    print("audio received")
    sio.emit("audio", {"data": message["aud"]}, room=sid)


@sio.event
def leave(sid, message):
    r = Rooms.objects.filter(room_id=message["room"]).count()
    r.count_s -= 1
    r.upd()
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)


@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    threading.Timer(20, sio.close_room, [message['room']])


@sio.event
def my_room_event(sid, message):
    try:
        d = float(message['data'])
    except:

        sio.emit('que', {'data': message['data']}, room=message['room'])
    else:
        sio.emit('done', {'data': d * 100}, room=message['room'])


@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)


@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

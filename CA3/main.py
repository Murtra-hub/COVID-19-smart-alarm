"""
This module runs a local web server that will need to run continuously and respond to
events rather than responding inline with user inputs. These events can be scheduled
by the user, for example set an alarm, or triggered by external events
and require an event driven software architecture that uses scheduled tasks, for example
every 6 hours show a notification with the weather o the location the user wants.
"""

import logging
import time
import sched
from test import tests
import pyttsx3
from flask import Flask, request, render_template
from time_conversions import alarm_to_time, current_time
from weather_update import get_weather
from get_covid_cases import get_cases
from news_filter import get_news




s = sched.scheduler(time.time, time.sleep)
s.run()
app = Flask(__name__)
engine = pyttsx3.init()
notifications = []
alarmsdict = {}
logging.basicConfig(filename= 'sys.log', encoding='utf-8', level=logging.DEBUG)

def print_news():
    """
    This function adds every six hours new weather, news and cases notifications
    into the notifications list that will be later displayed on the web server.
    """

    news_function = get_news()
    weather_funtion = get_weather()
    cases_function = get_cases()
    notifications.append({'title': current_time() + " - Weather", 'content': weather_funtion})
    notifications.append({'title': current_time() + " - Top news", 'content': news_function})
    notifications.append({'title': current_time() + " - Cases", 'content': cases_function})
    logging.info("Notifications added to notifications list")
    s.enter(6*3600, 5, print_news, [])

#Function called before the web server is started so when the user enters the interface
#he or she can read the notifications without having to wait the whole 6h.
print_news()

@app.route('/')
@app.route("/index")
def index():
    """
    This funtion controls all the functions of the web server, it is the one
    that returns the template of the web, submits alarms and notifications ...
    """

    s.run(blocking=False)
    alarm_time = request.args.get("alarm")
    alarm_item = request.args.get("alarm_item")
    alarm_news = request.args.get("news")
    alarm_weather = request.args.get("weather")
    notification_item = request.args.get("notif")

    if alarm_time:
        #Dectection of wether is a simple alarm, a news alarm, a weather alarm or a complete alarm
        if alarm_news and alarm_weather:
            logging.info("Alarm setted with news and weather")
            put_alarm_weather_news(alarm_time)
        else:
            if alarm_news:
                logging.info("Alarm setted with news")
                put_alarm_news(alarm_time)
            else:
                if alarm_weather:
                    logging.info("Alarm setted with weather")
                    put_alarm_weather(alarm_time)
                else:
                    logging.info("Alarm setted")
                    put_alarm(alarm_time)

    if alarm_item:
        #Selected alarm removed
        logging.info(alarm_time)
        quit_alarm(alarm_item)

    if notification_item:
        #Selected notification removed
        logging.info("Notification quited")
        quit_notification(notification_item)

    return render_template('index.html', title='Daily update', notifications=notifications ,alarms = alarmsdict.values(), image='clock.jpg')

def put_alarm_weather_news(alarm_time):
    """
    This function sets an alarm that will say out loud it's content and
    the weather of the place selected in advance and also the top news of the day.
    """

    #Time when the alarm is setted transformed to seconds
    tiempo = alarm_to_time(alarm_time)
    alarm_content = request.args.get("two")
    date = alarm_time[0: 10]
    hour = alarm_time[-5:-3] + ':' + alarm_time[-2:]
    alarm_title = "Alarm setted the "+ date + ' at ' + hour

    #Detection if the alarm is setted on the future or in the past
    if tiempo < time.time():
        structure = {'title': alarm_title, 'content': 'INVALID TIME', 'event': None}
        alarmsdict[structure['title']] = structure
    else:
        scheduled_time = s.enterabs(tiempo, 1 , announce_weather_and_news, [alarm_content,])
        structure = {'title': alarm_title, 'content': alarm_content, 'event': scheduled_time}
        alarmsdict[structure['title']] = structure

def put_alarm_news(alarm_time):
    """
    This function sets an alarm that will say out loud
    it's content and the top news of the day.
    """

    #Time when the alarm is setted transformed to seconds
    tiempo = alarm_to_time(alarm_time)
    alarm_content = request.args.get("two")
    date = alarm_time[0: 10]
    hour = alarm_time[-5:-3] + ':' + alarm_time[-2:]
    alarm_title = "Alarm setted the "+ date + ' at ' + hour

    #Detection if the alarm is setted on the future or in the past
    if tiempo < time.time():
        structure = {'title': alarm_title, 'content': 'INVALID TIME', 'event': None}
        alarmsdict[structure['title']] = structure
    else:
        scheduled_time = s.enterabs(tiempo, 1 , announce_news, [alarm_content,])
        structure = {'title': alarm_title, 'content': alarm_content, 'event': scheduled_time}
        alarmsdict[structure['title']] = structure

def put_alarm_weather(alarm_time):
    """
    This function sets an alarm that will say out loud it's content and
    the weather of the place selected in advance.
    """

    #Time when the alarm is setted transformed to seconds
    tiempo = alarm_to_time(alarm_time)
    alarm_content = request.args.get("two")
    date = alarm_time[0: 10]
    hour = alarm_time[-5:-3] + ':' + alarm_time[-2:]
    alarm_title = "Alarm setted the "+ date + ' at ' + hour

    #Detection if the alarm is setted on the future or in the past
    if tiempo < time.time():
        structure = {'title': alarm_title, 'content': 'INVALID TIME', 'event': None}
        alarmsdict[structure['title']] = structure
    else:
        scheduled_time = s.enterabs(tiempo, 1 , announce_weather, [alarm_content,])
        structure = {'title': alarm_title, 'content': alarm_content, 'event': scheduled_time}
        alarmsdict[structure['title']] = structure

def put_alarm(alarm_time):
    """
    This function sets an alarm that will say out loud it's content.
    """

    #Time when the alarm is setted transformed to seconds
    tiempo = alarm_to_time(alarm_time)
    alarm_content = request.args.get("two")
    date = alarm_time[0: 10]
    hour = alarm_time[-5:-3] + ':' + alarm_time[-2:]
    alarm_title = "Alarm setted the "+ date + ' at ' + hour

    #Detection if the alarm is setted on the future or in the past
    if tiempo < time.time():
        structure = {'title': alarm_title, 'content': 'INVALID TIME', 'event': None}
        alarmsdict[structure['title']] = structure
    else:
        scheduled_time = s.enterabs(tiempo, 1 , announce, [alarm_content,])
        structure = {'title': alarm_title, 'content': alarm_content, 'event': scheduled_time}
        alarmsdict[structure['title']] = structure

def quit_notification(notification_item):
    """
    This function removes the notification you select.
    """

    #Detection of what notification has to be removed
    for item in range(0, len(notifications)):
        if notification_item == notifications[item]['title']:
            try:
                notifications.remove(notifications[item])
                break
            except IndexError:
                logging.warning('notifications Index error')

def quit_alarm(alarm_item):
    """
    This function removes the alarm you select.
    """

    #Detection of what notification has to be removed
    alarm_selected = alarmsdict[alarm_item]

    if alarm_selected:
        del alarmsdict[alarm_item]
        try:
            s.cancel(alarm_selected['event'])

        except ValueError:
            logging.warning('alarmsdict Value error')

        except AttributeError:
            logging.warning('alarmsdict Attribute error')

        except KeyError:
            logging.warning('alarmsdict Key error')



def announce(announcement):
    """
    This function says out loud the content of the alarms that
    are not expected to contain neither the weather or the news.
    """

    logging.info("Alarm has been said")
    try:
        engine.endLoop()
    except:
        logging.error('PyTTSx3 Endloop error')

    engine.say(announcement)
    engine.runAndWait()

def announce_weather(announcement):
    """
    This function says out loud the content of the alarm that is expected to
    say also the weather. It also says out loud the weather.
    """

    logging.info("Alarm with weather has been said")
    try:
        engine.endLoop()
    except:
        logging.error('PyTTSx3 Endloop error')

    engine.say(announcement + get_weather())
    engine.runAndWait()

def announce_news(announcement):
    """
    This function says out loud the content of the alarm that is expected to
    say also the news. It also says out loud the news.
    """

    logging.info("Alarm with news has been said")
    try:
        engine.endLoop()
    except:
        logging.error('PyTTSx3 Endloop error')

    engine.say(announcement + get_news())
    engine.runAndWait()

def announce_weather_and_news(announcement):
    """
    This function says out loud the content of the alarm that is expected to
    say also the weather and the news. It also says out loud the weather and the news.
    """

    logging.info("Alarm with news and weather has been said")
    try:
        engine.endLoop()
    except:
        logging.error('PyTTSx3 Endloop error')

    engine.say(announcement + get_weather() + get_news())
    engine.runAndWait()


if __name__ == '__main__':

    try:
        tests()
    except AssertionError as message:
        print(message)

    logging.info('System starting')
    app.run(debug=True)

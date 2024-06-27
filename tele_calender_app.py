import os, telebot, datetime
from secrets import API_TOKEN


class Calendar:
    def __init__(self):
        self.events = {}

    def create_event(self, event_name, event_date, event_time, event_details):
        event_id = len(self.events) + 1
        event = {
            "id": event_id,
            "name": event_name,
            "date": event_date,
            "time": event_time,
            "details": event_details
        }
        self.events[event_id] = event
        return event_id

    def read_event(self, event_id):
        try:
            return self.events[event_id]
        except:
            return False

    def delete_event(self, event_id):
        try:
            return self.events.pop(event_id)
        except:
            return False

    def edit_event(self, event_id, event_name, event_date, event_time, event_details):
        try:
            self.events[event_id]  # checks existence of the event
            event = {
                "id": event_id,
                "name": event_name,
                "date": event_date,
                "time": event_time,
                "details": event_details
            }
            self.events[event_id].update(event)
            return event_id
        except:
            return False


calender = Calendar()
bot = telebot.TeleBot(API_TOKEN)
sessions = {}  # The variable stores temporary session information (like filename)


@bot.message_handler(commands=['start'])
def main(message):
    try:
        bot.send_message(message.from_user.id, text='Calender commands: /create_event, /read_event, /edit_event, '
                                                    '/delete_event, /list_events\n'
                                                    "\n"
                                                    'Please, enter the command from the list')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['create_event'])
def create_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event name')
        bot.register_next_step_handler(message, create_event_name)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def create_event_name(message):
    try:
        sessions[message.chat.id] = {'name': message.text}
        bot.send_message(message.from_user.id, text='Please, enter event date (use format YYYY-MM-DD)')
        bot.register_next_step_handler(message, create_event_date)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def create_event_date(message):
    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
    except ValueError as err:
        bot.send_message(message.from_user.id, text='The date has unknown format')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')
    else:
        sessions[message.chat.id].update({'date': str(event_date)})
        bot.send_message(message.from_user.id, text='Please, enter event time (use format hh:mm)')
        bot.register_next_step_handler(message, create_event_time)


def create_event_time(message):
    try:
        event_time = datetime.datetime.strptime(message.text, '%H:%M').time()
    except ValueError as err:
        bot.send_message(message.from_user.id, text='The time has unknown format')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')
    else:
        sessions[message.chat.id].update({'time': str(event_time)})
        bot.send_message(message.from_user.id, text='Please, enter event details')
        bot.register_next_step_handler(message, create_event_details)


def create_event_details(message):
    try:
        event_id = calender.create_event(sessions[message.chat.id]['name'],
                                         sessions[message.chat.id]['date'],
                                         sessions[message.chat.id]['time'],
                                         message.text
                                         )
        sessions[message.chat.id] = {}
        bot.send_message(message.from_user.id, text=f'The event {event_id} has been created!')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['read_event'])
def read_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, read_event)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def read_event(message):
    try:
        event = calender.read_event(int(message.text))
        if event:
            bot.send_message(message.from_user.id, text=f"{event['name']}\n"
                                                        f"{event['date']}\n"
                                                        f"{event['time']}\n"
                                                        f"{event['details']}")
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['delete_event'])
def delete_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, delete_event)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def delete_event(message):
    try:
        event = calender.delete_event(int(message.text))
        if event:
            bot.send_message(message.from_user.id, text=f'The event {event["id"]} {event["name"]} has been deleted')
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['list_events'])
def list_events_handler(message):
    try:
        events = calender.events
        if len(events) == 0:
            bot.send_message(message.from_user.id, text='There is no events!')
        else:
            for _, event in events.items():
                bot.send_message(message.from_user.id, text=f"id {event['id']}\n"
                                                            f"{event['name']}\n"
                                                            f"{event['date']}\n"
                                                            f"{event['time']}\n"
                                                            f"{event['details']}")
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['edit_event'])
def edit_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, read_editable_event)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def read_editable_event(message):
    """Checks event existence"""
    try:
        event = calender.read_event(int(message.text))
        if event:
            bot.send_message(message.from_user.id, text=f"name: {event['name']}\n"
                                                        f"date: {event['date']}\n"
                                                        f"time: {event['time']}\n"
                                                        f"details: {event['details']}")
            bot.send_message(message.from_user.id, text='Please, enter what needs to be changed')
            sessions[message.chat.id] = {'id': int(message.text)}
            bot.register_next_step_handler(message, define_editable_event_data)
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def define_editable_event_data(message):
    try:
        sessions[message.chat.id].update({'command': message.text.lower().strip()})
        if sessions[message.chat.id]['command'] not in ['name', 'date', 'time', 'details']:
            bot.send_message(message.from_user.id, text='Unknown event data')
        else:
            bot.send_message(message.from_user.id, text='Please, enter new value')
            bot.register_next_step_handler(message, edit_event)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def edit_event(message):
    """Changes value based on decision. All other values are kept"""
    try:
        if sessions[message.chat.id]['command'] == 'name':
            event_name = message.text
            calender.edit_event(sessions[message.chat.id]['id'],
                                event_name,
                                calender.events[sessions[message.chat.id]['id']]['date'],
                                calender.events[sessions[message.chat.id]['id']]['time'],
                                calender.events[sessions[message.chat.id]['id']]['details'])
            bot.send_message(message.from_user.id, text='The name has been updated')
            sessions[message.chat.id] = {}
        elif sessions[message.chat.id]['command'] == 'date':
            try:
                event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
                calender.edit_event(sessions[message.chat.id]['id'],
                                    calender.events[sessions[message.chat.id]['id']]['name'],
                                    event_date,
                                    calender.events[sessions[message.chat.id]['id']]['time'],
                                    calender.events[sessions[message.chat.id]['id']]['details'])
                bot.send_message(message.from_user.id, text='The date has been updated')
                sessions[message.chat.id] = {}
            except ValueError as err:
                bot.send_message(message.from_user.id, text='The date has unknown format')
        elif sessions[message.chat.id]['command'] == 'time':
            try:
                event_time = datetime.datetime.strptime(message.text, '%H:%M').time()
                calender.edit_event(sessions[message.chat.id]['id'],
                                    calender.events[sessions[message.chat.id]['id']]['name'],
                                    calender.events[sessions[message.chat.id]['id']]['date'],
                                    event_time,
                                    calender.events[sessions[message.chat.id]['id']]['details'])
                bot.send_message(message.from_user.id, text='The time has been updated')
                sessions[message.chat.id] = {}
            except ValueError as err:
                bot.send_message(message.from_user.id, text='The time has unknown format')
        elif sessions[message.chat.id]['command'] == 'details':
            event_details = message.text
            calender.edit_event(sessions[message.chat.id]['id'],
                                calender.events[sessions[message.chat.id]['id']]['name'],
                                calender.events[sessions[message.chat.id]['id']]['date'],
                                calender.events[sessions[message.chat.id]['id']]['time'],
                                event_details)
            bot.send_message(message.from_user.id, text='The details have been updated')
            sessions[message.chat.id] = {}
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


bot.infinity_polling(none_stop=True, interval=1)

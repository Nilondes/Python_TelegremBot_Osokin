import telebot, datetime, logging, psycopg2
from secrets import API_TOKEN, HOST, DATABASE, USER, PASSWORD
from functions import Calendar, BotStatisticsUpdater, Appointment, PublicEvents

conn = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    port='5432'
)
calender = Calendar(conn)
bot = telebot.TeleBot(API_TOKEN)
sessions = {}  # The variable stores temporary session information (like chat id)
bot_statistics = BotStatisticsUpdater(conn)
appointments = Appointment(conn)
public_events = PublicEvents(conn)

@bot.message_handler(commands=['start'])
def main(message):
    try:
        user_name = calender.check_user_name(message.chat.id)
        if user_name:
            bot_statistics.update_user_count()
            bot.send_message(message.from_user.id, text=f'Greetings, {user_name}!\n'
                                                        '\n'
                                                        'Calender commands: /create_event, /read_event, /edit_event, '
                                                        '/delete_event, /list_events, /register, '
                                                        '/invite, /check_invitations, /check_appointments, /public_events \n'
                                                        '/export_events\n'
                                                        "\n"
                                                        'Please, enter the command from the list')
        else:
            bot.send_message(message.from_user.id, text='Please, enter your name')
            bot.register_next_step_handler(message, create_user)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['register'])
def register_user(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter your name')
        bot.register_next_step_handler(message, create_user)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def create_user(message):
    try:
        user_name = message.text.split()
        if len(user_name) != 1:
            bot.send_message(message.from_user.id, text='The name should be in one word')
            bot.register_next_step_handler(message, create_user)
        else:
            calender.create_user(message.chat.id, user_name[0])
            main(message)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['create_event'])
def create_event_handler(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        bot.send_message(message.from_user.id, text='Please, enter event name')
        bot.register_next_step_handler(message, create_event_name)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def create_event_name(message):
    try:
        sessions[message.chat.id] = {'name': message.text}
        bot.send_message(message.from_user.id, text='Please, enter event date (use format YYYY-MM-DD)')
        bot.register_next_step_handler(message, create_event_date)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def create_event_date(message):
    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
    except ValueError as err:
        bot.send_message(message.from_user.id, text='The date has unknown format '
                                                    'Please, use YYYY-MM-DD.')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")
    else:
        sessions[message.chat.id].update({'date': str(event_date)})
        bot.send_message(message.from_user.id, text='Please, enter event time (use format hh:mm)')
        bot.register_next_step_handler(message, create_event_time)


def create_event_time(message):
    try:
        event_time = datetime.datetime.strptime(message.text, '%H:%M').time()
    except ValueError as err:
        bot.send_message(message.from_user.id, text='The time has unknown format '
                                                    'Please, use hh:mm')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")
    else:
        sessions[message.chat.id].update({'time': str(event_time)})
        bot.send_message(message.from_user.id, text='Please, enter event end time')
        bot.register_next_step_handler(message, create_event_end_time)


def create_event_end_time(message):
    try:
        event_end_time = datetime.datetime.strptime(message.text, '%H:%M').time()
    except ValueError as err:
        bot.send_message(message.from_user.id, text='The time has unknown format '
                                                    'Please, use hh:mm')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")
    else:
        if event_end_time <= datetime.datetime.strptime(sessions[message.chat.id]['time'], '%H:%M:%S').time():
            bot.send_message(message.from_user.id, text='The end time cannot be less than beginning')
            return None
        sessions[message.chat.id].update({'end_time': str(event_end_time)})
        bot.send_message(message.from_user.id, text='Please, enter event details')
        bot.register_next_step_handler(message, create_event_details)


def create_event_details(message):
    try:
        event_id = calender.create_event(sessions[message.chat.id]['name'],
                                         sessions[message.chat.id]['date'],
                                         sessions[message.chat.id]['time'],
                                         message.text,
                                         message.chat.id,
                                         sessions[message.chat.id]['end_time']
                                         )
        sessions[message.chat.id] = {}
        bot_statistics.update_event_count()
        bot.send_message(message.from_user.id, text=f'The event {event_id} has been created!')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['read_event'])
def read_event_handler(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, read_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def read_event(message):
    try:
        event = calender.read_event(int(message.text), message.chat.id)
        if event:
            keyboard = telebot.types.InlineKeyboardMarkup()
            key_public = telebot.types.InlineKeyboardButton(text='Make public',
                                                             callback_data=f'public {event['id']}')
            keyboard.add(key_public)
            key_private = telebot.types.InlineKeyboardButton(text='Make private',
                                                            callback_data=f'private {event['id']}')
            keyboard.add(key_private)
            bot.send_message(message.from_user.id, text=f"{event['name']}\n"
                                                        f"{event['date']}\n"
                                                        f"{event['time']}\n"
                                                        f"{event['end_time']}\n"
                                                        f"{event['details']}", reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('public ') or call.data.startswith('private '))
def change_status(call):
    status, event_id = call.data.split()
    event_id = int(event_id)
    if public_events.check_public_event(event_id):
        public_events.change_event_status(event_id, status)
    else:
        public_events.add_public_event(event_id, status)
    bot.send_message(call.message.chat.id, text=f'The status for {event_id} has been changed to {status}')


@bot.message_handler(commands=['delete_event'])
def delete_event_handler(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, delete_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def delete_event(message):
    try:
        event = calender.delete_event(int(message.text), message.chat.id)
        if event:
            bot_statistics.update_cancelled_event_count()
            bot.send_message(message.from_user.id, text=f'The event {event["id"]} {event["name"]} has been deleted')
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['list_events'])
def list_events_handler(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        events = calender.display_events(message.chat.id)
        if len(events) == 0:
            bot.send_message(message.from_user.id, text='There is no events!')
        else:
            for _, event in events.items():
                bot.send_message(message.from_user.id, text=f"id {event['id']}\n"
                                                            f"{event['name']}\n"
                                                            f"{event['date']}\n"
                                                            f"{event['time']}\n"
                                                            f"{event['end_time']}\n"
                                                            f"{event['details']}")
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['public_events'])
def list_events_handler(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        events = public_events.get_public_events()
        if len(events) == 0:
            bot.send_message(message.from_user.id, text='There is no public events!')
        else:
            for _, event in events.items():
                bot.send_message(message.from_user.id, text=f"id {event['id']}\n"
                                                            f"{event['name']}\n"
                                                            f"{event['date']}\n"
                                                            f"{event['time']}\n"
                                                            f"{event['end_time']}\n"
                                                            f"{event['details']}")
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['edit_event'])
def edit_event_handler(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, read_editable_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def read_editable_event(message):
    """Checks event existence"""
    try:
        event = calender.read_event(int(message.text), message.chat.id)
        if event:
            bot.send_message(message.from_user.id, text=f"name: {event['name']}\n"
                                                        f"date: {event['date']}\n"
                                                        f"time: {event['time']}\n"
                                                        f"end time: {event['end_time']}\n"
                                                        f"details: {event['details']}")
            bot.send_message(message.from_user.id, text='Please, enter what needs to be changed')
            sessions[message.chat.id] = event
            bot.register_next_step_handler(message, define_editable_event_data)
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def define_editable_event_data(message):
    try:
        sessions[message.chat.id].update({'command': message.text.lower().strip()})
        if sessions[message.chat.id]['command'] not in ['name', 'date', 'time', 'end time', 'details']:
            bot.send_message(message.from_user.id, text='Unknown event data')
        else:
            bot.send_message(message.from_user.id, text='Please, enter new value')
            bot.register_next_step_handler(message, edit_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def edit_event(message):
    """Changes value based on decision. All other values are kept"""
    try:
        if sessions[message.chat.id]['command'] == 'name':
            event_name = message.text
            calender.edit_event(sessions[message.chat.id]['id'],
                                event_name,
                                sessions[message.chat.id]['date'],
                                sessions[message.chat.id]['time'],
                                sessions[message.chat.id]['details'],
                                message.chat.id,
                                sessions[message.chat.id]['end_time'])
            bot.send_message(message.from_user.id, text='The name has been updated')
            sessions[message.chat.id] = {}
        elif sessions[message.chat.id]['command'] == 'date':
            try:
                event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
                calender.edit_event(sessions[message.chat.id]['id'],
                                    sessions[message.chat.id]['name'],
                                    event_date,
                                    sessions[message.chat.id]['time'],
                                    sessions[message.chat.id]['details'],
                                    message.chat.id,
                                    sessions[message.chat.id]['end_time'])
                bot.send_message(message.from_user.id, text='The date has been updated')
                sessions[message.chat.id] = {}
            except ValueError as err:
                bot.send_message(message.from_user.id, text='The date has unknown format')
        elif sessions[message.chat.id]['command'] == 'time':
            try:
                event_time = datetime.datetime.strptime(message.text, '%H:%M').time()
                if event_time >= sessions[message.chat.id]['end_time']:
                    bot.send_message(message.from_user.id, text='The end time cannot be less than beginning')
                    return None
                calender.edit_event(sessions[message.chat.id]['id'],
                                    sessions[message.chat.id]['name'],
                                    sessions[message.chat.id]['date'],
                                    event_time,
                                    sessions[message.chat.id]['details'],
                                    message.chat.id,
                                    sessions[message.chat.id]['end_time'])
                bot.send_message(message.from_user.id, text='The time has been updated')
                sessions[message.chat.id] = {}
            except ValueError as err:
                bot.send_message(message.from_user.id, text='The time has unknown format')
        elif sessions[message.chat.id]['command'] == 'end time':
            try:
                event_end_time = datetime.datetime.strptime(message.text, '%H:%M').time()
                if event_end_time <= sessions[message.chat.id]['time']:
                    bot.send_message(message.from_user.id, text='The end time cannot be less than beginning')
                    return None
                calender.edit_event(sessions[message.chat.id]['id'],
                                    sessions[message.chat.id]['name'],
                                    sessions[message.chat.id]['date'],
                                    sessions[message.chat.id]['time'],
                                    sessions[message.chat.id]['details'],
                                    message.chat.id,
                                    event_end_time)
                bot.send_message(message.from_user.id, text='The end time has been updated')
                sessions[message.chat.id] = {}
            except ValueError as err:
                bot.send_message(message.from_user.id, text='The end time has unknown format')
        elif sessions[message.chat.id]['command'] == 'details':
            event_details = message.text
            calender.edit_event(sessions[message.chat.id]['id'],
                                sessions[message.chat.id]['name'],
                                sessions[message.chat.id]['date'],
                                sessions[message.chat.id]['time'],
                                event_details,
                                message.chat.id,
                                sessions[message.chat.id]['end_time'])
            bot.send_message(message.from_user.id, text='The details have been updated')
            sessions[message.chat.id] = {}

        bot_statistics.update_edited_event_count()
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['invite'])
def invite_user(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        bot.send_message(message.from_user.id, text='Please, enter username')
        bot.register_next_step_handler(message, check_user)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def check_user(message):
    try:
        username = message.text
        if calender.check_user_existence(username):
            bot.send_message(message.from_user.id, text='Please, enter event id')
            sessions[message.chat.id] = username
            bot.register_next_step_handler(message, add_appointment)
        else:
            bot.send_message(message.from_user.id, text=f'There is no user with name {username}')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


def add_appointment(message):
    try:
        event = calender.read_event(int(message.text), message.chat.id)
        if event:
            if appointments.is_user_busy(sessions[message.chat.id], event['date'], event['time']):
                bot.send_message(message.from_user.id, text=f'The user {sessions[message.chat.id]} is busy on {event['date']} at {event['time']}')
            else:
                appointments.add_user_appointment(sessions[message.chat.id], event)
                bot.send_message(message.from_user.id, text=f'The user {sessions[message.chat.id]} has been invited for event:')
                bot.send_message(message.from_user.id, text=f"name: {event['name']}\n"
                                                            f"date: {event['date']}\n"
                                                            f"time: {event['time']}\n"
                                                            f"details: {event['details']}")
                sessions[message.chat.id] = {}
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['check_invitations'])
def check_invitations(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        user_name = calender.check_user_name(message.chat.id)
        user_appointments = appointments.get_user_appointments(user_name, status='awaiting')
        if user_appointments:
            for appointment in user_appointments:
                keyboard = telebot.types.InlineKeyboardMarkup()
                key_confirm = telebot.types.InlineKeyboardButton(text='Confirm', callback_data=f'confirmed {appointment[5]}')
                keyboard.add(key_confirm)
                key_decline = telebot.types.InlineKeyboardButton(text='Decline', callback_data=f'declined {appointment[5]}')
                keyboard.add(key_decline)
                bot.send_message(message.from_user.id, text=f'{appointment[0]}\n'
                                                            f'{appointment[1]}-{appointment[2]}\n'
                                                            f'{appointment[3]}\n', reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, text='You have no active invitations')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.message_handler(commands=['check_appointments'])
def check_appointments(message):
    if not calender.check_user_name(message.chat.id):
        return None
    try:
        user_name = calender.check_user_name(message.chat.id)
        user_appointments = appointments.get_user_appointments(user_name, status='confirmed')
        if user_appointments:
            for appointment in user_appointments:
                bot.send_message(message.from_user.id, text=f'{appointment[0]}\n'
                                                            f'{appointment[1]}-{appointment[2]}\n'
                                                            f'{appointment[3]}\n')
        else:
            bot.send_message(message.from_user.id, text='You have no confirmed appointments')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        logging.error(f"Error occurred: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirmed ') or call.data.startswith('declined '))
def change_status(call):
    status, appointment = call.data.split()
    appointment = int(appointment)
    appointments.change_appointment_status(appointment, status)
    bot.send_message(call.message.chat.id, text=f'The status for {appointment} has been changed to {status}')


@bot.message_handler(commands=['export_events'])
def export_events(message):
    if not calender.check_user_name(message.chat.id):
        return None
    bot.send_message(message.from_user.id, text=f'http://127.0.0.1:8000/{message.chat.id}')


bot.infinity_polling(none_stop=True, interval=1)

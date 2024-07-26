import telebot, datetime
from secrets import API_TOKEN, HOST, DATABASE, USER, PASSWORD
import psycopg2


class Calendar:
    def __init__(self, connector):
        self.conn = connector
        self.cursor = conn.cursor()

    def create_event(self, event_name, event_date, event_time, event_details):
        self.cursor.execute(f"""
            INSERT INTO events (name, date, time, event_details)
            VALUES ('{event_name}', '{event_date}', '{event_time}', '{event_details}');
            """)
        self.conn.commit()
        self.cursor.execute(f"""
            SELECT id FROM events where name = '{event_name}';
            """)
        res = self.cursor.fetchall()
        event_id = res[0][0]
        return event_id

    def read_event(self, event_id):
        try:
            self.cursor.execute(f"""
                        SELECT * FROM events where id = '{event_id}';
                        """)
            res = self.cursor.fetchall()
            res_dict = {
                'id': res[0][0],
                'name': res[0][1],
                'date': res[0][2],
                'time': res[0][3],
                'details': res[0][4]
            }
            return res_dict
        except:
            return False

    def delete_event(self, event_id):
        res_dict = self.read_event(event_id)
        if res_dict:
            self.cursor.execute(f"""
            DELETE FROM events WHERE id = '{event_id}';
            """)
            self.conn.commit()
            return res_dict
        return False

    def edit_event(self, event_id, event_name, event_date, event_time, event_details):
        try:
            self.cursor.execute(f"""
                        UPDATE events SET name = '{event_name}',
                        date = '{event_date}',
                        time = '{event_time}',
                        event_details = '{event_details}'
                        WHERE id = '{event_id}';
                        """)
            self.conn.commit()
            return event_id
        except:
            return False

    def display_events(self):
        events = {}
        self.cursor.execute("""
        SELECT * FROM events;
        """)
        res = self.cursor.fetchall()
        for event in res:
            events.update({event[0]: {
                'id': event[0],
                'name': event[1],
                'date': event[2],
                'time': event[3],
                'details': event[4]}})
        return events


conn = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD
)
calender = Calendar(conn)
bot = telebot.TeleBot(API_TOKEN)
sessions = {}  # The variable stores temporary session information (like filename)



@bot.message_handler(commands=['start'])
def main(message):
    try:
        bot.send_message(message.from_user.id, text='Calender commands: /create_event, /read_event, /edit_event, '
                                                    '/delete_event, /list_events\n'
                                                    "\n"
                                                    'Please, enter the command from the list')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


@bot.message_handler(commands=['create_event'])
def create_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event name')
        bot.register_next_step_handler(message, create_event_name)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


def create_event_name(message):
    try:
        sessions[message.chat.id] = {'name': message.text}
        bot.send_message(message.from_user.id, text='Please, enter event date (use format YYYY-MM-DD)')
        bot.register_next_step_handler(message, create_event_date)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


def create_event_date(message):
    try:
        event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
    except ValueError as err:
        bot.send_message(message.from_user.id, text='The date has unknown format')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')
    else:
        sessions[message.chat.id].update({'date': str(event_date)})
        bot.send_message(message.from_user.id, text='Please, enter event time (use format hh:mm)')
        bot.register_next_step_handler(message, create_event_time)


def create_event_time(message):
    try:
        event_time = datetime.datetime.strptime(message.text, '%H:%M').time()
    except ValueError as err:
        bot.send_message(message.from_user.id, text='The time has unknown format')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')
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
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


@bot.message_handler(commands=['read_event'])
def read_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, read_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


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
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


@bot.message_handler(commands=['delete_event'])
def delete_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, delete_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


def delete_event(message):
    try:
        event = calender.delete_event(int(message.text))
        if event:
            bot.send_message(message.from_user.id, text=f'The event {event["id"]} {event["name"]} has been deleted')
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


@bot.message_handler(commands=['list_events'])
def list_events_handler(message):
    try:
        events = calender.display_events()
        if len(events) == 0:
            bot.send_message(message.from_user.id, text='There is no events!')
        else:
            for _, event in events.items():
                bot.send_message(message.from_user.id, text=f"id {event['id']}\n"
                                                            f"{event['name']}\n"
                                                            f"{event['date']}\n"
                                                            f"{event['time']}\n"
                                                            f"{event['details']}")
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


@bot.message_handler(commands=['edit_event'])
def edit_event_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter event id')
        bot.register_next_step_handler(message, read_editable_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


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
            sessions[message.chat.id] = event
            bot.register_next_step_handler(message, define_editable_event_data)
        else:
            bot.send_message(message.from_user.id, text='There is no event with this id')
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


def define_editable_event_data(message):
    try:
        sessions[message.chat.id].update({'command': message.text.lower().strip()})
        if sessions[message.chat.id]['command'] not in ['name', 'date', 'time', 'details']:
            bot.send_message(message.from_user.id, text='Unknown event data')
        else:
            bot.send_message(message.from_user.id, text='Please, enter new value')
            bot.register_next_step_handler(message, edit_event)
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


def edit_event(message):
    """Changes value based on decision. All other values are kept"""
    try:
        if sessions[message.chat.id]['command'] == 'name':
            event_name = message.text
            calender.edit_event(sessions[message.chat.id]['id'],
                                event_name,
                                sessions[message.chat.id]['date'],
                                sessions[message.chat.id]['time'],
                                sessions[message.chat.id]['details'])
            bot.send_message(message.from_user.id, text='The name has been updated')
            sessions[message.chat.id] = {}
        elif sessions[message.chat.id]['command'] == 'date':
            try:
                event_date = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
                calender.edit_event(sessions[message.chat.id]['id'],
                                    sessions[message.chat.id]['name'],
                                    event_date,
                                    sessions[message.chat.id]['time'],
                                    sessions[message.chat.id]['details'])
                bot.send_message(message.from_user.id, text='The date has been updated')
                sessions[message.chat.id] = {}
            except ValueError as err:
                bot.send_message(message.from_user.id, text='The date has unknown format')
        elif sessions[message.chat.id]['command'] == 'time':
            try:
                event_time = datetime.datetime.strptime(message.text, '%H:%M').time()
                calender.edit_event(sessions[message.chat.id]['id'],
                                    sessions[message.chat.id]['name'],
                                    sessions[message.chat.id]['date'],
                                    event_time,
                                    sessions[message.chat.id]['details'])
                bot.send_message(message.from_user.id, text='The time has been updated')
                sessions[message.chat.id] = {}
            except ValueError as err:
                bot.send_message(message.from_user.id, text='The time has unknown format')
        elif sessions[message.chat.id]['command'] == 'details':
            event_details = message.text
            calender.edit_event(sessions[message.chat.id]['id'],
                                sessions[message.chat.id]['name'],
                                sessions[message.chat.id]['date'],
                                sessions[message.chat.id]['time'],
                                event_details)
            bot.send_message(message.from_user.id, text='The details have been updated')
            sessions[message.chat.id] = {}
    except Exception as e:
        bot.send_message(message.from_user.id, text='An error occurred')
        print(f'Error occurred : {e}')


bot.infinity_polling(none_stop=True, interval=1)

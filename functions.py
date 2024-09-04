import logging
from datetime import datetime


class TableClass:
    def __init__(self, connector):
        self.conn = connector
        self.cursor = self.conn.cursor()


class Calendar(TableClass):

    def create_event(self, event_name, event_date, event_time, event_details, chat_id, end_time):
        try:
            self.cursor.execute("""
                INSERT INTO calender_event (name, date, time, event_details, chat_id, end_time)
                VALUES (%s, %s, %s, %s, %s, %s);
                """, (event_name, event_date, event_time, event_details, chat_id, end_time))
            self.conn.commit()
            self.cursor.execute("""
                SELECT id FROM calender_event WHERE name = %s and chat_id = %s;
                """, (event_name, chat_id))
            res = self.cursor.fetchall()
            event_id = res[0][0]
            logging.info(f"Event created with ID: {event_id}")
            return event_id
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def read_event(self, event_id, chat_id):
        try:
            self.cursor.execute("""
                        SELECT id, name, date, time, event_details, chat_id, end_time
                        FROM calender_event WHERE id = %s AND chat_id = %s;
                        """, (event_id, chat_id))
            res = self.cursor.fetchall()
            res_dict = {
                'id': res[0][0],
                'name': res[0][1],
                'date': res[0][2],
                'time': res[0][3],
                'details': res[0][4],
                'chat_id': res[0][5],
                'end_time': res[0][6]
            }
            return res_dict
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")
            return False

    def delete_event(self, event_id, chat_id):
        res_dict = self.read_event(event_id, chat_id)
        if res_dict:
            try:
                self.cursor.execute("""
                DELETE FROM calender_event WHERE id = %s and chat_id = %s;
                """, (event_id, chat_id))
                self.conn.commit()
                logging.info(f"Event deleted with ID: {event_id}")
                return res_dict
            except Exception as e:
                self.conn.rollback()
                logging.error(f"Error occurred: {e}")
        return False

    def edit_event(self, event_id, event_name, event_date, event_time, event_details, chat_id, end_time):
        try:
            self.cursor.execute("""
                        UPDATE calender_event SET name = %s,
                        date = %s,
                        time = %s,
                        event_details = %s,
                        end_time = %s
                        WHERE id = %s and chat_id = %s;
                        """, (event_name, event_date, event_time, event_details, end_time, event_id, chat_id))
            self.conn.commit()
            logging.info(f"Event edited with ID: {event_id}")
            return event_id
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")
            return False

    def display_events(self, chat_id):
        events = {}
        self.cursor.execute("""
        SELECT id, name, date, time, event_details, end_time FROM calender_event WHERE chat_id = %s;
        """, (chat_id,))
        res = self.cursor.fetchall()
        for event in res:
            events.update({event[0]:
                {
                'id': event[0],
                'name': event[1],
                'date': event[2],
                'time': event[3],
                'details': event[4],
                'end_time': event[5]
                }
            })
        return events

    def check_user_name(self, chat_id):
        self.cursor.execute("""
        SELECT user_name FROM calender_user WHERE chat_id = %s;
        """, (chat_id,))
        res = self.cursor.fetchall()
        if res:
            return res[0][0]
        else:
            return False

    def create_user(self, chat_id, user_name):
        try:
            if self.check_user_name(chat_id):
                self.cursor.execute("""
                UPDATE calender_user SET user_name = %s WHERE chat_id = %s;
                """, (user_name, chat_id))
                logging.info(f"User edited with ID: {chat_id}")
            else:
                self.cursor.execute(f"""
                INSERT INTO calender_user (chat_id, user_name)
                VALUES (%s, %s);
                """, (chat_id, user_name))
                logging.info(f"User created with ID: {chat_id}")
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def check_user_existence(self, user_name):
        try:
            self.cursor.execute("""
            SELECT user_name FROM calender_user WHERE user_name = %s;
            """, (user_name,))
            res = self.cursor.fetchall()
            if res:
                return res[0][0]
            else:
                return False
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")


class BotStatisticsUpdater(TableClass):
    def __init__(self, connector):
        super().__init__(connector)
        self.stat_now()


    def stat_now(self):
        try:
            date = datetime.now().date()
            self.cursor.execute("""
            SELECT * FROM calender_botstatistics WHERE date = %s;
            """, (date,))
            res = self.cursor.fetchall()
            if res:
                return res[0]
            else:
                self.cursor.execute("""
                                INSERT INTO calender_botstatistics (date, user_count, event_count, edited_events, cancelled_events)
                                VALUES (%s, 0, 0, 0, 0);
                                """, (date,))
                logging.info(f"Bot statistics started for: {date}")
            self.conn.commit()
            return self.stat_now()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")


    def update_user_count(self):
        res = self.stat_now()
        try:
            self.cursor.execute("""
            UPDATE calender_botstatistics
            SET user_count = %s + %s
            WHERE date = %s;
            """, (res[2], 1, res[1]))
            self.conn.commit()
            logging.info(f"User count increased for 1 on: {res[1]}")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def update_event_count(self):
        res = self.stat_now()
        try:
            self.cursor.execute("""
            UPDATE calender_botstatistics
            SET event_count = %s + %s
            WHERE date = %s;
            """, (res[3], 1, res[1]))
            self.conn.commit()
            logging.info(f"Event count increased for 1 on: {res[1]}")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def update_edited_event_count(self):
        res = self.stat_now()
        try:
            self.cursor.execute("""
            UPDATE calender_botstatistics
            SET edited_events = %s + %s
            WHERE date = %s;
            """, (res[4], 1, res[1]))
            self.conn.commit()
            logging.info(f"Edited event count increased for 1 on: {res[1]}")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def update_cancelled_event_count(self):
        res = self.stat_now()
        try:
            self.cursor.execute("""
            UPDATE calender_botstatistics
            SET cancelled_events = %s + %s
            WHERE date = %s;
            """, (res[5], 1, res[1]))
            self.conn.commit()
            logging.info(f"Cancelled event count increased for 1 on: {res[1]}")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")


class Appointment(TableClass):

    def get_user_appointments(self, user_name, status):
        try:
            self.cursor.execute("""
            SELECT date, time, end_time, details, status, id FROM calender_appointment WHERE user_id = %s AND status = %s;
            """, (user_name, status))
            appointments = self.cursor.fetchall()
            return appointments
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def is_user_busy(self, username, date, time):
        appointments = self.get_user_appointments(username, 'confirmed')
        for appointment in appointments:
            if date == appointment[0] and appointment[1] <= time <= appointment[2]:
                return True
        return False

    def add_user_appointment(self, user_name, event):
        try:
            self.cursor.execute("""
            INSERT INTO calender_appointment (user_id, event_id, date, time, end_time, details, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (user_name, event['id'], event['date'], event['time'], event['end_time'], event['details'], 'awaiting'))
            self.conn.commit()
            logging.info(f"Event id {event['id']} has been added in appointments for user {user_name}: ")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def change_appointment_status(self, appointment, status):
        try:
            self.cursor.execute("""
            UPDATE calender_appointment
            SET status = %s
            WHERE id = %s;
            """, (status, appointment))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")


class PublicEvents(TableClass):

    def add_public_event(self, event_id, status):
        try:
            self.cursor.execute("""
            INSERT INTO calender_publicevents (event_id, status)
            VALUES (%s, %s);
            """, (event_id, status))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def change_event_status(self, event_id, status):
        try:
            self.cursor.execute("""
            UPDATE calender_publicevents
            SET status = %s
            WHERE event_id = %s;
            """, (status, event_id))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def check_public_event(self, event_id):
        try:
            self.cursor.execute("""
            SELECT event_id, status
            FROM calender_publicevents
            WHERE event_id = %s;
            """, (event_id, ))
            return self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")

    def get_public_events(self):
        try:
            events = {}
            self.cursor.execute("""
                    SELECT ce.id, ce.name, ce.date, ce.time, ce.event_details, ce.end_time 
                    FROM calender_event ce LEFT JOIN calender_publicevents cp ON (ce.id = cp.event_id) 
                    where cp.status = 'public';
                    """)
            res = self.cursor.fetchall()
            for event in res:
                events.update({event[0]:
                    {
                        'id': event[0],
                        'name': event[1],
                        'date': event[2],
                        'time': event[3],
                        'details': event[4],
                        'end_time': event[5]
                    }
                })
            return events
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Error occurred: {e}")
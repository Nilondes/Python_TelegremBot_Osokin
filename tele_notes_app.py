import os, telebot
from secrets import API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
sessions = {}  # The variable stores temporary session information (like filename)


def build_note(message):
    """Creates txt file with note_name as name and note_text as content"""
    try:
        note_text, note_name = message.text, sessions[message.chat.id]
        path = note_name + ".txt"
        with open(path, 'w') as f:
            f.write(note_text)
        bot.send_message(message.from_user.id, text=f'The file {path} has been created!')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['create'])
def create_note_handler(message):
    """Asks user for file name"""
    try:
        bot.send_message(message.from_user.id, text='Please, enter the name of your note')
        bot.register_next_step_handler(message, create_note_name)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def create_note_name(message):
    """Asks user for file content"""
    try:
        if os.path.isfile(message.text):
            bot.send_message(message.from_user.id, text='File already exists!')
            return False
        sessions[message.chat.id] = message.text
        bot.send_message(message.from_user.id, text='Please, enter your note')
        bot.register_next_step_handler(message, build_note)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def read_note(message):
    """Checks file existence and reads it"""
    try:
        if not os.path.isfile(message.text) or not message.text.endswith('.txt'):
            bot.send_message(message.from_user.id, text='Cannot find note with this name')
            return False
        with open(message.text, 'r') as f:
            file_text = f.read()
        bot.send_message(message.from_user.id, text=file_text)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['read'])
def read_note_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter the name of the note')
        bot.register_next_step_handler(message, read_note)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['edit'])
def edit_note_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter the name of the note')
        bot.register_next_step_handler(message, read_editable_note)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def read_editable_note(message):
    """Read file and ask for new content"""
    try:
        if not os.path.isfile(message.text) or not message.text.endswith('.txt'):
            bot.send_message(message.from_user.id, text='Cannot find note with this name')
            return False
        with open(message.text, 'r') as f:
            file_text = f.read()
        sessions[message.chat.id] = message.text
        bot.send_message(message.from_user.id, text=file_text + '\n'
                                                                'Please, enter new note')
        bot.register_next_step_handler(message, edit_note)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def edit_note(message):
    """Edit file"""
    try:
        note_text, note_name = message.text, sessions[message.chat.id]
        path = note_name
        with open(path, 'w') as f:
            f.write(note_text)
        bot.send_message(message.from_user.id, text=f'The file {path} has been updated!')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['delete'])
def delete_note_handler(message):
    try:
        bot.send_message(message.from_user.id, text='Please, enter the name of the note')
        bot.register_next_step_handler(message, delete_note)
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


def delete_note(message):
    """Delete file"""
    try:
        if not os.path.isfile(message.text) or not message.text.endswith('.txt'):
            bot.send_message(message.from_user.id, text='Cannot find note with this name')
            return False
        os.remove(message.text)
        bot.send_message(message.from_user.id, text=f'The file {message.text} has been removed!')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['start'])
def main(message):
    try:
        bot.send_message(message.from_user.id, text=f"Commands: /create, /read, /edit, /delete, /show_notes\n"
                                                    'Please, enter the command from the list')
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


@bot.message_handler(commands=['show_notes'])
def display_notes(message):
    """Lists all .txt files sorted by size"""
    try:
        txt_lst = list(filter(lambda x: x.endswith('.txt'), os.listdir()))
        file_sizes = {}
        for file in txt_lst:
            file_sizes[file] = os.stat(file).st_size
        files_sorted_by_size = sorted(file_sizes.items(), key=lambda item: item[1])
        for file in files_sorted_by_size:
            bot.send_message(message.from_user.id, text=file[0])
    except:
        bot.send_message(message.from_user.id, text='An error occurred')


bot.infinity_polling(none_stop=True, interval=1)

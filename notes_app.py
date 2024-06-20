import os


def build_note(note_text, note_name):
    """Creates txt file with note_name as name and note_text as content"""
    try:
        path = note_name + ".txt"
        with open(path, 'w') as f:
            f.write(note_text)
        print(f'The file {path} has been created!')
    except:
        print('An error occurred')


def create_note():
    """Asks user for file name and content"""
    try:
        note_name = input('Please, enter the name of your note: ').strip()
        note_text = input('Please, enter your note: ').strip()
        build_note(note_text, note_name)
    except:
        print('An error occurred')


def file_exists(file_name):
    """Checks file existence"""
    try:
        if not os.path.isfile(file_name):
            print('Cannot find note with this name')
            return False
        return True
    except:
        print('An error occurred')


def read_note():
    """Reads file"""
    try:
        note_name = input('Please, enter the name of the note: ').strip()
        if file_exists(note_name):
            with open(note_name, 'r') as f:
                print(f.read())
    except:
        print('An error occurred')


def edit_note():
    """Read and edit file"""
    try:
        note_name = input('Please, enter the name of the note: ').strip()
        if file_exists(note_name):
            with open(note_name, 'r') as f:
                print(f.read())
            note_text = input('Please, enter new note: ').strip()
            with open(note_name, 'w') as f:
                f.write(note_text)
                print(f'{note_name} has been updated!')
    except:
        print('An error occurred')


def delete_note():
    """Delete file"""
    try:
        note_name = input('Please, enter the name of the note: ').strip()
        if file_exists(note_name):
            os.remove(note_name)
            print(f'The file {note_name} has been removed!')
    except:
        print('An error occurred')


def main():
    try:
        commands = ['create', 'read', 'edit', 'delete', 'show_notes']
        print('Commands: ', *commands)
        command = input('Please, enter the command from the list: ').strip().lower()
        if command == commands[0]:
            create_note()
        elif command == commands[1]:
            read_note()
        elif command == commands[2]:
            edit_note()
        elif command == commands[3]:
            delete_note()
        elif command == commands[4]:
            display_sorted_notes()
        else:
            print('The command not found. Please, use one of available commands')
    except:
        print('An error occurred')


def display_notes():
    """Lists all .txt files sorted by size"""
    try:
        txt_lst = list(filter(lambda x: x.endswith('.txt'),os.listdir()))
        file_sizes = {}
        for file in txt_lst:
            file_sizes[file] = os.stat(file).st_size
        files_sorted_by_size = sorted(file_sizes.items(), key=lambda item: item[1])
        for file in files_sorted_by_size:
            print(file[0])
    except:
        print('An error occurred')


def display_sorted_notes():
    """Lists all .txt files sorted by size in reverse order"""
    try:
        txt_lst = list(filter(lambda x: x.endswith('.txt'),os.listdir()))
        file_sizes = {}
        for file in txt_lst:
            file_sizes[file] = os.stat(file).st_size
        files_sorted_by_size = sorted(file_sizes.items(), key=lambda item: item[1], reverse=True)
        for file in files_sorted_by_size:
            print(file[0])
    except:
        print('An error occurred')


while True:
    main()
    answer = input('If you want to continue, print "Yes": ').strip().lower()
    if answer != 'yes':
        print('Good bye!')
        break

import os


def build_note(note_text, note_name):
    """Creates txt file with note_name as name and note_text as content"""
    path = note_name + ".txt"
    with open(path, 'w') as f:
        f.write(note_text)
    print(f'The file {path} has been created!')


def create_note():
    """Asks user for file name and content"""
    note_name = input('Please, enter the name of your note: ').strip()
    note_text = input('Please, enter your note: ').strip()
    build_note(note_text, note_name)


def file_exists(file_name):
    """Checks file existence"""
    if not os.path.isfile(file_name):
        print('Cannot find note with this name')
        return False
    return True


def read_note():
    """Reads file"""
    note_name = input('Please, enter the name of the note: ').strip()
    if file_exists(note_name):
        with open(note_name, 'r') as f:
            print(f.read())


def edit_note():
    """Read and edit file"""
    note_name = input('Please, enter the name of the note: ').strip()
    if file_exists(note_name):
        with open(note_name, 'r') as f:
            print(f.read())
        note_text = input('Please, enter new note: ').strip()
        with open(note_name, 'w') as f:
            f.write(note_text)
            print(f'{note_name} has been updated!')


def delete_note():
    """Delete file"""
    note_name = input('Please, enter the name of the note: ').strip()
    if file_exists(note_name):
        os.remove(note_name)
        print(f'The file {note_name} has been removed!')


def main():
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


def display_notes():
    """Lists all .txt files sorted by size"""
    txt_lst = list(filter(lambda x: x.endswith('.txt'),os.listdir()))
    file_sizes = {}
    for file in txt_lst:
        file_sizes[file] = os.stat(file).st_size
    files_sorted_by_size = sorted(file_sizes.items(), key=lambda item: item[1])
    for file in files_sorted_by_size:
        print(file[0])


def display_sorted_notes():
    """Lists all .txt files sorted by size in reverse order"""
    txt_lst = list(filter(lambda x: x.endswith('.txt'),os.listdir()))
    file_sizes = {}
    for file in txt_lst:
        file_sizes[file] = os.stat(file).st_size
    files_sorted_by_size = sorted(file_sizes.items(), key=lambda item: item[1], reverse=True)
    for file in files_sorted_by_size:
        print(file[0])


while True:
    main()
    answer = input('If you want to continue, print "Yes": ').strip().lower()
    if answer != 'yes':
        break

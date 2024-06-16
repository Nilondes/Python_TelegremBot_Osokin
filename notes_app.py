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
    print('Commands: Create, Read, Edit, Delete')
    command = input('Please, enter the command from the list: ').strip().lower()
    if command == 'create':
        create_note()
    elif command == 'read':
        read_note()
    elif command == 'edit':
        edit_note()
    elif command == 'delete':
        delete_note()
    else:
        print('The command not found. Please, use one of available commands')


while True:
    main()
    answer = input('If you want to continue, print "Yes": ').strip().lower()
    if answer != 'yes':
        break

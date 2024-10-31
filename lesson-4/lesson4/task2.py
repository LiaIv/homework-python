documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice',  'number': '11-2',        'name': 'Геннадий Покемонов'},
    {'type': 'insurance','number': '10006',       'name': 'Аристарх Павлов'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

def find_owner(doc_number):
    for doc in documents:
        if doc['number'] == doc_number:
            return doc['name']
    return None

def find_shelf(doc_number):
    for shelf, docs in directories.items():
        if doc_number in docs:
            return shelf
    return None

def command_p():
    doc_number = input('Введите номер документа:\n')
    owner = find_owner(doc_number)
    if owner:
        print(f'Результат:\nВладелец документа: {owner}')
    else:
        print('Результат:\nДокумент не найден.')

def command_s():
    doc_number = input('Введите номер документа:\n')
    shelf = find_shelf(doc_number)
    if shelf:
        print(f'Результат:\nДокумент хранится на полке: {shelf}')
    else:
        print('Результат:\nДокумент не найден.')

def main():
    while True:
        command = input('Введите команду:\n')
        if command == 'p':
            command_p()
        elif command == 's':
            command_s()
        elif command == 'q':
            break
        else:
            print('Неверная команда. Попробуйте снова.')

if __name__ == '__main__':
    main()

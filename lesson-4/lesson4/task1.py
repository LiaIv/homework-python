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

def is_document_in_directories(doc_number):
    for docs in directories.values():
        if doc_number in docs:
            return True
    return False

def command_p():
    doc_number = input('Введите номер документа:\n')
    if is_document_in_directories(doc_number):
        owner = find_owner(doc_number)
        if owner:
            print(f'Результат:\nВладелец документа: {owner}')
        else:
            print('Результат:\nВладелец документа не найден в documents.')
    else:
        print('Результат:\nДокумент не найден в directories.')

def main():
    while True:
        command = input('Введите команду:\n')
        if command == 'p':
            command_p()
        elif command == 'q':
            break
        else:
            print('Неверная команда. Попробуйте снова.')

if __name__ == '__main__':
    main()

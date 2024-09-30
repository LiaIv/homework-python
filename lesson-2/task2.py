def input_name(sex):
    sex_text = {'female': 'девушки', 'male': 'парня'}.get(sex, '')
    names = []

    while True:
        name = input(f'Введите имя {sex_text} или "стоп", чтобы завершить ввод: ').strip()
        if name.lower() == 'стоп':
            break
        names.append(name)

    return sorted(names)

# Получаем отсортированные списки имён
girls = input_name('female')
boys = input_name('male')

# Проверяем и выводим результат
if len(girls) == len(boys):
    print('Результат\nИдеальные пары:')
    for girl, boy in zip(girls, boys):
        print(f'{girl} и {boy}')
else:
    print('Внимание, кто-то может остаться без пары.')

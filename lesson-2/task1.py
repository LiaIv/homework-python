def get_middle_letters(word):
    length = len(word)
    middle = length // 2
    result = word[middle] if bool(length % 2) else word[middle - 1:middle + 1]
    print(result)

# Пример использования:
word = input("Введите слово: ")
get_middle_letters(word)
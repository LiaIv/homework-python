# File paths
input_file_path = 'visit_log.csv'
output_file_path = 'funnel.csv'

# Data for purchase categories
purchase_categories = {
    "1840e0b9d4": "Продукты",
    "4e4f90fcfb": "Электроника",
    "96064ae9e0": "Одежда",
    "b4ea53e670": "Бытовая техника",
    "6450655ae8": "Книги",
    "e1bd168161": "Игрушки",
}

def process_visits(input_file, output_file, categories):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
            # Write header to the output file
            outfile.write("user_id,source,category\n")
            next(infile)  # Skip header

            count = 0
            skipped = 0
            for i, line in enumerate(infile, start=1):
                parts = line.strip().split(',')
                if len(parts) != 2:  # Skip malformed lines
                    skipped += 1
                    continue

                user_id, source = parts
                category = categories.get(user_id)
                if category:
                    outfile.write(f"{user_id},{source},{category}\n")
                    count += 1

                # Log progress every 10,000 lines
                if i % 10000 == 0:
                    print(f"Обработано {i} строк")

        print(f"Файл '{output_file}' успешно создан. Записано {count} строк, пропущено {skipped} некорректных строк.")
    except FileNotFoundError:
        print(f"Файл '{input_file}' не найден. Проверьте путь.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Run the processing
process_visits(input_file_path, output_file_path, purchase_categories)

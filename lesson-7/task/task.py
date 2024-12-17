import os
import pandas as pd
from datetime import datetime

def process_client_data(csv_path):
    try:
        clients_df = pd.read_csv(csv_path)
        print("Файл успешно загружен.")

        clients_df.columns = clients_df.columns.str.strip().str.lower()
        required_cols = {"name", "device_type", "browser", "sex", "age", "bill", "region"}
        missing_cols = required_cols - set(clients_df.columns)
        if missing_cols:
            print(f"Отсутствуют необходимые столбцы: {', '.join(missing_cols)}")
            return

        clients_df = clients_df.dropna(subset=["name", "sex", "age", "bill", "region"])
        clients_df["age"] = pd.to_numeric(clients_df["age"], errors='coerce').fillna(0).apply(lambda x: int(float(x)))
        clients_df["bill"] = pd.to_numeric(clients_df["bill"], errors='coerce')
        print("Данные успешно обработаны.")

        device_translation = {
            "mobile": "с мобильного браузера",
            "tablet": "с браузера планшета",
            "laptop": "с браузера ноутбука",
            "desktop": "с браузера настольного компьютера"
        }

        def generate_description(row):
            sex = row['sex'].strip().lower()
            sex_desc = "мужского пола" if sex == 'male' else "женского пола"
            device_desc = device_translation.get(row['device_type'].strip().lower(),
                                                 f"с устройства {row['device_type']}")
            action = "совершил" if sex == 'male' else "совершила"
            return (f"Пользователь {row['name']} {sex_desc}, {row['age']} лет "
                    f"{action} покупку на {int(row['bill'])} у.е. {device_desc} "
                    f"браузера {row['browser']}. Регион, из которого совершалась покупка: {row['region']}.")

        client_descriptions = clients_df.apply(generate_description, axis=1).tolist()
        print("Описание пользователей успешно сгенерировано.")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_directory = './txt-files'
        os.makedirs(output_directory, exist_ok=True)
        output_file = os.path.join(output_directory, f'client_descriptions_{timestamp}.txt')

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(client_descriptions))

        print(f"Описание пользователей успешно сохранено в файл: {output_file}")

    except Exception as e:
        print(f"Ошибка выполнения программы: {e}")


if __name__ == "__main__":
    csv_file = 'web_clients_correct.csv'
    process_client_data(csv_file)

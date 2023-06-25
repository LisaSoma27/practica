import json
from datetime import datetime
from pathlib import Path
import db
import myconfig


def input_date():
    while True:
        try:
            date_str = input('Введите дату 2000-01-1:  ')
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print('Формат даты: год-месяц-день')


def input_num(text, nums):
    while True:
        num = input(text)
        if num in nums:
            return num
        else:
            print(f'Варианты ввода {nums}')


def create_json(logs_list, path):
    log_data = {}
    for num, log in enumerate(logs_list):
        log_data[num] = ({
            'id': log.id,
            'ip': log.ip,
            'date': str(log.date),
            'time': str(log.time),
            'timezone': log.timezone,
            'request_method': log.request_method,
            'path': log.path,
            'status': log.status,
            'bytes_sent': log.bytes_sent})
    try:
        today = datetime.now().date()
        with open(Path(path) / f'{str(today)}.json', 'w') as file:
            json.dump(log_data, file, ensure_ascii=True, indent=4)
    except Exception as e:
        print(e)


def main():
    config = myconfig.read_config()
    status = input_num(text=(
        'Выберите:\n1) Просмотр данных\n2) Сохранить данные в json файл: '), nums=['1', '2'])
    parametr = input_num(text=(
        '\nВыберите:\n1) IP\n2) Дата в формате y-m-d\n3) Промежуток: '), nums=['1', '2', '3'])
    logs = db.get_data_db(parametr, config['db'])
    if status == '1':
        for log in logs:
            print(log.ip, log.date, log.time, log.timezone,
                  log.request_method, log.path, log.status, log.bytes_sent)
    else:
        json_folder = config['json']['folder_path']
        create_json(logs, json_folder)


if __name__ == '__main__':
    main()

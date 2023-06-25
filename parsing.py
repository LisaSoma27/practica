import re
import time
import schedule
from pathlib import Path
import db 
import myconfig


def get_data_file(path):
    try:
        with open(path, encoding='utf-8') as f:
            data = f.read().split('\n')
        return data
    except (FileNotFoundError, OSError) as e:
        print(e)


def parse_data_file(data, file_name, config):
    line_start = config['file'][file_name]
    if line_start != 0:
        line_start += 1
    else:
        line_start
        
    new_data = []
    r = r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>\d{2}/\w+/\d{4}):(?P<time>\d{2}:\d{2}:\d{2}) (?P<timezone>[\+\-]\d{4})\] "(?P<request_method>\S+?) (?P<path>\S+?) \S+" (?P<status>\d+) (?P<bytes_sent>\d+)'
    for num, line in enumerate(data[line_start:]):
        match = re.match(r, line)
        if match:
            new_data.append(match.groups())
        config['file'][file_name] = num
    
    return new_data, config


def main():
    try:
        config = myconfig.read_config()
        conf_db = config['db']
        conf_path = config['path']
        for path in sorted(Path(conf_path['folder_path']).glob(f'*{conf_path["mask"]}*')):
            file_name = path.name
            if not config.get('file'):
                config['file'] = {file_name: 0}
            else:
                if not config['file'].get(file_name):
                    config['file'][file_name] = 0
            new_data, config = parse_data_file(get_data_file(path), file_name, config)
            myconfig.write_config(config)
            if new_data:
                db.change_db(new_data, conf_db)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
    cron = myconfig.read_config()['cron']
    if cron['state']:
        schedule.every(cron['repeat_minutes']).minutes.do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)



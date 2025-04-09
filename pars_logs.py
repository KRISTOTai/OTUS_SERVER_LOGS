import re
import json
import argparse
from pathlib import Path
from collections import Counter

LOG_PATTERN = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+).*?'
    r'\[(?P<date>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+(?P<url>\S+)\s+[A-Z]+\/\d\.\d"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<size>\d+|-)\s+'  # размер ответа, взял как шаблон, можно '(?P<size>\d+)\s+'
    r'"(?P<referrer>[^"]*)"\s+'
    r'"(?P<agent>[^"]*)"\s+'
    r'(?P<duration>\d+)'  # длительность запроса
)


def main():
    parser = argparse.ArgumentParser(description="Анализ access.log файлов")
    parser.add_argument("path", help="Путь к файлу или директории с логами")
    args = parser.parse_args()
    process_path(args.path)


def process_path(path):
    path = Path(path)  # Преобразование пути в объект
    if path.is_file():
        stat = parse_log_file(path)
        save_report(stat, path.with_suffix('.json'))
    elif path.is_dir():
        for log_file in path.glob('*.log'):
            stat = parse_log_file(log_file)
            save_report(stat, log_file.with_suffix('.json'))
    else:
        print("Указанный путь не существует")


def parse_log_file(filepath):
    total_requests = 0
    method_counter = Counter()
    ip_counter = Counter()
    longest_requests = []

    with open(filepath, encoding='utf-8') as f:
        for line in f:
            match = LOG_PATTERN.match(line)
            if not match:
                continue

            total_requests += 1
            data = match.groupdict()

            method_counter[data['method']] += 1
            ip_counter[data['ip']] += 1

            longest_requests.append({
                "ip": data['ip'],
                "date": data['date'],
                "method": data['method'],
                "url": data['url'],
                "duration": int(data['duration'])
            })

    # топ-3 IP
    top_ips = dict(ip_counter.most_common(3))

    # топ-3 долгих запроса
    top_longest = sorted(longest_requests, key=lambda x: x['duration'], reverse=True)[:3]
    # lambda берет каждый словарь в списке longest_requests, и извлекает значение по ключу 'duration'.

    return {
        "top_ips": top_ips,
        "top_longest": top_longest,
        "total_stat": dict(method_counter),
        "total_requests": total_requests
    }


def save_report(stat, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stat, f, indent=2, ensure_ascii=False)
    print(f"\n==== {output_file.name} ====")
    print(json.dumps(stat, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

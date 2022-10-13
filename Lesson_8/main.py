"""Getting statistics on the use of domain names for mail."""
import os
import re

from collections import Counter
from prettytable import PrettyTable
from plotly import offline
from datetime import datetime
from pathlib import Path

import examples


def calc_time(func):
    """Calc execution time"""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        func_result = func(*args, **kwargs)
        end_time = datetime.now()
        print(f'Execution time {func.__name__}: {end_time - start_time}')
        return func_result
    return wrapper


def get_path_to_file(file: str) -> str:
    """creates a path to the location of the file."""
    folder = str(Path(examples.__file__).parent.absolute())
    current_write_file = os.path.join(folder, file)
    return current_write_file


def check_file_exist(file: str) -> str | bool:
    """Check file for type txt and check if the file exists."""
    try:
        open(file, mode='rt').readline()
    except UnicodeDecodeError:
        return 'App can use only text files'
    except FileNotFoundError:
        return 'File not found.'
    return False


def normalize_data(line: str) -> str | bool:
    """Delete lines that do not contain '@'."""
    char = '@'
    if char in line:
        return line
    return False


def read_data_from_file(file: str) -> list[str]:
    """Saving information from a file."""
    with open(file) as f:
        read_file = []
        for line in f:
            clean_line = line.strip()
            normalize_line = normalize_data(clean_line)
            if normalize_line:
                read_file.append(clean_line)
    return read_file


def find_mails(file: list[str]) -> list[str]:
    """Search for emails in a file."""
    results = []
    for line in file:
        result = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
        if result:
            result = ''.join(result)
            results.append(result)
    return results


def find_domains(mails: list[str]) -> list[str]:
    """Search for domains in a emails."""
    results = []
    for mail in mails:
        result = re.findall(r'\b@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', mail)
        result = ''.join(result)
        results.append(result[1:])
    return results


def count_coincidence(mails: list[str]) -> dict[str: int]:
    """Counting coincidence."""
    return Counter(mails)


def create_table(domains: list[tuple[str, int]], position='?') -> PrettyTable:
    """Print statistics in table."""
    element_table = PrettyTable()
    element_table.field_names = [f'unique {position}', 'qwt']
    for domain in domains:
        element_table.add_row([domain[0], domain[1]])
    return element_table


def together(mails: set[str], domains: set[str]) -> tuple[dict[str, tuple[int, list[str]]], dict[str, int]]:
    """Combine unique domain names with unique emails"""
    domain_qwt_mail = {}
    domain_qwt = {}
    for domain in domains:
        step = 0
        all_mail = []
        for mail in mails:
            index_char = re.search(r'@', mail).start()
            right_part_mail = mail[index_char + 1:]
            if right_part_mail == domain:
                step += 1
                all_mail.append(mail)
                domain_qwt_mail[domain] = step, all_mail
                domain_qwt[domain] = step

    return domain_qwt_mail, domain_qwt


def create_table_domain_qwt(domains_qwt: list[str]) -> PrettyTable:
    """Print domain statistics."""
    domains_qwt_table = PrettyTable()
    domains_qwt_table.field_names = ['unique domain', 'unique quantity of email']
    for domain, qwt in domains_qwt:
        domains_qwt_table.add_row([domain, qwt])
        domains_qwt_table.add_row(['-' * 25, '-' * 25])
    return domains_qwt_table


def create_table_domain_qwt_mail(domains_mail: list[str]) -> PrettyTable:
    """Print domain statistics."""
    domains_mail_table = PrettyTable()
    domains_mail_table.field_names = ['unique domain', 'unique quantity of email', 'unique mails']
    for domain, mail in domains_mail:
        split_mail = []
        for value in sorted(mail[1]):
            split_mail.append(value + '\n')
        domains_mail_table.add_row([domain, mail[0], ''.join(split_mail)])
    return domains_mail_table


def visualize_table(data_domain_qwt: list[str]) -> bool:
    """Visualization on Bar Chart."""
    domains, qtws = [], []
    for domain, qwt in data_domain_qwt:
        domains.append(domain)
        qtws.append(qwt)

    data = [{
        'type': 'bar',
        'x': domains,
        'y': qtws,
        'marker': {
            'color': 'rgb(60, 100, 150)',
            'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'},
        },
        'opacity': 0.6,
        'text': qtws,
    }]

    my_layout = {
        'title': 'Unique quantity of email for domain.',
        'titlefont': {'size': 28},
        'font': {'size': 20},
        'xaxis': {
            'title': 'Unique domain.',
            'titlefont': {'size': 24},
            'tickfont': {'size': 20},
        },
        'yaxis': {
            'title': 'Unique quantity of email.',
            'titlefont': {'size': 24},
            'tickfont': {'size': 14},
        },
    }

    fig = {'data': data, "layout": my_layout}
    offline.plot(fig, filename='table_result_domain_qwt.html')
    return True

@calc_time
def write_to_file(table: PrettyTable, file='') -> bool:
    """Wright table to text file."""
    with open(file, 'w') as f:
        print(table, file=f)
    return True


def work_with_mails(mails: list[str]) -> bool:
    """I count how many times the mail occurs and save it to a file in sorted form."""
    coincidence_mails = count_coincidence(mails)
    coincidence_mails = coincidence_mails.most_common()
    table_mails = create_table(coincidence_mails, position='mail')
    write_to_file(table_mails, file='mails.txt')
    return True


def work_with_domains(domains: list[str]) -> bool:
    """I count how many times the domain occurs and save it to a file in sorted form."""
    coincidence_domains = count_coincidence(domains)
    coincidence_domains = coincidence_domains.most_common()
    table_domains = create_table(coincidence_domains, position='domain')
    write_to_file(table_domains, file='domains.txt')
    return True


@calc_time
def main(file: str):
    path_file = get_path_to_file(file)

    check = check_file_exist(path_file)
    if check:
        print(check)
        exit()

    normalized_file = read_data_from_file(path_file)

    mails = find_mails(normalized_file)
    work_with_mails(mails)

    domains = find_domains(mails)
    work_with_domains(domains)

    unique_mails = set(mails)
    unique_domains = set(domains)
    unique_domains_qwt_mail, unique_domains_qwt = together(unique_mails, unique_domains)

    unique_domains_qwt = sorted(unique_domains_qwt.items(), key=lambda x: x[1], reverse=True)
    table_result_domain_qwt = create_table_domain_qwt(unique_domains_qwt)
    print(table_result_domain_qwt)
    visualize_table(unique_domains_qwt)

    unique_domains_qwt_mail = sorted(unique_domains_qwt_mail.items(), key=lambda x: x[1], reverse=True)
    table_result_domain_qwt_mail = create_table_domain_qwt_mail(unique_domains_qwt_mail)
    write_to_file(table_result_domain_qwt_mail, file='table_domain_qwt_mail.txt')


if __name__ == '__main__':
    filename = 'mbox.txt'
    main(filename)

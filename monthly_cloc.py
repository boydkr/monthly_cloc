import os
import sys
import re
from subprocess import check_output, check_call
import datetime
import calendar

default_branch = 'origin/master'
headers = set()

def add_months(date, months):
    months_count = date.month + months

    year = date.year + int(months_count / 12)

    month = months_count % 12
    month = 12 if month == 0 else month

    day = date.day
    last_day = calendar.monthrange(year, month)[1]
    day = last_day if day > last_day else day

    return datetime.date(year, month, day)

def date_sha(date, branch):
    #print('git', 'rev-list', '-n', '1', "--before={date}".format(**locals()), branch)
    result = check_output(['git', 'rev-list', '-n', '1', "--before={date}".format(**locals()), branch])
    return result.decode('utf-8').strip()

def checkout_sha(sha):
    result = check_call(['git', 'checkout', sha])

def count_lines():
    result = check_output(['cloc', '--vcs=git'])
    return result.decode('utf-8').strip()

def current_commit():
    return check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()

def decode_lines(cloc_output):
    lines = [x.strip() for x in cloc_output.split("\n")]
    start = False
    header = False
    result = {}
    for line in lines:
        if re.fullmatch(r'-+', line):
            if header:
                start = True
            else:
                header = True
            continue
        if not start:
            continue
        parse_line(line, result)
    return result

def parse_line(line, result):
    stats = line.split()
    header = stats[0]
    headers.add(header)
    result[header] = stats[4]
    return result

def str_to_date(datestr, format="%Y-%m-%d"):
    return datetime.datetime.strptime(datestr, format).date()

def collect_data(dates, branch):
    collected_data = {}
    for date in dates:
        sha = date_sha(date, branch)
        checkout_sha(sha)
        cloc_output = count_lines()
        stats = decode_lines(cloc_output)
        collected_data[date] = stats

    return collected_data

def format_csv(headers, data):
    outlines = []

    header_list = list(headers)
    header_list.sort()

    #Move SUM to the end
    header_list.remove('SUM:')
    header_list.append('SUM:')

    outlines.append('Date, ' + ', '.join(header_list))
    for date in dates:
        outlines.append("{date}, ".format(**locals()) + ', '.join([ date_stats[date].get(header, '0') for header in header_list ]))

    return "\n".join(outlines)

def parse_args(args):
    if not len(args) >= 3:
        print('Usage: monthly_cloc YYYY-mm-dd month_count [git_branch]')
        exit(1)

    start = str_to_date(args[1])
    months = int(args[2])
    branch = args[3] if len(args) > 3 else default_branch
    return start, months, branch

if __name__ == "__main__":
    start, months, branch = parse_args(sys.argv)

    dates = []

    start_sha = current_commit()

    for month in range(months):
        date = str(add_months(start, month))
        dates.append(date)

    date_stats = {}
    try:
        date_stats = collect_data(dates, branch)
    finally:
        checkout_sha(start_sha)

    csv = format_csv(headers, date_stats)

    print(csv)

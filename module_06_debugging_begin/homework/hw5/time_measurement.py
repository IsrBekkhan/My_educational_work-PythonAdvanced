"""
Программа для расчета среднего времени работы функции measure_me, на основании информации из лог-файла 'results.log'
"""

from json import loads
from datetime import timedelta


work_times = list()

with open('results.log', 'r') as log_file:

    for line in log_file.readlines():
        if 'Enter measure_me' in line:
            start_line = loads(line.rstrip('\n'))
            time = start_line['time'].split()[1]
            hour, minute, second_millisecond = time.split(':')
            second, millisecond = second_millisecond.split(',')
            start_time = timedelta(hours=int(hour),
                                   minutes=int(minute),
                                   seconds=int(second),
                                   microseconds=int(millisecond))

        if 'Leave measure_me' in line:
            end_line = loads(line.rstrip('\n'))
            time = end_line['time'].split()[1]
            hour, minute, second_millisecond = time.split(':')
            second, millisecond = second_millisecond.split(',')

            end_time = timedelta(hours=int(hour),
                                 minutes=int(minute),
                                 seconds=int(second),
                                 microseconds=int(millisecond))

            seconds_dif = end_time - start_time
            work_times.append(seconds_dif.seconds)

average_time = round(sum(work_times) / len(work_times), 3)
print(f'Среднее время работы программы: {average_time} сек')

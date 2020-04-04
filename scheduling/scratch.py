from operator import itemgetter

data = {
    'algo': 'priorr',
    'processes': [
        # {'process': 1, 'arrival': '4', 'burst': '3'},
        # {'process': 2, 'arrival': '0', 'burst': '24'},
        # {'process': 3, 'arrival': '0', 'burst': '6'},
        # {'process': 4, 'arrival': '3', 'burst': '1'},
        # {'process': 5, 'arrival': '6', 'burst': '2'},
        # {'process': 6, 'arrival': '0', 'burst': '8'},
        #
        # {'process': 1, 'arrival': '4', 'burst': '3'},
        # {'process': 2, 'arrival': '0', 'burst': '24'},
        # {'process': 3, 'arrival': '0', 'burst': '6'},
        # {'process': 4, 'arrival': '3', 'burst': '1'},
        # {'process': 5, 'arrival': '6', 'burst': '2'},
        # {'process': 6, 'arrival': '3', 'burst': '8'},
        # fcfs good
        # {'process': 1, 'arrival': '0', 'burst': '24'},
        # {'process': 2, 'arrival': '0', 'burst': '3'},
        # {'process': 3, 'arrival': '0', 'burst': '3'},
        # sjf 7 good
        # {'process': 1, 'arrival': '0', 'burst': '6'},
        # {'process': 2, 'arrival': '0', 'burst': '8'},
        # {'process': 3, 'arrival': '0', 'burst': '7'},
        # {'process': 4, 'arrival': '0', 'burst': '3'},
        # strf 6.5 good
        # {'process': 1, 'arrival': '0', 'burst': '8'},
        # {'process': 2, 'arrival': '1', 'burst': '4'},
        # {'process': 3, 'arrival': '2', 'burst': '9'},
        # {'process': 4, 'arrival': '3', 'burst': '5'},
        # rr 5.66667 good
        # {'process': 1, 'arrival': '0', 'burst': '24'},
        # {'process': 2, 'arrival': '0', 'burst': '3'},
        # {'process': 3, 'arrival': '0', 'burst': '3'},
        # priorr 13.4 good
        # {'process': 1, 'burst': '4', 'arrival': '3'},
        # {'process': 2, 'burst': '5', 'arrival': '2'},
        # {'process': 3, 'burst': '8', 'arrival': '2'},
        # {'process': 4, 'burst': '7', 'arrival': '1'},
        # {'process': 5, 'burst': '3', 'arrival': '3'},
        # prio 8.2 good
        # {'process': 1, 'burst': '10', 'arrival': '3'},
        # {'process': 2, 'burst': '1', 'arrival': '1'},
        # {'process': 3, 'burst': '2', 'arrival': '4'},
        # {'process': 4, 'burst': '1', 'arrival': '5'},
        # {'process': 5, 'burst': '5', 'arrival': '2'},
    ]
}


def round_robin(processes, init_start=0, init_end=0):
    start_time, end_time, ave_waiting_time, \
    burst_sum, index, duration, total_duration = init_start, init_end, 0, 0, 0, 0, 0
    q = 4  # quantum
    gantt_chart = {'sequence': []}
    # processes_copy = sorted(list(processes), key=itemgetter('arrival'))
    processes_copy = list(processes)

    def compute_awt():
        awt = 0
        for p in list(processes):
            occurrences = [j for j in gantt_chart['sequence'] if j['process'] == p['process']]
            previous = {}  # previous occurrence
            pwt = 0  # process waiting time
            for index, value in enumerate(occurrences):
                if index < 1:
                    pwt += value['start_time']
                    previous = value
                else:
                    pwt += value['start_time'] - previous['end_time']
                    previous = value
            awt += pwt
        return awt

    for i in processes_copy:
        burst_sum += int(i['burst'])

    partial_sum = 0
    while partial_sum < burst_sum:
        p_burst = int(processes_copy[index]['burst'])
        d = p_burst - q  # difference
        if p_burst > 0:
            duration = p_burst if d < 0 else q
            end_time += duration
            total_duration += duration
            partial_sum += duration
            processes_copy[index]['burst'] = str(p_burst - duration)
            if gantt_chart['sequence']:
                last = gantt_chart['sequence'][-1]
                start_time = last['end_time']
                gantt_chart['sequence'].append({
                    'process': processes_copy[index]['process'],
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': duration
                })
                total_duration = 0
            else:
                gantt_chart['sequence'].append({
                    'process': processes_copy[index]['process'],
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': duration
                })
                start_time = end_time
                total_duration = 0
        index = 0 if index >= len(processes_copy) - 1 else index + 1
    ave_waiting_time = compute_awt() / len(processes_copy)
    gantt_chart['ave_waiting_time'] = ave_waiting_time
    print(f'rr gantt: {gantt_chart}')
    return gantt_chart


def priority(processes):
    start_time, end_time, ave_waiting_time = 0, 0, 0
    # gantt_chart = {'sequence': list(processes)}
    gantt_chart = {'sequence': sorted(list(processes), key=itemgetter('arrival'))}
    for item in gantt_chart['sequence']:
        end_time += int(item['burst'])
        ave_waiting_time += start_time
        item['start_time'] = start_time
        item['end_time'] = end_time
        start_time = end_time
        item.pop('arrival', None)
    gantt_chart['ave_waiting_time'] = ave_waiting_time / float(len(processes))
    print(f'gantt: {gantt_chart}')
    return gantt_chart


def priority_round_robin(processes):
    start_time, end_time, ave_waiting_time = 0, 0, 0
    q = 4
    gantt_chart = {'sequence': []}
    processes_copy = sorted(list(processes), key=itemgetter('arrival'))
    # processes_copy = list(processes)

    def compute_awt():
        awt = 0
        for p in list(processes):
            occurrences = [j for j in gantt_chart['sequence'] if j['process'] == p['process']]
            previous = {}  # previous occurrence
            pwt = 0  # process waiting time
            for index, value in enumerate(occurrences):
                if index < 1:
                    pwt += value['start_time']
                    previous = value
                else:
                    pwt += value['start_time'] - previous['end_time']
                    previous = value
            awt += pwt
        return awt

    index = 0
    while index < len(processes_copy):
        same_priority = [i for i in processes_copy if i['arrival'] == processes_copy[index]['arrival']]
        if len(same_priority) > 1:
            partial_gantt = round_robin(same_priority, start_time, end_time)
            sequence = partial_gantt['sequence']
            index += len(same_priority)
            end_time = sequence[-1]['end_time']
            start_time = end_time
            gantt_chart['sequence'] += partial_gantt['sequence']
        else:
            end_time += int(processes_copy[index]['burst'])
            gantt_chart['sequence'].append({
                'process': processes_copy[index]['process'],
                'start_time': start_time,
                'end_time': end_time,
                'duration': int(processes_copy[index]['burst'])
            })
            start_time = end_time
            index += 1

    gantt_chart['ave_waiting_time'] = compute_awt() / float(len(processes))
    print(f'priorr gantt: {gantt_chart}\n\n')
    return gantt_chart


def designate_algo(algo, processes):
    switcher = {
        # 'fcfs': first_come_first_serve,
        # 'sjf': shortest_job_first,
        'rr': round_robin,
        'prio': priority,
        'priorr': priority_round_robin,
        # 'strf': shortest_time_remaining_first,
    }
    return switcher.get(algo, lambda: 'Scheduler invalid!')(processes)


def evaluate():
    algo = data['algo']
    processes = data['processes']
    print(f'{algo}')
    designate_algo(algo, processes)


if __name__ == '__main__':
    evaluate()

from flask import Flask

from operator import itemgetter


def first_come_first_serve(processes, q):
    start_time, end_time, ave_waiting_time = 0, 0, 0
    gantt_chart = {'sequence': sorted(list(processes), key=itemgetter('arrival'))}
    for item in gantt_chart['sequence']:
        end_time += item['burst']
        # ave_waiting_time += (start_time - int(item['arrival']))
        ave_waiting_time += start_time
        item['start_time'] = start_time
        item['end_time'] = end_time
        start_time = end_time
        item.pop('arrival', None)
    gantt_chart['ave_waiting_time'] = ave_waiting_time / float(len(processes))
    print(f'gantt: {gantt_chart}')
    return gantt_chart


def shortest_job_first(processes, q):
    start_time, end_time, ave_waiting_time = 0, 0, 0
    gantt_chart = {'sequence': sorted(list(processes), key=itemgetter('burst'))}
    print(f'{gantt_chart["sequence"]}')
    for item in gantt_chart['sequence']:
        item.pop('arrival', None)
        end_time += item['burst']
        ave_waiting_time += start_time
        item['start_time'] = start_time
        item['end_time'] = end_time
        start_time = end_time
    gantt_chart['ave_waiting_time'] = ave_waiting_time / float(len(processes))
    print(f'gantt: {gantt_chart}')
    return gantt_chart


def shortest_time_remaining_first(processes, q):
    start_time, end_time, ave_waiting_time, burst_sum = 0, 0, 0, 0
    gantt_chart = {'sequence': []}
    processes_copy = sorted(list(processes), key=itemgetter('arrival'))
    duration = 1

    def append_new_process(p_no, p_burst):
        gantt_chart['sequence'].append({
            'process': p_no,
            'burst': p_burst,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration
        })

    def compute_awt():
        awt = 0
        for p in list(processes):
            occurrences = [j for j in gantt_chart['sequence'] if j['process'] == p['process']]
            previous = {}  # previous occurrence
            pwt = 0  # process waiting time
            for index, value in enumerate(occurrences):
                if index < 1:
                    pwt += value['start_time'] - p['arrival']
                    previous = value
                else:
                    pwt += value['start_time'] - previous['end_time']
            awt += pwt
        return awt

    for i in processes_copy:
        burst_sum += i['burst']

    while end_time < burst_sum:
        processes_copy = [p for p in processes_copy if p['burst'] > 0]
        raw_alive = [p for p in processes_copy if p['arrival'] <= end_time]
        sorted_alive = sorted(raw_alive, key=itemgetter('burst'))
        sorted_alive[0]['burst'] = sorted_alive[0]['burst'] - 1
        shortest = sorted_alive[0]

        if shortest['burst'] < 1:
            processes_copy = [p for p in processes_copy if p['process'] != shortest['process']]

        end_time += 1
        if gantt_chart['sequence']:
            last = gantt_chart['sequence'][-1]
            if shortest['process'] != last['process']:
                duration = 1
                start_time = last['end_time']
                append_new_process(shortest['process'], shortest['burst'])
            else:
                duration += 1
                gantt_chart['sequence'][-1]['burst'] = gantt_chart['sequence'][-1]['burst'] - 1
                gantt_chart['sequence'][-1]['end_time'] = end_time
                gantt_chart['sequence'][-1]['duration'] = duration
        else:
            duration = 1
            append_new_process(shortest['process'], shortest['burst'])
            start_time = end_time
    ave_waiting_time = compute_awt() / float(len(processes))
    gantt_chart['ave_waiting_time'] = ave_waiting_time
    print(f'gantt: {gantt_chart}')
    return gantt_chart


def round_robin(processes, q, init_start=0, init_end=0):
    start_time, end_time, ave_waiting_time, \
    burst_sum, index, duration, total_duration = init_start, init_end, 0, 0, 0, 0, 0
    gantt_chart = {'sequence': []}
    processes_copy = list(processes)
    # processes_copy = sorted(list(processes), key=itemgetter('arrival'))

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
        burst_sum += i['burst']

    partial_sum = 0
    while partial_sum < burst_sum:
        p_burst = processes_copy[index]['burst']
        d = p_burst - q  # difference
        if p_burst > 0:
            duration = p_burst if d < 0 else q
            end_time += duration
            total_duration += duration
            partial_sum += duration
            processes_copy[index]['burst'] = p_burst - duration
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


def priority(processes, q):
    start_time, end_time, ave_waiting_time = 0, 0, 0
    gantt_chart = {'sequence': sorted(list(processes), key=itemgetter('priority'))}
    for item in gantt_chart['sequence']:
        end_time += item['burst']
        ave_waiting_time += start_time
        item['start_time'] = start_time
        item['end_time'] = end_time
        start_time = end_time
        item.pop('arrival', None)
    gantt_chart['ave_waiting_time'] = ave_waiting_time / float(len(processes))
    print(f'gantt: {gantt_chart}')
    return gantt_chart


def priority_round_robin(processes, q):
    start_time, end_time, ave_waiting_time = 0, 0, 0
    gantt_chart = {'sequence': []}
    processes_copy = sorted(list(processes), key=itemgetter('priority'))
    # start_time = processes_copy[0]['arrival']

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
        same_priority = [i for i in processes_copy if i['priority'] == processes_copy[index]['priority']]
        if len(same_priority) > 1:
            partial_gantt = round_robin(same_priority, q, start_time, end_time)
            sequence = partial_gantt['sequence']
            index += len(same_priority)
            end_time = sequence[-1]['end_time']
            start_time = end_time
            gantt_chart['sequence'] += partial_gantt['sequence']
        else:
            end_time += processes_copy[index]['burst']
            gantt_chart['sequence'].append({
                'process': processes_copy[index]['process'],
                'start_time': start_time,
                'end_time': end_time,
                'duration': processes_copy[index]['burst']
            })
            start_time = end_time
            index += 1

    gantt_chart['ave_waiting_time'] = compute_awt() / float(len(processes))
    print(f'priorr gantt: {gantt_chart}\n\n')
    return gantt_chart


def designate_algo(algo, processes, q):
    switcher = {
        'fcfs': first_come_first_serve,
        'sjf': shortest_job_first,
        'rr': round_robin,
        'prio': priority,
        'priorr': priority_round_robin,
        'srtf': shortest_time_remaining_first,
    }
    return switcher.get(algo, lambda: 'Scheduler invalid!')(processes, q)


def evaluate(data):
    algo = data['algo']
    processes = data['processes']

    processes = [{
        'process': int(i['process']),
        'burst': int(i['burst']),
        'arrival': int(i['arrival']),
        'priority': int(i['priority']),
    } for i in processes]
    q = data['quantum']
    print(f'{algo}')
    return designate_algo(algo, processes, q)


import time
import json
import csv
import multithreaded_algo
import standard_algo
import signal
import numpy as np


def measure(data, function):
    start = time.time()
    function(data)
    end = time.time()
    return end - start


def performance_eval(config, function):
    result = []
    save_results = lambda _signalNumber, _frame: export(config, result, "sigterm_backup")
    signal.signal(signal.SIGTERM, save_results)
    tests = config['test_params']
    for test in tests:
        print("Starting test range with {} dimensions".format(test['name']))
        for dim in range(test['start'], test['end'], test['step']):
            print("Testing dimension: {}".format(dim))
            vect = list(np.random.randint(low=0, high=dim, size=dim))
            elapsed_time = measure(vect, function)
            result.append([dim, elapsed_time])
    return result


def export(config, result, filename="exported"):
    # I want the same fields for all CSV files but filename is chosen at function-call time
    fields = config['fields']
    filename = "{}_{}.csv".format(filename, time.strftime("%d_%m_%Y_%H:%M:%S", time.localtime()))
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(fields)
        csv_writer.writerows(result)


def eval_and_export_results(config, function, filename):
    results = performance_eval(config, function)
    export(config, results, filename)


if __name__ == "__main__":
    with open("config.JSON", 'r') as f:
        config = json.load(f)
    eval_and_export_results(config, multithreaded_algo.mergeSort, "multi_thread_results_parallel_merge")
    eval_and_export_results(config, standard_algo.mergeSort, "single_thread_results")
    parallel_sort_serial_merge = lambda vector: multithreaded_algo.mergeSort(vector, parallel_merge=False)
    eval_and_export_results(config, parallel_sort_serial_merge, "multi_thread_results_serial_merge")

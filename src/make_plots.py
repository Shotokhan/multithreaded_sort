import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import csv
import json
import math

matplotlib.use('Agg')


def make_plots(config, data):
    for key in data.keys():
        # the time axis is the same for all but okay; other things as well could go outside the loop
        # I opted to not using logarithms at last
        # time_axis = [math.log10(float(data[key][j][0]) + 1) for j in range(len(data[key]))]
        time_axis = [float(data[key][j][0]) for j in range(len(data[key]))]
        # y_axis = [math.log10(float(data[key][j][1])) for j in range(len(data[key]))]
        y_axis = [float(data[key][j][1]) for j in range(len(data[key]))]
        plt.plot(time_axis, y_axis, label=key)
        # plt.axis([0, time_axis[-1], 0, 1000])
        plt.xlabel("{}".format(config['fields'][0]))
        plt.ylabel("{} (seconds)".format(config['fields'][1]))
        plt.legend(loc='upper left')
    # put these two inside the loop for separate plots
    plt.savefig("performance_eval_plot_{}.png".format(time.strftime("%d_%m_%Y_%H:%M:%S", time.localtime())))
    plt.close()


def read_data(multi_thread_file, single_thread_file):
    data = {}
    with open(multi_thread_file, 'r') as f:
        from_file = csv.reader(f)
        from_file = [line for line in from_file]
    from_file = from_file[1:]       # first line is header
    data["Multi-threading"] = from_file
    with open(single_thread_file, 'r') as f:
        from_file = csv.reader(f)
        from_file = [line for line in from_file]
    from_file = from_file[1:]
    data["Single-threading"] = from_file
    return data


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: {} <multi-threaded_results>.csv <single-threaded_results>.csv".format(sys.argv[0]))
    else:
        multi_threaded, single_threaded = sys.argv[1], sys.argv[2]
        with open('config.JSON', 'r') as f:
            config = json.load(f)
        data = read_data(multi_threaded, single_threaded)
        make_plots(config, data)

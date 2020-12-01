import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import csv
import json
# import math

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
    # put these two lines inside the loop for separate plots
    plt.savefig("performance_eval_plot_{}.png".format(time.strftime("%d_%m_%Y_%H:%M:%S", time.localtime())))
    plt.close()


def read_data(config, filenames):
    data = {}
    for i in range(len(filenames)):
        with open(filenames[i], 'r') as f:
            from_file = csv.reader(f)
            from_file = [line for line in from_file]
        from_file = from_file[1:]       # first line is header
        data[config["plot_names"][i]] = from_file
    return data


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: {} <multi-threaded-par-merge>.csv <single-threaded>.csv "
              "<multi-threaded-serial-merge>.csv".format(sys.argv[0]))
    else:
        files = sys.argv[1:]
        with open('config.JSON', 'r') as f:
            config = json.load(f)
        data = read_data(config, files)
        make_plots(config, data)

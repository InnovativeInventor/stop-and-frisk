import csv
import sys
import matplotlib.pyplot as plt
import numpy as np

def stats_by_group(filename, column_number_group, column_number_arrest):
    """
    race = 68
    arrest t/f = 23
    """
    stops_by_group_type = {}
    arrests_by_group_type = {}

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            group_type = row[column_number_group]

            # Checking if arrested
            if row[column_number_arrest] == "Y":
                arrest = True
            elif row[column_number_arrest] == "N":
                arrest = False
            else:
                raise ValueError("Invalid option in " + filename + ", expected Y/N, got " + row[column_number_arrest])

            # Counting race
            if group_type == "(null)":
                continue
            elif group_type not in stops_by_group_type:
                stops_by_group_type[group_type] = 1
            elif group_type in stops_by_group_type:
                stops_by_group_type[group_type] += 1
            else:
                raise ValueError("Dictionary is damaged")

            # Counting arrests
            if arrest:
                if group_type not in arrests_by_group_type:
                    arrests_by_group_type[group_type] = 1
                elif group_type in arrests_by_group_type:
                    arrests_by_group_type[group_type] += 1
                else:
                    raise ValueError("Dictionary is damaged")
    return arrests_by_group_type, stops_by_group_type

def percent_by_group(arrests, stops):
    arrests_list = []
    stops_list = []
    labels_list = []
    percent_list = []

    sorted_keys = sorted(stops, key=stops.get, reverse=True)
    
    for key in sorted_keys:
        stops_list.append(stops[key])
        if key in arrests:
            arrests_list.append(arrests[key])
        else:
            arrests_list.append(0)
        percent_list.append(100*arrests_list[-1]/stops[key])
        labels_list.append(key)
        
    return percent_list, arrests_list, stops_list, labels_list


def graph_data_race(percent_list, labels_list, location="New York", year="2017"):
    opp_percent_list = []
    for count, value in enumerate(percent_list):
        opp_percent_list.append(100-value)

    fig, ax = plt.subplots()

    index = np.arange(len(labels_list))
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(index, percent_list, bar_width,
                    alpha=opacity, color='r', 
                    error_kw=error_config,
                    label='Percents of arrests per stop')

    rects2 = ax.bar(index + bar_width, opp_percent_list, bar_width,
                    alpha=opacity, color='b',
                    error_kw=error_config,
                    label='Percent of non-arrests per stop')

    ax.set_xlabel('Race')
    ax.set_ylabel('Percent')
    ax.set_title("Percent of Arrests at Stop and Frisks in " + location + " during " + year)
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(labels_list)
    ax.legend()

    fig.tight_layout()
    plt.savefig(location + "_" + year + "_graph.png", aspect='auto')
    plt.show()
    

def graph_by_race():
    if len(sys.argv) is not 1:
        raise ValueError("You need to specify the file to read from")
        
    arrests_by_race, stops_by_race = stats_by_group(sys.argv[1], 68, 23)
    percent_list, arrests_list, stops_list, labels_list = percent_by_group(arrests_by_race, stops_by_race)

    # Debugging:
    # print(arrests_list)
    # print(stops_list)
    # print(percent_list)
    # print(labels_list)

    graph_data_race(percent_list, labels_list)

if __name__ == "__main__":
    graph_by_race()
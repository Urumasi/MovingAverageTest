#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Petr Salaba <salabapetr@email.cz>

import csv
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from MovingAverage import MovingAverage

CSV_FILENAME = 'cykloscitace.csv'
DATETIME_FORMAT = '%d.%m.%Y %H:%M'
MOVING_AVERAGE_WINDOW_SIZE = 10


def main():
    dates = []
    temps = []

    with open(CSV_FILENAME, 'r') as csv_file:
        r = csv.reader(csv_file, delimiter=',', quotechar='"')

        first_row = True
        for row in r:
            # First row contains csv table header, so we discard it
            if first_row:
                first_row = False
                continue

            dates.append(datetime.strptime(row[1], DATETIME_FORMAT))
            temps.append(int(row[5]))

    averages = list(MovingAverage(temps, MOVING_AVERAGE_WINDOW_SIZE))
    """
    Gives us points where the 2 graphs intersect by
    checking where the sign of the difference changes
    """
    intersections = np.argwhere(np.diff(
        np.sign([temps[i] - averages[i] for i in range(len(temps))]))).flatten()

    i_dates = []
    i_temps = []
    for inter in intersections:
        """
        No need for a bounds check, since intersection can't happen unless
        there's a point following this one that causes the intersection
        to take place
        """
        vt0 = temps[inter]
        vt1 = temps[inter + 1]
        slope_temp = vt1 - vt0

        va0 = averages[inter]
        va1 = averages[inter + 1]
        slope_avg = va1 - va0

        # Distance from point0 to the intersection point
        dist = abs(vt0 - va0) / abs(slope_temp - slope_avg)

        # Calculate the actual time and temperature of intersection
        time_delta = dates[inter + 1] - dates[inter]

        i_date = dates[inter] + time_delta * dist
        i_temp = vt0 + slope_temp * dist

        print("Průnik nalezen {0:%d. %m. %Y v %H:%M} o teplotě {1}°C".format(
            i_date, round(i_temp, 1)))

        i_dates.append(i_date)
        i_temps.append(i_temp)

    plt.plot(dates, temps, 'b-', dates, averages, 'g-', linewidth=1)
    plt.plot(i_dates, i_temps, 'r+', mew=2, ms=8)

    plt.ylabel('Teplota (°C)')
    plt.xlabel('Čas')
    plt.title('Průměrná templota v Chodově, Praha')
    plt.grid()

    plt.show()


if __name__ == "__main__":
    main()

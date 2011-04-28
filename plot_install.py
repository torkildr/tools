#!/usr/bin/env python

import datetime
import dateutil.rrule as rrule
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dates = []
totals = []
actives = []
versions = {}

f = open("/home/markild/stuff/trommelyd_installs.txt")
for line in f:
    data = line.split()

    if len(data) >= 3:
        try:
            date = datetime.datetime.strptime(data[0], "%d.%m.%Y")
            total = int(data[1])
            active = int(data[2])

            dates.append(date)
            totals.append(total)
            actives.append(active)

            if len(data) == 4:
                versions[dates[-1]] = data[3]
        except:
        	pass

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(dates, actives, 'b')
ax.plot(dates, totals, 'r')

# format the coords message box
def value(x):
	return '$%1.2f' % x

ax.format_ydata = value
ax.grid(True)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_minor_locator(mdates.DayLocator())

datemin = min(dates) - datetime.timedelta(days=3)
datemax = max(dates)
ax.set_xlim(datemin, datemax)

ax.set_xlabel("Date")
ax.set_ylabel("Installs")

for key, value in versions.items():
    ax.axvline(x=key, linestyle='--', color='g', label=value)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
#fig.autofmt_xdate()

plt.savefig("tempfile.png", format='png')


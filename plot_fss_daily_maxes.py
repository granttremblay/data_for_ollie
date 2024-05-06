import numpy as np
from Ska.engarchive import fetch_eng as fetch
from Ska.Matplotlib import plot_cxctime
from Chandra.Time import DateTime
import matplotlib.pyplot as plt

if 'dat' not in globals():
    dat = fetch.Msid('tfssbkt1', '1999:280', stat='daily')

# yrs = np.arange(2000, 2018)
yrs = np.arange(1999, 2023)
outs = []
outtimes = []
nsamp = 50

for yr in yrs:
    sec0 = DateTime('{}:180'.format(yr)).secs
    # sec1 = DateTime('{}:180'.format(yr + 1)).secs
    # sec1 = DateTime('{}:180'.format(yr + 1)).secs
    sec1 = DateTime('{}:060'.format(yr + 1)).secs
    i0, i1 = np.searchsorted(dat.times, [sec0, sec1])
    ivals = np.argsort(dat.maxes[i0:i1])
    vals = dat.maxes[i0:i1][ivals]
    times = dat.times[i0:i1][ivals]
    mean_val = np.mean(vals[-nsamp:])
    outs.append(mean_val)
    mean_time = np.mean(times[-nsamp:])
    outtimes.append(mean_time)
    print(f'{yr} {mean_val:.2f} {DateTime(mean_time).date}')

outs = np.array(outs)
outtimes = np.array(outtimes)

plt.close(10)
plt.figure(10)
plot_cxctime(outtimes, outs, 'o-')
plt.grid()
plt.margins(0.03)
plt.ylabel('Deg F')
# plt.title(f'Mean of highest {nsamp} max daily FSS temps per hot season')
plt.title('Peak Fine Sun Sensor temperatures each year')

ok = outtimes > DateTime('2002:180').secs

r = np.polyfit(outtimes[ok], outs[ok], 2)
linfit = np.polyval(r, outtimes)
plot_cxctime(outtimes, linfit, 'C1', lw=4, alpha=0.4)
plt.savefig('fss_hot_season_peak_fit.png')


plt.close(2)
plt.figure(2)
plot_cxctime(dat.times, dat.maxes, '-', color='C0', lw=1, alpha=0.5)
plot_cxctime(dat.times, dat.maxes, '.r', alpha=0.2)
plt.grid()
plt.title('FSS daily maxes')
plt.ylim(100, 220)
plt.ylabel('Deg F')
plt.margins(0.03)
plot_cxctime(outtimes, linfit, 'C1', lw=4, alpha=0.7)
plt.draw()
plt.show()
plt.savefig('fss_daily_maxes_fit.png')


# Make a zoom plot for 2017 - 2018 hot seasons to illustrate
# the mean of 30 maxes.
plt.close(3)
plt.figure(3)
plot_cxctime(dat.times, dat.maxes, '-', color='C0', lw=1, alpha=0.5)
plot_cxctime(dat.times, dat.maxes, '.r', alpha=0.2)
plt.grid()
plt.title('FSS daily maxes')
plt.xlim(736089, 736797)
plt.ylim(190, 215)
plt.ylabel('Deg F')
plot_cxctime(outtimes, linfit, 'C1', lw=4, alpha=0.7)
plt.draw()
plt.show()
plt.savefig('fss_daily_maxes_fit_zoom.png')

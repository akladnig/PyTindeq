import numpy as np
from enum import Enum

from src.test import TestResults


def get_rfd(x, y):
    ymax = np.max(x)
    f80 = ymax * 0.8
    f20 = ymax * 0.2
    ix = np.where(y > f80)[0]
    t80 = x[ix[0]]
    ix = np.where(y > f20)[0]
    t20 = x[ix[0]]
    f = f80 - f20
    t = t80 - t20
    return f, t, t20, t80, f20, f80


def max_strength(body_weight, max_left, max_right):
    maxx = np.array([max_right, max_left])
    max_onehand = np.mean(maxx[maxx > 0])
    kg = max_onehand * 2 - body_weight
    if kg <= 20:
        gmin = 7
        gmax = 11
    else:
        irca = (kg * 9.81 + 59.9) / 28.5
        gmin = np.round(irca) - 2
        gmax = np.round(irca) + 2
    if gmin < 1:
        gmin = 1
    if gmax > 30:
        gmax = 30
    if gmax < 1:
        gmax = 1
    if gmin > 30:
        gmin = 30

    return gmin, gmax


def critical_force(body_weight, critical_force):
    # irca = cf/bw* 100*0.3 + 6
    gmin = np.round(critical_force / body_weight * 100 * 0.25 + 6)
    gmax = np.round(critical_force / body_weight * 100 * 0.35 + 6)
    if gmin < 1:
        gmin = 1
    if gmax > 30:
        gmax = 30
    if gmax < 1:
        gmax = 1
    if gmin > 30:
        gmin = 30

    return gmin, gmax


def rfd(rfd_left, rfd_right):
    rfddd = np.array([rfd_right, rfd_left])
    rfd = np.mean(rfddd[rfddd > 0])
    # 117.8 irca - 798.3 = rfd new
    irca = (rfd * 9.81 + 798.3) / 117.8
    gmin = np.round(irca) - 1
    gmax = np.round(irca) + 1
    if gmin < 1:
        gmin = 1
    if gmax > 30:
        gmax = 30
    if gmax < 1:
        gmax = 1
    if gmin > 30:
        gmin = 30

    return gmin, gmax


def test_results():
    (max_gmax, max_gmin) = max_strength(
        TestResults.body_weight, TestResults.max_left, TestResults.max_right
    )
    (cf_gmax, cf_gmin) = critical_force(
        TestResults.body_weight, TestResults.critical_load
    )
    (rfd_gmax, rfd_gmin) = rfd(TestResults.rfd_left, TestResults.rfd_right)
    
    return max_gmax, max_gmin, cf_gmax, cf_gmin, rfd_gmax, rfd_gmin


def sigma_clipped_stats(data):
    mask = np.ones(data.shape).astype("bool")
    for i in range(5):
        mean = np.mean(data[mask])
        mask = np.fabs(data - mean) < 4 * np.std(data[mask])
    return data[mask].mean(), np.median(data[mask]), data[mask].std()


def get_edges(f, trigger_level=3):
    rising_edges = np.flatnonzero(
        np.logical_and(f[:-1] < trigger_level, f[1:] > trigger_level)
    )
    falling_edges = np.flatnonzero(
        np.logical_and(f[:-1] > trigger_level, f[1:] < trigger_level)
    )
    # check limits
    if f[0] > trigger_level:
        rising_edges = np.insert(rising_edges, 0, 0)
    return rising_edges, falling_edges


def measure_mean_loads(t, f, trigger_level=3):
    """
    Split the data into single work intervals, and calculate mean load in that interval
    """
    rising_edges, falling_edges = get_edges(f, trigger_level)
    fmeans = []
    durations = []
    fmeds = []
    tmeans = []
    errs = []
    for s, e in zip(rising_edges, falling_edges):
        if e - s < 3.5:
            continue

        elapsed = t[e] - t[s]
        time = t[s:e].mean()
        mean, med, std = sigma_clipped_stats(f[s:e])
        fmeans.append(mean)
        fmeds.append(med)
        durations.append(elapsed)
        tmeans.append(time)
        errs.append(std / np.sqrt(e - s))
    return (
        np.array(tmeans),
        np.array(durations),
        np.array(fmeans),
        np.array(fmeds),
        np.array(errs),
    )


def analyse_data(x, y, load_time, rest_time, interactive=False):
    t = np.array(x)
    f = np.array(y)
    tmeans, durations, _, fmeans, e_fmeans = measure_mean_loads(t, f)
    factor = load_time / (load_time + rest_time)
    load_asymptote = np.nanmean(fmeans[-5:-1])
    e_load_asymptote = np.nanstd(fmeans[-5:-1]) / np.sum(np.isfinite(fmeans[-5:-1]))

    critical_load = load_asymptote * factor
    e_critical_load = critical_load * (e_load_asymptote / load_asymptote)

    used_in_each_interval = (fmeans - critical_load) * durations - critical_load * (
        load_time + rest_time - durations
    )
    wprime_alt = np.sum(used_in_each_interval)
    remaining = wprime_alt - np.cumsum(used_in_each_interval)
    print("Analyse Data ", used_in_each_interval, wprime_alt, remaining)

    # force constant
    alpha = np.median((fmeans - load_asymptote) / remaining)

    msg = "<p>peak load = {:.2f} +/- {:.2f} kg</p>".format(fmeans[0], e_fmeans[0])
    msg += "<p>critical load = {:.2f} +/- {:.2f} kg</p>".format(
        critical_load, e_critical_load
    )
    msg += "<p>asymptotic load = {:.2f} +/- {:.2f} kg</p>".format(
        load_asymptote, e_load_asymptote
    )
    msg += "<p>W' = {:.0f} J</p>".format(9.8 * wprime_alt)
    msg += "<p>Anaerobic function score = {:.1f}</p>".format(wprime_alt / critical_load)

    predicted_force = load_asymptote + alpha * remaining

    TestResults.critical_load = critical_load

    return tmeans, fmeans, e_fmeans, msg, critical_load, load_asymptote, predicted_force


def analyse_cft(self):
    x = np.array(self.x)
    y = np.array(self.y)

    nlaps = (self.duration // 10) - 1

    # ix_lap= np.zeros(len(x))

    tmeans = []
    fmeans = []
    std_fmeans = []

    for n in range(nlaps):
        t1 = 10 + n * 10
        t2 = 10 + n * 10 + 7
        ix = (x >= t1) & (x <= t2) & (y > 3)
        # ix_lap[ix]=n+1

        tmeans.append(np.mean(x[ix]))
        fmeans.append(np.median(y[ix]))
        iqr = np.percentile(y[ix], 75) - np.percentile(y[ix], 25)
        std_fmeans.append(iqr / 2)
        # print([t1,t2])

    tmeans = np.array(tmeans)
    fmeans = np.array(fmeans)
    std_fmeans = np.array(std_fmeans)
    # breakpoint()

    self.cf_peak_load = np.max(fmeans)
    imax = np.argmax(fmeans)

    self.cf_critical_load = np.nanmean(fmeans[-5:-1])
    std_load_asymptote = np.nanstd(fmeans[-5:-1])
    self.cf_x = x
    self.cf_y = y

    msg = "<p>Peak force = {:.2f} +/- {:.2f} kg</p>".format(
        fmeans[imax], std_fmeans[imax]
    )
    msg += "<p>Critical force = {:.2f} +/- {:.2f} kg</p>".format(
        self.cf_critical_load, std_load_asymptote
    )
    msg += "<p>Critical force = {:.2f} % of peak force</p>".format(
        100 * self.cf_critical_load / fmeans[imax]
    )
    self.results_div.text = msg

    self.fig.circle(tmeans, fmeans, color="red", size=20, line_alpha=0)

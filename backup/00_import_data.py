import os
import glob

import matplotlib.pyplot as plt

import mne

from mne_nirs.preprocessing import peak_power, scalp_coupling_index_windowed
from mne_nirs.visualisation import plot_timechannel_quality_metric

# %%
# set-up file naming pattern
pattern = os.path.join(
    '../data_hc', '**', '*.nirs'
)

# %%
# look got available files
files = glob.glob(pattern)
files.sort()

# %%
for file in files:

    # import the data
    fdir = os.path.dirname(file)
    raw_data = mne.io.read_raw_nirx(fdir)
    sfreq = raw_data.info['sfreq']

    # %%
    # get events
    events, event_ids = mne.events_from_annotations(
        raw_data,
        event_id={
            "0.0": 0,
            "1.0": 1,
            "2.0": 2,
            "3.0": 3,
            "4.0": 4,
            "5.0": 5
        }
    )

    event_dict = {
        "Resting State": 0,
        "Sham": 1,
        "2 Hz": 2,
        "10 Hz": 3,
        "25 Hz": 4,
        "40 Hz": 5,
    }

    fig, ax = plt.subplots(figsize=(8, 6))
    mne.viz.plot_events(events,
                        event_id=event_dict,
                        sfreq=raw_data.info['sfreq'],
                        axes=ax,
                        show=False)
    ax.set_xlim(-250, raw_data.times[-1]+250)
    ax.set_title(os.path.dirname(file).split('/')[-1] + ' - ' + os.path.basename(file))
    fig.savefig('results/' + os.path.dirname(file).split('/')[-1].split(',')[0] + '_trigger.png')

    # %%
    raw_od = mne.preprocessing.nirs.optical_density(raw_data)

    tmin, tmax = events[1, 0] / sfreq, (events[1, 0] / sfreq) + 360
    raw_sig = raw_od.copy().crop(tmin, tmax)
    sci = mne.preprocessing.nirs.scalp_coupling_index(raw_sig)
    fig, ax = plt.subplots(layout="constrained")
    ax.hist(sci)
    ax.set(xlabel="Scalp Coupling Index", ylabel="Count", xlim=[0, 1])
    ax.set_title(os.path.dirname(file).split('/')[-1] + ' - ' + os.path.basename(file))
    fig.savefig('results/' + os.path.dirname(file).split('/')[-1].split(',')[0] + '_sci.png')

    _, scores, times = scalp_coupling_index_windowed(raw_od, time_window=60)
    fig = plot_timechannel_quality_metric(raw_od, scores, times, threshold=0.5,
                                          title="Scalp Coupling Index "
                                          "Quality Evaluation")
    fig.set_size_inches(30, 25)
    fig.savefig('results/' + os.path.dirname(file).split('/')[-1].split(',')[0] + '_metric.png')
    plt.close('all')

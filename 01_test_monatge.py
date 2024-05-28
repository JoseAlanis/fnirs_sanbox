import os
import glob

import matplotlib.pyplot as plt

import mne

# %%
# set-up file naming pattern
pattern = os.path.join(
    'data_hc', '**', '*.nirs'
)

# %%
# look got available files
files = glob.glob(pattern)
files.sort()

# import the data
fdir = os.path.dirname(files[0])
raw_data = mne.io.read_raw_nirx(fdir)
sfreq = raw_data.info['sfreq']

#%%
# Download anatomical locations
subjects_dir = str(mne.datasets.sample.data_path()) + '/subjects'
mne.datasets.fetch_hcp_mmp_parcellation(subjects_dir=subjects_dir, accept=True)
labels = mne.read_labels_from_annot('fsaverage', 'HCPMMP1', 'lh', subjects_dir=subjects_dir)
labels_combined = mne.read_labels_from_annot('fsaverage', 'HCPMMP1_combined', 'lh', subjects_dir=subjects_dir)

# %%
brain = mne.viz.Brain('fsaverage', subjects_dir=subjects_dir, background='w', cortex='0.5')
brain.add_sensors(raw.info, trans='fsaverage', fnirs=['channels', 'pairs', 'sources', 'detectors'])
brain.show_view(azimuth=180, elevation=80, distance=450)
import os
import glob

import matplotlib.pyplot as plt

import numpy as np

import mne
import mne_nirs
import mne_bids

from mne_nirs.io.fold import fold_landmark_specificity

# %%
src_det_names = dict(S1='AF7', S2='Fpz', S3='AF8', S4='AF3', S5='AF4',
                     S6='F3',
                     S7='Fz',
                     S8='F4',
                     S9='FC1',
                     S10='FC5',
                     S11='FT9',
                     S12='C3',
                     S13='T7',
                     S14='CP5',
                     S15='TP9',
                     S16='P7',
                     S17='FC2',
                     S18='FC6',
                     S19='FT10',
                     S20='C4',
                     S21='T8',
                     S22='CP6',
                     S23='TP10',
                     S24='P8',
                     S25='CP1',
                     S26='CP2',
                     S27='Pz',
                     S28='P3',
                     S29='P4',
                     S30='POz',
                     S31='O1',
                     S32='O2',

                     D1='Fp1',
                     D2='Fp2',
                     D3='AFz',
                     D4='F1',
                     D5='F2',
                     D6='FCz',
                     D7='C1',
                     D8='C2',
                     D9='FC3',
                     D10='FT7',
                     D11='F9',
                     D12='P5',
                     D13='TP7',
                     D14='P5',
                     D15='P9',
                     D16='PO7',
                     D17='FC4',
                     D18='FT8',
                     D19='F10',
                     D20='C6',
                     D21='TP8',
                     D22='P6',
                     D23='P10',
                     D24='PO8',
                     D25='CPz',
                     D26='P1',
                     D27='P2',
                     D28='PO3',
                     D29='PO4',
                     D30='Oz')

# %%
root = mne_nirs.datasets.audio_or_visual_speech.data_path()
dataset = mne_bids.BIDSPath(root=root, suffix="nirs", extension=".snirf", subject="04",
                            task="AudioVisualBroadVsRestricted", datatype="nirs", session="01")
raw = mne.io.read_raw_snirf(dataset.fpath)

# %%
# set-up file naming pattern
pattern = os.path.join(
    'data_hc', '**', '*.snirf'
)

# %%
# look got available files
files = glob.glob(pattern)
files.sort()

# import the data
fdir = files[0]
raw_data = mne.io.read_raw_snirf(fdir)
sfreq = raw_data.info['sfreq']

#%%
# Download anatomical locations
subjects_dir = mne.datasets.fetch_fsaverage()
subjects_dir = os.path.dirname(subjects_dir)
mne.datasets.fetch_hcp_mmp_parcellation(
    subjects_dir=subjects_dir,
    accept=True
)
labels = mne.read_labels_from_annot(
    'fsaverage',
    'HCPMMP1',
    'lh',
    subjects_dir=subjects_dir
)
labels_combined = mne.read_labels_from_annot(
    'fsaverage',
    'HCPMMP1_combined',
    'lh',
    subjects_dir=subjects_dir
)

# set-up file naming pattern
pattern = os.path.join(
    'data_hc', '**', '*.nirs'
)

# %%
# look got available files
files = glob.glob(pattern)
files.sort()

fdir = os.path.dirname(files[0])
raw_data = mne.io.read_raw_nirx(fdir)
sfreq = raw_data.info['sfreq']

# %%
brain = mne.viz.Brain(
    'fsaverage',
    subjects_dir=subjects_dir,
    background='w',
    cortex='0.5')

brain.add_sensors(
    raw.info,
    trans='fsaverage',
    fnirs=['channels', 'pairs', 'sources', 'detectors']
)

# %%
brain.show_view(azimuth=180, elevation=80, distance=450)

view_map = {
    'left-lat': np.array([1, 4]),
    'parietal': np.array([27, 30]),
    'right-lat': np.array([3, 5]),
}

# %%
fig_montage = mne_nirs.visualisation.plot_3d_montage(
    raw_data.info, src_det_names=src_det_names, view_map=view_map, subjects_dir=subjects_dir)

# Return specificity of each channel to the Left IFG
specificity = fold_landmark_specificity(raw_data, 'L IFG (p. Triangularis)')

# Retain only channels with specificity to left IFG of greater than 50%
raw_IFG = raw_data.copy().pick(picks=np.where(specificity > 50)[0])

brain = mne.viz.Brain('fsaverage', subjects_dir=subjects_dir, background='w', cortex='0.5')
brain.add_sensors(raw_IFG.info, trans='fsaverage', fnirs=['channels', 'pairs'])

ifg_label = [label for label in labels_combined if label.name == 'Inferior Frontal Cortex-lh'][0]
brain.add_label(ifg_label, borders=False, color='green')

brain.show_view(azimuth=140, elevation=95, distance=360)

import os.path as op

import matplotlib.pyplot as plt
import numpy as np

# Custom modules for loading and plotting
from circular import plot_connectivity_circle
from utils import load_mat_file, load_labels_from_mat, add_occurrence_suffix, get_category_order, shift_list
from config import DATA_PATH

# %%

# Load probe structure labeling file
fname_info_channel_depth = op.join(DATA_PATH, 'Depth_Label.mat')

# Load depth labels from the file
depth_labels = load_labels_from_mat(fname_info_channel_depth, 'Labels_1N')

# Process labels to add suffixes for occurrences
output_list = add_occurrence_suffix(depth_labels[:, 1])

# %%
# Load result matrices for healthy controls (HC) and major depressive disorder (MDD)
fname_mat_hc = op.join(DATA_PATH, 'RSFC_GoodCH_AllSub_HC_Window5s_SCI.mat')
fname_mat_mdd = op.join(DATA_PATH, 'RSFC_GoodCH_AllSub_MDD_Window5s_SCI.mat')

# Extract 'R6' data from loaded matrices
r6_mat_hc = load_mat_file(fname_mat_hc, 'R6')
r6_mat_mdd = load_mat_file(fname_mat_mdd, 'R6')

# Compute mean connectivity matrices across subjects for different conditions in HC
hc_rs0 = np.nanmean(r6_mat_hc[:, 0, :, :], axis=0)
hc_sham = np.nanmean(r6_mat_hc[:, 1, :, :], axis=0)
hc_2hz = np.nanmean(r6_mat_hc[:, 2, :, :], axis=0)
hc_10hz = np.nanmean(r6_mat_hc[:, 3, :, :], axis=0)
hc_25hz = np.nanmean(r6_mat_hc[:, 4, :, :], axis=0)
hc_40hz = np.nanmean(r6_mat_hc[:, 5, :, :], axis=0)
hc_rs1 = np.nanmean(r6_mat_hc[:, 6, :, :], axis=0)

# Compute mean connectivity matrices across subjects for different conditions in MDD
mdd_rs0 = np.nanmean(r6_mat_mdd[:, 0, :, :], axis=0)
mdd_sham = np.nanmean(r6_mat_mdd[:, 1, :, :], axis=0)
mdd_2hz = np.nanmean(r6_mat_mdd[:, 2, :, :], axis=0)
mdd_10hz = np.nanmean(r6_mat_mdd[:, 3, :, :], axis=0)
mdd_25hz = np.nanmean(r6_mat_mdd[:, 4, :, :], axis=0)
mdd_40hz = np.nanmean(r6_mat_mdd[:, 5, :, :], axis=0)
mdd_rs1 = np.nanmean(r6_mat_mdd[:, 6, :, :], axis=0)

# %%
# Plot connectivity matrix

# Compute difference between rs1 and sham for both groups
subject = r6_mat_mdd[4, 4, :, :] - r6_mat_mdd[4, 1, :, :]
subject[np.isnan(subject)] = 0

# Calculate group-level difference in connectivity between MDD and HC
mat_mdd = mdd_rs1 - mdd_sham
mat_hc = hc_rs1 - hc_sham
mat = mat_mdd - mat_hc

# %%

# Define category order for brain regions
category_order = ['cerebelum', 'occipital', 'lingual', 'temporal', 'supramarginal',
                  'calcarine', 'parietal', 'precuneus', 'postcentral', 'motor', 'precentral', 'frontal']

# Identify indices of right and left hemispheric labels
r_indices = [i for i, item in enumerate(output_list) if '_R_' in item]
l_indices = [i for i, item in enumerate(output_list) if '_L_' in item]

# Sort indices by category, grouping similar names together
r_indices_sorted = sorted(r_indices, key=lambda x: (get_category_order(output_list[x], category_order), output_list[x].split('_1')[0]))
l_indices_sorted = sorted(l_indices, key=lambda x: (get_category_order(output_list[x], category_order, -1), output_list[x].split('_1')[0]))

# Combine left and right indices for symmetric display
combined_indices = l_indices_sorted + r_indices_sorted

# Reorder connectivity matrix based on sorted indices
reordered_matrix = mat[np.ix_(combined_indices, combined_indices)]

# Define the shift amount
shift_amount = +23  # Negative for left shift
# Perform the column shift
shifted_matrix = np.roll(reordered_matrix, shift_amount, axis=1)
# Perform the row shift (to maintain correspondence with shifted columns)
shifted_matrix = np.roll(shifted_matrix, shift_amount, axis=0)

# Generate node names and colors based on brain regions
node_names = [output_list[i] for i in combined_indices]
node_names = shift_list(node_names, shift_amount)
base_names = ['_'.join(name.split('_')[:-2]) for name in node_names]
unique_base_names = sorted(set(base_names))

# Assign colors to each brain region category
color_map = plt.cm.get_cmap('tab20', len(unique_base_names))  # Using tab20 colormap
colors = {base_name: color_map(i) for i, base_name in enumerate(unique_base_names)}

# Map each node to its respective color
node_colors = [colors[base_name] for base_name in base_names]

# Print mapping of node names to colors (for debugging purposes)
for base_name, color in colors.items():
    print(f"{base_name}: {color}")

# Create a circular connectivity plot
fig, ax = plt.subplots(figsize=(10, 10), facecolor="white", subplot_kw=dict(polar=True))
plot_connectivity_circle(shifted_matrix,
                         node_names=node_names,
                         node_colors=node_colors,
                         colorbar_pos=(0.5, 1.5),
                         colormap='RdBu_r',
                         vmin=-0.25, vmax=0.25,
                         facecolor='white',
                         textcolor='black',
                         ax=ax)

# Save and display the plot
fig.savefig('/home/josealanis/Documents/projects/fnirs_sandbox/results/mdd-hc_10hz_effect.png', dpi=300)
plt.show()

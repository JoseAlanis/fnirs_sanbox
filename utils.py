import numpy as np

from scipy.io import loadmat

def load_mat_file(filepath, key):
    """
    Load a specific matrix from a MATLAB .mat file.

    Parameters:
    ----------
    filepath : str
        The path to the .mat file.
    key : str
        The key of the data matrix to extract from the .mat file.

    Returns:
    -------
    numpy.ndarray
        The matrix associated with the specified key.
    """
    try:
        mat_data = loadmat(filepath)
        if key in mat_data:
            return mat_data[key]
        else:
            raise KeyError(f"The key '{key}' was not found in the .mat file.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filepath}' was not found.")


def load_labels_from_mat(filepath, key):
    """
    Load and extract labels from a MATLAB .mat file, converting them into a 2D array.
    The first dimension indexes each label (starting from 1), and the second dimension contains the label strings.

    Parameters:
    ----------
    filepath : str
        The path to the .mat file.
    key : str
        The key of the label data to extract from the .mat file.

    Returns:
    -------
    numpy.ndarray
        A 2D array where the first column is an index (starting at 1) and the second column contains the labels as strings.

    Raises:
    ------
    KeyError
        If the specified key is not found in the .mat file.
    FileNotFoundError
        If the specified file is not found.
    """
    try:
        mat_data = loadmat(filepath)
        if key in mat_data:
            mat_shape = mat_data[key].shape
            output = np.empty(mat_shape, dtype='object')

            # Loop through rows and columns to unpack each item
            for row in range(mat_shape[0]):
                unpacked_list = [str(item[0]) if isinstance(item, np.ndarray) else str(item)
                                 for item in mat_data[key][row, :]]
                output[row, :] = unpacked_list

            # Create a 2D array with indices and labels
            indexed_labels = np.column_stack((np.arange(1, len(output) + 1), output))
            return indexed_labels
        else:
            raise KeyError(f"The key '{key}' was not found in the .mat file.")
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{filepath}' was not found.")


def add_occurrence_suffix(labels):
    """
    Append occurrence-based suffixes to each label in the list to handle duplicate items.
    Each unique item receives a suffix in the format "_n", where n is its occurrence count.

    Parameters:
    ----------
    labels : list of str
        A list of label strings, potentially containing duplicates.

    Returns:
    -------
    list of str
        A list of labels where duplicate items are suffixed with an occurrence count.

    Example:
    --------
    >>> labels = ["A", "B", "A", "A", "B"]
    >>> add_occurrence_suffix(labels)
    ["A_1", "B_1", "A_2", "A_3", "B_2"]
    """
    # Dictionary to keep track of occurrences
    occurrence_count = {}

    # Create the modified list
    output_list = []
    for item in labels:
        # Update occurrence count
        if item not in occurrence_count:
            occurrence_count[item] = 1
        else:
            occurrence_count[item] += 1
        # Append the item with its occurrence index as a suffix
        output_list.append(f"{item}_{occurrence_count[item]}")

    return output_list


# Helper function to extract the category for sorting
def get_category_order(item, categories, order = 1):
    item_lower = item.lower()
    if order == -1:
        categories = categories[::-1]

    for i, category in enumerate(categories):
        if category in item_lower:
            return i
    return len(categories)  # If not found, place at the end
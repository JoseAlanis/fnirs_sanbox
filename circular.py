from mne.viz.utils import mne_analyze_colormap, plt_show


def _get_cmap(colormap, lut=None):
    """
    Retrieve a colormap object based on the provided colormap name or object, with optional
    resampling to a specified number of colors.
    """
    from matplotlib import colors, rcParams

    try:
        from matplotlib import colormaps
    except Exception:
        from matplotlib.cm import get_cmap
    else:

        def get_cmap(cmap):
            return colormaps[cmap]

    if colormap is None:
        colormap = rcParams["image.cmap"]
    if isinstance(colormap, str) and colormap in ("mne", "mne_analyze"):
        colormap = mne_analyze_colormap([0, 1, 2], format="matplotlib")
    elif not isinstance(colormap, colors.Colormap):
        colormap = get_cmap(colormap)
    if lut is not None:
        colormap = colormap.resampled(lut)
    return colormap


def plot_connectivity_circle(
        con,
        node_names,
        indices=None,
        n_lines=None,
        node_angles=None,
        node_width=None,
        node_height=1.0,
        node_colors=None,
        facecolor="black",
        textcolor="white",
        node_edgecolor="black",
        linewidth=1.5,
        colormap="hot",
        vmin=None,
        vmax=None,
        colorbar=True,
        title=None,
        colorbar_size=0.2,
        colorbar_pos=(-0.3, 0.1),
        fontsize_title=12,
        fontsize_names=8,
        fontsize_colorbar=8,
        padding=6.0,
        ax=None,
        fig=None,
        subplot=None,
        interactive=True,
        node_linewidth=2.0,
        show=True,
):
    """Visualize connectivity as a circular graph.

    Parameters
    ----------
    con : array | Connectivity
        Connectivity scores. Can be a square matrix, or a 1D array. If a 1D
        array is provided, "indices" has to be used to define the connection
        indices.
    node_names : list of str
        Node names. The order corresponds to the order in con.
    indices : tuple of array | None
        Two arrays with indices of connections for which the connections
        strengths are defined in con. Only needed if con is a 1D array.
    n_lines : int | None
        If not None, only the n_lines strongest connections (strength=abs(con))
        are drawn.
    node_angles : array, shape (n_node_names,) | None
        Array with node positions in degrees. If None, the nodes are equally
        spaced on the circle. See mne.viz.circular_layout.
    node_width : float | None
        Width of each node in degrees. If None, the minimum angle between any
        two nodes is used as the width.
    node_height : float
        The relative height of the colored bar labeling each node. Default 1.0
        is the standard height.
    node_colors : list of tuple | list of str
        List with the color to use for each node. If fewer colors than nodes
        are provided, the colors will be repeated. Any color supported by
        matplotlib can be used, e.g., RGBA tuples, named colors.
    facecolor : str
        Color to use for background. See matplotlib.colors.
    textcolor : str
        Color to use for text. See matplotlib.colors.
    node_edgecolor : str
        Color to use for lines around nodes. See matplotlib.colors.
    linewidth : float
        Line width to use for connections.
    colormap : str | instance of matplotlib.colors.LinearSegmentedColormap
        Colormap to use for coloring the connections.
    vmin : float | None
        Minimum value for colormap. If None, it is determined automatically.
    vmax : float | None
        Maximum value for colormap. If None, it is determined automatically.
    colorbar : bool
        Display a colorbar or not.
    title : str
        The figure title.
    colorbar_size : float
        Size of the colorbar.
    colorbar_pos : tuple, shape (2,)
        Position of the colorbar.
    fontsize_title : int
        Font size to use for title.
    fontsize_names : int
        Font size to use for node names.
    fontsize_colorbar : int
        Font size to use for colorbar.
    padding : float
        Space to add around figure to accommodate long labels.
    ax : instance of matplotlib PolarAxes | None
        The axes to use to plot the connectivity circle.
    fig : None | instance of matplotlib.figure.Figure
        The figure to use. If None, a new figure with the specified background
        color will be created.

        Deprecated: will be removed in version 0.5.

    subplot : int | tuple, shape (3,)
        Location of the subplot when creating figures with multiple plots. E.g.
        121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See
        matplotlib.pyplot.subplot.

        Deprecated: will be removed in version 0.5.

    interactive : bool
        When enabled, left-click on a node to show only connections to that
        node. Right-click shows all connections.
    node_linewidth : float
        Line with for nodes.
    show : bool
        Show figure if True.

    Returns
    -------
    fig : instance of matplotlib.figure.Figure
        The figure handle.
    ax : instance of matplotlib.projections.polar.PolarAxes
        The subplot handle.

    Notes
    -----
    This code is based on a circle graph example by Nicolas P. Rougier

    By default, :func:`matplotlib.pyplot.savefig` does not take ``facecolor``
    into account when saving, even if set when a figure is generated. This
    can be addressed via, e.g.::

    >>> fig.savefig(fname_fig, facecolor='black') # doctest:+SKIP

    If ``facecolor`` is not set via :func:`matplotlib.pyplot.savefig`, the
    figure labels, title, and legend may be cut off in the output figure.
    """
    import matplotlib.pyplot as plt

    from mne_connectivity.base import BaseConnectivity

    if isinstance(con, BaseConnectivity):
        con = con.get_data()

    if fig is not None or subplot is not None:
        if ax is None:  # don't overwrite ax if passed
            if fig is None:
                fig = plt.figure(figsize=(8, 8), facecolor=facecolor)
            if not isinstance(subplot, tuple):
                subplot = (subplot,)
            ax = plt.subplot(*subplot, polar=True)

    return _plot_connectivity_circle(
        con=con,
        node_names=node_names,
        indices=indices,
        n_lines=n_lines,
        node_angles=node_angles,
        node_width=node_width,
        node_height=node_height,
        node_colors=node_colors,
        facecolor=facecolor,
        textcolor=textcolor,
        node_edgecolor=node_edgecolor,
        linewidth=linewidth,
        colormap=colormap,
        vmin=vmin,
        vmax=vmax,
        colorbar=colorbar,
        title=title,
        colorbar_size=colorbar_size,
        colorbar_pos=colorbar_pos,
        fontsize_title=fontsize_title,
        fontsize_names=fontsize_names,
        fontsize_colorbar=fontsize_colorbar,
        padding=padding,
        ax=ax,
        node_linewidth=node_linewidth,
        show=show,
    )


def _plot_connectivity_circle(
        con,
        node_names,
        indices=None,
        n_lines=None,
        node_angles=None,
        node_width=None,
        node_height=None,
        node_colors=None,
        facecolor="black",
        textcolor="white",
        node_edgecolor="black",
        linewidth=1.5,
        colormap="hot",
        vmin=None,
        vmax=None,
        colorbar=True,
        title=None,
        colorbar_size=None,
        colorbar_pos=None,
        fontsize_title=12,
        fontsize_names=8,
        fontsize_colorbar=8,
        padding=6.0,
        ax=None,
        node_linewidth=2.0,
        show=True,
):
    from itertools import cycle

    import numpy as np

    import matplotlib.patches as m_patches
    import matplotlib.path as m_path
    import matplotlib.pyplot as plt
    from matplotlib.projections.polar import PolarAxes

    if not isinstance(ax, (type(None), PolarAxes)):
        raise TypeError('Provide polar Axes')

    n_nodes = len(node_names)

    if node_angles is not None:
        if len(node_angles) != n_nodes:
            raise ValueError("node_angles has to be the same length as node_names")
        # convert it to radians
        node_angles = node_angles * np.pi / 180
    else:
        # uniform layout on unit circle
        node_angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)

    if node_width is None:
        # widths correspond to the minimum angle between two nodes
        dist_mat = node_angles[None, :] - node_angles[:, None]
        dist_mat[np.diag_indices(n_nodes)] = 1e9
        node_width = np.min(np.abs(dist_mat))
    else:
        node_width = node_width * np.pi / 180

    if node_height is None:
        node_height = 1.0

    if node_colors is not None:
        if len(node_colors) < n_nodes:
            node_colors = cycle(node_colors)
    else:
        # assign colors using colormap
        try:
            spectral = plt.cm.spectral
        except AttributeError:
            spectral = plt.cm.Spectral
        node_colors = [spectral(i / float(n_nodes)) for i in range(n_nodes)]

    # handle 1D and 2D connectivity information
    if con.ndim == 1:
        if indices is None:
            raise ValueError("indices has to be provided if con.ndim == 1")
    elif con.ndim == 2:
        if con.shape[0] != n_nodes or con.shape[1] != n_nodes:
            raise ValueError("con has to be 1D or a square matrix")
        # we use the lower-triangular part
        indices = np.tril_indices(n_nodes, -1)
        con = con[indices]
    else:
        raise ValueError("con has to be 1D or a square matrix")

    # get the colormap
    colormap = _get_cmap(colormap)

    # Use a polar axes
    if ax is None:
        fig = plt.figure(figsize=(8, 8), facecolor=facecolor, layout="constrained")
        ax = fig.add_subplot(polar=True)
    else:
        fig = ax.figure
    ax.set_facecolor(facecolor)

    # No ticks, we'll put our own
    ax.set_xticks([])
    ax.set_yticks([])

    # Set y axes limit, add additional space if requested
    ax.set_ylim(0, 10 + padding)

    # Remove the black axes border which may obscure the labels
    ax.spines["polar"].set_visible(False)

    # Draw lines between connected nodes, only draw the strongest connections
    if n_lines is not None and len(con) > n_lines:
        con_thresh = np.sort(np.abs(con).ravel())[-n_lines]
    else:
        con_thresh = 0.0

    # get the connections which we are drawing and sort by connection strength
    # this will allow us to draw the strongest connections first
    con_abs = np.abs(con)
    con_draw_idx = np.where(con_abs >= con_thresh)[0]

    con = con[con_draw_idx]
    con_abs = con_abs[con_draw_idx]
    indices = [ind[con_draw_idx] for ind in indices]

    # now sort them
    sort_idx = np.argsort(con_abs)
    del con_abs
    con = con[sort_idx]
    indices = [ind[sort_idx] for ind in indices]

    # Get vmin vmax for color scaling
    if vmin is None:
        vmin = np.min(con[np.abs(con) >= con_thresh])
    if vmax is None:
        vmax = np.max(con)
    vrange = vmax - vmin

    # We want to add some "noise" to the start and end position of the
    # edges: We modulate the noise with the number of connections of the
    # node and the connection strength, such that the strongest connections
    # are closer to the node center
    nodes_n_con = np.zeros((n_nodes), dtype=np.int64)
    for i, j in zip(indices[0], indices[1]):
        nodes_n_con[i] += 1
        nodes_n_con[j] += 1

    # initialize random number generator so plot is reproducible
    rng = np.random.mtrand.RandomState(0)

    n_con = len(indices[0])
    noise_max = 0.25 * node_width
    start_noise = rng.uniform(-noise_max, noise_max, n_con)
    end_noise = rng.uniform(-noise_max, noise_max, n_con)

    nodes_n_con_seen = np.zeros_like(nodes_n_con)
    for i, (start, end) in enumerate(zip(indices[0], indices[1])):
        nodes_n_con_seen[start] += 1
        nodes_n_con_seen[end] += 1

        start_noise[i] *= (nodes_n_con[start] - nodes_n_con_seen[start]) / float(
            nodes_n_con[start]
        )
        end_noise[i] *= (nodes_n_con[end] - nodes_n_con_seen[end]) / float(
            nodes_n_con[end]
        )

    # scale connectivity for colormap (vmin<=>0, vmax<=>1)
    con_val_scaled = (con - vmin) / vrange

    # Finally, we draw the connections
    for pos, (i, j) in enumerate(zip(indices[0], indices[1])):
        # Start point
        t0, r0 = node_angles[i], 10

        # End point
        t1, r1 = node_angles[j], 10

        # Some noise in start and end point
        t0 += start_noise[pos]
        t1 += end_noise[pos]

        verts = [(t0, r0), (t0, 5), (t1, 5), (t1, r1)]
        codes = [
            m_path.Path.MOVETO,
            m_path.Path.CURVE4,
            m_path.Path.CURVE4,
            m_path.Path.LINETO,
        ]
        path = m_path.Path(verts, codes)

        color = colormap(con_val_scaled[pos])

        # Actual line
        patch = m_patches.PathPatch(
            path, fill=False, edgecolor=color, linewidth=linewidth, alpha=1.0
        )
        ax.add_patch(patch)

    # Draw ring with colored nodes
    height = np.ones(n_nodes) * node_height
    bars = ax.bar(
        node_angles,
        height,
        width=node_width,
        bottom=9,
        edgecolor=node_edgecolor,
        lw=node_linewidth,
        facecolor=".9",
        align="center",
    )

    for bar, color in zip(bars, node_colors):
        bar.set_facecolor(color)

    # Draw node labels
    angles_deg = 180 * node_angles / np.pi
    for name, angle_rad, angle_deg in zip(node_names, node_angles, angles_deg):
        # if angle_deg >= 180:
        if '_R_' in name:
            ha = "left"
        else:
            # Flip the label, so text is always upright
            angle_deg += 180
            ha = "right"

        ax.text(
            angle_rad,
            9.4 + node_height,
            name,
            size=fontsize_names,
            rotation=angle_deg,
            rotation_mode="anchor",
            horizontalalignment=ha,
            verticalalignment="center",
            color=textcolor,
            )

    if title is not None:
        ax.set_title(title, color=textcolor, fontsize=fontsize_title)

    if colorbar:
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin, vmax))
        sm.set_array(np.linspace(vmin, vmax))
        colorbar_kwargs = dict()
        if colorbar_size is not None:
            colorbar_kwargs.update(shrink=colorbar_size)
        if colorbar_pos is not None:
            colorbar_kwargs.update(anchor=colorbar_pos)
        cb = fig.colorbar(sm, ax=ax, orientation='horizontal', **colorbar_kwargs)
        cb_yticks = plt.getp(cb.ax.axes, "yticklabels")
        cb.ax.tick_params(labelsize=fontsize_colorbar)
        plt.setp(cb_yticks, color=textcolor)

    plt_show(show)
    return fig, ax

from matplotlib.patches import Rectangle
from matplotlib.figure import Figure
from matplotlib.colors import to_rgb
from matplotlib.projections.polar import PolarAxes
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike

MPL_BLUE = "#11557c"


def create_axes(
    fig: Figure,
    ax_position: tuple[float, float, float, float],
    lw_bars: float,
    lw_grid: float,
    lw_border: float,
    rgrid: ArrayLike,
    data: dict[str, float],
    colors: dict[str, str],
) -> PolarAxes:
    """
    Create a polar Axes containing the matplotlib radar plot.

    ax_positions - the position of the created axes in figure coordinates as (x, y, width, hight)
    lw - line width
    rgrid - positions of the radial grid.

    returns - the created Axes.
    """

    data_size = len(data)

    with plt.rc_context({"axes.edgecolor": MPL_BLUE, "axes.linewidth": lw_border}):
        ax = PolarAxes(fig, ax_position)
        fig.add_axes(ax)
        ax.set_axisbelow(True)

        arc = 2.0 * np.pi
        theta = np.arange(0.0, arc, arc / data_size)
        radii = np.array([v * 10 for v in data.values()])
        width = arc / data_size

        radii_full = np.array([10] * data_size)

        for i, (k, v) in enumerate(data.items()):
            ax.text(
                theta[i] + width / 2,
                # radii[i],
                11,
                f"{k}\n{v:.2f}",
                ha="center",
                va="center",
                fontsize=8,
            )

        bars = ax.bar(
            theta,
            radii_full,
            width=width,
            bottom=0.0,
            align="edge",
            edgecolor="0.3",
            facecolor=list(colors.values()),
            alpha=0.1,
            lw=lw_bars,
        )

        bars = ax.bar(
            theta,
            radii,
            width=width,
            bottom=0.0,
            align="edge",
            edgecolor="0.3",
            facecolor=list(colors.values()),
            lw=lw_bars,
        )

        for bar in bars:
            pass

        ax.tick_params(
            labelbottom=False, labeltop=False, labelleft=False, labelright=False
        )

        ax.grid(lw=lw_grid, color="0.9")
        ax.set_rmax(10)
        ax.set_yticks(rgrid)

        # the actual visible background - extends a bit beyond the axis
        ax.add_patch(
            Rectangle(
                (0, 0),
                arc,
                10,
                facecolor="white",
                zorder=0,
                clip_on=False,
                in_layout=False,
            )
        )

        return ax


def render_polar_area_chart(
    indicator_name: str,
    height_px: int,
    data: dict[str, float],
    colors: dict[str, str],
):
    # -> tuple[plt.Figure, plt.Axes]:

    lw_bars = 0.7
    lw_grid = 0.5
    lw_border = 1
    rgrid = range(10)

    dpi = 100
    height = height_px / dpi
    figsize = (height, height)

    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0)

    ax_pos = (0.03, 0.03, 0.84, 0.84)
    ax = create_axes(
        fig,
        ax_pos,
        lw_bars,
        lw_grid,
        lw_border,
        rgrid,
        data,
        colors,
    )

    ax.set_title(f"Affective State for {indicator_name}", y=1.08)

    plt.show()
    # return fig, ax


def render_radar_chart(
    indicator_name: str,
    height_px: int,
    data: dict[str, float],
    colors: dict[str, str],
):

    data_size = len(data)
    categories = list(data.keys())
    values = [v * 10 for v in data.values()]

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, data_size, endpoint=False).tolist()

    # Complete the loop by appending the first value to the end
    values += values[:1]
    angles += angles[:1]

    dpi = 100
    height = height_px / dpi
    figsize = (height, height)

    # Create the plot
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi, subplot_kw=dict(polar=True))

    # Turn off the circular grid and spine
    ax.grid(False)
    ax.spines["polar"].set_visible(False)

    # Draw polygonal grid lines manually
    grid_levels = [2, 4, 6, 8, 10]
    for level in grid_levels:
        grid_angles = angles.copy()
        grid_values = [level] * len(grid_angles)
        ax.plot(grid_angles, grid_values, "k-", linewidth=0.5, alpha=0.3, zorder=0)

    # Draw the outer polygonal border
    outer_border_angles = angles.copy()
    outer_border_values = [10] * len(outer_border_angles)
    ax.plot(
        outer_border_angles, outer_border_values, "k-", linewidth=1, alpha=0.8, zorder=0
    )

    # Draw the outline and fill
    color_list = list(colors.values())
    for i in range(len(angles) - 1):
        color = color_list[i % len(color_list)]
        ax.plot(
            angles[i : i + 2],
            values[i : i + 2],
            "o-",
            linewidth=2,
            color=MPL_BLUE,
            markerfacecolor=color,
            markeredgecolor=color,
        )
        # Fill each segment
        ax.fill(
            [0, angles[i], angles[i + 1]],
            [0, values[i], values[i + 1]],
            alpha=0.25,
            color=MPL_BLUE,
        )

    # Draw radial lines from center to each corner
    for angle in angles[:-1]:
        ax.plot([angle, angle], [0, 10], "k-", linewidth=0.5, alpha=0.3, zorder=0)

    # Fix axis to go from 0 to max value
    ax.set_ylim(0, 10)

    # Hide the radial tick labels
    ax.set_yticklabels([])  # lines values.

    # Add labels with colors matching their data
    offset = 2 * np.pi / data_size / 10  # Offset labels slightly from the axes
    ax.set_xticks(
        [a + offset for a in angles[:-1]],
        labels=[f"{c}\n{v:.1f}" for c, v in zip(categories, values[:-1])],
    )

    # Darken colors and apply to labels
    for i, (label, color) in enumerate(zip(ax.get_xticklabels(), colors.values())):
        # Convert hex to RGB, darken, and apply
        r, g, b = to_rgb(color)
        darker_rgb = (r * 0.6, g * 0.6, b * 0.6)
        label.set_color(darker_rgb)
        label.set_fontweight("bold")

    # # Add a single entry to the legend
    # ax.plot(
    #     [],
    #     [],
    #     "o-",
    #     linewidth=2,
    #     color=MPL_BLUE,
    #     label="Affective State",
    # )

    # # Add legend and title
    # ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    ax.set_title(f"Affective State for {indicator_name}", y=1.08)

    # plt.tight_layout()
    plt.show()


def render_bar_chart(
    indicator_name: str, height_px: int, data: dict[str, float], colors: dict[str, str]
) -> None:
    keys = list(data.keys())
    values = list(data.values())

    markers_list = ["v", "1", "8", "s", "p", "P", "*", "X", "d"]
    if len(markers_list) < len(keys):
        print("Warning: markers_list size < keys size")

    # TODO: use height_px to set figure size
    fig2, ax2 = plt.subplots(layout="constrained", figsize=(8, 3))
    ax2.set_title(f"Affective State for {indicator_name}")

    i = 0
    for k, v in data.items():
        ax2.plot(k, [v], markers_list[i], c=colors[k])
        i += 1

    ax2.bar(keys, values)

    plt.show()


def render_charts(
    indicator_name: str,
    data: dict[str, float],
    colors: dict[str, str],
    height_px: int = 400,
):
    render_bar_chart(
        indicator_name=indicator_name,
        height_px=height_px,
        data=data,
        colors=colors,
    )

    render_polar_area_chart(
        indicator_name=indicator_name,
        height_px=height_px,
        data=data,
        colors=colors,
    )
    render_radar_chart(
        indicator_name=indicator_name,
        height_px=height_px,
        data=data,
        colors=colors,
    )

import itertools
import matplotlib.pyplot as plt
import numpy as np

# Marker and color cycles
MARKERS = ["o", "s", "D", "^", "v", "<", ">", "P", "X"]
COLOR_CYCLE = plt.cm.tab20.colors   # 20 distinct colors


def get_style_map(titles):
    """Assign a unique color + marker to each movie title."""
    styles = {}
    for title, color, marker in zip(titles, COLOR_CYCLE, itertools.cycle(MARKERS)):
        styles[title] = {"color": color, "marker": marker}
    return styles


def multi_dot_plot(df, plot_title):
    """
    df format:
    Title | Source | Rating
    """

    fig, ax = plt.subplots()

    titles = df["Title"].unique()
    styles = get_style_map(titles)

    for title in titles:
        sub = df[df["Title"] == title]

        ax.scatter(
            sub["Source"],
            sub["Rating"],
            s=120,
            label=title,
            color=styles[title]["color"],
            marker=styles[title]["marker"]
        )

        # Add text labels above each point
        for _, row in sub.iterrows():
            ax.text(
                row["Source"],
                row["Rating"] + 0.1,
                f"{row['Rating']:.1f}",
                ha="center"
            )

    ax.set_ylim(0, 10)
    ax.set_ylabel("Rating (0–10)")
    ax.set_title(plot_title)

    return fig, styles

def bar_charts(df, plot_title):
    """
    Create a grouped bar chart for rating sources across multiple movies.

    df format:
        Title | Source | Rating

    Example:
        Title        Source            Rating
        Inception    IMDb                8.8
        Inception    Rotten Tomatoes     8.7
        Inception    Metacritic          7.4
    """

    titles = df["Title"].unique()
    sources = ["IMDb", "Rotten Tomatoes", "Metacritic"]

    # numerical positions for sources
    x = np.arange(len(sources))

    # width of each bar group
    width = 0.8 / len(titles)

    fig, ax = plt.subplots(figsize=(8,5))

    for i, title in enumerate(titles):
        sub = df[df["Title"] == title]
        ratings = [sub[sub["Source"] == src]["Rating"].values[0]
                   if src in sub["Source"].values else 0
                   for src in sources]

        ax.bar(x + i*width, ratings, width=width, label=title)

    # Formatting
    ax.set_xticks(x + width*(len(titles)-1)/2)
    ax.set_xticklabels(sources)
    ax.set_ylim(0, 10)
    ax.set_ylabel("Rating (0–10)")
    ax.set_title(plot_title)
    ax.legend()

    return fig
"""
File: sankey.py
Author: Vichu Selvaraju

Description: A wrapper library for plotly sankey visualizations
"""

import pandas as pd
import plotly.graph_objects as go


def code_mapping(df, src, targ):
    """Map labels in src and targ colums to integers"""

    # Convert the src and targ columns to strings
    df[src] = df[src].astype(str)
    df[targ] = df[targ].astype(str)

    # Get the distinct labels
    labels = sorted(list(set(list(df[src]) + list(df[targ]))))

    # Create a label->code mapping
    codes = range(len(labels))
    lc_map = dict(zip(labels, codes))

    # Substitute codes for labels in the dataframe
    pd.set_option("future.no_silent_downcasting", True)
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels


def stack(df, src, targ, *cols, vals=None):
    """
    Stack a dataframe so there's only two columns
    df - Dataframe
    src - Source node column
    targ - Target node column
    cols - List of node columns
    vals - Link values (thickness)
    """
    # List of columns including the source, target and cols
    loc = [src, targ] + list(cols)
    # Generate pairs for the list of columns
    pairs = [(loc[i], loc[i + 1]) for i in range(len(loc) - 1)]
    stacked_df = pd.DataFrame()

    if vals == None:
        # For each pair make a dataframe and stack it
        for pair in pairs:
            new_df = df[[pair[0], pair[1]]]
            new_df.columns = ["src", "targ"]
            stacked_df = pd.concat([stacked_df, new_df], axis=0)

        # Set the values
        values = [1] * len(stacked_df)
    else:
        # For each pair make a dataframe and stack it
        for pair in pairs:
            new_df = df[[pair[0], pair[1], vals]]
            new_df.columns = ["src", "targ", vals]
            stacked_df = pd.concat([stacked_df, new_df], axis=0)
            # Aggregate the vals
            stacked_df = stacked_df.groupby(["src", "targ"], as_index=False)[vals].sum()

        # Set the values
        values = stacked_df[vals]

    return values, stacked_df


def make_sankey(df, src, targ, *cols, vals=None, **kwargs):
    """
    Create a sankey figure
    df - Dataframe
    src - Source node column
    targ - Target node column
    cols - List of node columns
    vals - Link values (thickness)
    """

    if cols:
        # Stack the dataframe so there's only 2 columns
        values, stacked_df = stack(df, src, targ, *cols, vals=vals)

        # Set the new source and target values for code_mapping
        src, targ = "src", "targ"
        # Get dataframe and labels from codemapping
        df, labels = code_mapping(stacked_df, src, targ)
    else:
        # Get dataframe and labels from codemapping
        df, labels = code_mapping(df, src, targ)

        if vals:
            values = df[vals]
        else:
            values = [1] * len(df)

    link = {"source": df[src], "target": df[targ], "value": values}

    thickness = kwargs.get("thickness", 50)
    pad = kwargs.get("pad", 50)

    node = {"label": labels, "thickness": thickness, "pad": pad}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()


def main():
    df = pd.read_csv("test.csv")
    make_sankey(df, "A", "B", "C", vals="Count")


if __name__ == "__main__":
    main()

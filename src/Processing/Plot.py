# -*- coding: utf-8 -*-

"""
Contains all the functions used to plot data

Todo
----
.. raw:: html

    <mark>Refactor this module</mark>
"""

import logging as logger
from typing import List, Union, overload
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.missing_ipywidgets import FigureWidget
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
#                               Main plots
# -----------------------------------------------------------------------------


@overload
def spider_plot(
        columns: List[str],
        names: str,
        values: List[float],
        show: bool = False) -> FigureWidget:
    """
    Does spider plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        The name for this plot (legend). If empty, will not show the legend
    `values`:
        The values for y axis

    Keyword Args
    ------------
    `show`:
        If settled will not show the figure at end

    Returns
    -------
    FigureWidget
        A figure plotly object (only access by ipykernel)

    Todo
    ----
    Missing treat exceptions
    """
    ...


@overload
def spider_plot(
        columns: List[str],
        names: List[str],
        values: List[List[float]],
        show: bool = False) -> FigureWidget:
    """
    Does spider plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        The names for each element in the array of values.
    `values`:
        An array of values 1-D for each element in `names`.

    Keyword Args
    ------------
    `show`:
        If settled will not show the figure at end

    Returns
    -------
    FigureWidget
        A figure plotly object (only access by ipykernel)

    Todo
    ----
    Missing treat exceptions
    """
    ...


def spider_plot(
        columns: List[str],
        names: Union[str, List[str]],
        values: Union[List[List[float]], List[float]],
        show: bool = False,
        file_name: str = None) -> FigureWidget:
    """
    Does spider plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        Can be a list of names or a single name. If empty, will not plot any legend
    `values`:
        An array of 1-D float lists or a single 1-D array of floats

    Keyword Args
    ------------
    `show`:
        If settled will not show the figure at end

    Returns
    -------
    FigureWidget
        A figure plotly object (only access by ipykernel)

    Todo
    ----
    Missing treat exceptions
    """
    logger.debug("Starting a new spyder/radial plot")

    # creating a new figure
    fig: FigureWidget = plotly.graph_objects.Figure()  # type: ignore

    isGrouped: bool = (type(names) is list) and (type(values[0]) is list)
    if not isGrouped:
        fig.add_trace(go.Scatterpolar(  # type: ignore
            r=values,
            theta=columns,
            fill='toself',
            name=names))
    else:
        # adding traces
        for k, v in zip(names, values):
            fig.add_trace(go.Scatterpolar(  # type: ignore
                r=v,
                theta=columns,
                fill='toself',
                name=k))

        fig.update_traces(texttemplate='%{text:.2f}')
        fig.update_layout(barmode='group', uniformtext_minsize=1,
                          uniformtext_mode='show', width=1000)

    # show this object
    if show:
        fig.show()
        
    if file_name:
        fig.write_html(file_name)

    # and return it
    return fig


@overload
def bar_plot(
    columns: List[str],
    names: str,
    values: List[float],
    show: bool = False
) -> FigureWidget:
    """
    Does a bar plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        The name for this plot (legend). If empty, will not show the legend
    `values`:
        The values for y axis

    Keyword Args
    ------------
    `show`:
        If settled, will show the generated image before return it.
    """
    ...


@overload
def bar_plot(
    columns: List[str],
    names: List[str],
    values: List[List[float]],
    show: bool = False
) -> FigureWidget:
    """
    Does a grouped bar plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        The names for each element in the array of values.
    `values`:
        An array of values 1-D for each element in `names`.

    Keyword Args
    ------------
    `show`:
        If settled, will show the generated image before return it.
    """
    ...


def bar_plot(
    columns: List[str],
    names: Union[str, List[str]],
    values: Union[List[List[float]], List[float]],
    show: bool = False,
    file_name: str = None) -> FigureWidget:
    """
    Does a grouped bar plot.

    Args
    ----
    `columns`:
        The values for x axis
    `names`:
        Can be a list of names or a single name. If empty, will not plot any legend
    `values`:
        An array of 1-D float lists or a single 1-D array of floats

    Keyword Args
    ------------
    `show`:
        If settled, will show the generated image before return it.
    """

    data: List[FigureWidget] = []
    isGrouped: bool = (type(names) is list) and (type(values[0]) is list)

    if not isGrouped:
        data.append(go.Bar(name=names, x=columns, y=values,
                    text=values, textposition='auto'))  # type: ignore

    else:
        # appending bar plots
        for k, v in zip(names, values):
            data.append(go.Bar(name=k, x=columns, y=v, text=v,
                        textposition='auto'))  # type: ignore
    fig = go.Figure(data)  # type: ignore

    # Change the bar mode
    if isGrouped:
        fig.update_traces(texttemplate='%{text:.2f}', textposition='auto')
        fig.update_layout(barmode='group', uniformtext_minsize=1,
                          uniformtext_mode='show', width=1500)
    if show:
        fig.show()
        
    if file_name:
        fig.write_html(file_name)

    return fig  # type: ignore


# -----------------------------------------------------------------------------
#                               Others plots
# -----------------------------------------------------------------------------

def parallel_plot(
    df: pd.DataFrame,
    column_color: str,
    s: int = 0,
    e: int = 5,
    show: bool = True,
    color_scale: List[str] = px.colors.diverging.Tealrose,
    width: int = 1200,
    height: int = 620
) -> FigureWidget:
    """
    Realize a parallel plot. A parallel plot is a plot similar to line plt.
    Check it out the `parallel plot`_ documentation.

    Keyword Args
    ---------------
        - `df`: The dataframe object to be plotted
        - `column_color`: The name of the column that holds the float equivalent number to be colored.\
            This column should hold ranges like 0.0..3.0

    :Kwargs:
        - `s`: start column to be plotted. *REMEBER* to include the column_color in this range.
        - `e`: end column
        - `show`: show the figure after generated
        - `color_scale`: it's a range of hexadecimal colors.\
            The default value is `plotly.express.colors.diverging.Tealrose`
        - `width`: the figure width
        - `height`: the figure height

    :Returns:
        A generated figure object

    .. _parallel plot: https://plotly.com/python/parallel-coordinates-plot/
    """
    # convert to list
    cols = df.columns.tolist()

    # cria um novo dataframe usando somente o range estipulado
    _d = df[cols[s:e]]

    fig: FigureWidget = px.parallel_coordinates(
        _d,
        color=column_color,
        width=width, height=height,
        color_continuous_scale=color_scale,
        color_continuous_midpoint=2,
    )  # type: ignore

    # exibe a figura
    if show:
        fig.show()

    return fig


def pie_plot(
    df: pd.DataFrame,
    col: str,
    threshold: float = 0.08,
    show: bool = False
) -> FigureWidget:
    """
    Generates a pie plot for a given dataframe.

    Keyword Args
    ---------------
        - `df`: A pandas dataframe object like
        - `col`: The column to be analysed

    :Kwargs:
        - `threshold`: The value that used to group elements in this column
        - `show`: If setled, show the generated plot too

    :Returns:
        A `plotly.Figure`
    """
    # removendo linhas onde essa competência não existe
    df = df.query(f"`{col}` > 0")
    # juntando índices com peso menor que threshold
    _index = df.loc[df[col] < threshold, col].index  # type:ignore
    # substituindo esses índices, gerando um "índice compartilhado"
    df.index = df.index.map(lambda x: "Outras" if x in _index else x)

    # gerando as anotações
    a = list(_index)
    a = [a[i:i+10] for i in range(0, len(a), 10)]
    annotation = "Outras: "
    for l in a:
        annotation += ','.join(l)
        annotation += '<br>'

    fig = px.pie(
        df,
        names=df.index,
        values=col,
        title=f"Distribuição da competência: {col}")

    # adicionando o nome das matérias ocultadas
    fig.add_annotation(  # type: ignore
        x=0, y=-0.27,
        text=annotation,
        showarrow=False)

    # fig.update_layout(showlegend=True)
    if show:
        fig.show()

    return fig


def all_competencies(df: pd.DataFrame, show: bool = False) -> FigureWidget:
    """
    Does a plot for all competencies (columns) in a given df.

    Keyword Args
    ---------------
        - `df`: A dataframe object like

    :Kwargs:
        - `show`: A flag to force show the generated figure

    :Returns:
        The generated plot
    """
    # generate subplots
    fig: FigureWidget = make_subplots(
        rows=df.shape[1],
        cols=1)  # type: ignore

    # add traces
    for i, competencia in enumerate(df.columns):
        _df = df[competencia]
        fig.add_trace(
            go.Scatter(
                x=list(map(lambda n: f'Resp#{n+1}', _df.index.tolist())),
                y=_df.values.tolist(),
                name=competencia,
                hovertemplate=f"<b>{competencia}</b><br>" +
                "<b>X:</b> %{x}<br><b>Valor:</b> %{y}<br><extra></extra>",
                hoverinfo="y+name",
                hoverlabel={'namelength': -1}
            ),  # type: ignore
            row=i+1, col=1)

    # update figure
    fig.update_yaxes(title="Valores")  # type: ignore
    fig.update_layout(
        height=4000,
        width=1000,
        title="Relação de Respostas x Competências",
        legend_title="Competências",
        hoverdistance=100,  # Distance to show hover label of data point
        spikedistance=1000,  # Distance to show spike
        font=dict(
            family="Courier New, monospace",
            size=9,
            color="RebeccaPurple"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=1),
        hoverlabel=dict(
            bgcolor="white",
            font_size=9,
            font_family="Rockwell"),
        showlegend=False)

    if show:
        fig.show()

    return fig

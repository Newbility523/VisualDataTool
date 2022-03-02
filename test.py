from bokeh.plotting import show, figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.tools import CustomJSHover

df = {'X_value': [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
      'model': ['m1', 'm1', 'm2', 'm2'],
      'color': ['red', 'red', 'blue', 'blue'],
      'Y_value': [[0.50, 0.66, 0.70, 0.67], [0.65, 0.68, 0.71, 0.66], [0.80, 0.79, 0.84, 0.80], [0.80, 0.83, 0.76, 0.64]]}

source = ColumnDataSource(df)

p = figure(plot_height=400)
p.multi_line(xs='X_value', ys='Y_value', legend="model", color='color',
             line_width=5, line_alpha=0.6, hover_line_alpha=1.0,
             source=source)

x_custom = CustomJSHover(code="""
    return '' + special_vars.data_x
""")

y_custom = CustomJSHover(code="""
    return '' + special_vars.data_y
""")

p.add_tools(
    HoverTool(
        show_arrow=False,
        line_policy='next',
        tooltips=[
            ('X_value', '@X_value{custom}'),  # or just ('X_value', '$data_x')
            ('Y_value', '@Y_value{custom}')
        ],
        formatters=dict(
            X_value=x_custom,
            Y_value=y_custom
        )
    )
)

show(p)
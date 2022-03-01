from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

from bokeh.models import BoxSelectTool
from bokeh.models import HoverTool
from bokeh.models import PanTool
from bokeh.models import WheelZoomTool
from bokeh.models import ResetTool
from bokeh.models import SaveTool

def get_count_data(size_list: list):
    temp_dic = {}
    for item in size_list:
        if item not in temp_dic:
            temp_dic[item] = 0
        temp_dic[item] += 1

    size_list.sort()
    data = {
        'size': [],
        'count': []
    }
    for item in size_list:
        data['size'].append(item)
        data['count'].append(temp_dic[item])

    return data, 'size', 'count'


raw_data = [3.3, 2.8, 1.1, 1, 10, 20, 1.1, 21, 22, 15, 15, 15, 16]
result = get_count_data(raw_data)
source = ColumnDataSource(data=result[0])

tools = [
    PanTool(),
    BoxSelectTool(dimensions="width"),
    WheelZoomTool(),
    ResetTool(),
    HoverTool(),
    SaveTool()
]

p = figure(title="Multiple glyphs example", x_axis_label="x", y_axis_label="y", tools=tools)
p.line(x=result[1], y=result[2], source=source, color="blue", line_width=2)

show(p)

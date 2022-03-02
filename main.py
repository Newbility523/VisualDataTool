import json
import os
import sys

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import column, row

from bokeh.models import BoxSelectTool
from bokeh.models import HoverTool
from bokeh.models import PanTool
from bokeh.models import WheelZoomTool
from bokeh.models import ResetTool
from bokeh.models import SaveTool

M = 1024 * 1024


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


def get_file_size(path_str: str):
    global M
    file_sizes = []
    max_size = 0
    max_size_file = None
    for root, dirs, files in os.walk(path_str):
        for file in files:
            if file.endswith(".ab"):
                size = os.path.getsize(os.path.join(root, file)) / M
                file_sizes.append(round(size, 2))
                if size > max_size:
                    max_size = size
                    max_size_file = os.path.join(root, file)

    print("max size file: ", max_size_file)
    print("max size: ", max_size)
    return file_sizes


def add_size_data(p: figure, path, name, color):
    # new
    file_sizes = get_file_size(path)
    result = get_count_data(file_sizes)
    source = ColumnDataSource(data=result[0])
    p.circle(x=result[1], y=result[2], legend_label=name, source=source, color=color, line_width=2)
    # p.line(x=result[1], y=result[2], legend_label=name, source=source, color=color, line_width=2)


def show_size_count(path1, path2):
    tools = [
        PanTool(),
        BoxSelectTool(dimensions="width"),
        WheelZoomTool(),
        ResetTool(),
        HoverTool(),
        SaveTool()
    ]

    polt = figure(
        title="Asset bundle 容量统计",
        x_axis_label="size",
        y_axis_label="count",
        sizing_mode="stretch_width",
        tools=tools,
        max_height=200
    )

    add_size_data(polt, path1, "new", "red")
    add_size_data(polt, path2, "old", "orange")

    return polt


def show_level_package_1(cfg_path: str, color):
    """
    等级分包的 AB 分布情况
    """
    if os.path.isfile(cfg_path):
        cfg_file = open(cfg_path, "r")
        resource_json = json.loads(cfg_file.read())

    level_size = {
        "level": [],
        "size": []
    }

    for v in resource_json.values():
        level_size["level"].append(v["level"])
        size = v["size"] / M
        level_size["size"].append(round(size, 2))

    tools = [
        PanTool(),
        BoxSelectTool(dimensions="width"),
        WheelZoomTool(),
        ResetTool(),
        HoverTool(),
        SaveTool()
    ]

    polt = figure(
        title="等级分包的 AB 分布情况",
        x_axis_label="level",
        y_axis_label="size",
        sizing_mode="stretch_width",
        tools=tools,
        max_height=200
    )

    source = ColumnDataSource(level_size)
    polt.circle(x="level", y="size", legend_label="level", source=source, color=color, line_width=2)

    return polt


def show_level_package_2(cfg_path: str, color):
    """
    等级分包的 AB 总容量分布情况
    """
    if os.path.isfile(cfg_path):
        cfg_file = open(cfg_path, "r")
        resource_json = json.loads(cfg_file.read())

    level_size = {}

    for v in resource_json.values():
        if not v["level"] in level_size:
            level_size[v["level"]] = 0

        level_size[v["level"]] += v["size"] / M

    tools = [
        PanTool(),
        BoxSelectTool(dimensions="width"),
        WheelZoomTool(),
        ResetTool(),
        HoverTool(),
        SaveTool()
    ]

    polt = figure(
        title="等级分包的 AB 总容量分布情况",
        x_axis_label="level",
        y_axis_label="size",
        sizing_mode="stretch_width",
        tools=tools,
        max_height=200
    )

    polt.vbar(x=list(level_size.keys()), top=list(level_size.values()), fill_color="#b3de69")

    return polt


def main():
    # test
    path1 = r"E:\Y08\Client\production\resources\win\assetbundle"
    path2 = r"C:\Users\Administrator\Desktop\assetbundle_bk\assetbundle"
    # path1 = sys.argv[1]
    # path2 = sys.argv[2]
    polt1 = show_size_count(path1, path2)

    cfg_path = r"E:\New3D\Client\production\resources\win\assetbundle\resource.json"
    polt2 = show_level_package_1(cfg_path, "blue")

    cfg_path = r"E:\New3D\Client\production\resources\win\assetbundle\resource.json"
    polt3 = show_level_package_2(cfg_path, "green")

    # show(column(polt1, polt2))
    show(column(children=[polt1, polt2, polt3], sizing_mode="scale_width"))
    # show(row(children=[polt1, polt2], sizing_mode="scale_width"))


if __name__ == '__main__':
    # print(sys.argv)
    main()


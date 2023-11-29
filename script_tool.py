from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
from typing import Dict

import pandas as pd


@dataclass
class Scene:
    """幕类"""
    index: int
    time: str
    location: str
    day_or_night: str
    in_or_out: str
    summary: str


@dataclass
class Chapter:
    """章类"""
    index: int
    name: str
    scenes: Dict[int, Scene]


def get_chapter_list(chapter_index: int, chapter_name: str) -> list:
    """将一章读取为一个列表"""
    chapter_file_name = "{}-{}.md".format(str(chapter_index).zfill(2), chapter_name)

    with open("./Chapters/" + chapter_file_name, "r", encoding="utf8") as f:
        chapter = f.read()

    return chapter.split("\n")


def get_scene(script, row: int) -> Scene:
    """
    读取剧本表格的某一行
    返还一个Scene对象
    """
    scene_index = int(script.loc[row, '幕次'])
    scene_time = _ if not pd.isna(_ := script.loc[row, '幕次时间']) else None
    # print(scene_time)
    # 尝试将excel的时间转换为可读的
    try:
        # time_true = pd.to_datetime('1899-12-30') + pd.Timedelta(str(scene_time) + 'days')
        scene_time = datetime.strptime(str(scene_time), "%Y-%m-%d %H:%M:%S")  # 从str转换为datetime
        scene_time = "{}年{}月{}日".format(scene_time.year, scene_time.month, scene_time.day)  # 从datetime转换为str
    except ValueError:
        pass

    scene_location = _ if not pd.isna(_ := script.loc[row, '地点']) else None
    scene_day_or_night = _ if not pd.isna(_ := script.loc[row, '日夜']) else None
    scene_in_or_out = _ if not pd.isna(_ := script.loc[row, '内外']) else None
    scene_summary = _ if not pd.isna(_ := script.loc[row, '概括']) else None
    scene = Scene(scene_index, scene_time, scene_location, scene_day_or_night, scene_in_or_out, scene_summary)

    return scene


def make_chapter_dict(script) -> Dict[int, Chapter]:
    """将剧本表格转换为chapter字典"""
    script_num_rows, script_num_columns = script.shape
    print("表格总行数 =", script_num_rows)

    chapter_dict = {}  # 章节字典
    current_chapter_index = -1

    for i in range(script_num_rows):  # 按行遍历表格

        if pd.isna(script.loc[i, '序号']):  # 如果章节号为空
            if not pd.isna(script.loc[i, '幕次']):  # 如果有幕次
                current_scene = get_scene(script, i)  # 读取幕次
                chapter_dict[current_chapter_index].scenes[current_scene.index] = current_scene
            else:
                continue

        else:  # 如果有新章节号
            current_chapter_index = int(script.loc[i, '序号'])
            current_chapter_name = script.loc[i, '章节']

            chapter_dict[current_chapter_index] = Chapter(current_chapter_index,
                                                          current_chapter_name,
                                                          {})

            if not pd.isna(script.loc[i, '幕次']):  # 如果有幕次则读取幕次
                current_scene = get_scene(script, i)
                chapter_dict[current_chapter_index].scenes[current_scene.index] = current_scene

    # pprint(chapter_dict)  # 打印chapter_dict
    return chapter_dict


def compile_chapter(chapter_dict: Dict[int, Chapter], current_chapter_index: int):
    """单独根据章节字典编译某一个章节的章节标题和幕次标题
    :param chapter_dict: 章节字典
    :param current_chapter_index: 要编译的章节的序号
    """

    current_chapter = chapter_dict[current_chapter_index]  # 当前章节对象

    current_chapter_list = get_chapter_list(current_chapter.index, current_chapter.name)  # 读取章节为列表

    scene_title_count = 1  # 记录读取到多少个幕次标题，默认1幕
    for line_index in range(len(current_chapter_list)):  # 按行遍历章节
        line = current_chapter_list[line_index]

        if line.startswith("## "):  # 读取到章节标题
            # 生成章节标题
            current_chapter_title_list = []  # 当前章节标题列表

            if current_chapter.index == 0:  # 标注是第几场
                current_chapter_title_list.append('序幕')
            else:
                current_chapter_title_list.append("第{}场".format(current_chapter.index))

            # 在场次中加上章节名
            current_chapter_title_list.append('《{}》'.format(current_chapter.name))

            if current_chapter.scenes[0]:  # 如果存在0号幕次
                if current_chapter.scenes[0].time:  # 如果0号幕有时间
                    current_chapter_title_list.append(current_chapter.scenes[0].time)
                if current_chapter.scenes[0].location:  # 如果0号幕有地点
                    current_chapter_title_list.append(current_chapter.scenes[0].location)
                if current_chapter.scenes[0].day_or_night:  # 如果0号幕有日夜
                    current_chapter_title_list.append(current_chapter.scenes[0].day_or_night)
                if current_chapter.scenes[0].in_or_out:  # 如果0号幕有内外
                    current_chapter_title_list.append(current_chapter.scenes[0].in_or_out)

            current_chapter_title = "## " + "-".join(current_chapter_title_list)  # 拼接章节标题

            current_chapter_list[line_index] = current_chapter_title  # 替换章节标题

        elif line.startswith("### "):  # 读取到幕次标题

            current_scene_title_list = ["第{}幕".format(scene_title_count)]  # 当前幕次标题列表

            if current_chapter.scenes[scene_title_count]:  # 如果存在对应幕次
                if current_chapter.scenes[scene_title_count].time:  # 如果0号幕有时间
                    current_scene_title_list.append(current_chapter.scenes[scene_title_count].time)
                if current_chapter.scenes[scene_title_count].location:  # 如果0号幕有地点
                    current_scene_title_list.append(current_chapter.scenes[scene_title_count].location)
                if current_chapter.scenes[scene_title_count].day_or_night:  # 如果0号幕有日夜
                    current_scene_title_list.append(current_chapter.scenes[scene_title_count].day_or_night)
                if current_chapter.scenes[scene_title_count].in_or_out:  # 如果0号幕有内外
                    current_scene_title_list.append(current_chapter.scenes[scene_title_count].in_or_out)
            else:  # 丢失幕次时报错
                print("怀疑丢失幕次")

            current_scene_title = "### " + "-".join(current_scene_title_list)  # 拼接幕次标题

            current_chapter_list[line_index] = current_scene_title  # 替换幕次标题

            scene_title_count += 1  # 最后将计数+1

    '''目前为止以及对章节原文完成了标题上的修改，下一步是写入文件'''

    with open("./Chapters/{}-{}.md".format(str(current_chapter.index).zfill(2), current_chapter.name),
              "w+", encoding="utf8") as f:
        f.write("\n".join(current_chapter_list))

    print("完成了对 {}-{} 的修改，该章节共 {} 幕。".format(str(current_chapter.index).zfill(2), current_chapter.name, scene_title_count))


if __name__ == "__main__":
    script = pd.read_excel('./事出无因-表格.xlsx', sheet_name='剧本')  # 从excel文件读取剧本表格
    chapter_dict = make_chapter_dict(script)  # 从剧本表格生成章节字典

    # 编译文件
    for i in range(58):
        compile_chapter(chapter_dict, i)

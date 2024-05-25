#!/usr/bin/env python3

# Copyright 2018-2024 Andrew Lyu. All Rights Reserved.

"""
A jianpu SVG generator.
"""

import argparse
import os
import requests
import simplejson as json
import subprocess

from lxml import etree


def pull_svg(source: str, output: str):
    font = "PingFang SC, Microsoft YaHei, Open Sans, sans-serif"
    config = {
        "page": "A5_horizontal",
        "margin_top": "80",
        "margin_bottom": "80",
        "margin_left": "80",
        "margin_right": "80",
        "biaoti_font": font,
        "shuzi_font": "b",
        "geci_font": font,
        "height_quci": "13",
        "height_cici": "10",
        "height_ciqu": "40",
        "height_shengbu": "0",
        "biaoti_size": "42",
        "fubiaoti_size": "24",
        "geci_size": "24",
        "body_margin_top": "40",
        "lianyinxian_type": "0",
    }
    data = {
        "code": source.replace("\n", "&hh&"),
        "customCode": "&hh&&hh&[fenye]",
        "pageConfig": json.dumps(config),
    }
    url = "http://zhipu.lezhi99.com/Zhipu-draw"
    res = requests.post(url, data=data)
    if res.ok:
        text = res.text.replace("[fenye]", "")
        with open(output, "w") as f:
            f.write(text)
        tree = etree.parse(output)
        root = tree.getroot()
        root.attrib["width"] = "1200"
        root.attrib["height"] = "675"
        root.attrib["viewBox"] = "0 0 1200 675"
        tree.write(output, encoding="UTF-8")


def optimize_svg(svg: str):
    cmd = f"svgo {svg}"
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    usage = "%(prog)s [<args>]"
    description = "A jianpu SVG generator."
    parser = argparse.ArgumentParser(usage=usage, description=description)
    parser.add_argument("-i", dest="input", help="input file")
    parser.add_argument("-o", dest="output", help="output file")
    args = parser.parse_args()
    with open(args.input, "r") as src:
        pull_svg(src.read(), args.output)
    optimize_svg(args.output)

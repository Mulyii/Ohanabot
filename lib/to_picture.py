from typing import Any
from nonebot_plugin_htmlrender import md_to_pic


def one_row(items: list[Any], is_header: bool) -> str:
    label = "th" if is_header else "td"
    res = '<tr>\n'
    for item in items:
        res += f'<{label} align="center"> {item} </{label}>\n'
    res += '</tr>\n'
    return res

# 传入表的标题， 表头， 表的内容， 图片的宽度（可选， 默认 500）
async def table_to_pic(title: str, headers: list[Any], table: list[list[Any]], w: int = 500):
    html = f'<div align="center"><h1>{title}</h1></div>\n'
    html += f'<table border="1" align="center">\n'
    html += one_row(headers, True)
    for row in table:
        html += one_row(row, False)
    html += f'</table>'
    return await md_to_pic(md=html, width=w)


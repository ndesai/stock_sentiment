# Take a list of stocks and format them into a readable email format

import schema
from jinja2 import Template
import json
from pathlib import Path


def get_html(date: str, data: schema.StockAnalysisList) -> str:
    with open(Path(__file__).parent / "tpl/email.tpl.html", "r") as f:
        template = Template(f.read())
    return template.render(date=date, stocks=data.stocks)


if __name__ == "__main__":
    with open(Path(__file__).parent / "example/StockAnalysisList.json", "r") as f:
        data = schema.StockAnalysisList(**json.load(f))
    html = get_html("January 27, 2026 at 12:30:04", data)
    with open("result.html", "w") as f:
        f.write(html)

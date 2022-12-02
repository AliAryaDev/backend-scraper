import xml.etree.ElementTree as ET
from typing import List, Tuple
import json


def indices(file_path: str = "market.json") -> List[dict]:
    """
        Load Stocks
    """
    try:
        with open(file_path, "r", encoding="utf-8") as target:
            return [item["stock_index"] for item in json.load(target)]
    except:
        pass
    return []


def xml_parser(content: bytes, stock_id: int) -> dict:
    """
        Parse the XML Content and Convert It Into A Dictionary Object
    """
    response_obj = {}

    xml_content = ET.fromstring(content)
    if not xml_content:
        return response_obj

    trades = xml_content.findall("row")
    if not trades:
        return response_obj

    cells = trades[-1].findall("cell")
    if cells:
        index = int(cells[0].text.strip())
        time = cells[1].text.strip()
        volume = int(cells[2].text.strip())
        price = int(cells[3].text.strip().split(".")[0])

        response_obj.update(stock_id=stock_id)
        response_obj.update(index=index)
        response_obj.update(time=time)
        response_obj.update(volume=volume)
        response_obj.update(price=price)

    return response_obj

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pymupdf
from sklearn.cluster import DBSCAN


@dataclass(frozen=True, eq=True)
class Page:
    starting_letters: frozenset[str]


@dataclass(eq=True)
class TextChunk:
    # is_code: bool
    text: tuple[str, ...]
    bbox: tuple[float, float, float, float]
    page: Page
    label: int = None
    line_nr: int = None

    @property
    def text_str(self) -> str:
        def clean(text: str) -> str:
            if text in ["-", "―","—","-----"]:
                return "---"
            # if text in ["."]:
            #     return ""
            return text

        text = [clean(text) for text in self.text]

        total_text = "".join(text)
        total_text = total_text.replace("to---day", "to-day")
        total_text = total_text.replace("to---night", "to-night")
        total_text = total_text.replace("to---morrow", "to-morrow")

        return total_text

    @property
    def is_just_dot(self) -> bool:
        return self.text_str in ['•', '·']

    @property
    def y_coord(self):
        return self.bbox[1]

    @property
    def xy_coord(self):
        return self.bbox[:2]

    @property
    def is_code(self) -> bool:
        if len(self.text) != 1:
            return False
        word = self.text[0]
        return word[0] in self.page.starting_letters

    @property
    def debug_dict(self):
        return {
            "text": self.text_str,
            "line_nr": self.line_nr,
            "xy_coord": self.xy_coord,
        }


doc = pymupdf.open("Unicode_The_Universal_Telegraphic_Phrase.pdf")

page_offset = 15


def rotate(origin, point, angle_deg):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    angle = math.radians(angle_deg)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def rotate_bbox(bbox, page_center, angle):
    xmin, ymin, xmax, ymax = bbox
    xmin, ymin = rotate(page_center, (xmin, ymin), angle)
    xmax, ymax = rotate(page_center, (xmax, ymax), angle)
    return xmin, ymin, xmax, ymax


angle = 0
# angle = 0.4


def extract_page(page_nr: int, starting_letters: frozenset[str], debug: bool = False):
    pdf_page: pymupdf.Page = doc[page_nr + page_offset]
    chunks = []
    page = Page(starting_letters)
    all_data = pdf_page.get_textpage().extractDICT()
    page_width = all_data["width"]
    page_height = all_data["height"]
    page_center = (page_width / 2, page_height / 2)
    for block in all_data["blocks"]:
        for line in block["lines"]:
            text = [s["text"] for s in line["spans"]]
            chunk = TextChunk(
                text=tuple(text),
                bbox=rotate_bbox(line["bbox"], page_center, angle),
                page=page,
            )
            if chunk.is_just_dot:
                continue
            chunks.append(chunk)

    y_coords = np.array([chunk.y_coord for chunk in chunks]).reshape(-1, 1)
    dbscan = DBSCAN(eps=5, min_samples=1)
    raw_labels = dbscan.fit_predict(y_coords)
    for chunk, label in zip(chunks, raw_labels):
        chunk.label = int(label)

    unique_labels = sorted(
        set(raw_labels),
        key=lambda label: np.mean([y for y, lbl in zip(y_coords.flatten(), raw_labels) if lbl == label])
    )

    label_to_line_nr = {label: idx for idx, label in enumerate(unique_labels)}

    for chunk in chunks:
        chunk.line_nr = label_to_line_nr[chunk.label]

    chunks.sort(key=lambda chunk: (chunk.line_nr, chunk.bbox[0]))
    out_data = {}

    code_chunks = [c for c in chunks if c.is_code]
    code_start_xs=[]
    for code_chunk in code_chunks:
        code_start_xs.append(code_chunk.xy_coord[0])
    print(code_start_xs[0],code_start_xs[-1])

    code_chunks.sort(key=lambda c: c.y_coord)
    other_chunks = [c for c in chunks if not c.is_code]

    for code_chunk in code_chunks:
        out_data[code_chunk.text_str] = {
            "line_nr": code_chunk.line_nr,
        }

    for c in other_chunks:
        if c.line_nr == 0:
            # title line
            continue
        matching_code = None
        for code_chunk in code_chunks:
            if code_chunk.line_nr >= c.line_nr:
                matching_code = code_chunk.text_str
                break
        if matching_code is None:
            print(f"no matching code found for chunk {c}")
            print(c.text_str)
            continue
        if "chunks" in out_data[matching_code]:
            out_data[matching_code]["chunks"].append(c)
        else:
            out_data[matching_code]["chunks"] = [c]
        out_data[matching_code]["text"] = " ".join(map(lambda c: c.text_str, out_data[matching_code]["chunks"]))

    # per string post-processing
    for k in sorted(out_data.keys()):
        try:
            text=out_data[k]["text"]
            if text.endswith(" ."):
                text = text[:-2]
                out_data[k]["text"] = text
            if text.endswith("."):
                print("ends with .:",text)
        except KeyError:
            continue

    # print(chunks)
    for d in out_data.values():
        if debug:
            c: TextChunk
            d["debug"] = list(map(lambda c: c.debug_dict, d["chunks"]))
        if "chunks" in d:
            del d["chunks"]
    outfile = Path(f"raw_data/{page_nr}.json")

    # names = list(out_data.keys())
    # print(names)
    # print(sorted(names))
    # assert names == sorted(names)

    # if outfile.exists():
    #     raise FileExistsError(f"File '{outfile}' already exists")
    with outfile.open("w") as f:
        json.dump(out_data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    extract_page(int(sys.argv[1]), frozenset(sys.argv[2]))

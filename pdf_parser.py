# TODO: rewrite as a OOP
import sys

import pdfquery
import numpy as np


# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


def url_to_name(file_url, iter_count=1):
    input_file_url = file_url
    file_name = file_url
    process_url = file_url
    error_counter = 0
    while iter_count > 0:

        # Checking infinite loop
        error_counter += 1
        if error_counter > 8000:
            print("[ERROR] url_to_name > infinite loop")
            print(input_file_url)
            raise LookupError

        # Method logic
        if process_url[-1] == '/':
            process_url = process_url[:-1]
        for _ in range(1, len(process_url)):
            char = process_url[-1]
            if char == '/':
                file_name = file_url[len(process_url):]
                file_url = process_url[:-1]
                iter_count -= 1
                break
            else:
                process_url = process_url[:-1]
    return file_name


def url_parent(file_url, iter_count=1):
    input_file_url = file_url
    parent_url = file_url
    process_url = file_url
    error_counter = 0
    while iter_count > 0:

        # Checking infinite loop
        error_counter += 1
        if error_counter > 8000:
            print("[ERROR] url_parent > infinite loop")
            print(input_file_url)
            raise LookupError

        # Method logic
        if process_url[-1] == '/':
            process_url = process_url[:-1]
        for _ in range(1, len(process_url)):
            char = process_url[-1]
            if char == '/':
                parent_url = process_url
                iter_count -= 1
                break
            else:
                process_url = process_url[:-1]

    return parent_url


# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


def find_tag_name_by_char_index(char_index, dom):
    """

    :param char_index: int      | The index of char inside the tag brackets "<" and ">" that are inside the dom string
    :param dom: str             | The DOM as a string
    :return: str                | Tag name
    """
    for tag_name_close_index in range(len(dom[char_index:])):
        if dom[char_index + tag_name_close_index] == " ":
            return dom[char_index + 1:char_index + tag_name_close_index]


def get_tag_by_attr_position(char_index, dom):

    # Finding open bracket for tag
    open_index = 0
    for open_bracket_index in range(char_index):
        if dom[char_index - open_bracket_index] == "<":
            open_index = char_index - open_bracket_index
            break

    # Getting tag name
    tag_name = find_tag_name_by_char_index(open_index, dom)

    # Finding close bracket for tag
    close_index = 0
    is_parent = False
    for close_bracket_index in range(len(dom[char_index:])):
        current_position = char_index + close_bracket_index
        if dom[current_position:current_position + len(tag_name) + 3] == f"</{tag_name}>":
            close_index = current_position + len(tag_name) + 3
            break
        if dom[current_position] == "<":
            is_parent = True

    if is_parent:
        tag = f"{dom[open_index:close_index]}1"
    else:
        tag = f"{dom[open_index:close_index]}0"

    return tag


def find_position(string_to_find, dom):
    for tag_name_open_index in range(len(dom) - len(string_to_find)):
        dom_process_str = dom[tag_name_open_index:tag_name_open_index + len(string_to_find)]
        if dom_process_str == string_to_find:
            return tag_name_open_index
    return None


def get_tag_by_name(tag_name, dom):
    """

    :param tag_name: str        | The name of tag
    :param dom: str             | The DOM as a string
    :return: str                | First tag that has the same name
    """
    # Getting the tag name position
    tag_name_first_char_index = find_position(tag_name, dom)

    # Getting the whole tag
    tag = get_tag_by_attr_position(tag_name_first_char_index, dom)
    return tag


def get_all_tags_by_name(tag_name, dom):
    """

        :param tag_name: str        | The name of tag
        :param dom: str             | The DOM as a string
        :return: str                | All tags that has the same name
        """
    # Finding the tag position
    tag_name_first_char_index_list = []
    for tag_name_open_index in range(len(dom) - len(tag_name)):
        dom_process_str = dom[tag_name_open_index:tag_name_open_index + len(tag_name)]
        dom_process_str_previous_char = dom[tag_name_open_index - 1]
        if (dom_process_str == tag_name) and dom_process_str_previous_char != "/":
            tag_name_first_char_index_list.append(tag_name_open_index)

    # Getting the whole tags
    tag_list = []
    for tag_name_first_char_index in tag_name_first_char_index_list:
        tag = get_tag_by_attr_position(tag_name_first_char_index, dom)
        tag_list.append(tag)

    return tag_list


def get_bbox(char_index, dom):
    # Finding open bracket for bbox
    open_index = char_index
    if dom[char_index + 7] == "[":
        open_index = char_index + 7
    else:
        for open_bracket_index in range(len(dom[char_index:])):
            if dom[char_index + open_bracket_index] == "[":
                open_index = char_index + open_bracket_index + 1
                break

    # Finding close bracket for tag
    close_index = 0
    for close_bracket_index in range(len(dom[char_index:])):
        if dom[char_index + close_bracket_index] == "]":
            close_index = char_index + close_bracket_index
            break

    bbox = [float(x.strip()) for x in dom[open_index:close_index].split(",")]

    return bbox


def relative_bbox_to_bbox(relative_bbox, page_bbox):
    """

    :param relative_bbox: tuple[float]  | (20, 20, 80, 80) -> (20%, 20%, 80%, 80%)
    :param page_bbox: tuple[float]      | (0, 0, 300, 600) -> (x0, y0, x1, y1)
    :return:
    """
    relative_bbox = np.array(relative_bbox)
    page_bbox = np.array((page_bbox[2], page_bbox[3], page_bbox[2], page_bbox[3])).transpose()
    return np.multiply(relative_bbox * 0.01, page_bbox)


def check_nesting(bbox, parent_bbox):
    """

    :param bbox: tuple[float]             | (200, 200, 300, 600) -> (x0, y0, x1, y1)
    :param parent_bbox: tuple[float]      | (200, 200, 300, 600) -> (x0, y0, x1, y1)
    :return:
    """
    # Checking types of input
    if (type(bbox) == list) or (type(bbox) == tuple):
        bbox = np.array(bbox)
    elif type(bbox) == np.ndarray:
        pass
    else:
        print("[ERROR] check_nesting > wrong bbox type:", type(bbox), "bbox:", bbox)

    if (type(parent_bbox) == list) or (type(parent_bbox) == tuple):
        parent_bbox = np.array(parent_bbox)
    elif type(parent_bbox) == np.ndarray:
        pass
    else:
        print("[ERROR] check_nesting > wrong parent_bbox type:", type(parent_bbox), "parent_bbox:", parent_bbox)

    check_bbox = bbox - parent_bbox
    filter_bbox = check_bbox < 0
    filter_bbox_to_check = (False, False, True, True)
    if ((filter_bbox[0] == filter_bbox_to_check[0]) and
        (filter_bbox[1] == filter_bbox_to_check[1]) and
        (filter_bbox[2] == filter_bbox_to_check[2]) and
        (filter_bbox[3] == filter_bbox_to_check[3])
    ):
        return True
    else:
        return False


def get_tag_text(tag):
    """

    :param tag: str
    :return:
    """
    text = ""
    key_to_write = False
    for char in tag:
        if char == "<":
            key_to_write = False
        if key_to_write:
            text += char
        if char == ">":
            key_to_write = True
    return text


def get_table(xml_text, bbox_to_find):

    # Finding first row
    bottom_bbox = [x for x in bbox_to_find]
    bottom_bbox[1] = float(bbox_to_find[3])
    right_bbox = [x for x in bbox_to_find]
    right_bbox[2] = bbox_to_find[0]
    tblr_bbox = {
        "top": bbox_to_find,
        "bottom": bottom_bbox,
        "left": bbox_to_find,
        "right": right_bbox,
    }
    first_row = []

    # # Searching tags inside the increasing bbox > bottom border -= 2.5% of top border coordinates; right border += 10%
    while bottom_bbox[1] > 0:
        bottom_bbox[1] -= bbox_to_find[3] * 0.025
        tblr_bbox.update({"bottom": bottom_bbox})
        while right_bbox[2] < bbox_to_find[2]:
            right_bbox[2] += bbox_to_find[2] * 0.1
            tblr_bbox.update({"right": right_bbox})
            bbox_to_find_first_row = tblr_to_bbox(tblr_bbox)
            item_tags = tags_inside_bbox(xml_text, bbox_to_find_first_row)
            if len(item_tags) > 0:
                for item in item_tags:
                    first_row.append(item)
                left_bbox = get_bbox(0, first_row[-1])
                left_bbox = [left_bbox[2], 0, 0, 0]
                tblr_bbox.update({"left": left_bbox})
        if len(first_row) > 0:
            break
        right_bbox[2] = bbox_to_find[0]

    if len(first_row) == 0:
        return []

    # Calculating width of columns
    list_of_col_params = []
    for column_tag in first_row:
        col_header_bbox = get_bbox(0, column_tag)
        col_header_width = col_header_bbox[2] - col_header_bbox[0]
        col_middle_coord = col_header_bbox[0] + (col_header_width / 2)
        col_params = {
                "left": col_header_bbox[0],
                "right": col_header_bbox[2],
                "middle": col_middle_coord,
                "width": col_header_width,
                "header_bbox": col_header_bbox,
            }
        list_of_col_params.append(col_params)

    # Finding the smaller left coordinate and the larger right coordinate
    for col_params, col_index in zip(list_of_col_params, range(len(list_of_col_params))):
        char_index = 0

        # Find bbox and associated tag
        while char_index <= len(xml_text) - 3:
            if xml_text[char_index:char_index + 4] == "bbox":
                tag = get_tag_by_attr_position(char_index, xml_text)

                # if tag is parent tag then skip
                if tag[-1] == "1":
                    char_index += 1
                    continue
                bbox = get_bbox(char_index, xml_text)

                # If middle coordinate inside bbox width
                if (bbox[0] < col_params["middle"]) and (bbox[2] > col_params["middle"]):

                    # If not first column
                    if col_index > 0:

                        # If left border coordinate of the bbox is less than current > replace
                        if (
                                (col_params["left"] > bbox[0]) and
                                check_nesting(bbox, bbox_to_find) and
                                (list_of_col_params[col_index - 1]["middle"] < bbox[0])
                        ):
                            col_params.update({"left": bbox[0]})

                    # If first column
                    else:

                        # If left border coordinate of the bbox is less than current > replace
                        if (col_params["left"] > bbox[0]) and check_nesting(bbox, bbox_to_find):
                            col_params.update({"left": bbox[0]})

                    # If not last column
                    if col_index < len(list_of_col_params) - 1:

                        # If right border coordinate of the bbox is greater than current > replace
                        if (
                                (col_params["right"] < bbox[2]) and
                                check_nesting(bbox, bbox_to_find) and
                                (list_of_col_params[col_index + 1]["middle"] > bbox[2])
                        ):
                            col_params.update({"right": bbox[2]})

                    # If last column
                    else:

                        # If left border coordinate of the bbox is less than current > replace
                        if (col_params["right"] < bbox[2]) and check_nesting(bbox, bbox_to_find):
                            col_params.update({"right": bbox[2]})

            char_index += 1

        col_width = col_params["right"] - col_params["left"]
        col_params.update({"width": col_width})
        list_of_col_params[col_index].update(col_params)

    sys.exit()
    # TODO: parse lost text ???
    ...
    # TODO: get rows heights
    ...
    # TODO: get columns
    ...
    # bbox = tblr_to_bbox(tblr_bbox)
    # tags = get_all_tags_by_name()

    table_tags = text_inside_bbox(xml_text, bbox_to_find)
    # print(table_tags)
    return None


def text_inside_bbox(xml_text, bbox_to_find):
    """

    :param xml_text: str                        | XML as a string or tag as a string
    :param bbox_to_find: tuple[float]           | (0, 0, 10, 10)
    :return: list[str]                          | The list of text inside the bbox_to_find
    """
    content_list = []
    char_index = 0
    while char_index <= len(xml_text) - 3:
        if xml_text[char_index:char_index + 4] == "bbox":
            bbox = get_bbox(char_index, xml_text)
            if check_nesting(bbox, bbox_to_find):
                tag = get_tag_by_attr_position(char_index, xml_text)
                char_index += len(tag) - 1
                tag_text = get_tag_text(tag)
                content_list.append(tag_text)
        char_index += 1
    return content_list


def tags_inside_bbox(xml_text, bbox_to_find):
    """

    :param xml_text: str                        | XML as a string or tag as a string
    :param bbox_to_find: tuple[float]           | (0, 0, 10, 10)
    :return: list[str]                          | The list of text inside the bbox_to_find
    """
    tags_list = []
    char_index = 0
    while char_index <= len(xml_text) - 3:
        if xml_text[char_index:char_index + 4] == "bbox":
            bbox = get_bbox(char_index, xml_text)
            if check_nesting(bbox, bbox_to_find):
                tag = get_tag_by_attr_position(char_index, xml_text)
                char_index += len(tag) - 1
                tags_list.append(tag)
        char_index += 1
    return tags_list


def parse_xml(xml_path):
    """
    return = {
        "xml_text": str,                                    \n
        "page_bbox": bbox,                                  \n
    }

    :param xml_path: str        | The path to XML file
    :return: dict               |
    """
    with open(xml_path, mode="r") as xml_file:
        xml_text = xml_file.read()

    # Finding page bbox
    page_bbox = None
    for char_index in range(len(xml_text) - 3):
        if xml_text[char_index:char_index + 4] == "bbox":
            bbox = get_bbox(char_index, xml_text)
            if (bbox[0] == 0) and (bbox[1] == 0):
                page_bbox = bbox
                break
            else:
                continue

    if page_bbox is None:
        print("[ERROR] xml_find > page_bbox is None")
        print("xml_text:", xml_text)
        raise ValueError

    return {"xml_text": xml_text, "page_bbox": page_bbox}


def convert_pdf_to_xml(file_path):
    """

    :param file_path: str       | Path to pdf file
    :return: str                | XML path
    """

    # Load the PDF
    pdf = pdfquery.PDFQuery(file_path)
    pdf.load()

    # Create XML path
    pdf_name = url_to_name(file_path)
    xml_name = pdf_name[:-3] + "xml"
    file_dir = url_parent(file_path)
    xml_path = f"{file_dir}{xml_name}"

    # Convert the pdf to XML
    pdf.tree.write(xml_path, pretty_print=False)

    return xml_path


def tblr_to_bbox(tblr_bbox, margin=0.005):
    """
    tblr_bbox = {
        "top": bbox,        \n
        "bottom": bbox,     \n
        "left": bbox,       \n
        "right": bbox,      \n
    }

    :param tblr_bbox: dict
    :param margin: float        | 0.01 -> 1%
    :return: list[float]
    """
    bbox = np.array(
        (
            float(tblr_bbox["left"][0]),
            float(tblr_bbox["bottom"][1]),
            float(tblr_bbox["right"][2]),
            float(tblr_bbox["top"][3])
        )
    )
    margin_diff = bbox * margin
    margin_diff[0] = margin_diff[0] * (-1)
    margin_diff[1] = margin_diff[1] * (-1)
    bbox = bbox + margin_diff

    return bbox


def main():
    pass


if __name__ == '__main__':

    main()
# TODO: rewrite as a OOP
import sys

import pytesseract
import numpy as np
import pandas as pd

# Custom imports
import general_methods as gm


# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====

...

# # ===== Base logic Methods ================================================================= Base logic Methods =====
...
# # ===== Base logic Methods ================================================================= Base logic Methods =====


def add_margin_to_ltrbbox(ltrbbox, margin):
    """
        Expanding the ltrbbox
            ltrbbox = [100, 100, 1000, 1000]    ->      ltrbbox = [99,   98, 1001, 1002]
            margin = [0.01, 0.02]               ->      margin  = [-1%, -2%,  +1%,  +2%]

    :param ltrbbox: list[float]   | [<left_coordinate>, <top_coordinate>, <right_coordinate>, <bottom_coordinate>]
    :param margin: list[float]    | [0.01, 0.02] -> margin_x = 1%, margin_y = 2%
    :return:
    """
    margin_x = margin[0]
    margin_y = margin[1]

    # width and height of ltrbbox
    x_len = ltrbbox[2] - ltrbbox[0]
    y_len = ltrbbox[3] - ltrbbox[1]

    # Margins for Y and X
    margin_y = y_len * margin_y
    margin_x = x_len * margin_x

    # Recalculating ltrbbox
    ltrbbox[0] = ltrbbox[0] - margin_x  # left
    ltrbbox[1] = ltrbbox[1] - margin_y  # top
    ltrbbox[2] = ltrbbox[2] + margin_x  # right
    ltrbbox[3] = ltrbbox[3] + margin_y  # bottom

    return ltrbbox


def get_data_df_inside_ltrbbox(ltrbbox, data_df, margin=None):
    """
            Getting DataFrame with rows whose coordinates are inside the ltrbbox
        :param ltrbbox: list[float]   | [<left_coordinate>, <top_coordinate>, <right_coordinate>, <bottom_coordinate>]
        :param data_df:               | DataFrame with columns ["left", "top", "width", "height", "right", "bottom", "text"]
        :param margin: list[float]    | [0.01, 0.02] -> margin_x = 1%, margin_y = 2%
        :return:
        """
    ltrbbox = [float(x) for x in ltrbbox]

    # Recalculating ltrbbox
    if margin is not None:
        ltrbbox = add_margin_to_ltrbbox(ltrbbox, margin)

    # Getting rows inside the ltrbbox
    df_to_return = pd.DataFrame()
    for index, row in data_df.iterrows():

        # Conditions
        if_left = float(row["left"]) > ltrbbox[0]
        if_top = float(row["top"]) > ltrbbox[1]
        if_right = float(row["right"]) < ltrbbox[2]
        if_bottom = float(row["bottom"]) < ltrbbox[3]

        if if_left and if_top and if_right and if_bottom:
            row = row.to_frame().T.reset_index(drop=True)
            df_to_return = pd.concat([df_to_return, row], ignore_index=True)

    return df_to_return


def get_text_inside_ltrbbox(ltrbbox, data_df, margin=None):
    """
        Getting list["text"] that inside the ltrbbox
    :param ltrbbox: list[float]   | [<left_coordinate>, <top_coordinate>, <right_coordinate>, <bottom_coordinate>]
    :param data_df:               | DataFrame with columns ["left", "top", "width", "height", "right", "bottom", "text"]
    :param margin: list[float]    | [0.01, 0.02] -> margin_x = 1%, margin_y = 2%
    :return:
    """

    ltrbbox = [float(x) for x in ltrbbox]

    # Recalculating ltrbbox
    if margin is not None:
        ltrbbox = add_margin_to_ltrbbox(ltrbbox, margin)

    # Getting list of text that is inside the box
    text_list = []
    for index, row in data_df.iterrows():

        # Conditions
        if_left = float(row["left"]) > ltrbbox[0]
        if_top = float(row["top"]) > ltrbbox[1]
        if_right = float(row["right"]) < ltrbbox[2]
        if_bottom = float(row["bottom"]) < ltrbbox[3]

        if if_left and if_top and if_right and if_bottom:
            text_list.append(row["text"])

    return text_list


def get_rb_columns(page_data_df):
    """
        Getting right and bottom coordinates for each row
    :param page_data_df:
    :return:
    """
    # Get names of columns
    start_columns_names = page_data_df.columns
    columns_names = []
    for col in start_columns_names:
        if col == "height":
            columns_names.extend(["height", "right", "bottom"])
        else:
            columns_names.append(col)

    # Calculating right and bottom coordinates
    df_to_return = pd.DataFrame([], columns=columns_names)
    rounding_value = min([int(x) for x in page_data_df.head()["height"]]) // 5 * 2
    for index, row in page_data_df.iterrows():
        row["right"] = int(row["left"]) + int(row["width"])
        row["top"] = int(row["top"]) // rounding_value * rounding_value
        row["bottom"] = int(row["top"]) + int(row["height"])
        row = row.to_frame().T.reset_index(drop=True)
        df_to_return = pd.concat([df_to_return, row], ignore_index=True)

    # Changing type of some columns
    types_dict = {col: "int32" for col in ["left", "top", "width", "height", "right", "bottom"]}
    df_to_return = df_to_return.astype(types_dict)

    return df_to_return


def ltrbbox_from_data_df_row(data_df_row):
    return [data_df_row["left"], data_df_row["top"], data_df_row["right"], data_df_row["bottom"]]


def find_near_words(ltrbbox, space_px_len, data_df, direction="RL"):
    """

    :param ltrbbox: list[float]   | [<left_coordinate>, <top_coordinate>, <right_coordinate>, <bottom_coordinate>]
    :param space_px_len: int      | length of space in pixels
    :param data_df:               | DataFrame with columns ["left", "top", "width", "height", "right", "bottom", "text"]
    :param direction:             | Direction of searching ["R", "L", "RL"]
    :return:
    """
    if direction.upper() == "L":
        ltrbbox[0] -= space_px_len
    elif direction.upper() == "R":
        ltrbbox[2] += space_px_len
    else:
        ltrbbox[0] -= space_px_len
        ltrbbox[2] += space_px_len


    # adding margin for Y direction
    ltrbbox = add_margin_to_ltrbbox(ltrbbox, margin=[0, 0.05])

    # Searching rows
    df_to_return = pd.DataFrame()
    for index, row in data_df.iterrows():

        # Conditions
        if_left = (row["left"] < ltrbbox[0]) and (row["right"] > ltrbbox[0])
        if_top = row["top"] > ltrbbox[1]
        if_right = (row["right"] > ltrbbox[2]) and (row["left"] < ltrbbox[2])
        if_bottom = row["bottom"] < ltrbbox[3]

        # row_ = row.to_frame().T.reset_index(drop=True)
        # print(ltrbbox, if_left, if_right)
        # print(row_)

        if if_top and if_bottom:
            if if_left or if_right:
                row = row.to_frame().T.reset_index(drop=True)
                df_to_return = pd.concat([df_to_return, row], ignore_index=True)

    return df_to_return


def collapse_all_data_df_rows(data_df):
    df_to_return = data_df.iloc[0]

    max_cols = ["right", "bottom"]
    for max_col in max_cols:
        df_to_return[max_col] = data_df[max_col].max()

    min_cols = ["left", "top"]
    for min_col in min_cols:
        df_to_return[min_col] = data_df[min_col].min()

    str_cols = ["text"]
    str_separator = " "
    for str_col in str_cols:
        str_cols_list = []
        for index, row in data_df.iterrows():
            if len(row[str_col]) > 0:
                str_cols_list.append(row[str_col])
        df_to_return[str_col] = str_separator.join(str_cols_list)

    df_to_return["height"] = df_to_return["bottom"] - df_to_return["top"]
    df_to_return["width"] = df_to_return["right"] - df_to_return["left"]

    df_to_return = df_to_return.to_frame().T.reset_index(drop=True)

    return df_to_return


def find_columns(table_data_df, space_px_len):

    # Start ltrbbox for finding first row
    min_left = min([x for x in table_data_df["left"]])
    min_top = min([x for x in table_data_df["top"]])
    max_right = max([x for x in table_data_df["right"]])
    max_bottom = max([x for x in table_data_df["bottom"]])
    table_height = max_bottom - min_top
    table_width = max_right - min_left
    # top_bot_step = table_height * 0.01 // 1
    top_bot_step = table_data_df["height"].head().sum() // len(table_data_df.head()) // 3
    left_right_step = table_width * 0.02 // 1
    fr_ltrbbox = [min_left, min_top, min_left, min_top]

    # Searching words inside the increasing box > bottom border += 1% of table height; right border += 1% of width
    columns_df = pd.DataFrame()
    # Moving from top to bottom
    while fr_ltrbbox[3] < max_bottom:
        fr_ltrbbox[3] += top_bot_step
        fr_ltrbbox[2] = min_left

        # Moving from left to right
        while fr_ltrbbox[2] < max_right:
            fr_ltrbbox[2] += left_right_step
            df_1 = get_data_df_inside_ltrbbox(fr_ltrbbox, table_data_df, margin=[0.01, 0.01])

            # If there is something then find words near
            if len(df_1) > 0:
                if not len(columns_df) > 0:
                    fr_ltrbbox[3] += top_bot_step * 2

                # Finding near words
                near_words_ltrbbox = ltrbbox_from_data_df_row(df_1.iloc[-1])
                column_df = find_near_words(near_words_ltrbbox, space_px_len, table_data_df, direction="R")
                while len(column_df) > 0:
                    row_df = pd.concat([df_1, column_df], ignore_index=True)
                    df_1 = collapse_all_data_df_rows(row_df)
                    near_words_ltrbbox = ltrbbox_from_data_df_row(df_1.iloc[-1])
                    column_df = find_near_words(near_words_ltrbbox, space_px_len, table_data_df, direction="R")

                columns_df = pd.concat([columns_df, df_1], ignore_index=True)
                fr_ltrbbox[0] = columns_df.iloc[-1]["right"]
            else:
                continue
        if len(columns_df) > 0:
            break

    return columns_df


def table_from_data_df(data_df: pd.DataFrame, margin=None):
    """

    :param data_df:               | DataFrame with columns ["left", "top", "width", "height", "right", "bottom", "text"]
    :param margin: list[float]    | [0.01, 0.02] -> margin_x = 1%, margin_y = 2%
    :return:
    """
    if margin is None:
        margin = [0.001, 0.002]

    data_df = data_df.sort_values(by=["top", "left"], ascending=True).reset_index(drop=True)

    # Calculating spaces between words
    single_char_indexes = data_df["text"].str.len() == 1
    single_char_df = data_df.loc[single_char_indexes]
    space_px_len = sum([x for x in single_char_df["width"].head(10)]) / len(single_char_df["width"].head(10)) * 1.3 // 1
    space_px_len = int(space_px_len)

    # Finding columns
    columns_df = find_columns(data_df, space_px_len)


    print(columns_df)
    sys.exit()

    # Calculating widths of columns ===================================================================================
    ...
    # # Calculating start tblr_bbox
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

    # # Searching tags inside the increasing bbox > bottom border -= 2.5% of top border coordinates; right border += 10%
    first_row = []
    # # Moving from top to bottom
    while bottom_bbox[1] > 0:
        bottom_bbox[1] -= bbox_to_find[3] * 0.025
        tblr_bbox.update({"bottom": bottom_bbox})
        # # # Moving from left to right
        while right_bbox[2] < bbox_to_find[2]:
            right_bbox[2] += bbox_to_find[2] * 0.1
            tblr_bbox.update({"right": right_bbox})
            bbox_to_find_first_row = tblr_to_bbox(tblr_bbox, margin=0.01)
            item_tags = tags_inside_bbox(xml_text, bbox_to_find_first_row)
            # # # # If there is any tag > append first_row
            if len(item_tags) > 0:
                for item in item_tags:
                    first_row.append(item)
                left_bbox = get_bbox(0, first_row[-1])
                left_bbox = [left_bbox[2], 0, 0, 0]
                tblr_bbox.update({"left": left_bbox})
        if len(first_row) > 0:
            break
        # # # Reset the right position (start position)
        right_bbox[2] = bbox_to_find[0]

    if len(first_row) == 0:
        print("\nfirst_row == []")
        return []

    # Unpack tags
    for item_index in range(len(first_row)):
        first_row[item_index] = unpack_tags(first_row[item_index])

    # Calculating width of columns
    ...
    # # Generate column parameters and place them in a list
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

    # # Finding the smaller left coordinate and the larger right coordinate
    for col_params, col_index in zip(list_of_col_params, range(len(list_of_col_params))):
        char_index = 0

        # # # Find bbox and associated tag
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

        # # #Rewrite column parameters
        col_width = col_params["right"] - col_params["left"]
        col_header_bbox = (
            col_params["left"],
            col_params["header_bbox"][1],
            col_params["right"],
            col_params["header_bbox"][3]
        )
        col_params.update(
            {
                "width": col_width,
                "header_bbox": col_header_bbox,
            }
        )
        list_of_col_params[col_index].update(col_params)

    # TODO: parse lost text ???
    ...
    # TODO: row/column alignment
    ...

    # Calculating heights of rows =====================================================================================
    ...
    # # Calculating bbox for find
    right_bbox = [x for x in list_of_col_params[0]["header_bbox"]]
    top_bbox = [x for x in list_of_col_params[0]["header_bbox"]]
    top_bbox[3] = top_bbox[1]
    bottom_bbox = [x for x in bbox_to_find]
    bottom_bbox[1] = float(top_bbox[1])
    left_bbox = [x for x in bbox_to_find]
    tblr_bbox = {
        "top": top_bbox,
        "bottom": bottom_bbox,
        "left": left_bbox,
        "right": right_bbox,
    }

    # # Searching tags inside the increasing bbox > bottom border -= 2.5% of top border coordinates
    first_col = []
    # # # Moving from top to bottom
    while bottom_bbox[1] > 0:
        bottom_bbox[1] -= bbox_to_find[3] * 0.015
        tblr_bbox.update({"bottom": bottom_bbox})
        bbox_to_find_first_col = tblr_to_bbox(tblr_bbox)
        item_tags = tags_inside_bbox(xml_text, bbox_to_find_first_col)
        # If there is any tag > append first_col
        if len(item_tags) > 0:
            for item in item_tags:
                first_col.append(item)
            top_bbox = get_bbox(0, first_col[-1])
            top_bbox = [0, 0, 0, top_bbox[1]]
            tblr_bbox.update({"top": top_bbox})

    if len(first_col) == 0:
        print("\nfirst_col == []")
        return []

    # Calculating heights of rows
    ...
    # # Generate rows parameters and place them in a list
    list_of_row_params = []
    for row_tag in first_col:
        row_header_bbox = get_bbox(0, row_tag)
        row_header_height = row_header_bbox[3] - row_header_bbox[1]
        row_middle_coord = row_header_bbox[1] + (row_header_height / 2)
        row_params = {
            "bottom": row_header_bbox[1],
            "top": row_header_bbox[3],
            "middle": row_middle_coord,
            "height": row_header_height,
            "header_bbox": row_header_bbox,
        }
        list_of_row_params.append(row_params)

    for row_param, row_index in zip(list_of_row_params, range(len(list_of_row_params))):
        if row_index < len(list_of_row_params) - 1:
            row_header_bottom = list_of_row_params[row_index + 1]["top"]
        else:
            row_header_bottom = bbox_to_find[1]
        row_header_height = row_param['top'] - row_header_bottom
        row_middle_coord = row_header_bottom + (row_header_height / 2)
        row_header_bbox = [
            row_param['header_bbox'][0],
            row_header_bottom,
            row_param['header_bbox'][2],
            row_param['header_bbox'][3]
        ]
        row_params = {
            "bottom": row_header_bbox[1],
            "middle": row_middle_coord,
            "height": row_header_height,
            "header_bbox": row_header_bbox,
        }
        list_of_row_params[row_index].update(row_params)

    # Getting table data ==============================================================================================
    table_data = [get_tag_text(x)[:-1] for x in first_row]
    table_data = [table_data]
    for row_params in list_of_row_params:
        row_items = []
        for column_params in list_of_col_params:
            top = row_params["top"]
            bottom = row_params["bottom"]
            left = column_params["left"]
            right = column_params["right"]
            tblr = {
                "left": left,
                "bottom": bottom,
                "right": right,
                "top": top,
            }
            bbox_to_find_item = tblr_to_bbox(tblr, margin_x=margin_x, margin_y=margin_y)
            tags = tags_inside_bbox(xml_text, bbox_to_find_item)

            # if tag is parent tag then skip
            item_string = ""
            for tag in tags:
                # if tag[-1] == "1":
                #     tag = unpack_tags(tag)
                item_string += get_tag_text(tag)[:-1]

            # # For debugging
            # if len(table_data) == 14:
            #     print("row:", len(table_data))
            #     print("col:", len(row_items))
            #     print("bbox_to_find_item:", bbox_to_find_item)
            #     print("item_string:", item_string)
            #     print(tags)
            #     print()

            row_items.append(item_string)

        table_data.append(row_items)

    # Create dataframe
    output_df = pd.DataFrame(
        table_data[1:],
        columns=table_data[0]
    )

    return output_df






def get_page_data_df(page_data):

    # Page recognition with tesseract
    data_array = np.array(page_data)
    page_as_str = pytesseract.image_to_data(data_array)
    page_as_str = gm.replace_chars(page_as_str)

    # Creating DataFrame from string
    page_data_array = [list(map(lambda x: x.upper(), j.split("\t"))) for j in [x for x in page_as_str.split("\n")]]
    page_data_df = pd.DataFrame(
        page_data_array[1:],
        columns=[x.lower() for x in page_data_array[0]]
    )
    page_data_df.iloc[0]["text"] = "page_size"

    # Drop all None or "" rows
    in_list = ['', "None", "NONE", None]
    page_data_df = page_data_df.loc[~page_data_df["text"].isin(in_list)].reset_index(drop=True)

    # Getting right and bottom coordinates for each row and rounding top coordinates
    page_data_df = get_rb_columns(page_data_df)

    return page_data_df


def main():
    pass


if __name__ == '__main__':

    main()
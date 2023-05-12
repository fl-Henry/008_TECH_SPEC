import sys

import pytesseract
import numpy as np
import pandas as pd

# Custom imports
import general_methods as gm


# # ===== General Methods ======================================================================= General Methods =====
...
# # ===== General Methods ======================================================================= General Methods =====


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
    # Creating names of columns list
    start_columns_names = page_data_df.columns
    columns_names = []
    for col in start_columns_names:
        if col == "height":
            columns_names.extend(["height", "right", "bottom"])
        else:
            columns_names.append(col)

    # Changing type of some columns
    types_dict = {col: "int32" for col in ["left", "top", "width", "height"]}
    page_data_df = page_data_df.astype(types_dict)

    page_data_df = page_data_df.sort_values(by=["top"], ascending=True).reset_index(drop=True)

    # rows bottom coordinates list // to round bottom coordinates and create a readable file structure
    bottom_list = [0]

    # average height of rows/words
    avg_height = sum([int(x) for x in page_data_df.tail(20)["height"]]) // len(page_data_df.tail(20)["height"])
    avg_height = avg_height * 1.2 // 2  # to comparison // 1.2 for include space between rows

    # Calculating bottom coordinates, adding to bottom_list or rounding by near coordinate
    page_row = pd.Series(page_data_df.iloc[0])
    page_row["right"] = int(page_row["left"]) + int(page_row["width"])
    page_row["bottom"] = int(page_row["top"]) + int(page_row["height"])
    df_to_return = pd.DataFrame([], columns=columns_names)
    for index, row in page_data_df.iterrows():
        if index == 0:
            continue
        row["right"] = int(row["left"]) + int(row["width"])
        bottom = int(row["top"]) + int(row["height"])

        # If newline then append bottom_list
        if bottom > bottom_list[-1] + avg_height:
            bottom_list.append(bottom)

        # Rounding bottom coordinate
        else:
            check_key = False
            for row_index in range(1, len(bottom_list)):
                if bottom_list[-row_index] + avg_height >= bottom > bottom_list[-(row_index + 1)] + avg_height:
                    bottom = bottom_list[-row_index]
                    check_key = True
                    break
            if not check_key:
                raise Exception(f"[ERROR] Rounding bottom coordinate > {check_key} > Rounding failed")

        row["bottom"] = bottom
        row = row.to_frame().T.reset_index(drop=True)
        df_to_return = pd.concat([df_to_return, row], ignore_index=True)

    df_to_return = df_to_return.sort_values(by=["bottom", "left"], ascending=True).reset_index(drop=True)
    df_to_return = pd.concat([page_row.to_frame().T, df_to_return], ignore_index=True)

    # Changing type of some columns
    types_dict = {col: "int32" for col in ["left", "top", "width", "height", "right", "bottom"]}
    df_to_return = df_to_return.astype(types_dict)

    return df_to_return


def ltrbbox_from_data_df_row(data_df_row):
    return [data_df_row["left"], data_df_row["top"], data_df_row["right"], data_df_row["bottom"]]


def find_near_words(ltrbbox, space_px_len, data_df, direction="R"):
    """

    :param ltrbbox: list[float]   | [<left_coordinate>, <top_coordinate>, <right_coordinate>, <bottom_coordinate>]
    :param space_px_len: int      | length of space in pixels
    :param data_df:               | DataFrame with columns ["left", "top", "width", "height", "right", "bottom", "text"]
    :param direction:             | Direction for searching ["R", "L"]
    :return:
    """

    in_ltrbbox = [*ltrbbox]
    if "L" in direction.upper():
        in_ltrbbox[0] = ltrbbox[0] - space_px_len
    else:
        in_ltrbbox[2] = ltrbbox[2] + space_px_len

    # adding margin for Y direction
    in_ltrbbox = add_margin_to_ltrbbox(in_ltrbbox, margin=[0, 0.05])

    # Searching rows
    df_to_return = pd.DataFrame()
    for index, row in data_df.iterrows():

        # Conditions
        if "L" in direction.upper():
            if_left = (row["left"] < in_ltrbbox[0]) and (row["right"] > in_ltrbbox[0])
        else:
            if_left = False
        if "R" in direction.upper():
            if_right = (row["right"] > in_ltrbbox[2]) and (row["left"] < in_ltrbbox[2])
        else:
            if_right = False
        if_top = row["top"] >= in_ltrbbox[1]
        if_bottom = row["bottom"] <= in_ltrbbox[3]

        if if_top and if_bottom:
            if if_left or if_right:
                row = row.to_frame().T.reset_index(drop=True)
                df_to_return = pd.concat([df_to_return, row], ignore_index=True)
                break

    return df_to_return


def find_all_near_words(df_1, table_data_df, space_px_len, direction="R"):
    """
        return df_1 with all words and recalculated left, right, width
    :param df_1:
    :param table_data_df:
    :param space_px_len:
    :param direction: str   | default "R" | ["R", "L", "LR"]
    :return:
    """
    if "L" in direction.upper():
        near_words_ltrbbox = ltrbbox_from_data_df_row(df_1.iloc[-1])
        row_df = find_near_words(near_words_ltrbbox, space_px_len, table_data_df, direction="L")

        while len(row_df) > 0:
            row_df = pd.concat([row_df, df_1], ignore_index=True)
            df_1 = collapse_all_data_df_rows(row_df)
            near_words_ltrbbox = ltrbbox_from_data_df_row(df_1.iloc[-1])
            row_df = find_near_words(near_words_ltrbbox, space_px_len, table_data_df, direction="L")

    if "R" in direction.upper():
        near_words_ltrbbox = ltrbbox_from_data_df_row(df_1.iloc[-1])
        row_df = find_near_words(near_words_ltrbbox, space_px_len, table_data_df, direction="R")
        while len(row_df) > 0:
            row_df = pd.concat([df_1, row_df], ignore_index=True)
            df_1 = collapse_all_data_df_rows(row_df)
            near_words_ltrbbox = ltrbbox_from_data_df_row(df_1.iloc[-1])
            row_df = find_near_words(near_words_ltrbbox, space_px_len, table_data_df, direction="R")

    return df_1


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
    in_list = ['', "None", "NONE", None, " "]
    page_data_df = page_data_df.loc[~page_data_df["text"].isin(in_list)].reset_index(drop=True)

    # Getting right and bottom coordinates for each row and rounding bottom coordinates
    page_data_df = get_rb_columns(page_data_df)

    return page_data_df


# # ===== Table parsing Methods =========================================================== Table parsing Methods =====
...
# # ===== Table parsing Methods =========================================================== Table parsing Methods =====
...
# TODO:
#    class Table:
#       class Cell [ltrbbox, data, type]
#       def as_dataframe
#       def as_array
#
# TODO: row/column alignment


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


def get_column_width(col,  space_px_len, table_data_df):
    left, right, width = col["left"], col["right"], col["width"]
    for index, row in table_data_df.iterrows():
        if_left = (row["left"] < left) and (row["right"] > left - space_px_len)
        if_right = (row["right"] > right) and (row["left"] < right + space_px_len)
        if_inside = (row["right"] < right) and (row["left"] > left)
        if_skip = "AMPARO" in row["text"]

        if (if_left or if_right or if_inside) and not if_skip:
            df_1 = find_all_near_words(row.to_frame().T, table_data_df, space_px_len, direction="RL")
            if left > df_1.iloc[0]["left"]:
                left = df_1.iloc[0]["left"]
            if right < df_1.iloc[0]["right"]:
                right = df_1.iloc[0]["right"]
    width = right - left
    return left, right, width


def recalculate_columns_params(columns_df, space_px_len, table_data_df):
    """
        Recalculating widths and right coordinates for each column
    :param columns_df:
    :param space_px_len:
    :param table_data_df:
    :return:
    """
    df_1 = pd.DataFrame()
    for index, col in columns_df.iterrows():
        col["left"], col["right"], col["width"] = get_column_width(col, space_px_len, table_data_df)
        if index < len(columns_df) - 1:
            if col["right"] > columns_df.iloc[index + 1]["left"]:
                col["right"] = columns_df.iloc[index + 1]["left"]
                col["width"] = col["right"] - col["left"]
        col = col.to_frame().T.reset_index(drop=True)
        df_1 = pd.concat([df_1, col], ignore_index=True)

    df_to_return = pd.DataFrame()
    df_to_return = pd.concat([df_to_return, df_1.iloc[0].to_frame().T.reset_index(drop=True)], ignore_index=True)
    for index, col in df_1.iterrows():
        if index < len(df_1) - 1:
            if col["right"] > df_1.iloc[index + 1]["left"]:
                df_1.iloc[index + 1]["left"] = col["right"]
                df_1.iloc[index + 1]["width"] = df_1.iloc[index + 1]["right"] - df_1.iloc[index + 1]["left"]
            col_next = df_1.iloc[index + 1].to_frame().T.reset_index(drop=True)
            df_to_return = pd.concat([df_to_return, col_next], ignore_index=True)

    return df_to_return


def find_columns(table_data_df, space_px_len):

    # Start ltrbbox for finding first row
    min_left = min([x for x in table_data_df["left"]])
    min_top = min([x for x in table_data_df["top"]])
    max_right = max([x for x in table_data_df["right"]])
    max_bottom = max([x for x in table_data_df["bottom"]])
    table_height = max_bottom - min_top
    table_width = max_right - min_left
    # top_bottom_step = table_height * 0.01 // 1
    top_bottom_step = table_data_df["height"].head().sum() // len(table_data_df.head()) // 3
    left_right_step = table_width * 0.02 // 1
    fr_ltrbbox = [min_left, min_top, min_left, min_top]

    # Searching words inside the increasing box > bottom border += 1% of table height; right border += 1% of width
    columns_df = pd.DataFrame()
    # Moving from top to bottom
    while fr_ltrbbox[3] < max_bottom:
        fr_ltrbbox[3] += top_bottom_step
        fr_ltrbbox[2] = min_left

        # Moving from left to right
        while fr_ltrbbox[2] < max_right:
            fr_ltrbbox[2] += left_right_step
            df_1 = get_data_df_inside_ltrbbox(fr_ltrbbox, table_data_df, margin=[0.01, 0.01])

            # If there is something then find words near
            if len(df_1) > 0:
                if not len(columns_df) > 0:
                    fr_ltrbbox[3] += top_bottom_step * 2

                # Finding all near words
                df_1 = find_all_near_words(df_1, table_data_df, space_px_len)

                columns_df = pd.concat([columns_df, df_1], ignore_index=True)
                fr_ltrbbox[0] = columns_df.iloc[-1]["right"]
            else:
                continue
        if len(columns_df) > 0:
            break

    # Recalculating widths and right coordinates for each column
    columns_df = recalculate_columns_params(columns_df, space_px_len, table_data_df)

    return columns_df


def get_row_top(top, table_data_df):
    for index, row in table_data_df.iterrows():
        if float(row["top"]) <= top <= float(row["bottom"]):
            top = float(row["top"])
    return top


def recalculate_rows_params(rows_df, table_ltrbbox, table_data_df):
    """
        Recalculating heights and bottom coordinates for each row
    :param rows_df:
    :param table_ltrbbox:
    :param table_data_df:
    :return:
    """

    df_to_find_top = pd.DataFrame()
    for index, row in rows_df.iterrows():
        row["top"] = get_row_top(row["top"], table_data_df)
        row = row.to_frame().T.reset_index(drop=True)
        df_to_find_top = pd.concat([df_to_find_top, row], ignore_index=True)

    rows_df = df_to_find_top
    df_to_return = pd.DataFrame()
    for index, row in rows_df.iterrows():
        if index + 1 < len(rows_df):
            row["bottom"] = rows_df.iloc[index + 1]["top"]
        else:
            row["bottom"] = table_ltrbbox[3]

        row["height"] = row["bottom"] - row["top"]
        row = row.to_frame().T.reset_index(drop=True)
        df_to_return = pd.concat([df_to_return, row], ignore_index=True)

    return df_to_return


def find_rows(table_data_df, space_px_len):

    # Start ltrbbox for finding first column
    min_left = min([x for x in table_data_df["left"]])
    min_top = min([x for x in table_data_df["top"]])
    max_right = max([x for x in table_data_df["right"]])
    max_bottom = max([x for x in table_data_df["bottom"]])
    table_height = max_bottom - min_top
    table_width = max_right - min_left
    # top_bottom_step = table_height * 0.01 // 1
    top_bottom_step = table_data_df["height"].head().sum() // len(table_data_df.head()) // 3
    left_right_step = table_width * 0.02 // 1
    fr_ltrbbox = [min_left, min_top, min_left, min_top]

    # Searching words inside the increasing box
    rows_df = pd.DataFrame()
    # Moving from top to bottom
    while fr_ltrbbox[3] < max_bottom:
        fr_ltrbbox[3] += top_bottom_step
        fr_ltrbbox[2] = min_left

        # Moving from left to right
        while fr_ltrbbox[2] < max_right:
            fr_ltrbbox[2] += left_right_step
            
            # Checking/getting anything inside the ltrbbox
            df_1 = get_data_df_inside_ltrbbox(fr_ltrbbox, table_data_df, margin=[0.01, 0.01])

            # If there is something then find words near
            if len(df_1) > 0:

                # Finding all near words
                df_1 = find_all_near_words(df_1, table_data_df, space_px_len)

                rows_df = pd.concat([rows_df, df_1], ignore_index=True)
                fr_ltrbbox[1] = rows_df.iloc[-1]["bottom"]
                fr_ltrbbox[3] = rows_df.iloc[-1]["bottom"]
                fr_ltrbbox[2] = rows_df.iloc[-1]["right"]

                # Moving from top to bottom
                while fr_ltrbbox[3] < max_bottom:
                    fr_ltrbbox[3] += top_bottom_step

                    # Checking/getting anything inside the ltrbbox and near the ltrbbox
                    df_1 = get_data_df_inside_ltrbbox(fr_ltrbbox, table_data_df, margin=[0.01, 0.01])
                    row_df = find_near_words(fr_ltrbbox, space_px_len, table_data_df, direction="R")

                    # If there is anything inside or near the ltrbbox then collapse it and find all near words
                    if (len(row_df) > 0) or (len(df_1) > 0):
                        row_df = pd.concat([df_1, row_df], ignore_index=True)
                        df_1 = collapse_all_data_df_rows(row_df)

                        # Finding all near words
                        df_1 = find_all_near_words(df_1, table_data_df, space_px_len)

                        rows_df = pd.concat([rows_df, df_1], ignore_index=True)
                        fr_ltrbbox[1] = rows_df.iloc[-1]["bottom"]
                break

            else:
                continue

        if len(rows_df) > 0:
            break

    # Recalculating heights and bottom coordinates for each row
    rows_df = recalculate_rows_params(rows_df, [min_left, min_top, max_right, max_bottom], table_data_df)

    return rows_df


def get_table_data(columns_df, rows_df, data_df):
    df_to_return = columns_df["text"].to_frame().T.reset_index(drop=True)

    for row_index, row in rows_df[1:].iterrows():
        df_row = pd.Series()
        for col_index, col in columns_df.iterrows():
            ltrbbox = [col["left"], row["top"], col["right"], row["bottom"]]
            text = get_text_inside_ltrbbox(ltrbbox, data_df, margin=[0.02, 0.02])
            if len(text) > 0:
                text = " ".join(text)
            else:
                text = ""
            df_row[col_index] = text
        df_row = df_row.to_frame().T
        df_to_return = pd.concat([df_to_return, df_row], ignore_index=True)

    return df_to_return


def table_from_data_df(data_df: pd.DataFrame):
    """

    :param data_df:               | DataFrame with columns ["left", "top", "width", "height", "right", "bottom", "text"]
    :param margin: list[float]    | [0.01, 0.02] -> margin_x = 1%, margin_y = 2%
    :return:
    """
    # Calculating spaces between words
    single_char_indexes = data_df["text"].str.len() == 1
    single_char_df = data_df.loc[single_char_indexes]
    if len(single_char_df) > 0:
        space_px_len = sum([x for x in single_char_df["width"].head(10)]) / len(single_char_df["width"].head(10)) * 1.3 // 1
    else:
        space_px_len = data_df["width"].head(1)[0] // len(data_df["text"].head(1)[0])
    space_px_len = int(space_px_len)

    # Finding columns
    columns_df = find_columns(data_df, space_px_len)

    # Finding rows
    rows_df = find_rows(data_df, space_px_len)

    # Getting data for each cell
    table_df = get_table_data(columns_df, rows_df, data_df)

    return table_df


def main():
    pass


if __name__ == '__main__':
    main()

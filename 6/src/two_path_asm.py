# 引数の名前のファイルを開き、各行をリストに入れ
import os


def read_file_to_list(filename):
    if not os.path.exists(filename):
        print(f"File {filename} does not exist.")
        return []
    with open(filename, "r") as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]


# hackの標準シンボルの辞書を用意する
standard_symbols = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,  # 0x4000
    "KBD": 24576,  # 0x6000
}


# リストを引数にして、各要素をリストに入れなおす。ただし、各行に以下を行う
# 1. 全ての空白を削除
# 2. //で始まる要素はリストに入れなおさない
# 3. (で始まり、)で終わる要素はリストに入れなおさないが、()の中身を、今のリストの番号＋１をキーとしたリストの要素に入れえる。
def process_list(input_list):
    noCommentAndNoSpaceList = []
    output_list = []
    parentheses_dict = standard_symbols
    symbol_count = 0

    for index, item in enumerate(input_list):
        # 空白を削除
        item = item.replace(" ", "")

        # //で始まる要素は無視
        if item.startswith("//"):
            continue
        noCommentAndNoSpaceList.append(item)
    for index, item in enumerate(noCommentAndNoSpaceList):
        # ()で始まり、)で終わる要素は無視
        if item.startswith("(") and item.endswith(")"):
            parentheses_dict[item[1:-1]] = index - symbol_count  # ()の中身を保存
            symbol_count += 1
            continue
        output_list.append(item)

    return output_list, parentheses_dict


def path1(filename):
    input_list = read_file_to_list(filename)
    if not input_list:
        return [], {}
    output_list, parentheses_dict = process_list(input_list)
    return output_list, parentheses_dict


def path2(path1List, parentheses_dict):
    # シンボル用の辞書を作成する
    # @で始まる要素に対して、parentheses_dictのキーに対応する場合は、path1listに対応する値を入れなおす。
    # @で始まるが、parentheses_dictのキーに対応しない場合は、シンボルの辞書に追加する。ただし、辞書の値は16から始まる連番とする。
    symbol_dict = {}
    next_value = 16
    for i, item in enumerate(path1List):
        if item.startswith("@"):
            key = item[1:]  # @を除去
            if key in parentheses_dict:
                # parentheses_dictのキーに対応する場合は、path1Listに対応する値を入れなおす
                path1List[i] = "@" + str(parentheses_dict[key])
            else:
                # シンボルの辞書に追加
                if key not in symbol_dict and not key.isdigit():
                    # シンボルがまだ辞書にない場合、次の値を割り当てる
                    symbol_dict[key] = next_value
                    next_value += 1
    print(symbol_dict)
    return path1List, symbol_dict

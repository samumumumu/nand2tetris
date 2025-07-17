def initialise(filename):
    # ファイルをを読み込み、各行をリストに格納する
    # 各行の最初の空白は削除する
    # ファイル名は引数で指定する
    with open(filename, "r") as file:
        lines = file.readlines()
    # 各行の最初の空白を削除し、空でない行のみをリストに格納
    return [line.lstrip() for line in lines if line.strip()]


def hasMoreLines(lines, index):
    # 指定されたインデックスがリストの範囲内かどうかを確認
    return index < len(lines)


def advance(lines, index):
    if hasMoreLines(lines, index):
        # 現在のインデックスの行を取得し、インデックスを1つ進める
        current_line = lines[index]
        index += 1
        return current_line, index


# コマンドタイプのリスト
COMMAND_TYPES = {
    "push": "C_PUSH",
    "pop": "C_POP",
    "add": "C_ARITHMETIC",
    "sub": "C_ARITHMETIC",
    "neg": "C_ARITHMETIC",
    "eq": "C_ARITHMETIC",
    "gt": "C_ARITHMETIC",
    "lt": "C_ARITHMETIC",
    "and": "C_ARITHMETIC",
    "or": "C_ARITHMETIC",
    "not": "C_ARITHMETIC",
    # TODO:今後追加予定
}


# 引数はvmファイルの1行
def commandType(line):
    # コマンドの種類を判定して、対応するコマンドタイプを返す
    # コマンドの最初の空白までの部分を取得
    command = line.split()
    # 対応するコマンドタイプを返す
    if command[0] in COMMAND_TYPES:
        return COMMAND_TYPES[command[0]]
    else:
        raise ValueError(f"Unknown command: {command[0]}")


def arg1(line):
    if commandType(line) == "C_ARITHMETIC":
        # C_ARITHMETICコマンドの場合は、引数はコマンド自体
        return line.split()[0]
    else:
        split = line.split()
        return split[1]


def arg2(line):
    if commandType(line) in ["C_PUSH", "C_POP"]:
        # C_PUSHまたはC_POPコマンドの場合は、2番目の引数を返す
        return line.split()[2]

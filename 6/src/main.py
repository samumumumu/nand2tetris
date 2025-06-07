# 引数の名前のファイルを開き、各行をリストに入れ
from two_path_asm import path1, path2
from code import convert_to_binary
import sys


def main():
    if len(sys.argv) < 2:
        print("引数を指定してください")
        sys.exit(1)

    argument = sys.argv[1]
    path1List, path1Dict = path1(argument)
    path2List, path2dict = path2(path1List, path1Dict)
    binary = convert_to_binary(path2List, path2dict)
    # リストをファイルに出力する。各要素が各行に出力されるようにする。
    output_file = argument.replace(".asm", ".hack")
    with open(output_file, "w") as f:
        for line in binary:
            f.write(line + "\n")


if __name__ == "__main__":
    main()

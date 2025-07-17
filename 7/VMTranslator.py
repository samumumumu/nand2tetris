import sys, os
from parser import *
from codeWriter import *


def main():
    if len(sys.argv) < 2:
        print("引数を指定してください")
        sys.exit(1)
    argument = sys.argv[1]
    asmCode = initialiseAsm([])

    input_list = process_list(initialise(argument))

    for arithmeticIndex, line in enumerate(input_list):
        asmCode.append(f"// {line}")
        Type = commandType(line)
        argument1 = arg1(line)
        argument2 = arg2(line)
        if Type == "C_PUSH" or Type == "C_POP":
            writePushPop(Type, argument1, argument2, asmCode)
        else:
            writeArithmetic(argument1, arithmeticIndex, asmCode)
    end(asmCode)
    output_file = argument.replace(".vm", ".asm")
    with open(output_file, "w") as f:
        for line in asmCode:
            f.write(line + "\n")


def process_list(input_list):
    output_list = []

    for index, item in enumerate(input_list):
        # //で始まる要素は無視
        if item.startswith("//") or not item.strip():
            continue
        output_list.append(item)
    # for index, item in enumerate(noCommentAndNoSpaceList):
    #     # ()で始まり、)で終わる要素は無視
    #     if item.startswith("(") and item.endswith(")"):
    #         parentheses_dict[item[1:-1]] = index - symbol_count  # ()の中身を保存
    #         symbol_count += 1
    #         continue
    #     output_list.append(item)

    return output_list


def initialiseAsm(asmCode):
    # asmCode.append("@1000")
    # asmCode.append("D=A")
    # asmCode.append("@SP")
    # asmCode.append("M=D")
    # asmCode.append("@2000")
    # asmCode.append("D=A")
    # asmCode.append("@LCL")
    # asmCode.append("M=D")
    # asmCode.append("@3000")
    # asmCode.append("D=A")
    # asmCode.append("@ARG")
    # asmCode.append("M=D")
    # asmCode.append("@4000")
    # asmCode.append("D=A")
    # asmCode.append("@THIS")
    # asmCode.append("M=D")
    # asmCode.append("@5000")
    # asmCode.append("D=A")
    # asmCode.append("@THAT")
    # asmCode.append("M=D")
    return asmCode


def end(asmCode):
    asmCode.append("(END)")
    asmCode.append("@END")
    asmCode.append("0;JMP")


if __name__ == "__main__":
    main()

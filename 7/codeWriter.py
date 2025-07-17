from parser import *


# push,popかどうかの判断はVMtransratorに任せることにして、ここではpush,popのコードが来たことにする
def writePushPop(commandType, segment, index, vmCommand):
    if commandType == "C_PUSH":
        if segment == "constant":
            vmCommand.append(f"@{index}")
            vmCommand.append("D=A")
        elif segment in ["argument", "local", "this", "that"]:
            if segment == "argument":
                vmCommand.append("@ARG")
            if segment == "local":
                vmCommand.append("@LCL")
            if segment == "this":
                vmCommand.append("@THIS")
            if segment == "that":
                vmCommand.append("@THAT")
            vmCommand.append("D=M")
            vmCommand.append(f"@{index}")
            vmCommand.append(f"D=D+A")
            vmCommand.append("A=D")
            vmCommand.append("D=M")
        else:
            if segment == "temp":
                vmCommand.append(f"@{5+int(index)}")
            if segment == "pointer":
                vmCommand.append(f"@{3+int(index)}")
            if segment == "static":
                vmCommand.append(f"@static.{index}")
            vmCommand.append("D=M")
        # spの値の番地にアクセス
        vmCommand.append("@SP")
        vmCommand.append("A=M")
        vmCommand.append("M=D")
        # spの値を＋１する
        vmCommand.append("@SP")
        vmCommand.append("M=M+1")
    if commandType == "C_POP":
        if segment in ["argument", "local", "this", "that"]:
            if segment == "argument":
                vmCommand.append("@ARG")
            if segment == "local":
                vmCommand.append("@LCL")

            if segment == "this":
                vmCommand.append("@THIS")
            if segment == "that":
                vmCommand.append("@THAT")

            vmCommand.append("D=M")
            vmCommand.append(f"@{index}")
            vmCommand.append(f"D=D+A")
            vmCommand.append("@R13")
            vmCommand.append("M=D")

            vmCommand.append("@SP")
            vmCommand.append("M=M-1")
            vmCommand.append("A=M")
            vmCommand.append("D=M")

            vmCommand.append("@R13")
            vmCommand.append("A=M")
            vmCommand.append("M=D")
        else:
            vmCommand.append("@SP")
            vmCommand.append("M=M-1")
            vmCommand.append("A=M")
            vmCommand.append("D=M")
            if segment == "pointer":
                vmCommand.append(f"@{3+int(index)}")
            if segment == "temp":
                vmCommand.append(f"@{5+int(index)}")
            if segment == "static":
                vmCommand.append(f"@static.{index}")
            vmCommand.append("M=D")

    return vmCommand


def writeArithmetic(command, index, vmCommand):
    if command == "neg":
        popForArithmetic(vmCommand)
        vmCommand.append("D=M")
        vmCommand.append("D=-D")
    elif command == "not":
        popForArithmetic(vmCommand)
        vmCommand.append("D=M")
        vmCommand.append("D=!D")
    elif command in ["add", "sub", "and", "or"]:
        popForArithmetic(vmCommand)
        vmCommand.append("D=M")
        popForArithmetic(vmCommand)
        vmCommand.append(f"D=M{arithmeticDict[command]}D")
    else:
        popForArithmetic(vmCommand)
        vmCommand.append("D=M")
        popForArithmetic(vmCommand)
        vmCommand.append("D=M-D")
        createCompare(command, index, vmCommand)
    # 値をpushする共通の処理
    vmCommand.append("@SP")
    vmCommand.append("A=M")
    vmCommand.append("M=D")
    vmCommand.append("@SP")
    vmCommand.append("M=M+1")


def createCompare(command, index, vmCommand):
    if command == "eq":
        jmp = "D;JEQ"
    if command == "lt":
        jmp = "D;JLT"
    if command == "gt":
        jmp = "D;JGT"
    upperCommand = command.upper()
    vmCommand += [
        f"@{upperCommand}TRUE{index}",
        jmp,
        f"({upperCommand}FALSE{index})",
        "D=0",
        f"@{upperCommand}END{index}",
        "0;JMP",
        f"({upperCommand}TRUE{index})",
        "D=-1",
        f"({upperCommand}END{index})",
    ]


# ポップした値はDに格納してないので注意
def popForArithmetic(vmCommand):
    vmCommand.append("@SP")
    vmCommand.append("M=M-1")
    vmCommand.append("A=M")


arithmeticDict = {
    # 各算術論理コマンドに対応する演算子の辞書
    "add": "+",
    "sub": "-",
    # "neg": "-",
    # "eq": "==",
    # "gt": ">",
    # "lt": "<",
    "and": "&",
    "or": "|",
    # "not": "Not"
}

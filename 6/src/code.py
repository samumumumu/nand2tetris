# hackアセンブラのC命令の辞書を作る
# acccccc
COMP_COMMAND = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101",
}
# dest命令の辞書
DEST_COMMAND = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111",
}
# jump命令の辞書
JUMP_COMMAND = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


# hackの命令のリストとシンボルテーブルを受け取り、各命令をバイナリに変換する関数
def convert_to_binary(hack_commands, symbol_table):
    binary_commands = []
    for command in hack_commands:
        if command.startswith("@"):

            # A命令
            address = command[1:]

            if address.isdigit():
                binary_commands.append("0" + f"{int(address):015b}")
            else:
                if address not in symbol_table:
                    # エラーを出力する
                    raise ValueError(f"Undefined symbol: {address}")
                binary_commands.append("0" + f"{symbol_table[address]:015b}")
        else:
            # C命令
            dest, comp, jump = "null", "0", "null"
            if "=" in command:
                dest, comp = command.split("=")
            elif ";" in command:
                comp, jump = command.split(";")
            else:
                comp = command

            comp_code = COMP_COMMAND.get(comp, "0000000")
            dest_code = DEST_COMMAND.get(dest, "000")
            jump_code = JUMP_COMMAND.get(jump, "000")

            binary_commands.append(f"111{comp_code}{dest_code}{jump_code}")

    return binary_commands

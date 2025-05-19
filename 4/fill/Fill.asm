// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.
@n
M=0
(LOOP)
@KBD
D=M
@WHITE
D;JEQ
@n
D=M
@SCREEN
A=D+A
M=-1
@n
M=M+1
@LOOP
0;JMP
(WHITE)
@n
//n<0の時はそこから引かない
D=M
@LOOP
D;JLT
@SCREEN
A=D+A
M=0
@n
M=M-1
@LOOP
0;JMP

@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@THIS
D=D+A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
@THAT
D=D+M
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@THAT
D=D+M
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

@0
D=A
@ARG
D=D+M
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
(MAIN_LOOP_START)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
@COMPUTE_ELEMENT
D;JNE
@END_PROGRAM
0;JMP
(COMPUTE_ELEMENT)
@0
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D

@2
D=A
@THAT
D=D+M
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
@1
D=A
@THIS
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M+D

@1
D=A
@THIS
D=D+A
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

@0
D=A
@ARG
D=D+M
@13
M=D
@SP
M=M-1
A=M
D=M
@13
A=M
M=D
@MAIN_LOOP_START
0;JMP
(END_PROGRAM)
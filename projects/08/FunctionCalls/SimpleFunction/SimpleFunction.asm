(SimpleFunction.test)
@2
D=A
@i
M=D
D=M
@SimpleFunction.test.2
D;JEQ
(SimpleFunction.test..2)
@SP
A=M
M=0
@SP
D=M
D=D+1
M=D
@i
D=M
D=D-1
M=D
@SimpleFunction.test..2
D;JNE
(SimpleFunction.test.2)
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
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

@SP
A=M-1
M=!M

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
M=M+D

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
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D

@LCL
D=M
@FRAME
M=D
@FRAME
D=M
@5
D=D-A
A=D
D=M
@RET
M=D
@SP
D=M
D=D-1
A=D
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@FRAME
D=M
D=D-1
A=D
D=M
@THAT
M=D
@FRAME
D=M
@2
D=D-A
A=D
D=M
@THIS
M=D
@FRAME
D=M
@3
D=D-A
A=D
D=M
@ARG
M=D
@FRAME
D=M
@4
D=D-A
A=D
D=M
@LCL
M=D
@RET
A=M
0;JMP

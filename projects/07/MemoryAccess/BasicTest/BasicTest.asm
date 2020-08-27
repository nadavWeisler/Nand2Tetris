@256
D=A
@0
M=D
// Push ret address
@BOOTSTRAP_RETURN_ADDRESS$ret.1
D=A
@0
A=M
M=D
@0
M=M+1
// Push LCL
@1
D=M
@0
A=M
M=D
@0
M=M+1
// Push ARG
@2
D=M
@0
A=M
M=D
@0
M=M+1
// Push THIS
@3
D=M
@0
A=M
M=D
@0
M=M+1
// Push THAT
@4
D=M
@0
A=M
M=D
@0
M=M+1
// ARG = SP  -5 -nARGS
@0
D=M
@5
D=D-A
@0
D=D-A
@2
M=D
// LCL = SP
@0
D=M
@1
M=D
@Sys.init
0;JMP
(BOOTSTRAP_RETURN_ADDRESS$ret.1)
// Push
@10

D=A
@0
A=M
M=D
@0
M=M+1
// Pop
@1
D=M
@0

D=A+D
@1
M=D
@0
M=M-1
@0
A=M
D=M
@1
A=M
M=D
@1
D=M
@0

D=D-A
@1
M=D
// Push
@21

D=A
@0
A=M
M=D
@0
M=M+1
// Push
@22

D=A
@0
A=M
M=D
@0
M=M+1
// Pop
@2
D=M
@2

D=A+D
@2
M=D
@0
M=M-1
@0
A=M
D=M
@2
A=M
M=D
@2
D=M
@2

D=D-A
@2
M=D
// Pop
@2
D=M
@1

D=A+D
@2
M=D
@0
M=M-1
@0
A=M
D=M
@2
A=M
M=D
@2
D=M
@1

D=D-A
@2
M=D
// Push
@36

D=A
@0
A=M
M=D
@0
M=M+1
// Pop
@3
D=M
@6

D=A+D
@3
M=D
@0
M=M-1
@0
A=M
D=M
@3
A=M
M=D
@3
D=M
@6

D=D-A
@3
M=D
// Push
@42

D=A
@0
A=M
M=D
@0
M=M+1
// Push
@45

D=A
@0
A=M
M=D
@0
M=M+1
// Pop
@4
D=M
@5

D=A+D
@4
M=D
@0
M=M-1
@0
A=M
D=M
@4
A=M
M=D
@4
D=M
@5

D=D-A
@4
M=D
// Pop
@4
D=M
@2

D=A+D
@4
M=D
@0
M=M-1
@0
A=M
D=M
@4
A=M
M=D
@4
D=M
@2

D=D-A
@4
M=D
// Push
@510

D=A
@0
A=M
M=D
@0
M=M+1
// Pop
@0
M=M-1
@0
A=M
D=M
@11
M=D
// Push
@1
D=M
@0

A=D+A
D=M
@0
A=M
M=D
@0
M=M+1
// Push
@4
D=M
@5

A=D+A
D=M
@0
A=M
M=D
@0
M=M+1
// Push
@2
D=M
@1

A=D+A
D=M
@0
A=M
M=D
@0
M=M+1
// Push
@3
D=M
@6

A=D+A
D=M
@0
A=M
M=D
@0
M=M+1
// Push
@3
D=M
@6

A=D+A
D=M
@0
A=M
M=D
@0
M=M+1
// Push
@11
D=M
@0
A=M
M=D
@0
M=M+1

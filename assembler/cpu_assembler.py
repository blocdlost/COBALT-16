# ASSEMBLER FOR CUSTOM 16 BIT CPU (SPOCsys16) ASSEMBLY LANGUAGE (SPAsm)
#
# MOV ART LGC JMP IDC CAP SHF MEM DSP | END

inserror = " [ERROR] Incorrect instruction: opCodeError "                  #opcode is not recognized
lenerror = " [ERROR] Incorrect instruction: lengthError "                  #the length of the line itself falls out of a possible instruction boundary
argerror = " [ERROR] Incorrect instruction argument(s): argumentError "    #general argument is incorrectly given
regerror = " [ERROR] Incorrect instruction argument(s): registerError "    #the register argument is not recognized
valerror = " [ERROR] Incorrect instruction argument(s): valueError "       #the value given in the argument reaches beyond its bitlimit

errorList = []
errors = []

def register(reg):
    if reg == "rax":
        return "b0000"
    elif reg == "rbx":
        return "b0001"
    elif reg == "rcx":
        return "b0010"
    elif reg == "rdx":
        return "b0011"
    elif reg == "r1x":
        return "b0100"
    elif reg == "r2x":
        return "b0101"
    elif reg == "r3x":
        return "b0110"
    elif reg == "r4x":
        return "b0111"
    elif str.isdecimal(reg) == True or reg[0:2] == "0b" or reg[0:2] == "0x":
        return reg
    else:
        return "N/A"

def hex2dec(num):
    for q in range(10):
        if num == str(q):
            return str(num)
    if num == "A":
        return "10"
    elif num == "B":
        return "11"
    elif num == "C":
        return "12"
    elif num == "D":
        return "13"
    elif num == "E":
        return "14"
    elif num == "F":
        return "15"
    else:
        return "N/A"

def exactbit(val, bits):
    val = int(val)
    val = bin(val)[2:len(bin(val))]
    val = (bits-len(val))*"0"+str(val)
    return val

rawFile = open("raw.txt", "r")
rawLine = rawFile.readline()

encodedFile = open("encoded.txt", "w")

lineNo = 0

while rawLine:

    mnemonic = rawLine.strip()
    comment = mnemonic.find("#")    #comment deletion
    if comment != -1:
        mnemonic = mnemonic[0:comment-1]

    #print(lineNo, mnemonic)


    line = mnemonic
    inst = line[0:3]
    length = len(line)
    contents = line.split()

    if inst == "MOV":       #move instruction: 0, 0000                      MOV rg1 rg2; MOV rg1 val
        if length < 9:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"

        else:
            movDest = register(line[4:7])
            movMove = register(line[8:length])
            movMoveVal = 0

            if movMove[0:2] == "0b": #if given value is binary
                for i in range(len(movMove[2:len(movMove)])):
                    if int(movMove[-(i+1)]) != 0 and int(movMove[-(i+1)]) != 1: #incorrect digit
                        movMoveVal = "N/A"
                        break
                    else:
                        bit = int(movMove[-(i+1)])*(2**i)
                        movMoveVal += bit
                movMove = movMoveVal

            elif movMove[0:2] == "0x": #if given value is hexadecimal
                for i in range(len(movMove[2:len(movMove)])):
                    if hex2dec(movMove[-(i+1)]) == "N/A": #incorrect digit
                        movMoveVal = "N/A"
                        break
                    else:
                        hexa = int(hex2dec(movMove[-(i+1)]))*(16**i)
                        movMoveVal += hexa
                movMove = movMoveVal

            movMove = str(movMove)

            if movMove == "N/A" and movMoveVal == "N/A":
                errors.append(str(lineNo+1)+valerror+"\n")     #value is incorrectly encoded; binary/hexadecimal setting uses wrong digits
                code = "N/A"
            elif movDest == "N/A" or movMove == "N/A" or str.isdecimal(movDest):
                errors.append(str(lineNo+1)+regerror+"\n")
                code = "N/A"
            elif str.isdecimal(movMove) == True and int(movMove) > 65535:
                errors.append(str(lineNo+1)+valerror+"\n")     #value is over 16 bits long
                code = "N/A"
            elif str.isdecimal(movMove) == True:
                movMove = exactbit(movMove, 16)
                code = "0000"+"1"+str(movDest)[1:5]+str(movMove)+"0000000"
            elif str.isdecimal(movMove) == False:
                code = "0000"+"0"+str(movDest)[1:5]+str(movMove)[1:5]+"0000000000000000000"

    elif inst == "ART":     #arithmetic instruction: 1, 0001                ART mth rg1 rg2
        if length != 15:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            artIns = line[4:7]
            artDest = line[8:11]
            artOp = line[12:15]

            if artIns == "add":
                artIns = "00"
            elif artIns == "sub":
                artIns = "01"
            elif artIns == "mul":
                artIns = "10"
            elif artIns == "div":
                artIns = "11"
            else:
                artIns = "N/A"
            artDest = register(artDest)
            artOp = register(artOp)

            if artIns == "N/A":
                errors.append(str(lineNo+1)+argerror+"\n")
                code = "N/A"
            elif artDest == "N/A" or artOp == "N/A" or str.isdecimal(artDest) or str.isdecimal(artOp):
                errors.append(str(lineNo+1)+regerror+"\n")
                code = "N/A"
            else:
                code = "0001"+artIns+artDest[1:5]+artOp[1:5]+"000000000000000000"

    elif inst == "LGC":     #logic instruction: 2, 0010                     LGC lgc rg1 rg2; LGC not reg
        if length != 15 and length != 11:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            lgcIns = line[4:7]
            lgcDest = line[8:11]
            lgcOp = line[12:15]

            if lgcIns == "and":
                lgcIns = "00"
            elif lgcIns == "_or":
                lgcIns = "01"
            elif lgcIns == "xor":
                lgcIns = "10"
            elif lgcIns == "not":
                lgcIns = "11"
            else:
                lgcIns = "N/A"
            lgcDest = register(lgcDest)
            lgcOp = register(lgcOp)

            if lgcIns == "N/A":
                errors.append(str(lineNo+1)+argerror+"\n")
                code = "N/A"
            elif lgcOp != "N/A" and lgcIns == "11":
                errors.append(str(lineNo+1)+argerror+"\n")
                code = "N/A"
            elif lgcOp == "N/A" and lgcIns == "11":
                code = "0010"+lgcIns+lgcDest[1:5]+"0000000000000000000000"
            elif lgcDest == "N/A" or lgcOp == "N/A" or str.isdecimal(lgcDest) or str.isdecimal(lgcOp):
                errors.append(str(lineNo+1)+regerror+"\n")
                code = "N/A"
            else:
                code = "0010"+lgcIns+lgcDest[1:5]+lgcOp[1:5]+"000000000000000000"

    elif inst == "JMP":     #process branch (jump) instruction: 3, 0011     JMP i cnd rg1 rg2
        if len(contents) < 3 or len(contents) > 5:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            jmpAddr = contents[1]

            if jmpAddr[1:len(jmpAddr)].isdecimal() or jmpAddr.isdecimal(): #converting address | or operator needed if address is single digit
                if jmpAddr[0] == "+": #dynamic -> static
                    jmpAddr = int(jmpAddr) + lineNo
                elif jmpAddr[0] == "-": #dynamic -> static
                    jmpAddr = lineNo + int(jmpAddr) 
                if int(jmpAddr) > 8191 or int(jmpAddr) < 0:
                    jmpAddr = "N/A,val" #returns valerror
                else:
                    jmpAddr = exactbit(jmpAddr, 13)
            else:
                jmpAddr = "N/A,arg" #returns argerror

            jmpCnd = contents[2]
            jmpCnd1 = ""
            jmpCnd2 = ""
            jmpCnd3 = ""
            jmpV0 = False

            jmpRg1 = ""
            jmpRg2 = ""

            if jmpCnd == "imd" and len(contents) == 3: #if immediate, registers do not need changing; the entire rest of the instruction is represented
                jmpCnd = "100000000000000"
            elif jmpCnd == "imd" and len(contents) != 3:
                jmpCnd = "N/A"
            else:
                match jmpCnd[0]: #is_zero
                    case "n":
                        jmpCnd1 = "0"
                    case "y":
                        jmpCnd1 = "1"
                    case "x":
                        jmpCnd1 = "0"
                        jmpV0 = True
                    case _:
                        jmpCnd1 = "N/A"
                match jmpCnd[1]: #comp
                    case "=":
                        jmpCnd2 = "00"
                    case ">":
                        jmpCnd2 = "01"
                    case "<":
                        jmpCnd2 = "10"
                    case _:
                        jmpCnd2 = "N/A"
                match jmpCnd[2]: #true/false
                    case "t":
                        jmpCnd3 = "1"
                    case "f":
                        jmpCnd3 = "0"
                    case _:
                        jmpCnd3 = "N/A"
                if jmpCnd1 == "N/A" or jmpCnd2 == "N/A" or jmpCnd3 == "N/A" or len(jmpCnd) != 3:
                    jmpCnd = "N/A" #returns argerror
                elif jmpV0:
                    jmpCnd = "001"+jmpCnd1+jmpCnd2+jmpCnd3
                else:
                    jmpCnd = "000"+jmpCnd1+jmpCnd2+jmpCnd3

                if len(contents) == 5: #only needed if not immediate
                    jmpRg1 = register(contents[3])[1:5]
                    jmpRg2 = register(contents[4])[1:5]
                else:
                    jmpRg1 = "N/A" #returns regerror
                    jmpRg2 = "N/A" #returns regerror

            if jmpAddr == "N/A,arg" or jmpCnd == "N/A": #error checks
                code = "N/A"
                errors.append(str(lineNo+1)+argerror+"\n")
            elif jmpAddr == "N/A,val":
                code = "N/A"
                errors.append(str(lineNo+1)+valerror+"\n")
            elif jmpRg1 == "N/A" or jmpRg2 == "N/A":
                code = "N/A"
                errors.append(str(lineNo+1)+regerror+"\n")
            else:
                code = "0011"+jmpAddr+jmpCnd+jmpRg1+jmpRg2

    elif inst == "IDC":     #in/decrement instruction: 4, 0100              IDC dir reg
        if length != 11:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            idcDir = line[4:7]
            idcReg = line[8:11]

            idcReg = register(idcReg)

            if idcDir == "inc":
                idcDir = "1"
            elif idcDir == "dec":
                idcDir = "0"
            else:
                idcDir = "N/A"

            if idcDir == "N/A":
                errors.append(str(lineNo+1)+argerror+"\n")
                code = "N/A"
            elif idcReg == "N/A" or str.isdecimal(idcReg):
                errors.append(str(lineNo+1)+regerror+"\n")
                code = "N/A"
            else:
                code = "0100"+idcDir+idcReg[1:5]+"00000000000000000000000"

    elif inst == "CAP":     #bitcapping instruction: 5, 0101                CAP reg b ln
        if length < 11 or length > 12:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            capReg = register(line[4:7])
            capBgn = line[8]
            capLen = line[10:length]

            if capReg == "N/A" or str.isdecimal(capReg):
                errors.append(str(lineNo+1)+regerror+"\n")
                code = "N/A"
            elif int(capLen) > 15:
                errors.append(str(lineNo+1)+valerror+"\n")
                code = "N/A"
            elif hex2dec(capBgn) == "N/A" or line[9] != " ":
                errors.append(str(lineNo+1)+argerror+"\n")
                code = "N/A"
            else:
                capBgn = exactbit(hex2dec(capBgn), 4)

                capLen = bin(int(capLen))[2:len(bin(int(capLen)))]
                capLen = str((4-len(capLen))*"0"+str(capLen))
                
                code = "0101"+capReg[1:5]+capBgn+capLen+"0000000000000000"

    elif inst == "SHF":     #bitshifting instruction: 6, 0110               SHF reg dir val
        if length < 13 or length > 14:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            shfReg = register(line[4:7])
            shfDir = line[8:11]
            shfVal = line[12:length]

            if shfReg == "N/A" or str.isdecimal(shfReg):
                errors.append(str(lineNo+1)+regerror+"\n")
                code = "N/A"
            elif shfDir != "dwn" and shfDir != "_up":
                errors.append(str(lineNo+1)+argerror+"\n")
                code = "N/A"
            elif int(shfVal) > 15:
                errors.append(str(lineNo+1)+valerror+"\n")
                code = "N/A"
            else:
                shfVal = exactbit(shfVal, 4)

                if shfDir == "dwn":
                    code = "0110"+shfReg[1:5]+"0"+shfVal+"0000000000000000000"
                elif shfDir == "_up":
                    code = "0110"+shfReg[1:5]+"1"+shfVal+"0000000000000000000"
                else:
                    code = "N/A"
                    errors.append(str(lineNo+1)+argerror+"\n")

    elif inst == "MEM":     #memory access instruction: 7, 0111             MEM pin rg1 rg2; MEM DMP adr val
        if length != 15 and line[4:7] != "dmp":
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        elif length < 13 and line[4:7] == "dmp":
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            if line[4:7] == "dmp":      #memory dump
                dmpAddr = line[8:11]
                dmpVal = line[12:length]

                dmpAddrVal = 0

                for i in range(3):
                    if hex2dec(dmpAddr[-i-1]) == "N/A":
                        dmpAddrVal = "N/A"
                        break
                    else:
                        dmpAddrVal += (16**i)*int(hex2dec(dmpAddr[-i-1]))
                dmpAddr = dmpAddrVal

                dmpValEx = 0

                if dmpVal[0:2] == "0b": #if given value is binary
                    for i in range(len(dmpVal[2:len(dmpVal)])):
                        if int(dmpVal[-(i+1)]) != 0 and int(dmpVal[-(i+1)]) != 1: #incorrect digit
                            dmpValEx = "N/A"
                            break
                        else:
                            bit = int(dmpVal[-(i+1)])*(2**i)
                            dmpValEx += bit
                    dmpVal = dmpValEx
                elif dmpVal[0:2] == "0x": #if given value is hexadecimal
                    for i in range(len(dmpVal[2:len(dmpVal)])):
                        if hex2dec(dmpVal[-(i+1)]) == "N/A": #incorrect digit
                            dmpValEx = "N/A"
                            break
                        else:
                            hexa = int(hex2dec(dmpVal[-(i+1)]))*(16**i)
                            dmpValEx += hexa
                    dmpVal = dmpValEx
                elif str.isdecimal(dmpVal) == False: #if given value cannot be recognized as hex, bin or decimal
                    dmpVal = "N/A"

                if dmpAddr == "N/A" or dmpVal == "N/A": #error checks
                    errors.append(str(lineNo+1)+argerror+"\n")
                    code = "N/A"
                elif int(dmpAddr) > 2047 or int(dmpVal) > 65535:
                    errors.append(str(lineNo+1)+valerror+"\n")
                    code = "N/A"
                else:
                    dmpVal = exactbit(dmpVal, 16)

                    dmpAddr = exactbit(dmpAddr, 11)

                    code = "0111"+dmpAddr+dmpVal+"1"

            elif line[4:7] == "pre" or line[4:7] == "pst" or line[4:7] == "hre" or line[4:7] == "hst":
                memPlc = line[4]
                memIns = line[5:7]

                if memPlc == "p":
                    memPlc = "0"
                elif memPlc == "h":
                    memPlc = "1"

                if memIns == "re":
                    memIns = "0"
                elif memIns == "st":
                    memIns = "1"

                memOp = register(line[8:11])
                memAddr = register(line[12:15])

                if memOp == "N/A" or memAddr == "N/A" or str.isdecimal(memOp) or str.isdecimal(memAddr):
                    errors.append(str(lineNo+1)+regerror+"\n")
                    code = "N/A"
                else:
                    code = "0111"+memPlc+memIns+memOp[1:5]+memAddr[1:5]+"000000000000000000"
            else:
                errors.append(str(lineNo+1)+argerror+"\n")
                code = "N/A"

    elif inst == "DSP":     #display access instruction: 8, 1000            DSP i/o reg
        if length != 11:
            errors.append(str(lineNo+1)+lenerror+"\n")
            code = "N/A"
        else:
            dspIO = line[4:7]
            dspReg = register(line[8:11])

            if dspReg == "N/A" or str.isdecimal(dspReg) == True:
                errors.append(str(lineNo+1)+regerror+"\n")
                code = "N/A"
            else:
                if dspIO == "inp":
                    code = "1000"+"1"+dspReg[1:5]+"00000000000000000000000"
                elif dspIO == "out":
                    code = "1000"+"0"+dspReg[1:5]+"00000000000000000000000"
                else:
                    errors.append(str(lineNo+1)+argerror+"\n")
                    code = "N/A"

    elif inst == "END":     #process halt instruction: F, 1111              END (exc)
        exCode = line[4:length]
        if len(exCode) == 0:
            code = "1111"+28*"0"
        elif str.isdecimal(exCode) == False:
            errors.append(str(lineNo+1)+argerror+"\n")
            code = "N/A"
        elif len(exCode) != 0 and int(exCode) < 65536:
            exCode = exactbit(exCode, 16)
            code = "1111"+str(exCode)+"000000000000"
        elif len(exCode) != 0 and int(exCode) > 65535:
            errors.append(str(lineNo+1)+valerror+"\n")
            code = "N/A"
    
    elif inst == "":
        code = ""
    
    else:
        errors.append(str(lineNo+1)+inserror+"\n")
        code = "N/A"

    if code == "N/A":
        errorList.append(lineNo+1)
    elif code == "":
        encodedFile.write("")
    else:
        full = ""
        for i in range(8):
            curr = code[i*4:(i+1)*4]
            if curr == "0000":
                curr = "0"
            elif curr == "0001":
                curr = "1"
            elif curr == "0010":
                curr = "2"
            elif curr == "0011":
                curr = "3"
            elif curr == "0100":
                curr = "4"
            elif curr == "0101":
                curr = "5"
            elif curr == "0110":
                curr = "6"
            elif curr == "0111":
                curr = "7"
            elif curr == "1000":
                curr = "8"
            elif curr == "1001":
                curr = "9"
            elif curr == "1010":
                curr = "A"
            elif curr == "1011":
                curr = "B"
            elif curr == "1100":
                curr = "C"
            elif curr == "1101":
                curr = "D"
            elif curr == "1110":
                curr = "E"
            elif curr == "1111":
                curr = "F"
            full += curr
        encodedFile.write(full+"\n")


    lineNo += 1
    rawLine = rawFile.readline()

rawFile.close()
encodedFile.close()

if len(errorList) > 0:
    print(f"[WARN] Error(s) ocurred in {len(errorList)} line(s): {errorList}")
    print("[WARN] List of error(s):")
    for err in errors:
        print(err, end="")
else:
    print(f"Assembly completed flawlessly: {lineNo} line(s), {(lineNo)*4} byte(s)")

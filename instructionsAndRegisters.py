#things still not implemented here:
#showing the work per timer increment



#registers as arrays of bits of length 16 or 12
#MSB is at arr[0] and LSB is at arr[15 || 12] to make it easier to output for visualisation
#example: DR = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
#               ^MSB                          ^LSB
AR = [0] * 12
memory = [[0] * 16] * 4096
PC = [0] * 12
DR = [0] * 16
AC = [0] * 16
INPR = [0] * 8 
IR = [0] * 16
OUTR = [0] * 8
opcode = [0] * 3
program = [] #list of all commands in the program.txt 


#flags
indirect = False #indirect bit
E = 0 #error bit

def fetchDecode():
    global IR
    global indirect
    global opcode
    global PC
    global AR

    current = binToDec(PC)
    AR = hexToBin(program[current])[4:16] #i have no idea if the program will always start at 0 or not since the proffesor described the program as an address + operation 
    #                      rather than just an operation so this is the a mathod that handels both cases

    location = binToDec(AR)
    print("reading IR in location:", location)
    IR = memory[location]
    PC = decToBin(current + 1)
    AR = IR[4:16]
    print("AR:", AR)
    indirect = IR[0]
    opcode = IR[1:4]

    if(indirect):
        location = binToDec(AR)
        AR = memory[location][4:16]




def binToDec(reg):
    value = 0
    for i in range(0, len(reg)):
        value += pow(2, i) * reg[len(reg) -1 - i]
    return value
    
def decToBin(num):
    value = bin(num).replace("0b", "")
    binOut = [0] * 16
    counter = 0
    for i in reversed(value):
        binOut[15-counter] = int(i)
        counter += 1
    return binOut


def hexToBin(num):
    binOut = [0] * 16
    value = int(num, 16)

    binOut = decToBin(value)


    return binOut


#!!!!!!!!!!!!!!!!!!!!!!!!!!these values are just here to test register instructions remove them before submitting!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
DR = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
AC = [0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0]



#memory reffrence instructions
def AND():
    global memory
    global AR
    global AC
    location = binToDec(AR)
    DR = memory[location]
    print("AC before:", AC)
    print("DR before:", DR)
    print("AR before:", AR)
    for i in range(len(AC)):
        AC[i] =  int(bool(AC[i]) & bool(DR[i]))
    print("DR after:", DR)
    print("AC after:", AC)
    print("AR after:", AR)

def ADD():
    global memory
    global AR
    location = binToDec(AR)
    global AC
    global DR
    
    print("AC before:", AC)
    print("DR before:", DR)
    print("AR before:", AR)

    DR = memory[location]
    x = binToDec(AC)
    y = binToDec(DR)

    AC = decToBin((x + y))

    print("AC after:", AC)
    print("DR after:", DR)
    print("AR after:", AR)

def LDA():
    global memory
    global AR
    location = binToDec(AR)
    global AC
    global DR

    print("AC before:", AC)
    print("DR before:", DR)
    print("AR before:", AR)
    
    DR = memory[location]

    AC = DR

    print("AC after:", AC)
    print("DR after:", DR)
    print("AR after:", AR)

def STA():
    global memory
    global AR
    global AC
    location = binToDec(AR)

    print("AC before:", AC)
    print("AR pointer location: ", location)
    print("memory at AR before:", memory[location])


    memory[location] = AC

    print("AC after:", AC)
    print("AR pointer location: ", location)
    print("memory at AR after:", memory[location])

def BUN():
    global PC
    print("PC before:", PC)
    PC = AR
    print("PC after: ", PC)

def BSA():
    global memory
    global AR
    global PC
    print("PC before:", PC)
    print("AR before:", AR)
    location = binToDec(AR)
    memory[location] = PC
    AR += 1
    PC = AR
    print("PC after:", PC)
    print("AR after:", AR)

def ISZ():
    global memory
    global AR
    global PC
    global AC
    global DR
    
    location = binToDec(AR)
    
    print("AR before:", AR)
    print("AC before:", AC)
    print("DR before:", DR)
    print("PC before:", PC)

    DR = memory[location]
    x = binToDec(DR)

    DR = decToBin((x + 1))
    memory[location] = DR
    if(binToDec(DR) == 0):
        x = binToDec(PC)

        PC = decToBin((x + 1))
    print("AR after:", AR)
    print("AC after:", AC)
    print("DR after:", DR)
    print("PC after:", PC)

#register reffrence instructions
def CLA():
    global AC
    print("AC before: ", AC)
    AC = [0] * 16
    print("AC after: ", AC)

def CLE():
    global E
    print("E before: ", E)
    E = 0
    print("E after: ", E)

def CMA():
    print("AC before: ", AC)
    for i in range(len(AC)):
        AC[i] =  int(not(bool(AC[i])))
    print("AC after: ", AC)

def CME():
    global E
    print("E before: ", E)
    E = not(E)
    print("E after: ", E)

def CIR():
    global AC
    global E

    print("AC before: ", AC)
    print("E before: ", E)

    E = AC[15] #again this is reversed between CIR and CIL since python arrays and the books visualisation of the registers are opposites
    x = binToDec(AC)
    x = x*2
    AC = decToBin(x)    
    print("AC after: ", AC)
    print("E after: ", E)

def CIL():
    global AC
    global E

    print("AC before: ", AC)
    print("E before: ", E)

    E = AC[0]
    x = binToDec(AC)
    x =int(x/2)
    AC = decToBin(x)

    print("AC after: ", AC)
    print("E after: ", E)


def INC():
    global AC
    print("AC before: ", AC)

    x = binToDec(AC)
    x += 1
    AC = decToBin(x)

    print("AC after: ", AC)

def SPA():
    global PC

    print("AC before: ", AC)
    print("PC before: ", PC)
    if(AC[0] == 0):
        x = binToDec(PC)
        PC = decToBin((x + 1))
    print("AC after: ", AC)
    print("PC after: ", PC)

def SNA():
    global AC
    global PC
    print("AC before: ", AC)
    print("PC before: ", PC)
    if(AC[0] == 1):
        x = binToDec(PC)
        PC = decToBin((x + 1))
    print("AC after: ", AC)
    print("PC after: ", PC)

def SZA():
    global PC
    global AR
    print("AC before: ", AC)
    print("PC before: ", PC)
    if(binToDec(AR) == 0):
       x = binToDec(PC)
       PC = decToBin((x + 1))
    print("AC after: ", AC)
    print("PC after: ", PC)

def SZE():
    global E
    global PC
    print("E before: ", E)
    print("PC before: ", PC)
    if(E == 0):
       x = binToDec(PC)
       PC = decToBin((x + 1))
    print("E after: ", E)
    print("PC after: ", PC)

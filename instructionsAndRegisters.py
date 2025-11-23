#registers as arrays of bits of length 16 or 12
#MSB is at arr[0] and LSB is at arr[15 || 12] to make it easier to output for visualisation
#example: DR = [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0]
#               ^MSB                          ^LSB
AR = [0] * 12
memory = [[0] * 16] * 4096
PC = [0] * 12
DR = [0] * 16
AC = [0] * 16
IR = [0] * 16
opcode = [0] * 3
cycles = 0 #keeps track of how many cycles need to be completed
instructions = 0 #keeps track of how many instructions need to be completed
totalCycles = 0
totalInstructions = 0
bandwidth = 0

#flags
indirect = False #indirect bit
E = 1 #error bit

#function thats responsible for making each instruction execute per clockcycle and handeling user inputs
def checkAndWait():
    
    global cycles
    global instructions
    global totalCycles
    global totalInstructions


    print("Current clockcycle: T"+ str(totalCycles))
    totalCycles += 1



    user_command = ""
    if(instructions > 0):
        return
    if(cycles > 0):
        cycles -= 1
        return
    else:
        while(cycles <= 0 and instructions <= 0):
            print("choose a command: (N indicates the number in decimal)")
            print("next_cycle | fast_cycle N | next_inst | fast_inst N | run | show reg_name | show mem N | show all | show profiler")
            user_command = input()
            user_command_split = user_command.split()
            if(user_command_split[0] == "next_cycle"):
                cycles += 1
            elif(user_command_split[0] == "fast_cycle"):
                cycles += int(user_command_split[1])
            elif(user_command_split[0] == "next_inst"):
                instructions += 1
            elif(user_command_split[0] == "fast_inst"):
                instructions += int(user_command_split[1]) 
            elif(user_command_split[0] == "show"):
                show(user_command_split)
            elif(user_command_split[0] == "run"):
                instructions = 10000
        
def show(option):
    global AC
    global AR
    global memory
    global PC
    global DR
    global IR
    if(option[1] == "AC"):
        print("AC = ",hex(binToDec(AC)), "(binary:",AC,")")
    if(option[1] == "PC"):
        print("PC = ",hex(binToDec(PC)), "(binary:",PC,")")
    if(option[1] == "AR"):
        print("AR = ",hex(binToDec(AR)), "(binary:",AR,")")
    if(option[1] == "DR"):
        print("DR = ",hex(binToDec(DR)), "(binary:",DR,")")
    if(option[1] == "IR"):
        print("IR = ",hex(binToDec(IR)), "(binary:",IR,")")
    if(option[1] == "mem"):
        print("MEM[",option[2],"] = 0x",hex(binToDec(memory[int(option[2])])), "(binary:",memory[int(option[2])],")")
    if(option[1] == "all"):
        print("AC = ",hex(binToDec(AC)), "(binary:",AC,")")
        print("PC = ",hex(binToDec(PC)), "(binary:",PC,")")
        print("AR = ",hex(binToDec(AR)), "(binary:",AR,")")
        print("DR = ",hex(binToDec(DR)), "(binary:",DR,")")
        print("IR = ",hex(binToDec(IR)), "(binary:",IR,")")
    if(option[1] == "profiler"):
        print("cycles: ", totalCycles)
        print("instruction: ", totalInstructions)
        print("CPI: ", totalCycles/totalInstructions)
        print("bandwidth: ", bandwidth)

def setEntry(entry): #sets the programs entry point from the user
    global PC
    PC = hexToBin(entry)

def fetchDecode():
    global IR
    global indirect
    global opcode
    global PC
    global AR
    global instructions
    global bandwidth

    checkAndWait()

    print("AR <--  PC")
    AR = PC
    
    print("AR = ", AR)

    checkAndWait()

    location = binToDec(AR)
    print("reading IR in location:", location)
    IR = memory[location]
    bandwidth += 1
    print("Instruction in hand: 0x", hex(binToDec(IR)).split('x')[-1])
    PC = decToBin(binToDec(PC) + 1)
    print("PC incremented")
    print(PC)
    AR = IR[4:16]
    print("AR:", AR)
    indirect = IR[0]
    opcode = IR[1:4]

    checkAndWait()

    if(indirect):
        location = binToDec(AR)
        AR = memory[location][4:16]
        bandwidth += 1
    
    checkAndWait()




def binToDec(reg):
    value = 0
    for i in range(0, len(reg)):
        value += pow(2, i) * reg[len(reg) -1 - i]
    return value
    
def decToBin(num):
    binOut = [0] * 16
    if(num > 65535):
        return binOut
    value = bin(num).replace("0b", "")
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




#memory reffrence instructions
def AND():
    global memory
    global AR
    global AC
    global instructions
    global bandwidth
    global totalInstructions
    totalInstructions += 1
    location = binToDec(AR)
    print("DR <-- M[AR]")
    DR = memory[location]
    bandwidth +=1
    print("Changed DR")

    checkAndWait()

    print("AC <-- AC && DR")
    for i in range(len(AC)):
        AC[i] =  int(bool(AC[i]) & bool(DR[i]))
    print("Changed AC")
    

    if(instructions > 0):
        instructions -= 1
    checkAndWait()


def ADD():
    global memory
    global AR
    location = binToDec(AR)
    global AC
    global DR
    global instructions
    global bandwidth
    global totalInstructions
    totalInstructions += 1
    
    print("DR <-- M[AR]")
    DR = memory[location]
    print("Changed DR")

    bandwidth += 1
    
    checkAndWait()

    x = binToDec(AC)
    y = binToDec(DR)

    print("AC <-- AC+DR")
    AC = decToBin((x + y))
    print("Changed AC")



    if(instructions > 0):
        instructions -= 1
    checkAndWait()


def LDA():
    global memory
    global AR
    location = binToDec(AR)
    global AC
    global DR
    global instructions
    global bandwidth
    global totalInstructions
    totalInstructions += 1


    print("DR <-- M[AR]")
    DR = memory[location]
    print("Changed DR")

    bandwidth += 1

    checkAndWait()

    AC = DR

    print("AC <-- Dr")
    print("Changed AC")

    if(instructions > 0):
        instructions -= 1
    checkAndWait()


def STA():
    global memory
    global AR
    global AC
    global instructions
    global bandwidth
    global totalInstructions
    totalInstructions += 1
    location = binToDec(AR)

    
    print("MEM[AR] <-- AC")
    print("Changed MEM[AR]")

    memory[location] = AC

    bandwidth += 1
    
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

    

def BUN():
    global PC
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("PC <-- AR")
    PC = AR
    print("Changed: PC")
    
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def BSA():
    global memory
    global AR
    global PC
    global instructions
    global bandwidth
    global totalInstructions
    totalInstructions += 1
    location = binToDec(AR)
    print("MEM[AR] <-- PC, AR <-- AR+1")
    memory[location] = PC
    AR += 1
    print("Changed: MEM[AR], AR")
    bandwidth += 1
    checkAndWait()
    print("PC <-- AR")
    PC = AR
    if(instructions > 0):
        instructions -= 1
    checkAndWait()


def ISZ():
    global memory
    global AR
    global PC
    global AC
    global DR
    global instructions
    global bandwidth
    global totalInstructions
    totalInstructions += 1

    location = binToDec(AR)
    
    print("DR <-- MEM[AR]")
    DR = memory[location]
    bandwidth += 1
    print("Changed: DR")
    checkAndWait()
    x = binToDec(DR)
    print("DR <-- DR + 1")
    DR = decToBin((x + 1))
    print("Changed: DR")
    checkAndWait()
    print("MEM(AR) <-- DR")
    bandwidth += 1 
    memory[location] = DR
    print("Changed MEM[AR]")
    print("if DR = 0 then PC <-- PC+1")
    print(binToDec(DR))
    if(binToDec(DR) == 0):
        print("PC incremented")
        x = binToDec(PC)

        PC = decToBin((x + 2))
    
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

#register reffrence instructions
def CLA():
    global AC
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("AC = 0")
    AC = [0] * 16
    print("Changed AC")
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def CLE():
    global E
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("E = 0")
    E = 0
    print("Changed E", E)
    
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def CMA():
    global AC
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("AC <-- AC'")
    for i in range(len(AC)):
        AC[i] =  int(not(bool(AC[i])))
    print("Changed AC")
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def CME():
    global E
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("E <-- E'")
    E = not(E)
    print("Changed E")
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def CIR():
    global AC
    global E
    global instructions
    global totalInstructions
    totalInstructions += 1

    print("AC <-- shr Ac, AC[15] <-- E, E <-- AC[0]")

    E = AC[15] #again this is reversed between CIR and CIL since python arrays and the books visualisation of the registers are opposites
    x = binToDec(AC)
    x = x*2
    AC = decToBin(x)    
    print("Changed AC, E")
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def CIL():
    global AC
    global E
    global instructions
    global totalInstructions
    totalInstructions += 1

    print("AC <-- shl AC, AC[0] <-- E, E <-- AC[15]")

    E = AC[0]
    x = binToDec(AC)
    x =int(x/2)
    AC = decToBin(x)

    if(instructions > 0):
        instructions -= 1
    checkAndWait()


def INC():
    global AC
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("AC <-- AC+1")

    x = binToDec(AC)
    x += 1
    AC = decToBin(x)

    print("Changed AC")

    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def SPA():
    global AC
    global PC
    global instructions
    global totalInstructions
    totalInstructions += 1

    print("If AC[15] = 0 then PC <-- PC+1")
    if(AC[0] == 0):
        x = binToDec(PC)
        PC = decToBin((x + 1))
        print("Changed PC")
    
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def SNA():
    global AC
    global PC
    global instructions
    print("If AC[15] = 1 then PC <-- PC+1")
    if(AC[0] == 1):
        x = binToDec(PC)
        PC = decToBin((x + 1))
        print("Changed PC")
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def SZA():
    global PC
    global AC
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("If AC = 0 then PC <-- PC+1")
    if(binToDec(AR) == 0):
       x = binToDec(PC)
       PC = decToBin((x + 1))
       print("Changed PC")
    if(instructions > 0):
        instructions -= 1
    checkAndWait()

def SZE():
    global E
    global PC
    global instructions
    global totalInstructions
    totalInstructions += 1
    print("If E == 0 then PC <-- PC + 1")
    if(E == 0):
       x = binToDec(PC)
       PC = decToBin((x + 1))
       print("Changed PC")
    if(instructions > 0):
        instructions -= 1
    checkAndWait()
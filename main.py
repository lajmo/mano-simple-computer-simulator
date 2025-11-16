#things not yet implemented here:
#1) all the user control functions
#2) showing the current instruction and the IR for that instruction


import instructionsAndRegisters as InR #writing the whole name is annoying
# declaring variables
currentCommand = "" #stores the command as string for later translation
data = [] #list of all data in the data.txt file
currentOperation = [] #the current instruction as bits


registerInstructionDict = {
    2048: InR.CLA,
    1024: InR.CLE,
    512: InR.CMA,
    256: InR.CME,
    128: InR.CIR,
    64: InR.CIL,
    32: InR.INC,
    16: InR.SPA,
    8: InR.SNA,
    4: InR.SZA,
    2: InR.SZE,
}

memoryInsructionDict = {
    0: InR.AND,
    1: InR.ADD,
    2: InR.LDA,
    3: InR.STA,
    4: InR.BUN,
    5: InR.BSA,
    6: InR.ISZ,
}



#initialise data from data.txt
def dataInit():
    dFile = open("hexprogram/data.txt")

    #loops for everyline. Splits line into data and register values and saves them to memory
    for line in dFile:
        temp = line.split()
        dRegister = temp[0]
        dData = temp[1]
        dData = InR.hexToBin(dData)

        location = int(dRegister, 16)

        InR.memory[location] = dData
        print(location,"   ",InR.memory[location])

def loadProgram():
    pFile = open("hexprogram/program.txt")
    for line in pFile:
        temp = line.split()
        pInstruction = temp[1]
        pAddress = temp[0]
        location = int(pAddress, 16)
        pInstruction = InR.hexToBin(pInstruction)
        InR.memory[location] = pInstruction
        print("location saved to:",location)
        print(InR.memory[location])
        InR.program.append(pAddress)


if __name__ == "__main__":
    dataInit()
    loadProgram()
    print(InR.program)
    for line in InR.program:
        InR.fetchDecode()
        #register reffrence set
        if(InR.binToDec(InR.opcode) == 7):
            registerInstructionDict[InR.binToDec(InR.AR)]()
        #register reffrence set
        else:
            memoryInsructionDict[InR.binToDec(InR.opcode)]()
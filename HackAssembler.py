import sys, os, re
import HackParser, HackEncoder, HackSymbolTable
from InstructionType import InstructionType

def resolveSymbol(instruction, symbolTable):
    if instruction['symbolic'] and symbolTable.contains(instruction['value']):
        return symbolTable.getAddress(instruction['value'])
    elif instruction['symbolic'] and not symbolTable.contains(instruction['value']):
        symbolTable.addAddressEntry(instruction['value'])
        return symbolTable.getAddress(instruction['value'])
    else:
        return instruction['value']
        

def main():
    #initialize environment
    if len(sys.argv) < 2:
        sys.exit("ERROR: No asm file specified")
    workingDirectory = os.getcwd()
    filePath = sys.argv[1]
    pathList = filePath.split("/")
    fileName = pathList[len(pathList) - 1]
    asmPath = os.path.join(workingDirectory, filePath)
    
    symbolTable = HackSymbolTable.HackSymbolTable()

    #read in file
    with open(asmPath,"r",encoding="utf-8") as file:
        asmFile = file.readlines()
    parser = HackParser.HackParser(symbolTable)
    #get list of instructions, each instruction separated into its fields
    parsedHack = parser.parse(asmFile)

    resolvedHack = []
    for instruction in parsedHack: 
        if instruction['type'] == InstructionType.ADDRESS:
            instruction['value'] = resolveSymbol(instruction, symbolTable)
        resolvedHack.append(instruction)

    encoder = HackEncoder.HackEncoder()
    encodedInstructionList = encoder.encode(resolvedHack)
    
    #write out asm file in working dir
    outFilePath = workingDirectory + "/" + re.sub(r'\.asm$',".hack", fileName)
    with open(outFilePath,"w", encoding="utf-8") as outFile:
        for instruction in encodedInstructionList:
            outFile.write(instruction)
            outFile.write(os.linesep)

main()


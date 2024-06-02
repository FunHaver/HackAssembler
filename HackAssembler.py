import sys, os, re
import HackParser, HackEncoder, HackSymbolTable
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
    
    encoder = HackEncoder.HackEncoder()
    encodedInstructionList = encoder.encode(parsedHack)
    
    #write out asm file in working dir
    outFilePath = workingDirectory + "/" + re.sub(r'\.asm$',".hack", fileName)
    with open(outFilePath,"w", encoding="utf-8") as outFile:
        for instruction in encodedInstructionList:
            outFile.write(instruction)
            outFile.write(os.linesep)

main()


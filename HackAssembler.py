import sys, os
import HackParser
def main():
    #initialize environment
    if len(sys.argv) < 2:
        sys.exit("ERROR: No asm file specified")
    workingDirectory = os.getcwd()
    filePath = sys.argv[1]
    asmPath = os.path.join(workingDirectory, filePath)

    #read in file
    with open(asmPath,"r",encoding="utf-8") as file:
        asmFile = file.readlines()
    parser = HackParser.HackParser()
    #get list of instructions, each instruction separated into its fields
    parsedHack = parser.parse(asmFile)
    print(parsedHack)

main()


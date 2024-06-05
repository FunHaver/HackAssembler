# Class with one public method: parse
# Takes an UTF-encoded text file containing the HACK assembler language
# And outputs a list of dicts, each dict containing the instruction type and fields that 
# are found in each instruction.
from InstructionType import InstructionType

import re, sys

class HackParser:
    def __init__(self, symbolTable):
        self.parsedInstructions = []
        self.symbolTable = symbolTable
        self.__sourceLine = 0 # keeps track of assembly source line for debugging
        self.__instructionLine = 0 #keeps track of actual "assembled" instruction line

    # Classifies instruction as an A, C, Symbolic, or ignorable instruction. 
    # otherwise return true
    def __instructionClassifier(self,line):
        index = 0
        while index < len(line) and line[index] == ' ':
            index += 1
            return InstructionType.IGNORE
        if index == len(line): #end of line, end of file?
            return InstructionType.IGNORE
        elif line[index] == '\n': #newline
            return InstructionType.IGNORE
        elif line[index] == '/': #potentially comment line
            if index + 1 < len(line) and line[index + 1] == '/': #definitely comment line
                return InstructionType.IGNORE
        else:
            return self.__classifyNonIgnorableInstruction(line, index)
    
    # Classifies all lines that are not white space or just comments
    def __classifyNonIgnorableInstruction(self, line, startingIdx):
        if line[startingIdx] == "@":
            return InstructionType.ADDRESS
        elif line[startingIdx] == "(":
            return InstructionType.SYMBOL
        elif self.__validCommandSymbol(line[startingIdx]):
            return InstructionType.COMMAND
        else:
            return InstructionType.UNKNOWN

    def __validCommandSymbol(self, character):
        validChar = False
        for command in "ADM01-!;":
            if command == character:
                validChar = True
                break
        return validChar

    # Splits A instruction into fields, will replace symbols with appropriate RAM address
    def __splitAInstruction(self,instruction):
        splitField = {
            "type": InstructionType.ADDRESS,
            "sourceLine": self.__getCurrentSourceLine(),
            "value": instruction[1:],
            "symbolic": False
        }
        if re.search(r'[0-9]',instruction[1]) is None:
            splitField["symbolic"] = True
        print(instruction[1])
        print(splitField["symbolic"])
        return splitField


    def __splitCInstruction(self,instruction):
        splitField = {
            "type": InstructionType.COMMAND,
            "sourceLine": self.__getCurrentSourceLine(),
            "dest": '',
            "comp": '',
            "jump": ''
        }

        field = ''
        hasDest = False
        hasJMP = False

        for i in range(len(instruction)):

            if instruction[i] != '=' and instruction[i] != ';' and instruction[i] != '\n':
                field += instruction[i]
            elif instruction[i] == '=':
                splitField['dest'] = field
                hasDest = True
                field = ''
            elif instruction[i] == ';':
                splitField['comp'] = field
                hasJMP = True
                field = ''
            
            # reached the end
            if i + 1 == len(instruction):
                if hasJMP:
                    splitField['jump'] = field
                elif hasDest:
                    splitField['comp'] = field
                else:
                    splitField['comp'] = field # <-- invalid, should never happen


        return splitField


    #Add to Symbol Table or mark for replacement, replace on second pass
    def __splitSymbolInstruction(self, line):
        symbolDeclaration = ""
        for char in line:
            if(char == ")"):
                break
            elif(char == "("):
                continue
            else:
                symbolDeclaration += char
        if line[len(symbolDeclaration) + 1] != ")":
            sys.exit("Error line " + self.__getCurrentSourceLine() + ": Malformed symbol " + line)
        else:
            symbolValue = self.__getCurrentInstructionLine()
            self.symbolTable.addEntry(symbolDeclaration,symbolValue)

            
    def __incrementSourceLine(self):
        self.__sourceLine += 1

    def __getCurrentSourceLine(self):
        return str(self.__sourceLine)
    
    def __incrementInstructionLine(self):
        self.__instructionLine += 1
    
    def __getCurrentInstructionLine(self):
        return self.__instructionLine
    
    # takes file in, outputs list dicts representing valid assembler instructions
    def parse(self,asmFile):
        # split by newline and store instruction as dict 
        # in list if valid asm instruction

        for line in asmFile:
            self.__incrementSourceLine()
            lineNoWS = "".join(line.split())
            lineType = self.__instructionClassifier(lineNoWS)
            if lineType == InstructionType.IGNORE:
                continue
            elif lineType == InstructionType.ADDRESS:
                self.parsedInstructions.append(self.__splitAInstruction(lineNoWS))
                self.__incrementInstructionLine()
            elif lineType == InstructionType.COMMAND:
                self.parsedInstructions.append(self.__splitCInstruction(lineNoWS))
                self.__incrementInstructionLine()
            elif lineType == InstructionType.SYMBOL:
                self.__splitSymbolInstruction(lineNoWS)
            else:
                sys.exit("ERROR Line " + self.__getCurrentSourceLine() + ": Unknown Instruction \"" + lineNoWS + "\"")
                


        return self.parsedInstructions
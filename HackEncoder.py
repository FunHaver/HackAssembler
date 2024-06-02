# Class with one public method: encode
# Takes the list from the Parser and replaces
# the values of each instruction's field with the
# corresponding binary encoding (Still UTF-8 string encoded)
import sys
from InstructionType import InstructionType
class HackEncoder:
    def __init__(self):
        self.encodedInstructions = []
        self.compFieldMap = {
            "0":   "0101010",
            "1":   "0111111",
            "-1":  "0111010",
            "D":   "0001100",
            "A":   "0110000",
            "!D":  "0001101",
            "!A":  "0110001",
            "-D":  "0001111",
            "-A":  "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M":   "1110000",
            "!M":  "1110001",
            "-M":  "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }

        self.jumpFieldMap = {
            "":    "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }


        

    def __translateOpCode(self,instructionType):
        if instructionType == InstructionType.ADDRESS:
            return "0"
        elif instructionType == InstructionType.COMMAND:
            return "111"
        else:
            sys.exit("Error, unknown instruction type: " + instructionType)
    
    # Input mneumonic dest field, return machine code representation
    def __encodeDestField(self,mDestField):
        encodedField = ["0","0","0"]
        for char in mDestField:
            if char == "A":
                encodedField[0] = "1"
            elif char == "D":
                encodedField[1] = "1"
            elif char == "M":
                encodedField[2] = "1"
            else:
                sys.exit("Error, unknown destination char: " + char)
        return "".join(encodedField)
    
    # Input mneumonic comp field, return machine code representation
    def __encodeCompField(self,mCompField):
        return self.compFieldMap[mCompField]
                
    def __encodeJumpField(self,mJumpField):
        return self.jumpFieldMap[mJumpField]
    
    def __encodeAddressField(self, value):
        return "{:0>15b}".format(int(value))
    
    def encode(self,parsedList):
        binInstructionList = []
        for instruction in parsedList:
            addressValue = ""
            destCode = ""
            compCode = ""
            jumpCode = ""
            opCode = self.__translateOpCode(instruction['type'])
            if(instruction['type'] == InstructionType.ADDRESS):
                addressValue = self.__encodeAddressField(instruction['value'])
                binInstructionList.append(opCode+addressValue)
            elif(instruction['type'] == InstructionType.COMMAND):
                destCode = self.__encodeDestField(instruction['dest'])
                compCode = self.__encodeCompField(instruction['comp'])
                jumpCode = self.__encodeJumpField(instruction['jump'])
                binInstructionList.append(opCode+compCode+destCode+jumpCode)
            else:
                sys.exit("Error on line " + instruction["sourceLine"] + ": unknown instruction type: " + instruction.type)

        return binInstructionList
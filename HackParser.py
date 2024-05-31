# Class with one public method: parse
# Takes an UTF-encoded text file containing the HACK assembler language
# And outputs a list of dicts, each dict containing the instruction type and fields that 
# are found in each instruction.

class HackParser:
    def __init__(self):
        self.parsedInstructions = []

    # If line is just newline or a comment, return false.
    # otherwise return true
    def __isInstruction(self,line):
        index = 0
        while index < len(line) and line[index] == ' ':
            index += 1
        
        if index == len(line): #end of line, end of file?
            return False
        elif line[index] == '\n': #newline
            return False
        elif line[index] == '/': #potentially comment line
            if index + 1 < len(line) and line[index + 1] == '/': #definitely comment line
                return False
        else:
            return True
    
    def __splitCInstruction(self,instruction):
        splitField = {
            "type": 'C',
            "dest": '',
            "comp": '',
            "jump": ''
        }

        field = ''
        hasDest = False
        hasJMP = False

        for i in range(len(instruction)):

            if instruction[i] != '=' and instruction[i] != ';':
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

    # Split instruction into fields
    def __splitIntoFields(self,instruction):
        instructionNoWS = ''.join(instruction.split())
        if instructionNoWS[0] == '@': #parse A instruction
            return { 
                     "type": "A",
                     "value": instructionNoWS[1:]
                   }
        else: #else it is a C instruction
            return self.__splitCInstruction(instructionNoWS)
            

    
    # takes file in, outputs array of valid assembler instructions
    def parse(self,asmFile):
        # split by newline and store instruction as dict 
        # in list if valid asm instruction
        for line in asmFile:
            if(self.__isInstruction(line)):
                self.parsedInstructions.append(self.__splitIntoFields(line))
        return self.parsedInstructions
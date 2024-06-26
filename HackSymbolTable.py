import sys

class HackSymbolTable:
    # A table containing all symbols used in the asm file
    def __init__(self):
        self.__symbolTable = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576
        }
        self.__symbolicRamCounter = 16

        for x in range(16):
            self.__symbolTable["R" + str(x)] = x

    
    def contains(self,symbol):
        return symbol in self.__symbolTable
    
    def addAddressEntry(self,symbol):
        self.addEntry(symbol,self.__symbolicRamCounter)
        self.__symbolicRamCounter += 1

    #Adds new entry to symbol table, will throw error if symbol already exists
    def addEntry(self, symbol, value):
        if symbol not in self.__symbolTable:
            self.__symbolTable[symbol] = value
        else:
            sys.exit("Error: " + symbol + " already has a value and cannot be reassigned.")

    def getAddress(self, symbol):
        return self.__symbolTable[symbol]
    


    

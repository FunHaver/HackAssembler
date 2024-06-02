from enum import Enum

InstructionType = Enum("InstructionType", ["COMMAND", "ADDRESS", "SYMBOL", "IGNORE", "UNKNOWN"])
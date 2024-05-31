# Hack Assembler
A Python implementation of the Hack assembler described in NAND2TETRIS Part 1, Unit 6. 

## Spec 
https://drive.google.com/file/d/1CITliwTJzq19ibBF5EeuNBZ3MJ01dKoI/view

## Usage
**System Requirements**
 * Python 3.x
 * git

To use this assembler, first you must have a file written in the HACK assembly language specified in this PDF [here](https://www.nand2tetris.org/_files/ugd/44046b_7ef1c00a714c46768f08c459a6cab45a.pdf).

Some example files are provided in the test_asm_files directory.

First, clone this repository
```bash
git clone https://github.com/FunHaver/HackAssembler.git
```

Then, execute the HackAssembler.py file found in the repository's root directory. This program takes one argument, the name of the .asm file that is to be assembled.

Example execution
```bash
cd HackAssembler
python3 HackAssembler.py test_asm_files/add/Add.asm
```

The resulting "binary" file (it is actually a UTF-8 encoded file of strings of binary numbers), will be written to your current working directory.

The result of the example command will place a .hack file in the hack_assembler directory.

## Running the .hack file
Now that you are in posession of an assembled file, it can be tested via the CPU emulator tool provided by the NAND2TETRIS course located here: https://nand2tetris.github.io/web-ide/cpu

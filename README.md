# COBALT-16
**Computer of Operations from Basic Arithmetic and Logic Tasks - 16bit**

16 bit processor (CPU) with custom ISA capable of running a single-thread process.
Currently in development, planning and building in [Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution).

_Documentation is currently unfinished, it is being worked on!_

# Specs:
    Register count: 8 (rax, rbx, rcx, rdx, r1x, r2x, r3x, r4x)
    Accessible RAM space: 2 × 8kB
    Maximum process length: 8191 lines
    Instructions: 10 (MOV, ART, LGC, JMP, IDC, CAP, SHF, MEM, DSP, END)
    Instruction length: 32 bit

# Releases:
Releases contain the `.circ` Logisim Evolution file, to be loaded and simulated in the software.
You are permitted to experiment with the circuit, and if you would like to share your ideas, open a PR.

The release file will also contain the Assembler, which will turn your mnemonic code into the hexadecimal version that Logisim Evolution ROM supports.
**Important**: The assembler requires you to have a `raw.txt` file for your mnemonic, and an `encoded.txt` file to store the hexadecimal code!

_Note: the documentation of the assembler is still underway, for now use the Instruction Documentation._

Documentation will also be included in every release for its respective version counterparts.
The repo's documentation, assembler and circuit may differ from each other, but in releases everything is paired together to work poperly.

_Note: most documentation about the project is still underway, the only available there is for now is the Instruction Documentation._

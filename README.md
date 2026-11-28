# COBALT-16
**Computer of Operations from Basic Arithmetic and Logic Tasks - 16bit**

16 bit processor (CPU) with custom ISA capable of running a single-thread process.
Currently in development, planning and building in [Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution).

_Documentation is currently unfinished, it is being worked on!_

# Specs:
    Register count: 8 (rax, rbx, rcx, rdx, r1x, r2x, r3x, r4x)
    Accessible RAM space: 2×8kB
    Maximum process length: 8191 lines
    Instructions: 10 (MOV, ART, LGC, JMP, IDC, CAP, SHF, MEM, DSP, END)
    Instruction length: 32 bit

# Releases:
Releases contain the `.circ` Logisim Evolution file, to be loaded and simulated in the software.
You are permitted to experiment with the circuit, and if you would like to share your ideas, open a PR.

The release file will also contain the Assembler, which will turn your mnemonic code into the hexadecimal version that Logisim Evolution ROM supports.
**Important**: The assembler requires you to have a `raw.txt` file for your mnemonic, and an `encoded.txt` file to store the hexadecimal code!

Documentation will also be included in every release for its respective version counterparts.
The repo's documentation, assembler and circuit may differ from each other, but in releases everything is paired together to work poperly.

_Note: most documentation about the project is still underway, the only available there are for now are the Instruction Documentation and Assembler Documentation._

# Roadmap:
_Ideas for what could come next, what is planned and what is currently being worked on._

**WIP, currently in development**

Assembler refactor: currently trying to make the program less of a mess and make it more readable with less redundant code.
Instructions currently done are `MOV`, `JMP` and `DSP`.

**Planned**

FPGA support: it is planned that the circuit is going to be tested on an FPGA, however the circuit is still far from being done to be tested thoroughly.

Stack, functions: callstack instructions with push and pop capabilities; this would also allow for functions to be made and called more easily.
The basic plan and idea is done for this, however nothing of it has been implemented in anything yet.

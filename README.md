# COBALT-16
**Computer of Operations from Basic Arithmetic and Logic Tasks - 16bit**

16 bit processor (CPU) with custom ISA capable of running a single-thread process.
Currently in development, planning and building in [Logisim Evolution](https://github.com/logisim-evolution/logisim-evolution).

_Documentation is currently unfinished, it is being worked on!_

# Specs:
    Register count: 8 (rax, rbx, rcx, rdx, r1x, r2x, r3x, r4x)
    Accessible RAM space: 8k (2¹³) entries in 2 partitions (4k entry each), each 2 bytes = **2 * 8kB** in total
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

# Roadmap:
_Ideas for what could come next, what is planned and what is currently being worked on._

**WIP, currently in development**

Assembler refactor: currently trying to make the program less of a mess and make it more readable and have less redundant code.
Instructions currently done are `MOV` and `JMP`.

Direct DSP in/output from registers: instead of only being able to use the external data partition of memory, it would also be able to read from/write to registers directly.
The beginning steps of the circuit is mostly done, but no logic/assembly or even instruction is started yet.

**Planned**

FPGA support: it is planned that the circuit is going to be tested on an FPGA, however the circuit is still far from being done to be tested thoroughly.

This is a circuit that I made for my Digital Electronics class. It is designed to be a very small Programmable Logic Device (PLD).

Problem Statement:
A single use state machine is wasteful. Why not have a programmable state machine?

Design Statement:
Design and build an programmable logic device that can perform 6 AOI operations on a set of 3 inputs, and can be programmed via a microcontroller/computer.

Criteria/Constraints:
You can design a string of numbers on a computer (or by hand) to program shift registers to perform 6 AIO operations on 3 inputs. The data will be stored on shift registers, and it will be read by multiplexers. These will determine the inputs for each AIO operation. The AIO operation will be carried out by and gates and or gates. The final output will be the output of the 6th AIO operation. In each AIO operation, you can select any of the 3 inputs and/or any of the outputs of the other AIO operations. 
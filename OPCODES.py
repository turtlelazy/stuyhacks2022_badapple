#16 OPCODES
#0000 - NOP - No operation
#0001 - LDA - Load value from ROM into the A register
#0010 - STA - Store value in A register to adress in RAM
#0011 - LRA - Load value from RAM into the A register
#0100 - LDB - Load value from A register into B register
#0101 - MTX - Ouput 16 bit row data to LED Matrix  
#0110 - BST - Shift value in A register by value in B register and store result into A
#0111 - ADD - Add value in A regsister to value in B register and store sum into A
#1000 - SUB - Subtract value in A register from value in B register and store difference into A
#1001 - JMP - Jump to specified address
#1010 - GJM - Jump to specified address if A > B
#1011 - LJM - Jump to specified address if A < B
#1100 - ZJM - Jump to specified address if 0 flag
#1101 - OJM - Jump to specified address if overflow
#1110 - OUT - Output value from A register to output register
#1111 - HLT - Halt clock

def combine(sequence):
    n = 0
    if sequence == '0': 
        return n
    sequence = sequence.split("|")
    for i in sequence: n = n|int(codes[i], 2)
    return n

codes = {
        "AI"   : '0b000000000000000000000001',  #0
        "BI"   : '0b000000000000000000000010',  #1
        "AO"   : '0b000000000000000000000100',  #2
        "BO"   : '0b000000000000000000001000',  #3
        "ADO"  : '0b000000000000000000010000',  #4
        "SAO"  : '0b000000000000000000100000',  #5
        "SUB"  : '0b000000000000000001000000',  #6
        "HBI"  : '0b000000000000000010000000',  #7
        "LBI"  : '0b000000000000000100000000',  #8
        "CO"   : '0b000000000000001000000000',  #9
        "COE"  : '0b000000000000010000000000',  #10
        "CI"   : '0b000000000000100000000000',  #11
        "MRI"  : '0b000000000001000000000000',  #12
        "RAO"  : '0b000000000010000000000000',  #13
        "RAI"  : '0b000000000100000000000000',  #14
        "CARO" : '0b000000001000000000000000',  #15
        "FI"   : '0b000000010000000000000000',  #16
        "IRI"  : '0b000000100000000000000000',  #17
        "HLT"  : '0b000001000000000000000000',  #18
        "CLR"  : '0b000010000000000000000000',  #19
        "OUT"  : '0b000100000000000000000000',  #20
        "NXT"  : '0b001000000000000000000000',  #21
        "MI"   : '0b010000000000000000000000',  #22
        "MAR"  : '0b100000000000000000000000'   #23
        }
#14 definable steps
print("Setting up data...")
data = [0] * 65536
operators = [
        ['NC', 0], #NOP 0000
        ['NC', 4096, 'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'CO|MRI', 'RAO|AI|COE', 'NXT'], #LDA 0001
        ['NC', 8192, 'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'RAI|AO', 'NXT'], #STA 0010
        ['NC', 12288,'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'RAO|AI', 'NXT'], #LRA 0011
        ['NC', 16384,'AO|BI', 'NXT'], #LDB 0100
        ['NC', 20480,'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'MI', 'NXT'], #MTX 0101
        ['NC', 24576,'SAO|AI', 'NXT'], #BST 0110
        ['NC', 28672,'ADO|AI', 'NXT'], #ADD 0111
        ['NC', 32768,'SUB|ADO|AI', 'NXT'], #SUB 1000
        ['NC', 36864,'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'CI', 'NXT'], #JMP 1001
        ['TC', 40960,['CARO|FI', 'COE', 'NXT|COE'], [128, 'CARO|FI', 'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'CI', 'NXT']], #GJM 1010
        ['TC', 45056,['CARO|FI', 'COE', 'NXT|COE'], [64, 'CARO|FI', 'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'CI', 'NXT']], #LJM 1011
        ['TC', 49152,['CARO|FI', 'COE', 'NXT|COE'], [32, 'CARO|FI', 'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'CI', 'NXT']], #ZJM 1100
        ['TC', 53248,['CARO|FI', 'COE', 'NXT|COE'], [16, 'CARO|FI', 'CO|MRI', 'RAO|HBI|COE', 'CO|MRI', 'RAO|LBI|COE', 'CI', 'NXT']], #OJM 1101
        ['NC', 57344,'AO|OUT', 'NXT'], #OUT 1110
        ['NC', 61440, 'CO|MRI', 'HLT', 'NXT']  #HLT 1111
        ]

#FIRST 3 STEPS OF SEQUENCE IS NOT READ BC HARDWARE ENCODED FETCH CYCLE
FETCH_CYCLE_LEN = 2
for operator in operators:
    cur_addr = operator[1]+FETCH_CYCLE_LEN
    inc_addr = [0, 16, 32, 64, 128] 
    if operator[0] == 'NC':
        for i in range(5):
            for y in range(2, len(operator)):
                data[cur_addr+inc_addr[i]+(y-2)] = combine(operator[y]) 

    elif operator[0] == 'TC':
        for i in range(5):
            if inc_addr[i] == operator[3][0]:
                for y in range(1, len(operator[3])):
                    data[cur_addr+inc_addr[i]+(y-1)] = combine(operator[3][y])
            else:
                for y in range(len(operator[2])):
                    data[cur_addr+inc_addr[i]+y] = combine(operator[2][y])

writedata = "v2.0 raw\n"
for i in data:
    writedata += hex(i) + '\n'

file = open('OPCODES2.hex', 'w')
file.write(writedata)
file.close()

print("ROM data set up correctly!")





    











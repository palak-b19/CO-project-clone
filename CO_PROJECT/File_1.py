# assumptions:
# variable name cannot be opcode instructions
op_code = {'add': '00000',
           'sub': '00001',
           'mov': '00010',
           'ld': '00100',
           'st': '00101',
           'mul': '00110',
           'div': '00111',
           'rs': '01000',
           'ls': '01001',
           'xor': '01010',
           'or': '01011',
           'and': '01100',
           'not': '01101',
           'cmp': '01110',
           'jmp': '01111',
           'jlt': '11100',
           'jgt': '11101',
           'je': '11111',
           'hlt': '11010'}

op_type = {"A": ['add', 'sub', 'mul', 'xor', 'or', 'and'],
           "B": ['mov', 'rs', 'ls'],
           "C": ['mov', 'div', 'not', 'cmp'],
           "D": ['ld', 'st'],
           "E": ['jmp', 'jlt', 'jgt', 'je'],
           "F": ['hlt']}

reg = {'R0': '000',
       'R1': '001',
       'R2': '010',
       'R3': '011',
       'R4': '100',
       'R5': '101',
       'R6': '110'}


def hlt_checker(list, tmp_words):
    flag = 1
    tmp_flag = 0
    for word in tmp_words:
        if "hlt" in word:
            tmp_flag |= 1
    if not (tmp_flag):
        flag = 0
        print("Missing hlt instruction")

    else:
        if (tmp_words[-1][-1] != "hlt"):
            flag = 0
            print("Error as hlt is not being used as the last instruction")
        for instruction in tmp_words[0:-1]:
            if instruction[-1] == "hlt":
                flag = 0
                print("ERROR_in_hlt: General syntax error.")  # hlt occurs before last instruction
    return flag


def check_imm(n):
    if 0 <= int(n) <= 127:
        return True
    else:
        print("Illegal immediate value")
        global error_counter
        error_counter += 1
        return False


def imm_to_bin(n):
    return "{0:07b}".format(int(n))


def typos(list):
    print("typos argument: ", list)
    flag = 1
    for words in list:
        flag &= identify_error_type(words)
    return flag

"""
def var_not_declared(lst):
    flag = 1
    declared = {}
    for i in lst:
        if i.startswith('var'):
            var_name = i.split()[1]
            declared[var_name] = "declared"
    for i in lst:
        word = i.split()
        for w in word:
            if 'var' in w:
                var_name = word[-1]
                if var_name not in declared:
                    print(f"ERROR: variable {var_name} is not declared")
                    flag = 0
    return flag
"""
def var_not_dec(inst,var):
    flag=1
    for ins in inst:
        if (ins[0] in op_type.get("D") or ins[0] in op_type.get("E")) and ins[-1] not in var:
            print(f"ERROR: variable {ins[-1]} is not declared")
            flag=0
    return flag

def not_defined_at_beginning(list1, list2):
    print(list)
    flag = 1
    for line in list1:
        if line[0] == "var" and len(line) == 2:
            if line[-1] in op_code.keys():
                print("Opcode cannot be used as instruction name")
                flag = 0
        # else:
        #    print("ERROR_in_ndab: General Syntax error")
    functions = []
    for line in list2:
        line = line.split()
        functions.append(line[0])
    # print(functions)
    for i in functions:
        # print(i)
        if i != 'var':
            non_var_index = functions.index(i)
            print(non_var_index)
            break
    for i in range(non_var_index, len(functions)):
        if functions[i] == 'var':
            print("ERROR:Variables not declared at the beginning")
            flag = 0
    return flag


def immediate():
    flag = 1
    for line in all_instructions:
        if "$" in line:
            k = line.split()
            imm = k[-1]
            if imm[1:].isdigit():
                imm = int(imm[1:])
                if not check_imm(imm):
                    flag = 0
            else:
                print("Immediate is not a numeric value or general syntax error")
                flag = 0
    return flag


def error_type_A(lst):
    flag = 1
    if len(lst) == 4:
        if not (lst[1] in reg.keys()) & (lst[2] in reg.keys()) & (lst[3] in reg.keys()):
            print("ERROR: Typos in register name")
            flag = 0
    else:
        print("ERROR: Syntax error")
        flag = 0
    return flag


def error_type_B(lst):
    flag = 1
    if len(lst) == 3:
        if not (lst[1] in reg.keys()):
            print("ERROR: Typos in register name")
            flag = 0
    else:
        print("ERROR: Syntax error")
        flag = 0
    return flag


def error_type_C(lst):
    flag = 1
    if len(lst) == 3:
        if not (lst[1] in reg.keys()) & (lst[2] in reg.keys()):
            print("ERROR: Typos in register name")
            flag = 0
    else:
        print("ERROR: Syntax error")
        flag = 0
    return flag

#need var wunly
def error_type_D(lst, labl, varl):  # call with var list. #ud var, label as var can be extended here.
    flag = 1
    if len(lst) == 3:
        if lst[1] in reg.keys():
            # modify to handle m_add error
            if lst[-1] in labl:
                flag = 0
                print("ERROR: Use of label as variable")
            elif (not (lst[2] in varl)):  # replace with condition if m_add is correct
                flag = 0
                print("ERROR: in m_add only variables can be used as m_add")

        else:
            flag = 0
            print("ERROR: Typos in register name")
            if lst[-1] + ":" in labl:
                print("ERROR: Use of label as variable")
    else:
        print("ERROR: Syntax error")
        flag = 0
    return flag

# use of label as var
def error_type_E(lst, varl):  # call with var list. #ud var, label as var can be extended here.
    flag = 0
    if len(lst) == 2:
        if lst[-1] + ":" in varl:
            flag = 0
            print("ERROR: Use of label as variable")

        elif not (lst[1] in varl):  # replace with condition if m_add is correct
            flag = 0
            print("ERROR: in m_add")
    else:
        flag = 0
        print("ERROR: Syntax error")
        if lst[-1] + ":" in  labels_list:
            print("ERROR: Use of label as variable")
    return flag


inst_type=[]
def identify_error_type(lst):
    flag = 1
    if lst[0] in ['mov']:
        if lst[-1][0] == '$':
            print("b")
            inst_type.append("b")
            flag = error_type_B(lst)
        else:
            print("c")
            flag = type_C(lst)
    elif lst[0] in op_type.get("A"):
        print("a")
        inst_type.append("a")
        flag = error_type_A(lst)
    elif lst[0] in op_type.get("B"):
        print("b")
        inst_type.append("b")
        flag = error_type_B(lst)
    elif lst[0] in op_type.get("C"):
        print("c")
        inst_type.append("c")
        flag = error_type_C(lst)
    elif lst[0] in op_type.get("D"):
        print("d")
        inst_type.append("d")
        flag = error_type_D(lst, labels_list, var)
        #print("d ka flag",flag)
    elif lst[0] in op_type.get("E"):
        print("e")
        inst_type.append("e")
        flag = error_type_E(lst,var)
    elif lst[0] in op_type.get("F"):
        print("f")
        inst_type.append("f")
        # flag= error_type_F(lst)
    else:
        print("ERROR: Typo in instruction name.")
        flag = 0
    #print("end ka flag",flag)
    return flag


pc = 0
# reading input file.
f = open('input.txt', 'r')
page = f.read()
all_instructions = [x.lstrip().rstrip() for x in page.split('\n') if x != ""]
#print("all_instructions: ", all_instructions, "\n", sep="")

tmp_words = []  # nested list to store all instructions
for line in all_instructions:
    words = line.split()
    tmp_words.append(words)
#print("tmp_words: ", tmp_words, "\n", sep="")


var, inst, labels_list, labels, var_dic = [], [], [], {}, {}
# classification of labels, var dec & instructions.

for line in tmp_words:
    if line[0] == "var":
        var.append(line[1])

    elif line[0][-1] == ":":
        labels[line[0]] = {pc, "mem_addr"}
        labels_list.append(line[0][0:-1])
        inst.append(line[1:])  # adding the instruction only not the name in the inst list
        pc += 1
    else:
        inst.append(line)
        pc += 1

var_counter= len(all_instructions) - len(var)
#print(var_counter)
for variable in var:
    var_dic[variable]= var_counter
    var_counter= var_counter + 1
#print("var: ", var, "\n", "inst: ", inst, "\n", "labels_list:", labels_list, "\n", sep="")



# checking all errors
def check_all_errors():
    flag = 1
    #if var_not_declared(all_instructions) != 1:
    if var_not_dec(inst,var) != 1:
        flag = 0
        print(flag, "1")
    if not_defined_at_beginning(tmp_words, all_instructions) != 1:
        flag = 0
        print(flag, "2")
    if hlt_checker(all_instructions, tmp_words) != 1:
        flag = 0
        print(flag, "3")
    if immediate() != 1:
        flag = 0
        print(flag, "4")
    if typos(inst) != 1:
        flag = 0
        print(flag, "5")
    if flag == 1:
        # runall
        print("runall")
    if flag == 0:
        print("error occured")
    return flag

def type_A(lst):
    opcode, r1, r2, r3 = lst[0], lst[1], lst[2], lst[3]
    return op_code.get(opcode) + '00' + reg.get(r1) + reg.get(r2) + reg.get(r3) + '\n'


def type_B(lst):
    opcode, r1, imm = lst[0], lst[1], lst[2]
    return op_code.get(opcode) + '0' + reg.get(r1) + imm_to_bin(imm[1:]) + '\n'


def type_C(lst):
    opcode, r1, r2 = lst[0], lst[1], lst[2]
    return op_code.get(opcode) + '00000' + reg.get(r1) + reg.get(r2) + '\n'


def type_D(lst):  # madd
    opcode, r1, m_add = lst[0], lst[1], str(imm_to_bin(var_dic.get(lst[2])))
    return op_code.get(opcode) + '0' + reg.get(r1) + m_add + '\n' # correct to get memory add and handle error here


def type_E(lst):
    opcode, m_add = lst[0], str(imm_to_bin(var_dic.get(lst[1])))
    return op_code.get(opcode) + '0000' + m_add + '\n'


def type_F(lst):
    opcode = lst[0]
    return op_code.get(opcode) + '00000000000'

def print_binary(inst,insttype):
    print(inst)
    print(insttype)
    out=""
    for i in range (0,len(insttype)):
        type=inst_type[i]
        if type=="a":
            out+=type_A(inst[i])
        elif type == "b":
            out+=type_B(inst[i])
        elif type == "c":
            out+=type_C(inst[i])
        elif type == "d":
            out+=type_D(inst[i])
        elif type == "e":
            out+=type_E(inst[i])
        elif type == "f":
            out+=type_F(inst[i])
    f = open('output.txt', 'w')
    f.write(out)

# generating and printing machine code
if check_all_errors():
    print("printing binary")
    print_binary(inst,inst_type)



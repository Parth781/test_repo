import re

class Symbol:
  def __init__(self, label, value, length, ar):
    self.label = label
    self.value = value
    self.length = length
    self.ar = ar

class Literal:
  def __init__(self, literal, value, length, ar):
    self.literal = literal
    self.value = value
    self.length = length
    self.ar = ar

def assign_literals(arr, lc, pseudo):
  mac_code.append([pseudo + '\n'])
  temp = []
  if len(arr) > 0:
    value = lc + (8 - (lc % 8))
    for l in arr:
      #print(l)
      literal = l
      obj = Literal(literal, value, 4, 'R')
      literal_table.append(obj)
      temp.append(value)
      value += 4

    del arr[:]
    return value
  
  return lc

pot = ['LTORG', 'START', 'END', 'USING', 'DROP', 'EQU', 'DC', 'DS']
mot = ['LA', 'SR', 'L', 'AR', 'A', 'ST', 'C', 'BNE', 'LR', 'BR']
len2 = ['SR', 'AR', 'LR', 'BR']

# pass 1
f = open('input1.txt', 'r+')
input_pgm = f.readlines()
f.close()

print(input_pgm)
print()

lc = 0
symbol_table = []
literal_table = []
temp_literals = []
mac_code = []
line_num = 0

for i in input_pgm:
  #print('lc ' + str(lc))
  line_num += 1
  
  split = re.split(r'[, ]', i)
  label = None
  split = list(filter(None, split)) 
  #print(split)
  if split[0] == '\n':
    continue

  if split[0] in mot:
    mac_code.append(split)
    if split[0] in len2:
      lc += 2
    else:
      lc += 4

    try:
      if split[2][0] == '=':
        temp_literals.append(split[2].strip())
    except IndexError:
      pass

  elif split[0].strip() in pot:     
    if split[0].strip() == 'LTORG' or split[0].strip() == 'END':
      lc = assign_literals(temp_literals, lc, split[0].strip())
    elif split[0].strip() == 'USING':
      mac_code.append(split)

  # label present
  else:    
    #print('label'+split[0])
    label = split[0].strip()
    code = split[1].strip()
    arg = split[2].strip()
    
    # found in pot
    if code in pot:
      if code == 'START':
        mac_code.append(split)
        obj = Symbol(label, lc, 1, 'R')
      elif code == 'EQU':
        if arg == '*':
          obj = Symbol(label, lc, 1, 'R')
        else:
          obj = Symbol(label, arg, 1, 'A')
      elif code == 'DS':
        value = lc
        mac_code.append(split)
        obj = Symbol(label, value, 4, 'R')
        value = 4*int(split[2][:-2])
        lc += value
      elif code == 'DC':
        value = lc
        mac_code.append(split)
        obj = Symbol(label, value, 4, 'R')
        value = 4*(len(split) - 2)
        lc += value
      else:
        mac_code.append(split)
        obj = Symbol(label, lc, 4, 'R')
        lc += 4
         
      symbol_table.append(obj) 

    # found in mot
    else:
      mac_code.append(split)
      if code in len2:
        obj = Symbol(label, lc, 2, 'R')
        lc += 2
      else:
        obj = Symbol(label, lc, 4, 'R')
        lc += 4
 
      symbol_table.append(obj)
 
     # skip this for END, LTORG
      try:
        if split[3][0] == '=':
          #print(arg)
          temp_literals.append(split[3].strip())
      except IndexError:
        pass

print() 
print('symbol table:')      
for k in symbol_table:
  print(k.label, end=' ')
  print(k.value, end=' ')
  print(k.length, end=' ')
  print(k.ar) 

print()
print('literal table:')
for k in literal_table:
  print(k.literal, end=' ')
  print(k.value, end=' ')
  print(k.length, end=' ')
  print(k.ar) 

print()
print('input to pass2:')
for m in mac_code:
  print(m) 

with open('output.txt', 'w') as output:
  for i in mac_code:
    string = ''
    for word in i:
      string = string + word + '\t'
    output.write(str(string))

print()
# end pass 1

# pass 2
base_table = []
machine_code = []

class BaseTable:
  def __init__(self, reg, value, avail='Y'):
    self.reg = reg
    self.value = value
    self.avail = avail

class MachineCode:
  def __init__(self, no, loc, instr, val):
    self.no = no
    self.loc = loc
    self.instr = instr
    self.val = val

def lookup_symbol(symbol):
  for s in symbol_table:
    if s.label == symbol:
      return s.value
  return -1

def lookup_literal(literal):
  for l in literal_table:
    if l.literal == literal:
      return l.value
  return -1

def isinteger(n):
  try:
    int(n)
  except ValueError:
    return False
  return True

def refine_literal(literal):
  if '(' in literal:
    literal = literal[literal.index('(')+1:-1]
    value = lookup_symbol(literal)
  else:
    value = literal[literal.index("'")+1:-1]
  
  return hex(int(value))

def find_BR(EA):
  d = {}
  for i in base_table:
    if i.avail == 'Y':
      d[i.reg] = [abs(i.value - EA), i.value]
  
  min_val = 999
  for key in d:
    if d[key][0] < min_val:
      BR = key
      content = d[key][1]

  return (BR , content)

def generate_code(split, lc):
  if split[0] == 'BNE':
    EA = lookup_symbol(split[1])
    value = 7
    index = 0
    split[0] = 'BC'
  else:
    index = 0
    if isinteger(split[1]):
      value = split[1]
    else:
      value = lookup_symbol(split[1])

    if split[-1][0] == '=':
      EA = lookup_literal(split[2])
    elif split[-1][-1] == ')':
      temp1 = split[2][:split[2].index('(')]
      temp2 = split[2][split[2].index('(')+1:split[2].index(')')]
      EA = lookup_symbol(temp1)
      index = lookup_symbol(temp2)
    else:
      EA = lookup_symbol(split[2])
      
  BR, content = find_BR(EA)
  offset = EA - content
  mac_code = str(value) + ',' + str(offset) + '(' + str(index) + ',' + BR + ')'
  obj = MachineCode(None, lc, split[0], mac_code)
  machine_code.append(obj)

f = open('output.txt', 'r+')
input_pgm = f.readlines()
f.close()
lc = 0

for i in input_pgm:
  #print(i.strip().split())
  split = i.strip().split()
  if len(split) == 0:
    continue

  if split[0] in mot:
    # RR
    if split[0] == 'BR':
      obj = MachineCode(None, lc, 'BCR', '15' + ',' + split[1])
      machine_code.append(obj)
      lc += 2
    elif split[0] in len2:     
      if not isinteger(split[1]):
        value1 = lookup_symbol(split[1])
      else:
        value1 = split[1]
      if not isinteger(split[2]):
        value2 = lookup_symbol(split[2])
      else:
        value2 = split[2]
      
      obj = MachineCode(None, lc, split[0], value1 + ',' + value2)
      machine_code.append(obj)
      lc += 2
    
    else:
      generate_code(split, lc)
      lc += 4

  elif split[0] in pot:
    if split[0] == 'USING':
      if split[1] == '*':
        obj = BaseTable(split[2], 0)
        base_table.append(obj)

      else:
        flag = False
        value = lookup_symbol(split[1])
        if isinteger(split[2]):
          for b in base_table:
            if b.reg == split[2]:
              flag = True
              b.value = value

          if flag == False:
            obj = BaseTable(split[2], value)
            base_table.append(obj)
        else:
          reg = lookup_symbol(split[2])
          value = lookup_symbol(split[1])
          obj = BaseTable(reg, value)
          base_table.append(obj)

    elif split[0] == 'LTORG':
      for l in literal_table:
        if l.value > lc:
          li = refine_literal(l.literal)
          obj = MachineCode(None, l.value, li, '')
          machine_code.append(obj)
          lc = l.value
      lc += 4

    elif split[0] == 'DROP':
      for b in base_table:
        if b.reg == split[1]:
          b.avail = 'N'

  else:
    code = split[1]
    if code in mot:
      split.remove(split[0])
      generate_code(split, lc)
      if code in len2:
        lc += 2
      else:
        lc += 4
    elif code in pot:
      if code == 'DS':
        ds_val = split[2][:-1]
        obj = MachineCode(None, lc, '', '')
        machine_code.append(obj)
        lc += 4*int(ds_val)
      elif code == 'DC':
        length = len(split) - 2
        for i in range(length):
          split[i+2] = split[i+2].replace("'", '')
          split[i+2] = split[i+2].replace("F", '')
          obj = MachineCode(None, lc, hex(int(split[i+2])), '')
          machine_code.append(obj) 
          lc += 4           

print()
print('base table:')
for i in base_table:
  print(i.reg, end=' ')
  print(i.value)

print()
print('machine code:')
for i in machine_code:
  print(i.loc, end=' ')
  print(i.instr, end=' ')
  print(i.val)
keywords = [
    'auto', 'break', 'case', 'const', 'char', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int',
    'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'volatile', 'void',
    'while'
]
 
operators = [
    '+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '(', ')'
]
functions = ['main', 'printf', 'scanf']
specials = ['{', '}', ';', '[', ']', ',']
literal = []
symbols = []
 
f = open('input.c', 'r+')
input_pgm = f.readlines()
f.close() 

print(input_pgm)
print()
word_after_split = []
for line in input_pgm:
	temp = line.split()
	print(temp)
	token = []
	
	for word in temp:	
		#print('word ' + word)
		end = 0	
		start = 0
		flag = False

		for char in word:
			
			if (char in operators or char in specials):
				if end != 0 and flag == False:
					token.append(word[start:end])
				#print(char)
				token.append(char)
				start = end + 1				
				end = end + 1
				flag = True

			else:
				end += 1
				flag = False
				#print(end, end='')

		if end != 0 and flag == False:
			token.append(word[start:end])	

	word_after_split.append(token)

print()
print(*word_after_split, sep='\n')
print()

'''
temp = re.split('(\W)', input_pgm)
temp = [x for x in temp if x != '\n' and x != '' and x != ' ']
print(temp)
'''

def is_number(n):
    try:
        float(n)   
    except ValueError:
        return False
    return True
  
final = []
for line in word_after_split:
	curr_line_token = []

	for i in line:
		token = ''

		if i in keywords:
			token = '<keyword#'+str(keywords.index(i))+'>'
		elif i in operators:
			token = '<operator#'+str(operators.index(i))+'>'
		elif i in functions:
			token = '<function#'+str(functions.index(i))+'>'
  	
		elif i in specials:
			token = '<specials#'+str(specials.index(i))+'>'

		else:
			if(is_number(i)):
				if i in literal:
					token = '<literal#'+str(literal.index(i))+'>'
				else:
					literal.append(i)
					token = '<literal#'+str(literal.index(i))+'>'
			else:
				if i in symbols:
					token = '<symbols#'+str(symbols.index(i))+'>'
				else:
					symbols.append(i)
					token = '<symbols#'+str(symbols.index(i))+'>'

		curr_line_token.append(token)
	final.append(curr_line_token)

print(*final, sep='\n')
print(literal)
print(symbols)
print()
print()

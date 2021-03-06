bits = 10
cSize = 8 								#log2 of the total regs in CU
puLoops = 4								#number of PU loops per cycle
GHz  = 4.0
cycles = 0

mem = [1]
with open('File3.lx', encoding = 'utf-16-le') as file: s = file.read(256)[1:]
mem = ([1]+[ord(i) for i in s]+[0]*((1<<bits)-1))[:(1<<bits)]	#all mem
# print(s)
# print(mem)

ei  = [0]*5								#explicit input for PU

file = open('MachineLog.csv', 'w')
[file.write(str(i)+',') for i in range(1<<bits)], file.write('\n')
while mem[-1]<=1<<bits-1:
	file.write(str(mem)[1:-1]+'\n')

	size  = (mem[0]>>cSize)+1			#extract from first bits
	fetch = mem[0]&(1<<cSize)-1			#extract from last  bits
	
	mem[0]+=2*size 						#fetch increment
	
	#reset destination values to support OR operation
	for i in range(size):
		if mem[fetch+2*i] not in range(256, 261):
			mem[mem[fetch+2*i]    ] = 0   #But what if it's one of the sources?
		else:ei[mem[fetch+2*i]-256] = 0	  #if destination happens to be ei

	#assign to destination values
	for i in range(size):
		if mem[fetch+2*i] not in range(256, 261):
			mem[mem[fetch+2*i]    ] |= mem[mem[fetch+1+2*i]]
		else:ei[mem[fetch+2*i]-256] |= mem[mem[fetch+1+2*i]]

	# if mem[0] == fetch: raise RecursionError('Stagnating fetch')


	# PU
	for _ in range(puLoops):

		ins = mem[256:261]+[255^i for i in mem[256:261]]+ei	#NIE
		gReg = 261							#start from first PU grid reg
		for inReg in ins:					#iterates over each bit
			for shifts in range(bits-1, -1, -1):	#with this (msb to lsb)
				if (inReg>>shifts)&1:		#that expression returns the bit
					for i in range(5):		#for each reg of the bit
					  mem[256+i] |= mem[gReg]	#main operation
					  gReg += 1			#inc gReg after processing that reg

				else: gReg += 5			#inc gReg to compensate not processing

	print('\r', end = '', flush = True)
	for i in mem[1011:-1]: print(chr(i), end = '')

	cycles += 1

	# All the parts and their indices

	# Part		From	To		Total
	# CU		0		255		256
	# PU outs	256		260		5
	# PU grid	261		1010	750
	# Extra		1011	1023	13
	# Total		0		1023	1024

print(f'\nProcess completed in {cycles} cycles. ({cycles/GHz}ns on {GHz}GHz)')
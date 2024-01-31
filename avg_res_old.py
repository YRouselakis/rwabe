'''
Getting Averaged results from the old schemes
'''
from toolbox.pairinggroup import *
from abenc_bsw07 import *
from abenc_waters09 import *
from abenc_lsw08 import *

#formatting function for time
def ft(timeReal):
	string = str(timeReal)
	ind = string.find(".")
	spcs = 7 - ind
	tmp = ""
	for i in range(spcs):
		tmp += " "
	string = tmp + string
	
		
	return string
	
def pad(s, sz = 10):
	length = len(s)
	buff = ""
	for i in range(sz-length):
		buff += " "
	return buff + s 

#number of iterations (BE CAREFUL WITH THIS!)
N = 10

#curves = [ 'SS512' ]
curves = [ 'SS512', 'SS1024', 'MNT159', 'MNT201', 'MNT224' ]
tests = ['STP', 'KG4', 'KG8', 'KG12', 'EC4', 'EC8', 'EC12', 'DE4', 'DE8', 'DE12']
schemes = ['BSW07','WAT09']

results = { scheme:{ curve:None for curve in curves } for scheme in schemes }

for curve in curves:
	groupObj = PairingGroup(curve)

	#BSW07
	print("CPABE BSW07 ",curve)
	scheme = CPabe_BSW07(groupObj)
	times = { test:0.0 for test in tests}
	
	#print(times)

	for i in range(0,N):
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		(pk,mk) = scheme.setup()
		EndBenchmark(ID)
		times['STP'] += GetGeneralBenchmarks(ID)[RealTime]
	
		########################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		sk1 = scheme.keygen(pk, mk, ['ONE', 'SIX', 'THREE', 'ELEVEN'])
		EndBenchmark(ID)
		times['KG4'] += GetGeneralBenchmarks(ID)[RealTime]
		
		######################################################
		
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		sk2 = scheme.keygen(pk, mk, ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT'])
		EndBenchmark(ID)
		times['KG8'] += GetGeneralBenchmarks(ID)[RealTime]
		
		######################################################

		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		sk3 = scheme.keygen(pk, mk, ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE'])
		EndBenchmark(ID)
		times['KG12'] += GetGeneralBenchmarks(ID)[RealTime]
				
		######################################################
		
		m = groupObj.random(GT)
		policy = '((four or three) and (three or one))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.encrypt(pk, m, policy)
		EndBenchmark(ID)
		times['EC4'] += GetGeneralBenchmarks(ID)[RealTime]
			
		#####################################################
			
		m = groupObj.random(GT)
		policy = '(((four or three) and (three or one)) and ((six or seven) and (nine or eleven)))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.encrypt(pk, m, policy)
		EndBenchmark(ID)
		times['EC8'] += GetGeneralBenchmarks(ID)[RealTime]
		
		#####################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.decrypt(pk, sk1, ct)
		EndBenchmark(ID)
		times['DE4'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
			
		#####################################################
			
		m = groupObj.random(GT)
		policy = '(((four and three) and (seven and one)) and ((six or seven) and (nine or eleven))) and ((ten or eight) and (twelve or six))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.encrypt(pk, m, policy)
		EndBenchmark(ID)
		times['EC12'] += GetGeneralBenchmarks(ID)[RealTime]
		
		#####################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.decrypt(pk, sk3, ct)
		EndBenchmark(ID)
		times['DE8'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
			
		#####################################################
		
		m = groupObj.random(GT)
		policy = '(((one and two) and (three and four)) and ((five and six) and (seven and eight))) and ((nine and ten) and (eleven and twelve))'
		ct = scheme.encrypt(pk, m, policy)
		
		#####################################################

		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.decrypt(pk, sk3, ct)
		EndBenchmark(ID)
		times['DE12'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
		
		#####################################################


	for (k,v) in times.items():
		times[k] = round((v * 1000) / N, 1)
	
	results['BSW07'][curve] = times
	
	################################################################
	################################################################
	################################################################
	################################################################
	################################################################
	################################################################
	################################################################
	
	#WAT09
	print("CPABE WAT09 ",curve)
	scheme = CPabe09(groupObj)
	times = { test:0.0 for test in tests}
	
	#print(times)

	for i in range(0,N):
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		(mk, pk) = scheme.setup()			# changed the order of outputs
		EndBenchmark(ID)
		times['STP'] += GetGeneralBenchmarks(ID)[RealTime]
	
		########################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		sk1 = scheme.keygen(pk, mk, ['ONE', 'SIX', 'THREE', 'ELEVEN'])
		EndBenchmark(ID)
		times['KG4'] += GetGeneralBenchmarks(ID)[RealTime]
		
		######################################################
		
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		sk2 = scheme.keygen(pk, mk, ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT'])
		EndBenchmark(ID)
		times['KG8'] += GetGeneralBenchmarks(ID)[RealTime]
		
		######################################################

		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		sk3 = scheme.keygen(pk, mk, ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE'])
		EndBenchmark(ID)
		times['KG12'] += GetGeneralBenchmarks(ID)[RealTime]
				
		######################################################
		
		m = groupObj.random(GT)
		policy = '((four or three) and (three or one))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.encrypt(pk, m, policy)
		EndBenchmark(ID)
		times['EC4'] += GetGeneralBenchmarks(ID)[RealTime]
			
		#####################################################
			
		m = groupObj.random(GT)
		policy = '(((four or three) and (three or one)) and ((six or seven) and (nine or eleven)))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.encrypt(pk, m, policy)
		EndBenchmark(ID)
		times['EC8'] += GetGeneralBenchmarks(ID)[RealTime]
		
		#####################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.decrypt(pk, sk1, ct)
		EndBenchmark(ID)
		times['DE4'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
			
		#####################################################
			
		m = groupObj.random(GT)
		policy = '(((four and three) and (seven and one)) and ((six or seven) and (nine or eleven))) and ((ten or eight) and (twelve or six))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.encrypt(pk, m, policy)
		EndBenchmark(ID)
		times['EC12'] += GetGeneralBenchmarks(ID)[RealTime]
		
		#####################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.decrypt(pk, sk3, ct)
		EndBenchmark(ID)
		times['DE8'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
			
		#####################################################
		
		m = groupObj.random(GT)
		policy = '(((one and two) and (three and four)) and ((five and six) and (seven and eight))) and ((nine and ten) and (eleven and twelve))'
		ct = scheme.encrypt(pk, m, policy)
		
		#####################################################

		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.decrypt(pk, sk3, ct)
		EndBenchmark(ID)
		times['DE12'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
		
		#####################################################


	for (k,v) in times.items():
		times[k] = round((v * 1000) / N, 1)
	
	results['WAT09'][curve] = times

#print(results)

print(" ")
print(N," iterations")


for k in range(len( schemes )):
	print("********* SCHEME:", schemes[k], "*****************" )

	buffT = pad("",8)
	for j in range(len( tests )):
		buffT += pad(tests[j], 9)
	print(buffT)
	

	for i in range(len(curves)):
		buff = pad(curves[i] + ": ",8)
		for j in range(len( tests )):
			buff += ft(results[schemes[k]][curves[i]][tests[j]])
		print(buff)

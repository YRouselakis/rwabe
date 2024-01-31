'''
Getting Averaged results
'''
from toolbox.pairinggroup import *
from maabe_rw12 import *

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
N = 4

#curves = [ 'SS512' ]
curves = [ 'SS512', 'SS1024', 'MNT159', 'MNT201', 'MNT224' ]
tests = ['GS', 'AS', 'KG4', 'KG8', 'KG12', 'EC4', 'EC8', 'EC12', 'DE4', 'DE8', 'DE12']

results = { curve:None for curve in curves }

for curve in curves:
	groupObj = PairingGroup(curve)

	#RW MAABE
	print("RW MAABE ",curve)
	scheme = MAABE_RW12(groupObj)
	times = { test:0.0 for test in tests}
	
	#print(times)


	for i in range(0,N):
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		gp = scheme.GlobalSetup()
		EndBenchmark(ID)
		times['GS'] += GetGeneralBenchmarks(ID)[RealTime]
	
		########################################################
		
		pks, sks = {}, {}
		
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		(pk,sk) = scheme.AuthSetup(gp,"UT")
		EndBenchmark(ID)
		times['AS'] += GetGeneralBenchmarks(ID)[RealTime]
		
		pks[pk['name']] = pk
		sks[sk['name']] = sk
	
		(pk,sk) = scheme.AuthSetup(gp,"OU")
		pks[pk['name']] = pk
		sks[sk['name']] = sk
		
		(pk,sk) = scheme.AuthSetup(gp,"US")
		pks[pk['name']] = pk
		sks[sk['name']] = sk
		
		(pk,sk) = scheme.AuthSetup(gp,"MS")
		pks[pk['name']] = pk
		sks[sk['name']] = sk
		
		#######################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		key = scheme.KeyGen(gp, "YANNIS", sks, {"STUDENT@UT", "PHD@UT", "GREEK@US", "RIVAL@OU"})
		EndBenchmark(ID)
		times['KG4'] += GetGeneralBenchmarks(ID)[RealTime]
		
		######################################################

		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		key2 = scheme.KeyGen(gp, "BRENT", sks, {"PROFESSOR@UT", "STAFF@UT", "FACULTY@UT", "VISITOR@OU", "LECTURER@OU", "CITIZEN@US", "NATIVE@US", "RIVAL@OU"})
		EndBenchmark(ID)
		times['KG8'] += GetGeneralBenchmarks(ID)[RealTime]
		
		######################################################

		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		key3 = scheme.KeyGen(gp, "OMKANT", sks, 
		{"POSTDOC@UT", "STAFF@UT", "GYM@UT", "VISITOR@OU", "LECTURER@OU", "INDIAN@US", "GREENCARD@US", "RIVAL@OU",
		"RESIDENT@US", "WORK@US", "EMPLOYEE@MS", "CRYPTO@UT"})
		EndBenchmark(ID)
		times['KG12'] += GetGeneralBenchmarks(ID)[RealTime]
		
		######################################################
		
		m = scheme.randomMessage()
		policy = '(STUDENT@UT or PROFESSOR@OU) and (STUDENT@UT or MASTERS@OU)'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.Encrypt(gp, pks, m, policy)
		EndBenchmark(ID)
		times['EC4'] += GetGeneralBenchmarks(ID)[RealTime]
			
		#####################################################
		
		m = scheme.randomMessage()
		policy = '((PROFESSOR@UT or PROFESSOR@OU) and (STAFF@UT or MASTERS@OU)) and ((CITIZEN@US or INDIAN@US) and (RIVAL@OU or MASTERS@OU))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.Encrypt(gp, pks, m, policy)
		EndBenchmark(ID)
		times['EC8'] += GetGeneralBenchmarks(ID)[RealTime]
		
		#####################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.Decrypt(gp, key2, ct)
		EndBenchmark(ID)
		times['DE4'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
			
		#####################################################
		
		m = scheme.randomMessage()
		policy = '(((POSTDOC@UT and GYM@UT) and (EMPLOYEE@MS and STAFF@UT)) and ((CITIZEN@US or INDIAN@US) and (RIVAL@OU or MASTERS@OU))) and ((GREENCARD@US or GREEK@US) and (UNDER@OU or CRYPTO@UT))'
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		ct = scheme.Encrypt(gp, pks, m, policy)
		EndBenchmark(ID)
		times['EC12'] += GetGeneralBenchmarks(ID)[RealTime]
		
		#####################################################
	
		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.Decrypt(gp, key3, ct)
		EndBenchmark(ID)
		times['DE8'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
			
		#####################################################
		
		m = scheme.randomMessage()
		policy = '(POSTDOC@UT and STAFF@UT) and (GYM@UT and VISITOR@OU) and (LECTURER@OU and INDIAN@US) and (GREENCARD@US and RIVAL@OU) and (RESIDENT@US and WORK@US) and (EMPLOYEE@MS and CRYPTO@UT)'
		ct = scheme.Encrypt(gp, pks, m, policy)
		
		#####################################################

		ID = InitBenchmark()
		StartBenchmark(ID, [RealTime])
		res = scheme.Decrypt(gp, key3, ct)
		EndBenchmark(ID)
		times['DE12'] += GetGeneralBenchmarks(ID)[RealTime]

		if res != m:
			print('Unsuccessful Decryption')
			break
			
		#####################################################


	for (k,v) in times.items():
		times[k] = round((v * 1000) / N, 1)
	
	results[curve] = times

#print(results)

print(" ")
print(N," iterations")

buffT = pad("",8)
for j in range(len( tests )):
	buffT += pad(tests[j], 9)
print(buffT)
	

for i in range(len(curves)):
	buff = pad(curves[i] + ": ",8)
	for j in range(len( tests )):
		buff += ft(results[curves[i]][tests[j]])
	print(buff)
		


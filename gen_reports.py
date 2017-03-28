import pandas as pd 


def load_data(posttest_dist = True, course_codes = True):
	'''
	Loads the data from excel files downloaded from the corresponding google sheets
	and outputs them as pandas DataFrames

	Inputs: booleans designating which data to return
	'''
	#load sequences
	if posttest_dist == True:
		pretests = pd.read_excel('SY16-17 SRI posttest distribution.xlsx', 
			sheetname = 'pretests')
		pretests = pretests[pretests['Assignment'] != 'SRI']
		spring_enrollement = pd.read_excel('SY16-17 SRI posttest distribution.xlsx', 
			sheetname = 'spring enrollement')
	if course_codes == True:
		codes = pd.read_excel('Computer & CS4All course code master list.xlsx', 
			sheetname = 'codes')
		codes = codes[codes['Course type'] == 'FIT']
	#return sequences
	if posttest_dist == True and course_codes == True:
		return pretests, spring_enrollement, codes 
	elif posttest_dist == True:
		return pretest, spring_enrollement
	elif course_codes = True:
		return codes 

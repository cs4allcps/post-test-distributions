import pandas as pd 
import csv
import requests


def load_data(posttest_dist = True, course_codes = True):
    '''
    Loads the data from excel files downloaded from the corresponding google sheets
    and outputs them as pandas DataFrames

    (In Computer & CS4All course code master list.xlsx, the column name 'Course type'
    was manually moved up to the same level as the other column names so pandas could
    properly index the columns)

    Inputs: booleans designating which data to return
    '''
    #load sequences
    if posttest_dist == True:
        pretests = pd.read_excel('SY16-17 SRI posttest distribution.xlsx', 
            sheetname = 'pretests', index_col = None)
        pretests = pretests[pretests['Assignment'] != 'SRI']
        spring_enrollment = pd.read_excel('SY16-17 SRI posttest distribution.xlsx', 
            sheetname = 'spring enrollment', index_col = None)
    if course_codes == True:
        codes = pd.read_excel('Computer & CS4All course code master list.xlsx', 
            sheetname = 'codes', index_col = None)
        codes = codes[codes['Course type'] == 'FIT']
    #return sequences
    if posttest_dist == True and course_codes == True:
        return pretests, spring_enrollment, codes 
    elif posttest_dist == True:
        return pretest, spring_enrollment
    elif course_codes == True:
        return codes 

def sections_report():
    '''
    Generates a csv with a row for each section of ECS and columns for teacher name,
    teacher email, school code, school name, course code, course name, and section enrollement
    '''
    pretests, spring_enrollment, codes = load_data()
    #filter out CTE and other non-ECS courses
    included_courses = codes['Course code'].tolist()
    sections = spring_enrollment[spring_enrollment['SubjectNumber'].isin(included_courses)]
    #write to csv
    with open('ecs_sections.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['teacher_name', 'teacher_email', 'school_code', 'school_name', 'course_code',
            'course_name', 'enrollment'])
        for row in range(len(sections)):
            info = [sections['StaffCompleteName'].iloc[row], sections['StaffEmail'].iloc[row], 
                sections['SchoolID'].iloc[row], sections['SchoolName'].iloc[row], 
                sections['SubjectNumber'].iloc[row], sections['SubjectName'].iloc[row],
                sections['StudentEnr'].iloc[row]]
            w.writerow(info)

def schools_report():
    '''
    Generates a csv with a row for each CPS high school with school name, school code, 
    number of ECS sections and total ECS enrollment
    '''
    pretests, spring_enrollment, codes = load_data()
    #filter out CTE and other non-ECS courses
    included_courses = codes['Course code'].tolist()
    sections = spring_enrollment[spring_enrollment['SubjectNumber'].isin(included_courses)]
    url = 'https://data.cityofchicago.org/resource/76dk-7ieb.json?is_high_school=Y'
    resp = requests.get(url)
    schools = pd.read_json(resp.text) #pandas dataframe with high school profile information
    high_schools = schools['school_id'].tolist()
    with open('ecs_schools_report.csv', 'w') as f:
        w = csv.writer(f)
        w.writerow(['school_name', 'school_id', 'ecs_sections', 'ecs_enrollment'])
        for school_id in high_schools:
            school = sections[sections['SchoolID'] == school_id]
            name = schools[schools['school_id'] == school_id]['short_name'].iloc[0]
            num_sections = len(school)
            enrollment = sum(school['StudentEnr'].tolist())
            w.writerow([name, school_id, num_sections, enrollment])



#!/usr/bin/env python3
"""
Sample Data Generator
Creates sample Excel files for testing the course data validator
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample course data with various valid and invalid entries"""
    
    # Sample data with intentional errors for testing
    data = {
        'Instituti': [108, 108, 108, 108, 108, 108, 108, 108, 108, 108],
        'Course I': [986855, 986856, 986857, 986858, 986859, 986860, 986861, 986862, 986863, 986864],
        'Course TDegree': ['Foundation FDA', 'Foundation FDA', 'Foundation FDA', 'Foundation FDA', 'Foundation FDA',
                          'Foundation FDA', 'Foundation FDA', 'Foundation FDA', 'Foundation FDA', 'Foundation FDA'],
        'Course': ['Business', 'Business', 'Business', 'Film, TV and Media', 'Computer Science',
                  'Engineering', 'Medicine', 'Law', 'Arts', 'Science'],
        'L3 Taggi': ['Business', 'Supply Chain', 'Supply Chain', 'Film Studies', 'Computer Science',
                    'Mechanical Engineering', 'Medicine', 'Law', 'Fine Arts', 'Physics'],
        'Course sCourse': ['2024-09-015720', '2024-09-0-15720', '2024-09-015720', '2024-09-017040', '2024-09-015720',
                          '2024-09-015720', '2024-09-015720', '2024-09-015720', '2024-09-015720', '2024-09-015720'],
        'LApplicati': [152010, 1520, 151010, 170010, 152010, 152010, 152010, 152010, 152010, 152010],
        'Applicati': ['NULL,NUL', 'NULL,NUL', 'NULL,NUL', 'NULL,NUL', 'NULL,NUL',
                     'NULL,NUL', 'NULL,NUL', 'NULL,NUL', 'NULL,NUL', 'NULL,NUL'],
        'Course LCourse SShow': ['https://www.example.com/course1Open, Ope No', 
                                'https://www.example.com/course2Open, Ope No',
                                'https://www.example.com/course3Open, Ope No',
                                'https://www.example.com/course4Open, Ope No',
                                'https://www.example.com/course5Open, Ope No',
                                'https://www.example.com/course6Open, Ope No',
                                'https://www.example.com/course7Open, Ope No',
                                'https://www.example.com/course8Open, Ope No',
                                'https://www.example.com/course9Open, Ope No',
                                'https://www.example.com/course10Open, Ope No'],
        'Study M': ['Full Time', 'Full Time', 'Full Time', 'Full Time', 'Full Time',
                   'Full Time', 'Full Time', 'Full Time', 'Full Time', 'Full Time'],
        'Previous': ['High School', 'High School', 'High School', 'High School', 'High School',
                    'High School', 'High School', 'High School', 'High School', 'High School'],
        'Commissionable': ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes']
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some intentional errors for testing
    # Error 1: Non-numeric Institution ID
    df.loc[5, 'Instituti'] = 'ABC'
    
    # Error 2: Duplicate Course ID
    df.loc[6, 'Course I'] = 986855
    
    # Error 3: Course name doesn't start with capital
    df.loc[7, 'Course'] = 'computer science'
    
    # Error 4: Blank L3 Tagging
    df.loc[8, 'L3 Taggi'] = ''
    
    # Error 5: Invalid date format
    df.loc[9, 'Course sCourse'] = '2024/09/01'
    
    # Error 6: Invalid Study Mode
    df.loc[0, 'Study M'] = 'Online'
    
    # Error 7: Invalid URL (will cause 404)
    df.loc[1, 'Course LCourse SShow'] = 'https://httpstat.us/404Open, Ope No'
    
    # Error 8: Course name with wrong capitalization
    df.loc[2, 'Course'] = 'Business And Management'
    
    # Error 9: Blank Degree Type
    df.loc[3, 'Course TDegree'] = ''
    
    # Error 10: Invalid Course Status
    df.loc[4, 'Course LCourse SShow'] = 'https://www.example.com/course5Pending, Pen Yes'
    
    return df

def create_extended_sample_data():
    """Create a larger sample dataset with more variety"""
    
    # Generate more data
    num_rows = 50
    
    # Base data
    institutions = [108, 109, 110, 111, 112]
    course_types = ['Foundation FDA', 'Bachelor', 'Master', 'PhD', 'Diploma']
    course_names = ['Business', 'Computer Science', 'Engineering', 'Medicine', 'Law', 'Arts', 'Science', 
                   'Economics', 'Psychology', 'History', 'Literature', 'Mathematics', 'Physics', 'Chemistry']
    l3_tags = ['Business', 'Computer Science', 'Mechanical Engineering', 'Medicine', 'Law', 'Fine Arts', 
              'Physics', 'Economics', 'Psychology', 'History', 'Literature', 'Mathematics', 'Chemistry']
    study_modes = ['Full Time', 'Part Time']
    previous_education = ['High School', 'A-Levels', 'IB Diploma', 'Foundation Year']
    
    data = {
        'Instituti': [random.choice(institutions) for _ in range(num_rows)],
        'Course I': list(range(100000, 100000 + num_rows)),
        'Course TDegree': [random.choice(course_types) for _ in range(num_rows)],
        'Course': [random.choice(course_names) for _ in range(num_rows)],
        'L3 Taggi': [random.choice(l3_tags) for _ in range(num_rows)],
        'Course sCourse': [f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}15720" for _ in range(num_rows)],
        'LApplicati': [random.randint(10000, 200000) for _ in range(num_rows)],
        'Applicati': ['NULL,NUL' for _ in range(num_rows)],
        'Course LCourse SShow': [f"https://www.example.com/course{i}Open, Ope No" for i in range(num_rows)],
        'Study M': [random.choice(study_modes) for _ in range(num_rows)],
        'Previous': [random.choice(previous_education) for _ in range(num_rows)],
        'Commissionable': ['Yes' for _ in range(num_rows)]
    }
    
    df = pd.DataFrame(data)
    
    # Add some errors
    error_indices = random.sample(range(num_rows), 15)
    
    for i, idx in enumerate(error_indices):
        if i == 0:
            df.loc[idx, 'Instituti'] = 'ABC'  # Non-numeric
        elif i == 1:
            df.loc[idx, 'Course I'] = 100000  # Duplicate
        elif i == 2:
            df.loc[idx, 'Course'] = 'computer science'  # Lowercase start
        elif i == 3:
            df.loc[idx, 'L3 Taggi'] = ''  # Blank
        elif i == 4:
            df.loc[idx, 'Course sCourse'] = '2024/09/01'  # Wrong format
        elif i == 5:
            df.loc[idx, 'Study M'] = 'Online'  # Invalid mode
        elif i == 6:
            df.loc[idx, 'Course LCourse SShow'] = 'https://httpstat.us/404Open, Ope No'  # 404 URL
        elif i == 7:
            df.loc[idx, 'Course'] = 'Business And Management'  # Wrong capitalization
        elif i == 8:
            df.loc[idx, 'Course TDegree'] = ''  # Blank
        elif i == 9:
            df.loc[idx, 'Course LCourse SShow'] = 'https://www.example.com/coursePending, Pen Yes'  # Invalid status
        elif i == 10:
            df.loc[idx, 'Course'] = 'Engineering With Technology'  # Wrong conjunction capitalization
        elif i == 11:
            df.loc[idx, 'Course sCourse'] = '2024-13-01'  # Invalid date
        elif i == 12:
            df.loc[idx, 'Study M'] = 'Fulltime'  # Wrong format
        elif i == 13:
            df.loc[idx, 'Course LCourse SShow'] = 'https://invalid-url-formatOpen, Ope No'  # Invalid URL
        elif i == 14:
            df.loc[idx, 'Commissionable'] = 'Maybe'  # Invalid value
    
    return df

def main():
    """Main function to create sample data files"""
    print("Creating sample data files...")
    
    # Create basic sample data
    df_basic = create_sample_data()
    df_basic.to_excel('sample_course_data.xlsx', index=False)
    print("Created: sample_course_data.xlsx")
    
    # Create extended sample data
    df_extended = create_extended_sample_data()
    df_extended.to_excel('sample_course_data_extended.xlsx', index=False)
    print("Created: sample_course_data_extended.xlsx")
    
    # Create CSV version
    df_basic.to_csv('sample_course_data.csv', index=False)
    print("Created: sample_course_data.csv")
    
    print("\nSample data files created successfully!")
    print("Files created:")
    print("- sample_course_data.xlsx (10 rows with intentional errors)")
    print("- sample_course_data_extended.xlsx (50 rows with more variety)")
    print("- sample_course_data.csv (CSV version)")
    
    print("\nIntentional errors included for testing:")
    print("- Non-numeric Institution IDs")
    print("- Duplicate Course IDs")
    print("- Course names not starting with capital letters")
    print("- Blank required fields")
    print("- Invalid date formats")
    print("- Invalid Study Mode values")
    print("- URLs that return 404 errors")
    print("- Wrong capitalization in course names")
    print("- Invalid status values")

if __name__ == "__main__":
    main()

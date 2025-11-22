#!/usr/bin/env python3
"""
Course Data Validators
Contains all validation functions for course data validation
"""

import re
import requests
from urllib.parse import urlparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
import pandas as pd

class CourseValidators:
    def __init__(self):
        # Define allowed values for different fields
        self.allowed_statuses = ['Open', 'Closed']
        self.allowed_study_modes = ['Full time', 'Part time']
        self.allowed_show_values = ['Yes', 'No']
        
        # Define conjunctions that should be lowercase in course names
        self.conjunctions = [
            'and', 'with', 'by', 'of', 'the', 'in', 'on', 'at', 'to', 'for', 
            'from', 'up', 'about', 'into', 'through', 'during', 'before', 
            'after', 'above', 'below', 'between', 'among', 'within', 'without',
            'against', 'toward', 'towards', 'upon', 'under', 'over', 'across'
        ]
    
    def validate_institution_id(self, value: Union[str, int, float]) -> Dict[str, Union[bool, str]]:
        """
        Validate Institution Id - must be numeric
        
        Args:
            value: The institution ID value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or value == '':
            return {'valid': False, 'message': 'Institution Id cannot be blank'}
        
        try:
            float(str(value))
            return {'valid': True, 'message': 'Valid institution ID'}
        except ValueError:
            return {'valid': False, 'message': 'Institution Id must be numeric'}
    
    def validate_course_id(self, value: Union[str, int, float], all_course_ids: List) -> Dict[str, Union[bool, str]]:
        """
        Validate Course Id - must be numeric and unique
        
        Args:
            value: The course ID value to validate
            all_course_ids: List of all course IDs to check for uniqueness
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or value == '':
            return {'valid': False, 'message': 'Course Id cannot be blank'}
        
        # Check if numeric
        try:
            float(str(value))
        except ValueError:
            return {'valid': False, 'message': 'Course Id must be numeric'}
        
        # Check if unique
        if all_course_ids.count(value) > 1:
            return {'valid': False, 'message': 'Course Id must be unique'}
        
        return {'valid': True, 'message': 'Valid course ID'}
    
    def validate_course_name(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Course Name - must start with capital letter and conjunctions should be lowercase
        
        Args:
            value: The course name to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or value == '':
            return {'valid': False, 'message': 'Course Name cannot be blank'}
        
        course_name = str(value).strip()
        
        # Check if starts with capital letter
        if not course_name[0].isupper():
            return {'valid': False, 'message': 'Course Name must start with capital letter'}
        
        # Check conjunctions
        words = course_name.split()
        for i, word in enumerate(words):
            if i > 0 and word.lower() in self.conjunctions and word[0].isupper():
                return {
                    'valid': False, 
                    'message': f'Conjunction "{word}" should be lowercase'
                }
        
        return {'valid': True, 'message': 'Valid course name'}
    
    def validate_l3_tagging(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate L3 Tagging - must not be blank
        
        Args:
            value: The L3 tagging value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'L3 Tagging must not be blank'}
        
        return {'valid': True, 'message': 'Valid L3 tagging'}
    
    def validate_degree_type(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Degree Type - must not be blank
        
        Args:
            value: The degree type value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'Degree Type must not be blank'}
        
        return {'valid': True, 'message': 'Valid degree type'}
    
    def validate_course_type(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Course Type - must not be blank
        
        Args:
            value: The course type value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'Course Type must not be blank'}
        
        return {'valid': True, 'message': 'Valid course type'}
    
    def validate_course_start_date(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Course Start Date - must be in YYYY-MM-DD format
        
        Args:
            value: The course start date value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'Course start date cannot be blank'}
        
        date_str = str(value).strip()
        
        # Handle multiple dates separated by commas
        if ',' in date_str:
            dates = [d.strip() for d in date_str.split(',')]
        else:
            dates = [date_str]
        
        for date in dates:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return {'valid': False, 'message': f'Invalid date format: {date}. Must be YYYY-MM-DD'}
        
        return {'valid': True, 'message': 'Valid course start date'}
    
    def validate_course_level_url(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Course Level URL - must be working URLs (no 404s)
        
        Args:
            value: The URL value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'Course Level URL cannot be blank'}
        
        urls = str(value).split(',')
        errors = []
        
        for url in urls:
            url = url.strip()
            if not url:
                continue
            
            # Check URL format
            try:
                result = urlparse(url)
                if not all([result.scheme, result.netloc]):
                    errors.append(f'Invalid URL format: {url}')
                    continue
            except:
                errors.append(f'Invalid URL format: {url}')
                continue
            
            # Check if URL is working with smarter error handling
            try:
                # Use a more realistic user agent to avoid being blocked
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                response = requests.head(url, timeout=10, allow_redirects=True, headers=headers)
                
                # Only flag truly broken URLs
                if response.status_code == 404:
                    errors.append(f'URL returns 404 (Not Found): {url}')
                elif response.status_code == 410:
                    errors.append(f'URL returns 410 (Gone): {url}')
                elif response.status_code == 500:
                    errors.append(f'URL returns 500 (Server Error): {url}')
                elif response.status_code == 502:
                    errors.append(f'URL returns 502 (Bad Gateway): {url}')
                elif response.status_code == 503:
                    errors.append(f'URL returns 503 (Service Unavailable): {url}')
                elif response.status_code == 504:
                    errors.append(f'URL returns 504 (Gateway Timeout): {url}')
                # Don't flag 403 (Forbidden) as it often means the URL exists but blocks bots
                # Don't flag 401 (Unauthorized) as it might be a valid page requiring login
                # Don't flag 429 (Too Many Requests) as it's temporary
                
            except requests.exceptions.Timeout:
                errors.append(f'URL timeout (server not responding): {url}')
            except requests.exceptions.ConnectionError:
                errors.append(f'URL connection error (server unreachable): {url}')
            except requests.exceptions.RequestException as e:
                # Only flag if it's a clear connection issue, not a 403/401
                if '403' not in str(e) and '401' not in str(e):
                    errors.append(f'URL not accessible: {url}')
        
        if errors:
            return {'valid': False, 'message': '; '.join(errors)}
        
        return {'valid': True, 'message': 'All URLs are working'}
    
    def validate_course_intake_ids(self, intake_ids: str, start_dates: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Course Intake IDs - count must match start dates count and must be unique
        
        Args:
            intake_ids: The intake IDs value to validate
            start_dates: The corresponding start dates value
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(intake_ids) or pd.isna(start_dates):
            return {'valid': False, 'message': 'Course Intake IDs and Course start date cannot be blank'}
        
        # Count intake IDs
        intake_list = [id.strip() for id in str(intake_ids).split(',') if id.strip()]
        intake_count = len(intake_list)
        
        # Count start dates
        if ',' in str(start_dates):
            date_count = len([d.strip() for d in str(start_dates).split(',') if d.strip()])
        else:
            date_count = 1 if str(start_dates).strip() else 0
        
        # Check count match
        if intake_count != date_count:
            return {
                'valid': False, 
                'message': f'Intake IDs count ({intake_count}) must match start dates count ({date_count})'
            }
        
        # Check uniqueness
        if len(intake_list) != len(set(intake_list)):
            return {'valid': False, 'message': 'Course Intake IDs must be unique'}
        
        return {'valid': True, 'message': 'Valid course intake IDs'}
    
    def validate_show(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Show field - must be "Yes" or "No"
        
        Args:
            value: The show value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'Show field cannot be blank'}
        
        show_value = str(value).strip()
        if show_value not in self.allowed_show_values:
            return {
                'valid': False, 
                'message': f'Show must be one of: {", ".join(self.allowed_show_values)}'
            }
        
        return {'valid': True, 'message': 'Valid show value'}
    
    def validate_course_status(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Course Status - must be "Open" or "Closed"
        
        Args:
            value: The course status value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'Course Status cannot be blank'}
        
        status_value = str(value).strip()
        
        # Handle comma-separated values
        if ',' in status_value:
            statuses = [s.strip() for s in status_value.split(',')]
            invalid_statuses = [s for s in statuses if s not in self.allowed_statuses]
            if invalid_statuses:
                return {
                    'valid': False, 
                    'message': f'Invalid status values: {", ".join(invalid_statuses)}. Must be one of: {", ".join(self.allowed_statuses)}'
                }
        else:
            if status_value not in self.allowed_statuses:
                return {
                    'valid': False, 
                    'message': f'Course Status must be one of: {", ".join(self.allowed_statuses)}'
                }
        
        return {'valid': True, 'message': 'Valid course status'}
    
    def validate_study_mode(self, value: str) -> Dict[str, Union[bool, str]]:
        """
        Validate Study Mode - must be "Full time" or "Part time"
        
        Args:
            value: The study mode value to validate
            
        Returns:
            Dict with 'valid' (bool) and 'message' (str) keys
        """
        if pd.isna(value) or str(value).strip() == '':
            return {'valid': False, 'message': 'Study Mode cannot be blank'}
        
        mode_value = str(value).strip()
        if mode_value not in self.allowed_study_modes:
            return {
                'valid': False, 
                'message': f'Study Mode must be one of: {", ".join(self.allowed_study_modes)}'
            }
        
        return {'valid': True, 'message': 'Valid study mode'}
    
    def validate_all_fields(self, row: Dict, row_index: int, all_course_ids: List) -> List[Dict]:
        """
        Validate all fields in a row
        
        Args:
            row: Dictionary containing the row data
            row_index: Index of the row (0-based)
            all_course_ids: List of all course IDs for uniqueness check
            
        Returns:
            List of validation results with error details
        """
        errors = []
        
        # Validate Institution Id
        if 'Institution Id' in row:
            result = self.validate_institution_id(row['Institution Id'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Institution Id',
                    'error_type': 'Numeric',
                    'message': result['message'],
                    'value': str(row['Institution Id'])
                })
        
        # Validate Course Id
        if 'Course Id' in row:
            result = self.validate_course_id(row['Course Id'], all_course_ids)
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Course Id',
                    'error_type': 'Unique' if 'unique' in result['message'].lower() else 'Numeric',
                    'message': result['message'],
                    'value': str(row['Course Id'])
                })
        
        # Validate Course Name
        if 'Course Name' in row:
            result = self.validate_course_name(row['Course Name'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Course Name',
                    'error_type': 'Capitalization',
                    'message': result['message'],
                    'value': str(row['Course Name'])
                })
        
        # Validate L3 Tagging
        if 'L3 Tagging' in row:
            result = self.validate_l3_tagging(row['L3 Tagging'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'L3 Tagging',
                    'error_type': 'Blank',
                    'message': result['message'],
                    'value': str(row['L3 Tagging'])
                })
        
        # Validate Degree Type
        if 'Degree Type' in row:
            result = self.validate_degree_type(row['Degree Type'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Degree Type',
                    'error_type': 'Blank',
                    'message': result['message'],
                    'value': str(row['Degree Type'])
                })
        
        # Validate Course Type
        if 'Course Type' in row:
            result = self.validate_course_type(row['Course Type'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Course Type',
                    'error_type': 'Blank',
                    'message': result['message'],
                    'value': str(row['Course Type'])
                })
        
        # Validate Course Start Date
        if 'Course start date' in row:
            result = self.validate_course_start_date(row['Course start date'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Course start date',
                    'error_type': 'Date',
                    'message': result['message'],
                    'value': str(row['Course start date'])
                })
        
        # Validate Course Level URL
        if 'Course Level URL' in row:
            result = self.validate_course_level_url(row['Course Level URL'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Course Level URL',
                    'error_type': 'URL',
                    'message': result['message'],
                    'value': str(row['Course Level URL'])
                })
        
        # Validate Course Intake Ids (requires start date)
        if 'Course Intake Ids' in row and 'Course start date' in row:
            result = self.validate_course_intake_ids(row['Course Intake Ids'], row['Course start date'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Course Intake Ids',
                    'error_type': 'Count',
                    'message': result['message'],
                    'value': str(row['Course Intake Ids'])
                })
        
        # Validate Show
        if 'Show' in row:
            result = self.validate_show(row['Show'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Show',
                    'error_type': 'Status',
                    'message': result['message'],
                    'value': str(row['Show'])
                })
        
        # Validate Course Status
        if 'Course Status' in row:
            result = self.validate_course_status(row['Course Status'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Course Status',
                    'error_type': 'Status',
                    'message': result['message'],
                    'value': str(row['Course Status'])
                })
        
        # Validate Study Mode
        if 'Study Mode' in row:
            result = self.validate_study_mode(row['Study Mode'])
            if not result['valid']:
                errors.append({
                    'row': row_index + 1,
                    'column': 'Study Mode',
                    'error_type': 'Status',
                    'message': result['message'],
                    'value': str(row['Study Mode'])
                })
        
        return errors

# Create a global instance for easy use
validators = CourseValidators()

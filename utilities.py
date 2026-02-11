"""
Data Preprocessing & Utility Functions
Supports the Career Dashboard with data processing and analysis functions
"""
from datasets import load_dataset
import pandas as pd
import numpy as np
from collections import Counter
import json
import re

class DataProcessor:
    """Pre-processes and cleans job data"""
    
    @staticmethod
    def extract_category(cat_string):
        """Extract primary category from JSON string"""
        if pd.isna(cat_string):
            return 'Unknown'
        try:
            cats = json.loads(cat_string.replace("'", '"'))
            if cats and len(cats) > 0:
                return cats[0].get('category', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    @staticmethod
    def clean_salary(value):
        """Clean and convert salary values"""
        if pd.isna(value):
            return 0
        try:
            return float(value)
        except:
            return 0
    
    @staticmethod
    def clean_experience(value):
        """Clean and convert experience values"""
        if pd.isna(value):
            return 0
        try:
            return int(float(value))
        except:
            return 0
    
    @classmethod
    def process_data(cls, df):
        """Comprehensive data preprocessing"""
        # Copy to avoid warnings
        df = df.copy()
        
        # Clean numeric columns
        df['minimumYearsExperience'] = df['minimumYearsExperience'].apply(cls.clean_experience)
        df['salary_minimum'] = df['salary_minimum'].apply(cls.clean_salary)
        df['salary_maximum'] = df['salary_maximum'].apply(cls.clean_salary)
        df['average_salary'] = (df['salary_minimum'] + df['salary_maximum']) / 2
        
        # Extract and clean categories
        df['primary_category'] = df['categories'].apply(cls.extract_category)
        
        # Clean position levels
        df['positionLevels'] = df['positionLevels'].fillna('Not Specified')
        
        # Handle missing titles
        df['title'] = df['title'].fillna('Unknown Position')
        
        return df


class SkillsAnalyzer:
    """Analyzes and extracts skills from job data"""
    
    # Comprehensive skills dictionary organized by category
    SKILLS_DICT = {
        'Programming Languages': [
            'Python', 'Java', 'C++', 'C#', 'JavaScript', 'TypeScript',
            'Ruby', 'PHP', 'Swift', 'Kotlin', 'Go', 'Rust'
        ],
        'Web Technologies': [
            'React', 'Vue.js', 'Angular', 'Node.js', 'Django', 'Flask',
            'Spring Boot', 'ASP.NET', 'Express.js', 'Next.js'
        ],
        'Database & Data': [
            'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis',
            'Elasticsearch', 'Oracle', 'Cassandra', 'Data Science', 
            'Data Analysis', 'Analytics', 'Tableau', 'Power BI'
        ],
        'Cloud & DevOps': [
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes',
            'CI/CD', 'Jenkins', 'GitLab', 'GitHub', 'DevOps',
            'Infrastructure as Code', 'Terraform', 'Ansible'
        ],
        'Machine Learning & AI': [
            'Machine Learning', 'Deep Learning', 'AI', 'TensorFlow',
            'PyTorch', 'NLP', 'Computer Vision', 'Scikit-learn'
        ],
        'Methods & Frameworks': [
            'Agile', 'Scrum', 'Kanban', 'Waterfall',
            'REST API', 'GraphQL', 'Microservices'
        ],
        'Leadership & Management': [
            'Leadership', 'Management', 'Team Lead', 'Technical Lead',
            'Project Management', 'Product Management', 'Mentoring'
        ],
        'Quality & Testing': [
            'QA', 'SDET', 'Test Automation', 'Selenium', 'Pytest',
            'Unit Testing', 'Integration Testing', 'Regression Testing'
        ],
        'Systems & Architecture': [
            'System Design', 'Microservices', 'Architecture',
            'Distributed Systems', 'High Availability', 'Scalability'
        ],
        'Soft Skills': [
            'Communication', 'Problem Solving', 'Critical Thinking',
            'Collaboration', 'Presentation', 'Negotiation', 'Adaptability'
        ]
    }
    
    # Flatten for easier searching
    FLAT_SKILLS = []
    for category_skills in SKILLS_DICT.values():
        FLAT_SKILLS.extend(category_skills)
    
    @classmethod
    def extract_skills(cls, text):
        """Extract skills from job title or description"""
        if pd.isna(text):
            return []
        
        text_upper = str(text).upper()
        found_skills = []
        
        for skill in cls.FLAT_SKILLS:
            if skill.upper() in text_upper:
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    @classmethod
    def get_skills_by_role(cls, df, role_keyword, limit=50):
        """Get most common skills for a specific role"""
        filtered = df[df['title'].str.contains(role_keyword, case=False, na=False)]
        filtered = filtered.head(limit)
        
        all_skills = []
        for title in filtered['title']:
            all_skills.extend(cls.extract_skills(title))
        
        skill_counts = Counter(all_skills)
        return skill_counts
    
    @classmethod
    def get_skills_by_category(cls, df, category):
        """Get common skills in a specific industry"""
        filtered = df[df['primary_category'] == category]
        
        all_skills = []
        for title in filtered['title'].head(100):
            all_skills.extend(cls.extract_skills(title))
        
        skill_counts = Counter(all_skills)
        return skill_counts.most_common(10)


class CareerPathAnalyzer:
    """Analyzes career paths and transitions"""
    
    @staticmethod
    def calculate_skill_match(user_skills, job_skills):
        """Calculate skill match percentage"""
        if len(job_skills) == 0:
            return 100.0
        
        user_set = set([s.lower() for s in user_skills])
        job_set = set([s.lower() for s in job_skills])
        
        matches = len(user_set.intersection(job_set))
        match_percentage = (matches / len(job_set)) * 100
        
        return round(match_percentage, 1)
    
    @staticmethod
    def identify_gaps(user_skills, target_skills):
        """Identify missing skills"""
        user_set = set([s.lower() for s in user_skills])
        target_set = set([s.lower() for s in target_skills])
        
        gaps = target_set - user_set
        return sorted(list(gaps))
    
    @staticmethod
    def estimate_transition_time(num_skills, complexity='medium'):
        """Estimate time to learn skills"""
        time_map = {
            'low': {'months': 3, 'weeks_per_skill': 4},
            'medium': {'months': 6, 'weeks_per_skill': 6},
            'high': {'months': 12, 'weeks_per_skill': 8}
        }
        
        base_time = time_map[complexity]
        total_months = (num_skills * base_time['weeks_per_skill']) / 4
        
        return int(max(base_time['months'], total_months))
    
    @staticmethod
    def estimate_salary_growth(current_salary, years_to_target, industry_growth_rate=0.08):
        """Estimate salary after skill development"""
        # Base growth + skill premium (typically 10-20% for major skills)
        annual_growth = 1 + industry_growth_rate
        professional_growth = 1.15  # Skills premium
        
        projected = current_salary * professional_growth * (annual_growth ** years_to_target)
        return round(projected)


class MarketAnalyzer:
    """Provides market insights and analysis"""
    
    @staticmethod
    def get_role_stats(df, role_keyword):
        """Get comprehensive statistics for a role"""
        filtered = df[df['title'].str.contains(role_keyword, case=False, na=False)]
        
        if len(filtered) == 0:
            return None
        
        stats = {
            'count': len(filtered),
            'avg_salary': filtered['average_salary'].mean(),
            'min_salary': filtered['salary_minimum'].mean(),
            'max_salary': filtered['salary_maximum'].mean(),
            'median_salary': filtered['average_salary'].median(),
            'min_experience': filtered['minimumYearsExperience'].min(),
            'avg_experience': filtered['minimumYearsExperience'].mean(),
            'max_experience': filtered['minimumYearsExperience'].max(),
            'top_companies': filtered['postedCompany_name'].value_counts().head(5).to_dict(),
            'job_status_dist': filtered['status_jobStatus'].value_counts().to_dict()
        }
        
        return stats
    
    @staticmethod
    def get_category_stats(df, category):
        """Get statistics for an industry category"""
        filtered = df[df['primary_category'] == category]
        
        if len(filtered) == 0:
            return None
        
        stats = {
            'count': len(filtered),
            'avg_salary': filtered['average_salary'].mean(),
            'avg_experience': filtered['minimumYearsExperience'].mean(),
            'position_levels': filtered['positionLevels'].value_counts().to_dict(),
            'employment_types': filtered['employmentTypes'].value_counts().to_dict()
        }
        
        return stats
    
    @staticmethod
    def get_salary_by_experience(df, max_years=15):
        """Get average salary by experience level"""
        filtered = df[df['minimumYearsExperience'] <= max_years]
        salary_by_exp = filtered.groupby('minimumYearsExperience')['average_salary'].agg(['mean', 'count'])
        
        return salary_by_exp


class TransitionPathFinder:
    """Finds realistic transition paths between roles"""
    
    @staticmethod
    def find_stepping_stones(df, current_role, target_role, max_gaps=3):
        """Find intermediate roles for career transition"""
        # This is simplified - in production, would use more sophisticated graph algorithms
        
        current_roles = df[df['title'].str.contains(current_role, case=False, na=False)]
        target_roles = df[df['title'].str.contains(target_role, case=False, na=False)]
        
        # Find roles that share skills with both current and target
        intermediate_candidates = []
        
        all_roles = df['title'].unique()
        for role in all_roles[:500]:  # Sample for performance
            role_skills = SkillsAnalyzer.extract_skills(role)
            
            current_skills_sample = set()
            target_skills_sample = set()
            
            for title in current_roles['title'].head(10):
                current_skills_sample.update(SkillsAnalyzer.extract_skills(title))
            
            for title in target_roles['title'].head(10):
                target_skills_sample.update(SkillsAnalyzer.extract_skills(title))
            
            overlap_current = len(set(role_skills) & current_skills_sample)
            overlap_target = len(set(role_skills) & target_skills_sample)
            
            if overlap_current > 1 and overlap_target > 1:
                intermediate_candidates.append({
                    'role': role,
                    'overlap_current': overlap_current,
                    'overlap_target': overlap_target
                })
        
        # Sort by total overlap
        intermediate_candidates.sort(
            key=lambda x: x['overlap_current'] + x['overlap_target'],
            reverse=True
        )
        
        return intermediate_candidates[:max_gaps]


# Example usage
if __name__ == "__main__":
    # Load and process data
    # df = pd.read_csv('data/SGJobData.csv', on_bad_lines='skip')
    ds = load_dataset("eshern/careerpath-data", data_files="SGJobData.csv")
    df = ds["train"].to_pandas()
    df = DataProcessor.process_data(df)
    
    # Example: Get skills for a role
    qe_skills = SkillsAnalyzer.get_skills_by_role(df, 'QA Engineer', limit=30)
    print("QA Engineer Skills:", dict(qe_skills.most_common(10)))
    
    # Example: Analyze a role
    stats = MarketAnalyzer.get_role_stats(df, 'QA Engineer')
    print("\nQA Engineer Market Stats:", stats)
    
    # Example: Salary by experience
    salary_analysis = MarketAnalyzer.get_salary_by_experience(df)
    print("\nSalary by Experience:\n", salary_analysis)

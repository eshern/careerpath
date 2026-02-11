"""
Configuration and Settings for Career Dashboard
Centralized configuration for easy customization
"""

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

APP_NAME = "Career Path & Skills Gap Analyzer"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Data-driven insights for personalized career progression"

# ============================================================================
# DATA SETTINGS
# ============================================================================

DATA_FILE = "data/SGJobData.csv"
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour in seconds

# Data filtering thresholds
MAX_EXPERIENCE_FILTER = 20  # Don't show roles requiring > 20 years
MIN_JOB_POSTINGS_THRESHOLD = 10  # Minimum postings to show role

# ============================================================================
# SKILLS CONFIGURATION
# ============================================================================

CORE_SKILLS = [
    'Python', 'Java', 'SQL', 'C++', 'C#', 'JavaScript', 'React', 'Node.js',
    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'Linux',
    'Machine Learning', 'AI', 'Data Science', 'Analytics', 'BI',
    'Tableau', 'Power BI', 'Agile', 'Scrum',
    'Leadership', 'Management', 'Communication', 'Problem Solving'
]

# Skill difficulty levels (for learning time estimation)
SKILL_DIFFICULTY = {
    'low': ['SQL', 'Excel', 'Communication', 'Problem Solving'],
    'medium': ['Python', 'JavaScript', 'Project Management', 'Leadership'],
    'high': ['Kubernetes', 'Machine Learning', 'System Design', 'Cloud Architecture']
}

# ============================================================================
# CAREER PATH CONFIGURATION
# ============================================================================

# Experience level categorization
EXPERIENCE_LEVELS = {
    'entry': (0, 2),
    'early': (2, 5),
    'mid': (5, 10),
    'senior': (10, 100)
}

EXPERIENCE_LABELS = {
    'entry': 'Entry Level (0-2 years)',
    'early': 'Early Career (2-5 years)',
    'mid': 'Mid Career (5-10 years)',
    'senior': 'Senior (10+ years)'
}

# Salary growth multipliers by role transition
SALARY_GROWTH_MULTIPLIERS = {
    'promotion_same_domain': 1.15,      # 15% for promotion in same domain
    'lateral_move': 1.10,                # 10% for lateral move to similar role
    'domain_transition': 1.20,           # 20% for successful domain transition
    'leadership_jump': 1.25,             # 25% jump to management
    'specialization': 1.18               # 18% for specialized role
}

# ============================================================================
# LEARNING PATH CONFIGURATION
# ============================================================================

LEARNING_TIMELINES = {
    'quick': {
        'duration_months': 3,
        'description': 'Fast Track - Focus on essentials',
        'pace': 'Intensive',
        'effort': '15-20 hours/week'
    },
    'standard': {
        'duration_months': 6,
        'description': 'Balanced - Comprehensive learning',
        'pace': 'Moderate',
        'effort': '10-15 hours/week'
    },
    'thorough': {
        'duration_months': 12,
        'description': 'Deep Dive - Expert level knowledge',
        'pace': 'Relaxed',
        'effort': '8-10 hours/week'
    }
}

# ============================================================================
# TRANSITION CONFIGURATION
# ============================================================================

TRANSITION_PATHS = {
    'direct': {
        'name': 'Direct Transition (Fast Track)',
        'duration': '6-12 months',
        'difficulty': 'Challenging',
        'description': 'Intensive learning focused on critical skills',
        'pros': ['Fastest path', 'Maintains continuous work'],
        'cons': ['High effort', 'May need side projects']
    },
    'stepping': {
        'name': 'Gradual Transition (Stepping Stone)',
        'duration': '18-24 months',
        'difficulty': 'Moderate',
        'description': 'Gradual transition through intermediate roles',
        'pros': ['Lower risk', 'Develop skills on job', 'Stable income'],
        'cons': ['Takes longer', 'Requires role changes']
    }
}

# ============================================================================
# VISUALIZATION SETTINGS
# ============================================================================

COLOR_PALETTE = {
    'primary': '#1f77b4',
    'success': '#00CC96',
    'warning': '#FFA500',
    'danger': '#EF553B',
    'neutral': '#636EFA',
    'secondary': '#AB63FA'
}

CHART_COLORS = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA500']

# ============================================================================
# LEARNING RESOURCES
# ============================================================================

LEARNING_PLATFORMS = {
    'online_courses': [
        {'name': 'Coursera', 'url': 'https://www.coursera.org', 'type': 'University-partnered'},
        {'name': 'Udemy', 'url': 'https://www.udemy.com', 'type': 'Affordable courses'},
        {'name': 'LinkedIn Learning', 'url': 'https://www.linkedin.com/learning', 'type': 'Professional'},
        {'name': 'Pluralsight', 'url': 'https://www.pluralsight.com', 'type': 'Technical skills'},
        {'name': 'DataCamp', 'url': 'https://www.datacamp.com', 'type': 'Data science'}
    ],
    'practice_platforms': [
        {'name': 'LeetCode', 'url': 'https://www.leetcode.com', 'type': 'Algorithm practice'},
        {'name': 'HackerRank', 'url': 'https://www.hackerrank.com', 'type': 'Coding challenges'},
        {'name': 'Kaggle', 'url': 'https://www.kaggle.com', 'type': 'Data science competitions'},
        {'name': 'GitHub', 'url': 'https://www.github.com', 'type': 'Code portfolio'}
    ],
    'certification': [
        {'name': 'AWS Solutions Architect', 'domain': 'Cloud'},
        {'name': 'Azure Administrator', 'domain': 'Cloud'},
        {'name': 'Google Cloud Professional', 'domain': 'Cloud'},
        {'name': 'Certified Kubernetes Administrator', 'domain': 'DevOps'},
        {'name': 'PMP', 'domain': 'Project Management'},
        {'name': 'Scrum Master', 'domain': 'Agile'}
    ]
}

# ============================================================================
# MARKET INSIGHTS
# ============================================================================

# Default market metrics
DEFAULT_METRICS = {
    'job_postings_period': 'Q4 2023',
    'data_freshness': 'Current',
    'geographic_scope': 'Singapore'
}

# ============================================================================
# UX/UI SETTINGS
# ============================================================================

SIDEBAR_WIDTH = 300
MAX_CHART_HEIGHT = 400
MOBILE_BREAKPOINT = 768

# ============================================================================
# VALIDATION SETTINGS
# ============================================================================

VALIDATION_RULES = {
    'min_experience': 0,
    'max_experience': 50,
    'min_salary': 1000,
    'max_salary': 100000,
    'min_skills': 1,
    'max_skills': 20
}

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURES = {
    'skills_gap_analysis': True,
    'salary_projection': True,
    'career_paths': True,
    'market_analytics': True,
    'profile_builder': True,
    'export_pdf': False,                # Future feature
    'job_alerts': False,                # Future feature
    'user_accounts': False,             # Future feature
    'mobile_app': False                 # Future feature
}

# ============================================================================
# CONTACT & SUPPORT
# ============================================================================

SUPPORT_INFO = {
    'email': 'support@careeranalyzer.com',
    'documentation': 'https://docs.careeranalyzer.com',
    'issues': 'https://github.com/careeranalyzer/issues'
}

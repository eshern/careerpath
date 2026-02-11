"""
Career Path & Skills Gap Analysis Dashboard
Interactive tool for job seekers to identify skills gaps and personalized career paths

Business Objectives:
- Help job seekers identify best-fit roles
- Understand required skills and gaps
- Accelerate career progression through data-driven insights

Target Users:
- Early-career professionals (0-3 years)
- Mid-career professionals (3-10 years)
- Career switchers/transitioning professionals
"""
# from datasets import load_dataset
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from collections import Counter
import json
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Career Path & Skills Gap Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header-section {
        color: #1f77b4;
        font-size: 24px;
        font-weight: bold;
        margin: 20px 0 10px 0;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-left: 4px solid #1f77b4;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 15px;
        border-left: 4px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING AND CACHING
# ============================================================================
@st.cache_data
def load_data():
    """Load and preprocess the job data"""

    # csv_path = "data/SGJobData.csv"
    csv_path = "hf://datasets/eshern/careerpath-data/SGJobData.csv"
    
    try:
        # ds = load_dataset("eshern/careerpath-data", data_files="SGJobData.csv")
        # df = ds["train"].to_pandas()

        df = pd.read_csv(csv_path, on_bad_lines='skip')
        
        # Data cleaning
        df['minimumYearsExperience'] = pd.to_numeric(df['minimumYearsExperience'], errors='coerce').fillna(0).astype(int)
        df['salary_minimum'] = pd.to_numeric(df['salary_minimum'], errors='coerce').fillna(0)
        df['salary_maximum'] = pd.to_numeric(df['salary_maximum'], errors='coerce').fillna(0)
        df['average_salary'] = (df['salary_minimum'] + df['salary_maximum']) / 2
        
        # Extract categories from JSON
        df['primary_category'] = df['categories'].apply(extract_category)
        
        # Clean position levels
        df['positionLevels'] = df['positionLevels'].fillna('Not Specified')
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
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

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def extract_skills_from_title(title):
    """Extract technical skills from job title"""
    if pd.isna(title):
        return []
    
    title = str(title).upper()
    skills_keywords = {
        'Python', 'Java', 'SQL', 'C++', 'C#', 'JavaScript', 'React', 'Node',
        'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'Linux',
        'Machine Learning', 'AI', 'Data Science', 'Analytics', 'BI',
        'Tableau', 'Power BI', 'Salesforce', 'SAP', 'Oracle',
        'Agile', 'Scrum', 'Product Management', 'Project Management',
        'Leadership', 'Management', 'Team Lead', 'Technical Lead',
        'Frontend', 'Backend', 'Full Stack', 'DevOps', 'QA', 'SDET'
    }
    
    found_skills = []
    for skill in skills_keywords:
        if skill.upper() in title:
            found_skills.append(skill)
    
    return found_skills

def categorize_experience_level(years):
    """Categorize professional based on years of experience"""
    if years < 2:
        return 'Entry Level (0-2 years)'
    elif years < 5:
        return 'Early Career (2-5 years)'
    elif years < 10:
        return 'Mid Career (5-10 years)'
    else:
        return 'Senior (10+ years)'

def calculate_skill_match(user_skills, job_skills, weight_match=0.6):
    """Calculate how well user skills match job requirements"""
    user_skills_set = set([s.lower() for s in user_skills])
    job_skills_set = set([s.lower() for s in job_skills])
    
    if len(job_skills_set) == 0:
        return 100
    
    matches = user_skills_set.intersection(job_skills_set)
    match_percentage = (len(matches) / len(job_skills_set)) * 100
    
    return round(match_percentage, 1)

def find_skill_gaps(user_skills, target_job_data):
    """Identify missing skills for a target role"""
    user_skills_set = set([s.lower() for s in user_skills])
    job_skills = set()
    
    for _, row in target_job_data.iterrows():
        skills = extract_skills_from_title(row['title'])
        job_skills.update([s.lower() for s in skills])
    
    gaps = job_skills - user_skills_set
    return list(gaps)

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Load data
    df = load_data()
    
    if df is None:
        st.error("Failed to load data. Please check the CSV file.")
        return
    
    # ========================================================================
    # SIDEBAR - Navigation and Filters
    # ========================================================================
    st.sidebar.markdown("## 🎯 Navigation")
    app_mode = st.sidebar.radio(
        "Select Your Journey:",
        [
            "🏠 Home & Overview",
            "👤 Mid-Career Professional",
            "🔄 Career Switcher",
            "📊 My Career Profile",
            "💡 Usage Guide"
        ]
    )
    
    # ========================================================================
    # PAGE 1: HOME & OVERVIEW
    # ========================================================================
    if app_mode == "🏠 Home & Overview":
        st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <h1>🎯 Career Path & Skills Gap Analyzer</h1>
            <p style='font-size: 18px; color: #555;'>
                Data-Driven Insights for Your Next Career Move
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Job Postings Analyzed",
                value=f"{len(df):,}",
                delta="Real-time data"
            )
        
        with col2:
            st.metric(
                label="Career Categories",
                value=df['primary_category'].nunique(),
                delta="Diverse opportunities"
            )
        
        with col3:
            avg_salary = df['average_salary'].mean()
            st.metric(
                label="Avg Salary Range",
                value=f"${avg_salary:,.0f}/month",
                delta="Market insights"
            )
        
        st.divider()
        
        st.markdown("### 📋 Who Are You?")
        
        user_type = st.select_slider(
            "Select your professional profile:",
            options=[
                "Early Career (0-3 years)",
                "Mid Career (3-10 years)",
                "Senior (10+ years)",
                "Career Switcher"
            ]
        )
        
        st.markdown(f"""
        <div class='insight-box'>
            <strong>Your Profile: {user_type}</strong><br><br>
            This dashboard is designed to help professionals like you navigate career decisions with data-driven insights.
            Browse the sections below to find personalized recommendations.
        </div>
        """, unsafe_allow_html=True)
        
        # Overview stats
        st.markdown("### 📈 Market Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top categories by job count
            top_categories = df['primary_category'].value_counts().head(8)
            fig = px.bar(
                x=top_categories.values,
                y=top_categories.index,
                orientation='h',
                title='Top 8 Industries by Job Postings',
                labels={'x': 'Number of Postings', 'y': 'Industry'}
            )
            fig.update_layout(height=400, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Experience requirements distribution
            exp_dist = df[df['minimumYearsExperience'] <= 20].groupby(pd.cut(df['minimumYearsExperience'], bins=[0, 2, 5, 10, 20])).size()
            fig = go.Figure(data=[
                go.Bar(
                    x=['0-2 years', '2-5 years', '5-10 years', '10-20 years'],
                    y=exp_dist.values,
                    marker_color=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']
                )
            ])
            fig.update_layout(
                title='Entry Requirements Distribution',
                xaxis_title='Years of Experience',
                yaxis_title='Number of Roles',
                height=400,
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Salary insights by experience
        st.markdown("### 💰 Salary Trends by Experience")
        salary_by_exp = df[df['minimumYearsExperience'] <= 15].groupby(pd.cut(df['minimumYearsExperience'], bins=6))['average_salary'].agg(['mean', 'count'])
        salary_by_exp.index = [f"{int(interval.left)}-{int(interval.right)}y" for interval in salary_by_exp.index]
        
        fig = px.line(
            x=salary_by_exp.index,
            y=salary_by_exp['mean'],
            markers=True,
            title='Average Salary Progression by Experience',
            labels={'x': 'Years of Experience', 'y': 'Average Monthly Salary ($)'}
        )
        fig.update_layout(height=400, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE 2: MID-CAREER PROFESSIONAL
    # ========================================================================
    elif app_mode == "👤 Mid-Career Professional":
        st.markdown("## 👤 Mid-Career Professional Path")
        st.markdown("""
        **For professionals with 3-10 years of experience**
        
        Answer key questions about promotion paths, skill mapping, and next-level roles.
        """)
        
        st.divider()
        
        # User Input Section
        st.markdown("### 📝 Your Current Profile")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_role = st.selectbox(
                "Your Current Role/Title:",
                options=['QA Engineer', 'Software Engineer', 'Data Analyst', 'Product Manager', 
                        'Business Analyst', 'DevOps Engineer', 'Solution Architect', 'Other']
            )
        
        with col2:
            years_exp = st.slider(
                "Years of Experience:",
                min_value=3, max_value=20, value=5, step=1
            )
        
        with col3:
            current_salary = st.number_input(
                "Current Monthly Salary ($):",
                min_value=2000, max_value=15000, value=5000, step=500
            )
        
        st.divider()
        
        # Current skills
        st.markdown("### 🛠️ Your Current Skills")
        col1, col2 = st.columns(2)
        
        all_skills = ['Python', 'Java', 'SQL', 'AWS', 'Azure', 'Docker', 'Kubernetes', 
                     'JavaScript', 'React', 'Node.js', 'Machine Learning', 'Data Science',
                     'Project Management', 'Leadership', 'Agile', 'Communication']
        
        with col1:
            current_skills = st.multiselect(
                "Select skills you currently have:",
                options=all_skills,
                default=all_skills[:3]
            )
        
        with col2:
            proficiency_levels = {}
            st.write("**Proficiency Level:**")
            for skill in current_skills:
                proficiency_levels[skill] = st.select_slider(
                    f"{skill}:",
                    options=['Beginner', 'Intermediate', 'Advanced', 'Expert'],
                    value='Intermediate',
                    key=f"prof_{skill}"
                )
        
        st.divider()
        
        # Career goals
        st.markdown("### 🎯 Your Career Goals")
        career_goal = st.selectbox(
            "What's your primary career goal?",
            options=[
                "Promotion within current role",
                "Transition to higher-level role",
                "Domain/technology shift",
                "Leadership track",
                "Specialist/Expert track"
            ]
        )
        
        target_role = st.text_input(
            "Target role (e.g., 'Senior SDET', 'Team Lead', 'Product Manager'):",
            value="Senior " + current_role
        )
        
        st.divider()
        
        # Analysis
        if st.button("🔍 Analyze My Career Path", type="primary", use_container_width=True):
            with st.spinner("Analyzing job market and identifying opportunities..."):
                
                # Filter relevant roles
                role_filter_df = df[df['title'].str.contains(current_role, case=False, na=False)]
                target_filter_df = df[df['title'].str.contains(target_role, case=False, na=False)]
                
                # Create analysis columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 📊 Current Role Market Analysis")
                    
                    if len(role_filter_df) > 0:
                        current_stats = {
                            'Avg Experience Required': role_filter_df['minimumYearsExperience'].mean(),
                            'Avg Salary': role_filter_df['average_salary'].mean(),
                            'Salary Range': f"${role_filter_df['salary_minimum'].mean():,.0f} - ${role_filter_df['salary_maximum'].mean():,.0f}"
                        }
                        
                        st.metric("Number of Openings", value=len(role_filter_df))
                        st.metric("Average Salary", value=f"${current_stats['Avg Salary']:,.0f}/month")
                        st.metric("Avg Exp Required", value=f"{current_stats['Avg Experience Required']:.1f} years")
                    else:
                        st.info("Limited data for exact role match. Showing related opportunities...")
                
                with col2:
                    st.markdown("### 🎯 Target Role Market Analysis")
                    
                    if len(target_filter_df) > 0:
                        target_stats = {
                            'Avg Experience Required': target_filter_df['minimumYearsExperience'].mean(),
                            'Avg Salary': target_filter_df['average_salary'].mean(),
                            'Salary Range': f"${target_filter_df['salary_minimum'].mean():,.0f} - ${target_filter_df['salary_maximum'].mean():,.0f}"
                        }
                        
                        st.metric("Number of Openings", value=len(target_filter_df))
                        st.metric("Average Salary", value=f"${target_stats['Avg Salary']:,.0f}/month")
                        st.metric("Avg Exp Required", value=f"{target_stats['Avg Experience Required']:.1f} years")
                        
                        # Salary jump calculation
                        salary_jump = target_stats['Avg Salary'] - current_salary
                        jump_percentage = (salary_jump / current_salary * 100) if current_salary > 0 else 0
                        st.success(f"💰 Potential Salary Jump: ${salary_jump:,.0f}/month ({jump_percentage:.1f}%)")
                    else:
                        st.warning("Limited data for target role. Try a different target.")
                
                st.divider()
                
                # Skills gap analysis
                st.markdown("### 🔍 Skills Gap Analysis")
                
                # Extract skills from job titles
                current_job_skills = set()
                target_job_skills = set()
                
                for title in role_filter_df['title'].head(20):
                    current_job_skills.update(extract_skills_from_title(title))
                
                for title in target_filter_df['title'].head(20):
                    target_job_skills.update(extract_skills_from_title(title))
                
                user_skills_set = set(current_skills)
                gaps = target_job_skills - user_skills_set
                overlaps = target_job_skills.intersection(user_skills_set)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ✅ Skills You Already Have")
                    if overlaps:
                        for skill in sorted(overlaps):
                            st.success(f"• {skill}")
                    else:
                        st.info("Add relevant skills to see matches")
                
                with col2:
                    st.markdown("#### ❌ Skills Gap (Missing)")
                    if gaps:
                        st.warning(f"You're missing {len(gaps)} key skills:")
                        for skill in sorted(gaps):
                            st.warning(f"• {skill}")
                    else:
                        st.success("Great! Your skills align well with target role!")
                
                st.divider()
                
                # Upskilling roadmap
                st.markdown("### 📚 Personalized Upskilling Roadmap")
                
                if gaps:
                    st.info(f"""
                    **Timeline Estimate:** 3-6 months to gain proficiency in {len(gaps)} key skills
                    
                    **Recommended Learning Path:**
                    """)
                    
                    roadmap_tabs = st.tabs(['Quick Path (3 months)', 'Thorough Path (6 months)', 'Expert Path (12 months)'])
                    
                    with roadmap_tabs[0]:
                        st.markdown("""
                        Focus on the top 2-3 most impactful skills:
                        1. **Month 1:** Online courses + hands-on projects
                        2. **Month 2:** Build portfolio projects
                        3. **Month 3:** Practice interview scenarios
                        """)
                    
                    with roadmap_tabs[1]:
                        st.markdown("""
                        Balanced approach across all critical skills:
                        1. **Months 1-2:** Core concept learning
                        2. **Months 3-4:** Intermediate projects
                        3. **Months 5-6:** Advanced scenarios + interviews
                        """)
                    
                    with roadmap_tabs[2]:
                        st.markdown("""
                        Deep expertise development:
                        1. **Months 1-4:** Strong foundational learning
                        2. **Months 5-8:** Advanced applications
                        3. **Months 9-12:** Expert-level projects + certifications
                        """)
                
                st.divider()
                
                # Salary projection
                st.markdown("### 💹 Your Salary Growth Projection")
                
                milestones = ['Current', 'With Key Skills (3-6mo)', 'Promoted (12mo)', 'Senior Role (24mo)']
                projected_salaries = [
                    current_salary,
                    current_salary * 1.15,
                    current_salary * 1.35,
                    current_salary * 1.65
                ]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=milestones,
                    y=projected_salaries,
                    mode='lines+markers',
                    fill='tozeroy',
                    line_color='#00CC96',
                    marker=dict(size=12),
                    fillcolor='rgba(0, 204, 150, 0.1)'
                ))
                fig.update_layout(
                    title='Your Salary Growth Projection',
                    yaxis_title='Monthly Salary ($)',
                    height=400,
                    template="plotly_white",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                # Action items
                st.markdown("### ✨ Recommended Next Steps")
                
                steps = [
                    ("🎓", "Enroll in online courses", "Platforms: Coursera, Udemy, LinkedIn Learning"),
                    ("💻", "Build portfolio projects", "GitHub projects showcasing your skills"),
                    ("🤝", "Network in your target domain", "LinkedIn, meetups, conferences"),
                    ("📝", "Update your resume", "Highlight transferable skills"),
                    ("🗣️", "Practice interviews", "Focus on behavioral + technical questions")
                ]
                
                for emoji, step, detail in steps:
                    st.info(f"{emoji} **{step}**\n\n{detail}")
    
    # ========================================================================
    # PAGE 3: CAREER SWITCHER
    # ========================================================================
    elif app_mode == "🔄 Career Switcher":
        st.markdown("## 🔄 Career Transition & Domain Shift")
        st.markdown("""
        **For professionals looking to transition into a new role or domain**
        
        Discover realistic transition paths and identify your competitive advantages.
        """)
        
        st.divider()
        
        st.markdown("### 📝 Your Current Background")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_domain = st.selectbox(
                "Your Current Domain/Field:",
                options=['Engineering', 'Operations', 'Teaching/Education', 'Sales/Business Development',
                        'Finance', 'Government/Public Service', 'Hospitality', 'Healthcare',
                        'Manufacturing', 'Consulting', 'Other']
            )
            
            current_years = st.slider(
                "Years in Current Field:",
                min_value=1, max_value=30, value=5, step=1
            )
        
        with col2:
            target_domain = st.selectbox(
                "Target Domain/Field:",
                options=['Product Management', 'Data Science', 'Cloud Engineering', 
                        'Learning & Development (L&D)', 'HR/People Operations', 'Software Engineering',
                        'Project Management', 'Business Analysis', 'UX/UI Design', 'Other']
            )
        
        st.divider()
        
        st.markdown("### 🛠️ Your Transferable Skills")
        
        transferable_skills = st.multiselect(
            "Select skills you have that transfer across domains:",
            options=['Project Management', 'Communication', 'Leadership', 'Problem Solving',
                    'Data Analysis', 'Training/Teaching', 'Customer Relations', 'Strategic Thinking',
                    'Process Improvement', 'Technical Writing', 'Agile Methodology', 'Attention to Detail'],
            default=['Communication', 'Problem Solving']
        )
        
        st.divider()
        
        if st.button("🔍 Analyze My Transition Path", type="primary", use_container_width=True):
            with st.spinner("Analyzing career transition opportunities..."):
                
                st.markdown("### 📊 Transition Feasibility Analysis")
                
                # Find roles that match skills
                domain_roles_df = df[df['title'].str.contains(target_domain, case=False, na=False)]
                
                # Calculate transition difficulty
                transition_difficulty = "Moderate"
                difficulty_color = "🟡"
                
                if len(domain_roles_df) > 0:
                    avg_exp_target = domain_roles_df['minimumYearsExperience'].mean()
                    
                    if current_years >= avg_exp_target * 0.5:
                        transition_difficulty = "Low-Moderate"
                        difficulty_color = "🟢"
                    elif current_years >= avg_exp_target * 0.3:
                        transition_difficulty = "Moderate"
                        difficulty_color = "🟡"
                    else:
                        transition_difficulty = "Challenging"
                        difficulty_color = "🔴"
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Transition Difficulty", value=transition_difficulty)
                
                with col2:
                    st.metric("Target Domain Openings", value=len(domain_roles_df))
                
                with col3:
                    if len(domain_roles_df) > 0:
                        st.metric("Avg Salary (Target)", f"${domain_roles_df['average_salary'].mean():,.0f}")
                
                st.divider()
                
                # Transition paths
                st.markdown("### 🗺️ Recommended Transition Paths")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### Path 1: Direct Transition (Fast Track)")
                    st.markdown("""
                    **Timeline:** 6-12 months
                    
                    **Steps:**
                    1. Identify overlapping skills
                    2. Fill critical knowledge gaps
                    3. Build portfolio/projects in new domain
                    4. Network and find mentors
                    5. Apply to entry/junior roles in new domain
                    
                    **Best for:** Strong foundational skills + dedicated learning
                    """)
                
                with col2:
                    st.markdown("#### Path 2: Gradual Transition (Stepping Stone)")
                    st.markdown("""
                    **Timeline:** 18-24 months
                    
                    **Steps:**
                    1. Find intermediate roles combining both domains
                    2. Build experience in new domain part-time
                    3. Develop new domain expertise gradually
                    4. Transition full-time with hybrid background
                    5. Leverage unique perspective as competitive advantage
                    
                    **Best for:** Risk mitigation + stable income
                    """)
                
                st.divider()
                
                # Skills gap for transition
                st.markdown("### 🎯 Critical Skills You Need")
                
                if target_domain == "Data Science":
                    required_skills = ['Python', 'SQL', 'Machine Learning', 'Statistics', 'Data Visualization']
                elif target_domain == "Product Management":
                    required_skills = ['Product Strategy', 'User Research', 'Data Analysis', 'Communication', 'Leadership']
                elif target_domain == "Cloud Engineering":
                    required_skills = ['AWS/Azure/GCP', 'DevOps', 'Containerization', 'Infrastructure as Code', 'System Design']
                elif target_domain == "Learning & Development (L&D)":
                    required_skills = ['Instructional Design', 'Learning Technologies', 'Training Facilitation', 'Adult Learning Theory']
                else:
                    required_skills = ['Technical Skills', 'Domain Knowledge', 'Industry Standards']
                
                # Identify skill gaps
                gaps = [s for s in required_skills if s not in transferable_skills]
                matches = [s for s in required_skills if s in transferable_skills]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success(f"**Your Advantages ({len(matches)} matches):**")
                    if matches:
                        for skill in matches:
                            st.success(f"✅ {skill}")
                    
                    st.markdown("""
                    **Leverage your transferable skills in:**
                    - Team collaboration and communication
                    - Project delivery and management
                    - Cross-functional work
                    - Understanding business needs
                    """)
                
                with col2:
                    st.warning(f"**Skills to Develop ({len(gaps)} gaps):**")
                    if gaps:
                        for skill in gaps:
                            st.warning(f"❌ {skill}")
                    
                    st.markdown("""
                    **Suggested Learning Resources:**
                    - Structured online courses
                    - Industry certifications
                    - Hands-on projects
                    - Mentorship programs
                    """)
                
                st.divider()
                
                # Learning plan
                st.markdown("### 📚 Your Personalized Learning Plan")
                
                if len(gaps) > 0:
                    timeline_tabs = st.tabs(['6-Month Plan', '12-Month Plan', '18-Month Plan'])
                    
                    with timeline_tabs[0]:
                        st.markdown(f"""
                        **Intensive Fast-Track ({len(gaps)} skills)**
                        
                        - **Month 1-2:** Online courses in top 2 priorities
                        - **Month 2-3:** Parallel learning + side projects
                        - **Month 4-5:** Advanced applications + portfolio
                        - **Month 6:** Interview prep + job search
                        """)
                    
                    with timeline_tabs[1]:
                        st.markdown(f"""
                        **Balanced Approach ({len(gaps)} skills)**
                        
                        - **Months 1-3:** Foundational knowledge
                        - **Months 4-6:** Intermediate projects
                        - **Months 7-9:** Advanced concepts
                        - **Months 10-12:** Specialization + job search
                        """)
                    
                    with timeline_tabs[2]:
                        st.markdown(f"""
                        **Comprehensive Development ({len(gaps)} skills)**
                        
                        - **Months 1-5:** Deep foundational learning
                        - **Months 6-10:** Industry-level projects
                        - **Months 11-15:** Expertise development
                        - **Months 16-18:** Leadership/mentoring + job search
                        """)
                
                st.divider()
                
                # Real-world scenarios
                st.markdown("### 💼 Real-World Transition Scenarios")
                
                scenarios = {
                    "Teacher → L&D": """
                    **Example: "I'm a teacher wanting to move into L&D or HR"**
                    
                    **Your Advantages:** Training experience, curriculum design, learner psychology
                    **Skills to Develop:** Learning technologies, corporate culture, compliance training
                    **Timeline:** 6-12 months
                    **First Roles:** Instructional Designer, Training Coordinator, Learning Content Creator
                    """,
                    "Project Engineer → Cloud Engineer": """
                    **Example: "I'm a project engineer aiming for cloud engineering"**
                    
                    **Your Advantages:** Project management, infrastructure planning, systems thinking
                    **Skills to Develop:** Cloud platforms (AWS/Azure), containerization, automation
                    **Timeline:** 9-15 months
                    **First Roles:** Cloud Operations, Infrastructure Support, DevOps Intern-level
                    """,
                    "Operations → Product Management": """
                    **Example: "I want to move from operations to product management"**
                    
                    **Your Advantages:** Process optimization, business acumen, stakeholder management
                    **Skills to Develop:** Product strategy, user research, data analytics
                    **Timeline:** 12-18 months
                    **First Roles:** Product Analyst, Associate Product Manager
                    """
                }
                
                selected_scenario = st.selectbox(
                    "Select a relevant scenario:",
                    options=list(scenarios.keys())
                )
                
                st.info(scenarios[selected_scenario])
                
                st.divider()
                
                # Action plan
                st.markdown("### ✨ Your Action Plan (Next 30 Days)")
                
                actions = [
                    ("📚", "Research Phase", "Study job postings, talk to people in target role"),
                    ("🎯", "Skill Assessment", "Identify top 3 skills to prioritize"),
                    ("📝", "Create Learning Plan", "Enroll in courses, find resources"),
                    ("🤝", "Start Networking", "Connect with professionals in target field"),
                    ("💼", "Build Portfolio", "Start small projects showcasing transition skills")
                ]
                
                for emoji, action, detail in actions:
                    st.success(f"{emoji} **{action}**\n\n{detail}")
    
    # ========================================================================
    # PAGE 4: MY CAREER PROFILE
    # ========================================================================
    elif app_mode == "📊 My Career Profile":
        st.markdown("## 📊 Your Personalized Career Profile")
        st.markdown("Build and track your career profile with real-time job market insights.")
        
        st.divider()
        
        # Create a simple profile builder
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name:", "")
            role = st.text_input("Current Role:", "")
            years = st.number_input("Years of Experience:", min_value=0, max_value=50, value=5)
            salary = st.number_input("Current Salary ($):", min_value=0, max_value=100000, value=5000, step=500)
        
        with col2:
            education = st.selectbox("Highest Education:", ["Diploma", "Bachelor's", "Master's", "PhD"])
            industry = st.selectbox("Current Industry:", df['primary_category'].unique()[:10])
            location = st.text_input("Location:", "Singapore")
            availability = st.selectbox("Job Search Status:", ["Open to Opportunities", "Passive", "Not Looking"])
        
        st.divider()
        
        st.markdown("### 🛠️ Your Skills & Proficiencies")
        
        skills_input = st.text_area(
            "Enter your skills (comma-separated):",
            value="Python, SQL, Analysis, Leadership",
            height=80
        )
        
        skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
        
        st.divider()
        
        # Market alignment
        st.markdown("### 📈 Your Market Position")
        
        if role:
            matching_roles = df[df['title'].str.contains(role, case=False, na=False)]
            
            if len(matching_roles) > 0:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    peer_salary = matching_roles['average_salary'].median()
                    salary_diff = salary - peer_salary
                    st.metric(
                        "Peer Median Salary",
                        f"${peer_salary:,.0f}",
                        f"{salary_diff:+,.0f}" if salary_diff != 0 else "At market"
                    )
                
                with col2:
                    peer_exp = matching_roles['minimumYearsExperience'].median()
                    st.metric(
                        "Typical Experience",
                        f"{peer_exp:.1f} years",
                        f"{years - peer_exp:+.1f}y" if years != peer_exp else "On track"
                    )
                
                with col3:
                    st.metric(
                        "Job Openings",
                        f"{len(matching_roles):,}",
                        "Active market"
                    )
                
                # Radar chart for skill requirements
                st.markdown("### 📊 Typical Skills for Your Role")
                
                from_titles = []
                for title in matching_roles['title'].head(50):
                    from_titles.extend(extract_skills_from_title(title))
                
                skill_counts = Counter(from_titles)
                top_skills = dict(skill_counts.most_common(8))
                
                if top_skills:
                    fig = px.bar(
                        x=list(top_skills.values()),
                        y=list(top_skills.keys()),
                        orientation='h',
                        title='Most Common Skills in Your Role',
                        labels={'x': 'Frequency', 'y': 'Skill'}
                    )
                    fig.update_layout(height=400, template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
    
    # ========================================================================
    # PAGE 5: USAGE GUIDE
    # ========================================================================
    elif app_mode == "💡 Usage Guide":
        st.markdown("## 💡 How to Use This Dashboard")
        
        st.divider()
        
        st.markdown("### 🎯 Getting Started")
        
        getting_started = """
        This dashboard is designed to help you navigate your career with data-driven insights. Here's how to get started:
        
        **1. Identify Your Profile**
        - Start on the Home page to see market overview
        - Identify which section matches your situation:
          - **Mid-Career Professional:** If you have 3-10 years experience and want promotion/growth
          - **Career Switcher:** If you're transitioning to a new domain/role
        
        **2. Enter Your Information**
        - Provide your current role, experience, and salary
        - List your current skills and proficiencies
        - Define your career goal and target role
        
        **3. Get Personalized Insights**
        - View market analysis for your current and target roles
        - Identify your skills gaps
        - Review salary growth projections
        - Get actionable recommendations
        """
        
        st.markdown(getting_started)
        
        st.divider()
        
        st.markdown("### 👤 For Mid-Career Professionals (3-10 years)")
        
        mid_career_guide = """
        **Use this section to answer:**
        - How do my current skills map to higher-level roles?
        - What are the top skills required for promotion in my field?
        - What roles offer the best salary jump given my current skill set?
        - How far am I from qualifying for a Senior/Manager role?
        - What are the fastest upskilling paths to reach my next milestone?
        
        **Key Features:**
        1. **Current & Target Role Analysis**
           - Compare average salary, experience requirements, and job openings
           - See your potential salary growth
        
        2. **Skills Gap Analysis**
           - Visualize skills you have vs. what's needed
           - Get specific skills to develop
        
        3. **Personalized Upskilling Roadmap**
           - Choose your timeline (3, 6, or 12 months)
           - Get structured learning path
           - See estimated salary progression
        
        4. **Action Items**
           - Concrete next steps to take
           - Resource recommendations
           - Interview preparation tips
        
        **Example Scenario:**
        *"I'm a QA Engineer with 5 years of experience. What's the most achievable path to becoming an SDET?"*
        - Input: QA Engineer + 5 years experience
        - Target: Senior QA / SDET
        - Result: See specific skills to develop (Python, CI/CD, automation), timeline, salary projection
        """
        
        st.markdown(mid_career_guide)
        
        st.divider()
        
        st.markdown("### 🔄 For Career Switchers (Domain Transition)")
        
        switcher_guide = """
        **Use this section to answer:**
        - Which roles are closest to my current skills even if in different industry?
        - What are common transition paths for someone with my background?
        - How big is the skill gap between my current and target role?
        - What is the expected time and effort for this transition?
        - Which of my transferable skills give me an advantage?
        
        **Key Features:**
        1. **Transition Feasibility Analysis**
           - Assess difficulty level of your transition
           - See target domain job market
           - Compare salary expectations
        
        2. **Transition Path Options**
           - Direct transition (fast track): 6-12 months
           - Gradual transition (stepping stone): 18-24 months
           - Choose what works for your situation
        
        3. **Skills & Advantages Analysis**
           - See your transferable skills
           - Identify critical gaps
           - Understand your competitive advantages
        
        4. **Real-World Scenarios**
           - Learn from similar transitions
           - See actual career paths
           - Get timeline expectations
        
        **Example Scenarios:**
        
        *"I'm a teacher wanting to move into L&D or HR"*
        - Your Advantages: Training experience, curriculum design, understanding of learning
        - Skills to Develop: Learning technologies, corporate structures, compliance training
        - Timeline: 6-12 months to transition
        - First Roles: Instructional Designer, Training Coordinator, L&D Specialist
        
        *"I'm a project engineer aiming for a cloud engineering role"*
        - Your Advantages: Project management, infrastructure knowledge, systems thinking
        - Skills to Develop: Cloud platforms (AWS/Azure/GCP), containerization, IaC
        - Timeline: 9-15 months
        - First Roles: Cloud Operations, Infrastructure Support, Junior DevOps Engineer
        """
        
        st.markdown(switcher_guide)
        
        st.divider()
        
        st.markdown("### 📊 Understanding the Insights")
        
        insights_guide = """
        **Skills Gap Color Coding:**
        - ✅ **Green (Your Advantages):** Skills you already have that match the role
        - ❌ **Red (Gaps):** Skills missing that you need to develop
        
        **Salary Projections:**
        - Based on actual market data from job postings
        - Conservative estimates for timeline
        - Accounts for skill development in your field
        
        **Experience Requirements:**
        - Median values from actual job postings
        - Shows realistic entry points
        - Helps identify which roles are within reach
        
        **Timeline Estimates:**
        - Based on complexity and number of skills
        - Assumes consistent effort
        - Can be accelerated with focused learning
        """
        
        st.markdown(insights_guide)
        
        st.divider()
        
        st.markdown("### 💡 Tips for Best Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Do's ✅**
            - Be honest about your current skills
            - Set realistic career goals
            - Focus on high-impact skills first
            - Update your profile regularly
            - Take action on recommendations
            - Seek mentorship in your field
            - Network while learning
            """)
        
        with col2:
            st.markdown("""
            **Don'ts ❌**
            - Don't ignore foundational skills
            - Don't rush the transition
            - Don't learn everything at once
            - Don't rely only on this tool
            - Don't skip portfolio building
            - Don't underestimate soft skills
            - Don't give up during the learning
            """)
        
        st.divider()
        
        st.markdown("### 🔗 Additional Resources")
        
        resources = {
            "Learning Platforms": """
            - **Coursera:** Structured courses with certificates
            - **Udemy:** Affordable, wide range of topics
            - **LinkedIn Learning:** Professional development
            - **Pluralsight:** Technical skill development
            - **DataCamp/Codecademy:** Hands-on coding practice
            """,
            
            "Portfolio Building": """
            - **GitHub:** Showcase your code projects
            - **Medium/Dev.to:** Write about what you learn
            - **Personal Website:** Professional portfolio
            - **Kaggle:** Data science competitions
            - **LeetCode:** Algorithm practice
            """,
            
            "Career Development": """
            - **LinkedIn:** Professional networking
            - **Industry Conferences:** Stay current
            - **Meetups:** Local community events
            - **Mentorship Programs:** Learn from others
            - **Reddit/Discord Communities:** Peer support
            """,
            
            "Job Search": """
            - **LinkedIn Jobs:** Largest professional network
            - **Glassdoor:** Company insights and reviews
            - **Indeed:** Comprehensive job board
            - **GitHub Jobs:** Tech-focused roles
            - **Specialized Boards:** Domain-specific boards
            """
        }
        
        for category, content in resources.items():
            with st.expander(f"🎯 {category}"):
                st.markdown(content)
        
        st.divider()
        
        st.markdown("### ❓ FAQ")
        
        with st.expander("How often should I update my profile?"):
            st.markdown("""
            Update your profile every 3 months or whenever you:
            - Learn a new significant skill
            - Get promoted or move to a new role
            - Complete a major project
            - Achieve a salary increase
            - Make progress on your career goal
            """)
        
        with st.expander("Can I use this if I'm just starting my career?"):
            st.markdown("""
            Yes! While optimized for early career+ professionals, the insights are valuable for:
            - Understanding what skills are in demand
            - Planning your learning path
            - Identifying entry-level opportunities
            - Setting realistic career goals
            
            Consider starting as "Early Career (0-3 years)" on the home page.
            """)
        
        with st.expander("How accurate are the salary projections?"):
            st.markdown("""
            Salary projections are based on:
            - Actual job posting data from the market
            - Conservative growth estimates
            - Industry standards
            
            Actual results vary based on:
            - Your negotiation skills
            - Company size and location
            - Specific skill combination
            - Market demand
            
            Use these as guidance, not guarantees.
            """)
        
        with st.expander("What if my target role isn't in the database?"):
            st.markdown("""
            If you don't find exact matches:
            1. Try similar role titles
            2. Search for related positions
            3. Look at adjacent career paths
            4. Identify the closest match
            5. Synthesize insights from multiple similar roles
            
            Always supplement with manual research.
            """)
        
        st.divider()
        
        st.markdown("### 📞 Support & Feedback")
        
        st.info("""
        **Have questions or feedback?**
        
        This tool is designed to provide data-driven career insights. Remember:
        - Use these insights as guidance, not absolute truth
        - Each career path is unique
        - Combine data insights with personal reflection
        - Seek mentorship for personalized advice
        - Stay flexible and adapt as you learn
        
        **Good luck with your career journey! 🚀**
        """)

if __name__ == "__main__":
    main()

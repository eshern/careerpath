# 🚀 QUICKSTART GUIDE

Get up and running in 5 minutes!

---

## ⚡ 5-Minute Setup

### 1. **Install Python** (if needed)
   - Download from: https://www.python.org/downloads/
   - Requires Python 3.8 or higher
   - Check version: `python --version`

### 2. **Project Folder Directory**
   - Place SGJobData.csv file to folder `data`
   ```bash
   data/SGJobData.csv
   ```

### 3. **Install Dependencies** (2-3 minutes)
   ```bash
   conda env create -f environment.yml
   ```

### 4. **Activate Environment**
   ```bash
   conda activate careerpath_app
   ```
### 5. **Start Dashboard**
   ```bash
   streamlit run dashboard.py
   ```
### 6. **Access Dashboard**
   Opens automatically in browser at: `http://localhost:8501`

---

## 🎯 First Time Using Dashboard?

### Step 1: Home & Overview (2 minutes)
- See market statistics
- Understand your professional profile
- Browse industry trends
- View salary insights

### Step 2: Select Your Path
Choose based on your situation:

**👤 Mid-Career Professional** (3-10 years experience)
- Want promotion or role growth
- Looking for salary increase
- Ready to develop new skills

**🔄 Career Switcher** (Any experience level)
- Transitioning to new domain
- Changing industries
- Building on transfer skills

### Step 3: Enter Your Information
Fill in your profile:
- Current role
- Years of experience
- Current salary
- Your skills
- Career goal

### Step 4: Get Insights
Review personalized analysis:
- Market comparison
- Skills gap analysis
- Recommended learning path
- Salary projections
- Action items

### Step 5: Take Action
Follow recommendations:
- Enroll in courses
- Build portfolio projects
- Update your resume
- Network in target domain

---

## 📊 Quick Examples

### Example 1: QA Engineer → SDET (Mid-Career)

**Input:**
- Current Role: QA Engineer
- Experience: 5 years
- Current Salary: $4,000/month
- Skills: Test Automation, Python, JavaScript
- Target: Senior QA / SDET

**Result:**
- Market has 150+ SDET roles
- Average SDET salary: $5,500-$6,000/month
- Potential salary jump: +25% ($4,750→$6,000+)
- Required new skills: Advanced Python, CI/CD, DevOps basics
- Timeline: 3-6 months with focused learning
- Recommended path: Python mastery → CI/CD pipeline practice → SDET interview prep

---

### Example 2: Teacher → L&D (Career Switcher)

**Input:**
- Current Background: Teaching (10 years)
- Target Domain: Learning & Development (L&D)
- Transferable Skills: Communication, Training, Curriculum Design

**Result:**
- L&D market has 200+ openings
- Entry role: Training Coordinator / Instructional Designer
- Salary range: $3,500-$4,500/month
- Transition difficulty: Low-Moderate
- Your advantages: Training experience, adult learning understanding
- Skill gaps: Learning management systems (LMS), compliance training
- Timeline: 6-12 months for entry role
- Recommended path: Online L&D certificate → LMS training → Build portfolio

---

## 🎓 Common Scenarios

### Scenario 1: Promotion Within Same Role
*"I want to become a Team Lead but stay in my technical domain"*

**Use:** Mid-Career Professional → Input leadership as target
**Timeline:** 12-18 months
**Key Skills:** Leadership, communication, mentoring
**Salary Impact:** +20-30%

### Scenario 2: Specialization Path
*"I'm a full-stack engineer but want to specialize in cloud engineering"*

**Use:** Mid-Career Professional → Input cloud role as target
**Timeline:** 6-12 months
**Key Skills:** AWS/Azure, Infrastructure as Code, DevOps
**Salary Impact:** +15-25%

### Scenario 3: Industry Transition
*"I work in operations but want to move to tech product management"*

**Use:** Career Switcher → Select target industry
**Timeline:** 12-18 months (direct path: 9-12 months)
**Your Advantages:** Process optimization, business understanding
**Key Skills:** Data analysis, user research, product strategy
**Salary Impact:** Varies by background

### Scenario 4: Complete Domain Shift
*"I'm a mechanical engineer interested in software development"*

**Use:** Career Switcher → Select software domain
**Timeline:** 12-24 months (depends on depth)
**Your Advantages:** Problem-solving, logical thinking, project management
**Key Skills:** Programming language, web frameworks, software design patterns
**Salary Impact:** +10-20% after transition

---

## 🛠️ Troubleshooting

### **Dashboard won't start**
```
Error: Module not found (streamlit, pandas, etc.)
Fix: pip install -r requirements.txt
```

### **Data file error**
```
Error: Cannot open file SGJobData.csv
Fix: Make sure SGJobData.csv is in the same folder as dashboard.py
```

### **Dashboard slow**
```
First load takes 1-2 minutes (data caching)
Subsequent loads are instant
To clear cache: Delete .streamlit/cache folder
```

### **Port already in use**
```
Error: Port 8501 already in use
Fix: streamlit run dashboard.py --server.port 8502
```

### **Import errors on first run**
```
Restart Python kernel/terminal after pip install
Command: pip install -r requirements.txt --force-reinstall
```

---

## 📚 Key Reports & Outputs

### 1. **Skills Gap Report**
- Your current skills (green ✅)
- Missing skills (red ❌)
- Priority order for learning
- Estimated learning time

### 2. **Market Analysis Report**
- Job openings for target role
- Average salary and range
- Experience requirements
- Top companies hiring
- Employment types available

### 3. **Career Path Recommendation**
- Timeline to target role
- Monthly milestones
- Required learning resources
- Salary projections
- Portfolio projects needed

### 4. **Salary Projection**
- Current salary baseline
- Projected salary with key skills (3-6 months)
- Projected salary with promotion (12 months)
- Long-term salary potential (24 months)

---

## 💡 Pro Tips

### ✅ Maximize Your Learning
1. **Focus on Top 3 Skills** - Don't try to learn everything
2. **Build Projects** - Apply learning to real projects
3. **Get Mentorship** - Find experienced people in target role
4. **Network Early** - Start connecting before you're job-ready
5. **Update Resume** - Highlight transferable skills

### ✅ Job Search Tips
1. **Data-Driven Approach** - Use market insights from dashboard
2. **Portfolio Evidence** - Showcase projects matching target role
3. **Network First** - 70% of jobs filled through connections
4. **Target Companies** - Research companies hiring for target role
5. **Negotiate Salary** - Use dashboard salary data in negotiations

### ✅ Timeline Management
- **Month 1:** Learning + side projects
- **Month 2-3:** Deeper projects + portfolio building
- **Month 4-5:** Interview preparation + networking
- **Month 6+:** Active job search with confidence

---

## 🔗 External Resources

### Learning Platforms
- **Coursera** - University-backed courses
- **Udemy** - Affordable, practical courses
- **Pluralsight** - Technical skills focus
- **LinkedIn Learning** - Professional development
- **Codecademy/DataCamp** - Hands-on practice

### Portfolio/Practice
- **GitHub** - Showcase your code
- **LeetCode** - Algorithm practice
- **Kaggle** - Data science competitions
- **Medium** - Write about what you learn

### Networking
- **LinkedIn** - Professional network
- **Meetup.com** - Local tech communities
- **GitHub** - Open source contributions
- **Twitter/Dev.to** - Tech community

### Job Boards
- **LinkedIn Jobs** - Largest professional network
- **Glassdoor** - Company reviews + jobs
- **Indeed** - Comprehensive job board
- **GitHub Jobs** - Tech roles
- **Specialized Boards** - Domain-specific jobs

---

## 📞 Getting Help

### Within Dashboard
- **Usage Guide Tab** - Comprehensive tutorials
- **FAQ Section** - Common questions
- **Real-world Examples** - Learn from scenarios
- **Resource Recommendations** - Links to learning platforms

### External Support
- **Documentation** - Detailed guides
- **Example Walkthrough** - Watch demo scenarios
- **Community Forums** - Ask other users

---

## ✨ Next Steps After Setup

1. **Today:** Explore Home & Overview
2. **This Week:** Complete your profile analysis
3. **Week 2:** Choose learning path + enroll in courses
4. **Month 1:** Start building portfolio projects
5. **Month 3:** Interview preparation
6. **Month 6:** Active job search

---

## 🎯 Remember

> "Career progression is a marathon, not a sprint. Use data to guide your decisions, stay consistent with learning, and network actively. You've got this! 🚀"

---

**Ready to start? Run:** 
```bash
streamlit run dashboard.py
```

**Questions?** Check the Usage Guide inside the dashboard!

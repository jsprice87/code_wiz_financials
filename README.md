# code_wiz_financials
Python scripts to generate cashflow, profit-loss, etc. for Code Wiz franchise startup.


## ASSUMPTIONS
### Timeline Definition
FRAN_START_DATE = Jan 15, 2024
SIGN_LEASE = FRAN_START_DATE + 2 Months
BUILDOUT_COMPLETE = SIGN_LEASE + 10 Weeks
GRAND_OPENING = BUILDOUT_COMPLETE + 3 Weeks
TRAINING_START = FRAN_START_DATE
TRAINING_COMPLETE = TRAINING_START + 8 Weeks
DIRECTOR_HIRED = GRAND_OPENING - 8 Weeks
STAFF_HIRING_START = GRAND_OPENING - 6 Weeks
PERIOD_END = Dec 31, 2026


### Revenue Variables
GO_STUDENT_COUNT = 50 # Grand opening student count
GROWTH_RATE = 10%
SS_STUDENT_COUNT = 384 # 80% of maximum possible
MAX_STUDENTS = 480 # See below calculation
MONTHLY_STUDENT_PRICE = 225 # Dollars, 2x classes per week #Comparable to Code Ninjas in Denver-Metro area
camp_revenue = 300 * 15 # 15 kids at $300 # Wild guess

### Expense Variables
SQ_FT = 1500 # facility
LEASE = 28 * SQ_FT # yearly
NNN = 10 * SQ_FT # yearly
RENT = (LEASE + NNN) / 12
DIR_SALARY = 65000 / 12 # Guessed here
HOURLY_RATE = 30 # Guessed here
INTEREST_RATE = 9%
INST_COMP_COST = 17500 # cost of instructional equpiment
USEFUL_LIFE = 36 # 36 Months, 3 years # for depreciation
TAX = 2.9%
ROYALTY = 9%

### CASHFLOW
STARTING_LIQUID = 50000
STARTING_HELOC = 115000
STARTING_CASH = STARTING_LIQUID + STARTING_HELOC # assume use of available HELOC to make sure cashflow never runs negative

### Calculating max number of students
1. The max number of students a teacher can teach at once is 4.
2. There are up to 16 kids per session (so that's 16/4 = 4 teachers per session).
3. There are up to 3 sessions per night.
4. There are sessions 5 nights per week.
5. Each student comes 2 times per week (as you've mentioned to keep sessions_per_student_weekly constant at 2).

Assuming 4 weeks per month.

1. First, let's find out how many students can be handled in a single session:
   Maximum students in one session = 4 students/teacher × 4 teachers = 16 students (as given)

2. Maximum students in a day (since they come twice a week and there are 5 days in a week):
   Maximum students/day = 16 students/session × 3 sessions/day = 48 students

3. Now, because each student comes 2 times a week:
   Maximum unique students in a day = 48 students/day ÷ 2 = 24 students/day

4. Over a week:
   Maximum unique students/week = 24 students/day × 5 days/week = 120 students

5. Finally, over a month (assuming 4 weeks per month):
   Maximum unique students/month = 120 students/week × 4 weeks/month = 480 students

So, based on the given rules, the maximum number of unique students that can be accommodated in a month is 480 students.

### Calculating the number of teachers based on current student count
    MAX_STUDENTS_PER_TEACHER = 4
    MAX_STUDENTS_PER_SESSION = 16
    SESSIONS_PER_NIGHT = 3
    NIGHTS_PER_WEEK = 5
    WEEKS_PER_MONTH = 4
    SESSIONS_PER_STUDENT_WEEKLY = 2

    # Calculate total sessions a student attends per month
    sessions_per_student_monthly = SESSIONS_PER_STUDENT_WEEKLY * WEEKS_PER_MONTH
    
    # Total sessions for all students
    total_sessions_monthly = student_count * sessions_per_student_monthly
    
    # Teachers required for each session
    teachers_per_session = MAX_STUDENTS_PER_SESSION / MAX_STUDENTS_PER_TEACHER
    
    # Total teacher sessions required monthly
    total_teacher_sessions_monthly = teachers_per_session * total_sessions_monthly
    
    # Given there are multiple sessions per night and multiple nights per week,
    # calculate the number of sessions a single teacher can conduct in a month
    sessions_per_teacher_monthly = SESSIONS_PER_NIGHT * NIGHTS_PER_WEEK * WEEKS_PER_MONTH

    # Calculate total number of teachers needed monthly
    num_teachers = total_teacher_sessions_monthly / sessions_per_teacher_monthly
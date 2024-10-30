import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict


def read_student_data(file_path):
    """Read data from csv file and return"""
    students_list = []
    with open(file_path, mode='r') as file:
        headers = file.readline().strip().split(",")
        for line in file:
            student = {}
            values = line.strip().split(",")
            for i, header in enumerate(headers):
                student[header.strip()] = values[i].strip()
                if header.strip() == "CGPA":
                    student[header.strip()] = float(student[header.strip()])

            students_list.append(student)

    return students_list


def pick_student(all_students, tut_grp):
    """pick student out from the tutorial group"""
    students_list = []

    for student in all_students:
        if student['Tutorial Group'] == f'G-{tut_grp}':
            students_list.append(student)

    return students_list


def diverse_team(sorted_student_more, sorted_student_less, team_index):  # index(0,-1,or middle)
    team = []
    i = 0  # round
    sorted_student = [sorted_student_more, sorted_student_less]

    gender_run_two_time = False
    next_gender_same = False
    if len(sorted_student_more) - len(sorted_student_less) >= 10-team_index:
        gender_run_two_time = True

    gender_index = 0

    while len(team) < 5 and (sorted_student[0] or sorted_student[1]):  # add student into team when teams is not full
        index_changes = [+1, -1, +1]
        pick_index = [0, -1, len(sorted_student[gender_index]) // 2]
        while True:
            if not sorted_student[gender_index]:
                break
            elif index_changes[i] >= 0 and pick_index[i] + index_changes[i] < len(sorted_student[gender_index]) and index_changes[
                i] <= 5:
                # Check if school is not in the team
                if sorted_student[gender_index][pick_index[i] + index_changes[i]]['School'] not in [student['School'] for student in
                                                                                                    team]:
                    team.append(sorted_student[gender_index].pop(pick_index[i] + index_changes[i]))
                    break
                else:
                    index_changes[i] += 1
            elif index_changes[i] < 0 and abs(pick_index[i] + index_changes[i]) <= len(sorted_student[gender_index]) and abs(
                    index_changes[i]) <= 5:
                # Check if school is not in the team
                if sorted_student[gender_index][pick_index[i] + index_changes[i]]['School'] not in [student['School'] for student in
                                                                                                    team]:
                    team.append(sorted_student[gender_index].pop(pick_index[i] + index_changes[i]))
                    break
                else:
                    index_changes[i] -= 1
            else:
                # If the index exceeds the list length, reset index_changes or break
                team.append(sorted_student[gender_index].pop(pick_index[i]))
                break

        i += 1
        if not next_gender_same:
            gender_index += 1
        elif next_gender_same:
            next_gender_same = False
        if i > 2:
            i = 0
        if gender_index > 1:
            gender_index = 0

        if gender_run_two_time:
            gender_index = 0
            gender_run_two_time = False
            next_gender_same = True

    return team


def division_into_team(students_list):
    """Divides student from student_list into group of 5 with balance of cgpa and gender, and diverse of school"""
    # Separate male and female students into two lists
    male_students = [student for student in students_list if student['Gender'] == 'Male']
    female_students = [student for student in students_list if student['Gender'] == 'Female']

    # Sort the male and female students by CGPA
    male_sorted_students = sorted(male_students, key=lambda student: student['CGPA'])
    female_sorted_students = sorted(female_students, key=lambda student: student['CGPA'])

    teams = [[] for _ in range(len(students_list) // 5)]
    team_index = 0

    while team_index < len(teams):  # while haven't added student into all teams
        if len(male_sorted_students) >= len(female_sorted_students):  # if remain male student more than remain female student
            teams[team_index] = diverse_team(male_sorted_students, female_sorted_students, team_index)

        else:  # if remain male student less than remain female student
            teams[team_index] = diverse_team(female_sorted_students, male_sorted_students, team_index)

        team_index += 1

    return teams


def see_group_division(group_div):
    for i, x in enumerate(group_div):
        print(f"Group {i}")
        cgpa = 0
        for j in x:
            print(j["Student ID"], j["School"], j["CGPA"], j["Gender"])
            cgpa += j["CGPA"]
        print(f" the mean cgpa of this group is {cgpa / len(x)}")
        print()


def count_students_by_school(students):
    """Count the number of males and females from each school."""
    school_counts = defaultdict(lambda: {'Male': 0, 'Female': 0})

    for student in students:
        school = student['School']
        if student['Gender'] == 'Male':
            school_counts[school]['Male'] += 1
        else:
            school_counts[school]['Female'] += 1

    return school_counts

def visualize_school_representation(school_counts):
    """Visualize the representation of males and females from each school in a stacked bar chart."""
    schools = list(school_counts.keys())
    males = [school_counts[school]['Male'] for school in schools]
    females = [school_counts[school]['Female'] for school in schools]
    total_students = [school_counts[school]['Male'] + school_counts[school]['Female'] for school in schools]  # Total students in each school

    x = range(len(schools))  # x-axis locations

    plt.figure(figsize=(12, 6))
    bars_male = plt.bar(x, males, label='Males', color='skyblue')
    bars_female = plt.bar(x, females, bottom=males, label='Females', color='lightcoral')  # Stack females on top of males

    # Adding counts on top of each bar
    for bar in bars_male:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), 
                 ha='center', va='bottom', fontsize=10)  # Centered above male bar

    for bar in bars_female:
        yval = bar.get_height() + bars_male[bars_female.index(bar)].get_height()  # Get the top of the stacked female bar
        plt.text(bar.get_x() + bar.get_width() / 2, yval, int(bar.get_height()), 
                 ha='center', va='bottom', fontsize=10)  # Centered above female bar

    # Updating x-ticks to include total students
    x_labels = [f"{school}\n ({total})" for school, total in zip(schools, total_students)]
    plt.xticks(x, x_labels, rotation=45, ha='right')

    plt.xlabel('Schools')
    plt.ylabel('Number of Students')
    plt.title('School Representation by Gender')
    plt.legend()
    plt.tight_layout()
    plt.show()



def count_unique_schools_in_division(group_division):
    """Count the number of unique schools in each team."""
    unique_school_counts = []

    for team in group_division:
        schools_in_team = set(student['School'] for student in team)  # Use a set to get unique schools
        unique_school_counts.append(len(schools_in_team))  # Count of unique schools

    return unique_school_counts

def visualize_unique_school_distribution(unique_school_counts):
    """Visualize the distribution of unique schools in teams as a histogram."""
    plt.figure(figsize=(10, 6))
    counts, bins, patches = plt.hist(unique_school_counts, bins=range(1, max(unique_school_counts) + 2), 
                                      color='skyblue', edgecolor='black', align='left')
    
    plt.xticks(range(1, max(unique_school_counts) + 1))  # Set x-ticks
    plt.xlabel("Number of Unique Schools per Team")
    plt.ylabel("Number of Teams")
    plt.title("Distribution of Unique Schools in Teams")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adding labels on top of each bar
    for count, x in zip(counts, bins):
        if count > 0:  # Only label if there's a bar
            plt.text(x, count, int(count), ha='center', va='bottom')

    plt.show()











students = read_student_data('records.csv')
group_division = []
tutorial_grp = 1

while tutorial_grp <= 150:
    group_division.extend(division_into_team(pick_student(students, tutorial_grp)))
    tutorial_grp += 1

see_group_division(group_division)

with open("group-base.txt", mode="w") as f:
    for i, x in enumerate(group_division):
        f.write(f"Group {i}\n")
        cgpa = 0
        for j in x:
            l = f"{j['Student ID'], j['School'], j['CGPA'], j['Gender']}\n"
            f.write(l)
            cgpa += j["CGPA"]
        f.write(f" the mean cgpa of this group is {cgpa / len(x)}\n")
        f.write("\n")


school_counts = count_students_by_school(students)
visualize_school_representation(school_counts)#stacked bar graph

# Assuming you have your group_division variable from previous code
unique_school_counts = count_unique_schools_in_division(group_division)
visualize_unique_school_distribution(unique_school_counts)#bar graph

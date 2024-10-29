#import matplotlib.pyplot as plt
#import seaborn as sns
import math

def read_student_data(file_path):
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


def division_into_team(students_list, size):
    # Separate male and female students into two lists
    male_students = [student for student in students_list if student['Gender'] == 'Male']
    female_students = [student for student in students_list if student['Gender'] == 'Female']

    # Sort the male and female students by CGPA
    male_sorted_students = sorted(male_students, key=lambda student: student['CGPA'])
    female_sorted_students = sorted(female_students, key=lambda student: student['CGPA'])

    teams = [[] for _ in range(len(students_list) // size)]
    team_index = 0

    while team_index < len(teams):
        if len(male_sorted_students) >= len(female_sorted_students):
            teams[team_index].append(male_sorted_students.pop(0))
            teams[team_index].append(male_sorted_students.pop(-1))
            teams[team_index].append(male_sorted_students.pop(len(male_sorted_students) // 2))

            teams[team_index].append(female_sorted_students.pop(0))
            teams[team_index].append(female_sorted_students.pop(-1))

        else:
            teams[team_index].append(male_sorted_students.pop(0))
            teams[team_index].append(male_sorted_students.pop(-1))

            teams[team_index].append(female_sorted_students.pop(0))
            teams[team_index].append(female_sorted_students.pop(-1))
            teams[team_index].append(female_sorted_students.pop(len(male_sorted_students) // 2))

        team_index += 1

    return teams

students = read_student_data('records.csv')
group_division = []
tutorial_grp = 1
team_size = 5

group_division.extend(division_into_team(pick_student(students, tutorial_grp), team_size))


def visualize_data(group_division):
    total_sd = []
    total_deviations = []
    compiled_z_score = []

    for i, x in enumerate(group_division):
        print(f"Group {i}")
        total_cgpa = 0
        icgpa = []
        for j in x:
            print(j["Student ID"], j["School"], j["CGPA"])
            total_cgpa += j["CGPA"]
            icgpa.append(j["CGPA"])

        mean = total_cgpa / 5
        deviations = [(each-mean)**2 for each in icgpa]
        variance = sum(deviations) / 5
        sd = math.sqrt(variance)
        total_sd.append(sd)
        total_deviations.extend(deviations)
        
        z_score = [(each - mean) / sd for each in icgpa]
        compiled_z_score.extend(z_score)

        print(f"The mean cgpa of this group is {mean}\nThe variance of this group is {variance:.5f}\nThe standard deviation of this group is {sd:.5f}")
        print()

    print (f"compiled z score list: {compiled_z_score}")

visualize_data(group_division)

# while tutorial_grp <= 150:
#     group_division.extend(division_into_teams(students, tutorial_grp, team_size))

# add
import math

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

students = read_student_data('records.csv')
group_division = []
tutorial_grp = 1

while tutorial_grp <= 150:
    group_division.extend(division_into_team(pick_student(students, tutorial_grp)))
    tutorial_grp += 1

visualize_data(group_division)

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
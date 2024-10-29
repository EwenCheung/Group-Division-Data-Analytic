# import matplotlib.pyplot as plt
# import seaborn as sns


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


def diverse_team(size_team, sorted_student_more, sorted_student_less):  # size of team, index(0,-1,or middle)
    team = []
    i = 0  # round
    sorted_student = [sorted_student_more, sorted_student_less]

    gender_run_two_time = False
    if size_team % 2 == 0 and len(sorted_student_more) - len(sorted_student_less) >= size_team / 2:
        gender_run_two_time = True

    gender_index = 0

    while len(team) < size_team and (sorted_student[0] or sorted_student[1]):  # add student into team when teams is not full
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
        gender_index += 1
        if i > 2:
            i = 0
        if gender_index > 1 or gender_run_two_time:
            gender_index = 0
            gender_run_two_time = False

    return team


def division_into_team(students_list, size):
    """Divides student from student_list into group of size with balance of cgpa and gender, and diverse of school"""
    # Separate male and female students into two lists
    male_students = [student for student in students_list if student['Gender'] == 'Male']
    female_students = [student for student in students_list if student['Gender'] == 'Female']

    # Sort the male and female students by CGPA
    male_sorted_students = sorted(male_students, key=lambda student: student['CGPA'])
    female_sorted_students = sorted(female_students, key=lambda student: student['CGPA'])

    teams = [[] for _ in range(len(students_list) // size)]
    team_index = 0

    while team_index < len(teams):  # while haven't added student into all teams
        if len(male_sorted_students) >= len(female_sorted_students):  # if remain male student more than remain female student
            teams[team_index] = diverse_team(size, male_sorted_students, female_sorted_students)

        else:  # if remain male student less than remain female student
            teams[team_index] = diverse_team(size, female_sorted_students, male_sorted_students)

        team_index += 1

    first_run = True
    while male_sorted_students or female_sorted_students:
        for team in teams:
            male = sum(1 for student in team if student['Gender'] == 'Male')
            female = sum(1 for student in team if student['Gender'] == 'Female')

            # Handle male students first
            if male_sorted_students:
                if male > female:
                    continue
                elif female > male:
                    team.append(male_sorted_students.pop(0))
                    continue
                elif not first_run and male - female < 2:
                    team.append(male_sorted_students.pop(0))
                    continue

            # Handle female students
            if female_sorted_students:
                if male > female:
                    team.append(female_sorted_students.pop(0))
                    continue
                elif female > male:
                    continue
                elif not first_run and female - male < 2:
                    team.append(female_sorted_students.pop(0))
                    continue

        if not first_run:
            break

        # Mark the first run complete
        first_run = False

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


students = read_student_data('records.csv')
group_division = []
tutorial_grp = 1
team_size = int(input("Input the desired number of students in a group:"))  # can adjust

while tutorial_grp <= 150:
    group_division.extend(division_into_team(pick_student(students, tutorial_grp), team_size))
    tutorial_grp += 1

see_group_division(group_division)

import matplotlib.pyplot as plt

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
    all_sd = []
    all_deviations = []
    all_mean = []
    compiled_z_score = []
    compiled_gender = []
    unique_school_counts = []

    for i, x in enumerate(group_division):
        print(f"Group {i}")
        total_cgpa = 0
        ind_cgpa = []
        ind_gender = []
        ind_school =[]
        for j in x:
            #print(j["Student ID"], j["School"], j["CGPA"],j["Gender"])
            total_cgpa += j["CGPA"]
            ind_cgpa.append(j["CGPA"])
            ind_gender.append(j["Gender"])
            ind_school.append(j["School"])

        ind_mean = total_cgpa / 5
        deviations = [(each-ind_mean)**2 for each in ind_cgpa]
        variance = sum(deviations) / 5
        sd = (variance)**0.5
        all_sd.append(sd)
        all_mean.append(ind_mean)
        schools_in_team = set(sch for sch in ind_school)  # Use a set to get unique schools
        unique_school_counts.append(len(schools_in_team))  # Count of unique schools

        compiled_gender.append(ind_gender)

        #z_score = [(each - ind_mean) / sd for each in ind_cgpa]
        #compiled_z_score.extend(z_score)

        print(f"The mean CGPA of {i} group is {ind_mean:.2f}")
        print(f"The variance of {i} group is {variance:.5f}")
        print(f"The standard deviation of {i} group is {sd:.5f}")
        print()
    
    total_mean = sum(all_mean) / len(all_mean)
    population_deviations = [(each-total_mean)**2 for each in all_mean]
    population_sd = (sum(population_deviations) / len(all_mean))**0.5
    
    
    print(f"The mean of the population is {total_mean:.2f}")
    print(f"The standard deviation of the population is {population_sd:.5f}")
    #print(f"Compiled Gender: {compiled_gender}")
    #print (f"compiled school list: {unique_school_counts}")

    for i in all_mean:
        z_score = (i - total_mean) / population_sd
        compiled_z_score.append(z_score)

    #print (f"compiled z score list: {compiled_z_score}")

    count_gender = {'m5f0' : 0, 'm4f1' : 0, 'm3f2' : 0, 'm2f3' : 0, 'm1f4': 0, 'm0f5' : 0}
    for teamg in compiled_gender:
        count = sum(1 for gender in teamg if gender == "Male")
        if count > 5:
            count = 5
        count_gender[f'm{count}f{5-count}'] += 1
    print(f"Gender count {count_gender}")

    # Data for the bar chart (this to visualize the count_gender dict)
    labels = list(count_gender.keys())  # Category labels like 'm5f0', 'm4f1', etc.
    frequencies = list(count_gender.values())  # Corresponding frequencies for each category
    
    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create the bar chart
    bars = ax.bar(labels, frequencies, color='skyblue')
    
    # Adding titles and labels
    ax.set_title("Frequency of Gender Composition in Teams")
    ax.set_xlabel("Gender Composition (e.g., m5f0 means 5 males, 0 females)")
    ax.set_ylabel("Number of Teams")
    
    # Adding frequency labels on top of each bar
    for bar in bars:
        yval = bar.get_height()  # Get the height of each bar
        ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')
    
    # Display the chart
    plt.xticks(rotation=45)
    plt.show()

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

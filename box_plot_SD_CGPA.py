import math
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


def calculate_sd(group_division):
    sd_values = []
    
    # Calculate SD for each team's CGPA
    for team in group_division:
        cgpa_values = [student["CGPA"] for student in team]
        
        if len(cgpa_values) > 1:  # SD calculation requires at least two values
            mean = sum(cgpa_values) / len(cgpa_values)
            variance = sum((x - mean) ** 2 for x in cgpa_values) / (len(cgpa_values) - 1)
            sd = math.sqrt(variance)
            sd_values.append(sd)

    return sd_values

# Calculate standard deviations
sd_values = calculate_sd(group_division)

# Calculate percentiles manually
sd_values.sort()
n = len(sd_values)

percentiles = {
    '0th': sd_values[0],
    '25th': sd_values[int(0.25 * n)],
    '50th': sd_values[int(0.5 * n)],
    '75th': sd_values[int(0.75 * n)],
    '100th': sd_values[-1]
}

# Count teams in each percentile
percentile_counts = {
    '0th': sum(1 for sd in sd_values if sd == percentiles['0th']),
    '25th': sum(1 for sd in sd_values if sd <= percentiles['25th']),
    '50th': sum(1 for sd in sd_values if sd <= percentiles['50th']),
    '75th': sum(1 for sd in sd_values if sd <= percentiles['75th']),
    '100th': len(sd_values)  # All teams
}

# Calculate IQR and determine outliers
Q1 = percentiles['25th']
Q3 = percentiles['75th']
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Calculate percentiles and prepare text
percentile_info = ""
for key in percentiles:
    line = f"{key} Percentile SD: {percentiles[key]:.4f}, Number of Teams: {percentile_counts[key]}"
    print(line)  # Original print statement
    percentile_info += line + "\n"  # Append each line to a single string for display

# Add number of outliers to the text string
# Count outliers
outliers = [sd for sd in sd_values if sd < lower_bound or sd > upper_bound]
num_outliers = len(outliers)
print(f"Number of outliers: {num_outliers}")  # Original print statement
percentile_info += f"Number of outliers: {num_outliers}"



# Create a boxplot for SD values
plt.figure(figsize=(10, 6))
plt.boxplot(sd_values, vert=False)

# Set x-axis limits based on the maximum SD + 0.2
plt.xlim(0, max(sd_values) + 0.2)

# Adding titles and labels
plt.title('Boxplot of Standard Deviations of CGPA Across Teams')
plt.xlabel('Standard Deviation (SD)')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.grid(axis='x', linestyle='--')

# Annotate each percentile on the plot with varying vertical positions to avoid overlap
y_pos = 1.4
gap = 0.2

# Dynamically generate y-coordinates with decreasing values for each percentile
percentile_positions = [y_pos - (i * gap) for i in range(5)]


for (label, sd_value), y_pos in zip(percentiles.items(), percentile_positions):
    plt.axvline(sd_value, color='r', linestyle='--')
    plt.text(sd_value, y_pos, f"{sd_value:.4f}", color='red', ha='center')

# Adding the text box with percentile information
plt.text(
    max(sd_values) * 0.8,  # X position of the box
    1.5,  # Y position of the box (adjust if needed)
    percentile_info,  # Text content
    fontsize=10,
    verticalalignment='top',
    bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow")  # Box styling
)


# Show the plot
plt.show()





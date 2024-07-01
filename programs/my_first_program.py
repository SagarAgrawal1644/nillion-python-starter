from nada_dsl import *

def nada_main():
    # Create two parties
    company1 = Party(name="Company1")
    company2 = Party(name="Company2")

    # Inputs: Each company provides their employee data
    salaries_company1 = Input(name="salaries_company1", party=company1)
    years_experience_company1 = Input(name="years_experience_company1", party=company1)
    departments_company1 = Input(name="departments_company1", party=company1)
    genders_company1 = Input(name="genders_company1", party=company1)

    salaries_company2 = Input(name="salaries_company2", party=company2)
    years_experience_company2 = Input(name="years_experience_company2", party=company2)
    departments_company2 = Input(name="departments_company2", party=company2)
    genders_company2 = Input(name="genders_company2", party=company2)

    # Combine data from both companies
    combined_salaries = Concat(salaries_company1, salaries_company2)
    combined_years_experience = Concat(years_experience_company1, years_experience_company2)
    combined_departments = Concat(departments_company1, departments_company2)
    combined_genders = Concat(genders_company1, genders_company2)

    total_employees = Length(combined_salaries)

    # Calculate total and average salary
    total_salary = Sum(combined_salaries)
    average_salary = total_salary / total_employees

    # Calculate total and average years of experience
    total_years_experience = Sum(combined_years_experience)
    average_years_experience = total_years_experience / total_employees

    # Calculate median salary (approximate)
    sorted_salaries = Sort(combined_salaries)
    median_salary = sorted_salaries[total_employees // 2]

    # Calculate highest and lowest salary
    highest_salary = Max(combined_salaries)
    lowest_salary = Min(combined_salaries)

    # Calculate department-wise metrics
    department_experience_totals = {}
    department_salary_totals = {}
    department_employee_counts = {}

    for i in range(total_employees):
        dept = combined_departments[i]
        salary = combined_salaries[i]
        experience = combined_years_experience[i]
        if dept not in department_experience_totals:
            department_experience_totals[dept] = 0
            department_salary_totals[dept] = 0
            department_employee_counts[dept] = 0
        department_experience_totals[dept] += experience
        department_salary_totals[dept] += salary
        department_employee_counts[dept] += 1

    average_experience_per_department = {
        dept: department_experience_totals[dept] / department_employee_counts[dept]
        for dept in department_experience_totals
    }

    average_salary_per_department = {
        dept: department_salary_totals[dept] / department_employee_counts[dept]
        for dept in department_salary_totals
    }

    # Gender pay gap analysis
    male_salary_total = 0
    female_salary_total = 0
    male_count = 0
    female_count = 0

    for i in range(total_employees):
        gender = combined_genders[i]
        salary = combined_salaries[i]
        if gender == 0:  # Assuming 0 for male, 1 for female
            male_salary_total += salary
            male_count += 1
        elif gender == 1:
            female_salary_total += salary
            female_count += 1

    average_male_salary = male_salary_total / male_count if male_count > 0 else 0
    average_female_salary = female_salary_total / female_count if female_count > 0 else 0
    gender_pay_gap = average_male_salary - average_female_salary

    # Output metrics
    outputs = [
        Output(average_salary, "average_salary", company1),
        Output(average_salary, "average_salary", company2),
        Output(median_salary, "median_salary", company1),
        Output(median_salary, "median_salary", company2),
        Output(total_salary, "total_salary", company1),
        Output(total_salary, "total_salary", company2),
        Output(average_years_experience, "average_years_experience", company1),
        Output(average_years_experience, "average_years_experience", company2),
        Output(highest_salary, "highest_salary", company1),
        Output(highest_salary, "highest_salary", company2),
        Output(lowest_salary, "lowest_salary", company1),
        Output(lowest_salary, "lowest_salary", company2),
        Output(gender_pay_gap, "gender_pay_gap", company1),
        Output(gender_pay_gap, "gender_pay_gap", company2)
    ]

    for dept in average_experience_per_department:
        outputs.append(Output(average_experience_per_department[dept], f"average_experience_{dept}", company1))
        outputs.append(Output(average_experience_per_department[dept], f"average_experience_{dept}", company2))

    for dept in average_salary_per_department:
        outputs.append(Output(average_salary_per_department[dept], f"average_salary_{dept}", company1))
        outputs.append(Output(average_salary_per_department[dept], f"average_salary_{dept}", company2))

    return outputs

import csv
from typing import Dict, List, Optional, Tuple

class Student:
    student_details: Dict[int, 'Student'] = {}
    
    GRADE_POINTS = {
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'F': 0.0
    }

    def __init__(self, id: int, firstname: str, lastname: str, dept_id: int):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.dept_id = dept_id
        self.course_curriculum: Dict[int, 'Curriculum'] = {}
        self.courses_taken: Dict[str, List[Tuple[int, str]]] = {}
        self.total_credit_hour_taken: int = 0
        self.cgpa: float = 0.0

    def fullname(self) -> str:
        return f'{self.lastname} {self.firstname}'

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Student']:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        student = cls(
                            id=int(row['id']),
                            firstname=row['firstname'],
                            lastname=row['lastname'],
                            dept_id=int(row['dept_id'])
                        )
                        cls.student_details[student.id] = student
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.student_details

    def load_course_list(self) -> None:
        self.course_curriculum = {
            numeric_course_code: curriculum 
            for numeric_course_code, curriculum in Curriculum.Curriculum_details.items()
        }

    def add_course(self, semester: str, numeric_course_code: int, grade: str) -> None:
        try:
            if numeric_course_code not in self.course_curriculum:
                raise ValueError(f"Course {numeric_course_code} not found in curriculum")
            
            if grade.upper() not in self.GRADE_POINTS:
                raise ValueError(f"Invalid grade '{grade}'. Must be one of: {list(self.GRADE_POINTS.keys())}")
            
            if semester not in self.courses_taken:
                self.courses_taken[semester] = []
            
            for idx, (existing_code, _) in enumerate(self.courses_taken[semester]):
                if existing_code == numeric_course_code:
                    self.courses_taken[semester][idx] = (numeric_course_code, grade.upper())
                    break
            else:
                self.courses_taken[semester].append((numeric_course_code, grade.upper()))
            
            self.update_credit_hours()
            self.calculate_cgpa()
            
        except ValueError as e:
            print(f"Error adding course: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error adding course: {e}")
            raise

    def calculate_semester_gpa(self, semester: str) -> Optional[float]:
        if semester not in self.courses_taken or not self.courses_taken[semester]:
            return None

        total_quality_points = 0.0
        total_credits = 0

        for numeric_course_code, grade in self.courses_taken[semester]:
            if numeric_course_code not in self.course_curriculum:
                continue

            curriculum = self.course_curriculum[numeric_course_code]
            credit = curriculum.credit
            grade_point = self.GRADE_POINTS.get(grade.upper(), 0.0)

            total_quality_points += grade_point * credit
            total_credits += credit

        if total_credits == 0:
            return 0.0

        return round(total_quality_points / total_credits, 2)

    def calculate_cgpa(self) -> float:
        total_quality_points = 0.0
        total_credits = 0

        for semester in self.courses_taken:
            for numeric_course_code, grade in self.courses_taken[semester]:
                if numeric_course_code not in self.course_curriculum:
                    continue

                curriculum = self.course_curriculum[numeric_course_code]
                credit = curriculum.credit
                grade_point = self.GRADE_POINTS.get(grade.upper(), 0.0)

                total_quality_points += grade_point * credit
                total_credits += credit

        if total_credits == 0:
            return 0.0

        self.cgpa = round(total_quality_points / total_credits, 2)
        return self.cgpa

    def update_credit_hours(self) -> None:
        self.total_credit_hour_taken = sum(
            self.course_curriculum[course].credit
            for semester in self.courses_taken.values()
            for course, _ in semester
            if course in self.course_curriculum
        )


class Department:
    department_details: Dict[int, 'Department'] = {}

    def __init__(self, dept_id: int, dept_name: str):
        self.dept_id = dept_id
        self.dept_name = dept_name

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Department']:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        department = cls(
                            dept_id=int(row['dept_id']),
                            dept_name=row['dept_name']
                        )
                        cls.department_details[department.dept_id] = department
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.department_details


class Course:
    course_details: Dict[int, 'Course'] = {}

    def __init__(self, numeric_course_code: int, course_code: str, course_name: str):
        self.numeric_course_code = numeric_course_code
        self.course_code = course_code
        self.course_name = course_name

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Course']:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        course = cls(
                            numeric_course_code=int(row['numeric_course_code']),
                            course_code=row['course_code'],
                            course_name=row['course_name']
                        )
                        cls.course_details[course.numeric_course_code] = course
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.course_details


class Curriculum:
    Curriculum_details: Dict[int, 'Curriculum'] = {}

    def __init__(self, numeric_course_code: int, credit: int, theory: int, 
                 practical: int, ects: float, prerequisite: List[int]):
        self.numeric_course_code = numeric_course_code
        self.credit = credit
        self.theory = theory
        self.practical = practical
        self.ects = ects
        self.prerequisite = prerequisite

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Curriculum']:
        cls.Curriculum_details.clear()
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        numeric_course_code = int(row['numeric_course_code'])
                        if numeric_course_code not in Course.course_details:
                            raise ValueError(f"Course {numeric_course_code} not found")
                        
                        prerequisite = []
                        if row['prerequisite'].strip():
                            prerequisite = [int(code) for code in row['prerequisite'].split('|')]
                            for code in prerequisite:
                                if code not in Course.course_details:
                                    raise ValueError(f"Prerequisite {code} not found")

                        curriculum = cls(
                            numeric_course_code=numeric_course_code,
                            credit=int(row['credit']),
                            theory=int(row['theory']),
                            practical=int(row['practical']),
                            ects=float(row['ects']),
                            prerequisite=prerequisite
                        )
                        cls.Curriculum_details[numeric_course_code] = curriculum
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.Curriculum_details
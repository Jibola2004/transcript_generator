import csv

class Student:
    student_details = {}

    def __init__(self, id: int, firstname: str, lastname: str, dept_id: int):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.dept_id = dept_id

    def fullname(self):
        return f'{self.lastname} {self.firstname}'

    @classmethod
    def from_csv(cls, file_path):
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
                    except KeyError as e:
                        print(f"Missing expected column in row: {e}")
                    except ValueError as e:
                        print(f"Data format error: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return cls.student_details




class Department:
    department_details={}
    def __int__(self,dept_id:int,dept_name:str):
        self.dept_id=dept_id
        self.dept_name=dept_name

    @classmethod
    def from_csv(cls,file_path):
        try:
            with open(file_path,newline='',encoding='utf-8') as csvfile:
                reader= csv.DictReader(csvfile)
                for row in reader:
                    try:
                        department = cls(
                            dept_id=int(row['dept_id']),
                            dept_name=row['dept_name']
                        )
                        cls.department_details[department.dept_id]=department
                    except KeyError as e:
                        print(f"Missing expected column in row: {e}")
                    except ValueError as e:
                        print(f"Data format error: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return cls.department_details


class Course:
    course_details={}
    def __init__(self,numeric_course_code:int,course_code:str,course_name:str):
        self.numeric_course_code=numeric_course_code
        self.course_code=course_code
        self.course_name=course_name

    @classmethod
    def from_csv(cls,file_path):
        try:
            with open(file_path,newline='',encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        course = cls(
                            numeric_course_code=int(row['numeric_course_code']),
                            course_code=row['course_code'],
                            course_name=row['course_name']
                        )
                        cls.course_details[course.numeric_course_code]=course
                    except KeyError as e :
                        print(f'Missing expected column in row: {e}')
                    except ValueError as e:
                        print(f"Data format error: {e}")

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


        return cls.course_details




class Curriculum:
    Curriculum_details = {}

    def __init__(self, numeric_course_code: int, credit: int, theory: int, practical: int, ects: float, prerequisite: list[int]):
        self.numeric_course_code = numeric_course_code
        self.credit = credit
        self.theory = theory
        self.practical = practical
        self.ects = ects
        self.prerequisite = prerequisite

    @classmethod
    def from_csv(cls, file_path):
        cls.Curriculum_details.clear()

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    try:
                        numeric_course_code = int(row['numeric_course_code'])

                        # Raise error if course is not defined in Course
                        if numeric_course_code not in Course.course_details:
                            raise ValueError(f"Course {numeric_course_code} not found in Course list.")

                        credit = int(row['credit'])
                        theory = int(row['theory'])
                        practical = int(row['practical'])
                        ects = float(row['ects'])

                        # Handle prerequisites (| delimited)
                        prereq_field = row['prerequisite'].strip()
                        if prereq_field:
                            prerequisite = [int(code.strip()) for code in prereq_field.split('|')]

                            # Raise error if any prerequisite is not defined
                            for code in prerequisite:
                                if code not in Course.course_details:
                                    raise ValueError(f"Prerequisite course {code} for course {numeric_course_code} not found in Course list.")
                        else:
                            prerequisite = []

                        curriculum_obj = cls(numeric_course_code, credit, theory, practical, ects, prerequisite)
                        cls.Curriculum_details[numeric_course_code] = curriculum_obj

                    except KeyError as e:
                        raise KeyError(f"Missing expected column: {e}")
                    except ValueError as e:
                        raise ValueError(f"Data error in course {row.get('numeric_course_code')}: {e}")

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error while reading curriculum: {e}")

        return cls.Curriculum_details








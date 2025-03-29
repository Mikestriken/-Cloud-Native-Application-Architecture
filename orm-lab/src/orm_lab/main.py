# docker exec -it lab-postgres psql -U lab_user -d lab_database -c "SELECT * FROM students;"

from orm_lab.config import SessionLocal
from orm_lab.models import Student, Course
def create_student(name: str, age: int, course_name:str):
    db = SessionLocal()
    try:
        course_id = db.query(Course.id).filter(Course.name == course_name).first()[0]
        new_student = Student(name=name, age=age, course_id=course_id)
        db.add(new_student)
        db.commit()
        db.refresh(new_student) # refresh to get the generated ID
        print(f"Created new student: {new_student.id} - {new_student.name}, {new_student.age}, {new_student.course_id}")
    except Exception as e:
        db.rollback()
        print("Error creating student:", e)
    finally:
        db.close()
        
        
def get_students():
    db = SessionLocal()
    try:
        return db.query(Student).all()
    finally:
        db.close()

def update_student(student_id: int, new_age: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).one_or_none()
        if not student:
            print(f"Student with id {student_id} not found.")
            return
        student.age = new_age
        db.commit()
        db.refresh(student)
        print(f"Updated student {student.id}'s age to {student.age}")
    except Exception as e:
        db.rollback()
        print("Error updating student:", e)
    finally:
        db.close()
        
def delete_student(student_id: int):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).one_or_none()
        if not student:
            print(f"Student with id {student_id} not found.")
            return
        db.delete(student)
        db.commit()
        print(f"Deleted student with id {student_id}")
    except Exception as e:
        db.rollback()
        print("Error deleting student:", e)
    finally:
        db.close()
# ===================================================================================================
def create_course(name: str):
    db = SessionLocal()
    try:
        new_course = Course(name=name)
        db.add(new_course)
        db.commit()
        db.refresh(new_course) # refresh to get the generated ID
        print(f"Created new course: {new_course.id} - {new_course.name}")
    except Exception as e:
        db.rollback()
        print("Error creating course:", e)
    finally:
        db.close()
        
        
def get_courses():
    db = SessionLocal()
    try:
        return db.query(Course).all()
    finally:
        db.close()

def update_course(course_id: int, new_name: int):
    db = SessionLocal()
    try:
        course = db.query(Course).filter(course.id == course_id).one_or_none()
        if not course:
            print(f"course with id {course_id} not found.")
            return
        course.name = new_name
        db.commit()
        db.refresh(course)
        print(f"Updated course {course.id}'s name to {course.name}")
    except Exception as e:
        db.rollback()
        print("Error updating course:", e)
    finally:
        db.close()
        
def delete_course(course_id: int):
    db = SessionLocal()
    try:
        course = db.query(Course).filter(course.id == course_id).one_or_none()
        if not course:
            print(f"course with id {course_id} not found.")
            return
        db.delete(course)
        db.commit()
        print(f"Deleted course with id {course_id}")
    except Exception as e:
        db.rollback()
        print("Error deleting course:", e)
    finally:
        db.close()
    
if __name__ == "__main__":
    # 1. Create some students
    create_course("ENGR 1201")
    
    create_student("Alice", 22, "ENGR 1201")

    create_student("Bob", 25, "ENGR 1201")
    # 2. Read (get) all students
    students_list = get_students()
    print("Current students:")
    for s in students_list:
        print(f"ID: {s.id}, Name: {s.name}, Age: {s.age}, Course ID: {s.course_id}")
        
    # 3. Update the first student's age (if any student exists)
    if students_list:
        first_student_id = students_list[0].id
        update_student(first_student_id, 28)
    # 4. Delete the second student (if it exists)
    if len(students_list) > 1:
        second_student_id = students_list[1].id
        delete_student(second_student_id)
    # 5. Print final students to verify changes
    final_students_list = get_students()
    print("Students after updates:")
    for s in final_students_list:
        print(f"ID: {s.id}, Name: {s.name}, Age: {s.age}, Course ID: {s.course_id}")
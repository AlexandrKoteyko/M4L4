import os
import django
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management import call_command

# Ініціалізація Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from school_app.models import Subject, Teacher, SchoolClass, Student, Schedule, Grade

def add_subject():
    name = input("Назва предмету: ")
    description = input("Опис (не обов'язково): ")
    
    if Subject.objects.filter(name=name).exists():
        print("Предмет з такою назвою вже існує!")
        return
    
    Subject.objects.create(name=name, description=description)
    print("Предмет успішно додано!")

def edit_subject():
    list_subjects()
    try:
        subject_id = int(input("Введіть ID предмету для редагування: "))
        subject = Subject.objects.get(id=subject_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID предмету!")
        return
    
    new_name = input(f"Нова назва ({subject.name}): ") or subject.name
    new_desc = input(f"Новий опис ({subject.description}): ") or subject.description
    
    if new_name != subject.name and Subject.objects.filter(name=new_name).exists():
        print("Предмет з такою назвою вже існує!")
        return
    
    subject.name = new_name
    subject.description = new_desc
    subject.save()
    print("Предмет успішно оновлено!")

def delete_subject():
    list_subjects()
    try:
        subject_id = int(input("Введіть ID предмету для видалення: "))
        subject = Subject.objects.get(id=subject_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID предмету!")
        return
    
    subject.delete()
    print("Предмет успішно видалено!")

def add_teacher():
    first_name = input("Ім'я вчителя: ")
    last_name = input("Прізвище вчителя: ")
    
    list_subjects()
    try:
        subject_id = int(input("ID предмету: "))
        subject = Subject.objects.get(id=subject_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID предмету!")
        return
    
    Teacher.objects.create(
        first_name=first_name,
        last_name=last_name,
        subject=subject
    )
    print("Вчителя успішно додано!")

def add_class():
    name = input("Назва класу: ")
    year = input("Рік навчання: ")
    
    if SchoolClass.objects.filter(name=name).exists():
        print("Клас з такою назвою вже існує!")
        return
    
    try:
        year = int(year)
    except ValueError:
        print("Рік має бути числом!")
        return
    
    SchoolClass.objects.create(name=name, year=year)
    print("Клас успішно додано!")

def edit_class():
    list_classes()
    try:
        class_id = int(input("Введіть ID класу для редагування: "))
        school_class = SchoolClass.objects.get(id=class_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID класу!")
        return
    
    new_name = input(f"Нова назва ({school_class.name}): ") or school_class.name
    new_year = input(f"Новий рік ({school_class.year}): ") or school_class.year
    
    if new_name != school_class.name and SchoolClass.objects.filter(name=new_name).exists():
        print("Клас з такою назвою вже існує!")
        return
    
    try:
        new_year = int(new_year)
    except ValueError:
        print("Рік має бути числом!")
        return
    
    school_class.name = new_name
    school_class.year = new_year
    school_class.save()
    print("Клас успішно оновлено!")

def delete_class():
    list_classes()
    try:
        class_id = int(input("Введіть ID класу для видалення: "))
        school_class = SchoolClass.objects.get(id=class_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID класу!")
        return
    
    school_class.delete()
    print("Клас успішно видалено!")

def add_student():
    first_name = input("Ім'я учня: ")
    last_name = input("Прізвище учня: ")
    
    list_classes()
    try:
        class_id = int(input("ID класу: "))
        school_class = SchoolClass.objects.get(id=class_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID класу!")
        return
    
    Student.objects.create(
        first_name=first_name,
        last_name=last_name,
        school_class=school_class
    )
    print("Учня успішно додано!")

def add_schedule():
    print("День тижня: Mon, Tue, Wed, Thu, Fri")
    day = input("День: ")
    start_time = input("Час початку (ГГ:ХХ): ")
    
    list_subjects()
    try:
        subject_id = int(input("ID предмету: "))
        subject = Subject.objects.get(id=subject_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID предмету!")
        return
    
    list_classes()
    try:
        class_id = int(input("ID класу: "))
        school_class = SchoolClass.objects.get(id=class_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID класу!")
        return
    
    list_teachers()
    try:
        teacher_id = int(input("ID вчителя: "))
        teacher = Teacher.objects.get(id=teacher_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID вчителя!")
        return
    
    Schedule.objects.create(
        day=day,
        start_time=start_time,
        subject=subject,
        school_class=school_class,
        teacher=teacher
    )
    print("Заняття успішно додано до розкладу!")

def add_grade():
    list_students()
    try:
        student_id = int(input("ID учня: "))
        student = Student.objects.get(id=student_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID учня!")
        return
    
    list_subjects()
    try:
        subject_id = int(input("ID предмету: "))
        subject = Subject.objects.get(id=subject_id)
    except (ObjectDoesNotExist, ValueError):
        print("Невірний ID предмету!")
        return
    
    try:
        value = int(input("Оцінка (1-12): "))
        date = input("Дата (РРРР-ММ-ДД): ")
    except ValueError:
        print("Невірний формат даних!")
        return
    
    try:
        Grade.objects.create(
            student=student,
            subject=subject,
            value=value,
            date=date
        )
        print("Оцінку успішно додано!")
    except ValidationError as e:
        print(f"Помилка: {e}")

# Функції для відображення списків
def list_subjects():
    print("\nСписок предметів:")
    for s in Subject.objects.all():
        print(f"{s.id}: {s.name} - {s.description}")

def list_teachers():
    print("\nСписок вчителів:")
    for t in Teacher.objects.all():
        print(f"{t.id}: {t.last_name} {t.first_name} ({t.subject.name})")

def list_classes():
    print("\nСписок класів:")
    for c in SchoolClass.objects.all():
        print(f"{c.id}: {c.name} ({c.year} рік)")

def list_students():
    print("\nСписок учнів:")
    for s in Student.objects.all():
        print(f"{s.id}: {s.last_name} {s.first_name} - {s.school_class.name}")

def list_schedules():
    print("\nРозклад занять:")
    for s in Schedule.objects.all():
        print(f"{s.day} {s.start_time}: {s.subject.name} - {s.school_class.name} ({s.teacher})")

def list_grades():
    print("\nОцінки:")
    for g in Grade.objects.all():
        print(f"{g.date}: {g.student} - {g.subject.name} = {g.value}")

def main_menu():
    while True:
        print("\n===== Головне меню =====")
        print("1. Предмети")
        print("2. Вчителі")
        print("3. Класи")
        print("4. Учні")
        print("5. Розклад")
        print("6. Оцінки")
        print("7. Вийти")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            subject_menu()
        elif choice == '2':
            teacher_menu()
        elif choice == '3':
            class_menu()
        elif choice == '4':
            student_menu()
        elif choice == '5':
            schedule_menu()
        elif choice == '6':
            grade_menu()
        elif choice == '7':
            print("До побачення!")
            break
        else:
            print("Невірний вибір!")

def subject_menu():
    while True:
        print("\n--- Меню предметів ---")
        print("1. Додати предмет")
        print("2. Редагувати предмет")
        print("3. Видалити предмет")
        print("4. Список предметів")
        print("5. Повернутись")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            add_subject()
        elif choice == '2':
            edit_subject()
        elif choice == '3':
            delete_subject()
        elif choice == '4':
            list_subjects()
        elif choice == '5':
            break
        else:
            print("Невірний вибір!")

def teacher_menu():
    while True:
        print("\n--- Меню вчителів ---")
        print("1. Додати вчителя")
        print("2. Список вчителів")
        print("3. Повернутись")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            add_teacher()
        elif choice == '2':
            list_teachers()
        elif choice == '3':
            break
        else:
            print("Невірний вибір!")

def class_menu():
    while True:
        print("\n--- Меню класів ---")
        print("1. Додати клас")
        print("2. Редагувати клас")
        print("3. Видалити клас")
        print("4. Список класів")
        print("5. Повернутись")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            add_class()
        elif choice == '2':
            edit_class()
        elif choice == '3':
            delete_class()
        elif choice == '4':
            list_classes()
        elif choice == '5':
            break
        else:
            print("Невірний вибір!")

def student_menu():
    while True:
        print("\n--- Меню учнів ---")
        print("1. Додати учня")
        print("2. Список учнів")
        print("3. Повернутись")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            list_students()
        elif choice == '3':
            break
        else:
            print("Невірний вибір!")

def schedule_menu():
    while True:
        print("\n--- Меню розкладу ---")
        print("1. Додати заняття")
        print("2. Переглянути розклад")
        print("3. Повернутись")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            add_schedule()
        elif choice == '2':
            list_schedules()
        elif choice == '3':
            break
        else:
            print("Невірний вибір!")

def grade_menu():
    while True:
        print("\n--- Меню оцінок ---")
        print("1. Додати оцінку")
        print("2. Переглянути оцінки")
        print("3. Повернутись")
        
        choice = input("Ваш вибір: ")
        
        if choice == '1':
            add_grade()
        elif choice == '2':
            list_grades()
        elif choice == '3':
            break
        else:
            print("Невірний вибір!")

if __name__ == "__main__":
    # Створення БД при першому запуску
    if not os.path.exists('db.sqlite3'):
        call_command('makemigrations')
        call_command('migrate')
        print("Базу даних створено!")
    
    main_menu()
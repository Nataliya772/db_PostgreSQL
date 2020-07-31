import binary as binary
import psycopg2 as pg

with pg.connect(database='test', user='postgres', password='tvoug13777T', host='localhost', port='5432') as conn:
    cur = conn.cursor()

def create_db():
    cur.execute('''
        create table if not exists Student(
        id serial primary key, name varchar(100) not null, gpa numeric(10,2) null, birth timestamp with time zone
        );
        ''')

    cur.execute('''
        create table if not exists Course(
        id serial primary key, name varchar(100) not null);
        ''')

    cur.execute('''
        create table if not exists student_course(
        id serial primary key,
        student_id integer references Student(id),
        course_id integer references Course(id));
        ''')
    pass

def get_list_student():
    stud_list = []
    name = input('Укажите ФИО студента: ')
    gpa = input('Укажите средний балл студента, если он есть: ')
    birth = input('Укажите дату рождения студента: ')
    stud_list.append(name)
    stud_list.append(gpa)
    stud_list.append(birth)
    return stud_list

def add_student_from_list():
    stud_list = get_list_student()
    if stud_list[1] == '':
        cur.execute('''
            insert into Student(name, birth) values (%s, %s);
            ''', (stud_list[0], stud_list[2]))
    else:
        cur.execute('''
            insert into Student(name, gpa, birth) values (%s, %s, %s);
            ''', (stud_list[0], float(stud_list[1]), stud_list[2]))
    pass

def add_students(course_id, students):
    cur.execute('''
        select max(id) from Student;
        ''')
    new_id = cur.fetchall()
    cur.execute('''
            insert into student_course(student_id, course_id) values (%s, %s)
            ''', (new_id[0][0], course_id))
    pass

def get_students(course_id):
    cur.execute('''
        select s.id, s.name, c.id, c.name from student_course sc
        join Student s on s.id = sc.student_id
        join Course c on c.id = sc.course_id
        where c.id = %s
        ''', (course_id,))
    for sc in cur.fetchall():
        print(sc)
    pass

def get_student(student_id):
    cur.execute('select * from Student where id = %s', (student_id,))
    for s in map(lambda x: (x[0], x[1], float(x[2]) if x[2] else None, x[3].strftime('%d.%m.%Y')), cur.fetchall()):
        print(s)
    pass

def add_course(name):
    cur.execute('''
    insert into Course(name) values (%s);
    ''', (name,))
    pass

if __name__ == '__main__':
    create_db()
    get_students(1)
    get_student(12)
    get_student(13)
    add_students(3, add_student_from_list())
    get_students(1)


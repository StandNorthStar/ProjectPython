# coding: utf-8

import peewee
from peewee import Column, CharField, IntegerField, PrimaryKeyField

dbname = 'test'
parms = dict(
    dbhost='192.168.10.66',
    dbuser='root',
    dbpassword='',
)

db = peewee.MySQLDatabase(dbname, parms)

class My_student(peewee.Model):

    name = CharField()
    age = IntegerField()
    email = CharField()

    class Meta:
        database = db
        table_name = 'student_my'

if __name__ == "__main__":
    
    db.connect()
    
    if not db.table_exists(My_student._meta.table_name):
        My_student.create_table()
    
    t1 = My_student.create(name='hely', age=28, email='test@test.com')
    t1.save()

    db.close()

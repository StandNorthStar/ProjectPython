# coding: utf-8

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):

    __tablename__ = "user"

    id = Column(String(10), primary_key=True)
    name = Column(String(20))


if __name__ == "__main__":
    mysqlconn = 'mysql+mysqlconnector://root@192.168.10.66:3306/test'
    # 创建数据库连接引擎
    engine = create_engine(mysqlconn, encoding="utf-8", echo=True)

    # 创建数据表
    Base.metadata.create_all(engine)

    # 创建一个连接session  (session用于插入/查询)
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    '''
    session.query().all()   查询所有
    session.query().limit(10).all()   查询前十条 1-10
    session.query().limit(20).offset(10).all()  从前20条开始，查询十条数据 20-30
    session.query().slice(start,end).all()  切片只针对列表有用      
    '''

    # 插入字段
    # newuser = User(id='16', name='hely1')
    # session.add(newuser)

    # 查询某一条数据
    # select_user = session.query(User).filter(User.id=='15').one()

    # 查询多条数据
    select_user = session.query(User).filter(User.name.like('%hely%'))
    print select_user               # 其实是sql语句(其实是一个对象)
    for result in select_user:      # 通过遍历查询到的数据对象获取所有数据
        print result.id


    session.commit()
    session.close()


# sqlalchemy.orm.relationship 映射两张表的关系(可以理解为Django中的主外键对应关系，通过此字段获取另一张表中数据)



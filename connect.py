import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

Base = declarative_base()

engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)

class Role(Base):
	__tablename__ = 'Role'
	id = Column(Integer, primary_key=True, nullable=False)
	role = Column(String(45), nullable=False)

class Users(Base):
	__tablename__ = 'Users'
	id = Column(Integer, primary_key=True, nullable=False)
	firstname = Column(String(45), nullable=False)
	lastname = Column(String(45), nullable=False)
	surename = Column(String(45), nullable=True)
	phone = Column(String(45), nullable=False)
	email = Column(String(45), nullable=False)
	login = Column(String(45), nullable=False)
	password = Column(String(45), nullable=False)
	role = Column(Integer, ForeignKey(Role.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

class Status(Base):
	__tablename__ = 'Status'
	id = Column(Integer, primary_key=True, nullable=False)
	status = Column(String(45), nullable=False)

class Orders(Base):
	__tablename__ = 'Orders'
	id = Column(Integer, primary_key=True, nullable=False)
	id_user = Column(Integer, ForeignKey(Users.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
	auto_number = Column(String(45))
	violation_description = Column(Text, nullable=False)
	status = Column(Integer, ForeignKey(Status.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


try:
	Base.metadata.create_all(engine)
	session = sessionmaker(bind=engine)
	s = session()
	print(session)
except:
	print('Отсутствует подключение')

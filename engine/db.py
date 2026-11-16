from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

# Config
engine = create_engine('postgresql://user:pass@localhost/dbname')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

# Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    wallet_address = Column(String)
    verification_status = Column(String)
    balance_pounds = Column(Float)
    tasks = relationship('Task', backref='user')
    earnings = relationship('Earning', backref='user')
    payments = relationship('Payment', backref='user')

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    ai_worker_id = Column(Integer, ForeignKey('users.id'))
    task_type = Column(String)
    status = Column(String)
    reward_pounds = Column(Float)

class Earning(Base):
    __tablename__ = 'earnings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount_pounds = Column(Float)
    date = Column(Date)

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount_pounds = Column(Float)
    crypto_amount = Column(Float)
    network = Column(String)
    status = Column(String)

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()
    return jsonify([{'id': u.id, 'wallet': u.wallet_address} for u in users])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(ai_worker_id=data['user_id'], task_type=data['type'], reward_pounds=data['reward'])
    session.add(task)
    session.commit()
    return jsonify({'id': task.id}), 201

if __name__ == '__main__':
    app.run(debug=True)

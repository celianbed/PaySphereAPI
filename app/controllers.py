from app.models import Test
from app import db

#def get_all_users():l
    #return User.query.all()

def add_user(name):
    #user = User(name=name)
    #db.session.add(user)
    #db.session.commit()
    #return user
    pass

def get_all_nom():
    rq = Test.query.all()
    print(rq)
    return rq
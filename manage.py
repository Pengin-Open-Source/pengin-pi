from app import create_app
from app import db
from app.db.models import Thread, ThreadRoles, User, UserRoles, ForumPost, ForumComment, Home, About, Order, ShippingAddress, Customer, Company, CompanyMembers, Role, Contracts, Event, BlogPost
from datetime import datetime
from app.util.uuid import id
from werkzeug.security import generate_password_hash


def out(string):
        try:
            output = input(string)
            if output == 'Q':
                quit()
            return output
        except:
            out(string)

def password():
    return generate_password_hash(out('Q to quit | Input password: '), method='sha256')


def create_all():
    app = create_app()
    
    with app.app_context():
        db.create_all()

        
def create(model, **kwargs):
    new = model(kwargs)
    app = create_app()
    
    with app.app_context():
        db.session.add(new)
        db.session.commit()

def getone(model, **kwargs):
    app = create_app()
    with app.app_context():
        return model.query.filter_by(kwargs).first()
        
def update(model, search:dict, change:dict):
    lookup = getone(model, **search)
    #TODO: apply changes to lookup 
    #db.session.commit()
    
def build():
    app = create_app()
    with app.app_context():
        roles = ({'id':id(),'name':'admin'},{'id':id(),'name':'user'},{'id':id(),'name':'sales'},{'id':id(),'name':'marketing'},{'id':id(),'name':'support'})
        threads = ({'name':'General','id':id()},{'name':'Sales','id':id()},{'name':'Support','id':id()},{'name':'Marketing','id':id()})
        threadroles = ({'id':id(),'thread_id':threads[0]['id'],'role_id':roles[1]['id']},{'id':id(),'thread_id':threads[1]['id'],'role_id':roles[2]['id']},{'id':id(),'thread_id':threads[2]['id'],'role_id':roles[4]['id']},{'id':id(),'thread_id':threads[3]['id'],'role_id':roles[3]['id']})
        users = ({'id':id(),'email':'bob@bob.com','password':password,'name':'Bobby Bob', 'validated':True, 'validation_date':datetime.utcnow(), 'validation_id':id()},)
        userroles = ({'id':id(),'user_id':users[0]['id'],'role_id':[i['id'] for i in roles if i['name'] == 'admin'][0]},
                     {'id':id(),'user_id':users[0]['id'],'role_id':[i['id'] for i in roles if i['name'] == 'user'][0]},
                     {'id':id(),'user_id':users[0]['id'],'role_id':[i['id'] for i in roles if i['name'] == 'sales'][0]},
                     {'id':id(),'user_id':users[0]['id'],'role_id':[i['id'] for i in roles if i['name'] == 'marketing'][0]},
                     {'id':id(),'user_id':users[0]['id'],'role_id':[i['id'] for i in roles if i['name'] == 'support'][0]})
        for i in roles:
            db.session.add(Role(id=i['id'],name=i['name'])) 
        for i in threads:
            db.session.add(Thread(id=i['id'], name=i['name']))
        for i in threadroles:
            db.session.add(ThreadRoles(id=i['id'], thread_id=i['thread_id'], role_id=i['role_id']))
        for i in users:
            db.session.add(User(id=i['id'],email=i['email'],password=i['password'],name=i['name'],validated=i['validated'],validation_date=i['validation_date'],validation_id=i['validation_id']))
        for i in userroles:
            db.session.add(UserRoles(user_id=i['user_id'],role_id=i['role_id']))
        db.session.commit()
        
    def create_admin():
        email = out('Q for quit | input email: ')
        name = out('Q for quit | input name: ')
        password = password()
        user = ({'id':id(),'email':email,'password':password,'name':name, 'validated':True, 'validation_date':datetime.utcnow(), 'validation_id':id()},)
        app = create_app()
    
        with app.app_context():
            for i in user:
                db.session.add(User(id=i['id'],email=i['email'],password=i['password'],name=i['name'],validated=i['validated'],validation_date=i['validation_date'],validation_id=i['validation_id']))
            db.session.commit()
            user_id = User.query.filter_by(email=email).first().id
            role_id = Role.query.filter_by(name="admin").first().id
            db.session.add(UserRoles(user_id=user_id,role_id=role_id))
            role_id = Role.query.filter_by(name="user").first().id
            db.session.add(UserRoles(user_id=user_id,role_id=role_id))
            db.session.commit()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        pass
    
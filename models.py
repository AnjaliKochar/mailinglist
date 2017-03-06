from app import db
class BlogPost(db.Model):
    __tablenmae__="users"
    id=db.Column(db.TEXT,primary_key=True)
    user_name=db.column(db.TEXT,nullable=False)
    email = db.column(db.TEXT, nullable=False)
    phoneno = db.column(db.TEXT, nullable=False)
    password = db.column(db.TEXT, nullable=False)
    address = db.column(db.TEXT, nullable=False)

    def __init__(self,user_name,email,phoneno,password,address):
        self.user_name=user_name
        self.email=email
        self.phoneno=phoneno
        self.password=password
        self.address=address

    def __repr__(self):
        return '<user_name{}'.format(self.user_name)
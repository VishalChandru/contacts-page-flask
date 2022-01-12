from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'

db = SQLAlchemy(app)

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    company = db.Column(db.String(100))
    phno = db.Column(db.String(100))
    email = db.Column(db.String(100))
    fbook = db.Column(db.String(100))
    insta = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
    linked = db.Column(db.String(100))

    def __init__(self, fname, lname, company, phno, email, fbook, insta, twitter, linked):
        self.fname = fname
        self.lname = lname
        self.company = company
        self.phno = phno
        self.email = email
        self.fbook = fbook
        self.insta = insta
        self.twitter = twitter
        self.linked = linked

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST":
        contact_fname = request.form.get('fname')
        contact_lname = request.form.get('lname')
        contact_company = request.form.get('company')
        contact_phone = request.form.get('phone')
        contact_email = request.form.get('email')
        contact_fbook = request.form.get('fbook') or None
        contact_twitter = request.form.get('twitter') or None
        contact_insta = request.form.get('insta') or None
        contact_linked = request.form.get('linked') or None

        new_contact = Contacts(contact_fname,contact_lname,contact_company,contact_phone,contact_email,contact_fbook,contact_insta,contact_twitter,contact_linked)

        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error connecting to data base"
    else:
        contacts = Contacts.query.order_by(Contacts.id).all()
        return render_template('index.html', contacts=contacts)

@app.route('/delete/<int:id>')
def delete(id):
    delete_contact = Contacts.query.get_or_404(id)

    try:
        db.session.delete(delete_contact)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the contact'

@app.route('/update/<int:id>', methods = ["POST","GET"])
def update(id):
    contact = Contacts.query.get_or_404(id)

    if request.method == "POST":
        contact.fname = request.form.get('fname')
        contact.lname = request.form.get('lname')
        contact.company = request.form.get('company')
        contact.phno = request.form.get('phone')
        contact.email = request.form.get('email')
        contact.fbook = request.form.get('fbook')
        contact.twitter = request.form.get('twitter')
        contact.insta = request.form.get('insta')
        contact.linked = request.form.get('linked')
    
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem connecting to the database'

@app.route('/search', methods=["POST","GET"])
def search():
    find = request.form.get('searchname')
    contacts = Contacts.query.filter(Contacts.fname.like(find+'%')).all()
    return render_template('index.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)








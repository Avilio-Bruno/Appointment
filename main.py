from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fioDoctor = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)
    fioPatient = db.Column(db.String(100), nullable=False)
    text1 = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Schedule %r>' % self.id


class Doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fioDoctor = db.Column(db.String(50), nullable=False)
    specialization = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Doctors %r>' % self.id


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fioPatient = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Patients %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/patients', methods=['POST', 'GET'])  #Создаем декоратор пациентов
def patients():
    addPatient = Patients.query.order_by(Patients.id).all()
    return render_template("patients.html", addPatient=addPatient)


@app.route('/deletePatient', methods=['POST'])
def deletePatient():
    patient_id = request.form['patient_id']
    patient = Patients.query.get(patient_id)
    try:
        db.session.delete(patient)
        db.session.commit()
        return redirect('/patients')
    except:
        return "При удалении пациента произошла ошибка..."


@app.route('/doctors', methods=['POST', 'GET'])  #Создаем декоратор врачей
def doctors():
    addDoctor = Doctors.query.order_by(Doctors.id).all()
    return render_template("doctors.html", addDoctor=addDoctor)


@app.route('/delete_doctor', methods=['POST'])
def delete_doctor():
    doctor_id = request.form['doctor_id']
    doctor = Doctors.query.get(doctor_id)
    try:
        db.session.delete(doctor)
        db.session.commit()
        return redirect('/doctors')
    except:
        return "При удалении врача произошла ошибка..."


@app.route('/')  #Создаем декоратор главной страницы
def index():
    schedule = Schedule.query.order_by(Schedule.date.desc()).all()
    return render_template("index.html", schedule=schedule)


@app.route('/index/<int:id>')  #Создаем декоратор главной страницы
def sch(id):
    sch = Schedule.query.get(id)
    return render_template("schedule_detail.html", sch=sch)


@app.route('/about', methods=['POST', 'GET'])  #Создаем декоратор формы
def about():
    doctors = Doctors.query.all()
    patients = Patients.query.all()
    if request.method == "POST":
        fioPatient = request.form['fioPatient']
        fioDoctor = request.form['fioDoctor']
        text1 = request.form['text1']

        schedule = Schedule(fioPatient=fioPatient, fioDoctor=fioDoctor, text1=text1)


        try:
            db.session.add(schedule)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка при создании записи!"
    else:
        return render_template("about.html", doctors=doctors, patients=patients)


@app.route('/index/<int:id>/upd', methods=['POST', 'GET'])  #Создаем декоратор формы
def sch_update(id):
    sch = Schedule.query.get(id)
    doctors = Doctors.query.all()
    patients = Patients.query.all()
    if request.method == "POST":
        sch.fioDoctor = request.form['fioDoctor']
        sch.fioPatient = request.form['fioPatient']
        sch.text1 = request.form['text1']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка при изменении записи"
    else:
        return render_template("schedule_update.html", sch=sch, doctors=doctors, patients=patients)


@app.route('/index/<int:id>/delete')  # Создаем декоратор главной страницы
def sch_delete(id):
    sch = Schedule.query.get_or_404(id)
    try:
        db.session.delete(sch)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении записи произошла ошибка..."


@app.route('/addDoctor', methods=['POST', 'GET'])  # Создаем декоратор формы
def addDoctor():
    if request.method == "POST":
        fioDoctor = request.form['fioDoctor']
        specialization = request.form['specialization']
        doctors = Doctors(fioDoctor=fioDoctor, specialization=specialization)

        try:
            db.session.add(doctors)
            db.session.commit()
            return redirect('/doctors')
        except:
            return "Ошибка при создании записи!"
    else:
        return render_template("addDoctor.html")


@app.route('/addPatient', methods=['POST', 'GET'])  # Создаем декоратор формы
def addPatient():
    if request.method == "POST":
        fioPatient = request.form['fioPatient']
        patient = Patients(fioPatient=fioPatient)

        try:
            db.session.add(patient)
            db.session.commit()
            return redirect('/patients')
        except:
            return "Ошибка при создании записи!"
    else:
        return render_template("addPatient.html")



if __name__ == "__main__":
    app.run(debug=True)


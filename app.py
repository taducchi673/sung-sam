from flask import send_file, Flask, render_template, request, flash, redirect
from sqlalchemy import create_engine, MetaData, Table, insert, func, Text
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import insert, delete,update, Column, String, Sequence, Integer
from wtforms import IntegerField, RadioField, SubmitField, Form, StringField
import seaborn as sns
from flask_wtf import Form
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'

engine = create_engine('sqlite:///response.db')
connection = engine.connect()
metadata = MetaData()
responses = Table('responses', metadata, 
    Column('name', Text),
    Column('gender', Text),
    Column('age', Integer),
    Column('phone', Text),
    Column('email', Text),
    Column('ques1', Text),
    Column('ques2', Text),
    Column('ques3', Text),
)

metadata.create_all(engine)
df = pd.read_sql_table('responses', connection)

@app.route('/plot_gender')
def plot_gender():
    fig1, ax1 = plt.subplots(figsize=(6, 6))
    ax1 = sns.set_style(style='darkgrid')
    ax1.set_title("Phân tích giới tính")
    ax1.set(xlabel="New X Label",ylabel="New Y Label")
    sns.countplot(data= df, x = df['gender'])
    canvas = FigureCanvas(fig1)
    img1=io.BytesIO()
    fig1.savefig(img1)
    img1.seek(0)
    return send_file(img1, mimetype='img/png')
@app.route('/plot_age')    
def plot_age():
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2 = sns.set_style(style='darkgrid')
    sns.countplot(data= df, x = df['age'])
    fig2.suptitle('Phan tich độ tuổi')
    canvas = FigureCanvas(fig2)
    img2=io.BytesIO()
    fig2.savefig(img2)
    img2.seek(0)
    return send_file(img2, mimetype='img/png')
@app.route('/plot_ques1')
def plot_ques1():
    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3 = sns.set_style(style='darkgrid')
    fig3.suptitle("Phân tích câu hỏi 1")
    sns.countplot(data= df, x = df['ques1'])
    canvas = FigureCanvas(fig3)
    img3=io.BytesIO()
    fig3.savefig(img3)
    img3.seek(0)
    return send_file(img3, mimetype='img/png')

@app.route('/plot_ques2')
def plot_ques2():
    fig4, ax4 = plt.subplots(figsize=(6, 6))
    ax4= sns.set_style(style='darkgrid')
    fig4.suptitle("Phân tích câu hỏi 2")
    sns.countplot(data= df, x = df['ques2'])
    canvas = FigureCanvas(fig4)
    img4=io.BytesIO()
    fig4.savefig(img4)
    img4.seek(0)
    return send_file(img4, mimetype='img/png')

@app.route('/plot_ques3')
def plot_ques3():
    fig5, ax5= plt.subplots(figsize=(6, 6))
    ax5= sns.set_style(style='darkgrid')
    fig5.suptitle("Phân tích câu hỏi 3")
    sns.countplot(data= df, x = df['ques3'])
    canvas = FigureCanvas(fig5)
    img5=io.BytesIO()
    fig5.savefig(img5)
    img5.seek(0)
    return send_file(img5, mimetype='img/png')


class ResponseForm(Form):
    name = StringField(label = 'Tên của bạn')
    gender = RadioField(label='Giới tính', choices = ['Male', 'Female'])
    age = IntegerField(label ='Tuổi')
    phone = StringField(label='Số điện thoại')
    email = StringField(label ='Email')
    ques1 = RadioField(label ='Bạn đánh giá thế nào về thiết kế của Galaxy S22?', choices = ['Tuyệt đẹp', 'Đẹp', 'Bình thường', 'Xấu'])
    ques2 = RadioField(label ='Bạn thích màu sắc nào trên Galaxy S22?', choices = ['Đen', 'Trắng', 'Xanh','Tím'])
    ques3 = RadioField(label ='Nhận xét về mức giá của sản phẩm?', choices = ['Quá đắt', 'Đắt', 'Hợp túi tiền', 'Rẻ'])
    submit = SubmitField(label ='Submit')



@app.route("/", methods=['GET', 'POST'])
def form():
    form = ResponseForm()
    if request.method == "POST":
        name_form  = request.form['name']
        gender_form = request.form['gender']
        age_form = request.form['age']
        phone_form = request.form['phone']
        email_form = request.form['email']
        ques1_form = request.form['ques1']
        ques2_form = request.form['ques2']
        ques3_form = request.form['ques3']
        print('Commited')
        engine = create_engine('sqlite:///response.db')
        connection = engine.connect()   
        stmt  = insert(responses).values(name = name_form, age = age_form, gender = gender_form, phone = phone_form, email = email_form, ques1 = ques1_form, ques2 = ques2_form, ques3 =ques3_form)
        connection.execute(stmt)
        print('Commited')
    return render_template("form.html", form = form)



select_all = 'SELECT * FROM responses'
table_cmd = connection.execute(select_all)
table = table_cmd.fetchall()

@app.route("/display_forms")
def display():
    return render_template("display_response.html", table=table, df = df)

if __name__ == '__main__':
    app.run(debug = True)
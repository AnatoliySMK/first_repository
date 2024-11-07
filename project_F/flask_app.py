from flask import *
import sqlite3
import datetime as dt




app = Flask(__name__)

app.config['SECRET_KEY'] = '12343212'

def getConnection():
    conn = sqlite3.connect('forum_data_base.db')
    conn.row_factory = sqlite3.Row #для того, щоб можна було звертатись до полів за іменами
    return conn


#Створення сторінки профіль
@app.route('/')
def profile():    #Назва функції в вказуванні шляху має бути унікальна
    login = session.get('login') #Інфа про людину яка зайшла на сайт
    register_data = session.get('UTC_regdata')
    return render_template('profile.html', Login = login , Reg_data = register_data ) #render_template - відображення html шаблону



#Сторінка для логіну
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        global user_login
        login = request.form['login']
        alpha_user_login = login
        password = request.form['password']
        conn = getConnection()
        user = conn.execute('SELECT * FROM Register_user_data WHERE login = ? AND password = ?',(login,password)).fetchone()
        conn.close()
        if user:
            session['login'] = user['login']
            user_login = alpha_user_login
            session['UTC_regdata'] = user['UTC_regdata']
            return redirect(url_for('profile'))
        else:
            flash('НЕВІРНИЙ ЛОГІН АБО ПАРОЛЬ')
            return redirect(url_for('login'))
        
    
    return render_template('login.html')#відображення html шаблону







#Сторінка реєстрації
@app.route('/signup', methods = ['GET','POST'] )
def signup():       #Функція для входу (Реєстрація)
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        confimPassword = request.form['confirm_password']
        if password != confimPassword:
            flash("Паролі не співпадають!")
            return redirect(url_for('signup')) #Переадрисація на функцію
        conn = getConnection()
        user = conn.execute('SELECT * FROM Register_user_data WHERE login = ?', (login,)).fetchone() #fetchone() - переводить рядок елементів данних в кортеж
        if user:
            flash('Логін вже зайнятий :3')
            conn.close()
            return redirect(url_for('signup'))
        register_data = dt.datetime.utcnow()
        UTC_reg_data = register_data.strftime("%Y-%m-%d %H:%M:%S")
        conn.execute('INSERT INTO Register_user_data (login, password, UTC_regdata) VALUES (?, ?, ?)', (login, password,UTC_reg_data))
        conn.commit() #Зберігаємо базу данних
        conn.close()
        flash("Реєстрація successful. Welcome") #Виведення на екрані з верху
        return redirect(url_for('login'))
    return render_template('register.html')






@app.route('/main_f', methods = ['GET','POST'])
def main_f():
    
    
    return render_template('main_f.html')











#Sport Topic
@app.route('/topic_sport', methods=['GET', 'POST'])
def topic_sport():

    conn = getConnection()
    # Об'єднаний запит для отримання всіх даних
    query = """
        SELECT message, message_id, message_time, user_login
        FROM sport_topic_bd
    """
    result = conn.execute(query).fetchall()

    # Створюємо список словників для зберігання даних
    messages = []
    for row in result:
        messages.append({
            'message': row[0],
            'message_id': row[1],
            'message_time': row[2],
            'user_login': row[3]
        })
    conn.commit() 
    conn.close()
    
    return render_template('topic_sport.html', Messages = messages)


#Message to sport db
@app.route('/sended_message_to_sport', methods = ['POST'])
def sended_message_to_sport():
    if request.method == 'POST':
        message = request.form['message_input']
        try:
            user_sended_message = session['login']
        except:
            user_sended_message = request.remote_addr
        message_sended_time = dt.datetime.utcnow()
        UTC_message_sended_time = message_sended_time.strftime("%Y-%m-%d %H:%M:%S")
        conn = getConnection()
        conn.execute('INSERT INTO sport_topic_bd (user_login, message, message_time) VALUES (?, ?, ?)', (user_sended_message, message, UTC_message_sended_time))
        conn.commit() #Зберігаємо базу данних
        conn.close()    
        return redirect(url_for('topic_sport'))




#Games Topic
@app.route('/topic_games' , methods = ['GET','POST'])
def topic_games():
    
    conn = getConnection()
    # Об'єднаний запит для отримання всіх даних
    query = """
        SELECT message, message_id, message_time, user_login
        FROM game_topic_bd
    """
    result = conn.execute(query).fetchall()

    # Створюємо список словників для зберігання даних
    messages = []
    for row in result:
        messages.append({
            'message': row[0],
            'message_id': row[1],
            'message_time': row[2],
            'user_login': row[3]
        })
    conn.commit() 
    conn.close()
    
    return render_template('topic_games.html', Messages = messages)


#Message to game db
@app.route('/sended_message_to_games', methods = ['POST'])
def sended_message_to_games():
    if request.method == 'POST':
        message = request.form['message_input']
        try:
            user_sended_message = session['login']
        except:
            user_sended_message = request.remote_addr
        message_sended_time = dt.datetime.utcnow()
        UTC_message_sended_time = message_sended_time.strftime("%Y-%m-%d %H:%M:%S")
        conn = getConnection()
        conn.execute('INSERT INTO game_topic_bd (user_login, message, message_time) VALUES (?, ?, ?)', (user_sended_message, message, UTC_message_sended_time))
        conn.commit() #Зберігаємо базу данних
        conn.close()    
        return redirect(url_for('topic_games'))






#FFIP ubrades Topic
@app.route('/topic_upgrade_FFIP' , methods = ['GET','POST'])
def topic_upgrade_FFIP():
    
    conn = getConnection()
    # Об'єднаний запит для отримання всіх даних
    query = """
        SELECT message, message_id, message_time, user_login
        FROM FFIP_upgrades_topic_bd
    """
    result = conn.execute(query).fetchall()

    # Створюємо список словників для зберігання даних
    messages = []
    for row in result:
        messages.append({
            'message': row[0],
            'message_id': row[1],
            'message_time': row[2],
            'user_login': row[3]
        })
    conn.commit() 
    conn.close()
    
    return render_template('topic_upgrade_FFIP.html', Messages = messages)


#Message to FFIP ubrades db
@app.route('/sended_message_to_upgrade_FFIP', methods = ['POST'])
def sended_message_to_upgrade_FFIP():
    if request.method == 'POST':
        message = request.form['message_input']
        try:
            user_sended_message = session['login']
        except:
            user_sended_message = request.remote_addr
        message_sended_time = dt.datetime.utcnow()
        UTC_message_sended_time = message_sended_time.strftime("%Y-%m-%d %H:%M:%S")
        conn = getConnection()
        conn.execute('INSERT INTO FFIP_upgrades_topic_bd (user_login, message, message_time) VALUES (?, ?, ?)', (user_sended_message, message, UTC_message_sended_time))
        conn.commit() #Зберігаємо базу данних
        conn.close()    
        return redirect(url_for('topic_upgrade_FFIP'))













#Створення логіки виходу з сайту
@app.route('/logout')
def logout():
    session.pop('login', None) #pop() - видаляє данні про користувача з сесіїі
    return redirect(url_for('login'))    


    


#Відстежування анонімного користувача
@app.route('/register_anonim_ip', methods=['POST'])
def red__anonim_user_IP():
    register_data = dt.datetime.utcnow()
    anonim_user_ip = request.remote_addr
    last_anonim_join = register_data.strftime("%Y-%m-%d %H:%M:%S")
    conn = getConnection()
    conn.execute('INSERT INTO anonim_users_IP (ip_adress , time) VALUES (?,?)',(anonim_user_ip,last_anonim_join))
    conn.commit() 
    conn.close()
    return anonim_user_ip 






#Відстежування залогіненог користувача
@app.route('/register_ip', methods=['POST'])
def red_user_IP():
    register_data = dt.datetime.utcnow()
    user_ip = request.remote_addr
    last_user_join = register_data.strftime("%Y-%m-%d %H:%M:%S")
    user_login2 = session['login']
    conn = getConnection()
    try:
        conn.execute('INSERT INTO logined_user (login, user_ip , UTC_data_time) VALUES (?,?,?)',(user_login,user_ip,last_user_join))
    except: 
        conn.execute('INSERT INTO logined_user (login, user_ip , UTC_data_time) VALUES (?,?,?)',(user_login2,user_ip,last_user_join))
    conn.commit() 
    conn.close()
    return user_ip 






if __name__ == "__main__":
    app.run(debug=True)



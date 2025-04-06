from flask import *
import psycopg2
import datetime as dt
import psycopg2.extras



app = Flask(__name__)

app.config['SECRET_KEY'] = '12343212'

def make_connection():
    return psycopg2.connect(
        host = "127.0.0.1",
        user = "postgres",
        password = "88005553535",
        dbname = "forum_database",
        port = 5432)




#Створення сторінки профіль
@app.route('/')
def profile():    #Назва функції в вказуванні шляху має бути унікальна
    login = session.get('login') #Інфа про людину яка зайшла на сайт
    register_data = session.get('utc_regdata')
    return render_template('profile.html', Login = login , Reg_data = register_data ) #render_template - відображення html шаблону



#Сторінка для логіну
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        global user_login
        login = request.form['login']
        alpha_user_login = login
        password = request.form['password']
        conn = make_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) #Створення курсор з конфігурацією словника 
        cursor.execute('SELECT * FROM register_user_data WHERE user_login = %s AND user_password = %s',(login,password))#Знаходження відповідного ключа зі значенням
        user = cursor.fetchone() #Якщо вихід з цієї умови вірний (знайдеться підходящий login та password), то сама змінна буде True
        conn.commit()
        conn.close()
        if user:
            session['login'] = user['user_login']
            user_login = alpha_user_login
            session['utc_regdata'] = user['utc_user_regdata']
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
        conn = make_connection()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM register_user_data WHERE user_login = %s',(login,)) #fetchone() - переводить рядок елементів данних в кортеж
        user = cursor.fetchone()
        if user:
            flash('Логін вже зайнятий :3')
            conn.close()
            return redirect(url_for('signup'))
        register_data = dt.datetime.utcnow()
        UTC_reg_data = register_data.strftime("%Y-%m-%d %H:%M:%S")
        user_ip = request.remote_addr
        cursor.execute(
            'INSERT INTO register_user_data (user_login, user_password, user_ip, utc_user_regdata) VALUES (%s, %s, %s, %s)',
                (login, password,user_ip,UTC_reg_data))
        conn.commit() #Зберігаємо базу данних
        conn.close()
        flash("Registration successful. Welcome") #Виведення на екрані з верху
        return redirect(url_for('login'))
    return render_template('register.html')






@app.route('/main_f', methods = ['GET','POST'])
def main_f():
    return render_template('main_f.html')











#Sport Topic
@app.route('/topic_sport', methods=['GET', 'POST'])
def topic_sport():

    conn = make_connection()
    cursor = conn.cursor()
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
        conn.execute('INSERT INTO sport_topic_bd (user_login, message, message_time) VALUES (%s, %s, %s)', (user_sended_message, message, UTC_message_sended_time))
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
        conn.execute('INSERT INTO game_topic_bd (user_login, message, message_time) VALUES (%s, %s, %s)', (user_sended_message, message, UTC_message_sended_time))
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
        conn.execute('INSERT INTO FFIP_upgrades_topic_bd (user_login, message, message_time) VALUES %s, %s, %s)', (user_sended_message, message, UTC_message_sended_time))
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
    conn.execute('INSERT INTO anonim_users_IP (ip_adress , time) VALUES (%s,%s)',(anonim_user_ip,last_anonim_join))
    conn.commit() 
    conn.close()
    return anonim_user_ip 






#Відстежування залогіненог користувача
@app.route('/register_ip', methods=['POST'])
def red_logined_user_IP():
    logined_user_data = dt.datetime.utcnow()
    user_ip = request.remote_addr
    logined_user_data_formated = logined_user_data.strftime("%Y-%m-%d %H:%M:%S")
    user_login = session['login']
    conn = getConnection()
    try:
        conn.execute('INSERT INTO logined_user (user_login, user_logined_ip , user_logined_utc_data) VALUES (%s,%s,%s)',(user_login,user_ip,logined_user_data_formated))
    except: 
        conn.execute('INSERT INTO logined_user (user_login, user_logined_ip , user_logined_utc_data) VALUES (%s,%s,%s)',(user_login,user_ip,logined_user_data_formated))
    conn.commit() 
    conn.close()
    return user_ip 
#Переробити логіку, зробити нову таблицю та обєднати їх через IP




if __name__ == "__main__":
    app.run(debug=True)



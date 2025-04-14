from flask import *
import psycopg2
from datetime import datetime, timezone
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

#Функція відстежування
def follow(topic_name,UTC_message_sended_time, user_sended_message, message):
    user_sended_message_ip = request.remote_addr
    try:
        conn = make_connection()
        cursor = conn.cursor()            
        if 'login' in session:
            cursor.execute('INSERT INTO user_follow (user_logined_ip, user_login, user_logined_utc_data, user_done, topic_name, user_message) VALUES (%s,%s,%s,%s,%s,%s);',(user_sended_message_ip, user_sended_message, UTC_message_sended_time, 'send_message', topic_name ,message))
        else:
            cursor.execute('INSERT INTO user_follow (user_logined_ip, user_login, user_logined_utc_data, user_done, topic_name, user_message) VALUES (%s,%s,%s,%s,%s,%s);',(user_sended_message_ip, user_sended_message, UTC_message_sended_time,'send_message', topic_name ,message))
        conn.commit() #Зберігаємо базу данних
    except Exception as e:
        print(f'Помилка при записі в БД: {e}')
        return "Сталася помилка при збереженні", 500
    finally:
        cursor.close()
        conn.close()
    return '1'


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

    #Добавить відстеження
    
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
        register_data = datetime.now(timezone.utc)
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
    query = cursor.execute('SELECT user_message_id, user_message, user_message_utc_time, user_login FROM sport_topic_bd')
    query = cursor.fetchall()

    # Створюємо список словників для зберігання даних
    messages = []
    for row in query:
        messages.append({
            'user_message_id': row[0],
            'user_message': row[1],
            'user_message_utc_time': row[2],
            'user_login': row[3]
        })
    conn.commit() 
    conn.close()
    
    return render_template('topic_sport.html', Messages = messages)

#Message to sport db
@app.route('/sended_message_to_sport', methods = ['POST'])
def sended_message_to_sport():
    if request.method == 'POST':
        #Збереження отриманого повідомлення з шаблону в змінну
        #Не залежно від того що метод POST ми можемо викликати get(), (воно не залежить один від одного)
        message = request.form.get('message_input')
        if not message:
            return "Помилка: повідомлення не надійшло", 400
        
        #Реалізація методу відстежування людини, що надіслала повідомлення
        try:
            #Для залогінених юзерів
            user_sended_message = session['login']
        except:
            #Для анонімних юзерів (потрібно змінити на анонімний профіль замість IP)
            user_sended_message = 'Anonim'
        message_sended_time = datetime.now(timezone.utc)
        UTC_message_sended_time = message_sended_time.strftime("%Y-%m-%d %H:%M:%S")

        conn = make_connection()
        cursor = conn.cursor()
        #Збереження данних в таблицю
        cursor.execute('INSERT INTO sport_topic_bd (user_login, user_message, user_message_utc_time) VALUES (%s, %s, %s)', (user_sended_message, message, UTC_message_sended_time))
        conn.commit() #Зберігаємо базу данних
        conn.close()
        topic_name = 'topic_sport'  
        follow(topic_name,UTC_message_sended_time, user_sended_message, message)
        return redirect(url_for(f'{topic_name}'))





#Games Topic
@app.route('/topic_games' , methods = ['GET','POST'])
def topic_games():
    conn = make_connection()
    cursor = conn.cursor()
    # Об'єднаний запит для отримання всіх даних
    query = cursor.execute('SELECT user_message_id, user_message, user_message_utc_time, user_login FROM games_topic_bd')
    query = cursor.fetchall()

    # Створюємо список словників для зберігання даних
    messages = []
    for row in query:
        messages.append({
            'user_message_id': row[0],
            'user_message': row[1],
            'user_message_utc_time': row[2],
            'user_login': row[3]
        })
    conn.commit() 
    conn.close()
    
    return render_template('topic_games.html', Messages = messages)

#Message to game db
@app.route('/sended_message_to_games', methods = ['POST'])
def sended_message_to_games():
    if request.method == 'POST':
        #Збереження отриманого повідомлення з шаблону в змінну
        #Не залежно від того що метод POST ми можемо викликати get(), точніше це буде правильний вид призову самого методу
        message = request.form.get('message_input')
        if not message:
            return "Помилка: повідомлення не надійшло", 400
        
        #Реалізація методу відстежування людини, що надіслала повідомлення
        try:
            #Для залогінених юзерів
            user_sended_message = session['login']
        except:
            #Для анонімних юзерів (потрібно змінити на анонімний профіль замість IP)
            user_sended_message = 'Anonim'
        message_sended_time = datetime.now(timezone.utc)
        UTC_message_sended_time = message_sended_time.strftime("%Y-%m-%d %H:%M:%S")
        topic_name = 'topic_games'

        conn = make_connection()
        cursor = conn.cursor()
        #Збереження данних в таблицю
        cursor.execute('INSERT INTO games_topic_bd (user_login, user_message, user_message_utc_time) VALUES (%s, %s, %s)', (user_sended_message, message, UTC_message_sended_time))
        conn.commit() #Зберігаємо базу данних
        conn.close()    
        follow(topic_name,UTC_message_sended_time, user_sended_message, message)
        return redirect(url_for(f'{topic_name}'))





#FFIP ubrades Topic
@app.route('/topic_upgrade_FFIP' , methods = ['GET','POST'])
def topic_upgrade_FFIP():
    conn = make_connection()
    cursor = conn.cursor()
    # Об'єднаний запит для отримання всіх даних
    query = cursor.execute('SELECT user_message_id, user_message, user_message_utc_time, user_login FROM FFIP_upgrades_topic_bd')
    query = cursor.fetchall()

    # Створюємо список словників для зберігання даних
    messages = []
    for row in query:
        messages.append({
            'user_message_id': row[0],
            'user_message': row[1],
            'user_message_utc_time': row[2],
            'user_login': row[3]
        })
    conn.commit() 
    conn.close()
    
    return render_template('topic_upgrade_FFIP.html', Messages = messages)

#Message to FFIP ubrades db
@app.route('/sended_message_to_upgrade_FFIP', methods = ['POST'])
def sended_message_to_upgrade_FFIP():
    if request.method == 'POST':
        #Збереження отриманого повідомлення з шаблону в змінну
        #Не залежно від того що метод POST ми можемо викликати get(), (воно не залежить один від одного)
        message = request.form.get('message_input')
        if not message:
            return "Помилка: повідомлення не надійшло", 400
        #Реалізація методу відстежування людини, що надіслала повідомлення
        try:
            #Для залогінених юзерів
            user_sended_message = session['login']
        except:
            #Для анонімних юзерів (потрібно змінити на анонімний профіль замість IP)
            user_sended_message = 'Anonim'
        message_sended_time = datetime.now(timezone.utc)
        UTC_message_sended_time = message_sended_time.strftime("%Y-%m-%d %H:%M:%S")
        topic_name = 'topic_upgrade_FFIP'

        conn = make_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO ffip_upgrades_topic_bd (user_login, user_message, user_message_utc_time) VALUES (%s, %s, %s);', (user_sended_message, message, UTC_message_sended_time))
        conn.commit()
        conn.close()
        follow(topic_name,UTC_message_sended_time, user_sended_message, message)
    return redirect(url_for(f'{topic_name}'))



    







#Створення логіки виходу з сайту
@app.route('/logout')
def logout():
    session.pop('login', None) #pop() - видаляє данні про користувача з сесіїі
    return redirect(url_for('login'))    


    


if __name__ == "__main__":
    app.run(debug=True)



#Routes - endpoints do URL - rotas
#Importar render_template significa importar os templates html dinâmicos
#return render_template("{nome}.html")

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import psycopg2

#CONEXÃO BANCO DE DADOS
POSTGRESQL_URI = "postgres://rrsllcdu:VErRUumdSLoypdkk5nLts9HolGC0xnYA@babar.db.elephantsql.com/rrsllcdu"
connection = psycopg2.connect(POSTGRESQL_URI)


with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'usuarios');")
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            cursor.execute("CREATE TABLE usuarios (nome TEXT, email TEXT, senha TEXT);")


views = Blueprint("views", __name__)

@views.route('/home/<username>')
def home(username):
    return render_template('index.html',name_login = username)


@views.route('/', methods=['GET', 'POST'])
@views.route('login', methods=['GET', 'POST'])
def login():

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        with connection.cursor() as cursor:
            # Executar o SELECT na tabela 'usuarios' com um nome de usuário e senha específicos
            cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s;", (username, password))
            result = cursor.fetchone()  # Obter o resultado do SELECT
            if result is None:
                error = 'Usuário ou senha incorretos. Tente novamente.'
            else:
                return redirect(url_for('views.home',username=username))

        """ if username != 'pietro' or password != '123321':
            error = 'Usuário ou senha incorretos. Tente novamente.'
        else:
            return redirect(url_for('views.home',username=username)) """
    return render_template('index2.html', error= error)

@views.route('singup', methods=['GET', 'POST'])
def singup():

    """ Verificar existencia e registrar no banco de dados """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        password_confirm = request.form['password_confirm']


        if password != password_confirm:
            error = 'A senha digitada não é semelhante à sua confirmação'
            return render_template('index3.html',error=error)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO usuarios VALUES(%s,%s,%s);",
                                (email,
                                username,
                                password), 
                                )
        # aqui você pode fazer as validações e o cadastro do usuário
        # e depois redirecionar para a tela de login
        return redirect(url_for('views.home',username=username))
    
    return render_template('index3.html')
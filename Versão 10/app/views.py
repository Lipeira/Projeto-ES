#Routes - endpoints do URL - rotas
#Importar render_template significa importar os templates html dinâmicos
#return render_template("{nome}.html")

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import psycopg2

# Registrar o filtro na environment do Jinja2




#CONEXÃO BANCO DE DADOS
POSTGRESQL_URI = "postgres://rrsllcdu:VErRUumdSLoypdkk5nLts9HolGC0xnYA@babar.db.elephantsql.com/rrsllcdu"
connection = psycopg2.connect(POSTGRESQL_URI)


with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'usuarios');")
        table_exists = cursor.fetchone()[0]
        if not table_exists:
            cursor.execute("CREATE TABLE usuarios (nome TEXT, email TEXT, senha TEXT);")


with connection:
    with connection.cursor() as cursor:
        # Cria tabela Centro
        cursor.execute("""

            CREATE TABLE IF NOT EXISTS animal (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            especie VARCHAR(255) NOT NULL,
            raca VARCHAR(255) NOT NULL,
            idade INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            imagem VARCHAR(255) NOT NULL,
            local_circulacao VARCHAR(255) NOT NULL);
            
        """)

        # Confirma as alterações no banco de dados
        connection.commit()


views = Blueprint("views", __name__)

@views.route('/home/<username>', methods=['GET', 'POST'])
def home(username):
    if request.method == 'POST':
        # Obtenha os dados do formulário
        nome = request.form['name']
        especie = request.form['species']
        raca = request.form['breed']
        idade = request.form['age']
        descricao = request.form['description']
        centro = request.form['center']

        imagem = request.files['image']  # Obtém o arquivo de imagem do formulário
        imagem.save('static/images/' + imagem.filename)  # Salva a imagem no diretório local
        caminho_imagem = 'images/' + imagem.filename  # Obtém o caminho completo do arquivo salvo

        # Insira os dados no banco de dados
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO animal (nome, especie, raca, idade, descricao, imagem, local_circulacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (nome, especie, raca, idade, descricao, caminho_imagem, centro))


    with connection:
        with connection.cursor() as cursor:
            # Execute uma consulta SQL para obter os dados da tabela 'animal'
                cursor.execute("SELECT id, nome, especie, raca, idade, descricao, imagem, local_circulacao FROM animal")
                animal = cursor.fetchall()  # Obtém todos os registros como uma lista de tuplas


    return render_template('index.html', name_login=username, animal = animal)





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


@views.route('/fetch_animals', methods=['GET'])
def fetch_animals():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, especie, raca, idade, descricao, imagem, local_circulacao FROM animal")
            animal = cursor.fetchall()
    return jsonify(animal)

@views.route('/remove_animal', methods=['POST'])
def remove_animal():
    data = request.get_json()
    animal_id = data['id']

    with connection:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM animal WHERE id = %s", (animal_id,))


    return redirect(url_for('views.home', username='ufpe'))


@views.route('/animal/<int:animal_id>', methods=['GET'])
def get_animal(animal_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, nome, especie, raca, idade, descricao, imagem, local_circulacao FROM animal WHERE id = %s", (animal_id,))
            animal = cursor.fetchone()  # Obtenha um único registro
    return jsonify(animal)  # Envie os dados do animal como uma resposta JSON
#Routes - endpoints do URL - rotas
#Importar render_template significa importar os templates html dinâmicos
#    return render_template("{nome}.html")
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

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
        if username != 'pietro' or password != '123321':
            error = 'Usuário ou senha incorretos. Tente novamente.'
        else:
            return redirect(url_for('views.home',username=username))
    return render_template('index2.html', error= error)

@views.route('singup', methods=['GET', 'POST'])
def singup():

    """ Verificar existencia e registrar no banco de dados """

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        if password != password_confirm:
            error = 'A senha digitada não é semelhante à sua confirmação'
            return render_template('index3.html',error=error)

        # aqui você pode fazer as validações e o cadastro do usuário
        # e depois redirecionar para a tela de login
        return redirect(url_for('views.home',username=username))
    
    return render_template('index3.html')
# Importando as bibliotecas:
from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL
from db import *
import os
from werkzeug.utils import secure_filename

# Instanciando o objeto Flask
app = Flask(__name__)

# definido o endereço em que as imagens serão salvas
UPLOAD_FOLDER = 'C://Users//Adm//PycharmProjects//projeto_site_concessionaria//static//images'

# configurando a pasta de upload a qual as imagens enviadas  pelo usuario serão armazenadas
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Instanciando o objeto MySQL
mysql = MySQL()

# Conectando MySQL ao Flask
mysql.init_app(app)

# Configuração do Banco de dados:
config(app)


# Rota para o index:
@app.route('/')
def index():
    return render_template('index.html')


# rota para a pagina de administração do superior
@app.route('/adm', methods=['GET','POST'])
def adm():
    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # renderizando a pagina do administrador:
    return render_template('adm.html', lista_fun=get_fun(cursor), lista_car=get_carros(cursor))


# rota para a pagina do funcionario, com as reservas
@app.route('/funcionario')
def funcionario():

    # renderizando a pagina do funcionario:
    return render_template('funcionario.html')


# rota para a pagina de login
@app.route('/login')
def login():
    return render_template('login.html')


# rota para entrar, seja como funcionario seja como administrador
@app.route('/entrar', methods=['GET','POST'])
def entrar():
    if request.method == 'POST':

        login = request.form.get('login')
        senha = request.form.get('senha')

        # Obtendo o cursor para acessar o BD
        conn, cursor = get_db(mysql)

        # VARIAVEL CONTENDO A RESPOSTA SE O LOGIN ESTÁ NA TABELA FUNCIONARIO:
        fun = get_idfun(cursor, login, senha)

        # VARIAVEL CONTENDO A RESPOSTA SE O LOGIN ESTÁ NA TABELA ADM:
        adm = get_idadm(cursor, login, senha)

        if fun is None:
            if adm is None:
                # Fechar o cursor
                cursor.close()
                # Fechar a conexao
                conn.close()
                return render_template('login.html', erro='Login/Senha não cadastrado!')

            else:

                return redirect(url_for('adm'))

        else:
            # Fechar o cursor
            cursor.close()
            # Fechar a conexao
            conn.close()
            return render_template('funcionario.html')

    else:
        return render_template('index.html', erro='Método incorreto. Use POST!')


# rota para o formulario de adição de funcionario
@app.route('/form_func')
def form_func():
    return render_template('form_func.html')


# rota que adiciona o funcionario criado e retorna para a pagina do administrador
@app.route('/add_func', methods=['GET','POST'])
def add_func():

    novo_login = request.form.get('novo_login')
    nova_senha = request.form.get('nova_senha')

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # função que insere funcionario:
    add_new_func(conn, cursor, novo_login, nova_senha)

    return redirect(url_for('adm'))


# rota para remover um funcionario do banco de dados
@app.route('/deletar_func/<id>')
def deletar_func(id):

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # função para deletar funcionarios do banco de dados:
    del_func(conn, cursor, id)

    return redirect(url_for('adm'))


# rota para remover anuncio do banco de dados
@app.route('/deletar_anun/<id>')
def deletar_anun(id):
    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    # função para deletar funcionarios do banco de dados:
    del_anun(conn, cursor, id)

    return redirect(url_for('adm'))


# rota para o formulario de alteração de dados dos funcionarios
@app.route('/form_alter_func/<id>')
def form_alter_func(id):

    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    infos = info_func(cursor, id)

    return render_template('form_alter_func.html', informacoes=infos)


# rota para salvar as alterações nos dados do formulario
@app.route('/save_alter_func', methods=['POST'])
def save_alter_func():
    if request.method == 'POST':

        # Obtendo o cursor para acessar o BD
        conn, cursor = get_db(mysql)

        updated_login = request.form.get('updated_login')
        updated_senha = request.form.get('updated_senha')
        idfuncionario = request.form.get('idfuncionario')

        # função de alteração de senha:
        alter_func(conn, cursor, updated_login, updated_senha, idfuncionario)

        # redirecionamento para a função adm da rota adm
        return redirect(url_for('adm'))

    else:
        # redirecionamento para a função adm da rota adm
        return redirect(url_for('adm'))


# rota para adicionar um carro a lista de carros vips
@app.route('/add_vip/<id>/<estado>')
def add_vip(id, estado):
    # Obtendo o cursor para acessar o BD
    conn, cursor = get_db(mysql)

    vip(conn, cursor, id, estado)

    return redirect(url_for('adm'))


# rota para o formulario de adição de carros
@app.route('/form_car')
def form_car():
    return render_template('form_car.html')


# rota para adicionar o carro novo ao banco de dados e sua foto a pasta static
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():

    # Verificação do metodo:
    if request.method == 'POST':

        # Obtendo o cursor para acessar o BD
        conn, cursor = get_db(mysql)

        # conn, cursor, modelo, marca, ano, preco, vip, img
        modelo = request.form.get('modelo')
        marca = request.form.get('marca')
        ano = request.form.get('ano')
        preco = request.form.get('preco')
        vip = request.form.get('y_or_n')

        print(f'modelo: {modelo}, marca: {marca}, ano:{ano}, preco:{preco}, vip: {vip}')
        # verifica se tem a parte file no request
        if 'img' not in request.files:
            # print('o arquivo não foi encontrado')
            return render_template('index.html')

        # pega o arquivo
        arquivo = request.files['img']

        # se o usuario nao selecionar o arquivo
        # o browser manda um arquivo sem nome
        if arquivo.filename == '':
            # print('Arquivo sem nome')
            return render_template('index.html')

        else:
            # armazenando o nome do arquivo em uma variavel:
            img_name = secure_filename(arquivo.filename)
            arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename))
            # print(f'O nome do arquivo é: {img_name}')

            # print(f'modelo: {modelo}, marca: {marca}, ano:{ano}, preco:{preco}, vip: {vip}, nome da img: {img_name}')
            add_new_car(conn, cursor, modelo, marca, ano, preco, vip, img_name)

            return redirect(url_for('adm'))


# Rodando a app
if __name__ == '__main__':
    app.run(debug=True)



# Importando biblioteca para manipulação de Banco de Dados:
from flaskext.mysql import MySQL


# função para configurar o acesso a banco
def config(app):
    # Configurando o acesso ao MySQL
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'concessionaria'


# funação que retorna a conexão e o cursor:
def get_db(mysql):
    # Obtendo a concxão para acessar o BD
    conn = mysql.connect()
    # Obtendo o cursor para acessar o BD
    cursor = conn.cursor()
    # retornando a conexão e o cursor:
    return conn, cursor


# função que retorna se o login enviado está na tabela adm, caso esteja retorna seu ID
def get_idadm(cursor, login, senha):
    # Executar o sql
    cursor.execute(f'select idadministrador from administrador where login = "{login}" and senha = "{senha}"')

    # Recuperando o retorno do BD
    idadm = cursor.fetchone()

    # Retornar o idlogin
    return idadm


# função que retorna se o login enviado está na tabela funcionario, caso esteja retorna seu ID
def get_idfun(cursor, login, senha):
    # Executar o sql
    cursor.execute(f'select idfuncionario from funcionario where login = "{login}" and senha = "{senha}"')

    # Recuperando o retorno do BD
    idfun = cursor.fetchone()

    # Retornar o idlogin
    return idfun


# função que retorna a lista de funcionarios do banco de dados
def get_fun(cursor):
    # Executar o sql
    cursor.execute(f'select idfuncionario, login, senha from funcionario')

    # Recuperando o retorno do BD
    lista_fun = cursor.fetchall()

    # retorna a lista de funcionarios:
    return lista_fun


# função que retorna a lista de carros do banco de dados
def get_carros(cursor):
    # Executar o sql
    cursor.execute(f'select * from carros order by reservado DESC, vip DESC')

    # Recuperando o retorno do BD
    lista_car = cursor.fetchall()

    # retorna a lista de funcionarios:
    return lista_car


# função que adiciona um novo funcionario ao banco de dados
def add_new_func(conn, cursor, novo_login, nova_senha):
    # Executar o sql
    cursor.execute(f'INSERT INTO `concessionaria`.`funcionario` (`login`, `senha`) VALUES ("{novo_login}", "{nova_senha}");')

    # efetivar adição
    conn.commit()


# função que deleta o funcionario do Banco de Dados
def del_func(conn, cursor, id):
    # Executar o SQL
    cursor.execute(f'DELETE from funcionario WHERE idfuncionario = { id }')

    # efetivar exclusão
    conn.commit()


# função que deleta o anuncio do Banco de Dados
def del_anun(conn, cursor, id):
    # Executar o SQL
    cursor.execute(f'DELETE from carros WHERE idcarros = { id }')

    # efetivar exclusão
    conn.commit()


# função que altera os dados do funcionario
def alter_func(conn, cursor, updated_login, updated_senha, id):
    cursor.execute(f'UPDATE funcionario SET login = "{updated_login}", senha ="{updated_senha}" WHERE idfuncionario= { id }')
    # print(f'novo login: {updated_login}, nova senha: {updated_senha} no id: {id}')
    # efetivar alteração
    conn.commit()


# função que pega informações do funcionario para preencher formulario
def info_func(cursor, id):
    cursor.execute(f'select * from funcionario where idfuncionario = { id }')

    # Recuperando o retorno do BD
    dados = cursor.fetchone()

    print(dados)

    return dados


# função que altera o estado do carro, set se ele é ou não VIP
def vip(conn, cursor, id, estado):
    if estado == 'N':
        cursor.execute(f'UPDATE carros SET vip= "S" WHERE idcarros={ id }')
        # efetivar alteração
        conn.commit()

    elif estado == 'S':
        cursor.execute(f'UPDATE carros SET vip= "N" WHERE idcarros= { id }')
        # efetivar alteração
        conn.commit()


# funçãp para adicionar carros:
def add_new_car(conn, cursor, modelo, marca, ano, preco, vip, img):
    # Executar o sql
    cursor.execute(f'INSERT INTO carros ( modelo, marca, ano, reservado, preco, vip, img) VALUES ( "{ modelo }", "{ marca }", "{ano}", "N", "{ preco }", "{ vip }", "{ img }" )')
    # print(f'os dados dentro do banco são: "{ modelo }", "{ marca }", "{ano}", "N", "{ preco }", "{ vip }", "{ img }" ')
    # efetivar adição
    conn.commit()


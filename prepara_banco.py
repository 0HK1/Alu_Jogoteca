import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='***',
        user='***',
        password='***'
    )
    cursor = conn.cursor()  # Move esta linha para dentro do bloco try
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)
else:
    # Exclui o banco de dados 'jogoteca' se ele já existir
    cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

    # Cria o banco de dados 'jogoteca'
    cursor.execute("CREATE DATABASE `jogoteca`;")

    # Seleciona o banco de dados 'jogoteca'
    cursor.execute("USE `jogoteca`;")

    # Definições das tabelas
    TABLES = {}
    TABLES['Jogos'] = ('''
          CREATE TABLE `jogos` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `nome` varchar(50) NOT NULL,
          `categoria` varchar(40) NOT NULL,
          `console` varchar(20) NOT NULL,
          PRIMARY KEY (`id`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

    TABLES['Usuarios'] = ('''
          CREATE TABLE `usuarios` (
          `nome` varchar(20) NOT NULL,
          `nickname` varchar(8) NOT NULL,
          `senha` varchar(100) NOT NULL,
          PRIMARY KEY (`nickname`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

    for tabela_nome in TABLES:
        tabela_sql = TABLES[tabela_nome]
        try:
            print('Criando tabela {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('Já existe')
            else:
                print(err.msg)
        else:
            print('OK')

    # Inserindo usuários
    usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
    usuarios = [
        ("Bruno Divino", "BD", "alohomora"),
        ("Camila Ferreira", "Mila", "paozinho"),
        ("Guilherme Louro", "Cake", "python_eh_vida")
    ]
    cursor.executemany(usuario_sql, usuarios)

    cursor.execute('SELECT * FROM jogoteca.usuarios')
    print(' -------------  Usuários:  -------------')
    for user in cursor.fetchall():
        print(user[1])

    # Inserindo jogos
    jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
    jogos = [
        ('Tetris', 'Puzzle', 'Atari'),
        ('God of War', 'Hack n Slash', 'PS2'),
        ('Mortal Kombat', 'Luta', 'PS2'),
        ('Valorant', 'FPS', 'PC'),
        ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
        ('Need for Speed', 'Corrida', 'PS2'),
    ]
    cursor.executemany(jogos_sql, jogos)

    cursor.execute('SELECT * FROM jogoteca.jogos')
    print(' -------------  Jogos:  -------------')
    for jogo in cursor.fetchall():
        print(jogo[1])

    # Commitando se não nada tem efeito
    conn.commit()

    # Fechando cursor e conexão
    cursor.close()
    conn.close()

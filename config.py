SECRET_KEY = 'Coxinha123'

# Conexão Banco de Dados

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{user}:{password}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        user='root',
        password='Zy(S_Tw0%(^V$pc.',
        servidor='localhost',
        database='jogoteca'
    )

import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="12345678",
        database="db_produtos"
    )


def gerar_codigo(grupo, tipo_alimento, pais):

    if not grupo or not tipo_alimento or not pais:
        raise ValueError("Parâmetros inválidos")

    if len(pais) != 2:
        raise ValueError("Pais deve ter 2 caracteres")

    conn = conectar()
    cursor = conn.cursor()

    query = "SELECT MAX(sec) FROM produtos WHERE Grupo = %s"
    cursor.execute(query, (grupo,))
    resultado = cursor.fetchone()

    if resultado[0] is None:
        sec = 1
    else:
        sec = resultado[0] + 1

    sequencia = str(sec).zfill(4)
    codigo = f"{pais}{grupo}{sequencia}{tipo_alimento}"

    cursor.close()
    conn.close()

    return codigo, sec


def inserir_produto(grupo, tipo_alimento, pais):

    codigo, sec = gerar_codigo(grupo, tipo_alimento, pais)

    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO produtos (codigo, sec, Grupo, Tipo_Alimento, Pais)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (codigo, sec, grupo, tipo_alimento, pais))
    conn.commit()

    cursor.close()
    conn.close()

    print("Produto inserido:", codigo)


if __name__ == "__main__":
    inserir_produto("C", "A", "BR")

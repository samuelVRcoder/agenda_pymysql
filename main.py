import PySimpleGUI as sg
import pymysql as sql
import dotenv
import os

dotenv.load_dotenv()

sg.theme("Black")

conn = sql.connect(
    host = os.environ['host'],
    user = os.environ['user'],
    password = os.environ['password'],
    database = os.environ['database'],
    )

cursor = conn.cursor()

cursor.execute("create table if not exists users (nome varchar(255), telefone varchar(255)); ")

layout = [   

    [sg.Text("Nome")],
    [sg.Input(key="nome")],
    [sg.Text("Telefone")],
    [sg.Input(key="fone")],
    [sg.Button("Salvar")],
    [sg.Button("Pesquisar por Nome")],
    [sg.Button("Deletar por Nome")]

    ]

window = sg.Window("Tela de Gestão", layout=layout)

while True:
    events, values = window.read()

    if events == "Salvar":

        if len(values["nome"]) > 0:
            if len(values["fone"]) > 0:
                cursor.execute(f"insert into users (nome, telefone) values (%s, %s) ",(values['nome'], values['fone']))
                conn.commit()

    if events == "Pesquisar por Nome":
        cursor.execute("select * from users where nome = %s limit 5 ", values["nome"])
        lista = cursor.fetchall()

        lista_str = ''
        for i,a in lista:
            lista_str += i+","+a+"\n\n"

        sg.popup(lista_str)

    if events == "Deletar por Nome":
        cursor.execute("delete from users where nome = %s ", values["nome"])
        conn.commit()

    if events == sg.WIN_CLOSED:
        break

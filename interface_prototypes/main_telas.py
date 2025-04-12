import sys
import requests
import os
# import cv2
import random
import shutil
import bcrypt
import glob
# import imutils
from PIL import Image

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QImage, QPixmap
#Importndo as telas
from _cadastro_administrador_1_0 import Cad_adm
from _cadastro_imagens1_0 import Cad_images
from _login_administrador_1_0 import Login_adm
from _menu_inicial_1_1 import Menu_inicial
from _update_data import Update_data
from _visualizar_individuo_1_0 import Show_data

class Ui_Main(QtWidgets.QWidget):
    '''
    O objeto Ui_Main possibilita ter acesso a todas as telas varias telas.
    '''

    def setupUi(self,Main):

        Main.setObjectName('Main')
        Main.resize(640,480)#tamnaho da tela

        self.QtStack=QtWidgets.QStackedLayout()#cria pilha
class Ui_Main(QtWidgets.QWidget):
    '''
    O objeto Ui_Main possibilita ter acesso a todas as telas varias telas.
    '''

    def setupUi(self,Main):

        Main.setObjectName('Main')
        Main.resize(640,480)#tamnaho da tela

        self.QtStack=QtWidgets.QStackedLayout()#cria pilha


        #quantidde de telas
        self.stack0 = QMainWindow()
        self.stack1 = QMainWindow()
        self.stack2 = QMainWindow()
        self.stack3 = QMainWindow()
        self.stack4 = QMainWindow()
        self.stack5 = QMainWindow()

        #Crindo os objetos par as telas
        self.tela_login_adm = Login_adm()
        self.tela_login_adm.setupUi(self.stack0)

        self.tela_cad_adm = Cad_adm()
        self.tela_cad_adm.setupUi(self.stack2)

        self.tela_cad_images = Cad_images()
        self.tela_cad_images.setupUi(self.stack1)
        
        self.tela_menu_inicial = Menu_inicial()
        self.tela_menu_inicial.setupUi(self.stack3)
        
        self.tela_update_data = Update_data()
        self.tela_update_data.setupUi(self.stack4)
        
        self.tela_show_data = Show_data()
        self.tela_show_data.setupUi(self.stack5)

        #add ao QtStack
        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)


class Main(QMainWindow,Ui_Main):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)

        self.file_name = ''
        self.list_images_of_dir = dict()

        #Botões

        # tela_login_adm
        self.tela_login_adm.login_pushButton_logar.clicked.connect(self.botao_login)
        self.tela_login_adm.login_pushButton_entrar_cadastro.clicked.connect(self.abrir_cad_adm)

        # tela_cad_adm
        self.tela_cad_adm.cadastro_pushButton_cadastrar.clicked.connect(self.botao_cadastro_adm)
        self.tela_cad_adm.cadastro_pushButton_entrar_login.clicked.connect(self.abrir_login_adm)

        # tela_menu_inicial
        self.tela_menu_inicial.sair_pushButton.clicked.connect(self.abrir_login_adm)
        self.tela_menu_inicial.reconhecimento_pushButton.clicked.connect(self.abrir_update_data)
        self.tela_menu_inicial.cadastro_pushButton.clicked.connect(self.abrir_cad_images)

        # tela_cad_images
        self.tela_cad_images.cad_img_pushButton_start_camera.clicked.connect(self.load_imgens)
        self.tela_cad_images.cad_img_pushButton_captura_2.clicked.connect(self.import_dir)
        self.tela_cad_images.cad_img_pushButton_captura.clicked.connect(self.paciente_nao_informado)
        self.tela_cad_images.cadastrar_pushButton_imagens.clicked.connect(self.classification_imagens)
        self.tela_cad_images.voltar.clicked.connect(self.sair_clas_pac)

        # tela_show_data
        self.tela_show_data.edita_pushButton_editar.clicked.connect(self.cad_paciente)
        self.tela_show_data.edita_pushButton_voltar.clicked.connect(self.sair_cad_pac)
        self.tela_show_data.edita_pushButton_remover.clicked.connect(self.abrir_menu_inicial)

        # tela_update_data
        self.tela_update_data.edita_pushButton_voltar.clicked.connect(self.abrir_menu_inicial)
        self.tela_update_data.editar_pushButton_buscar.clicked.connect(self.busca_paciente)
        self.tela_update_data.edita_pushButton_editar.clicked.connect(self.editar_paciente)
        self.tela_update_data.edita_pushButton_remover.clicked.connect(self.remove_paciente)

    # Busca do paciente
    def busca_paciente(self):
        email_mng = self._adm['Email']
        id_paciente = self.tela_update_data.login_lineEdit_cpf_3.text()
        query = {'email_mng': email_mng, 'id_paciente': id_paciente}
        url = "http://127.0.0.1:8000/search_paciente"
        response_metadata = requests.get(url, params=query).json()
        print(response_metadata)
        
        if response_metadata['mensagem'] != 'Error: Paciente não encontrado encontrado':
            if os.path.exists(response_metadata['path_in_local_machine']):
                image = QPixmap(response_metadata['path_in_local_machine'])
                self.setPhoto(self.tela_update_data.display_camera,image)
                predicao = response_metadata['predicao']
                confidence = response_metadata['confianca']

                if predicao == '0':
                    text_result = f'{confidence.split(" ")[0][3:5]}% Sem Glaucoma\n'
                elif predicao == '1':
                    text_result = f'{confidence.split(" ")[1][2:4]}% Com Glaucoma\n'
                elif predicao == '_1':
                    text_result = f'{confidence.split(" ")[2][2:4]}% Indefinido\n'
                self.tela_update_data.label_7.setText(text_result)
                # Verificar se a imagem esta no buffer
                # caso não esteja importar
                # coso esteja colocar no displai e atulizar campo editavel
                id_paciente = self.tela_update_data.login_lineEdit_cpf_5.setText(id_paciente)
            else:
                QMessageBox.information(None, 'Busca do Paciente', 'Erro: paciente não encontrado.')
        else:
            id_paciente = self.tela_update_data.login_lineEdit_cpf_3.setText('')
            QMessageBox.information(None, 'Busca do Paciente', 'Erro: paciente não encontrado.')
        # TODO esquema de conserto para imagens faltantes no buffer

    # editar paciente
    def editar_paciente(self):
        id_paciente = self.tela_update_data.login_lineEdit_cpf_3.text()
        new_id_paciente = self.tela_update_data.login_lineEdit_cpf_5.text()
        data = {'query_id_paciente': id_paciente, 
                'new_id_paciente': new_id_paciente}
        url = "http://127.0.0.1:8000/editar_paciente"
        response = requests.get(url, params=data).json()
        self.tela_update_data.login_lineEdit_cpf_3.setText('')
        QMessageBox.information(None, 'Editar Paciente', response['mensagem'])

    def remove_paciente(self):
        id_paciente = self.tela_update_data.login_lineEdit_cpf_5.text()
        data = {'query_id_paciente': id_paciente}
        url = "http://127.0.0.1:8000/remove_paciente"
        response = requests.get(url, params=data).json()
        QMessageBox.information(None, 'Editar Paciente', response['mensagem'])
        self.tela_update_data.display_camera.clear()

    # cad imagens
    def cad_paciente(self):
        # print(self.list_images_of_dir)
        for key in self.list_images_of_dir.keys():
            
            if '-' in key:
                id_for_path = '_'+key[1:]
            else:
                id_for_path = '_'+key

            random_integer = random.randint(1, 5000)
            dst_path = f"../../../buffer/{id_for_path}_{random_integer}.png"
            
            shutil.copy(self.list_images_of_dir[key], dst_path)

            with open(dst_path, "rb") as image_file:
                url_classificacao = "http://127.0.0.1:8000/cad_image"
                files = {"file": image_file,}
                data = {"id_paciente":key,
                        "email_mng": self._adm['Email'],
                        "path_in_local_machine":dst_path,}
                
                        # Fazer a requisição GET com cabeçalhos
                response = requests.post(url_classificacao, files=files, data=data).json()
            print(type(key))
            print(response)
            print(data)
            if response["mensagem"] == 'OK: Paciente cadastrada':
                QMessageBox.information(None, 'Cadastro do Paciente', f'Paciente {key} cadastrado.')
            else:
                QMessageBox.information(None, 'Cadastro do Paciente', 'Erro: paciente não cadastrado.')
        if response["mensagem"] == 'OK: Paciente cadastrada':
            self.abrir_menu_inicial()

    # classificacao de imagens
    def classification_imagens(self):
        # Pegar os dados e imagem
        id_paciente = self.tela_cad_images.cadastro_lineEdit_email.text()
        if id_paciente != '':
            if self.file_name != '':
                # Colocar imagem no display de classficiação
                image = QPixmap(self.file_name)
                # print('image.shape:',type(image))
                self.setPhoto(self.tela_show_data.display_camera,image)
                # Classificar paciente
                # Abrir o arquivo de imagem em modo binário
                with open(self.file_name, "rb") as image_file:
                    # Criar um dicionário de arquivos, onde a chave é o nome do campo esperado pela API e o valor é o arquivo
                    files = {"file": image_file}
                    # Fazer a requisição GET com cabeçalhos
                    url = "http://127.0.0.1:8000/classification_image"
                    response = requests.post(url, files=files).json()
                    # pegar inferencia

                predicao = response['predicao']
                confidence = response['confianca']
                    # Colocar dados do dysplay de classificação
                print(response)
                if predicao == '0':
                    self.tela_show_data.label_7.setText(f"{confidence.split(' ')[0][3:5]}% sem Glaucoma")
                elif predicao == '1':
                    self.tela_show_data.label_7.setText(f"{confidence.split(' ')[1][2:4]}% com Glaucoma")
                elif predicao == '_1':
                    self.tela_show_data.label_7.setText(f"{confidence.split(' ')[2][2:4]}% não definido")
                self.tela_show_data.label_3.setText(id_paciente)
                
                self.list_images_of_dir = dict()
                self.list_images_of_dir[id_paciente] = self.file_name

                self.abrir_show_data()
            else:
                QMessageBox.information(None, 'Cadastro do Paciente', 'Erro: Imagem do paciente não importada.')
        else:
            QMessageBox.information(None, 'Cadastro do Paciente', 'ERRO: Id do paciente não informado.')
        # Entrar na pagina de classificação e cadastro
        # limpar display

    # Paciente não informado
    def paciente_nao_informado(self):
        # print('Aqui')
        # Buscar todos os pacientes
        url = "http://127.0.0.1:8000/retorna_todos_pacientes"
        response = requests.get(url).json()
        # print(response)
        generate_it_list = list()
        # Verificar quais pacientes com id negativo eixstem
        for key in response.keys():
            if key != 'mensagem':
                if '-' in response[key]['id_paciente']:
                    generate_it_list.append(response[key]['id_paciente'])
        
        cont = -1
        while str(cont) in generate_it_list:
            cont -= 1
        # Salvar um não existente
        self.tela_cad_images.cadastro_lineEdit_email.setText(f'{cont}')


    # Busca de imagens
    def browsefiles(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io')
        return file_name

    def setPhoto(self,display,image,h=300, w=502):
            
        """
            Essa função vair utilizar a imagem passadapor parametro realizar o
            preprocessamento ajustando seu diametro e inserindo no display da
            da interface.
            :param image:
            :return:
        """
        # self.tmp = image
        # frame = image.resize((w, h), Image.Resampling.LANCZOS)
        # image = QImage(frame,w,h,QImage.Format_RGB888)
        display.setPixmap(image)

    def load_imgens(self):
        self.file_name = self.browsefiles()[0]
        #image = Image.open(file_name[0])
        image = QPixmap(self.file_name)
        # print('image.shape:',type(image))
        self.setPhoto(self.tela_cad_images.display_camera,image)

    # Buscar diretorio
    def browsedir(self):
        file_name = QFileDialog.getExistingDirectory(self, 'Open Directory', 'D:\codefirst.io')
        return file_name

    def import_dir(self):
        file_name = self.browsedir()
        text_result = ''
        id_result = 'id:\n'
        cont = 0
        self.list_images_of_dir = dict()
        for path_images in glob.glob(file_name+'/*.png'):
            with open(path_images, "rb") as image_file:
                # Criar um dicionário de arquivos, onde a chave é o nome do campo esperado pela API e o valor é o arquivo
                files = {"file": image_file}
                # Fazer a requisição GET com cabeçalhos
                url = "http://127.0.0.1:8000/classification_image"
                response = requests.post(url, files=files).json()
                # pegar inferencia
                print(response)

            predicao = response['predicao']
            confidence = response['confianca']

            if predicao == '0':
                text_result+= f'{confidence.split(" ")[0][3:5]}% Sem Glaucoma\n'
            elif predicao == '1':
                text_result+= f'{confidence.split(" ")[1][2:4]}% Com Glaucoma\n'
            elif predicao == '_1':
                text_result+= f'{confidence.split(" ")[2][2:4]}% Indefinido\n'
            
            id_result += path_images.split('/')[-1][:-4]+'\n'
            self.list_images_of_dir[path_images.split('/')[-1][:-4]] = path_images
            cont += 1
            #if cont == 4:
            #     text_result += '...'
            #     id_result += '...'

        self.tela_show_data.label_7.setText(text_result)
        self.tela_show_data.label_3.setText(id_result)

        self.abrir_show_data()

        print(text_result)
        print(id_result)

    def sair_cad_pac(self):
        self.tela_show_data.display_camera.clear()
        self.abrir_cad_images()

    def sair_clas_pac(self):
        self.tela_cad_images.cadastro_lineEdit_email.setText('')
        self.tela_cad_images.display_camera.clear()
        self.abrir_menu_inicial()

    #Abrindo as telas
    def abrir_cad_images(self):
        self.QtStack.setCurrentIndex(1)

    def abrir_login_adm(self):
        self.QtStack.setCurrentIndex(0)

    def abrir_cad_adm(self):
        self.QtStack.setCurrentIndex(2)

    def cleaning_registration_adm_fields(self):
        self.tela_cad_adm.cadastro_lineEdit_email.setText('')
        self.tela_cad_adm.cadastro_lineEdit_nome.setText('')
        self.tela_cad_adm.cadastro_lineEdit_senha.setText('')
        self.tela_cad_adm.cadastro_lineEdit_conf_senha.setText('')

    def botao_cadastro_adm(self):
        email_adm    = self.tela_cad_adm.cadastro_lineEdit_email.text()
        nome_adm     = self.tela_cad_adm.cadastro_lineEdit_nome.text()
        senha_adm    = self.tela_cad_adm.cadastro_lineEdit_senha.text()
        confir_senha = self.tela_cad_adm.cadastro_lineEdit_conf_senha.text()
        if(email_adm != ''and nome_adm != '' and senha_adm != '' and confir_senha != ''):
            
            url = "http://127.0.0.1:8000/busca_mng"
            new_mng = {
                'email': 'email_adm',
            }
            response = requests.get(url, params=new_mng).json()
            print('response:',response)
            checking_email = response["mensagem"].split(':')[0] == "Error"
            if(checking_email):
                checking_password = senha_adm == confir_senha
                if checking_password:
                    self.cleaning_registration_adm_fields()

                    url = "http://127.0.0.1:8000/cad_mng"

                    new_mng = {
                        'email': email_adm,
                        'nome': nome_adm,
                        'senha': bcrypt.hashpw(senha_adm.encode('UTF-8'), bcrypt.gensalt(10)),
                    }
                    response = requests.get(url, params=new_mng).json()

                    checking_cad = response["mensagem"].split(':')[0] == "Error"
                    if checking_cad:
                        QMessageBox.information(None, 'Cadastro do Administrador', 'Esse endereço de email já está em uso.')
                    else:
                        QMessageBox.information(None, 'Cadastro do Administrador', 'Cadastro feito com sucesso.')
                        self.cleaning_registration_adm_fields()
                        self.abrir_login_adm()
                else:
                    self.cleaning_registration_adm_fields()
                    QMessageBox.information(None, 'Cadastro do Administrador', 'Confirmação de senha não confere.')
            else:
                self.cleaning_registration_adm_fields()
                QMessageBox.information(None, 'Cadastro do Administrador', 'Esse endereço de email já está em uso.')
        else:
            self.cleaning_registration_adm_fields()
            QMessageBox.information(None, 'Cadastro do Administrador', 'Todos os campos devem ser preenchidos.')

    def cleaning_login_adm_fields(self):
        self.tela_login_adm.login_lineEdit_email.setText('')
        self.tela_login_adm.login_lineEdit_senha.setText('')

    def abrir_menu_inicial(self):
        # buscar todos os registros de meta dados
        url = "http://127.0.0.1:8000/retorna_todos_pacientes"
        response = requests.get(url).json()
        print(response)
        # atualizar a tabela
        row = 0
        self.tela_menu_inicial.indiv_cadastrados_tableWidget.setRowCount(len(response.keys())-1)
        for key in response.keys():
            print("Aqui:",key)
            if key != 'mensagem':
                self.tela_menu_inicial.indiv_cadastrados_tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(response[key]['email_mng']))
                self.tela_menu_inicial.indiv_cadastrados_tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(response[key]['id_paciente']))

                if response[key]['predicao'] == '0':
                    _class = 'Negativo'
                    confidence = f'{response[key]["confianca"].split(" ")[0][3:5]}%'
                elif response[key]['predicao'] == '1':
                    _class = 'Positivo'
                    confidence = f'{response[key]["confianca"].split(" ")[1][2:4]}%'
                else:
                    _class = 'Indefinido'
                    confidence = f'{response[key]["confianca"].split(" ")[2][2:4]}%'

                self.tela_menu_inicial.indiv_cadastrados_tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(_class))
                self.tela_menu_inicial.indiv_cadastrados_tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(confidence))
                self.tela_menu_inicial.indiv_cadastrados_tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(response[key]['data']))
                self.tela_menu_inicial.indiv_cadastrados_tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(response[key]['hora']))
                row += 1

        self.QtStack.setCurrentIndex(3)

    def botao_login(self):
        email_adm = self.tela_login_adm.login_lineEdit_email.text()
        senha_adm = self.tela_login_adm.login_lineEdit_senha.text()
        if email_adm != '' and senha_adm != '':
            hashpasswd = senha_adm
            # realizar a busca de um mng
            url = "http://127.0.0.1:8000/login_mng"
            login = {
                'email': email_adm,
                'senha': hashpasswd,
            }
            response = requests.get(url, params=login).json()
            checking_email = response["mensagem"].split(':')[0] == "Error"
            if(checking_email):
                self.cleaning_login_adm_fields()
                QMessageBox.information(None, 'Login do Administrador', 'Conta não encontrada.')
            else:
                self._adm = response
                self.cleaning_login_adm_fields()
                QMessageBox.information(None, 'Login do Administrador', 'Bem vindo {}.'.format(self._adm['Nome']))
                # self.inicializando_tela__inicial()
                # Abrir tela inical
                self.abrir_menu_inicial()
                self.tela_menu_inicial.nome_adm.setText('{}'.format(self._adm['Nome']))
        else:
            QMessageBox.information(None, 'Login do Administrador', 'Todos os campos devem ser preenchidos.')

    def abrir_update_data(self):
        self.QtStack.setCurrentIndex(4)

    def abrir_show_data(self):
        self.QtStack.setCurrentIndex(5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main=Main()
    sys.exit(app.exec_())

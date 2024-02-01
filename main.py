import sys
from PyQt6.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QMainWindow, QLabel, QPushButton, QComboBox, QWidget
from PyQt6.QtGui import QPixmap, QIcon, QIntValidator
import draw_routes
from nearest_neightboor import Constructive
import json
from sa import SA

route = [[{"x": 78, "y": 571, "label": "Base 1"}, {"index": 8, "x": 597, "y": 598, "punctuation": 20, "time_needed": 8, "factor": 4, "label": "Movie Set"}, {"x": 1125, "y": 571, "label": "Base 2"}]]



# constructive.nearest_neightboor()

# draw_routes.generate_routes_images(route, 1.9265625, 2.0055)

def save_json_to_file(dictionary, file_name):
    with open(file_name, 'w') as file:
        json.dump(dictionary, file, indent=4)

class SettingsWindow(QWidget):
    def __init__(self, configuration = {}, file = ""):
        super().__init__()

        self.configuration = configuration
        self.mission_index = 0
        

        self.setGeometry(300, 300, 800, 594)
        self.setWindowTitle("Configurações")
        self.setStyleSheet("background-color: #ffffff;")
        self.setWindowIcon(QIcon('delta_logo.ico'))



        logo_label = QLabel(self)
        logo_pixmap = QPixmap("delta_logo.png").scaled(100, 100)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setGeometry(10, 10, 100, 100)

        # Criar QLabel "Runs" e definir sua posição usando setGeometry
        
        

        

        self.save_button = QPushButton("Salvar", self)
        style_sheet = """
            QPushButton {
                background-color: #0345fc;
                border: none;
                color: white;
                font-weight: bold;
            }
        """
        self.save_button.setStyleSheet(style_sheet)
        self.save_button.setGeometry(325, 530, 150, 30)
        self.save_button.clicked.connect(self.save_settings)

        runs_label = QLabel("Saídas", self)
        runs_label.setGeometry(10, 115, 50, 30)

        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(60, 115, 50, 30)
        self.text_input.setText(str(self.configuration["runs"]))
        self.text_input.textChanged.connect(self.on_runs_changed)
        runs_validator = QIntValidator()
        self.text_input.setValidator(runs_validator)

        max_time_label = QLabel("Tempo máximo", self)
        max_time_label.setGeometry(115, 115, 100, 30)


        self.max_time_input = QLineEdit(self)
        self.max_time_input.setGeometry(205, 115, 50, 30)
        self.max_time_input.setText(str(self.configuration["max_time"]))
        self.max_time_input.setValidator(QIntValidator())
        self.max_time_input.textChanged.connect(self.on_max_time_changed)


        max_complexity = QLabel("Complexidade máxima", self)
        max_complexity.setGeometry(265, 115, 140, 30)


        self.max_complexity_input = QLineEdit(self)
        self.max_complexity_input.setGeometry(405, 115, 50, 30)
        self.max_complexity_input.setValidator(QIntValidator())
        self.max_complexity_input.setText(str(self.configuration["max_complexity"]))
        self.max_complexity_input.textChanged.connect(self.on_complexity_changed)

        WeightsTitle = QLabel("Missões", self)
        WeightsTitle.setGeometry(10, 160, 100, 30)

        # Modificação do stylesheet
        WeightsTitle.setStyleSheet("color: black; font-weight: bold; font-size: 25px;")

        select_mission = QLabel("Selecionar Missão: ", self)
        select_mission.setGeometry(10, 200, 100, 30)

        

        combo_box = QComboBox(self)
        combo_box.setStyleSheet(
            "QComboBox { border: 1px solid #666; }"  # Define a borda cinza ao redor do seletor
            "QComboBox::drop-down { border: none; }"  # Remove a borda do seletor
        )
        
        for key in configuration["positions"]:
            combo_box.addItem(key["label"])

        combo_box.setGeometry(150, 200, 100, 30)

        combo_box.currentIndexChanged.connect(self.on_mission_change)

        mission_info = {"index": 0, "x": 3, "y": 266, "punctuation": 20, "time_needed": 2, "factor": 2, "label": "3D Cinema"}
        
        self.setup_mission_info(self.configuration["positions"][0])

        sa_label = QLabel("Configurações do Algoritmo", self)
        sa_label.setGeometry(10, 310, 350, 40)

        # Modificação do stylesheet
        sa_label.setStyleSheet("color: black; font-weight: bold; font-size: 25px;")

        sa_iterations = QLabel("Iterações: ", self)
        sa_iterations.setGeometry(10, 360, 60, 30)

        self.sa_iterations_edit = QLineEdit(self)
        self.sa_iterations_edit.setGeometry(70, 360, 50, 30)
        self.sa_iterations_edit.setText(str(self.configuration["simulated_anealing_configuration"]["parameters"]["iterations"]))
        self.sa_iterations_edit.textChanged.connect(self.on_sa_iterations_change)

        temperature = QLabel("Temperatura Inicial: ", self)
        temperature.setGeometry(130, 360, 100, 30)

        self.temperature_edit = QLineEdit(self)
        self.temperature_edit.setGeometry(240, 360, 50, 30)
        self.temperature_edit.setText(str(self.configuration["simulated_anealing_configuration"]["parameters"]["start_temperature"]))
        self.temperature_edit.textChanged.connect(self.on_sa_temperature_changed)

        decay_factor = QLabel("Fator de decaimento: ", self)
        decay_factor.setGeometry(300, 360, 150, 30)

        self.decay_factor_edit = QLineEdit(self)
        self.decay_factor_edit.setGeometry(450, 360, 50, 30)
        self.decay_factor_edit.setText(str(self.configuration["simulated_anealing_configuration"]["parameters"]["decay_factor"]))
        self.decay_factor_edit.textChanged.connect(self.on_decay_factor_changed)

        final_temperature = QLabel("Temperatura Final: ", self)
        final_temperature.setGeometry(10, 420, 110, 30)

        self.final_temperature_edit = QLineEdit(self)
        self.final_temperature_edit.setGeometry(130, 420, 50, 30)
        self.final_temperature_edit.setText(str(self.configuration["simulated_anealing_configuration"]["parameters"]["final_temperature"]))
        self.final_temperature_edit.textChanged.connect(self.on_final_temperature_change)

        pixmap = QPixmap(self.size())
        # Renderiza o conteúdo da janela na QPixmap
        self.render(pixmap)
        # Salva a QPixmap como uma imagem (formato PNG neste exemplo)
        pixmap.save("screenshot.png")
        self.file = file

        



    def save_settings(self):
        print("Salvando configurações")
        save_json_to_file(self.configuration, self.file)

    def on_sa_iterations_change(self):
        data = int(self.sa_iterations_edit.text())
        self.configuration["simulated_anealing_configuration"]["parameters"]["iterations"] = data

    def on_sa_temperature_changed(self):
        data = int(self.temperature_edit.text())
        self.configuration["simulated_anealing_configuration"]["parameters"]["start_temperature"] = data

    def on_decay_factor_changed(self):
        data = int(self.decay_factor_edit.text())
        self.configuration["simulated_anealing_configuration"]["parameters"]["decay_factor"] = data

    def on_final_temperature_change(self):
        data = int(self.final_temperature_edit.text())
        self.configuration["simulated_anealing_configuration"]["parameters"]["final_temperature"] = data


    def on_runs_changed(self):
        # Método chamado quando o texto no QLineEdit é alterado
        data = self.text_input.text()
        self.configuration["runs"] = int(data)
        # print(self.properties)

    def on_max_time_changed(self):
        data = self.max_time_input.text()
        self.configuration["max_time"] = int(data)

    def on_complexity_changed(self):
        data = self.max_complexity_input.text()
        self.configuration["max_complexity"] = int(data)

    def on_mission_change(self, index):
        self.mission_index = index
        self.change_mission_info(self.configuration["positions"][index])

    
    def change_mission_info(self, mission_info = {}):
        self.mission_position_label_x.setText("Posição x: " + str(mission_info['x']))
        self.mission_position_label_y.setText("Posição y: " + str(mission_info['y']))
        self.mission_position_label_punctuation.setText("Pontuação: " + str(mission_info['punctuation']))
        self.time_needed_edit.setText(str(mission_info['time_needed']))
        self.factor_edit.setText(str(mission_info['factor']))

    
    def on_factor_change(self):
        self.configuration["positions"][self.mission_index]["factor"] = int(self.factor_edit.text())

    def on_time_needed_change(self):
        self.configuration["positions"][self.mission_index]["time_needed"] = int(self.time_needed_edit.text())


    def setup_mission_info(self, mission_info = {}):
        self.mission_position_label_x = QLabel("Posição x: " + str(mission_info['x']), self)
        self.mission_position_label_x.setGeometry(10, 250, 100, 30)

        self.mission_position_label_y = QLabel("Posição y: " + str(mission_info['y']), self)
        self.mission_position_label_y.setGeometry(115, 250, 100, 30)

        self.mission_position_label_punctuation = QLabel("Pontuação: " + str(mission_info['punctuation']), self)
        self.mission_position_label_punctuation.setGeometry(215, 250, 100, 30)

        self.mission_label_time_needed = QLabel("Tempo necessário(segundos): ", self)
        self.mission_label_time_needed.setGeometry(335, 250, 160, 30)
    

        self.time_needed_edit = QLineEdit(self)
        self.time_needed_edit.setGeometry(500, 250, 50, 30)
        self.time_needed_edit.setText(str(mission_info['time_needed']))
        self.time_needed_edit.textChanged.connect(self.on_time_needed_change)


        self.mission_label_factor = QLabel("Fator de complexidade: ", self)
        self.mission_label_factor.setGeometry(560, 250, 190, 30)

        self.factor_edit = QLineEdit(self)
        self.factor_edit.setGeometry(690, 250, 50, 30)
        self.factor_edit.setText(str(mission_info['factor']))
        self.factor_edit.textChanged.connect(self.on_factor_change)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1660, 900)
        self.setWindowTitle("Delta FLL Optimizer Visualization")
        self.setStyleSheet("background-color: #ffffff;")

        self.label = QLabel(self)
        pixmap = QPixmap("routes1.jpg").scaled(1360, 900)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(300, 0, 1360, 900)

        logo_label = QLabel(self)
        logo_pixmap = QPixmap("delta_logo.png").scaled(100, 100)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setGeometry(100, 0, 100, 100)

        self.settings_button = QPushButton("Configurações", self)
        style_sheet = """
            QPushButton {
                background-color: #0345fc;
                border: none;
                color: white;
                font-weight: bold;
            }
        """

        style_sheet_2 = """
            QPushButton {
                background-color: #1ac447;
                border: none;
                color: white;
                font-weight: bold;
            }
        """

        

        self.settings_button.setStyleSheet(style_sheet)
        self.settings_button.setGeometry(75, 100, 150, 30)
        self.settings_button.clicked.connect(self.show_settings)

        
        self.execute_button = QPushButton("Executar", self)
        self.execute_button.setStyleSheet(style_sheet_2)
        self.execute_button.setGeometry(75, 150, 150, 30)
        self.execute_button.clicked.connect(self.execute)

        run_label = QLabel("Visualizar saída", self)
        run_label.setStyleSheet("font-size: 15px; font-weight: bold; text-align: center;")
        run_label.setGeometry(100, 190, 150, 30)

        pinout = ['Saida 1', 'Saida 2', 'Saida 3', 'Saida 4', 'Saida 5']

        layout = QVBoxLayout()
        layout.setSpacing(20)
        

        # Criar um botão para cada elemento na lista
        index = 0

        self.buttons = []
        for pin in pinout:
            button = QPushButton(pin, self)
            button.setGeometry(75, 240 + 45 * index, 150, 30)
            button.clicked.connect(lambda checked, idx=index: self.change_image(idx + 1))  # Conectar o sinal clicked à função
            if index != 0:
                button.setStyleSheet("background-color: #02b0fa ; border: 0px solid red;color: white; font-weight:bold;")
            else:
                button.setStyleSheet("background-color: #025375 ; border: 0px solid red;color: white; font-weight:bold;")

            self.buttons.append(button)
            index += 1

            
        self.constructive = Constructive(sys.argv[1])
        self.file = sys.argv[1]
        
        pixmap = QPixmap(self.size())
        # Renderiza o conteúdo da janela na QPixmap
        self.render(pixmap)
        # Salva a QPixmap como uma imagem (formato PNG neste exemplo)
        pixmap.save("screenshot_2.png")

        self.settings_window = None

    def show_settings(self):
        if not self.settings_window:
            self.settings_window = SettingsWindow(self.constructive.configuration, self.file)
        self.settings_window.show()

    def execute(self):
        print("Executing")
        route = self.constructive.nearest_neightboor()
        sa = SA(self.constructive.configuration["simulated_anealing_configuration"]["parameters"]["start_temperature"],
                self.constructive.configuration["simulated_anealing_configuration"]["parameters"]["final_temperature"],
                self.constructive.configuration["simulated_anealing_configuration"]["parameters"]["iterations"],
                self.constructive.configuration["simulated_anealing_configuration"]["parameters"]["decay_factor"])
        
        best_route = sa.execute(route)

        draw_routes.generate_routes_images(route.route, 1.9265625, 2.0055555555555555)
        pixmap = QPixmap("routes1.jpg").scaled(1360, 900)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(300, 0, 1360, 900)
        
    def change_image(self, image_number):
        image_path = f"routes{image_number}.jpg"
        pixmap = QPixmap(image_path).scaled(1360, 900)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(300, 0, 1360, 900)
        for i in range(len(self.buttons)):
            if i == image_number - 1:
                self.buttons[i].setStyleSheet("background-color: #025375 ; border: 0px solid red;color: white; font-weight:bold;")
            else:
                self.buttons[i].setStyleSheet("background-color: #02b0fa ; border: 0px solid red;color: white; font-weight:bold;")

def window():
    print(sys.argv)
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

window()

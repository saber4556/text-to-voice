import sys
import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QComboBox,
    QMessageBox,
    QLineEdit,
    QProgressBar,
    QHBoxLayout
)
from PyQt5.QtGui import QFont
from gtts import gTTS

class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text to Speech Converter")
        self.setGeometry(100, 100, 400, 400)
        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.language_combobox = QComboBox()
        self.populate_languages()
        self.layout.addWidget(self.language_combobox)

        self.output_path_layout = QHBoxLayout()
        self.output_path_label = QLabel("Output Path:")
        self.output_path_layout.addWidget(self.output_path_label)
        self.output_path_lineedit = QLineEdit()
        self.output_path_lineedit.setPlaceholderText("Select output path")
        self.output_path_layout.addWidget(self.output_path_lineedit)
        self.browse_output_button = QPushButton("Browse")
        self.browse_output_button.clicked.connect(self.browse_output_folder)
        self.output_path_layout.addWidget(self.browse_output_button)
        self.layout.addLayout(self.output_path_layout)

        self.browse_file_button = QPushButton("Browse File(s)")
        self.browse_file_button.clicked.connect(self.browse_text_files)
        self.layout.addWidget(self.browse_file_button)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_text_to_speech)
        self.layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)
        self.progress_bar.hide()

    def populate_languages(self):
        """تعبئة قائمة اختيار اللغة باللغات المدعومة."""
        languages = ['English', 'Spanish', 'French', 'Arabic', 'Chinese', 'Korean', 'Japanese']
        self.language_combobox.addItems(languages)

    def convert_text_to_speech(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            self.show_message_box("Error", "Please enter some text to convert.")
            return

        language_index = self.language_combobox.currentIndex()
        if language_index < 0:
            self.show_message_box("Error", "Please select a language.")
            return

        output_path = self.output_path_lineedit.text().strip()
        if not output_path:
            self.show_message_box("Error", "Please select output path.")
            return

        if not os.path.exists(output_path):
            self.show_message_box("Error", "Output path does not exist.")
            return

        try:
            self.progress_bar.show()
            self.progress_bar.setValue(0)

            language_code = self.get_language_code(language_index)

            paragraphs = [paragraph.strip() for paragraph in text.split('\n') if paragraph.strip()]
            full_text = ' '.join(paragraphs)

            # استخدام اسم الملف النصي الأصلي كاسم للملف الصوتي الناتج
            output_file_name = os.path.basename(self.current_file_path).split('.')[0]
            output_file_path = os.path.join(output_path, f"{output_file_name}.mp3")

            tts = gTTS(text=full_text, lang=language_code, slow=False)
            tts.save(output_file_path)

            self.progress_bar.setValue(100)
            self.show_message_box("Success", "Conversion completed successfully.")
        except Exception as e:
            self.show_message_box("Error", f"An error occurred: {str(e)}")
        finally:
            self.progress_bar.hide()

    def get_language_code(self, index):
        language_codes = {0: 'en', 1: 'es', 2: 'fr', 3: 'ar', 4: 'zh-cn', 5: 'ko', 6: 'ja'}
        return language_codes.get(index)

    def browse_output_folder(self):
        output_folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if output_folder_path:
            self.output_path_lineedit.setText(output_folder_path)

    def browse_text_files(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open Text Files", "", "Text files (*.txt)")
        if file_paths:
            self.current_file_path = file_paths[0]  
            for file_path in file_paths:
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    self.text_edit.append(text)  

    def show_message_box(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(10)
    app.setFont(font)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec_())

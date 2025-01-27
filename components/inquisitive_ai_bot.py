from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTextEdit, QPushButton, 
                            QHBoxLayout, QLabel, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
from openai import OpenAI
import json
from . import config  # Import the config file

class InquisitiveAIChatbot(QWidget):
    def __init__(self):
        super().__init__()
        self.client = OpenAI(
            api_key=config.api_key,  # Use API key from config
            base_url=config.base_url  # Use base URL from config
        )
        self.chat_history = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Add welcome header
        header = QLabel("🤖 Inquisitive AI Assistant")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        # Add subtitle
        subtitle = QLabel("Ask me anything about engineering, math, or programming!")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 15px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Create question box with title
        question_label = QLabel("🤔 Your Question:")
        question_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(question_label)
        
        self.question_box = QTextEdit()
        self.question_box.setPlaceholderText("Type your question here... (Press Ctrl+Enter to ask)")
        self.question_box.setMaximumHeight(100)
        self.question_box.keyPressEvent = self.handle_key_press
        layout.addWidget(self.question_box)

        # Create answer box with title
        answer_label = QLabel("💡 AI Response:")
        answer_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        layout.addWidget(answer_label)
        
        self.answer_box = QTextEdit()
        self.answer_box.setPlaceholderText("I'm excited to help! Ask me something above.")
        self.answer_box.setReadOnly(True)
        layout.addWidget(self.answer_box)

        # Create progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Create button layout
        button_layout = QHBoxLayout()

        # Create Ask button
        self.ask_button = QPushButton("🚀 Ask")
        self.ask_button.clicked.connect(self.ask_question)
        button_layout.addWidget(self.ask_button)

        # Create Reset button
        self.reset_button = QPushButton("🔄 Reset Chat")
        self.reset_button.clicked.connect(self.reset_chat)
        button_layout.addWidget(self.reset_button)

        # Add button layout
        layout.addLayout(button_layout)

        # Add tips label
        tips_label = QLabel("💡 Tip: Press Ctrl+Enter to quickly ask a question!")
        tips_label.setFont(QFont("Segoe UI", 8))
        tips_label.setStyleSheet("color: #95a5a6;")
        tips_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tips_label)

        self.setLayout(layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
            }
            QTextEdit {
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 8px;
                background-color: white;
                font-family: 'Segoe UI', Arial;
                font-size: 11pt;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTextEdit:focus {
                border-color: #2980b9;
            }
            QPushButton {
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                background-color: #3498db;
                color: white;
                font-family: 'Segoe UI', Arial;
                font-size: 10pt;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2475a7;
            }
            QLabel {
                font-family: 'Segoe UI', Arial;
            }
        """)

    def handle_key_press(self, event):
        # Check for Ctrl+Enter
        if event.key() == Qt.Key.Key_Return and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.ask_question()
        else:
            QTextEdit.keyPressEvent(self.question_box, event)

    def show_thinking_animation(self):
        self.progress_bar.show()
        self.progress_bar.setRange(0, 0)  # Infinite progress
        self.ask_button.setEnabled(False)
        self.question_box.setReadOnly(True)

    def hide_thinking_animation(self):
        self.progress_bar.hide()
        self.ask_button.setEnabled(True)
        self.question_box.setReadOnly(False)

    def ask_question(self):
        question = self.question_box.toPlainText()
        if question.strip():
            try:
                self.show_thinking_animation()
                self.answer_box.setText("🤔 Thinking...")
                
                # Add to chat history
                self.chat_history.append({"role": "user", "content": question})
                
                # Prepare messages with history
                messages = [
                    {"role": "system", "content": "You are a friendly and helpful assistant focused on engineering, mathematics, and programming concepts. You provide clear, concise answers with a touch of enthusiasm!"}
                ] + self.chat_history[-5:]  # Keep last 5 messages for context
                
                # Call DeepSeek API
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=messages,
                    stream=False
                )
                
                # Get and format the response
                answer = response.choices[0].message.content
                self.chat_history.append({"role": "assistant", "content": answer})
                
                # Format the display
                formatted_answer = f"🤖 {answer}"
                self.answer_box.setText(formatted_answer)
                
            except Exception as e:
                self.answer_box.setText(f"❌ Oops! Something went wrong:\n{str(e)}\nPlease try again.")
            
            finally:
                self.hide_thinking_animation()

    def reset_chat(self):
        self.question_box.clear()
        self.answer_box.clear()
        self.chat_history = []
        self.answer_box.setPlaceholderText("Chat history cleared! Ask me something new. 😊") 
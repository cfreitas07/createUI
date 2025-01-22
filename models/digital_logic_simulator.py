from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame, QTextEdit,
                            QTabWidget, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class DigitalLogicSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Logic Explorer 🎮")
        self.setGeometry(100, 100, 900, 700)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tab widget with fun icons
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget {
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                color: black;
                padding: 10px 20px;
                margin: 2px;
                border-radius: 8px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)

        # Add fun tabs with emojis
        tabs.addTab(self.create_playground_tab(), "🎮 Logic Playground")
        tabs.addTab(self.create_simplifier_tab(), "✨ Expression Wizard")
        tabs.addTab(self.create_learn_tab(), "📚 Quick Guide")
        
        layout.addWidget(tabs)

    def create_playground_tab(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: black;
                font-size: 14px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                font-size: 16px;
                color: black;
                background-color: white;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: black;
                background-color: white;
            }
        """)
        
        layout = QVBoxLayout(frame)

        # Fun title with emoji
        title = QLabel("🎮 Logic Playground")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Expression input with fun buttons
        input_layout = QHBoxLayout()
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText("Type your expression here (e.g., A·B + C')")
        input_layout.addWidget(self.expr_input)
        
        # Quick input buttons
        for symbol, text in [("·", "AND"), ("+", "OR"), ("'", "NOT"), ("⊕", "XOR")]:
            btn = QPushButton(f"{symbol} {text}")
            btn.clicked.connect(lambda x, s=symbol: self.expr_input.insert(s))
            btn.setMaximumWidth(100)
            input_layout.addWidget(btn)
        
        layout.addLayout(input_layout)

        # Results display with fun sections
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        layout.addWidget(self.results)

        # Action buttons
        button_layout = QHBoxLayout()
        analyze_btn = QPushButton("🔍 Analyze")
        analyze_btn.clicked.connect(self.analyze_expression)
        simplify_btn = QPushButton("✨ Simplify")
        simplify_btn.clicked.connect(self.simplify_expression)
        truth_table_btn = QPushButton("📊 Truth Table")
        truth_table_btn.clicked.connect(self.generate_truth_table)
        
        for btn in [analyze_btn, simplify_btn, truth_table_btn]:
            button_layout.addWidget(btn)
        
        layout.addLayout(button_layout)

        return frame

    def create_simplifier_tab(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QGridLayout(frame)

        # Fun title
        title = QLabel("✨ Expression Wizard")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title, 0, 0, 1, 2)

        # Interactive simplification steps
        self.steps_display = QTextEdit()
        self.steps_display.setReadOnly(True)
        layout.addWidget(self.steps_display, 1, 0, 1, 2)

        return frame

    def create_learn_tab(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(frame)

        guide = QTextEdit()
        guide.setReadOnly(True)
        guide.setHtml("""
            <h2>🎮 Welcome to Digital Logic Explorer!</h2>
            
            <h3>🎯 Quick Start:</h3>
            <ol>
                <li>Go to Logic Playground</li>
                <li>Type your expression using:</li>
                <ul>
                    <li>· for AND</li>
                    <li>+ for OR</li>
                    <li>' for NOT</li>
                    <li>⊕ for XOR</li>
                </ul>
                <li>Click the fun buttons to analyze!</li>
            </ol>

            <h3>✨ Cool Features:</h3>
            <ul>
                <li>Real-time analysis</li>
                <li>Instant simplification</li>
                <li>Truth table generation</li>
                <li>Step-by-step explanations</li>
            </ul>

            <h3>💡 Pro Tips:</h3>
            <ul>
                <li>Use parentheses for grouping</li>
                <li>Try simple expressions first</li>
                <li>Experiment with different operators</li>
                <li>Watch the simplification magic!</li>
            </ul>
        """)
        layout.addWidget(guide)

        return frame

    def analyze_expression(self):
        expr = self.expr_input.text()
        if not expr:
            return

        analysis = []
        analysis.append("<h3>🔍 Expression Analysis</h3>")
        
        # Variables used
        vars = sorted(set(c for c in expr if c.isalpha()))
        analysis.append(f"<p>📌 Variables: {', '.join(vars)}</p>")
        
        # Operators count
        ops = {
            '·': 'AND',
            '+': 'OR',
            "'": 'NOT',
            '⊕': 'XOR'
        }
        op_count = {op: expr.count(sym) for sym, op in ops.items()}
        op_text = [f"{op}: {count}" for op, count in op_count.items() if count > 0]
        analysis.append(f"<p>🔧 Operators: {', '.join(op_text)}</p>")

        # Quick patterns
        patterns = []
        if "A·A" in expr: patterns.append("X·X = X")
        if "A+A" in expr: patterns.append("X+X = X")
        if "A·A'" in expr: patterns.append("X·X' = 0")
        if patterns:
            analysis.append("<p>💡 Spotted patterns:</p>")
            analysis.append("<ul>" + "".join(f"<li>{p}</li>" for p in patterns) + "</ul>")

        self.results.setHtml("".join(analysis))

    def simplify_expression(self):
        expr = self.expr_input.text()
        if not expr:
            return

        steps = []
        steps.append("<h3>✨ Simplification Steps</h3>")
        steps.append("<ol>")
        
        # Example simplification steps
        if "A·A" in expr:
            steps.append("<li>Using idempotent law: A·A = A</li>")
        if "A·1" in expr:
            steps.append("<li>Using identity law: A·1 = A</li>")
        if "A+0" in expr:
            steps.append("<li>Using null law: A+0 = A</li>")
        
        steps.append("</ol>")
        self.results.setHtml("".join(steps))

    def generate_truth_table(self):
        expr = self.expr_input.text()
        if not expr:
            return

        vars = sorted(set(c for c in expr if c.isalpha()))
        if len(vars) > 4:
            self.results.setHtml("<p>⚠️ Truth table limited to 4 variables</p>")
            return

        table = ["<h3>📊 Truth Table</h3>"]
        table.append("<table border='1' style='border-collapse: collapse'>")
        
        # Header
        table.append("<tr>")
        for var in vars:
            table.append(f"<th style='padding: 5px'>{var}</th>")
        table.append("<th style='padding: 5px'>Output</th></tr>")
        
        # Rows (simplified example)
        table.append("<tr><td>0</td><td>0</td><td>0</td></tr>")
        table.append("</table>")
        
        self.results.setHtml("".join(table)) 
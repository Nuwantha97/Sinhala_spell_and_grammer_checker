from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QFrame, QGroupBox,
    QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QThreadPool
from PySide6.QtGui import QFont, QColor, QPalette
from api_client import APIWorker


class MainWindow(QMainWindow):
    """Main application window for Sinhala Spell and Grammar Checker"""
    
    # Signals for connecting to backend logic
    check_requested = Signal(str)  # Emits input text when check is requested
    clear_requested = Signal()      # Emits when clear is requested
    
    def __init__(self):
        super().__init__()
        self._setup_window()
        self._setup_styles()
        self._create_ui()
        self._center_window()
        
        # Initialize thread pool for API calls
        self.thread_pool = QThreadPool()
    
    def _setup_window(self):
        """Configure main window properties"""
        self.setWindowTitle("Sinhala Spell and Grammar Checker")
        self.setMinimumSize(700, 500)
        self.resize(900, 700)
    
    def _setup_styles(self):
        """Setup application styles and color palette"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QWidget {
                color: #eaeaea;
                font-family: 'Noto Sans Sinhala', 'Iskoola Pota', 'Nirmala UI', sans-serif;

            }
            QGroupBox {
                background-color: #16213e;
                border: 1px solid #2a3f5f;
                border-radius: 10px;
                margin-top: 15px;
                padding: 15px;
                font-size: 13px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
                color: #00d9ff;
            }
            QTextEdit {
                background-color: #0f0f23;
                border: 2px solid #2a3f5f;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #ffffff;
                selection-background-color: #00d9ff;
                selection-color: #000000;
            }
            QTextEdit:focus {
                border: 2px solid #00d9ff;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f3460, stop:1 #16537e);
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 14px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a4f7a, stop:1 #1e6a9c);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0a2540, stop:1 #0f3460);
            }
            QPushButton#checkButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b4d8, stop:1 #0077b6);
            }
            QPushButton#checkButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00c4e8, stop:1 #0087c6);
            }
            QPushButton#clearButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e63946, stop:1 #c1121f);
            }
            QPushButton#clearButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f64956, stop:1 #d1222f);
            }
            QLabel#titleLabel {
                color: #00d9ff;
                font-size: 28px;
                font-weight: bold;
                padding: 10px;
            }
            QLabel#subtitleLabel {
                color: #7f8c8d;
                font-size: 14px;
                padding-bottom: 10px;
            }
        """)
    
    def _create_ui(self):
        """Create the main UI layout"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)
        
        # Title section
        self._create_title_section(main_layout)
        
        # Input section
        self._create_input_section(main_layout)
        
        # Button section
        self._create_button_section(main_layout)
        
        # Result section
        self._create_result_section(main_layout)
    
    def _create_title_section(self, parent_layout):
        """Create the title and subtitle labels"""
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setAlignment(Qt.AlignCenter)
        title_layout.setSpacing(5)
        
        # Main title
        self.title_label = QLabel("📝 Sinhala Spell and Grammar Checker")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Enter Sinhala text below to check for spelling and grammar errors")
        self.subtitle_label.setObjectName("subtitleLabel")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.subtitle_label)
        
        parent_layout.addWidget(title_frame)
    
    def _create_input_section(self, parent_layout):
        """Create the input text area"""
        self.input_group = QGroupBox("Enter Text")
        input_layout = QVBoxLayout(self.input_group)
        
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Type or paste your Sinhala text here...")
        self.input_text.setMinimumHeight(150)
        self.input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        input_layout.addWidget(self.input_text)
        parent_layout.addWidget(self.input_group)
    
    def _create_button_section(self, parent_layout):
        """Create the action buttons"""
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(20)
        
        # Check button
        self.check_button = QPushButton("🔍 Check Spelling and Grammar")
        self.check_button.setObjectName("checkButton")
        self.check_button.setCursor(Qt.PointingHandCursor)
        self.check_button.clicked.connect(self._on_check_clicked)
        button_layout.addWidget(self.check_button)
        
        # Clear button
        self.clear_button = QPushButton("🗑️ Clear All")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.clicked.connect(self._on_clear_clicked)
        button_layout.addWidget(self.clear_button)
        
        parent_layout.addWidget(button_frame)
    
    def _create_result_section(self, parent_layout):
        """Create the result text area"""
        self.result_group = QGroupBox("Corrected Sentence")
        result_layout = QVBoxLayout(self.result_group)
        
        self.result_text = QTextEdit()
        self.result_text.setPlaceholderText("Results will appear here...")
        self.result_text.setMinimumHeight(150)
        self.result_text.setReadOnly(True)
        self.result_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        result_layout.addWidget(self.result_text)
        parent_layout.addWidget(self.result_group)
    
    def _center_window(self):
        """Center the window on the screen"""
        screen = self.screen().availableGeometry()
        window_size = self.geometry()
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        self.move(x, y)
    
    # --- Public Methods ---
    
    def get_input_text(self) -> str:
        """Get the current input text"""
        return self.input_text.toPlainText().strip()
    
    def set_result_text(self, text: str):
        """Set the result text area content"""
        self.result_text.setPlainText(text)
    
    def append_result_text(self, text: str):
        """Append text to the result area"""
        self.result_text.append(text)
    
    def clear_all(self):
        """Clear both input and result text areas"""
        self.input_text.clear()
        self.result_text.clear()
    
    def set_checking_state(self, is_checking: bool):
        """Update UI state during checking operation"""
        self.check_button.setEnabled(not is_checking)
        if is_checking:
            self.check_button.setText("⏳ Checking...")
        else:
            self.check_button.setText("🔍 Check Spelling and Grammar")
    
    def show_success_result(self, corrected_sentence: str, has_errors: bool = False, 
                           corrections: list = None):
        """Display the checking results in a formatted way"""
        self.result_text.clear()
        
        # Show corrected sentence
        self.result_text.append(corrected_sentence)
        self.result_text.append("")
        self.result_text.append("━" * 50)
        self.result_text.append("Grammar Check Results:")
        self.result_text.append("")
        
        if has_errors and corrections:
            self.result_text.append("Status: ⚠️ Grammatical errors found")
            self.result_text.append("")
            self.result_text.append("Corrections needed:")
            for error in corrections:
                word = error.get('word', '')
                correction = error.get('correction', '')
                self.result_text.append(f"  • '{word}' → '{correction}'")
        else:
            self.result_text.append("Status: ✓ No grammatical errors found")
    
    def show_error(self, title: str, message: str):
        """Display an error message in the result area"""
        self.result_text.clear()
        self.result_text.append(f"❌ {title}")
        self.result_text.append("")
        self.result_text.append(message)
    
    # --- Signal Handlers ---
    
    def _on_check_clicked(self):
        """Handle check button click"""
        input_text = self.get_input_text()
        if input_text:
            self.set_checking_state(True)
            
            # Create worker and connect signals
            worker = APIWorker(input_text)
            worker.signals.finished.connect(self._on_api_success)
            worker.signals.error.connect(self._on_api_error)
            
            # Run in thread pool
            self.thread_pool.start(worker)
        else:
            self.show_error("Input Error", "Please enter some text!")
    
    def _on_api_success(self, result: dict):
        """Handle successful API response"""
        self.set_checking_state(False)
        
        corrected_sentence = result.get("corrected_sentence", "")
        corrections = result.get("corrections", [])
        has_errors = len(corrections) > 0
        print(result, has_errors, corrections)
        self.show_success_result(corrected_sentence, has_errors, corrections)
    
    def _on_api_error(self, error_message: str):
        """Handle API error"""
        self.set_checking_state(False)
        self.show_error("Connection Error", error_message)
    
    def _on_clear_clicked(self):
        """Handle clear button click"""
        self.clear_all()
        self.clear_requested.emit()

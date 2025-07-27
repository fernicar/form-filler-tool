import sys
import os
import shutil
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QTabWidget, QSplitter, QMenuBar, QToolBar, QFileDialog,
    QMessageBox, QLabel, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QSizePolicy,
    QDialog, QDialogButtonBox, QFormLayout, QStyleFactory, QStatusBar, QGroupBox,
    QRadioButton, QCheckBox, QToolButton, QCommandLinkButton, QDateTimeEdit,
    QSlider, QScrollBar, QDial, QProgressBar, QGridLayout, QMenu, QInputDialog
)
from PySide6.QtGui import QAction, QKeySequence, QTextCursor, QShortcut
from PySide6.QtCore import Qt, Slot, QSize, QSettings, QFile, QTextStream, QDateTime, QTimer, QObject
APP_NAME = "Cool GUI Example"
APP_VERSION = "1.0"
SETTINGS_ORG = "ExampleOrg"
SETTINGS_APP = "CoolGUIExample"
DEFAULT_WINDOW_SIZE = QSize(1200, 800)
DEFAULT_FONT_SIZE = 11
RESOURCES_DIR = Path("resources")
DEFAULT_THEME_PATH = RESOURCES_DIR / "default_theme.qss"
STYLE_THEMES = ['windows11', 'windowsvista', 'Windows', 'Fusion']
STYLE_SELECTED_THEME = STYLE_THEMES[3]
COLOR_SCHEMES = ['Auto', 'Light', 'Dark']
DEFAULT_COLOR_SCHEME = COLOR_SCHEMES[0]
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(SETTINGS_ORG, SETTINGS_APP)
        if not RESOURCES_DIR.exists():
            RESOURCES_DIR.mkdir(parents=True)
        if not DEFAULT_THEME_PATH.exists():
            with open(DEFAULT_THEME_PATH, 'w', encoding='utf-8') as file:
                file.write('')
        self._init_ui()
        self._load_settings()
        self._apply_current_theme()
        self.app = QApplication.instance()
    def _init_ui(self):
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, DEFAULT_WINDOW_SIZE.width(), DEFAULT_WINDOW_SIZE.height())
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        view_menu = menu_bar.addMenu("&View")
        color_scheme_menu = view_menu.addMenu("&Color Scheme")
        self.color_scheme_actions = []
        auto_scheme_action = QAction("Auto", self)
        auto_scheme_action.setCheckable(True)
        auto_scheme_action.setData(0)
        auto_scheme_action.triggered.connect(self._on_color_scheme_selected)
        color_scheme_menu.addAction(auto_scheme_action)
        self.color_scheme_actions.append(auto_scheme_action)
        light_scheme_action = QAction("Light", self)
        light_scheme_action.setCheckable(True)
        light_scheme_action.setData(1)
        light_scheme_action.triggered.connect(self._on_color_scheme_selected)
        color_scheme_menu.addAction(light_scheme_action)
        self.color_scheme_actions.append(light_scheme_action)
        dark_scheme_action = QAction("Dark", self)
        dark_scheme_action.setCheckable(True)
        dark_scheme_action.setData(2)
        dark_scheme_action.triggered.connect(self._on_color_scheme_selected)
        color_scheme_menu.addAction(dark_scheme_action)
        self.color_scheme_actions.append(dark_scheme_action)
        theme_menu = view_menu.addMenu("&Theme")
        self.theme_actions = []
        load_qss_action = QAction("Load Custom QSS...", self)
        load_qss_action.triggered.connect(self._load_custom_qss)
        theme_menu.addAction(load_qss_action)
        theme_menu.addSeparator()
        default_fusion_action = QAction("Default Fusion Style", self)
        default_fusion_action.triggered.connect(self._apply_default_fusion_style)
        theme_menu.addAction(default_fusion_action)
        main_splitter_h = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(main_splitter_h, 1)
        example_widgets_layout = QHBoxLayout()
        main_layout.addLayout(example_widgets_layout)
        buttons_group_box = self._create_buttons_group_box()
        example_widgets_layout.addWidget(buttons_group_box)
        input_widgets_group_box = self._create_input_widgets_group_box()
        example_widgets_layout.addWidget(input_widgets_group_box)
        self.progress_bar = self._create_progress_bar()
        main_layout.addWidget(self.progress_bar)
        top_pane_widget = QWidget()
        top_pane_layout = QHBoxLayout(top_pane_widget)
        top_pane_layout.setContentsMargins(0, 0, 0, 0)
        display_splitter_v = QSplitter(Qt.Orientation.Horizontal)
        top_pane_layout.addWidget(display_splitter_v)
        main_splitter_h.addWidget(top_pane_widget)
        left_display_widget = QWidget()
        left_display_layout = QVBoxLayout(left_display_widget)
        story_label = QLabel("Content Display:")
        left_display_layout.addWidget(story_label)
        self.story_display = QTextEdit()
        self.story_display.setReadOnly(True)
        self.story_display.setPlaceholderText("Content will be displayed here")
        left_display_layout.addWidget(self.story_display)
        display_splitter_v.addWidget(left_display_widget)
        right_display_widget = QWidget()
        right_display_layout = QVBoxLayout(right_display_widget)
        self.monitor_tabs = QTabWidget()
        right_display_layout.addWidget(self.monitor_tabs)
        display_splitter_v.addWidget(right_display_widget)
        info_tab = QWidget()
        info_layout = QVBoxLayout(info_tab)
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setPlaceholderText("Information will be displayed here")
        info_layout.addWidget(self.info_display)
        self.monitor_tabs.addTab(info_tab, "Info")
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)
        self.settings_display = QTextEdit()
        self.settings_display.setReadOnly(True)
        self.settings_display.setPlaceholderText("Settings information will be displayed here")
        settings_layout.addWidget(self.settings_display)
        self.monitor_tabs.addTab(settings_tab, "Settings")
        bottom_pane_widget = QWidget()
        bottom_pane_layout = QVBoxLayout(bottom_pane_widget)
        bottom_pane_layout.setContentsMargins(0, 5, 0, 0)
        self.input_tabs = QTabWidget()
        bottom_pane_layout.addWidget(self.input_tabs)
        main_splitter_h.addWidget(bottom_pane_widget)
        main_input_tab = QWidget()
        main_input_layout = QVBoxLayout(main_input_tab)
        self.main_input = QTextEdit()
        self.main_input.setPlaceholderText("Type your input here...")
        main_input_layout.addWidget(self.main_input)
        main_input_buttons_layout = QHBoxLayout()
        send_button_main = QPushButton("Send")
        send_button_main.clicked.connect(self._handle_send)
        main_input_buttons_layout.addWidget(send_button_main)
        main_input_layout.addLayout(main_input_buttons_layout)
        self.input_tabs.addTab(main_input_tab, "Main Input")
        secondary_input_tab = QWidget()
        secondary_input_layout = QVBoxLayout(secondary_input_tab)
        self.secondary_input = QTextEdit()
        self.secondary_input.setPlaceholderText("Type your secondary input here...")
        secondary_input_layout.addWidget(self.secondary_input)
        secondary_input_buttons_layout = QHBoxLayout()
        send_button_secondary = QPushButton("Send")
        send_button_secondary.clicked.connect(self._handle_send)
        secondary_input_buttons_layout.addWidget(send_button_secondary)
        secondary_input_layout.addLayout(secondary_input_buttons_layout)
        self.input_tabs.addTab(secondary_input_tab, "Secondary Input")
        main_splitter_h.setSizes([int(self.height() * 0.65), int(self.height() * 0.35)])
        display_splitter_v.setSizes([int(self.width() * 0.6), int(self.width() * 0.4)])
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, toolbar)
        toolbar.addWidget(QLabel(" Style: "))
        self.style_selector = QComboBox()
        self.style_selector.addItems(STYLE_THEMES)
        self.style_selector.setCurrentText(STYLE_SELECTED_THEME)
        self.style_selector.setMinimumWidth(150)
        self.style_selector.currentTextChanged.connect(self._on_style_changed)
        toolbar.addWidget(self.style_selector)
        toolbar.addWidget(QLabel(" Temp: "))
        self.temp_spinbox = QDoubleSpinBox()
        self.temp_spinbox.setRange(0.0, 2.0)
        self.temp_spinbox.setSingleStep(0.1)
        self.temp_spinbox.setValue(0.7)
        toolbar.addWidget(self.temp_spinbox)
        toolbar.addWidget(QLabel(" Max Tokens: "))
        self.max_tokens_spinbox = QSpinBox()
        self.max_tokens_spinbox.setRange(50, 8192)
        self.max_tokens_spinbox.setSingleStep(10)
        self.max_tokens_spinbox.setValue(1024)
        toolbar.addWidget(self.max_tokens_spinbox)
        toolbar.addSeparator()
        toolbar.addWidget(QLabel(" Tag: "))
        self.xml_tag_input = QLineEdit()
        self.xml_tag_input.setPlaceholderText("e.g., <instruction>")
        self.xml_tag_input.setFixedWidth(120)
        toolbar.addWidget(self.xml_tag_input)
        toolbar.addSeparator()
        toolbar.addWidget(QLabel(" Font Size: "))
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(8, 24)
        self.font_size_spinbox.setValue(DEFAULT_FONT_SIZE)
        self.font_size_spinbox.valueChanged.connect(self._update_font_size)
        toolbar.addWidget(self.font_size_spinbox)
        self.theme_button = QPushButton("Dark Mode")
        self.theme_button.setCheckable(True)
        self.theme_button.toggled.connect(self._toggle_color_scheme)
        toolbar.addWidget(self.theme_button)
        toolbar.addSeparator()
        toolbar.addWidget(QLabel(" Sys Prompt: "))
        self.system_prompt_selector = QComboBox()
        self.system_prompt_selector.addItems(["Default", "Creative", "Technical"])
        self.system_prompt_selector.setMinimumWidth(150)
        toolbar.addWidget(self.system_prompt_selector)
        self.send_button = QPushButton("Send")
        self.send_button.setToolTip("Send input based on active tab")
        self.send_button.clicked.connect(self._handle_send)
        toolbar.addWidget(self.send_button)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        self._add_sample_content()
    def _add_sample_content(self):
        sample_text = """
This is a demonstration of a cool GUI implementation using PySide6.
- Color Scheme selection (Auto, Light, Dark) via View > Color Scheme menu
- Toggle between light and dark modes with the Dark Mode button
- Load custom QSS themes (experimental feature)
- Style selection via the Style dropdown
- Default Fusion style option in View > Theme menu
- Adjustable font size
- Tab-based input area
- Splitter for resizable panels
- Various example widgets (buttons, input fields, progress bar)
1. Try the Auto/Light/Dark options in the View > Color Scheme menu
2. Toggle between Light/Dark modes using the button in the toolbar
3. Try different Qt styles from the Style dropdown in the toolbar
4. Experiment with custom themes via View > Theme > Load Custom QSS (experimental)
5. Select "Default Fusion Style" from the View > Theme menu to reset
6. Experiment with the example widgets below
Note: The Auto/Light/Dark color schemes are the recommended way to handle theming. Custom QSS themes are experimental and may not work perfectly with all styles.
"""
        self.story_display.setMarkdown(sample_text)
        info_text = """
This panel displays information about the application.
- QMainWindow: Main application window
- QWidget: Container widgets
- QVBoxLayout/QHBoxLayout: Layout managers
- QSplitter: Resizable panel dividers
- QTabWidget: Tab containers
- QTextEdit: Text editing/display areas
- QPushButton: Action buttons
- QLabel: Text labels
- QSpinBox: Numeric input for font size
- QToolBar: Toolbar container
- QStatusBar: Status information
- QAction: Menu actions
- QGroupBox: Grouped widget container
- QRadioButton: Exclusive selection button
- QCheckBox: Checkable option button
- QToolButton: Compact button with menu support
- QCommandLinkButton: Vista-style link button
- QDateTimeEdit: Date and time editor
- QSlider: Sliding value selector
- QScrollBar: Scrolling control
- QDial: Rotary value control
- QProgressBar: Progress indicator
"""
        self.info_display.setMarkdown(info_text)
        settings_text = """
The application supports system color schemes via the View > Color Scheme menu:
- Auto: Uses the system default (light or dark based on OS settings)
- Light: Forces light mode
- Dark: Forces dark mode
The Dark Mode toggle button in the toolbar provides a quick way to switch between Light and Dark modes.
The application supports custom themes via QSS (Qt Style Sheets) as an experimental feature.
You can load custom QSS files via View > Theme > Load Custom QSS.
The theme files are stored in the 'resources' directory with names based on what you provide.
Note: Custom QSS themes may conflict with the system color schemes and might not work perfectly with all styles.
You can select different Qt styles from the Style dropdown in the toolbar.
The application uses the Fusion style by default, which provides a consistent look across platforms.
Select "Default Fusion Style" from the View > Theme menu to reset to the default Fusion style with Auto color scheme.
This is useful if you want to clear any custom themes and return to the default appearance.
"""
        self.settings_display.setMarkdown(settings_text)
    @Slot()
    def _handle_send(self):
        active_tab = self.input_tabs.currentWidget()
        if active_tab == self.input_tabs.widget(0):
            input_text = self.main_input.toPlainText()
            if input_text:
                self.story_display.append(f"\n\n**User Input:**\n{input_text}")
                self.main_input.clear()
                self.status_bar.showMessage("Message sent", 3000)
        elif active_tab == self.input_tabs.widget(1):
            input_text = self.secondary_input.toPlainText()
            if input_text:
                self.story_display.append(f"\n\n**Secondary Input:**\n{input_text}")
                self.secondary_input.clear()
                self.status_bar.showMessage("Secondary message sent", 3000)
    @Slot(int)
    def _update_font_size(self, size: int):
        font = self.font()
        font.setPointSize(size)
        widgets_to_update = [
            self.story_display,
            self.info_display,
            self.settings_display,
            self.main_input,
            self.secondary_input
        ]
        for widget in widgets_to_update:
            widget.setFont(font)
        self.settings.setValue("fontSize", size)
    @Slot(bool)
    def _toggle_color_scheme(self, checked: bool):
        app.setStyle(QStyleFactory.create(STYLE_SELECTED_THEME))
        self.style_selector.setCurrentText(STYLE_SELECTED_THEME)
        with open(DEFAULT_THEME_PATH, 'w', encoding='utf-8') as file:
            file.write('')
        app.setStyleSheet('')
        if checked:
            app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
            scheme_index = 2
            self.settings.setValue("colorScheme", scheme_index)
            self.theme_button.setText("Light Mode")
        else:
            app.styleHints().setColorScheme(Qt.ColorScheme.Light)
            scheme_index = 1
            self.settings.setValue("colorScheme", scheme_index)
            self.theme_button.setText("Dark Mode")
        for action in self.color_scheme_actions:
            action.setChecked(action.data() == scheme_index)
        for action in self.theme_actions:
            action.setChecked(False)
        scheme_name = COLOR_SCHEMES[scheme_index]
        self.status_bar.showMessage(f"{scheme_name} color scheme applied", 3000)
    def _apply_theme_from_file(self, theme_path: Path):
        if not theme_path.exists():
            QMessageBox.warning(self, "Theme Error", f"Theme file not found: {theme_path}")
            return False
        try:
            with open(theme_path, 'r', encoding='utf-8') as file:
                qss = file.read()
            app.setStyle(QStyleFactory.create(STYLE_SELECTED_THEME))
            app.setStyleSheet(qss)
            return True
        except Exception as e:
            QMessageBox.warning(self, "Theme Error", f"Error applying theme: {str(e)}")
            return False
    @Slot(bool)
    def _on_theme_selected(self, checked: bool):
        action = self.sender()
        if not isinstance(action, QAction) or not checked: return
        theme_type = action.data()
        if theme_type:
            for other_action in self.theme_actions:
                if other_action != action:
                    other_action.setChecked(False)
            for action in self.color_scheme_actions:
                action.setChecked(False)
            app.setStyle(QStyleFactory.create(STYLE_SELECTED_THEME))
            if theme_type == "dark":
                app.styleHints().setColorScheme(Qt.ColorScheme.Dark)
                self.theme_button.setText("Light Mode")
                self.theme_button.setChecked(True)
                self.settings.setValue("colorScheme", 2)
            else:
                app.styleHints().setColorScheme(Qt.ColorScheme.Light)
                self.theme_button.setText("Dark Mode")
                self.theme_button.setChecked(False)
                self.settings.setValue("colorScheme", 1)
    @Slot(str)
    def _on_style_changed(self, style_name: str):
        try:
            app.setStyle(QStyleFactory.create(style_name))
            global STYLE_SELECTED_THEME
            STYLE_SELECTED_THEME = style_name
            color_scheme = self.settings.value("colorScheme", 0, type=int)
            app.styleHints().setColorScheme(Qt.ColorScheme(color_scheme))
            self.status_bar.showMessage(f"{style_name} style applied", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Style Error", f"Error applying {style_name} style: {str(e)}")
    @Slot()
    def _apply_default_fusion_style(self):
        try:
            self.settings.setValue("customTheme", "")
            app.setStyle(QStyleFactory.create(STYLE_SELECTED_THEME))
            app.setStyleSheet('')
            self.status_bar.showMessage("Default Fusion style applied", 3000)
            for action in self.theme_actions:
                action.setChecked(False)
            self.style_selector.setCurrentText(STYLE_SELECTED_THEME)
            self._on_color_scheme_selected(True, force_index=0)
        except Exception as e:
            QMessageBox.warning(self, "Style Error", f"Error applying default style: {str(e)}")
    @Slot(bool)
    def _on_color_scheme_selected(self, checked: bool, force_index=None):
        if not checked and force_index is None:
            return
        if force_index is not None:
            scheme_index = force_index
        else:
            action = self.sender()
            if not isinstance(action, QAction): return
            scheme_index = action.data()
        for action in self.color_scheme_actions:
            action.setChecked(action.data() == scheme_index)
        app.styleHints().setColorScheme(Qt.ColorScheme(scheme_index))
        app.setStyleSheet('')
        self.settings.setValue("customTheme", "")
        self.settings.setValue("colorScheme", scheme_index)
        scheme_name = COLOR_SCHEMES[scheme_index]
        self.status_bar.showMessage(f"{scheme_name} color scheme applied", 3000)
        for action in self.theme_actions:
            action.setChecked(False)
        if scheme_index == 2:
            self.theme_button.setChecked(True)
            self.theme_button.setText("Light Mode")
        else:
            self.theme_button.setChecked(False)
            self.theme_button.setText("Dark Mode")
    @Slot()
    def _load_custom_qss(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Custom QSS Theme",
            str(RESOURCES_DIR),
            "QSS Files (*.qss);;All Files (*)"
        )
        if not file_path:
            return
        theme_name, ok = QInputDialog.getText(
            self,
            "Theme Name",
            "Enter a name for this theme (e.g., 'Blue Accent'):"
        )
        if not ok or not theme_name:
            theme_name = "custom"
        safe_name = "".join(c if c.isalnum() or c in "_- " else "_" for c in theme_name).lower()
        safe_name = safe_name.replace(" ", "_")
        new_theme_path = RESOURCES_DIR / f"{safe_name}_theme.qss"
        try:
            shutil.copy(file_path, new_theme_path)
            shutil.copy(file_path, DEFAULT_THEME_PATH)
            success = self._apply_theme_from_file(new_theme_path)
            if success:
                self.settings.setValue("customTheme", safe_name)
                for action in self.color_scheme_actions:
                    action.setChecked(False)
                self.status_bar.showMessage(f"Custom theme '{theme_name}' applied", 3000)
                theme_exists = False
                for action in self.theme_actions:
                    if action.text() == theme_name:
                        action.setChecked(True)
                        theme_exists = True
                        break
                if not theme_exists:
                    new_theme_action = QAction(theme_name, self)
                    new_theme_action.setCheckable(True)
                    new_theme_action.setData(safe_name)
                    new_theme_action.setChecked(True)
                    new_theme_action.triggered.connect(self._on_custom_theme_selected)
                    menu = self.theme_actions[0].parentWidget()
                    if menu:
                        menu.insertAction(self.theme_actions[-1], new_theme_action)
                        self.theme_actions.append(new_theme_action)
        except Exception as e:
            QMessageBox.warning(self, "Theme Error", f"Error loading custom theme: {str(e)}")
    @Slot(bool)
    def _on_custom_theme_selected(self, checked: bool):
        if not checked:
            return
        action = self.sender()
        if not isinstance(action, QAction): return
        theme_id = action.data()
        theme_path = RESOURCES_DIR / f"{theme_id}_theme.qss"
        if theme_path.exists():
            self.settings.setValue("customTheme", theme_id)
            self._apply_theme_from_file(theme_path)
            for other_action in self.theme_actions:
                if other_action != action:
                    other_action.setChecked(False)
            for scheme_action in self.color_scheme_actions:
                scheme_action.setChecked(False)
            self.status_bar.showMessage(f"Theme '{action.text()}' applied", 3000)
        else:
            QMessageBox.warning(self, "Theme Error", f"Theme file not found: {theme_path}")
            action.setChecked(False)
            self.settings.setValue("customTheme", "")
    def _create_buttons_group_box(self):
        group_box = QGroupBox("Buttons")
        group_box.setObjectName("buttonsGroupBox")
        default_push_button = QPushButton("Default Push Button")
        default_push_button.setDefault(True)
        toggle_push_button = QPushButton("Toggle Push Button")
        toggle_push_button.setCheckable(True)
        toggle_push_button.setChecked(True)
        flat_push_button = QPushButton("Flat Push Button")
        flat_push_button.setFlat(True)
        tool_button = QToolButton()
        tool_button.setText("Tool Button")
        menu_tool_button = QToolButton()
        menu_tool_button.setText("Menu Button")
        tool_menu = QMenu(menu_tool_button)
        menu_tool_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_menu.addAction("Option")
        tool_menu.addSeparator()
        action = tool_menu.addAction("Checkable Option")
        action.setCheckable(True)
        menu_tool_button.setMenu(tool_menu)
        tool_layout = QHBoxLayout()
        tool_layout.addWidget(tool_button)
        tool_layout.addWidget(menu_tool_button)
        command_link_button = QCommandLinkButton("Command Link Button")
        command_link_button.setDescription("Description")
        radio_button1 = QRadioButton("Radio button 1")
        radio_button2 = QRadioButton("Radio button 2")
        radio_button3 = QRadioButton("Radio button 3")
        radio_button1.setChecked(True)
        check_box = QCheckBox("Tri-state check box")
        check_box.setTristate(True)
        check_box.setCheckState(Qt.CheckState.PartiallyChecked)
        button_layout = QVBoxLayout()
        button_layout.addWidget(default_push_button)
        button_layout.addWidget(toggle_push_button)
        button_layout.addWidget(flat_push_button)
        button_layout.addLayout(tool_layout)
        button_layout.addWidget(command_link_button)
        button_layout.addStretch(1)
        checkable_layout = QVBoxLayout()
        checkable_layout.addWidget(radio_button1)
        checkable_layout.addWidget(radio_button2)
        checkable_layout.addWidget(radio_button3)
        checkable_layout.addWidget(check_box)
        checkable_layout.addStretch(1)
        main_layout = QHBoxLayout(group_box)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(checkable_layout)
        main_layout.addStretch()
        return group_box
    def _create_input_widgets_group_box(self):
        group_box = QGroupBox("Simple Input Widgets")
        group_box.setObjectName("inputWidgetsGroupBox")
        group_box.setCheckable(True)
        group_box.setChecked(True)
        line_edit = QLineEdit("s3cRe7")
        line_edit.setClearButtonEnabled(True)
        line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        spin_box = QSpinBox()
        spin_box.setValue(50)
        date_time_edit = QDateTimeEdit()
        date_time_edit.setDateTime(QDateTime.currentDateTime())
        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setValue(40)
        scroll_bar = QScrollBar()
        scroll_bar.setOrientation(Qt.Orientation.Horizontal)
        scroll_bar.setValue(60)
        dial = QDial()
        dial.setValue(30)
        dial.setNotchesVisible(True)
        layout = QGridLayout(group_box)
        layout.addWidget(line_edit, 0, 0, 1, 2)
        layout.addWidget(spin_box, 1, 0, 1, 2)
        layout.addWidget(date_time_edit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scroll_bar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        return group_box
    def _create_progress_bar(self):
        progress_bar = QProgressBar()
        progress_bar.setObjectName("progressBar")
        progress_bar.setRange(0, 10000)
        progress_bar.setValue(0)
        timer = QTimer(self)
        timer.timeout.connect(self._advance_progress_bar)
        timer.start(100)
        return progress_bar
    @Slot()
    def _advance_progress_bar(self):
        current_value = self.progress_bar.value()
        max_value = self.progress_bar.maximum()
        self.progress_bar.setValue(current_value + (max_value - current_value) // 100)
    def _apply_current_theme(self):
        color_scheme = self.settings.value("colorScheme", 0, type=int)
        self.style_selector.setCurrentText(STYLE_SELECTED_THEME)
        app.styleHints().setColorScheme(Qt.ColorScheme(color_scheme))
        app.setStyleSheet('')
        if not RESOURCES_DIR.exists():
            RESOURCES_DIR.mkdir(parents=True)
        with open(DEFAULT_THEME_PATH, 'w', encoding='utf-8') as file:
            file.write('')
        for action in self.color_scheme_actions:
            action.setChecked(action.data() == color_scheme)
        if color_scheme == 2:
            self.theme_button.setChecked(True)
            self.theme_button.setText("Light Mode")
        else:
            self.theme_button.setChecked(False)
            self.theme_button.setText("Dark Mode")
        custom_theme = self.settings.value("customTheme", "", type=str)
        if custom_theme:
            theme_path = RESOURCES_DIR / f"{custom_theme}_theme.qss"
            if theme_path.exists():
                self._apply_theme_from_file(theme_path)
                for action in self.theme_actions:
                    action.setChecked(action.data() == custom_theme)
    def _load_settings(self):
        font_size = self.settings.value("fontSize", DEFAULT_FONT_SIZE, type=int)
        if not isinstance(font_size, int): return
        self.font_size_spinbox.setValue(font_size)
        self._update_font_size(font_size)
    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName(SETTINGS_APP)
    app.setOrganizationName(SETTINGS_ORG)
    app.setStyle(QStyleFactory.create(STYLE_SELECTED_THEME))
    app.styleHints().setColorScheme(Qt.ColorScheme.Unknown)
    window = MainWindow()
    geometry = window.settings.value("geometry")
    if geometry:
        window.restoreGeometry(geometry)
    else:
        window.resize(DEFAULT_WINDOW_SIZE)
    window.show()
    sys.exit(app.exec())

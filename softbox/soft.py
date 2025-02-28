import sys
import re
import random
from PySide6.QtWidgets import (
    QWidget, QPushButton, QFrame, QApplication, 
    QMainWindow, QMenu, QVBoxLayout, QHBoxLayout, 
    QSizePolicy, QMessageBox, QSlider, QLabel,
    QComboBox, QGroupBox, QGridLayout, QTabWidget,
    QSplitter
)
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt, QTimer, Signal, QPropertyAnimation, QEasingCurve
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class ColorSlider(QWidget):
    """A custom widget that combines a slider with its label."""
    def __init__(self, label, value=255, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(f"{label} {value:03d}")
        self.label.setMinimumWidth(50)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 255)
        self.slider.setValue(value)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        
    def value(self):
        return self.slider.value()
    
    def setValue(self, value):
        self.slider.setValue(value)
        
    def update_label(self):
        self.label.setText(f"{self.label.text()[0]} {self.slider.value():03d}")


class SpeedSlider(QWidget):
    """A custom widget for controlling effect speed."""
    def __init__(self, label="Speed", min_value=50, max_value=1000, value=500, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.label = QLabel(f"{label}: {value}ms")
        self.label.setMinimumWidth(100)
        
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_value, max_value)
        self.slider.setValue(value)
        self.slider.valueChanged.connect(self._update_label)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
    
    def value(self):
        return self.slider.value()
    
    def setValue(self, value):
        self.slider.setValue(value)
        
    def _update_label(self):
        self.label.setText(f"Speed: {self.slider.value()}ms")


class ColorDisplay(QFrame):
    """Enhanced color display widget with animation capabilities."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Box)
        self.setMinimumHeight(180)
        self.color = QColor(255, 255, 255)
        self._effect_timer = QTimer(self)
        self._effect_timer.timeout.connect(self._update_effect)
        self._current_effect = "None"
        self._effect_colors = []
        self._effect_step = 0
        self._effect_base_color = QColor(255, 255, 255)
    
    def setColor(self, color):
        """Set a static color."""
        self.color = color
        self._effect_base_color = QColor(color)  # Store the base color for effects
        
        if self._current_effect == "None":
            self.setStyleSheet(f"background-color: {self.color.name()}")
    
    def _stop_effect(self):
        """Stop any running effect."""
        if self._effect_timer.isActive():
            self._effect_timer.stop()
        self._current_effect = "None"
        self.setStyleSheet(f"background-color: {self.color.name()}")
    
    def start_effect(self, effect_name, speed=500):
        """Start a lighting effect."""
        old_effect = self._current_effect
        self._stop_effect()
        
        if effect_name == "None":
            return
            
        self._current_effect = effect_name
        self._effect_step = 0
        
        # Setup effect-specific parameters
        if effect_name == "Strobe":
            self._effect_colors = [self._effect_base_color, QColor(0, 0, 0)]
        elif effect_name == "Police":
            self._effect_colors = [QColor(255, 0, 0), QColor(0, 0, 255)]
        elif effect_name == "Ambulance":
            self._effect_colors = [QColor(255, 0, 0), QColor(255, 255, 255)]
        elif effect_name == "Neon":
            self._effect_colors = [
                QColor(255, 0, 0), QColor(255, 165, 0), 
                QColor(255, 255, 0), QColor(0, 255, 0),
                QColor(0, 0, 255), QColor(75, 0, 130), 
                QColor(238, 130, 238)
            ]
        elif effect_name == "Sun":
            self._effect_colors = [QColor(255, 200, 0), QColor(255, 160, 0)]
        elif effect_name == "Moon":
            self._effect_colors = [QColor(200, 200, 255), QColor(160, 160, 200)]
        elif effect_name == "Custom":
            # Use the base color for custom effects
            self._effect_colors = [self._effect_base_color, QColor(max(0, self._effect_base_color.red()-100), 
                                                                 max(0, self._effect_base_color.green()-100), 
                                                                 max(0, self._effect_base_color.blue()-100))]
        
        # Start the effect timer
        self._effect_timer.setInterval(speed)
        self._effect_timer.start()
    
    def set_speed(self, speed):
        """Set the speed of the current effect."""
        if self._effect_timer.isActive():
            self._effect_timer.setInterval(speed)
    
    def _update_effect(self):
        """Update the visual state of the current effect."""
        if self._current_effect == "None":
            return
            
        if self._current_effect in ["Strobe", "Police", "Ambulance", "Custom"]:
            # Simple alternating effect
            color = self._effect_colors[self._effect_step % len(self._effect_colors)]
            self.setStyleSheet(f"background-color: {color.name()}")
            self._effect_step += 1
            
        elif self._current_effect == "Neon":
            # Smooth transition through colors
            color = self._effect_colors[self._effect_step % len(self._effect_colors)]
            self.setStyleSheet(f"background-color: {color.name()}")
            self._effect_step += 1
            
        elif self._current_effect == "Sun":
            # Pulsing effect
            intensity = abs(50 - (self._effect_step % 100)) / 50.0  # 0.0 to 1.0
            base_color = self._effect_colors[0]
            r = max(0, min(255, base_color.red() - int(40 * intensity)))
            g = max(0, min(255, base_color.green() - int(40 * intensity)))
            b = max(0, min(255, base_color.blue()))
            color = QColor(r, g, b)
            self.setStyleSheet(f"background-color: {color.name()}")
            self._effect_step += 1
            
        elif self._current_effect == "Moon":
            # Subtle glow effect
            intensity = abs(50 - (self._effect_step % 100)) / 50.0  # 0.0 to 1.0
            base_color = self._effect_colors[0]
            r = max(0, min(255, base_color.red() - int(30 * intensity)))
            g = max(0, min(255, base_color.green() - int(30 * intensity)))
            b = max(0, min(255, base_color.blue() - int(30 * intensity)))
            color = QColor(r, g, b)
            self.setStyleSheet(f"background-color: {color.name()}")
            self._effect_step += 1


class SoftBox(QMainWindow):
    """Main application window for color selection and light effects."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('SoftBox - Advanced Light Controller')
        self.setup_ui()
        
    def setup_ui(self):
        # Create the main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        main_layout = QVBoxLayout(self.main_widget)
        
        # Create the color display area
        self.color_display = ColorDisplay()
        main_layout.addWidget(self.color_display, 1)
        
        # Create splitter for controls
        self.control_splitter = QSplitter(Qt.Horizontal)
        self.control_splitter.setHandleWidth(6)
        self.control_splitter.setChildrenCollapsible(False)
        
        # Left side - RGB Color Control
        rgb_container = QWidget()
        rgb_layout = QVBoxLayout(rgb_container)
        rgb_layout.setContentsMargins(9, 9, 9, 9)  # Maintain proper margins
        
        rgb_group = QGroupBox("RGB Color Control")
        rgb_group_layout = QVBoxLayout(rgb_group)
        
        self.color = QColor(255, 255, 255)
        
        self.slider_r = ColorSlider("R", 255)
        self.slider_g = ColorSlider("G", 255)
        self.slider_b = ColorSlider("B", 255)
        
        # Connect signals
        self.slider_r.slider.valueChanged.connect(self.update_color)
        self.slider_g.slider.valueChanged.connect(self.update_color)
        self.slider_b.slider.valueChanged.connect(self.update_color)
        
        # Add the widgets to the layout
        rgb_group_layout.addWidget(self.slider_r)
        rgb_group_layout.addWidget(self.slider_g)
        rgb_group_layout.addWidget(self.slider_b)
        
        # Add the preset buttons
        presets_layout = QVBoxLayout()
        
        # Standard presets
        standard_presets_layout = QHBoxLayout()
        presets_label = QLabel("Standard Presets:")
        standard_presets_layout.addWidget(presets_label)
        
        self.preset_buttons = []
        standard_preset_colors = [
            ("White", QColor(255, 255, 255)),
            ("Red", QColor(255, 0, 0)),
            ("Green", QColor(0, 255, 0)),
            ("Blue", QColor(0, 0, 255)),
            ("Warm", QColor(255, 180, 100)),
            ("Cool", QColor(180, 200, 255))
        ]
        
        for name, color in standard_preset_colors:
            btn = QPushButton(name)
            btn.setStyleSheet(f"background-color: {color.name()}; color: {'black' if color.lightness() > 128 else 'white'}")
            btn.setFixedHeight(25)
            btn.clicked.connect(lambda checked=False, c=color: self.apply_preset(c))
            self.preset_buttons.append(btn)
            standard_presets_layout.addWidget(btn)
        
        presets_layout.addLayout(standard_presets_layout)
        
        # Designer presets
        designer_presets_layout = QHBoxLayout()
        designer_label = QLabel("Designer Colors:")
        designer_presets_layout.addWidget(designer_label)
        
        designer_preset_colors = [
            ("Prussian", QColor(0, 49, 83)),   # 普鲁士蓝
            ("Hermès", QColor(255, 88, 0)),    # 爱马仕橙色
            ("LV Brown", QColor(101, 67, 33)), # LV棕色
            ("Tiffany", QColor(0, 175, 152)),  # 蒂芙尼蓝
            ("Louboutin", QColor(224, 23, 58)) # 鲁布托红底色
        ]
        
        for name, color in designer_preset_colors:
            btn = QPushButton(name)
            btn.setStyleSheet(f"background-color: {color.name()}; color: {'black' if color.lightness() > 128 else 'white'}")
            btn.setFixedHeight(25)
            btn.clicked.connect(lambda checked=False, c=color: self.apply_preset(c))
            self.preset_buttons.append(btn)
            designer_presets_layout.addWidget(btn)
        
        presets_layout.addLayout(designer_presets_layout)
        
        rgb_group_layout.addLayout(presets_layout)
        
        rgb_group_layout.addLayout(presets_layout)
        rgb_layout.addWidget(rgb_group)
        
        # Right side - Light Effects
        effects_container = QWidget()
        effects_layout = QVBoxLayout(effects_container)
        effects_layout.setContentsMargins(9, 9, 9, 9)  # Maintain proper margins
        
        effects_group = QGroupBox("Light Effects")
        effects_group_layout = QVBoxLayout(effects_group)
        
        # Effect selection combo
        effect_selection_layout = QHBoxLayout()
        effect_label = QLabel("Effect:")
        self.effect_combo = QComboBox()
        self.effect_combo.addItems(["None", "Strobe", "Police", "Ambulance", 
                                   "Neon", "Sun", "Moon", "Custom"])
        self.effect_combo.currentTextChanged.connect(self.change_effect)
        
        effect_selection_layout.addWidget(effect_label)
        effect_selection_layout.addWidget(self.effect_combo)
        
        # Speed control
        self.speed_slider = SpeedSlider("Speed", 50, 1000, 500)
        self.speed_slider.slider.valueChanged.connect(self.update_speed)
        
        effects_group_layout.addLayout(effect_selection_layout)
        effects_group_layout.addWidget(self.speed_slider)
        
        # Effect quick buttons
        effects_buttons_layout = QGridLayout()
        effect_buttons = [
            ("Strobe", 0, 0), ("Police", 0, 1), 
            ("Ambulance", 1, 0), ("Neon", 1, 1),
            ("Sun", 2, 0), ("Moon", 2, 1)
        ]
        
        for name, row, col in effect_buttons:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked=False, effect=name: self.effect_combo.setCurrentText(effect))
            effects_buttons_layout.addWidget(btn, row, col)
        
        effects_group_layout.addLayout(effects_buttons_layout)
        effects_layout.addWidget(effects_group)
        
        # Add containers to splitter
        self.control_splitter.addWidget(rgb_container)
        self.control_splitter.addWidget(effects_container)
        
        # Set initial splitter sizes (equal width)
        self.control_splitter.setSizes([1, 1])
        
        # Add splitter to main layout
        main_layout.addWidget(self.control_splitter)
        
        # Set the initial color
        self.update_color()
        
        # Set a reasonable default size
        self.resize(650, 450)
        
    def update_color(self):
        """Update the UI when the RGB values change."""
        # Update color
        r = self.slider_r.value()
        g = self.slider_g.value()
        b = self.slider_b.value()
        
        # Update the color
        self.color.setRgb(r, g, b)
        
        # Update the labels
        self.slider_r.update_label()
        self.slider_g.update_label()
        self.slider_b.update_label()
        
        # Update the color display
        self.color_display.setColor(self.color)
        
        # If current effect is Custom, update it with new color
        if self.effect_combo.currentText() == "Custom":
            self.color_display.start_effect("Custom", self.speed_slider.value())
        
    def change_effect(self, effect_name):
        """Change the current light effect."""
        self.color_display.start_effect(effect_name, self.speed_slider.value())
    
    def update_speed(self):
        """Update the speed of the current effect."""
        self.color_display.set_speed(self.speed_slider.value())
        
    def apply_preset(self, color):
        """Apply a preset color."""
        self.slider_r.setValue(color.red())
        self.slider_g.setValue(color.green())
        self.slider_b.setValue(color.blue())
        self.update_color()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    window = SoftBox()
    window.show()
    return app.exec()


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
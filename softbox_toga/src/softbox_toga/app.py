"""
A tool for photographer to use screen as a light box
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.colors import rgb
import random
import threading
import time


class ColorSlider(toga.Box):
    """A custom widget that combines a slider with its label and direct input."""
    def __init__(self, label, value=255, min_value=0, max_value=255, on_change=None):
        super().__init__(style=Pack(direction=ROW, padding=(0, 0, 2, 0)))
        
        # Create label
        self.label_widget = toga.Label(
            label,
            style=Pack(width=15, padding=(0, 2))
        )
        
        # Create slider with correct parameter names and callbacks
        self.slider = toga.Slider(
            min=min_value,
            max=max_value,
            value=value,
            on_change=self._slider_changed,
            style=Pack(flex=1)
        )
        
        # Create numeric input with correct parameter names
        self.spin_box = toga.NumberInput(
            min=min_value,
            max=max_value,
            value=value,
            step=1,
            on_change=self._spinbox_changed,
            style=Pack(width=40)  # Reduced width
        )
        
        # Add widgets to layout
        self.add(self.label_widget)
        self.add(self.slider)
        self.add(self.spin_box)
        
        # Store the callback
        self.on_change_callback = on_change

    def value(self):
        return int(self.slider.value)
    
    def set_value(self, value):
        # Update both controls
        self.slider.value = value
        self.spin_box.value = value
    
    def _slider_changed(self, widget):
        # Update spin box when slider changes
        self.spin_box.value = int(self.slider.value)
        if self.on_change_callback:
            self.on_change_callback()
    
    def _spinbox_changed(self, widget):
        # Update slider when spin box changes
        try:
            value = int(self.spin_box.value)
            self.slider.value = value
            if self.on_change_callback:
                self.on_change_callback()
        except (ValueError, TypeError):
            pass


class SpeedSlider(toga.Box):
    """A custom widget for controlling effect speed with direct input."""
    def __init__(self, label="Speed", min_value=50, max_value=1000, value=500, on_change=None):
        super().__init__(style=Pack(direction=ROW, padding=(0, 0, 2, 0)))
        
        # Create label
        self.label_widget = toga.Label(
            f"{label}:",
            style=Pack(width=36, padding=(0, 2))
        )
        
        # Create slider with correct parameter names
        self.slider = toga.Slider(
            min=min_value,
            max=max_value,
            value=value,
            on_change=self._slider_changed,
            style=Pack(flex=1)
        )
        
        # Create numeric input with correct parameter names
        self.spin_box = toga.NumberInput(
            min=min_value,
            max=max_value,
            value=value,
            step=10,
            on_change=self._spinbox_changed,
            style=Pack(width=45)  # Reduced width
        )
        
        # Add widgets to layout
        self.add(self.label_widget)
        self.add(self.slider)
        self.add(self.spin_box)
        
        # Store the callback
        self.on_change_callback = on_change

    def value(self):
        return int(self.slider.value)
    
    def set_value(self, value):
        # Update both controls
        self.slider.value = value
        self.spin_box.value = value
    
    def _slider_changed(self, widget):
        # Update spin box when slider changes
        self.spin_box.value = int(self.slider.value)
        if self.on_change_callback:
            self.on_change_callback()
    
    def _spinbox_changed(self, widget):
        # Update slider when spin box changes
        try:
            value = int(self.spin_box.value)
            self.slider.value = value
            if self.on_change_callback:
                self.on_change_callback()
        except (ValueError, TypeError):
            pass


class ColorDisplay(toga.Box):
    """Color display widget with animation capabilities."""
    def __init__(self):
        # Use flex for scaling
        super().__init__(style=Pack(flex=1))
        
        # Set initial values
        self.color = rgb(255, 255, 255)
        self._effect_base_color = self.color
        self._current_effect = "None"
        self._effect_colors = []
        self._effect_step = 0
        self._effect_running = False
        self._effect_speed = 500
        
        # Apply initial background
        self.style.background_color = self.color
        
    def set_color(self, color):
        """Set a static color."""
        self.color = color
        self._effect_base_color = color
        
        if self._current_effect == "None":
            self.style.background_color = color

    def _stop_effect(self):
        """Stop any running effect."""
        self._effect_running = False
        self._current_effect = "None"
        self.style.background_color = self.color
    
    def start_effect(self, effect_name, speed=500):
        """Start a lighting effect."""
        # Stop previous effect
        old_effect = self._current_effect
        self._stop_effect()
        
        if effect_name == "None":
            return
            
        self._current_effect = effect_name
        self._effect_step = 0
        self._effect_speed = speed
        
        # Setup effect-specific parameters
        if effect_name == "Strobe":
            self._effect_colors = [self._effect_base_color, rgb(0, 0, 0)]
        elif effect_name == "Police":
            self._effect_colors = [rgb(255, 0, 0), rgb(0, 0, 255)]
        elif effect_name == "Ambulance":
            self._effect_colors = [rgb(255, 0, 0), rgb(255, 255, 255)]
        elif effect_name == "Neon":
            self._effect_colors = [
                rgb(255, 0, 0), rgb(255, 165, 0), 
                rgb(255, 255, 0), rgb(0, 255, 0),
                rgb(0, 0, 255), rgb(75, 0, 130), 
                rgb(238, 130, 238)
            ]
        elif effect_name == "Sun":
            self._effect_colors = [rgb(255, 200, 0), rgb(255, 160, 0)]
        elif effect_name == "Moon":
            self._effect_colors = [rgb(200, 200, 255), rgb(160, 160, 200)]
        elif effect_name == "Custom":
            # Use the base color for custom effects
            r, g, b = self._effect_base_color.r, self._effect_base_color.g, self._effect_base_color.b
            self._effect_colors = [
                self._effect_base_color, 
                rgb(max(0, r-100), max(0, g-100), max(0, b-100))
            ]
        
        # Start the effect in a background thread
        self._effect_running = True
        self._effect_thread = threading.Thread(target=self._run_effect)
        self._effect_thread.daemon = True
        self._effect_thread.start()
    
    def set_speed(self, speed):
        """Set the speed of the current effect."""
        self._effect_speed = speed
    
    def _run_effect(self):
        """Run the effect in a background thread."""
        while self._effect_running:
            self._update_effect()
            time.sleep(self._effect_speed / 1000)
    
    def _update_effect(self):
        """Update the visual state of the current effect."""
        if self._current_effect == "None" or not self._effect_running:
            return
            
        if self._current_effect in ["Strobe", "Police", "Ambulance", "Custom"]:
            # Simple alternating effect
            color = self._effect_colors[self._effect_step % len(self._effect_colors)]
            self._apply_color(color)
            self._effect_step += 1
            
        elif self._current_effect == "Neon":
            # Cycle through colors
            color = self._effect_colors[self._effect_step % len(self._effect_colors)]
            self._apply_color(color)
            self._effect_step += 1
            
        elif self._current_effect == "Sun":
            # Pulsing effect
            intensity = abs(50 - (self._effect_step % 100)) / 50.0  # 0.0 to 1.0
            base_color = self._effect_colors[0]
            r = max(0, min(255, base_color.r - int(40 * intensity)))
            g = max(0, min(255, base_color.g - int(40 * intensity)))
            b = max(0, min(255, base_color.b))
            self._apply_color(rgb(r, g, b))
            self._effect_step += 1
            
        elif self._current_effect == "Moon":
            # Subtle glow effect
            intensity = abs(50 - (self._effect_step % 100)) / 50.0  # 0.0 to 1.0
            base_color = self._effect_colors[0]
            r = max(0, min(255, base_color.r - int(30 * intensity)))
            g = max(0, min(255, base_color.g - int(30 * intensity)))
            b = max(0, min(255, base_color.b - int(30 * intensity)))
            self._apply_color(rgb(r, g, b))
            self._effect_step += 1
    
    def _apply_color(self, color):
        """Apply color to the display (thread-safe)."""
        # This needs to run on the main thread since it's updating the UI
        try:
            # Use the current app instance directly
            app = toga.App.app
            if app:
                # Fix: The lambda needs to accept an argument that Toga will pass
                app.add_background_task(lambda _: self._update_ui_sync(color))
        except Exception:
            pass
    
    def _update_ui_sync(self, color):
        """Update the UI with the new color (on main thread)."""
        try:
            self.style.background_color = color
            self.refresh()
        except Exception:
            # Handles possible widget disposal during operation
            pass


class ToggleButton(toga.Button):
    """Custom toggle button for control panel visibility."""
    def __init__(self, text, on_toggle=None):
        super().__init__(
            text="▼",
            on_press=self._on_press,
            style=Pack(width=20, height=20, padding=0)
        )
        self.is_open = True
        self.on_toggle_callback = on_toggle
        
    def _on_press(self, widget):
        self.is_open = not self.is_open
        # Update icon
        if self.is_open:
            self.text = "▼"  # Down arrow
        else:
            self.text = "▲"  # Up arrow
            
        if self.on_toggle_callback:
            self.on_toggle_callback(self.is_open)


class SoftBoxApp(toga.App):
    def startup(self):
        # Create main window
        self.main_window = toga.MainWindow(title="SoftBox - Advanced Light Controller")
        
        # Main container with vertical layout
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=2))
        
        # Color display - This will expand as window resizes
        self.color_display = ColorDisplay()
        color_display_container = toga.Box(style=Pack(flex=1))
        color_display_container.add(self.color_display)
        
        # Toggle button container (stays small)
        toggle_btn_container = toga.Box(style=Pack(direction=ROW, alignment='center', padding=(2, 0)))
        self.toggle_button = ToggleButton(text="▼", on_toggle=self.toggle_controls_visibility)
        toggle_btn_container.add(self.toggle_button)
        
        # Controls container with fixed max height
        self.controls_container = toga.Box(style=Pack(direction=COLUMN))
        
        # Create controls area with more compact layout
        controls_box = toga.Box(style=Pack(direction=COLUMN, padding=(2, 2)))
        
        # Top row containing both RGB controls and effect selection
        top_row = toga.Box(style=Pack(direction=ROW, padding=0))
        
        # RGB Controls (left side)
        rgb_controls = toga.Box(style=Pack(direction=COLUMN, padding=0, flex=1))
        
        # Create compact RGB sliders group
        rgb_sliders = toga.Box(style=Pack(direction=COLUMN, padding=0))
        self.slider_r = ColorSlider("R", 255, on_change=self.update_color)
        self.slider_g = ColorSlider("G", 255, on_change=self.update_color)
        self.slider_b = ColorSlider("B", 255, on_change=self.update_color)
        
        rgb_sliders.add(self.slider_r)
        rgb_sliders.add(self.slider_g)
        rgb_sliders.add(self.slider_b)
        rgb_controls.add(rgb_sliders)
        
        # Effects Controls (right side)
        effects_controls = toga.Box(style=Pack(direction=COLUMN, padding=0, flex=1))
        
        # Effect selection
        effect_selection = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 2, 0)))
        effect_label = toga.Label("Effect:", style=Pack(width=36, padding=(0, 2)))
        
        effect_items = ["None", "Strobe", "Police", "Ambulance", "Neon", "Sun", "Moon", "Custom"]
        self.effect_combo = toga.Selection(
            items=effect_items,
            on_change=self.change_effect,
            style=Pack(flex=1, height=25)
        )
        
        effect_selection.add(effect_label)
        effect_selection.add(self.effect_combo)
        effects_controls.add(effect_selection)
        
        # Speed control
        self.speed_slider = SpeedSlider("Speed", 50, 1000, 500, on_change=self.update_speed)
        effects_controls.add(self.speed_slider)
        
        # Add both control sections to the top row
        top_row.add(rgb_controls)
        top_row.add(effects_controls)
        controls_box.add(top_row)
        
        # Bottom row with all buttons in a more compact layout
        buttons_box = toga.Box(style=Pack(direction=ROW, padding=(2, 0, 0, 0)))
        
        # Left side - Standard colors
        std_colors = toga.Box(style=Pack(direction=COLUMN, padding=0, flex=1))
        
        # Standard color buttons - 3x2 grid
        std_presets = [
            ("White", rgb(255, 255, 255)), ("Red", rgb(255, 0, 0)), ("Green", rgb(0, 255, 0)),
            ("Blue", rgb(0, 0, 255)), ("Warm", rgb(255, 180, 100)), ("Cool", rgb(180, 200, 255))
        ]
        
        std_grid = toga.Box(style=Pack(direction=COLUMN, padding=0))
        std_row1 = toga.Box(style=Pack(direction=ROW, padding=0))
        std_row2 = toga.Box(style=Pack(direction=ROW, padding=0))
        
        for i, (name, color) in enumerate(std_presets):
            btn = toga.Button(
                name, 
                on_press=self.create_preset_handler(color),
                style=Pack(flex=1, padding=1, height=22, width=50)
            )
            if i < 3:
                std_row1.add(btn)
            else:
                std_row2.add(btn)
        
        std_grid.add(std_row1)
        std_grid.add(std_row2)
        std_colors.add(std_grid)
        
        # Middle - Designer colors
        designer_colors = toga.Box(style=Pack(direction=COLUMN, padding=0, flex=1))
        
        # Designer color buttons - More compact grid layout
        designer_presets = [
            ("Prussian", rgb(0, 49, 83)), ("Hermès", rgb(255, 88, 0)), 
            ("LV Brown", rgb(101, 67, 33)), ("Tiffany", rgb(0, 175, 152)),
            ("Louboutin", rgb(224, 23, 58))
        ]
        
        designer_grid = toga.Box(style=Pack(direction=COLUMN, padding=0))
        designer_row1 = toga.Box(style=Pack(direction=ROW, padding=0))
        designer_row2 = toga.Box(style=Pack(direction=ROW, padding=0))
        
        for i, (name, color) in enumerate(designer_presets):
            btn = toga.Button(
                name,
                on_press=self.create_preset_handler(color),
                style=Pack(flex=1, padding=1, height=22, width=50)
            )
            if i < 3:
                designer_row1.add(btn)
            elif i < 5:
                designer_row2.add(btn)
        
        # Add one empty space to balance the row
        if len(designer_presets) % 3 != 0:
            empty_space = toga.Box(style=Pack(flex=1))
            designer_row2.add(empty_space)
            
        designer_grid.add(designer_row1)
        designer_grid.add(designer_row2)
        designer_colors.add(designer_grid)
        
        # Right side - Effect buttons
        effect_buttons_container = toga.Box(style=Pack(direction=COLUMN, padding=0, flex=1))
        
        # Effect buttons - Compact grid layout
        effect_buttons = [
            ("Strobe", "Strobe"), ("Police", "Police"), ("Ambulance", "Ambulance"),
            ("Neon", "Neon"), ("Sun", "Sun"), ("Moon", "Moon")
        ]
        
        effects_grid = toga.Box(style=Pack(direction=COLUMN, padding=0))
        effects_row1 = toga.Box(style=Pack(direction=ROW, padding=0))
        effects_row2 = toga.Box(style=Pack(direction=ROW, padding=0))
        
        for i, (name, effect) in enumerate(effect_buttons):
            btn = toga.Button(
                name,
                on_press=self.create_effect_handler(effect),
                style=Pack(flex=1, padding=1, height=22, width=50)
            )
            if i < 3:
                effects_row1.add(btn)
            else:
                effects_row2.add(btn)
        
        effects_grid.add(effects_row1)
        effects_grid.add(effects_row2)
        effect_buttons_container.add(effects_grid)
        
        # Add all button sections to the bottom row
        buttons_box.add(std_colors)
        buttons_box.add(designer_colors)
        buttons_box.add(effect_buttons_container)
        
        # Add bottom row to controls
        controls_box.add(buttons_box)
        
        # Add controls box to the container
        self.controls_container.add(controls_box)
        
        # Build the main UI
        main_box.add(color_display_container)
        main_box.add(toggle_btn_container)
        main_box.add(self.controls_container)
        
        # Set up the main window
        self.main_window.content = main_box
        self.main_window.size = (650, 400)  # Made overall window smaller
        self.main_window.show()
        
        # Set initial color
        self.update_color()
    
    def toggle_controls_visibility(self, is_visible):
        """Toggle the visibility of control panels."""
        if is_visible:
            # Show controls
            self.controls_container.style.display = "pack"
            self.controls_container.refresh()
        else:
            # Hide controls
            self.controls_container.style.display = "none"
            self.controls_container.refresh()
    
    def create_preset_handler(self, color):
        """Create a handler for preset color buttons."""
        def handler(widget):
            self.apply_preset(color)
        return handler
        
    def create_effect_handler(self, effect):
        """Create a handler for effect buttons."""
        def handler(widget):
            self.effect_combo.value = effect
            self.change_effect(self.effect_combo)
        return handler
    
    def update_color(self):
        """Update the UI when RGB values change."""
        # Get RGB values
        r = self.slider_r.value()
        g = self.slider_g.value()
        b = self.slider_b.value()
        
        # Update color
        self.color = rgb(r, g, b)
        
        # Update color display
        self.color_display.set_color(self.color)
        
        # If current effect is Custom, update it with new color
        if hasattr(self.effect_combo, 'value') and self.effect_combo.value == "Custom":
            self.color_display.start_effect("Custom", self.speed_slider.value())
    
    def change_effect(self, widget):
        """Change the current light effect."""
        if hasattr(widget, 'value') and widget.value:  # Check if attribute exists and has a value
            self.color_display.start_effect(widget.value, self.speed_slider.value())
    
    def update_speed(self):
        """Update the speed of the current effect."""
        self.color_display.set_speed(self.speed_slider.value())
    
    def apply_preset(self, color):
        """Apply a preset color."""
        # Fix: Access the RGB components using properties
        self.slider_r.set_value(color.r)
        self.slider_g.set_value(color.g)
        self.slider_b.set_value(color.b)
        self.update_color()


def main():
    # Use app_id as keyword argument
    return SoftBoxApp(app_id='org.example.softbox', formal_name="SoftBox")

if __name__ == '__main__':
    app = main()
    app.main_loop()
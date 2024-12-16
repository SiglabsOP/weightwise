from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QCalendarWidget, QLineEdit, QMessageBox, QDialog, QRadioButton, QFormLayout, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDate
import sys
import os
import json
from PyQt5.QtWidgets import QMessageBox, QTextBrowser

DATA_FILE = "weight_data.json"

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QPushButton, QGroupBox, QRadioButton
from PyQt5.QtGui import QIcon

class WaterRetentionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Estimate Water Retention")
        self.setGeometry(150, 150, 400, 250)
        self.setWindowIcon(QIcon("logo.ico"))

        self.water_retention_factor = 1.0  # Default to 1.0 (no extra retention)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Salt intake
        salt_group = self.create_radio_group("Do you consume a lot of salt?", ["Low", "Medium", "High"])
        form_layout.addRow(salt_group)

        # Carbohydrates intake
        carb_group = self.create_radio_group("Do you consume a lot of carbs?", ["Low", "Medium", "High"])
        form_layout.addRow(carb_group)

        # Exercise activity level
        exercise_group = self.create_radio_group("How active are you physically?", ["Sedentary", "Moderate", "Very Active"])
        form_layout.addRow(exercise_group)

        # Submit Button
        submit_button = QPushButton("Estimate Water Retention")
        submit_button.clicked.connect(self.estimate_water_retention)
        
        layout.addLayout(form_layout)
        layout.addWidget(submit_button)
        
        self.setLayout(layout)

    def create_radio_group(self, title, options):
        """Helper function to create a group of radio buttons."""
        group = QGroupBox(title)
        layout = QVBoxLayout()
        
        for option in options:
            radio_button = QRadioButton(option)
            layout.addWidget(radio_button)
        
        group.setLayout(layout)
        return group

    def estimate_water_retention(self):
        """Estimate water retention based on user input."""
        
        salt_factor = self.get_radio_button_value("Do you consume a lot of salt?", ["Low", "Medium", "High"])
        carb_factor = self.get_radio_button_value("Do you consume a lot of carbs?", ["Low", "Medium", "High"])
        exercise_factor = self.get_radio_button_value("How active are you physically?", ["Sedentary", "Moderate", "Very Active"])

        # Improved weighted average to calculate water retention factor
        salt_weight = salt_factor * 0.4  # Low: 0.0, Medium: 0.2, High: 0.4
        carb_weight = carb_factor * 0.3   # Low: 0.0, Medium: 0.15, High: 0.3
        exercise_weight = (1 - exercise_factor) * 0.3  # Sedentary: 0.3, Moderate: 0.15, Very Active: 0.0

        # Calculate new water retention factor with adjusted weights
        self.water_retention_factor = max(1.0 + (salt_weight + carb_weight - exercise_weight), 1.0) 
        
        self.accept()

    def get_radio_button_value(self, group_name, options):
        """Helper function to get the value based on selected radio button."""
        
        group = self.findChildren(QGroupBox)
        
        for g in group:
            if g.title() == group_name:
                selected_button = [button for button in g.findChildren(QRadioButton) if button.isChecked()]
                
                if selected_button:
                    return options.index(selected_button[0].text()) / 2  # Low = 0, Medium = 0.5, High = 1

        return 0  # Default to 0 if no selection is made


class WeightTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WeightWise v2.0")
        self.setGeometry(100, 100, 600, 500)
        self.setWindowIcon(QIcon("logo.ico"))

        self.weight_data = self.load_data()

        if "target_weight" not in self.weight_data or "water_retention" not in self.weight_data:
            self.ask_water_retention()

        self.target_weight = self.weight_data.get("target_weight", 0)
        self.water_retention_factor = self.weight_data.get("water_retention", 1.0)
        self.last_water_retention_date = self.weight_data.get("last_water_retention_date", QDate.currentDate().toString("yyyy-MM-dd"))

        self.init_ui()
        self.showMaximized()

    def load_data(self):
        """Load weight data from the file."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self):
        """Save weight data to the file."""
        with open(DATA_FILE, 'w') as file:
            json.dump(self.weight_data, file, indent=4)

    def init_ui(self):
        """Initialize the UI components."""
        main_layout = QVBoxLayout()

        title = QLabel("WeightWise v2.0")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)

        # Target weight input
        target_layout = self.create_input_layout("Target Weight (kg):", self.target_weight, self.set_target_weight)
        main_layout.addLayout(target_layout)

        # Calendar and weight input
        input_layout = QHBoxLayout()
        self.calendar = QCalendarWidget()
        input_layout.addWidget(self.calendar)

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Enter weight (kg)")
        input_layout.addWidget(self.weight_input)

        add_button = QPushButton("Add Record")
        add_button.setStyleSheet("font-size: 14px; background-color: #4CAF50; color: white;")
        add_button.clicked.connect(self.add_record)
        input_layout.addWidget(add_button)

        main_layout.addLayout(input_layout)

        # Weight history table
        self.table = self.create_table()
        main_layout.addWidget(self.table)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_button("Refresh", self.load_table))
        button_layout.addWidget(self.create_button("Save & Exit", self.save_and_exit))
        button_layout.addWidget(self.create_button("About", self.show_about_dialog))
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.load_table()

    def create_input_layout(self, label_text, default_value, button_action):
        """Helper function to create input fields for target weight."""
        layout = QHBoxLayout()
        label = QLabel(label_text)
        layout.addWidget(label)
    
        self.target_input = QLineEdit(str(default_value))  # Store the QLineEdit widget as an attribute
        layout.addWidget(self.target_input)  # Use self.target_input instead of line_edit
    
        button = QPushButton("Set Target")
        button.clicked.connect(button_action)
        layout.addWidget(button)
    
        return layout

    def create_button(self, text, action):
        """Helper function to create buttons."""
        button = QPushButton(text)
        button.clicked.connect(action)
        return button
        
        
    def check_weight_warning(self):
        if self.table.rowCount() < 1:
            return  # No rows to check
    
        # Get the last row and the value in the "Real Gain/Loss" column
        last_row = self.table.rowCount() - 1
        real_gain_loss_item = self.table.item(last_row, 3)  # Column index for "Real Gain/Loss"
    
        if real_gain_loss_item is None:
            return  # No item in the last row, column 3
    
        # Extract and clean the value from the last row
        real_gain_loss_text = real_gain_loss_item.text()
    
        try:
            # Convert to float after cleaning up text
            real_gain_loss_value = float(real_gain_loss_text.replace('+', '').replace('-', '').replace(' kg', ''))
        except ValueError:
            return  # Handle conversion error if text is not a valid float
    
        # Check if the absolute value exceeds the threshold
        if abs(real_gain_loss_value) > 10:
            warning_message = f"Your last real gain/loss value is {real_gain_loss_text}."
            dietary_advice = "Consider reducing your calorie intake or increasing your activity level."
            self.show_warning_dialog(warning_message, dietary_advice)
 
 
    def show_warning_dialog(self, message, dietary_advice):
        """Show a fancy warning dialog with dietary advice."""
        # Create a custom dialog
        warning_dialog = QDialog(self)
        warning_dialog.setWindowTitle("Weight Warning")
        warning_dialog.setGeometry(300, 300, 400, 300)
    
        # Layout for the dialog
        layout = QVBoxLayout()
    
        # Add a warning icon and message
        icon_label = QLabel()
        icon_label.setPixmap(QIcon("warning_icon.png").pixmap(64, 64))  # Replace with your icon path
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
    
        # Add the main warning message
        warning_label = QLabel(f"<h2 style='color: red;'>{message}</h2>")
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label)
    
        # Add dietary advice
        advice_label = QLabel(f"""
            <h3>Dietary Advice</h3>
            <p>{dietary_advice}</p>
            <ul>
                <li>Reduce sodium intake to prevent water retention.</li>
                <li>Focus on whole foods like vegetables and lean proteins.</li>
                <li>Drink plenty of water to stay hydrated.</li>
                <li>Consult a dietitian for a personalized plan.</li>
            </ul>
        """)
        advice_label.setWordWrap(True)
        layout.addWidget(advice_label)
    
        # Add a button to close the dialog
        close_button = QPushButton("Got It!")
        close_button.clicked.connect(warning_dialog.accept)
        layout.addWidget(close_button)
    
        # Apply layout to dialog
        warning_dialog.setLayout(layout)
        warning_dialog.exec_()   

    def create_table(self):
        """Create table for displaying weight records."""
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Date", "Weight (kg)", "Gain/Loss to Target (kg)", "Real Gain/Loss (kg)"])
        table.horizontalHeader().setStretchLastSection(True)
        return table

    def load_table(self):
        """Load data into the table."""
        self.table.setRowCount(0)  # Clear existing rows
    
        # Apply and update water retention decay
        decayed_retention = self.get_current_water_retention()  # Update and get current retention factor
    
        for row, (date, weight) in enumerate(sorted(self.weight_data.items())):
            if date in ["target_weight", "water_retention", "last_water_retention_date"]:
                continue  # Skip non-record entries
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(date))
            self.table.setItem(row, 1, QTableWidgetItem(str(weight)))
    
            # Calculate differences using decayed retention
            difference = float(weight) - self.target_weight
            real_difference = min(difference * decayed_retention, difference + 10)  # Cap at 10kg additional water
    
            # Populate table with calculated differences
            self.table.setItem(row, 2, QTableWidgetItem(f"{difference:+.2f} kg"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{real_difference:+.2f} kg"))
    
        # Check warning for the last row only
        self.check_weight_warning()

    def get_current_water_retention(self):
        """Get and update the current water retention factor based on time decay."""
        last_update = QDate.fromString(self.last_water_retention_date, "yyyy-MM-dd")
        current_date = QDate.currentDate()
        
        # Handle invalid date parsing
        if not last_update.isValid():
            print(f"Invalid last update date: {self.last_water_retention_date}. Resetting to current date.")
            last_update = current_date
            self.last_water_retention_date = current_date.toString("yyyy-MM-dd")
            self.weight_data["last_water_retention_date"] = self.last_water_retention_date
            self.save_data()
        
        # Calculate days since last update
        days_since_update = last_update.daysTo(current_date)
        print(f"Last update date: {last_update.toString('yyyy-MM-dd')}")
        print(f"Current date: {current_date.toString('yyyy-MM-dd')}")
        print(f"Days since update: {days_since_update}")
        
        # Apply decay: 10% per week
        decay_rate_per_week = 0.1
        weeks_since_update = days_since_update / 7
        decay_factor = max(0.1, (1 - decay_rate_per_week * weeks_since_update))
        print(f"Decay factor: {decay_factor}")
        
        # Calculate the decayed retention factor
        decayed_retention = self.water_retention_factor * decay_factor
        self.water_retention_factor = max(decayed_retention, 1.0)
        self.water_retention_factor = min(self.water_retention_factor, 1.5)  # Apply cap of 1.5

        print(f"Updated water retention factor: {self.water_retention_factor}")
        
        # Save updated retention factor
        self.weight_data["water_retention"] = self.water_retention_factor
        self.weight_data["last_water_retention_date"] = current_date.toString("yyyy-MM-dd")
        self.save_data()
        
        return self.water_retention_factor
    
 
    
    def add_record(self):
        """Add a new record to the data."""
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        weight = self.weight_input.text().strip()
        
        if not weight.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid weight in kg.")
            return
        
        # Add the new weight record
        self.weight_data[selected_date] = weight
        
        # Update last water retention date to the selected date
        self.last_water_retention_date = selected_date
        self.weight_data["last_water_retention_date"] = self.last_water_retention_date
        
        # Recalculate water retention decay and update
        self.get_current_water_retention()
        
        # Refresh table to apply updated retention factor
        self.load_table()
        self.check_weight_warning()  # Add this line

        self.weight_input.clear()
        
        QMessageBox.information(self, "Record Added", f"Added: {selected_date} -> {weight} kg")
    
    def calculate_new_water_retention_factor(self):
        """Calculate the new water retention factor considering decay."""
        return self.get_current_water_retention()

 
    
 

    def set_target_weight(self):
        """Set the target weight."""
        target = self.target_input.text().strip()  # Use the attribute directly
        if not target.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid target weight in kg.")
            return
    
        self.target_weight = float(target)
        self.weight_data["target_weight"] = self.target_weight
        self.save_data()
        self.load_table()
        QMessageBox.information(self, "Target Set", f"Target weight set to {self.target_weight} kg")

    def save_and_exit(self):
        """Save data and exit the application."""
        self.save_data()
        QMessageBox.information(self, "Data Saved", "Your data has been saved.")
        QApplication.quit()

    def ask_water_retention(self):
        """Ask the user about their water retention estimate."""
        dialog = WaterRetentionDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.water_retention_factor = dialog.water_retention_factor
            self.weight_data["water_retention"] = self.water_retention_factor
            self.weight_data["last_water_retention_date"] = QDate.currentDate().toString("yyyy-MM-dd")
            self.save_data()

    from PyQt5.QtWidgets import QMessageBox, QTextBrowser
    
    def show_about_dialog(self):
        """Show the about dialog with clickable links."""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About WeightWise v2.0")
        about_dialog.setGeometry(200, 200, 400, 300)
        about_dialog.setWindowState(Qt.WindowMaximized)

        
        # Create a layout for the dialog
        layout = QVBoxLayout()
    
        # Create a QTextBrowser to allow rich HTML content with clickable links
        about_text = """
        <h2>WeightWise v2.0</h2>
        <p><b>Developed by:</b> Peter De Ceuster</p>
        <p>This application helps you track your weight and manage your target weight with water retention estimates.</p>
        <p>For more information:</p>
        <ul>
            <li><a href="https://peterdeceuster.uk">Visit our website</a></li>
            <li><a href="https://buymeacoffee.com/siglabo">Buy me a coffee</a></li>
          
        </ul>
        <p>&copy; 2024 Peter De Ceuster</p>
        """
    
        # Set up QTextBrowser to display the HTML content
        text_browser = QTextBrowser()
        text_browser.setHtml(about_text)
        text_browser.setOpenExternalLinks(True)  # Allow clickable links
    
        # Add QTextBrowser to the layout
        layout.addWidget(text_browser)
    
        # Add a button to close the dialog
        close_button = QPushButton("Close")
        close_button.clicked.connect(about_dialog.accept)
        layout.addWidget(close_button)
    
        about_dialog.setLayout(layout)
        about_dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = WeightTrackerApp()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

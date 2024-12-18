import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QScrollArea, QDialog,
    QLabel, QLineEdit, QDateEdit, QHBoxLayout, QFormLayout, QMessageBox, QListWidget, QListWidgetItem,
    QSystemTrayIcon, QMenu, QColorDialog, QGroupBox, QCheckBox, QSpinBox, QTabWidget, QComboBox, QTextEdit, QDialogButtonBox, QFileDialog
)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter, QDoubleValidator
from PyQt6.QtCharts import (
    QChartView, QChart, QValueAxis, QBarSeries, QBarSet, QBarCategoryAxis
)
import json
import sys


LOGO_DIR = Path("logos")
LOGO_DIR.mkdir(exist_ok=True)
DEFAULT_ICON = str(LOGO_DIR / "default_logo.png")



PREDEFINED_SUBSCRIPTIONS = [
    {"name": "Netflix", "color": "#E50914", "logo": str(LOGO_DIR / "netflix.png")},
    {"name": "Spotify", "color": "#1DB954", "logo": str(LOGO_DIR / "spotify.png")},
    {"name": "Amazon Prime", "color": "#00A8E1", "logo": str(LOGO_DIR / "amazon_prime.png")},
    {"name": "Disney+", "color": "#113CCF", "logo": str(LOGO_DIR / "disney_plus.png")},
    {"name": "Slack", "color": "#4A154B", "logo": str(LOGO_DIR / "slack.png")},
    {"name": "LinkedIn Premium", "color": "#0077B5", "logo": str(LOGO_DIR / "linkedin_premium.png")},
    {"name": "YouTube Premium", "color": "#FF0000", "logo": str(LOGO_DIR / "youtube.png")},
    {"name": "HBO Max", "color": "#8400FF", "logo": str(LOGO_DIR / "hbo.png")},
    {"name": "Apple TV+", "color": "#000000", "logo": str(LOGO_DIR / "appletv.png")},
    {"name": "Xbox Game Pass", "color": "#107C10", "logo": str(LOGO_DIR / "xbox.png")},
    {"name": "PlayStation Plus", "color": "#003791", "logo": str(LOGO_DIR / "playstation.png")},
    {"name": "Apple Music", "color": "#FC3C44", "logo": str(LOGO_DIR / "applemusic.png")},
    {"name": "Adobe Creative Cloud", "color": "#FF0000", "logo": str(LOGO_DIR / "adobe.png")},
    {"name": "Microsoft 365", "color": "#0078D4", "logo": str(LOGO_DIR / "office365.png")},
    {"name": "Google One", "color": "#4285F4", "logo": str(LOGO_DIR / "googleone.png")},
    {"name": "Dropbox", "color": "#0061FF", "logo": str(LOGO_DIR / "dropbox.png")},
    {"name": "iCloud+", "color": "#147EFB", "logo": str(LOGO_DIR / "icloud.png")},
    {"name": "Hulu", "color": "#1CE783", "logo": str(LOGO_DIR / "hulu.png")},
    {"name": "EA Play", "color": "#FF4747", "logo": str(LOGO_DIR / "eaplay.png")},
    {"name": "Paramount+", "color": "#0064FF", "logo": str(LOGO_DIR / "paramount.png")},
    {"name": "Discord Nitro", "color": "#5865F2", "logo": str(LOGO_DIR / "discord.png")},
    {"name": "GitHub Pro", "color": "#24292E", "logo": str(LOGO_DIR / "github.png")},
    {"name": "Nord VPN", "color": "#4687FF", "logo": str(LOGO_DIR / "nordvpn.png")},
    {"name": "Twitch Prime", "color": "#9146FF", "logo": str(LOGO_DIR / "twitch.png")},
    {"name": "Crunchyroll", "color": "#F47521", "logo": str(LOGO_DIR / "crunchyroll.png")},
    {"name": "Amazon Music", "color": "#00A8E1", "logo": str(LOGO_DIR / "amazonmusic.png")}
]

MODERN_COLORS = {
    "background": "#1A1A1A",     
    "card": "#2D2D2D",          
    "card_hover": "#333333",     
    "text_primary": "#FFFFFF",  
    "text_secondary": "#B3B3B3", 
    "accent": "#4F46E5",         
    "accent_hover": "#4338CA",   
    "border": "#404040",         
    "button": "#404040",         
    "button_hover": "#4A4A4A"   
}

CATEGORIES = [
    "Streaming", "Software", "Gaming", "Cloud Storage", 
    "Music", "Fitness", "News", "Other"
]

CURRENCIES = [
    {"symbol": "$", "code": "USD", "name": "US Dollar"},
    {"symbol": "€", "code": "EUR", "name": "Euro"},
    {"symbol": "£", "code": "GBP", "name": "British Pound"},
    {"symbol": "¥", "code": "JPY", "name": "Japanese Yen"}
]

BILLING_FREQUENCIES = [
    "Monthly", "Quarterly", "Semi-Annually", "Annually"
]

LIGHT_COLORS = {
    "background": "#FFFFFF",
    "card": "#F5F5F5",
    "card_hover": "#EEEEEE",
    "text_primary": "#000000",
    "text_secondary": "#666666",
    "accent": "#4F46E5",
    "accent_hover": "#4338CA",
    "border": "#E0E0E0",
    "button": "#E0E0E0",
    "button_hover": "#D0D0D0"
}

class SubscriptionCard(QWidget):
    def __init__(self, name, renewal_date, cost, color, logo, category, on_edit, on_delete, parent=None):
        super().__init__(parent)
        self.name = name
        self.renewal_date = renewal_date
        self.cost = str(float(cost))
        self.color = color
        self.logo = logo if os.path.exists(logo) else DEFAULT_ICON
        self.category = category

        
        self.setFixedSize(390, 120)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.container = QWidget()
        self.container.setObjectName("card")
        
        
        container_layout = QHBoxLayout(self.container)
        container_layout.setContentsMargins(16, 8, 16, 16)
        container_layout.setSpacing(8)

        
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        
        logo_label = QLabel()
        pixmap = QPixmap(self.logo)
        if pixmap.isNull():
            pixmap = QPixmap(DEFAULT_ICON)
        scaled_pixmap = pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, 
                                    Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setFixedSize(48, 48)
        
        
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(8, 0, 0, 0)
        details_layout.setSpacing(4)

        self.name_label = QLabel(name)
        self.name_label.setWordWrap(True)
        self.date_label = QLabel(f"Renewal: {renewal_date}")
        self.cost_label = QLabel(f"${float(cost):.2f}/month")
        
        details_layout.addWidget(self.name_label)
        details_layout.addWidget(self.date_label)
        details_layout.addWidget(self.cost_label)
        
        content_layout.addWidget(logo_label)
        content_layout.addWidget(details_widget, 1)
        
        
        buttons_widget = QWidget()
        buttons_layout = QVBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(16)
        
       
        edit_button = QPushButton("⋮")
        edit_button.setFixedSize(32, 32)
        edit_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {MODERN_COLORS["button"]};
                color: {MODERN_COLORS["text_primary"]};
                border: none;
                border-radius: 16px;
                font-size: 18px;
            }}
            QPushButton:hover {{
                background-color: {MODERN_COLORS["button_hover"]};
            }}
        """)
        
        
        self.status_indicator = QPushButton()
        self.status_indicator.setFixedSize(24, 24)
        self.status_indicator.clicked.connect(self.show_days_to_renewal)
        
       
        buttons_layout.addWidget(edit_button, 0, Qt.AlignmentFlag.AlignTop)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.status_indicator, 0, Qt.AlignmentFlag.AlignBottom)
        
        
        container_layout.addWidget(content_widget)
        container_layout.addWidget(buttons_widget, 0, Qt.AlignmentFlag.AlignRight)
        
       
        separator = QWidget()
        separator.setFixedHeight(2)
        separator.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent,
                    stop:0.2 {MODERN_COLORS["border"]},
                    stop:0.8 {MODERN_COLORS["border"]},
                    stop:1 transparent
                );
                margin-top: 8px;
                margin-bottom: 8px;
            }}
        """)
        
        
        container_layout.addWidget(separator)
        container_layout.setStretch(0, 1)  # Make separator expand horizontally
        
        main_layout.addWidget(self.container)
        
       
        menu = QMenu()
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {MODERN_COLORS["card"]};
                border: 1px solid {MODERN_COLORS["border"]};
                border-radius: 4px;
                padding: 4px;
            }}
            QMenu::item {{
                color: {MODERN_COLORS["text_primary"]};
                padding: 8px 16px;
            }}
            QMenu::item:selected {{
                background-color: {MODERN_COLORS["button_hover"]};
            }}
        """)
        
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        edit_action.triggered.connect(lambda: on_edit(self))
        delete_action.triggered.connect(lambda: on_delete(self))
        edit_button.clicked.connect(lambda: menu.exec(edit_button.mapToGlobal(
            edit_button.rect().bottomRight())))
        
        self.update_status_indicator()

    def show_days_to_renewal(self):
        days = QDate.currentDate().daysTo(QDate.fromString(self.renewal_date, "yyyy-MM-dd"))
        QMessageBox.information(self, "Days to Renewal", 
            f"Days until renewal: {days}\nRenewal date: {self.renewal_date}")

    def update_status_indicator(self):
        days = QDate.currentDate().daysTo(QDate.fromString(self.renewal_date, "yyyy-MM-dd"))
        
        if days > 15:
            color = "#2ECC71"  # Green
        elif 8 <= days <= 15:
            color = "#F1C40F"  # Yellow
        elif 3 <= days < 8:
            color = "#E67E22"  # Orange
        else:
            color = "#E74C3C"  # Red
            
        self.status_indicator.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 12px;
            }}
            QPushButton:hover {{
                border: 2px solid {MODERN_COLORS["text_primary"]};
            }}
        """)
        self.status_indicator.setToolTip(f"Days until renewal: {days}")

class SubscriptionStats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        
        select_button = QPushButton("Select Subscriptions")
        select_button.clicked.connect(self.show_selection_dialog)
        layout.addWidget(select_button)
        
        
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.setBackgroundBrush(QColor(MODERN_COLORS["background"]))
        self.chart.setTitleBrush(QColor(MODERN_COLORS["text_primary"]))
        self.chart.setTitle("Monthly Spending")
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.chart_view.setMinimumHeight(400)  
        layout.addWidget(self.chart_view)
        
        
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMinimumHeight(200)  
        layout.addWidget(self.stats_text)
        
        self.selected_subscriptions = []
        self.all_subscriptions = []
    
    def update_subscriptions(self, subscriptions):
       
        self.all_subscriptions = subscriptions
        self.selected_subscriptions = []  
        self.update_graph()  
    def show_selection_dialog(self):
        dialog = SelectSubscriptionsDialog(self.all_subscriptions, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.selected_subscriptions = dialog.get_selected_subscriptions()
            self.update_graph()
    
    def update_graph(self):
        try:
            self.chart.removeAllSeries()
            if not self.selected_subscriptions:
                return
                
           
            series = QBarSeries()
            costs = []
            
           
            for sub in self.selected_subscriptions:
                bar_set = QBarSet(sub.name)
                cost = float(sub.cost)
                bar_set.append(cost)
                series.append(bar_set)
                costs.append(cost)
            
            
            self.chart.addSeries(series)
            
           
            axis_x = QBarCategoryAxis()
            axis_x.append("Monthly Cost")
            axis_x.setLabelsColor(QColor(MODERN_COLORS["text_primary"]))
            
            axis_y = QValueAxis()
            max_cost = max(costs) if costs else 0
            axis_y.setRange(0, max_cost * 1.2)
            axis_y.setLabelsColor(QColor(MODERN_COLORS["text_primary"]))
            
            
            self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
            self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
            series.attachAxis(axis_x)
            series.attachAxis(axis_y)
            
            
            self.chart.legend().setVisible(True)
            self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
            self.chart.legend().setLabelColor(QColor(MODERN_COLORS["text_primary"]))
            
           
            total = sum(costs)
            yearly = total * 12
            stats = f"""Selected Subscriptions Summary:
            Monthly Total: ${total:.2f}
            Yearly Total: ${yearly:.2f}
            Number of Subscriptions: {len(self.selected_subscriptions)}
            """
            self.stats_text.setText(stats)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to update graph: {str(e)}")

class ExportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Export Data")
        layout = QVBoxLayout(self)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "PDF", "JSON"])
        layout.addWidget(self.format_combo)
        
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_data)
        layout.addWidget(export_button)

class AddSubscriptionDialog(QDialog):
    def __init__(self, subscription=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Subscription")
        self.setFixedSize(450, 600)
        
        form_layout = QFormLayout()
        
        
        self.subscription_list = QListWidget()
        for sub in PREDEFINED_SUBSCRIPTIONS:
            item = QListWidgetItem(QIcon(sub["logo"]), sub["name"])
            item.setData(Qt.ItemDataRole.UserRole, sub)
            self.subscription_list.addItem(item)
            
       
        if subscription:
            self.current_subscription = {
                "name": subscription.name,
                "color": subscription.color,
                "logo": subscription.logo
            }
        else:
            self.current_subscription = None
            
       
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate() if not subscription else QDate.fromString(subscription.renewal_date, "yyyy-MM-dd"))
        
        self.cost_input = QLineEdit()
        self.cost_input.setText(subscription.cost if subscription else "")
        self.cost_input.setValidator(QDoubleValidator(0.00, 999999.99, 2))
        
        
        form_layout.addRow("Choose Subscription:", self.subscription_list)
        form_layout.addRow("Renewal Date:", self.date_input)
        form_layout.addRow("Cost ($):", self.cost_input)
        
        
        self.submit_button = QPushButton("Save")
        self.submit_button.clicked.connect(self.accept)
        form_layout.addWidget(self.submit_button)
        
        self.setLayout(form_layout)
        
       
        if subscription:
            for i in range(self.subscription_list.count()):
                item = self.subscription_list.item(i)
                if item.text() == subscription.name:
                    self.subscription_list.setCurrentItem(item)
                    break

    def pick_color(self):
        color = QColorDialog.getColor(QColor(self.current_color), self)
        if color.isValid():
            self.current_color = color.name()
            self.update_color_button()

    def update_color_button(self):
        self.color_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_color};
                border: 2px solid {MODERN_COLORS["border"]};
                border-radius: 20px;
            }}
        """)

    def get_selected_data(self):
        selected_item = self.subscription_list.currentItem()
        selected_data = selected_item.data(Qt.ItemDataRole.UserRole) if selected_item else self.current_subscription
        
        if not selected_data:
            raise ValueError("Please select a subscription")
            
        return {
            "subscription": {
                "name": selected_data["name"],
                "logo": selected_data["logo"],
                "color": selected_data["color"]
            },
            "renewal_date": self.date_input.date(),
            "cost": self.cost_input.text() or "0.00",
            "color": selected_data["color"]
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subscription Manager")
        self.setFixedSize(450, 800)  

        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

       
        self.tray_icon = QSystemTrayIcon(QIcon(DEFAULT_ICON), self)
        self.tray_icon.show()

       
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search subscriptions...")
        self.search_bar.textChanged.connect(self.filter_subscriptions)
        self.main_layout.addWidget(self.search_bar)

       
        self.total_cost_label = QLabel("Total Monthly Cost: $0.00")
        self.total_cost_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        
       
        self.stats_widget = SubscriptionStats()
        self.tab_widget = QTabWidget()
        
       
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(500) 
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        
      
        self.tab_widget.addTab(self.scroll_area, "Subscriptions")
        self.tab_widget.addTab(self.stats_widget, "Analytics")
        
       
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "Name (A-Z)", 
            "Name (Z-A)",
            "Price (High-Low)", 
            "Price (Low-High)",
            "Renewal (Newest-Oldest)", 
            "Renewal (Oldest-Newest)"
        ])
        self.sort_combo.currentTextChanged.connect(self.sort_subscriptions)
        
      
        self.add_button = QPushButton("Add Subscription")
        self.add_button.setFixedHeight(40)
        self.add_button.clicked.connect(self.open_add_subscription_dialog)
        
       
        self.main_layout.addWidget(self.sort_combo)
        self.main_layout.addWidget(self.tab_widget)
        self.main_layout.addWidget(self.total_cost_label)
        self.main_layout.addWidget(self.add_button)
        
       
        self.subscriptions = []
        self.load_data()

        
        menubar = self.menuBar()
        settings_menu = menubar.addMenu('Settings')
        settings_action = settings_menu.addAction('Preferences')
        settings_action.triggered.connect(self.open_settings)
        
       
        self.notification_status = QLabel()
        self.update_notification_status()
        self.main_layout.addWidget(self.notification_status)
        
       
        self.sort_combo.clear()
        self.sort_combo.addItems([
            "Name (A-Z)", 
            "Name (Z-A)",
            "Price (High-Low)", 
            "Price (Low-High)",
            "Due Soon", 
            "Due Later", 
            "Recently Added",
            "Oldest Added"
        ])

    def open_add_subscription_dialog(self, subscription=None):
        try:
            dialog = AddSubscriptionDialog(subscription, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                data = dialog.get_selected_data()
                
                if subscription:
                    
                    subscription.name = data["subscription"]["name"]
                    subscription.renewal_date = data["renewal_date"].toString("yyyy-MM-dd")
                    subscription.cost = data["cost"]
                    subscription.color = data["color"]
                    subscription.update_display()
                else:
                
                    card = SubscriptionCard(
                        name=data["subscription"]["name"],
                        renewal_date=data["renewal_date"].toString("yyyy-MM-dd"),
                        cost=float(data["cost"]),
                        color=data["color"],
                        logo=data["subscription"]["logo"],
                        category="",  
                        on_edit=self.edit_subscription,
                        on_delete=self.delete_subscription,
                        parent=self
                    )
                    self.subscriptions.append(card)
                    self.scroll_layout.addWidget(card)
                
                self.save_data()
                self.update_total_cost()
                self.stats_widget.update_subscriptions(self.subscriptions)  
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to {('update' if subscription else 'add')} subscription: {str(e)}")
        self.stats_widget.update_subscriptions(self.subscriptions)

    def edit_subscription(self, card):
        self.open_add_subscription_dialog(card)

    def delete_subscription(self, card):
        confirmation = QMessageBox.question(self, "Delete Subscription", f"Are you sure you want to delete {card.name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirmation == QMessageBox.StandardButton.Yes:
            self.subscriptions.remove(card)
            card.deleteLater()
            self.save_data()
            self.update_total_cost()
            self.stats_widget.update_subscriptions(self.subscriptions) 

    def filter_subscriptions(self):
        query = self.search_bar.text().lower()
        for card in self.subscriptions:
            card.setVisible(query in card.name.lower())

    def update_total_cost(self):
        try:
            total_cost = 0
            for card in self.subscriptions:
                try:
                    cost = float(card.cost.replace('$', '').strip())
                    if cost > 0:
                        total_cost += cost
                except (ValueError, AttributeError):
                    continue
                    
            self.total_cost_label.setText(f"Total Monthly Cost: ${total_cost:.2f}")
        except Exception as e:
            print(f"Error calculating total cost: {e}")
            self.total_cost_label.setText("Total Monthly Cost: $0.00")

    def save_data(self):
        try:
            data = []
            for card in self.subscriptions:
                if hasattr(card, 'name'): 
                    data.append({
                        "name": card.name,
                        "renewal_date": card.renewal_date,
                        "cost": card.cost,
                        "color": card.color,
                        "logo": card.logo,
                        "category": getattr(card, 'category', "")
                    })
            
            with open("subscriptions.json", "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save data: {str(e)}")

    def load_data(self):
        try:
            if os.path.exists("subscriptions.json"):
                with open("subscriptions.json", "r") as file:
                    data = json.load(file)
                    for sub in data:
                        if all(key in sub for key in ["name", "renewal_date", "cost", "color", "logo"]):
                            try:
                                
                                cost = float(str(sub["cost"]).replace('$', '').strip())
                                if cost <= 0:
                                    continue
                                    
                                card = SubscriptionCard(
                                    name=sub["name"],
                                    renewal_date=sub["renewal_date"],
                                    cost=cost,
                                    color=sub["color"],
                                    logo=sub.get("logo", DEFAULT_ICON),
                                    category=sub.get("category", ""),
                                    on_edit=self.edit_subscription,
                                    on_delete=self.delete_subscription,
                                    parent=self
                                )
                                self.subscriptions.append(card)
                                self.scroll_layout.addWidget(card)
                            except ValueError:
                                continue
                                
                self.update_total_cost()
                self.stats_widget.update_subscriptions(self.subscriptions)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {str(e)}")

    def check_renewals(self):
        for card in self.subscriptions:
            renewal_date = QDate.fromString(card.renewal_date, "yyyy-MM-dd")
            days_to_renewal = QDate.currentDate().daysTo(renewal_date)
            if days_to_renewal <= 7:
                self.tray_icon.showMessage(
                    "Subscription Renewal Reminder",
                    f"{card.name} is due for renewal in {days_to_renewal} days.",
                    QSystemTrayIcon.MessageIcon.Information,
                    5000
                )

    def open_settings(self):
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_notification_status()

    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow, QDialog {
                    background-color: #2C3E50;
                    color: #ECF0F1;
                }
                QLabel {
                    color: #ECF0F1;
                }
                QPushButton {
                    background-color: #34495E;
                    color: #ECF0F1;
                    border: none;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #415B76;
                }
            """)
        else:
            self.setStyleSheet("")

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
            self.apply_theme(settings.get("theme", "light"))
        except:
            self.apply_theme("light")

    def show_export_dialog(self):
        dialog = ExportDialog(self)
        dialog.exec()

    def sort_subscriptions(self, criteria):
        try:
            if criteria == "Name (A-Z)":
                self.subscriptions.sort(key=lambda x: x.name.lower())
            elif criteria == "Name (Z-A)":
                self.subscriptions.sort(key=lambda x: x.name.lower(), reverse=True)
            elif criteria == "Price (High-Low)":
                self.subscriptions.sort(key=lambda x: float(x.cost.replace('$', '').strip()), reverse=True)
            elif criteria == "Price (Low-High)":
                self.subscriptions.sort(key=lambda x: float(x.cost.replace('$', '').strip()))
            elif criteria == "Due Soon":
                
                self.subscriptions.sort(
                    key=lambda x: QDate.currentDate().daysTo(QDate.fromString(x.renewal_date, "yyyy-MM-dd"))
                )
            elif criteria == "Due Later":
                
                self.subscriptions.sort(
                    key=lambda x: QDate.currentDate().daysTo(QDate.fromString(x.renewal_date, "yyyy-MM-dd")),
                    reverse=True
                )
            elif criteria == "Recently Added":
               
                self.subscriptions.sort(key=lambda x: getattr(x, 'date_added', QDate.currentDate()), reverse=True)
            elif criteria == "Oldest Added":
                
                self.subscriptions.sort(key=lambda x: getattr(x, 'date_added', QDate.currentDate()))
            
           
            while self.scroll_layout.count():
                item = self.scroll_layout.takeAt(0)
                if item.widget():
                    item.widget().setParent(None)
            
            for card in self.subscriptions:
                self.scroll_layout.addWidget(card)
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to sort: {str(e)}")
            
    def update_notification_status(self):
        try:
            with open("settings.json", "r") as f:
                settings = json.load(f)
                enabled = settings.get("notifications_enabled", False)
                days = settings.get("notification_days", 7)
                self.notification_status.setText(
                    f"Notifications: {'Enabled' if enabled else 'Disabled'} ({days} days before renewal)"
                )
                self.notification_status.setStyleSheet(
                    f"color: {'green' if enabled else 'red'}; padding: 5px;"
                )
        except:
            self.notification_status.setText("Notifications: Not configured")
            self.notification_status.setStyleSheet("color: orange; padding: 5px;")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 600)
        self.default_settings = {
            "notifications_enabled": False,
            "notification_days": 7,
            "notification_sound": False,
            "desktop_notifications": True,
            "email_notifications": False,
            "email": "",
            "currency_symbol": "$",
            "currency_position": "Before amount",
            "decimal_places": 2,
            "monthly_budget": 0,
            "budget_alert": False,
            "budget_threshold": 80,
            "compact_view": False,
            "show_yearly_cost": False,
            "default_sort": "Name",
            "auto_backup": False,
            "backup_frequency": "Weekly",
            "backup_location": os.path.expanduser("~/Documents/SubscriptionBackups"),
            "show_all_periods": False,
            "highlight_expensive": False,
            "expense_threshold": 50,
            "cost_period": "Monthly"
        }
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout = QVBoxLayout()
        
       
        notif_group = QGroupBox("Notifications")
        notif_layout = QVBoxLayout()
        self.enable_notifications = QCheckBox("Enable Renewal Notifications")
        self.notification_days = QSpinBox()
        self.notification_days.setRange(1, 30)
        self.notification_sound = QCheckBox("Play Sound")
        self.desktop_notifications = QCheckBox("Show Desktop Notifications")
        self.email_notifications = QCheckBox("Send Email Notifications")
        self.email_input = QLineEdit()
        notif_layout.addWidget(self.enable_notifications)
        notif_layout.addWidget(QLabel("Days before renewal:"))
        notif_layout.addWidget(self.notification_days)
        notif_layout.addWidget(self.notification_sound)
        notif_layout.addWidget(self.desktop_notifications)
        notif_layout.addWidget(self.email_notifications)
        notif_layout.addWidget(self.email_input)
        notif_group.setLayout(notif_layout)
        
       
        currency_group = QGroupBox("Currency")
        currency_layout = QVBoxLayout()
        self.currency_symbol = QLineEdit("$")
        self.currency_position = QComboBox()
        self.currency_position.addItems(["Before amount", "After amount"])
        self.decimal_places = QSpinBox()
        self.decimal_places.setRange(0, 4)
        currency_layout.addWidget(QLabel("Symbol:"))
        currency_layout.addWidget(self.currency_symbol)
        currency_layout.addWidget(QLabel("Position:"))
        currency_layout.addWidget(self.currency_position)
        currency_layout.addWidget(QLabel("Decimal Places:"))
        currency_layout.addWidget(self.decimal_places)
        currency_group.setLayout(currency_layout)
        
        
        budget_group = QGroupBox("Budget")
        budget_layout = QVBoxLayout()
        self.monthly_budget = QSpinBox()
        self.monthly_budget.setRange(0, 999999)
        self.monthly_budget.setSuffix(" $")
        self.budget_alert = QCheckBox("Enable Budget Alerts")
        self.budget_threshold = QSpinBox()
        self.budget_threshold.setRange(50, 100)
        self.budget_threshold.setSuffix(" %")
        budget_layout.addWidget(QLabel("Monthly Budget:"))
        budget_layout.addWidget(self.monthly_budget)
        budget_layout.addWidget(self.budget_alert)
        budget_layout.addWidget(QLabel("Alert Threshold:"))
        budget_layout.addWidget(self.budget_threshold)
        budget_group.setLayout(budget_layout)
        
       
        display_group = QGroupBox("Display")
        display_layout = QVBoxLayout()
        self.compact_view = QCheckBox("Compact View")
        self.show_yearly_cost = QCheckBox("Show Yearly Cost")
        self.default_sort = QComboBox()
        self.default_sort.addItems(["Name", "Price", "Renewal Date"])
        display_layout.addWidget(self.compact_view)
        display_layout.addWidget(self.show_yearly_cost)
        display_layout.addWidget(QLabel("Default Sort:"))
        display_layout.addWidget(self.default_sort)
        display_group.setLayout(display_layout)
        
        
        backup_group = QGroupBox("Backup")
        backup_layout = QVBoxLayout()
        self.auto_backup = QCheckBox("Enable Auto-Backup")
        self.backup_frequency = QComboBox()
        self.backup_frequency.addItems(["Daily", "Weekly", "Monthly"])
        self.backup_location = QLineEdit()
        browse_button = QPushButton("Browse")
        backup_layout.addWidget(self.auto_backup)
        backup_layout.addWidget(QLabel("Frequency:"))
        backup_layout.addWidget(self.backup_frequency)
        backup_layout.addWidget(QLabel("Location:"))
        backup_layout.addWidget(self.backup_location)
        backup_layout.addWidget(browse_button)
        backup_group.setLayout(backup_layout)

       
        cost_display_group = QGroupBox("Cost Display")
        cost_layout = QVBoxLayout()
        
        self.cost_period = QComboBox()
        self.cost_period.addItems(["Monthly", "3 Months", "6 Months", "Yearly"])
        
        self.show_all_periods = QCheckBox("Show all periods in cards")
        self.highlight_expensive = QCheckBox("Highlight expensive subscriptions")
        self.expense_threshold = QSpinBox()
        self.expense_threshold.setRange(0, 1000)
        self.expense_threshold.setSuffix(" $")
        
        cost_layout.addWidget(QLabel("Default period:"))
        cost_layout.addWidget(self.cost_period)
        cost_layout.addWidget(self.show_all_periods)
        cost_layout.addWidget(self.highlight_expensive)
        cost_layout.addWidget(QLabel("Expense threshold:"))
        cost_layout.addWidget(self.expense_threshold)
        cost_display_group.setLayout(cost_layout)
        
        
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(notif_group)
        main_layout.addWidget(currency_group)
        main_layout.addWidget(budget_group)
        main_layout.addWidget(display_group)
        main_layout.addWidget(backup_group)
        main_layout.addWidget(cost_display_group)
        
        scroll.setWidget(main_widget)
        layout.addWidget(scroll)
        
       
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
        self.load_settings()

        
        browse_button.clicked.connect(self.browse_backup_location)
        
    def browse_backup_location(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Backup Location",
            self.backup_location.text() or os.path.expanduser("~"),
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.backup_location.setText(folder)
            
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
            else:
                settings = self.default_settings
                
           
            self.enable_notifications.setChecked(settings.get("notifications_enabled", False))
            self.notification_days.setValue(settings.get("notification_days", 7))
            self.notification_sound.setChecked(settings.get("notification_sound", False))
            self.desktop_notifications.setChecked(settings.get("desktop_notifications", True))
            self.email_notifications.setChecked(settings.get("email_notifications", False))
            self.email_input.setText(settings.get("email", ""))
            self.currency_symbol.setText(settings.get("currency_symbol", "$"))
            self.currency_position.setCurrentText(settings.get("currency_position", "Before amount"))
            self.decimal_places.setValue(settings.get("decimal_places", 2))
            self.monthly_budget.setValue(settings.get("monthly_budget", 0))
            self.budget_alert.setChecked(settings.get("budget_alert", False))
            self.budget_threshold.setValue(settings.get("budget_threshold", 80))
            self.compact_view.setChecked(settings.get("compact_view", False))
            self.show_yearly_cost.setChecked(settings.get("show_yearly_cost", False))
            self.default_sort.setCurrentText(settings.get("default_sort", "Name"))
            self.auto_backup.setChecked(settings.get("auto_backup", False))
            self.backup_frequency.setCurrentText(settings.get("backup_frequency", "Weekly"))
            self.backup_location.setText(settings.get("backup_location", os.path.expanduser("~/Documents/SubscriptionBackups")))
            self.show_all_periods.setChecked(settings.get("show_all_periods", False))
            self.highlight_expensive.setChecked(settings.get("highlight_expensive", False))
            self.expense_threshold.setValue(settings.get("expense_threshold", 50))
            self.cost_period.setCurrentText(settings.get("cost_period", "Monthly"))
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load settings: {str(e)}")

    def save_settings(self):
        try:
            settings = {
                "notifications_enabled": self.enable_notifications.isChecked(),
                "notification_days": self.notification_days.value(),
                "notification_sound": self.notification_sound.isChecked(),
                "desktop_notifications": self.desktop_notifications.isChecked(),
                "email_notifications": self.email_notifications.isChecked(),
                "email": self.email_input.text(),
                "currency_symbol": self.currency_symbol.text(),
                "currency_position": self.currency_position.currentText(),
                "decimal_places": self.decimal_places.value(),
                "monthly_budget": self.monthly_budget.value(),
                "budget_alert": self.budget_alert.isChecked(),
                "budget_threshold": self.budget_threshold.value(),
                "compact_view": self.compact_view.isChecked(),
                "show_yearly_cost": self.show_yearly_cost.isChecked(),
                "default_sort": self.default_sort.currentText(),
                "auto_backup": self.auto_backup.isChecked(),
                "backup_frequency": self.backup_frequency.currentText(),
                "backup_location": self.backup_location.text(),
                "show_all_periods": self.show_all_periods.isChecked(),
                "highlight_expensive": self.highlight_expensive.isChecked(),
                "expense_threshold": self.expense_threshold.value(),
                "cost_period": self.cost_period.currentText()
            }
            
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")

class SelectSubscriptionsDialog(QDialog):
    def __init__(self, subscriptions, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Subscriptions")
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout()
        
       
        self.subscription_list = QListWidget()
        for sub in subscriptions:
            item = QListWidgetItem()
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            item.setText(f"{sub.name} (${float(sub.cost):.2f}/month)")
            item.setData(Qt.ItemDataRole.UserRole, sub)
            self.subscription_list.addItem(item)
            
        
        buttons_layout = QHBoxLayout()
        select_all = QPushButton("Select All")
        deselect_all = QPushButton("Deselect All")
        select_all.clicked.connect(self.select_all)
        deselect_all.clicked.connect(self.deselect_all)
        buttons_layout.addWidget(select_all)
        buttons_layout.addWidget(deselect_all)
        
        
        layout.addLayout(buttons_layout)
        layout.addWidget(self.subscription_list)
        
        
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
    def select_all(self):
        for i in range(self.subscription_list.count()):
            self.subscription_list.item(i).setCheckState(Qt.CheckState.Checked)
            
    def deselect_all(self):
        for i in range(self.subscription_list.count()):
            self.subscription_list.item(i).setCheckState(Qt.CheckState.Unchecked)
            
    def get_selected_subscriptions(self):
        selected = []
        for i in range(self.subscription_list.count()):
            item = self.subscription_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.data(Qt.ItemDataRole.UserRole))
        return selected

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# 💰 AI Expense Manager

A smart expense tracking application with an AI chatbot interface built with Python and tkinter.

## ✨ Features

- 💬 Chat-based expense tracking
- 📊 Visual expense graphs
- 📅 Date filtering (today, week, month)
- 🔍 Search expenses
- 🎯 Budget tracking with alerts
- 🎨 Emoji categories
- 💱 Multi-currency support

## 🖥️ System Requirements

- Windows 7/8/10/11
- No Python installation required (for .exe version)

## 📥 Download

### Option 1: Download Executable (Recommended)
1. Go to the [Releases](https://github.com/YOUR_USERNAME/expense-manager/releases) page
2. Download `ExpenseManager.exe`
3. Run the file directly

### Option 2: Run from Source
1. Clone this repository
2. Install Python 3.8+
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python expense_manager.py`

## 🎮 How to Use

### Chat Commands
- `spent 500 on food` - Add expense
- `show` - View all expenses
- `summary` - View spending summary
- `today` / `this month` / `this week` - Filter expenses
- `search pizza` - Search expenses
- `edit 2 to 600` - Edit expense
- `delete 3` - Delete expense
- `budget 5000` - Set monthly budget
- `help` - Show all commands

### GUI Buttons
Use the sidebar buttons for quick access to main features.

## 🛠️ Development

### Build from Source
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python expense_manager.py

# Build executable
pip install pyinstaller
pyinstaller --onefile --windowed --name "ExpenseManager" expense_manager.py

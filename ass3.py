import json
import tkinter as tk
from tkinter import simpledialog, messagebox
import re
import random
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "expenses.json"
BUDGET_FILE = "budget.json"

# 🎨 Emoji map for categories
CATEGORY_EMOJI = {
    "food": "🍔", "mess": "🍱", "lunch": "🥗", "dinner": "🍛", "breakfast": "🍳",
    "travel": "🚕", "uber": "🚖", "bus": "🚌", "train": "🚆", "fuel": "⛽",
    "shopping": "🛍️", "clothes": "👕", "shoes": "👟",
    "bills": "💡", "electricity": "🔌", "water": "💧", "internet": "🌐", "rent": "🏠",
    "movie": "🎬", "entertainment": "🎮", "game": "🎮",
    "medical": "💊", "doctor": "👨‍⚕️", "medicine": "💊",
    "education": "📚", "books": "📖", "fees": "🎓",
    "grocery": "🛒", "vegetables": "🥦", "fruits": "🍎",
    "general": "💰"
}

def get_emoji(category):
    for key in CATEGORY_EMOJI:
        if key in category.lower():
            return CATEGORY_EMOJI[key]
    return "💰"

# ---------- FILE HANDLING ----------
def load_expenses():
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except:
        return []

def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)

def load_budget():
    try:
        with open(BUDGET_FILE, "r") as f:
            return json.load(f).get("budget", 0)
    except:
        return 0

def save_budget(amount):
    with open(BUDGET_FILE, "w") as f:
        json.dump({"budget": amount}, f)

# ---------- FEATURES ----------
def add_expense(amount, category, currency="₹"):
    expenses = load_expenses()
    emoji = get_emoji(category)
    expenses.append({
        "amount": amount,
        "category": category,
        "emoji": emoji,
        "currency": currency,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_expenses(expenses)

    # 🎭 Random replies
    replies = [
        f"Got it! Added {currency}{amount} for {category} {emoji}",
        f"Noted! {currency}{amount} spent on {category} ✅ {emoji}",
        f"Okay, {currency}{amount} for {category} saved! 💾 {emoji}",
        f"Done! {emoji} {currency}{amount} added under {category}",
        f"Recorded ✍️ {currency}{amount} → {category} {emoji}"
    ]
    reply = random.choice(replies)

    # 💸 Budget alert
    budget = load_budget()
    if budget > 0:
        total = sum(e['amount'] for e in expenses)
        if total > budget:  # Fixed: Changed from >= to >
            reply += f"\n⚠️ ALERT! You crossed your budget of ₹{budget}! Total spent: ₹{total}"
        elif total >= budget * 0.8:
            reply += f"\n⚠️ Warning! You've used 80% of your budget (₹{total}/₹{budget})"

    return reply

def show_expenses():
    expenses = load_expenses()
    if not expenses:
        return "No expenses found. 📭"

    result = "📋 Your Expenses:\n"
    for i, e in enumerate(expenses, 1):
        emoji = e.get("emoji", "💰")
        currency = e.get("currency", "₹")
        result += f"{i}. {emoji} {currency}{e['amount']} - {e['category']} ({e['date']})\n"
    return result

def delete_expense(index):
    expenses = load_expenses()
    if 0 < index <= len(expenses):
        removed = expenses.pop(index - 1)
        save_expenses(expenses)
        currency = removed.get("currency", "₹")
        return f"🗑️ Deleted {currency}{removed['amount']} ({removed['category']})"
    return "❌ Invalid index!"

def show_summary():
    expenses = load_expenses()
    if not expenses:
        return "No expenses yet! 📭"

    total = sum(e['amount'] for e in expenses)
    budget = load_budget()

    result = f"💰 Total spent: ₹{total}\n"
    if budget > 0:
        remaining = budget - total
        result += f"🎯 Budget: ₹{budget}\n"
        if remaining >= 0:
            result += f"✅ Remaining: ₹{remaining}\n"
        else:
            result += f"⚠️ Over budget by: ₹{abs(remaining)}\n"

    # 🏆 Top spending category
    cat_totals = {}
    for e in expenses:
        cat_totals[e['category']] = cat_totals.get(e['category'], 0) + e['amount']

    if cat_totals:
        top_cat = max(cat_totals, key=cat_totals.get)
        emoji = get_emoji(top_cat)
        result += f"🏆 Top spending: {emoji} {top_cat} (₹{cat_totals[top_cat]})"

    return result

def search_expense(category):
    expenses = load_expenses()
    results = [e for e in expenses if category.lower() in e['category'].lower()]

    if not results:
        return f"🔍 No matching expenses found for '{category}'."

    result = f"🔍 Results for '{category}':\n"
    for e in results:
        emoji = e.get("emoji", "💰")
        currency = e.get("currency", "₹")
        result += f"{emoji} {currency}{e['amount']} - {e['category']} ({e['date']})\n"
    return result

# 📅 Date filter
def filter_by_date(period):
    expenses = load_expenses()
    today = datetime.now()
    filtered = []

    for e in expenses:
        try:
            exp_date = datetime.strptime(e['date'], "%Y-%m-%d %H:%M")
        except (ValueError, KeyError):
            # Skip invalid date entries
            continue

        if period == "today" and exp_date.date() == today.date():
            filtered.append(e)
        elif period == "month" and exp_date.month == today.month and exp_date.year == today.year:
            filtered.append(e)
        elif period == "week":
            diff = (today - exp_date).days
            if 0 <= diff <= 7:
                filtered.append(e)

    if not filtered:
        return f"📅 No expenses found for {period}."

    total = sum(e['amount'] for e in filtered)
    result = f"📅 Expenses for {period.upper()}:\n"
    for e in filtered:
        emoji = e.get("emoji", "💰")
        currency = e.get("currency", "₹")
        result += f"{emoji} {currency}{e['amount']} - {e['category']} ({e['date']})\n"
    result += f"\n💰 Total: {currency}{total}"
    return result

# ✏️ Edit expense
def edit_expense(index, new_amount):
    expenses = load_expenses()
    if 0 < index <= len(expenses):
        old_amount = expenses[index-1]['amount']
        currency = expenses[index-1].get("currency", "₹")
        expenses[index-1]['amount'] = new_amount
        save_expenses(expenses)
        return f"✏️ Updated expense #{index}: {currency}{old_amount} → {currency}{new_amount}"
    return "❌ Invalid expense number!"

# ---------- CHATBOT LOGIC ----------
def extract_amount(text):
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else None

def extract_currency(text):
    if "$" in text or "dollar" in text.lower():
        return "$"
    elif "€" in text or "euro" in text.lower():
        return "€"
    elif "£" in text or "pound" in text.lower():
        return "£"
    return "₹"

def extract_category(text):
    # First try to find after prepositions
    match = re.search(r'(?:on|for|in|at|to|from)\s+([a-zA-Z ]+)', text.lower())
    if match:
        return match.group(1).strip()
    
    # If no preposition, extract words and filter
    words = re.findall(r'[a-zA-Z]+', text)
    skip = {
        "i", "spent", "spend", "add", "paid", "pay", "buy", "bought",
        "rs", "rupees", "dollar", "dollars", "euro", "pound", "for", "on", 
        "at", "in", "to", "from", "with", "about", "of", "the", "and", "or",
        "my", "your", "our", "their", "me", "you", "us", "them"
    }
    words = [w for w in words if w.lower() not in skip]
    return words[-1] if words else "general"

def chatbot_response(user_input):
    user_input = user_input.lower().strip()

    # 👋 Greetings
    greetings = ["hi","hii", "hello", "hey", "good morning", "good evening", "good afternoon"]
    if any(g == user_input or user_input.startswith(g + " ") for g in greetings):
        return random.choice([
            "Hey there! 👋 Ready to track your expenses?",
            "Hello! 😊 How can I help you today?",
            "Hi! 🌟 What did you spend on today?",
            "Hey! 💰 Let's manage your money smartly!",
            "Hello friend! 👋 Tell me about your expenses."
        ])

    # 🙏 Thanks
    if "thank" in user_input:
        return random.choice([
            "You're welcome! 💖",
            "Anytime! 😊",
            "Happy to help! 🌟",
            "My pleasure! 🤗"
        ])

    # 👋 Bye
    if any(word in user_input for word in ["bye", "goodbye", "see you","thank you"]):
        return random.choice([
            "Goodbye! Spend wisely! 👋",
            "See you later! 💰",
            "Bye bye! Take care! 🌟"
        ])

    # 🤖 How are you
    if "how are you" in user_input:
        return "I'm great! 🤖 Ready to help you save money! How about you?"

    # ❓ Help
    if "help" in user_input:
        return """🆘 Here's what I can do:
💸 add 500 on food → Add expense
📋 show → Show all expenses
📅 today / this month / this week → Filter by date
🔍 search food → Search expenses
📊 summary → View totals + top category
✏️ edit 2 to 600 → Edit expense #2
🗑 delete 1 → Delete expense #1
🎯 set budget → Set monthly budget
👋 hi, bye, thanks → Chat with me!"""

    # 📅 Date filters
    if "today" in user_input:
        return filter_by_date("today")
    if "this month" in user_input or "month" in user_input:
        return filter_by_date("month")
    if "this week" in user_input or "week" in user_input:
        return filter_by_date("week")

    # ✏️ Edit
    if "edit" in user_input or "change" in user_input or "update" in user_input:
        numbers = re.findall(r'\d+', user_input)
        if len(numbers) >= 2:
            return edit_expense(int(numbers[0]), int(numbers[1]))
        return "✏️ Format: edit 2 to 600 (edits expense #2 to ₹600)"

    # 🎯 Budget
    if "budget" in user_input:
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            save_budget(int(numbers[0]))
            return f"🎯 Budget set to ₹{numbers[0]}! I'll alert you when you cross it."
        budget = load_budget()
        if budget > 0:
            return f"🎯 Your current budget: ₹{budget}"
        return "🎯 Say: 'set budget 5000' to set your monthly budget"

    # 💸 Add expense
    if any(word in user_input for word in ["add", "spent", "spend", "pay", "paid", "buy", "bought"]):
        amount = extract_amount(user_input)
        category = extract_category(user_input)
        currency = extract_currency(user_input)
        if amount:
            return add_expense(amount, category, currency)
        return "💡 Please specify amount! Example: 'spent 500 on food'"

    # 📋 Show
    if "show" in user_input or "list" in user_input:
        return show_expenses()

    # 🗑 Delete
    if "delete" in user_input or "remove" in user_input:
        index = extract_amount(user_input)
        return delete_expense(index) if index else "🗑 Give expense number to delete."

    # 📊 Summary
    if "summary" in user_input or "total" in user_input:
        return show_summary()

    # 🔍 Search
    if "search" in user_input or "find" in user_input:
        parts = user_input.split()
        if len(parts) > 1:
            return search_expense(parts[-1])
        return "🔍 Please specify category to search."

    # 🧹 Clear
    if "clear" in user_input:
        # Add confirmation
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to delete all expenses?"):
            save_expenses([])
            return "🧹 All expenses cleared!"
        return "Clear operation cancelled."

    # 🚪 Exit
    if "exit" in user_input or "quit" in user_input:
        return "exit"

    return "🤔 I didn't understand. Type 'help' to see what I can do!"

# ---------- GRAPH ----------
def show_graph():
    expenses = load_expenses()
    if not expenses:
        add_message("📊 No data for graph.", "bot")
        return

    data = {}
    for e in expenses:
        data[e["category"]] = data.get(e["category"], 0) + e["amount"]

    plt.figure(figsize=(8, 6))
    plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.show()

# 🔍 Search popup
def open_search_popup():
    popup = tk.Toplevel(root)
    popup.title("Search Expense")
    popup.geometry("300x130")
    popup.configure(bg="#2c2c3e")

    tk.Label(popup, text="Enter category to search:",
             bg="#2c2c3e", fg="white",
             font=("Segoe UI", 11)).pack(pady=10)

    search_entry = tk.Entry(popup, font=("Segoe UI", 11))
    search_entry.pack(pady=5, padx=20, fill="x")

    def do_search():
        category = search_entry.get().strip()
        if category:
            add_message(search_expense(category), "bot")
            popup.destroy()

    tk.Button(popup, text="Search", command=do_search,
              bg="#4CAF50", fg="white",
              font=("Segoe UI", 11, "bold"),
              bd=0, padx=10, pady=5).pack(pady=5)

    search_entry.bind("<Return>", lambda e: do_search())
    search_entry.focus()

# 🎯 Set budget dialog
def set_budget_dialog():
    """Set budget using a dialog window"""
    amount = simpledialog.askinteger("Set Budget", "Enter monthly budget (₹):", parent=root)
    if amount and amount > 0:
        save_budget(amount)
        add_message(f"🎯 Budget set to ₹{amount}! I'll alert you when you're close.", "bot")
    elif amount == 0:
        add_message("❌ Budget must be greater than 0!", "bot")

# ---------- MESSAGE UI ----------
def add_message(msg, sender="bot"):
    """Add a message to the chat window"""
    frame = tk.Frame(chat_container, bg="#1e1e2f")

    if sender == "user":
        bubble = tk.Label(frame, text=msg, bg="#4CAF50", fg="white",
                          font=("Segoe UI", 11), wraplength=400,
                          padx=12, pady=8, justify="left")
        bubble.pack(anchor="e", padx=10)
    else:
        bubble = tk.Label(frame, text=msg, bg="#2f3142", fg="white",
                          font=("Segoe UI", 11), wraplength=400,
                          padx=12, pady=8, justify="left")
        bubble.pack(anchor="w", padx=10)

    frame.pack(fill="x", pady=2)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

# ---------- SEND ----------
def send_message(event=None):
    """Send user message and get bot response"""
    text = entry.get().strip()
    if not text:
        return

    add_message(text, "user")
    reply = chatbot_response(text)

    if reply == "exit":
        if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
            root.quit()
    else:
        add_message(reply, "bot")

    entry.delete(0, tk.END)

# 🔔 Daily reminder (shows on startup)
def show_reminder():
    """Show daily reminder on startup"""
    expenses = load_expenses()
    today = datetime.now().date()
    today_expenses = []
    
    for e in expenses:
        try:
            exp_date = datetime.strptime(e['date'], "%Y-%m-%d %H:%M").date()
            if exp_date == today:
                today_expenses.append(e)
        except (ValueError, KeyError):
            continue

    if not today_expenses:
        add_message("🔔 Reminder: You haven't tracked any expenses today!", "bot")
    else:
        total = sum(e['amount'] for e in today_expenses)
        add_message(f"📊 You've spent ₹{total} today ({len(today_expenses)} items)", "bot")

# ---------- GUI ----------
root = tk.Tk()
root.title("AI Expense Manager")
root.geometry("900x600")
root.configure(bg="#1e1e2f")

# Sidebar
sidebar = tk.Frame(root, bg="#2c2c3e", width=220)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False)

tk.Label(sidebar, text="💰 Expense AI", bg="#2c2c3e", fg="white",
         font=("Segoe UI", 16, "bold")).pack(pady=20)

btn_style = {"font":("Segoe UI",11),"bg":"#3a3d5c","fg":"white","bd":0,"padx":10,"pady":8}

tk.Button(sidebar, text="📋 Show Expenses",
          command=lambda: add_message(show_expenses(),"bot"),
          **btn_style).pack(fill="x", pady=5, padx=10)

tk.Button(sidebar, text="📊 Summary",
          command=lambda: add_message(show_summary(),"bot"),
          **btn_style).pack(fill="x", pady=5, padx=10)

tk.Button(sidebar, text="🔍 Search",
          command=open_search_popup,
          **btn_style).pack(fill="x", pady=5, padx=10)

tk.Button(sidebar, text="📅 Today",
          command=lambda: add_message(filter_by_date("today"),"bot"),
          **btn_style).pack(fill="x", pady=5, padx=10)

tk.Button(sidebar, text="📆 This Month",
          command=lambda: add_message(filter_by_date("month"),"bot"),
          **btn_style).pack(fill="x", pady=5, padx=10)

tk.Button(sidebar, text="🎯 Set Budget",
          command=set_budget_dialog,
          **btn_style).pack(fill="x", pady=5, padx=10)

tk.Button(sidebar, text="🗑 Clear All",
          command=lambda: [messagebox.askyesno("Confirm", "Clear all expenses?") and 
                          (save_expenses([]), add_message("🧹 All expenses cleared!", "bot"))],
          **btn_style).pack(fill="x", pady=5, padx=10)

tk.Button(sidebar, text="📈 Show Graph",
          command=show_graph,
          **btn_style).pack(fill="x", pady=5, padx=10)

# Chat area
main = tk.Frame(root, bg="#1e1e2f")
main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main, bg="#1e1e2f", highlightthickness=0)
scroll = tk.Scrollbar(main, command=canvas.yview)
chat_container = tk.Frame(canvas, bg="#1e1e2f")

canvas_window = canvas.create_window((0,0), window=chat_container, anchor="nw", width=680)

def resize_chat(event):
    """Resize chat area dynamically"""
    canvas.itemconfig(canvas_window, width=event.width - 10)

canvas.bind("<Configure>", resize_chat)
chat_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Input
bottom = tk.Frame(main, bg="#1e1e2f")
bottom.pack(side=tk.BOTTOM,fill=tk.X, padx=10, pady=10)

entry = tk.Entry(bottom, font=("Segoe UI", 12), bd=0)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10), ipady=8)

tk.Button(bottom, text="➤", command=send_message,
          bg="#4CAF50", fg="white",
          font=("Segoe UI",12,"bold"),
          bd=0, padx=15, pady=5).pack(side=tk.RIGHT)

entry.bind("<Return>", send_message)

# Welcome messages
add_message("👋 Welcome! I'm your Expense Assistant.", "bot")
add_message("💡 Type 'help' to see what I can do!", "bot")
show_reminder()  # 🔔 Daily reminder

root.mainloop()
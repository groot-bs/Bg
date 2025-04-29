from flask import Flask, render_template, request, redirect, url_for, flash
import json
import uuid
from datetime import datetime, date
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# File paths
DATA_FILE = 'data/data.json'
DAILY_FILE = 'data/daily_display.json'
SEEN_FILE = 'data/user_seen.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize JSON files if they don't exist
for file in [DATA_FILE, DAILY_FILE, SEEN_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump([] if file != DAILY_FILE else {}, f)

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    # Load daily display and seen texts
    daily = load_json(DAILY_FILE)
    seen = load_json(SEEN_FILE)
    texts = load_json(DATA_FILE)
    
    # Get current date
    today = str(date.today())
    
    # Check if we need to select a new text
    if daily.get('date') != today or not daily.get('text_id'):
        # Filter out seen texts
        available_texts = [t for t in texts if t['id'] not in seen]
        
        if available_texts:
            # Select first available text
            selected_text = available_texts[0]
            daily = {'date': today, 'text_id': selected_text['id']}
            save_json(DAILY_FILE, daily)
        else:
            # If no new texts, clear seen and try again
            save_json(SEEN_FILE, [])
            available_texts = texts
            if available_texts:
                selected_text = available_texts[0]
                daily = {'date': today, 'text_id': selected_text['id']}
                save_json(DAILY_FILE, daily)
            else:
                selected_text = None
    
    else:
        # Find the text for today's ID
        selected_text = next((t for t in texts if t['id'] == daily['text_id']), None)
    
    return render_template('index.html', text=selected_text)

@app.route('/see_again', methods=['POST'])
def see_again():
    # Clear seen texts
    save_json(SEEN_FILE, [])
    flash('You can now see previously viewed texts again!')
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    texts = load_json(DATA_FILE)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            new_text = {
                'id': str(uuid.uuid4()),
                'sanskrit': request.form.get('sanskrit'),
                'english': request.form.get('english'),
                'hindi': request.form.get('hindi')
            }
            texts.append(new_text)
            save_json(DATA_FILE, texts)
            flash('Text added successfully!')
        
        elif action == 'edit':
            text_id = request.form.get('id')
            for text in texts:
                if text['id'] == text_id:
                    text['sanskrit'] = request.form.get('sanskrit')
                    text['english'] = request.form.get('english')
                    text['hindi'] = request.form.get('hindi')
                    break
            save_json(DATA_FILE, texts)
            flash('Text updated successfully!')
        
        elif action == 'delete':
            text_id = request.form.get('id')
            texts = [t for t in texts if t['id'] != text_id]
            save_json(DATA_FILE, texts)
            flash('Text deleted successfully!')
        
        return redirect(url_for('admin'))
    
    return render_template('admin.html', texts=texts)

@app.route('/edit/<text_id>')
def edit_text(text_id):
    texts = load_json(DATA_FILE)
    text = next((t for t in texts if t['id'] == text_id), None)
    return render_template('admin.html', texts=texts, edit_text=text)

@app.route('/mark_seen/<text_id>')
def mark_seen(text_id):
    seen = load_json(SEEN_FILE)
    if text_id not in seen:
        seen.append(text_id)
        save_json(SEEN_FILE, seen)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

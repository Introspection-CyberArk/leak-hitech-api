#!/usr/bin/env python3
# Telegram Leak Search Bot - Simplified Vercel Version
# Powered by @Introspection007

import os
import re
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ============================================
# CONFIGURATION
# ============================================
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8943932232:AAFPJ0LQ1_BZWuizo_c-AHA_znztujtDgws")
API_ENDPOINT = "https://ukraine-xinfo-onrender-leak.42web.io/leak-api.php"
API_KEY = "TusharT"
DEVELOPER = "@Introspection007"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ============================================
# TELEGRAM FUNCTIONS
# ============================================

def send_message(chat_id, text, parse_mode="Markdown"):
    """Send message to Telegram"""
    url = f"{TELEGRAM_API}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, json=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def query_leak_api(term: str):
    """Query the leak API"""
    params = {"key": API_KEY, "type": "leakk", "term": term}
    try:
        response = requests.get(API_ENDPOINT, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        return {"success": False, "message": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"success": False, "message": str(e)}

def format_leak_results(data: dict, term: str) -> str:
    """Format leak data beautifully"""
    
    if not data.get("success"):
        return f"❌ No results found for `{term}`"
    
    result = data.get("result", {})
    sources = result.get("data", {})
    
    if not sources:
        return f"🔍 No leak records found for `{term}`"
    
    msg = f"🔍 **LEAK RESULTS for:** `{term}`\n\n"
    
    for source_name, source_data in sources.items():
        title = source_data.get("title", source_name)
        records = source_data.get("records", [])
        
        msg += f"📁 **{title}**\n"
        
        for idx, record in enumerate(records, 1):
            msg += f"  👤 **Record {idx}:**\n"
            for field, value in record.items():
                if value and len(str(value)) < 200:
                    field_name = field.replace("_", " ").title()
                    if "phone" in field.lower():
                        msg += f"    ├ 📱 {field_name}: `{value}`\n"
                    elif "email" in field.lower():
                        msg += f"    ├ 📧 {field_name}: `{value}`\n"
                    else:
                        msg += f"    ├ {field_name}: `{value}`\n"
            msg += "\n"
    
    msg += f"---\n🤖 **Powered by:** {DEVELOPER}"
    return msg

# ============================================
# WEBHOOK HANDLER
# ============================================

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    """Handle incoming Telegram updates"""
    try:
        update = request.get_json()
        if not update:
            return jsonify({"status": "ok"})
        
        message = update.get("message")
        if not message:
            return jsonify({"status": "ok"})
        
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").strip()
        
        if not chat_id:
            return jsonify({"status": "ok"})
        
        # Handle commands
        if text == "/start":
            send_message(chat_id, "🔍 **Leak Search Bot**\n\nSend a phone number to search for leaks.\n\nExample: `916239545693`\n\n🤖 Powered by @Introspection007")
        elif text.startswith("/search"):
            parts = text.split(maxsplit=1)
            if len(parts) > 1:
                term = parts[1]
                send_message(chat_id, f"🔎 Searching `{term}`...")
                result = query_leak_api(term)
                formatted = format_leak_results(result, term)
                send_message(chat_id, formatted)
            else:
                send_message(chat_id, "❌ Usage: `/search 916239545693`")
        elif re.search(r'\d{10,15}', text):
            # Auto-detect phone number
            term = re.search(r'\d{10,15}', text).group()
            send_message(chat_id, f"🔎 Searching `{term}`...")
            result = query_leak_api(term)
            formatted = format_leak_results(result, term)
            send_message(chat_id, formatted)
        else:
            send_message(chat_id, "❌ Send a phone number or use /search")
        
        return jsonify({"status": "ok"})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error"}), 500

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "Leak Search Bot Running",
        "developer": DEVELOPER,
        "webhook": f"/webhook/{BOT_TOKEN[:10]}..."
    })

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

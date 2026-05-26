#!/usr/bin/env python3
# Telegram Leak Search Bot - Vercel Webhook Version
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

# Telegram API URLs
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ============================================
# HELPER FUNCTIONS
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
        print(f"Error sending message: {e}")
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
        return f"❌ No results found for `{term}`\n\n💡 Try another phone number."
    
    result = data.get("result", {})
    sources = result.get("data", {})
    
    if not sources:
        return f"🔍 No leak records found for `{term}`"
    
    msg = f"🔍 **LEAK SEARCH RESULTS**\n"
    msg += f"├ Query: `{term}`\n"
    msg += f"├ Requested by: `{data.get('requested_by', 'Unknown')}`\n"
    msg += f"└ Valid until: `{data.get('valid_till', 'N/A')}`\n\n"
    
    total_records = 0
    
    for source_name, source_data in sources.items():
        title = source_data.get("title", source_name)
        description = source_data.get("description", "")
        records = source_data.get("records", [])
        total_records += len(records)
        
        msg += f"📁 **{title}**\n"
        if description:
            if len(description) > 200:
                description = description[:197] + "..."
            msg += f"└ {description}\n\n"
        
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
            
            msg += f"    └ {'─' * 25}\n"
        
        msg += "\n"
    
    msg += f"📊 **Total records:** {total_records}\n\n"
    msg += f"---\n"
    msg += f"🤖 **Powered by:** {DEVELOPER}\n"
    msg += f"⚠️ Data from public leaks. Use responsibly."
    
    return msg

# ============================================
# BOT COMMAND HANDLERS
# ============================================

def handle_start(chat_id):
    """Handle /start command"""
    welcome_msg = (
        f"🔍 **Leak Search Bot**\n\n"
        f"Search for leaked data from major breaches including:\n"
        f"• 📱 TrueCaller India (286M records)\n"
        f"• 💾 HiTeckGroop (1.8B records)\n\n"
        f"**Commands:**\n"
        f"/search `<phone>` - Search for leaks\n"
        f"/help - Show help\n\n"
        f"**Example:**\n"
        f"`/search 916239545693`\n\n"
        f"🤖 **Powered by:** {DEVELOPER}"
    )
    send_message(chat_id, welcome_msg)

def handle_help(chat_id):
    """Handle /help command"""
    help_msg = (
        f"📖 **Help Guide**\n\n"
        f"**Usage:**\n"
        f"Send a phone number or use /search command\n\n"
        f"**Example queries:**\n"
        f"`916239545693`\n"
        f`"/search 916239545693`\n\n"
        f"**What data can you find?**\n"
        f"• Full name\n"
        f"• Father's name\n"
        f"• Aadhaar/Document number\n"
        f"• Address\n"
        f"• Email (if available)\n"
        f"• Carrier/Region info\n\n"
        f"🤖 **Powered by:** {DEVELOPER}"
    )
    send_message(chat_id, help_msg)

def handle_search(chat_id, term):
    """Handle search command"""
    send_message(chat_id, f"🔎 Searching `{term}` in leak databases...\n⏳ Please wait")
    
    result = query_leak_api(term)
    formatted = format_leak_results(result, term)
    
    # Split long messages
    if len(formatted) > 4096:
        parts = [formatted[i:i+4096] for i in range(0, len(formatted), 4096)]
        for part in parts:
            send_message(chat_id, part)
    else:
        send_message(chat_id, formatted)

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
        
        # Extract message info
        message = update.get("message")
        if not message:
            return jsonify({"status": "ok"})
        
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "").strip()
        
        if not chat_id:
            return jsonify({"status": "ok"})
        
        # Handle commands
        if text.startswith("/"):
            if text == "/start":
                handle_start(chat_id)
            elif text == "/help":
                handle_help(chat_id)
            elif text.startswith("/search"):
                parts = text.split(maxsplit=1)
                if len(parts) > 1:
                    handle_search(chat_id, parts[1])
                else:
                    send_message(chat_id, "❌ Usage: `/search <phone_number>`")
            else:
                send_message(chat_id, "❌ Unknown command. Use /start or /help")
        else:
            # Auto-detect phone numbers
            if re.search(r'\d{10,15}', text):
                handle_search(chat_id, text)
            else:
                send_message(chat_id, "❌ Send a valid phone number or use /search command")
        
        return jsonify({"status": "ok"})
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"status": "error"}), 500

@app.route("/", methods=["GET"])
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "Leak Search Bot is running",
        "developer": DEVELOPER,
        "endpoint": f"/webhook/{BOT_TOKEN[:10]}... (POST only)"
    })

# ============================================
# MAIN (for local testing)
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

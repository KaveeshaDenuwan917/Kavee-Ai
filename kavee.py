import wikipedia
from flask import Flask, request, render_template_string
from googletrans import Translator

app = Flask(__name__)
translator = Translator()
wikipedia.set_lang("en")

def search_and_translate(query):
    # සිංග්ලිෂ් වචන වල හැම ප්‍රභේදයක්ම (Variations) මෙතනට දාලා තියෙන්නේ
    bad_words = [
        "kauda", "kuda", "kawuda", "mokakda", "mokadda", "mkkda", "mokak",
        "koheda", "kheda", "monada", "mnd", "kiyanna", "kynna",
        "gana", "kiyanne", "ekak", "vage", "wage", "da", "d", "is", "what", "who","oya","mata","haduve"
    ]
    
    # 1. පිරිසිදු කිරීම: ප්‍රශ්නය වචන වලට කඩා අනවශ්‍ය දෑ ඉවත් කිරීම
    words = query.lower().replace("?", "").replace(".", "").split()
    filtered_words = [w for w in words if w not in bad_words]
    clean_query = " ".join(filtered_words).strip()
    
    if not clean_query:
        return "කරුණාකර ඔබට දැනගැනීමට අවශ්‍ය මාතෘකාව සඳහන් කරන්න."

    try:
        # 2. Wikipedia සෙවීම
        wiki_res = wikipedia.summary(clean_query, sentences=2)
        translated = translator.translate(wiki_res, src='en', dest='si')
        return translated.text
        
    except Exception:
        # 3. සර්ච් එක අසාර්ථක වුණොත් (උදා: Wennappuwa වගේ ඒවාට Summary එකක් නැති වුණොත්)
        try:
            trans_only = translator.translate(clean_query, src='en', dest='si')
            return f"සවිස්තරාත්මක විස්තරයක් නැතත්, '{clean_query}' යනු: {trans_only.text}"
        except:
            return "සමාවෙන්න, මට ඒ ගැන තොරතුරු සොයාගැනීමට අපහසුයි."

@app.route("/", methods=["GET", "POST"])
def home():
    res = ""
    if request.method == "POST":
        user_msg = request.form.get("txt").strip()
        low_msg = user_msg.lower()
        
        # පෞද්ගලික Q&A
        if any(x in low_msg for x in ["oyava haduve kauda", "creator"]):
            res = "මාව නිර්මාණය කළේ (Kaveesha Denuwan) විසින්."
        elif any(x in low_msg for x in ["oyage nama mokak da", "name"]):
            res = "මගේ නම KAVEE AI."
        else:
            res = search_and_translate(user_msg)
            
    return render_template_string('''
        <body style="text-align:center; padding:50px; font-family:sans-serif; background:#0f0c29; color:white;">
            <div style="background:rgba(255,255,255,0.1); padding:40px; border-radius:20px; display:inline-block; width:90%; max-width:500px; border:1px solid #00d2ff;">
                <h1 style="color:#00d2ff;">🧠 KAVEE AI</h1>
                <form method="POST">
                    <input type="text" name="txt" style="width:80%; padding:15px; border-radius:30px;" placeholder="Ask anything..." required>
                    <br><br>
                    <button type="submit" style="background:#00d2ff; padding:10px 30px; border-radius:30px; border:none; font-weight:bold; cursor:pointer;">ASK ANYTHING</button>
                </form>
                {% if res %}<div style="margin-top:25px; text-align:left; background:rgba(0,0,0,0.5); padding:20px; border-radius:15px; border-left:5px solid #00d2ff;">{{ res }}</div>{% endif %}
            </div>
        </body>
    ''', res=res)

if __name__ == "__main__":
    app.run(debug=False, port=5000)
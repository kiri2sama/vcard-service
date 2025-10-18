from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)
vcards = {}

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
<title>Create vCard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}
.container{max-width:600px;margin:40px auto;background:rgba(255,255,255,0.95);backdrop-filter:blur(10px);border-radius:20px;padding:40px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
h1{font-size:32px;font-weight:700;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:30px;text-align:center}
.form-group{margin-bottom:20px}
label{display:block;font-weight:600;color:#333;margin-bottom:8px;font-size:14px}
input,textarea{width:100%;padding:12px 16px;border:2px solid #e0e0e0;border-radius:10px;font-size:15px;transition:all 0.3s;font-family:inherit}
input:focus,textarea:focus{outline:none;border-color:#667eea;box-shadow:0 0 0 3px rgba(102,126,234,0.1)}
textarea{resize:vertical;min-height:80px}
button{width:100%;padding:14px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer;transition:transform 0.2s,box-shadow 0.2s}
button:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(102,126,234,0.4)}
button:active{transform:translateY(0)}
.divider{height:1px;background:linear-gradient(90deg,transparent,#e0e0e0,transparent);margin:30px 0}
</style>
</head>
<body>
<div class="container">
<h1>✨ Create vCard</h1>
<form method="POST" action="/api/vcards">
<div class="form-group"><label>Card Name</label><input name="cardName" required></div>
<div class="form-group"><label>Email (for editing)</label><input name="email" type="email" required></div>
<div class="form-group"><label>Password</label><input name="password" type="password" required></div>
<div class="divider"></div>
<div class="form-group"><label>First Name</label><input name="firstName" required></div>
<div class="form-group"><label>Last Name</label><input name="lastName" required></div>
<div class="form-group"><label>Organization</label><input name="organization"></div>
<div class="form-group"><label>Position</label><input name="position"></div>
<div class="form-group"><label>Phone</label><input name="phone" type="tel"></div>
<div class="form-group"><label>Email Contact</label><input name="emailContact" type="email"></div>
<div class="form-group"><label>Website</label><input name="website" type="url"></div>
<div class="form-group"><label>Address</label><textarea name="address"></textarea></div>
<button type="submit">Create Card ✨</button>
</form>
</div>
</body>
</html>
'''

VCARD_VIEW = '''
<!DOCTYPE html>
<html>
<head>
<title>{{ name }}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh;padding:20px}
.card{max-width:600px;margin:40px auto;background:rgba(255,255,255,0.95);backdrop-filter:blur(10px);border-radius:20px;padding:40px;box-shadow:0 20px 60px rgba(0,0,0,0.3)}
.avatar{width:120px;height:120px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);margin:0 auto 20px;display:flex;align-items:center;justify-content:center;font-size:48px;color:white;font-weight:700;box-shadow:0 10px 30px rgba(102,126,234,0.3)}
h1{font-size:32px;font-weight:700;color:#333;text-align:center;margin-bottom:8px}
.position{font-size:18px;color:#667eea;text-align:center;font-weight:600;margin-bottom:6px}
.org{font-size:16px;color:#888;text-align:center;margin-bottom:30px}
.contact-item{display:flex;align-items:center;padding:16px;background:#f8f9fa;border-radius:12px;margin-bottom:12px;transition:all 0.3s}
.contact-item:hover{background:#e9ecef;transform:translateX(4px)}
.contact-icon{width:40px;height:40px;border-radius:10px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:white;font-size:18px;margin-right:16px;flex-shrink:0}
.contact-label{font-weight:600;color:#666;font-size:13px;margin-bottom:4px}
.contact-value{color:#333;font-size:15px}
.contact-value a{color:#667eea;text-decoration:none}
.contact-value a:hover{text-decoration:underline}
.btn{display:block;width:100%;padding:16px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;text-align:center;text-decoration:none;border-radius:12px;font-size:16px;font-weight:600;margin-top:30px;transition:transform 0.2s,box-shadow 0.2s}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(102,126,234,0.4)}
</style>
</head>
<body>
<div class="card">
<div class="avatar">{{ name[0] }}</div>
<h1>{{ name }}</h1>
{% if position %}<div class="position">{{ position }}</div>{% endif %}
{% if organization %}<div class="org">{{ organization }}</div>{% endif %}
<div style="margin-top:30px">
{% if phone %}
<div class="contact-item">
<div class="contact-icon">📱</div>
<div><div class="contact-label">Phone</div><div class="contact-value"><a href="tel:{{ phone }}">{{ phone }}</a></div></div>
</div>
{% endif %}
{% if email %}
<div class="contact-item">
<div class="contact-icon">✉️</div>
<div><div class="contact-label">Email</div><div class="contact-value"><a href="mailto:{{ email }}">{{ email }}</a></div></div>
</div>
{% endif %}
{% if website %}
<div class="contact-item">
<div class="contact-icon">🌐</div>
<div><div class="contact-label">Website</div><div class="contact-value"><a href="{{ website }}" target="_blank">{{ website }}</a></div></div>
</div>
{% endif %}
{% if address %}
<div class="contact-item">
<div class="contact-icon">📍</div>
<div><div class="contact-label">Address</div><div class="contact-value">{{ address }}</div></div>
</div>
{% endif %}
</div>
<a href="/api/vcards/{{ slug }}/download" class="btn">💾 Save Contact</a>
</div>
</body>
</html>
'''

@app.route('/')
def home():
    return HTML_FORM

@app.route('/api/vcards', methods=['POST'])
def create_vcard():
    data = request.form.to_dict()
    slug = data['firstName'].lower() + '-' + str(int(datetime.now().timestamp()))
    vcards[slug] = data
    return f'<script>window.location.href="/c/{slug}"</script>'

@app.route('/c/<slug>')
def view_vcard(slug):
    if slug not in vcards:
        return 'vCard not found', 404
    v = vcards[slug]
    return render_template_string(VCARD_VIEW, 
        slug=slug,
        name=f"{v.get('firstName','')} {v.get('lastName','')}",
        position=v.get('position',''),
        organization=v.get('organization',''),
        phone=v.get('phone',''),
        email=v.get('emailContact',''),
        website=v.get('website',''),
        address=v.get('address',''))

@app.route('/api/vcards/<slug>/download')
def download_vcf(slug):
    if slug not in vcards:
        return 'Not found', 404
    v = vcards[slug]
    vcf = f"""BEGIN:VCARD
VERSION:3.0
FN:{v.get('firstName','')} {v.get('lastName','')}
N:{v.get('lastName','')};{v.get('firstName','')};;;
ORG:{v.get('organization','')}
TITLE:{v.get('position','')}
TEL:{v.get('phone','')}
EMAIL:{v.get('emailContact','')}
URL:{v.get('website','')}
ADR:;;{v.get('address','')};;;;
END:VCARD"""
    return vcf, 200, {'Content-Type': 'text/vcard', 'Content-Disposition': f'attachment; filename="{v.get("firstName","contact")}.vcf"'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6509, debug=True)

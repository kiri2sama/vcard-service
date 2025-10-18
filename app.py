from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime

app = Flask(__name__)
vcards = {}

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head><title>Create vCard</title></head>
<body style="max-width:600px;margin:40px auto;padding:20px;font-family:system-ui">
<h1>Create vCard</h1>
<form method="POST" action="/api/vcards">
<div style="margin-bottom:15px"><label>Card Name</label><input name="cardName" style="width:100%;padding:8px" required></div>
<div style="margin-bottom:15px"><label>Email (for editing)</label><input name="email" type="email" style="width:100%;padding:8px" required></div>
<div style="margin-bottom:15px"><label>Password</label><input name="password" type="password" style="width:100%;padding:8px" required></div>
<div style="margin-bottom:15px"><label>First Name</label><input name="firstName" style="width:100%;padding:8px" required></div>
<div style="margin-bottom:15px"><label>Last Name</label><input name="lastName" style="width:100%;padding:8px" required></div>
<div style="margin-bottom:15px"><label>Organization</label><input name="organization" style="width:100%;padding:8px"></div>
<div style="margin-bottom:15px"><label>Position</label><input name="position" style="width:100%;padding:8px"></div>
<div style="margin-bottom:15px"><label>Phone</label><input name="phone" style="width:100%;padding:8px"></div>
<div style="margin-bottom:15px"><label>Email Contact</label><input name="emailContact" type="email" style="width:100%;padding:8px"></div>
<div style="margin-bottom:15px"><label>Website</label><input name="website" style="width:100%;padding:8px"></div>
<div style="margin-bottom:15px"><label>Address</label><textarea name="address" style="width:100%;padding:8px"></textarea></div>
<button type="submit" style="padding:10px 20px;background:#0070f3;color:white;border:none;cursor:pointer">Create Card</button>
</form>
</body>
</html>
'''

VCARD_VIEW = '''
<!DOCTYPE html>
<html>
<head><title>{{ name }}</title></head>
<body style="max-width:600px;margin:40px auto;padding:20px;font-family:system-ui">
<div style="text-align:center;margin-bottom:30px">
<h1>{{ name }}</h1>
{% if position %}<p style="font-size:18px;color:#666">{{ position }}</p>{% endif %}
{% if organization %}<p style="font-size:16px;color:#888">{{ organization }}</p>{% endif %}
</div>
<div style="margin-bottom:20px">
{% if phone %}<div style="margin-bottom:10px"><strong>Phone:</strong> <a href="tel:{{ phone }}">{{ phone }}</a></div>{% endif %}
{% if email %}<div style="margin-bottom:10px"><strong>Email:</strong> <a href="mailto:{{ email }}">{{ email }}</a></div>{% endif %}
{% if website %}<div style="margin-bottom:10px"><strong>Website:</strong> <a href="{{ website }}" target="_blank">{{ website }}</a></div>{% endif %}
{% if address %}<div style="margin-bottom:10px"><strong>Address:</strong> {{ address }}</div>{% endif %}
</div>
<a href="/api/vcards/{{ slug }}/download" style="display:block;padding:10px 20px;background:#0070f3;color:white;text-align:center;text-decoration:none">Save Contact</a>
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

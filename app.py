
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

openai.api_key = "your-openai-api-key"

def analyze_patient_info(patient_info):
    prompt = f"Analyze the following patient information and provide ICF classification: {patient_info}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    icf_output = response['choices'][0]['message']['content']
    return icf_output

def send_email_report(email, report):
    msg = EmailMessage()
    msg['Subject'] = 'ICF Disability Report'
    msg['From'] = 'your@email.com'
    msg['To'] = email
    msg.set_content(f"""Here is your ICF report:

{report}
""")
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('your@email.com', 'your-email-password')
        smtp.send_message(msg)
    return True

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    patient_info = data.get('patient_info', '')
    email = data.get('email', '')
    icf_report = analyze_patient_info(patient_info)
    email_sent = False
    if email:
        try:
            send_email_report(email, icf_report)
            email_sent = email
        except:
            pass
    return jsonify({"ICF_Classification": icf_report, "Email_Sent": email_sent})

if __name__ == '__main__':
    app.run(debug=True)

import base64
import io
import qrcode
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Fiverr Portfolio</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #121212; color: #ffffff; text-align: center; padding: 40px 20px; }
        .container { max-width: 450px; margin: auto; background: #1e1e1e; padding: 30px; border-radius: 12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.5); border: 1px solid #2d2d2d; }
        h1 { color: #ff4757; font-size: 24px; margin-bottom: 5px; }
        p { color: #aaa; font-size: 14px; }
        input[type="text"] { width: 90%; padding: 12px; margin: 20px 0 10px 0; border-radius: 6px; border: 1px solid #333; background: #2d2d2d; color: white; outline: none; }
        button { background: #ff4757; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; width: 95%; transition: 0.3s; }
        button:hover { background: #ff6b81; }
        .result-box { margin-top: 25px; background: #252525; padding: 15px; border-radius: 8px; }
        img { max-width: 180px; margin-top: 10px; border-radius: 4px; border: 3px solid #fff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Python Developer Portfolio 🚀</h1>
        <p>Advanced Backend Solutions & Automation</p>
        <div style="border-top: 1px solid #333; margin: 20px 0;"></div>
        
        <h3>Live Tool: Instant QR Generator</h3>
        <form method="POST">
            <input type="text" name="url" placeholder="Enter URL or Text here..." required>
            <br>
            <button type="submit">Generate QR Code</button>
        </form>

        {% if qr_data %}
            <div class="result-box">
                <p style="color: #2ed573; font-weight: bold;">✔ QR Code Generated Successfully!</p>
                <img src="data:image/png;base64,{{ qr_data }}" alt="QR Code">
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    qr_base64 = None
    if request.method == "POST":
        user_input = request.form.get("url")

        qr = qrcode.QRCode(version=1, box_size=10, border=3)
        qr.add_data(user_input)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render_template_string(HTML_TEMPLATE, qr_data=qr_base64)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


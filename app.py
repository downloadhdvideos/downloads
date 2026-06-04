from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

MY_AFFILIATE_ID = "lambraine2026"

# গ্লোবাল লিস্ট যেখানে প্রোডাক্টগুলো জমা থাকবে
PRODUCTS = [
    {
        "title": "Premium Gaming Headphone",
        "price": "১,২০০",
        "old_price": "৩,০০০",
        "discount": "60% OFF",
        "source": "Daraz.com.bd",
        "original_link": "https://www.daraz.com.bd/products/gaming-headphone-i12345.html"
    }
]

def convert_to_affiliate_link(url, source):
    if "daraz.com.bd" in url.lower():
        return f"{url}?pid={MY_AFFILIATE_ID}&af_click_look=true"
    return url

# --- মূল হোমপেজ টেমপ্লেট ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lambraine official</title>
    <style>
        body { font-family: sans-serif; background-color: #121212; color: #fff; margin: 0; padding: 0; text-align: center; }
        header { background-color: #1f1f1f; padding: 20px; border-bottom: 3px solid #ff4757; }
        h1 { color: #ff4757; margin: 0; }
        .container { max-width: 800px; margin: 30px auto; padding: 20px; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; }
        .card { background: #1f1f1f; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.3); position: relative; text-align: left; }
        .badge { background: #2ed573; color: #fff; padding: 5px 10px; border-radius: 4px; font-weight: bold; position: absolute; top: 10px; right: 10px; }
        .price { color: #2ed573; font-size: 20px; font-weight: bold; }
        .btn { display: block; background: #ff4757; color: #fff; text-decoration: none; padding: 10px; border-radius: 5px; margin-top: 15px; text-align: center; font-weight: bold; }
        .track-info { font-size: 11px; color: #888; margin-top: 5px; font-style: italic; }
        .admin-btn { display: inline-block; margin-top: 15px; color: #ff4757; text-decoration: none; font-size: 14px; }
    </style>
</head>
<body>
    <header>
        <h1>Lambraine official</h1>
        <p>লাইভ ডিল ও ডিসকাউন্ট ড্যাশবোর্ড ⚡</p>
    </header>
    <div class="container">
        {% for product in products %}
        <div class="card">
            <span class="badge">{{ product.discount }}</span>
            <h3 style="margin-top: 25px;">{{ product.title }}</h3>
            <p class="price">৳{{ product.price }} <span style="text-decoration: line-through; color: #888; font-size: 14px;">৳{{ product.old_price }}</span></p>
            <p style="color:#ffa502; margin: 0;">Source: {{ product.source }}</p>
            <a href="{{ convert_link(product.original_link, product.source) }}" target="_blank" class="btn">ডিলটি দেখুন</a>
            <div class="track-info">ID: {{ my_id if "daraz" in product.source.lower() else "None" }} Connected</div>
        </div>
        {% endfor %}
    </div>
    <a href="/admin" class="admin-btn">Go to Secret Admin Panel →</a>
</body>
</html>
"""

# --- গোপন অ্যাডমিন প্যানেল টেমপ্লেট ---
ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel | Lambraine</title>
    <style>
        body { font-family: sans-serif; background-color: #121212; color: #fff; padding: 20px; text-align: center; }
        .form-box { max-width: 400px; margin: 30px auto; background: #1f1f1f; padding: 30px; border-radius: 8px; border: 1px solid #ff4757; text-align: left; }
        label { display: block; margin-top: 10px; color: #aaa; font-size: 14px; }
        input, select { width: 100%; padding: 10px; margin-top: 5px; background: #2d2d2d; border: 1px solid #444; color: #fff; border-radius: 4px; box-sizing: border-box; }
        .submit-btn { width: 100%; background: #2ed573; color: white; border: none; padding: 12px; margin-top: 20px; font-weight: bold; border-radius: 4px; cursor: pointer; }
        a { color: #ff4757; text-decoration: none; display: block; text-align: center; margin-top: 15px; }
    </style>
</head>
<body>
    <h1>Lambraine Admin Panel 🔐</h1>
    <p>নতুন ডিসকাউন্ট প্রোডাক্ট যোগ করো</p>
    <div class="form-box">
        <form method="POST">
            <label>প্রোডাক্টের নাম:</label>
            <input type="text" name="title" placeholder="e.g., Realme C53" required>
            
            <label>অফার মূল্য (৳):</label>
            <input type="text" name="price" placeholder="e.g., ৯,৫০০" required>
            
            <label>আসল মূল্য (৳):</label>
            <input type="text" name="old_price" placeholder="e.g., ১৫,০০০" required>
            
            <label>ডিসকাউন্ট পার্সেন্টেজ:</label>
            <input type="text" name="discount" placeholder="e.g., 36% OFF" required>
            
            <label>সোর্স (ওয়েবসাইট):</label>
            <select name="source">
                <option value="Daraz.com.bd">Daraz.com.bd</option>
                <option value="Bikroy.com">Bikroy.com</option>
                <option value="Other">Other</option>
            </select>
            
            <label>আসল প্রোডাক্ট লিংক:</label>
            <input type="url" name="original_link" placeholder="https://..." required>
            
            <button type="submit" class="submit-btn">প্রোডাক্ট লাইভ করো 🚀</button>
        </form>
        <a href="/">← ব্যাক টু হোমপেজ</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(
        HTML_TEMPLATE, 
        products=PRODUCTS, 
        convert_link=convert_to_affiliate_link,
        my_id=MY_AFFILIATE_ID
    )

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # ফর্ম থেকে ডেটা রিসিভ করা
        new_product = {
            "title": request.form['title'],
            "price": request.form['price'],
            "old_price": request.form['old_price'],
            "discount": request.form['discount'],
            "source": request.form['source'],
            "original_link": request.form['original_link']
        }
        # লিস্টে নতুন প্রোডাক্ট পুশ করা
        PRODUCTS.append(new_product)
        return redirect(url_for('home'))
    
    return render_template_string(ADMIN_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

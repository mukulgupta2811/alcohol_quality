from flask import Flask, request, render_template_string
import alcohol_model

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Wine Quality Predictor</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, sans-serif;
}

body {
    min-height: 100vh;
    background: linear-gradient(135deg, #16090c, #3b1019, #12070a);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 25px;
}

.container {
    width: 100%;
    max-width: 1100px;
    min-height: 650px;
    display: flex;
    overflow: hidden;
    border-radius: 28px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 0 25px 70px rgba(0,0,0,.55);
    backdrop-filter: blur(15px);
    animation: show .8s ease;
}

.left {
    width: 58%;
    padding: 45px;
    background: linear-gradient(145deg, rgba(25,8,12,.96), rgba(67,17,28,.88));
}

.badge {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 20px;
    background: rgba(214,77,101,.14);
    border: 1px solid rgba(255,130,150,.25);
    color: #ff9bae;
    font-size: 12px;
    letter-spacing: 1px;
    margin-bottom: 18px;
}

h1 {
    font-size: 42px;
    line-height: 1.1;
    margin-bottom: 12px;
}

h1 span {
    color: #ff718c;
}

.description {
    color: #c8abb1;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 28px;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

label {
    display: block;
    color: #ead8dc;
    font-size: 13px;
    font-weight: bold;
    margin-bottom: 7px;
}

input {
    width: 100%;
    padding: 14px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,.12);
    outline: none;
    background: rgba(255,255,255,.07);
    color: white;
    font-size: 14px;
    transition: .3s;
}

input:focus {
    border-color: #ff718c;
    box-shadow: 0 0 0 3px rgba(255,113,140,.12);
    transform: translateY(-2px);
}

button {
    width: 100%;
    margin-top: 22px;
    padding: 16px;
    border: none;
    border-radius: 13px;
    background: linear-gradient(135deg, #ff5475, #b71943);
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: .3s;
    box-shadow: 0 12px 30px rgba(190,25,67,.3);
}

button:hover {
    transform: translateY(-3px);
    box-shadow: 0 17px 35px rgba(190,25,67,.45);
}

.result {
    margin-top: 22px;
    padding: 18px;
    text-align: center;
    border-radius: 15px;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.12);
    animation: pop .5s ease;
}

.result-title {
    color: #bca4aa;
    font-size: 12px;
    letter-spacing: 1px;
    margin-bottom: 7px;
}

.result-value {
    font-size: 28px;
    font-weight: bold;
    color: #ff91a4;
}

.confidence {
    color: #d8c2c7;
    font-size: 13px;
    margin-top: 7px;
}

.right {
    width: 42%;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    background: radial-gradient(circle, rgba(255,70,100,.15), transparent 65%);
}

.glow {
    position: absolute;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: rgba(255,70,100,.08);
    filter: blur(12px);
    animation: pulse 4s infinite alternate;
}

.card {
    position: relative;
    width: 300px;
    padding: 38px 25px;
    text-align: center;
    border-radius: 25px;
    background: rgba(255,255,255,.07);
    border: 1px solid rgba(255,255,255,.13);
    backdrop-filter: blur(15px);
    box-shadow: 0 20px 50px rgba(0,0,0,.3);
    animation: float 4s ease-in-out infinite;
}

.icon {
    width: 115px;
    height: 115px;
    margin: auto auto 22px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 58px;
    background: linear-gradient(135deg, #551522, #9f2945);
    box-shadow: 0 0 35px rgba(255,75,105,.2);
}

.card h2 {
    font-size: 24px;
    margin-bottom: 10px;
}

.card p {
    color: #c0aeb3;
    font-size: 13px;
    line-height: 1.7;
}

.powered {
    position: absolute;
    bottom: 22px;
    color: #927b81;
    font-size: 11px;
    letter-spacing: 1px;
}

@keyframes show {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-12px); }
}

@keyframes pulse {
    from { transform: scale(1); opacity: .4; }
    to { transform: scale(1.25); opacity: 1; }
}

@keyframes pop {
    from { opacity: 0; transform: scale(.95); }
    to { opacity: 1; transform: scale(1); }
}

@media(max-width:800px) {
    .container { flex-direction: column; }
    .left, .right { width: 100%; }
    .right { min-height: 400px; }
    .left { padding: 30px 22px; }
    h1 { font-size: 34px; }
}

@media(max-width:500px) {
    .form-grid { grid-template-columns: 1fr; }
}
</style>
</head>

<body>
<div class="container">

<div class="left">
<div class="badge">🍷 MACHINE LEARNING PROJECT</div>

<h1>Wine <span>Quality</span> Predictor</h1>

<p class="description">
Enter the chemical properties of a wine sample.
The Machine Learning model will classify its
predicted quality category.
</p>

<form method="POST">
<div class="form-grid">

<div>
<label>🍷 Alcohol (%)</label>
<input type="number" name="alcohol" step="0.01" min="8" max="15" placeholder="Example: 11.5" required>
</div>

<div>
<label>⚗️ pH</label>
<input type="number" name="ph" step="0.01" min="2.5" max="4.5" placeholder="Example: 3.3" required>
</div>

<div>
<label>🍋 Citric Acid</label>
<input type="number" name="citric_acid" step="0.01" min="0" max="1" placeholder="Example: 0.4" required>
</div>

<div>
<label>🧪 Sulphates</label>
<input type="number" name="sulphates" step="0.01" min="0" max="2" placeholder="Example: 0.65" required>
</div>

<div>
<label>🧫 Volatile Acidity</label>
<input type="number" name="volatile_acidity" step="0.01" min="0" max="2" placeholder="Example: 0.5" required>
</div>

<div>
<label>🍬 Residual Sugar</label>
<input type="number" name="residual_sugar" step="0.01" min="0" max="20" placeholder="Example: 4.0" required>
</div>

</div>

<button type="submit">🔮 Predict Wine Quality</button>
</form>

{% if result %}
<div class="result">
<div class="result-title">PREDICTION RESULT</div>
<div class="result-value">{{ result }}</div>
<div class="confidence">Model confidence: {{ confidence }}%</div>
</div>
{% endif %}

</div>

<div class="right">
<div class="glow"></div>

<div class="card">
<div class="icon">🍷</div>
<h2>AI Quality Analysis</h2>
<p>
This educational ML application uses
<strong>Logistic Regression</strong>
to classify a wine sample into
Low, Medium, or High Quality.
</p>
</div>

<div class="powered">⚡ POWERED BY MACHINE LEARNING</div>
</div>

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None

    if request.method == "POST":
        alcohol = float(request.form["alcohol"])
        ph = float(request.form["ph"])
        citric_acid = float(request.form["citric_acid"])
        sulphates = float(request.form["sulphates"])
        volatile_acidity = float(request.form["volatile_acidity"])
        residual_sugar = float(request.form["residual_sugar"])

        result, confidence = alcohol_model.predict_quality(
            alcohol,
            ph,
            citric_acid,
            sulphates,
            volatile_acidity,
            residual_sugar
        )

    return render_template_string(
        HTML,
        result=result,
        confidence=confidence
    )

if __name__ == "__main__":
    app.run(debug=True)

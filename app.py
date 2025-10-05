from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
NASA_API_KEY = "DEMO_KEY"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_images")
def get_images():
    query = request.args.get("q", "galaxy")
    url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
    
    response = requests.get(url)
    data = response.json()

    images = []
    for item in data["collection"]["items"][:12]:
        try:
            img_url = item["links"][0]["href"]
            title = item["data"][0]["title"]
            images.append({"title": title, "url": img_url})
        except:
            continue

    return jsonify(images)

@app.route("/viewer")
def viewer():
    img_url = request.args.get("img")
    if not img_url:
        return "No image selected!"
    return render_template("viewer.html", img_url=img_url)

if __name__ == "__main__":
    app.run(debug=True)

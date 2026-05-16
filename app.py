from flask import Flask, render_template, request, redirect, url_for, session
from batch import run_batch
from shopify_update import update_product
import json

app = Flask(__name__)
app.secret_key = 'onboard-dev-key'

enriched_products = []
current_index = 0

@app.route('/')
def index():
    global enriched_products, current_index
    enriched_products = run_batch(limit=5)
    current_index = 0
    return redirect(url_for('review'))

@app.route('/review')
def review():
    global current_index
    if current_index >= len(enriched_products):
        return redirect(url_for('complete'))
    ep = enriched_products[current_index]
    return render_template('review.html', ep=ep, index=current_index, total=len(enriched_products))

@app.route('/approve', methods=['POST'])
def approve():
    global current_index
    ep = enriched_products[current_index]
    update_product(ep)
    current_index += 1
    return redirect(url_for('review'))

@app.route('/reject', methods=['POST'])
def reject():
    global current_index
    current_index += 1
    return redirect(url_for('review'))

@app.route('/complete')
def complete():
    return "<h1>Batch complete.</h1>"

if __name__ == "__main__":
    app.run(debug=True)
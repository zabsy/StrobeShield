from flask import Flask, jsonify, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SeizureEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# Route to serve the HTML page
@app.route('/')
def index():
    events = SeizureEvent.query.all()
    return render_template('index.html', events=events)

@app.route('/seizure_events', methods=['POST'])
def add_seizure_event():
    new_event_data = request.get_json()
    new_event = SeizureEvent(timestamp=new_event_data['timestamp'], description=new_event_data['description'])
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Seizure event added successfully"}), 201


if __name__ == '__main__':
    app.run(debug=True)

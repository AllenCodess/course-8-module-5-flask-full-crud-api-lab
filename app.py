from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# ------------------------------
# POST /events - Create a new event
# ------------------------------
@app.route("/events", methods=["POST"])
def create_event():
    # Task 1: Get JSON input
    data = request.get_json()

    if not data or "title" not in data:
        return ("Missing 'title' field", 400)

    # Task 2: Generate new ID
    new_id = max((e.id for e in events), default=0) + 1

    # Task 3: Create new Event object
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    # Task 4: Return result
    return jsonify(new_event.to_dict()), 201


# ------------------------------
# PATCH /events/<event_id> - Update an existing event
# ------------------------------
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Task 1: Find event
    event = next((e for e in events if e.id == event_id), None)

    if not event:
        return ("Event not found", 404)

    # Task 2: Parse JSON input
    data = request.get_json()
    if not data:
        return ("No data provided", 400)

    # Task 3: Update fields
    if "title" in data:
        event.title = data["title"]

    # Task 4: Return updated event
    return jsonify(event.to_dict())


# ------------------------------
# DELETE /events/<event_id> - Delete event
# ------------------------------
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Task 1: Find event
    event = next((e for e in events if e.id == event_id), None)

    if not event:
        return ("Event not found", 404)

    # Task 2: Remove from list
    events.remove(event)

    # Task 3/4: Return success
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)

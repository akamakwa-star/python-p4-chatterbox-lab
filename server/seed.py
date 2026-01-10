from app import app, db
from models import Message

with app.app_context():  # ✅ Use app, not db
    # Delete all existing messages (optional)
    Message.query.delete()

    # Seed messages
    msg1 = Message(body="Hello, world!", username="Alice")
    msg2 = Message(body="Hi there!", username="Bob")
    db.session.add_all([msg1, msg2])
    db.session.commit()
    print("Database seeded with initial messages!")

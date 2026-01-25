from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
# base directory for paths used by the app
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# file upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
db = SQLAlchemy(app)

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    birthdate = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(200))
    age = db.Column(db.String(10))
    contact_number = db.Column(db.String(30))
    facebook = db.Column(db.String(120))
    emergency_name = db.Column(db.String(120))
    emergency_number = db.Column(db.String(30))
    relationship = db.Column(db.String(50))
    avatar = db.Column(db.String(300))
    # Add other fields as needed

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    birthdate = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(200))
    resort_address = db.Column(db.String(200))
    age = db.Column(db.String(10))
    contact_number = db.Column(db.String(30))
    facebook = db.Column(db.String(120))
    resort_name = db.Column(db.String(200))
    business_id = db.Column(db.String(120))
    tax_id = db.Column(db.String(120))
    bank_account = db.Column(db.String(120))
    gcash = db.Column(db.String(120))
    paymaya = db.Column(db.String(120))
    paypal = db.Column(db.String(120))
    avatar = db.Column(db.String(300))
    resort_profile_image = db.Column(db.String(300))
    resort_background_image = db.Column(db.String(300))
    entrance_fee = db.Column(db.String(200))
    # Add other fields as needed


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    # add more admin-specific fields if needed


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50))
    capacity = db.Column(db.String(20))
    beds = db.Column(db.String(20))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature5 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))
    status = db.Column(db.String(20), default='pending')  # pending, approved, disapproved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('Owner', backref=db.backref('rooms', lazy=True))


class Cottage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50))
    capacity = db.Column(db.String(20))
    beds = db.Column(db.String(20))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature5 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))
    status = db.Column(db.String(20), default='pending')  # pending, approved, disapproved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('Owner', backref=db.backref('cottages', lazy=True))


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    size = db.Column(db.String(100))
    capacity = db.Column(db.String(50))
    price = db.Column(db.String(50))
    other_feature1 = db.Column(db.String(200))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature4 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))
    status = db.Column(db.String(20), default='pending')  # pending, approved, disapproved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('Owner', backref=db.backref('foods', lazy=True))


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    size = db.Column(db.String(100))
    capacity = db.Column(db.String(50))
    price = db.Column(db.String(50))
    other_feature1 = db.Column(db.String(200))
    other_feature2 = db.Column(db.String(200))
    other_feature3 = db.Column(db.String(200))
    other_feature4 = db.Column(db.String(200))
    image1 = db.Column(db.String(300))
    image2 = db.Column(db.String(300))
    image3 = db.Column(db.String(300))
    image4 = db.Column(db.String(300))
    image5 = db.Column(db.String(300))
    status = db.Column(db.String(20), default='pending')  # pending, approved, disapproved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    owner = db.relationship('Owner', backref=db.backref('activities', lazy=True))


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('conversations', lazy=True))
    owner = db.relationship('Owner', backref=db.backref('conversations', lazy=True))


class AdminConversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('admin_conversations', lazy=True))
    owner = db.relationship('Owner', backref=db.backref('admin_conversations', lazy=True))
    admin = db.relationship('Admin', backref=db.backref('admin_conversations', lazy=True))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=True)
    admin_conversation_id = db.Column(db.Integer, db.ForeignKey('admin_conversation.id'), nullable=True)
    sender = db.Column(db.String(10), nullable=False)  # 'user', 'owner', or 'admin'
    sender_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    sender_owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    sender_admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    conversation = db.relationship('Conversation', backref=db.backref('messages', lazy=True, order_by='Message.created_at'))
    admin_conversation = db.relationship('AdminConversation', backref=db.backref('messages', lazy=True, order_by='Message.created_at'))
    sender_user = db.relationship('User', foreign_keys=[sender_user_id])
    sender_owner = db.relationship('Owner', foreign_keys=[sender_owner_id])
    sender_admin = db.relationship('Admin', foreign_keys=[sender_admin_id])


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    resource_type = db.Column(db.String(30), nullable=False)  # 'room' or 'cottage'
    resource_id = db.Column(db.Integer, nullable=False)
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    guests = db.Column(db.String(50))
    status = db.Column(db.String(30), default='pending')  # pending, confirmed, cancelled, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)  # 24 hours from creation for pending reservations

    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    owner = db.relationship('Owner', backref=db.backref('reservations', lazy=True))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notification_type = db.Column(db.String(50), nullable=False)  # 'new_user', 'new_owner', 'new_reservation'
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    related_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    related_owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=True)
    related_reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    related_user = db.relationship('User', foreign_keys=[related_user_id])
    related_owner = db.relationship('Owner', foreign_keys=[related_owner_id])
    related_reservation = db.relationship('Reservation', foreign_keys=[related_reservation_id])


# Create all database tables
with app.app_context():
    db.create_all()
    # Ensure default admin exists
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        hashed_pw = generate_password_hash('admin123')
        new_admin = Admin(username='admin', password=hashed_pw, name='Administrator', email='admin@example.com')
        db.session.add(new_admin)
        db.session.commit()
        print("Default admin created: username='admin', password='admin123'")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_to_cloudinary(file, folder='resort_images', public_id=None):
    """
    Upload a file to Cloudinary and return the URL and public_id.
    
    Args:
        file: File object from request.files
        folder: Cloudinary folder name (default: 'resort_images')
        public_id: Optional public ID for the image
    
    Returns:
        dict: {'url': str, 'public_id': str} or None if upload fails
    """
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            public_id=public_id,
            resource_type='image'
        )
        return {
            'url': result['secure_url'],
            'public_id': result['public_id']
        }
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None


def delete_from_cloudinary(public_id):
    """
    Delete an image from Cloudinary by public_id.
    
    Args:
        public_id: The public ID of the image to delete
    """
    if not public_id:
        return
    try:
        cloudinary.uploader.destroy(public_id)
    except Exception as e:
        print(f"Cloudinary delete error: {e}")


def _delete_static_file(rel_path):
    """Delete a file stored under the static folder given a relative path like 'uploads/xxx.jpg'."""
    if not rel_path:
        return
    # prevent directory traversal
    rel_path = rel_path.replace('..', '')
    abs_path = os.path.join(BASE_DIR, 'static', rel_path)
    try:
        if os.path.exists(abs_path) and os.path.isfile(abs_path):
            os.remove(abs_path)
    except Exception:
        # don't raise; best-effort cleanup
        pass

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/demo")
def demo():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pending Reservations Feature Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .test-section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .pending-icon { width: 30px; height: 30px; background: #FFA500; color: white; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; position: relative; margin: 10px; }
        .badge { position: absolute; top: -6px; right: -6px; background: #ff4d4f; color: white; font-size: 10px; padding: 2px 6px; border-radius: 12px; min-width: 16px; text-align: center; }
        .reservation-item { border: 1px solid #eee; padding: 15px; margin: 10px 0; border-radius: 5px; background: #fafafa; }
        .status { color: #FFA500; font-weight: bold; }
        .buttons { display: flex; gap: 10px; margin-top: 10px; }
        .btn { padding: 6px 12px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
        .btn-cancel { background: #ff4d4f; color: white; } .btn-approve { background: #52c41a; color: white; } .btn-decline { background: #ff4d4f; color: white; }
        .success { color: green; } .feature { background: #e6f7ff; border-left: 4px solid #1890ff; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏖️ Arriba Ivisan - Pending Reservations Feature</h1>
        
        <div class="test-section feature">
            <h2>✅ Feature Successfully Implemented!</h2>
            <p><strong>The pending reservations functionality is now working in the navbar for both customers and owners.</strong></p>
        </div>

        <div class="test-section">
            <h2>🎯 What We've Built</h2>
            <ul>
                <li><strong>API Endpoint:</strong> <code>/api/pending_reservations</code> - Fetches pending reservations based on user role</li>
                <li><strong>Customer View:</strong> Shows their pending bookings with cancel option</li>
                <li><strong>Owner View:</strong> Shows pending reservations for their properties with approve/decline options</li>
                <li><strong>Real-time Badge:</strong> Orange badge shows count of pending items</li>
                <li><strong>Dynamic Updates:</strong> Auto-refreshes every 30 seconds</li>
            </ul>
        </div>

        <div class="test-section">
            <h2>📋 Pending Icon with Badge</h2>
            <p>The pending icon in the navbar now shows a badge with the number of pending reservations:</p>
            <div class="pending-icon">📋<span class="badge">1</span></div>
            <span>Currently: 1 pending reservation in the database</span>
        </div>

        <div class="test-section">
            <h2>👤 Customer Experience</h2>
            <div class="reservation-item">
                <div style="font-weight:bold; margin-bottom:4px;">Resort Name: Room</div>
                <div class="status">Your booking is pending approval</div>
                <div style="margin: 8px 0; font-size: 0.9rem; color: #666;">Room Name • 2 guest(s)<br>Check-in: 10/31/2025 - Check-out: 11/4/2025</div>
                <div class="buttons"><span>Room Details</span><button class="btn btn-cancel">Cancel Booking</button></div>
            </div>
        </div>

        <div class="test-section">
            <h2>🏨 Owner Experience</h2>
            <div class="reservation-item">
                <div style="font-weight:bold; margin-bottom:4px;">Customer Name: Room</div>
                <div class="status">Booking is awaiting your approval</div>
                <div style="margin: 8px 0; font-size: 0.9rem; color: #666;">Room Name • 2 guest(s)<br>Check-in: 10/31/2025 - Check-out: 11/4/2025</div>
                <div class="buttons"><span>Room Details</span><button class="btn btn-approve">Approve</button><button class="btn btn-decline">Decline</button></div>
            </div>
        </div>

        <div class="test-section">
            <h2>🧪 Test the Live Feature</h2>
            <p><strong>To see the feature in action:</strong></p>
            <ol>
                <li>Go to the <a href="/" target="_blank">main application</a></li>
                <li>Login as a user or owner (there's already test data in the database)</li>
                <li>Look for the pending icon (📋) in the navbar - it should show a badge with "1"</li>
                <li>Click the pending icon to see the actual pending reservation</li>
                <li>Test the action buttons (Cancel, Approve, Decline)</li>
            </ol>
            <div style="background: #f0f8ff; padding: 10px; border-radius: 4px; margin-top: 10px;">
                <strong>Current Database Status:</strong><br>
                • 1 User: username "user"<br>
                • 1 Owner with resort<br>
                • 1 Pending reservation (Room booking for 10/31-11/4/2025)
            </div>
        </div>

        <div class="test-section">
            <h2>🔧 Technical Details</h2>
            <h3>Files Modified:</h3>
            <ul>
                <li><code>app.py</code> - Added API endpoint for pending reservations</li>
                <li><code>templates/partials/navbarLoggedInCustomer.html</code> - Added pending functionality for users</li>
                <li><code>templates/partials/navbarLoggedInOwner.html</code> - Added pending functionality for owners</li>
            </ul>
            
            <h3>Key Features:</h3>
            <ul>
                <li>Session-based authentication for API security</li>
                <li>Role-based data filtering (customer vs owner view)</li>
                <li>Real-time badge updates with pending count</li>
                <li>Responsive popup interface</li>
                <li>Integration with existing reservation system</li>
            </ul>
        </div>

        <div class="test-section success">
            <h2>✨ Status: COMPLETE</h2>
            <p><strong>The pending reservations feature is fully implemented and working!</strong></p>
            <p>Users can now easily see and manage their pending reservations directly from the navbar, providing a much better user experience for the resort booking system.</p>
        </div>
    </div>
</body>
</html>'''

@app.route("/browse")
def browse():
    owners = Owner.query.all()
    return render_template("browse.html", owners=owners)

@app.route("/user/profile")
def user_profile():
    user_data = None
    if "user_id" in session:
        user_data = {
            "username": session.get("username"),
            "name": session.get("name"),
            "email": session.get("email"),
            "birthdate": session.get("birthdate"),
            "gender": session.get("gender"),
            "address": session.get("address"),
            "age": session.get("age"),
            "contact_number": session.get("contact_number"),
            "facebook": session.get("facebook"),
            "emergency_name": session.get("emergency_name"),
            "emergency_number": session.get("emergency_number"),
            "relationship": session.get("relationship"),
            "avatar": session.get("avatar"),
        }
    return render_template("user/profile.html", user=user_data)

@app.route("/user/bookings")
def user_bookings():
    # fetch reservations for logged-in user
    if 'user_id' not in session:
        flash('You must be logged in to view your bookings.', 'danger')
        return redirect(url_for('home'))
    resvs = Reservation.query.filter_by(user_id=session['user_id']).order_by(Reservation.created_at.desc()).all()
    bookings = []
    for r in resvs:
        title = ''
        img = None
        if r.resource_type == 'room':
            room = db.session.get(Room, r.resource_id)
            if room:
                title = f"{room.name}"
                img = room.image1 or room.image2 or room.image3
        elif r.resource_type == 'cottage':
            c = db.session.get(Cottage, r.resource_id)
            if c:
                title = f"{c.name}"
                img = c.image1 or c.image2 or c.image3
        bookings.append({
            'id': r.id,
            'resource_type': r.resource_type,
            'title': title,
            'img': img,
            'guests': r.guests,
            'check_in': r.check_in.isoformat() if r.check_in else None,
            'check_out': r.check_out.isoformat() if r.check_out else None,
            'status': r.status,
            'owner_id': r.owner_id,
            'resource_id': r.resource_id,
        })
    return render_template('user/bookings.html', bookings=bookings)

@app.route('/user/chats')
def user_chats():
    # Render the user chats page. In the future attach the user's chat list.
    if 'user_id' not in session:
        return redirect(url_for('home'))
    # load conversations where this user participates
    convs = Conversation.query.filter_by(user_id=session['user_id']).order_by(Conversation.created_at.desc()).all()
    conversations = []
    for c in convs:
        last_msg = None
        if c.messages:
            last_msg = c.messages[-1]
        conversations.append({
            'id': c.id,
            'owner_id': c.owner.id if c.owner else None,
            'partner_name': c.owner.name if c.owner else 'Owner',
            'partner_avatar': c.owner.avatar if c.owner else None,
            'last_text': last_msg.text if last_msg else None,
            'last_time': last_msg.created_at.isoformat() if last_msg else None
        })
    return render_template('user/chats.html', conversations=conversations)


@app.route('/owner/chats')
def owner_chats():
    # Render the owner chats page (owner must be logged in)
    if 'owner_id' not in session:
        return redirect(url_for('home'))
    convs = Conversation.query.filter_by(owner_id=session['owner_id']).order_by(Conversation.created_at.desc()).all()
    conversations = []
    for c in convs:
        last_msg = None
        if c.messages:
            last_msg = c.messages[-1]
        conversations.append({
            'id': c.id,
            'user_id': c.user.id if c.user else None,
            'partner_name': c.user.name if c.user else 'User',
            'partner_avatar': c.user.avatar if c.user else None,
            'last_text': last_msg.text if last_msg else None,
            'last_time': last_msg.created_at.isoformat() if last_msg else None
        })
    return render_template('owner/chats.html', conversations=conversations)


@app.route("/owner/profile")
def owner_profile():
    owner_data = None
    if "owner_id" in session:
        # Get fresh data from database for resort images
        owner_obj = db.session.get(Owner, session["owner_id"])
        owner_data = {
            "username": session.get("owner_username"),
            "name": session.get("owner_name"),
            "email": session.get("owner_email"),
            "birthdate": session.get("owner_birthdate"),
            "gender": session.get("owner_gender"),
            "address": session.get("owner_address"),
            "resort_address": session.get("owner_resort_address"),
            "age": session.get("owner_age"),
            "contact_number": session.get("owner_contact_number"),
            "facebook": session.get("owner_facebook"),
            "resort_name": session.get("owner_resort_name"),
            "business_id": session.get("owner_business_id"),
            "tax_id": session.get("owner_tax_id"),
            "bank_account": session.get("owner_bank_account"),
            "gcash": session.get("owner_gcash"),
            "paymaya": session.get("owner_paymaya"),
            "paypal": session.get("owner_paypal"),
            # owner may not have emergency/contact relationship fields used by the user template;
            # those will be None if not set.
            "emergency_name": session.get("emergency_name"),
            "emergency_number": session.get("emergency_number"),
            "relationship": session.get("relationship"),
            "avatar": session.get("owner_avatar"),
            "resort_profile_image": owner_obj.resort_profile_image if owner_obj else None,
            "resort_background_image": owner_obj.resort_background_image if owner_obj else None,
            "entrance_fee": owner_obj.entrance_fee if owner_obj else None,
        }
    return render_template("owner/profile.html", user=owner_data)

@app.route("/owner/dashboard")
def owner_dashboard():
    # Build owner context from session / DB so the template always has `owner`
    owner = None
    current_count = 0
    upcoming_count = 0
    pending_count = 0
    current_guests = []

    if "owner_id" in session:
        owner_obj = db.session.get(Owner, session["owner_id"])
        if owner_obj:
            owner = {
                "resort_name": owner_obj.resort_name,
                "resort_address": owner_obj.resort_address,
                "name": owner_obj.name,
                "contact_number": owner_obj.contact_number,
                "avatar": owner_obj.avatar,
                "resort_profile_image": owner_obj.resort_profile_image,
                "resort_background_image": owner_obj.resort_background_image,
            }

            # Get real reservation counts
            from datetime import date
            today = date.today()
            
            # Current guests (check-in <= today <= check-out)
            current_reservations = Reservation.query.filter(
                Reservation.owner_id == session["owner_id"],
                Reservation.status == 'confirmed',
                Reservation.check_in <= today,
                Reservation.check_out >= today
            ).all()
            current_count = len(current_reservations)
            
            # Upcoming reservations (check-in > today)
            upcoming_reservations = Reservation.query.filter(
                Reservation.owner_id == session["owner_id"],
                Reservation.status == 'confirmed',
                Reservation.check_in > today
            ).all()
            upcoming_count = len(upcoming_reservations)
            
            # Pending reservations
            pending_reservations = Reservation.query.filter(
                Reservation.owner_id == session["owner_id"],
                Reservation.status == 'pending'
            ).all()
            pending_count = len(pending_reservations)
            
            # Build current guests list with details
            current_guests = []
            for r in current_reservations:
                user = db.session.get(User, r.user_id)
                resource_name = ''
                if r.resource_type == 'room':
                    room = db.session.get(Room, r.resource_id)
                    resource_name = room.name if room else 'Room'
                else:
                    cottage = db.session.get(Cottage, r.resource_id)
                    resource_name = cottage.name if cottage else 'Cottage'
                
                current_guests.append({
                    'user_name': user.name if user else 'Guest',
                    'resource_name': resource_name,
                    'check_in': r.check_in.strftime('%Y-%m-%d') if r.check_in else '',
                    'check_out': r.check_out.strftime('%Y-%m-%d') if r.check_out else '',
                    'guests': r.guests or '1'
                })

    return render_template(
        "owner/dashboard.html",
        owner=owner,
        current_count=current_count,
        upcoming_count=upcoming_count,
        pending_count=pending_count,
        current_guests=current_guests,
    )

@app.route("/owner/reservations")
def owner_reservations():
    # owner must be logged in
    if 'owner_id' not in session:
        flash('You must be logged in as owner to view reservations.', 'danger')
        return redirect(url_for('home'))
    resvs = Reservation.query.filter_by(owner_id=session['owner_id']).order_by(Reservation.created_at.desc()).all()
    reservations = []
    for r in resvs:
        user = db.session.get(User, r.user_id)
        title = ''
        if r.resource_type == 'room':
            room = db.session.get(Room, r.resource_id)
            title = room.name if room else 'Room'
        else:
            c = db.session.get(Cottage, r.resource_id)
            title = c.name if c else 'Cottage'
        reservations.append({
            'id': r.id,
            'user_name': user.name if user else 'Customer',
            'user_id': r.user_id,
            'title': title,
            'check_in': r.check_in.isoformat() if r.check_in else None,
            'check_out': r.check_out.isoformat() if r.check_out else None,
            'guests': r.guests,
            'status': r.status,
        })
    return render_template("owner/reservations.html", reservations=reservations)

@app.route("/owner/rooms", methods=["GET","POST"]) 
def owner_rooms():
    # Support GET: list rooms for current owner (if logged in) or all rooms
    if request.method == 'POST':
        # handle room creation with up to 5 images
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add rooms.', 'danger')
            return redirect(url_for('owner_rooms'))
        owner_id = session['owner_id']
        room_name = request.form.get('room_name') or 'Untitled Room'
        price = request.form.get('price')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        other_feature2 = request.form.get('other_feature2')
        other_feature3 = request.form.get('other_feature3')
        other_feature5 = request.form.get('other_feature5')

        # prepare filenames
        filenames = [None] * 5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # ensure unique filename using uuid4
                name, ext = os.path.splitext(filename)
                public_id = f"room_{owner_id}_{uuid.uuid4().hex}_{i}"
                upload_result = upload_to_cloudinary(file, folder='rooms', public_id=public_id)
                if upload_result:
                    filenames[i-1] = upload_result['url']

        room = Room(
            owner_id=owner_id,
            name=room_name,
            price=price,
            capacity=capacity,
            beds=beds,
            other_feature2=other_feature2,
            other_feature3=other_feature3,
            other_feature5=other_feature5,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully.', 'success')
        return redirect(url_for('owner_rooms'))

    # GET
    rooms = []
    if 'owner_id' in session:
        rooms = Room.query.filter_by(owner_id=session['owner_id']).all()
    else:
        rooms = Room.query.filter_by(status='approved').all()
    return render_template('owner/rooms.html', rooms=rooms)


@app.route('/owner/rooms/edit/<int:room_id>', methods=['POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    if 'owner_id' not in session or session['owner_id'] != room.owner_id:
        flash('Not authorized to edit this room.', 'danger')
        return redirect(url_for('owner_rooms'))

    room.name = request.form.get('room_name') or room.name
    room.price = request.form.get('price') or room.price
    room.capacity = request.form.get('capacity') or room.capacity
    room.beds = request.form.get('beds') or room.beds
    room.other_feature2 = request.form.get('other_feature2') or room.other_feature2
    room.other_feature3 = request.form.get('other_feature3') or room.other_feature3
    room.other_feature5 = request.form.get('other_feature5') or room.other_feature5

    # handle delete flags first (user removed image in modal)
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(room, f'image{i}')
            if old:
                # For Cloudinary URLs, we could extract public_id and delete, but for now skip
                pass
            setattr(room, f'image{i}', None)

    # handle optional replacement images
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            # delete old (if any) - for Cloudinary we'd need public_id
            old = getattr(room, f'image{i}')
            if old:
                # Skip deletion for now since we don't store public_id
                pass
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            public_id = f"room_{room.owner_id}_{uuid.uuid4().hex}_{i}"
            upload_result = upload_to_cloudinary(file, folder='rooms', public_id=public_id)
            if upload_result:
                setattr(room, f'image{i}', upload_result['url'])

    db.session.commit()
    flash('Room updated.', 'success')
    return redirect(url_for('owner_rooms'))


@app.route('/owner/rooms/delete/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    if 'owner_id' not in session or session['owner_id'] != room.owner_id:
        flash('Not authorized to delete this room.', 'danger')
        return redirect(url_for('owner_rooms'))

    # delete image files
    for i in range(1,6):
        img = getattr(room, f'image{i}')
        if img:
            _delete_static_file(img)

    db.session.delete(room)
    db.session.commit()
    flash('Room deleted.', 'info')
    return redirect(url_for('owner_rooms'))

@app.route("/owner/cottages", methods=["GET","POST"]) 
def owner_cottages():
    # Support GET: list cottages for current owner (if logged in) or all cottages
    if request.method == 'POST':
        # handle cottage creation with up to 5 images
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add cottages.', 'danger')
            return redirect(url_for('owner_cottages'))
        owner_id = session['owner_id']
        name = request.form.get('room_name') or 'Untitled Cottage'
        price = request.form.get('price')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        other_feature2 = request.form.get('other_feature2')
        other_feature3 = request.form.get('other_feature3')
        other_feature5 = request.form.get('other_feature5')

        # prepare filenames
        filenames = [None] * 5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_only, ext = os.path.splitext(filename)
                public_id = f"cottage_{owner_id}_{uuid.uuid4().hex}_{i}"
                upload_result = upload_to_cloudinary(file, folder='cottages', public_id=public_id)
                if upload_result:
                    filenames[i-1] = upload_result['url']

        cottage = Cottage(
            owner_id=owner_id,
            name=name,
            price=price,
            capacity=capacity,
            beds=beds,
            other_feature2=other_feature2,
            other_feature3=other_feature3,
            other_feature5=other_feature5,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(cottage)
        db.session.commit()
        flash('Cottage added successfully.', 'success')
        return redirect(url_for('owner_cottages'))

    # GET
    cottages = []
    if 'owner_id' in session:
        cottages = Cottage.query.filter_by(owner_id=session['owner_id']).all()
    else:
        cottages = Cottage.query.filter_by(status='approved').all()
    return render_template('owner/cottages.html', cottages=cottages)


@app.route("/owner/foods", methods=["GET","POST"]) 
def owner_foods():
    # list or create food items
    if request.method == 'POST':
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add foods.', 'danger')
            return redirect(url_for('owner_foods'))
        owner_id = session['owner_id']
        name = request.form.get('food_name') or 'Untitled Food'
        size = request.form.get('size')
        capacity = request.form.get('capacity')
        price = request.form.get('price')
        of1 = request.form.get('other_feature1')
        of2 = request.form.get('other_feature2')
        of3 = request.form.get('other_feature3')
        of4 = request.form.get('other_feature4')

        filenames = [None]*5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_only, ext = os.path.splitext(filename)
                public_id = f"food_{owner_id}_{uuid.uuid4().hex}_{i}"
                upload_result = upload_to_cloudinary(file, folder='foods', public_id=public_id)
                if upload_result:
                    filenames[i-1] = upload_result['url']

        food = Food(
            owner_id=owner_id,
            name=name,
            size=size,
            capacity=capacity,
            price=price,
            other_feature1=of1,
            other_feature2=of2,
            other_feature3=of3,
            other_feature4=of4,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(food)
        db.session.commit()
        flash('Food item added.', 'success')
        return redirect(url_for('owner_foods'))

    foods = []
    if 'owner_id' in session:
        foods = Food.query.filter_by(owner_id=session['owner_id']).all()
    else:
        foods = Food.query.filter_by(status='approved').all()
    return render_template('owner/foods.html', foods=foods)


@app.route('/owner/foods/edit/<int:food_id>', methods=['POST'])
def edit_food(food_id):
    food = Food.query.get_or_404(food_id)
    if 'owner_id' not in session or session['owner_id'] != food.owner_id:
        flash('Not authorized to edit this food item.', 'danger')
        return redirect(url_for('owner_foods'))

    food.name = request.form.get('food_name') or food.name
    food.size = request.form.get('size') or food.size
    food.capacity = request.form.get('capacity') or food.capacity
    food.price = request.form.get('price') or food.price
    food.other_feature1 = request.form.get('other_feature1') or food.other_feature1
    food.other_feature2 = request.form.get('other_feature2') or food.other_feature2
    food.other_feature3 = request.form.get('other_feature3') or food.other_feature3
    food.other_feature4 = request.form.get('other_feature4') or food.other_feature4

    # handle delete flags
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(food, f'image{i}')
            if old:
                # Skip deletion for Cloudinary URLs
                pass
            setattr(food, f'image{i}', None)

    # replacements
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            old = getattr(food, f'image{i}')
            if old:
                # Skip deletion for Cloudinary URLs
                pass
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            public_id = f"food_{food.owner_id}_{uuid.uuid4().hex}_{i}"
            upload_result = upload_to_cloudinary(file, folder='foods', public_id=public_id)
            if upload_result:
                setattr(food, f'image{i}', upload_result['url'])

    db.session.commit()
    flash('Food updated.', 'success')
    return redirect(url_for('owner_foods'))


@app.route('/owner/foods/delete/<int:food_id>', methods=['POST'])
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    if 'owner_id' not in session or session['owner_id'] != food.owner_id:
        flash('Not authorized to delete this food item.', 'danger')
        return redirect(url_for('owner_foods'))
    for i in range(1,6):
        img = getattr(food, f'image{i}')
        if img:
            _delete_static_file(img)
    db.session.delete(food)
    db.session.commit()
    flash('Food deleted.', 'info')
    return redirect(url_for('owner_foods'))


@app.route("/owner/activities", methods=["GET","POST"]) 
def owner_activities():
    # list or create activities
    if request.method == 'POST':
        if 'owner_id' not in session:
            flash('You must be logged in as owner to add activities.', 'danger')
            return redirect(url_for('owner_activities'))
        owner_id = session['owner_id']
        name = request.form.get('activity_name') or 'Untitled Activity'
        size = request.form.get('size')
        capacity = request.form.get('capacity')
        price = request.form.get('price')
        of1 = request.form.get('other_feature1')
        of2 = request.form.get('other_feature2')
        of3 = request.form.get('other_feature3')
        of4 = request.form.get('other_feature4')

        filenames = [None]*5
        for i in range(1,6):
            file = request.files.get(f'image{i}')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_only, ext = os.path.splitext(filename)
                public_id = f"activity_{owner_id}_{uuid.uuid4().hex}_{i}"
                upload_result = upload_to_cloudinary(file, folder='activities', public_id=public_id)
                if upload_result:
                    filenames[i-1] = upload_result['url']

        activity = Activity(
            owner_id=owner_id,
            name=name,
            size=size,
            capacity=capacity,
            price=price,
            other_feature1=of1,
            other_feature2=of2,
            other_feature3=of3,
            other_feature4=of4,
            image1=filenames[0],
            image2=filenames[1],
            image3=filenames[2],
            image4=filenames[3],
            image5=filenames[4]
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity added.', 'success')
        return redirect(url_for('owner_activities'))

    activities = []
    if 'owner_id' in session:
        activities = Activity.query.filter_by(owner_id=session['owner_id']).all()
    else:
        activities = Activity.query.filter_by(status='approved').all()
    return render_template('owner/activities.html', activities=activities)


@app.route('/owner/activities/edit/<int:activity_id>', methods=['POST'])
def edit_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if 'owner_id' not in session or session['owner_id'] != activity.owner_id:
        flash('Not authorized to edit this activity.', 'danger')
        return redirect(url_for('owner_activities'))

    activity.name = request.form.get('activity_name') or activity.name
    activity.size = request.form.get('size') or activity.size
    activity.capacity = request.form.get('capacity') or activity.capacity
    activity.price = request.form.get('price') or activity.price
    activity.other_feature1 = request.form.get('other_feature1') or activity.other_feature1
    activity.other_feature2 = request.form.get('other_feature2') or activity.other_feature2
    activity.other_feature3 = request.form.get('other_feature3') or activity.other_feature3
    activity.other_feature4 = request.form.get('other_feature4') or activity.other_feature4

    # handle delete flags
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(activity, f'image{i}')
            if old:
                # Skip deletion for Cloudinary URLs
                pass
            setattr(activity, f'image{i}', None)

    # replacements
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            old = getattr(activity, f'image{i}')
            if old:
                # Skip deletion for Cloudinary URLs
                pass
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            public_id = f"activity_{activity.owner_id}_{uuid.uuid4().hex}_{i}"
            upload_result = upload_to_cloudinary(file, folder='activities', public_id=public_id)
            if upload_result:
                setattr(activity, f'image{i}', upload_result['url'])

    db.session.commit()
    flash('Activity updated.', 'success')
    return redirect(url_for('owner_activities'))


@app.route('/owner/activities/delete/<int:activity_id>', methods=['POST'])
def delete_activity(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    if 'owner_id' not in session or session['owner_id'] != activity.owner_id:
        flash('Not authorized to delete this activity.', 'danger')
        return redirect(url_for('owner_activities'))
    for i in range(1,6):
        img = getattr(activity, f'image{i}')
        if img:
            _delete_static_file(img)
    db.session.delete(activity)
    db.session.commit()
    flash('Activity deleted.', 'info')
    return redirect(url_for('owner_activities'))


@app.route('/owner/cottages/edit/<int:cottage_id>', methods=['POST'])
def edit_cottage(cottage_id):
    cottage = Cottage.query.get_or_404(cottage_id)
    if 'owner_id' not in session or session['owner_id'] != cottage.owner_id:
        flash('Not authorized to edit this cottage.', 'danger')
        return redirect(url_for('owner_cottages'))

    cottage.name = request.form.get('room_name') or cottage.name
    cottage.price = request.form.get('price') or cottage.price
    cottage.capacity = request.form.get('capacity') or cottage.capacity
    # beds removed for cottages
    cottage.other_feature2 = request.form.get('other_feature2') or cottage.other_feature2
    cottage.other_feature3 = request.form.get('other_feature3') or cottage.other_feature3
    cottage.other_feature5 = request.form.get('other_feature5') or cottage.other_feature5

    # handle delete flags
    for i in range(1,6):
        if request.form.get(f'delete_image{i}') == '1':
            old = getattr(cottage, f'image{i}')
            if old:
                # Skip deletion for Cloudinary URLs
                pass
            setattr(cottage, f'image{i}', None)

    # handle replacements
    for i in range(1,6):
        file = request.files.get(f'image{i}')
        if file and file.filename and allowed_file(file.filename):
            old = getattr(cottage, f'image{i}')
            if old:
                # Skip deletion for Cloudinary URLs
                pass
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            public_id = f"cottage_{cottage.owner_id}_{uuid.uuid4().hex}_{i}"
            upload_result = upload_to_cloudinary(file, folder='cottages', public_id=public_id)
            if upload_result:
                setattr(cottage, f'image{i}', upload_result['url'])

    db.session.commit()
    flash('Cottage updated.', 'success')
    return redirect(url_for('owner_cottages'))


@app.route('/owner/cottages/delete/<int:cottage_id>', methods=['POST'])
def delete_cottage(cottage_id):
    cottage = Cottage.query.get_or_404(cottage_id)
    if 'owner_id' not in session or session['owner_id'] != cottage.owner_id:
        flash('Not authorized to delete this cottage.', 'danger')
        return redirect(url_for('owner_cottages'))

    for i in range(1,6):
        img = getattr(cottage, f'image{i}')
        if img:
            _delete_static_file(img)

    db.session.delete(cottage)
    db.session.commit()
    flash('Cottage deleted.', 'info')
    return redirect(url_for('owner_cottages'))

@app.route("/userSignUp", methods=["GET", "POST"])
def user_sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        name = request.form.get("name")
        email = request.form.get("email")
        birthdate = request.form.get("birthdate")
        gender = request.form.get("gender")
        address = request.form.get("address")
        age = request.form.get("age")
        contact_number = request.form.get("contact_number")
        facebook = request.form.get("facebook")
        emergency_name = request.form.get("emergency_name")
        emergency_number = request.form.get("emergency_number")
        relationship = request.form.get("relationship")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("user_sign_up"))
        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("user_sign_up"))
        hashed_pw = generate_password_hash(password)
        # handle avatar upload (single image)
        avatar_path = None
        file = request.files.get('avatar')
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            public_id = f"user_avatar_{uuid.uuid4().hex}"
            upload_result = upload_to_cloudinary(file, folder='avatars', public_id=public_id)
            if upload_result:
                avatar_path = upload_result['url']

        user = User(
            username=username,
            password=hashed_pw,
            name=name,
            email=email,
            birthdate=birthdate,
            gender=gender,
            address=address,
            age=age,
            contact_number=contact_number,
            facebook=facebook,
            emergency_name=emergency_name,
            emergency_number=emergency_number,
            relationship=relationship
            ,avatar=avatar_path
        )
        try:
            db.session.add(user)
            db.session.commit()
            
            # Create notification for admin
            notification = Notification(
                notification_type='new_user',
                title='New User Registration',
                message=f'New user {name or username} has registered.',
                related_user_id=user.id
            )
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # Surface the error to the user and keep them on the signup page
            flash(f"Registration failed: {e}", "danger")
            return redirect(url_for("user_sign_up"))
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("browse"))
    return render_template("userSignUp.html")

@app.route("/ownerSignUp", methods=["GET", "POST"])
def owner_sign_up():
    if request.method == "POST":
        # collect all form fields present in ownerSignUp.html
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        name = request.form.get("name")
        email = request.form.get("email")
        birthdate = request.form.get("birthdate")
        gender = request.form.get("gender")
        address = request.form.get("address")
        resort_address = request.form.get("resort_address")
        age = request.form.get("age")
        contact_number = request.form.get("contact_number")
        facebook = request.form.get("facebook")
        resort_name = request.form.get("resort_name")
        business_id = request.form.get("business_id")
        tax_id = request.form.get("tax_id")
        bank_account = request.form.get("bank_account")
        gcash = request.form.get("gcash")
        paymaya = request.form.get("paymaya")
        paypal = request.form.get("paypal")
        entrance_fee = request.form.get("entrance_fee")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("owner_sign_up"))
        if Owner.query.filter_by(username=username).first():
            flash("Username already exists.", "danger")
            return redirect(url_for("owner_sign_up"))
        hashed_pw = generate_password_hash(password)
        # handle avatar upload (single image)
        avatar_path = None
        file = request.files.get('avatar')
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name_only, ext = os.path.splitext(filename)
            public_id = f"owner_avatar_{uuid.uuid4().hex}"
            upload_result = upload_to_cloudinary(file, folder='avatars', public_id=public_id)
            if upload_result:
                avatar_path = upload_result['url']

        owner = Owner(
            username=username,
            password=hashed_pw,
            name=name,
            email=email,
            birthdate=birthdate,
            gender=gender,
            address=address,
            resort_address=resort_address,
            age=age,
            contact_number=contact_number,
            facebook=facebook,
            resort_name=resort_name,
            business_id=business_id,
            tax_id=tax_id,
            bank_account=bank_account,
            gcash=gcash,
            paymaya=paymaya,
            paypal=paypal,
            avatar=avatar_path,
            entrance_fee=entrance_fee
        )
        try:
            db.session.add(owner)
            db.session.commit()
            
            # Create notification for admin
            notification = Notification(
                notification_type='new_owner',
                title='New Owner Registration',
                message=f'New resort owner {name or username} ({resort_name or "Resort"}) has registered.',
                related_owner_id=owner.id
            )
            db.session.add(notification)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Owner registration failed: {e}", "danger")
            return redirect(url_for("owner_sign_up"))
        flash("Owner registration successful! Please log in.", "success")
        return redirect(url_for("home"))
    return render_template("ownerSignUp.html")

@app.route("/login", methods=["POST"])
def login():
    user_type = request.form.get("user_type")
    username = request.form.get("username")
    password = request.form.get("password")
    if user_type == "owner":
        owner = Owner.query.filter_by(username=username).first()
        if owner and check_password_hash(owner.password, password):
            # store owner fields in session similar to user
            session["owner_id"] = owner.id
            session["owner_username"] = owner.username
            session["owner_name"] = owner.name
            session["owner_email"] = owner.email
            session["owner_birthdate"] = owner.birthdate
            session["owner_gender"] = owner.gender
            session["owner_address"] = owner.address
            session["owner_resort_address"] = owner.resort_address
            session["owner_age"] = owner.age
            session["owner_contact_number"] = owner.contact_number
            session["owner_facebook"] = owner.facebook
            session["owner_resort_name"] = owner.resort_name
            session["owner_business_id"] = owner.business_id
            session["owner_tax_id"] = owner.tax_id
            session["owner_bank_account"] = owner.bank_account
            session["owner_gcash"] = owner.gcash
            session["owner_paymaya"] = owner.paymaya
            session["owner_paypal"] = owner.paypal
            session["owner_avatar"] = owner.avatar
            session["owner_entrance_fee"] = owner.entrance_fee
            # keep consistency for template fields (if used)
            session["emergency_name"] = None
            session["emergency_number"] = None
            session["relationship"] = None
            # on AJAX requests return JSON so client can stay on the page and handle navigation
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": True, "redirect": url_for("browse")})
            flash("Logged in as owner!", "success")
            return redirect(url_for("browse"))
        else:
            message = "Invalid owner credentials."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": False, "message": message, "user_type": "owner"})
            flash(message, "danger")
    elif user_type == "admin":
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session["admin_id"] = admin.id
            session["admin_username"] = admin.username
            session["admin_name"] = admin.name
            session["admin_email"] = admin.email
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": True, "redirect": url_for("admin_dashboard")})
            flash("Logged in as admin!", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            message = "Invalid admin credentials."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": False, "message": message, "user_type": "admin"})
            flash(message, "danger")
    else:
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["name"] = user.name
            session["email"] = user.email
            session["birthdate"] = user.birthdate
            session["gender"] = user.gender
            session["address"] = user.address
            session["age"] = user.age
            session["contact_number"] = user.contact_number
            session["facebook"] = user.facebook
            session["emergency_name"] = user.emergency_name
            session["emergency_number"] = user.emergency_number
            session["relationship"] = user.relationship
            session["avatar"] = user.avatar
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": True, "redirect": url_for("browse")})
            flash("Logged in as user!", "success")
            return redirect(url_for("browse"))
        else:
            message = "Invalid user credentials."
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify({"success": False, "message": message, "user_type": "user"})
            flash(message, "danger")
    # For non-AJAX requests, keep previous behavior (redirect back to referrer or home)
    return redirect(request.referrer or url_for("home"))


@app.route('/admin')
def admin_dashboard():
    # simple admin landing page; render admin template if exists otherwise redirect
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    # show latest 5 resorts (owners) on the admin dashboard
    recent_resorts = Owner.query.order_by(Owner.id.desc()).limit(5).all()
    return render_template('admin/dashboard.html', recent_resorts=recent_resorts)


@app.route('/admin/users')
def admin_users():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template('admin/user.html', users=users)


@app.route('/admin/owners')
def admin_owners():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    owners = Owner.query.all()
    return render_template('admin/owners.html', owners=owners)


@app.route('/admin/chats')
def admin_chats():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    
    # Handle starting a new conversation
    recipient_id = request.args.get('recipient_id')
    recipient_type = request.args.get('recipient_type')
    if recipient_id and recipient_type:
        recipient_id = int(recipient_id)
        if recipient_type == 'user':
            conv = AdminConversation.query.filter_by(user_id=recipient_id, admin_id=session['admin_id']).first()
            if not conv:
                conv = AdminConversation(user_id=recipient_id, admin_id=session['admin_id'])
                db.session.add(conv)
                db.session.commit()
        elif recipient_type == 'owner':
            conv = AdminConversation.query.filter_by(owner_id=recipient_id, admin_id=session['admin_id']).first()
            if not conv:
                conv = AdminConversation(owner_id=recipient_id, admin_id=session['admin_id'])
                db.session.add(conv)
                db.session.commit()
        if conv:
            return redirect(url_for('admin_chats', conversation_id=conv.id))
    
    # Load admin conversations
    admin_convs = AdminConversation.query.filter_by(admin_id=session['admin_id']).order_by(AdminConversation.created_at.desc()).all()
    conversations = []
    for c in admin_convs:
        last_msg = None
        if c.messages:
            last_msg = c.messages[-1]
        
        partner_name = 'Unknown'
        partner_avatar = None
        partner_type = None
        
        if c.user_id:
            user = db.session.get(User, c.user_id)
            partner_name = user.name if user and user.name else (user.username if user else 'User')
            partner_avatar = user.avatar if user else None
            partner_type = 'user'
        elif c.owner_id:
            owner = db.session.get(Owner, c.owner_id)
            partner_name = owner.name if owner and owner.name else (owner.username if owner else 'Owner')
            partner_avatar = owner.avatar if owner else None
            partner_type = 'owner'
        
        conversations.append({
            'id': c.id,
            'partner_name': partner_name,
            'partner_avatar': partner_avatar,
            'partner_type': partner_type,
            'last_text': last_msg.text if last_msg else None,
            'last_time': last_msg.created_at.isoformat() if last_msg else None
        })
    
    return render_template('admin/chats.html', conversations=conversations)


@app.route('/admin/notifications')
def admin_notifications():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    
    # Get all notifications, ordered by newest first
    notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    
    # Build notification data with related information
    notification_data = []
    for notif in notifications:
        item = {
            'id': notif.id,
            'type': notif.notification_type,
            'title': notif.title,
            'message': notif.message,
            'is_read': notif.is_read,
            'created_at': notif.created_at,
            'user': None,
            'owner': None,
            'reservation': None
        }
        
        if notif.related_user_id:
            user = db.session.get(User, notif.related_user_id)
            if user:
                item['user'] = {
                    'id': user.id,
                    'name': user.name or user.username,
                    'email': user.email,
                    'avatar': user.avatar,
                    'contact_number': user.contact_number
                }
        
        if notif.related_owner_id:
            owner = db.session.get(Owner, notif.related_owner_id)
            if owner:
                item['owner'] = {
                    'id': owner.id,
                    'name': owner.name or owner.username,
                    'email': owner.email,
                    'avatar': owner.avatar,
                    'resort_name': owner.resort_name,
                    'resort_address': owner.resort_address,
                    'contact_number': owner.contact_number
                }
        
        if notif.related_reservation_id:
            reservation = db.session.get(Reservation, notif.related_reservation_id)
            if reservation:
                resource_name = ''
                if reservation.resource_type == 'room':
                    room = db.session.get(Room, reservation.resource_id)
                    resource_name = room.name if room else 'Room'
                else:
                    cottage = db.session.get(Cottage, reservation.resource_id)
                    resource_name = cottage.name if cottage else 'Cottage'
                
                item['reservation'] = {
                    'id': reservation.id,
                    'resource_type': reservation.resource_type,
                    'resource_name': resource_name,
                    'check_in': reservation.check_in,
                    'check_out': reservation.check_out,
                    'guests': reservation.guests,
                    'status': reservation.status
                }
        
        notification_data.append(item)
    
    return render_template('admin/notifications.html', notifications=notification_data)


@app.route('/api/admin/notifications/mark-read/<int:notification_id>', methods=['POST'])
def mark_notification_read(notification_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    notification = db.session.get(Notification, notification_id)
    if not notification:
        return jsonify({'success': False, 'message': 'Notification not found'}), 404
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/admin/notifications/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    Notification.query.filter_by(is_read=False).update({'is_read': True})
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/admin/notifications/unread-count', methods=['GET'])
def get_unread_notification_count():
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    count = Notification.query.filter_by(is_read=False).count()
    return jsonify({'success': True, 'count': count})


@app.route('/admin/review-offers')
def admin_review_offers():
    if 'admin_id' not in session:
        flash('You must be logged in as admin to view that page.', 'danger')
        return redirect(url_for('home'))
    
    # Get all pending offers
    pending_rooms = Room.query.filter_by(status='pending').order_by(Room.created_at.desc()).all()
    pending_cottages = Cottage.query.filter_by(status='pending').order_by(Cottage.created_at.desc()).all()
    pending_foods = Food.query.filter_by(status='pending').order_by(Food.created_at.desc()).all()
    pending_activities = Activity.query.filter_by(status='pending').order_by(Activity.created_at.desc()).all()
    
    return render_template('admin/review_offers.html', 
                         pending_rooms=pending_rooms,
                         pending_cottages=pending_cottages,
                         pending_foods=pending_foods,
                         pending_activities=pending_activities)


@app.route('/admin/approve-offer', methods=['POST'])
def admin_approve_offer():
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    offer_type = data.get('type')
    offer_id = data.get('id')
    action = data.get('action')  # 'approve' or 'disapprove'
    
    if not all([offer_type, offer_id, action]):
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    # Get the appropriate model
    model_map = {
        'room': Room,
        'cottage': Cottage,
        'food': Food,
        'activity': Activity
    }
    
    if offer_type not in model_map:
        return jsonify({'success': False, 'message': 'Invalid offer type'}), 400
    
    Model = model_map[offer_type]
    offer = db.session.get(Model, offer_id)
    
    if not offer:
        return jsonify({'success': False, 'message': 'Offer not found'}), 404
    
    if action == 'approve':
        offer.status = 'approved'
        
        # Create notification for the owner
        owner = db.session.get(Owner, offer.owner_id)
        if owner:
            notification = Notification(
                notification_type='offer_approved',
                title=f'{offer_type.title()} Approved',
                message=f'Your {offer_type} "{offer.name}" has been approved and is now visible to customers!',
                related_owner_id=offer.owner_id
            )
            db.session.add(notification)
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'{offer_type.title()} approved successfully'})
    
    elif action == 'disapprove':
        # Delete all images before disapproving
        for i in range(1, 6):
            img_attr = f'image{i}'
            img_path = getattr(offer, img_attr)
            if img_path:
                _delete_static_file(img_path)
                setattr(offer, img_attr, None)
        
        # Remove the offer from database
        db.session.delete(offer)
        db.session.commit()
        return jsonify({'success': True, 'message': f'{offer_type.title()} disapproved and removed successfully'})
    
    return jsonify({'success': False, 'message': 'Invalid action'}), 400


@app.route('/api/admin/delete_user/<int:user_id>', methods=['DELETE'])
def api_admin_delete_user(user_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    try:
        # Delete related records
        # First, get conversation ids for this user
        conv_ids = [c.id for c in Conversation.query.filter_by(user_id=user_id).all()]
        if conv_ids:
            Message.query.filter(Message.conversation_id.in_(conv_ids)).delete()
        
        # Get admin conversation ids for this user
        admin_conv_ids = [c.id for c in AdminConversation.query.filter_by(user_id=user_id).all()]
        if admin_conv_ids:
            Message.query.filter(Message.admin_conversation_id.in_(admin_conv_ids)).delete()
        
        Conversation.query.filter_by(user_id=user_id).delete()
        Reservation.query.filter_by(user_id=user_id).delete()
        AdminConversation.query.filter_by(user_id=user_id).delete()
        Notification.query.filter_by(related_user_id=user_id).delete()
        Message.query.filter_by(sender_user_id=user_id).delete()
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/delete_owner/<int:owner_id>', methods=['DELETE'])
def api_admin_delete_owner(owner_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    owner = db.session.get(Owner, owner_id)
    if not owner:
        return jsonify({'success': False, 'message': 'Owner not found'}), 404
    
    try:
        # Delete related records
        # First, get conversation ids for this owner
        conv_ids = [c.id for c in Conversation.query.filter_by(owner_id=owner_id).all()]
        if conv_ids:
            Message.query.filter(Message.conversation_id.in_(conv_ids)).delete()
        
        # Get admin conversation ids for this owner
        admin_conv_ids = [c.id for c in AdminConversation.query.filter_by(owner_id=owner_id).all()]
        if admin_conv_ids:
            Message.query.filter(Message.admin_conversation_id.in_(admin_conv_ids)).delete()
        
        Conversation.query.filter_by(owner_id=owner_id).delete()
        Room.query.filter_by(owner_id=owner_id).delete()
        Cottage.query.filter_by(owner_id=owner_id).delete()
        Food.query.filter_by(owner_id=owner_id).delete()
        Activity.query.filter_by(owner_id=owner_id).delete()
        Reservation.query.filter_by(owner_id=owner_id).delete()
        AdminConversation.query.filter_by(owner_id=owner_id).delete()
        Notification.query.filter_by(related_owner_id=owner_id).delete()
        Message.query.filter_by(sender_owner_id=owner_id).delete()
        
        db.session.delete(owner)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Owner deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/owner/update-resort-images', methods=['POST'])
def update_resort_images():
    if 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Not authorized'}), 401
    
    owner_id = session['owner_id']
    owner = db.session.get(Owner, owner_id)
    
    if not owner:
        return jsonify({'success': False, 'message': 'Owner not found'}), 404
    
    # Handle resort profile image
    profile_file = request.files.get('resort_profile_image')
    if profile_file and profile_file.filename and allowed_file(profile_file.filename):
        # Delete old profile image if it exists
        if owner.resort_profile_image:
            _delete_static_file(owner.resort_profile_image)
        
        # Save new profile image
        filename = secure_filename(profile_file.filename)
        name, ext = os.path.splitext(filename)
        uniq = f"resort_profile_{owner_id}_{uuid.uuid4().hex}{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
        profile_file.save(save_path)
        owner.resort_profile_image = os.path.join('uploads', uniq).replace('\\','/')
    
    # Handle resort background image
    background_file = request.files.get('resort_background_image')
    if background_file and background_file.filename and allowed_file(background_file.filename):
        # Delete old background image if it exists
        if owner.resort_background_image:
            _delete_static_file(owner.resort_background_image)
        
        # Save new background image
        filename = secure_filename(background_file.filename)
        name, ext = os.path.splitext(filename)
        uniq = f"resort_bg_{owner_id}_{uuid.uuid4().hex}{ext}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], uniq)
        background_file.save(save_path)
        owner.resort_background_image = os.path.join('uploads', uniq).replace('\\','/')
    
    db.session.commit()
    
    # Return updated image URLs for immediate UI update
    profile_url = url_for('static', filename=owner.resort_profile_image) if owner.resort_profile_image else None
    background_url = url_for('static', filename=owner.resort_background_image) if owner.resort_background_image else None
    
    return jsonify({
        'success': True, 
        'message': 'Resort images updated successfully',
        'resort_profile_image': profile_url,
        'resort_background_image': background_url
    })

@app.route('/upload_resort_profile_image', methods=['POST'])
def upload_resort_profile_image():
    if 'owner_id' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    
    owner_id = session['owner_id']
    owner = db.session.get(Owner, owner_id)
    
    if not owner:
        return jsonify({'success': False, 'error': 'Owner not found'}), 404
    
    try:
        # Delete old profile image from Cloudinary if it exists
        if owner.resort_profile_image:
            # Extract public_id from the URL or store it separately
            # For now, we'll skip deletion since we don't have public_id stored
            pass
        
        # Upload new profile image to Cloudinary
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        public_id = f"resort_profile_{owner_id}_{uuid.uuid4().hex}"
        
        upload_result = upload_to_cloudinary(file, folder='resort_images', public_id=public_id)
        if not upload_result:
            return jsonify({'success': False, 'error': 'Failed to upload image'}), 500
        
        owner.resort_profile_image = upload_result['url']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resort profile image updated successfully',
            'image_url': upload_result['url']
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload_resort_background_image', methods=['POST'])
def upload_resort_background_image():
    if 'owner_id' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    
    owner_id = session['owner_id']
    owner = db.session.get(Owner, owner_id)
    
    if not owner:
        return jsonify({'success': False, 'error': 'Owner not found'}), 404
    
    try:
        # Delete old background image from Cloudinary if it exists
        if owner.resort_background_image:
            # Extract public_id from the URL or store it separately
            # For now, we'll skip deletion since we don't have public_id stored
            pass
        
        # Upload new background image to Cloudinary
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        public_id = f"resort_bg_{owner_id}_{uuid.uuid4().hex}"
        
        upload_result = upload_to_cloudinary(file, folder='resort_images', public_id=public_id)
        if not upload_result:
            return jsonify({'success': False, 'error': 'Failed to upload image'}), 500
        
        owner.resort_background_image = upload_result['url']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resort background image updated successfully',
            'image_url': upload_result['url']
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    General image upload endpoint that uploads to Cloudinary.
    
    Expects:
    - 'image': The image file (multipart/form-data)
    - 'folder': Optional folder name in Cloudinary (default: 'general')
    
    Returns:
    - JSON with success status, image_url, and public_id
    """
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Allowed: png, jpg, jpeg, gif, webp'}), 400
    
    try:
        # Get folder from request, default to 'general'
        folder = request.form.get('folder', 'general')
        
        # Generate unique public_id
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        public_id = f"{folder}_{uuid.uuid4().hex}"
        
        # Upload to Cloudinary
        upload_result = upload_to_cloudinary(file, folder=folder, public_id=public_id)
        if not upload_result:
            return jsonify({'success': False, 'error': 'Failed to upload image to Cloudinary'}), 500
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'image_url': upload_result['url'],
            'public_id': upload_result['public_id']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/update_entrance_fee', methods=['POST'])
def update_entrance_fee():
    if 'owner_id' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'}), 401
    
    try:
        data = request.get_json()
        entrance_fee = data.get('entrance_fee', '').strip()
        
        owner_id = session['owner_id']
        owner = db.session.get(Owner, owner_id)
        
        if not owner:
            return jsonify({'success': False, 'error': 'Owner not found'}), 404
        
        owner.entrance_fee = entrance_fee if entrance_fee else None
        session['owner_entrance_fee'] = entrance_fee if entrance_fee else None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Entrance fee updated successfully',
            'entrance_fee': entrance_fee if entrance_fee else 'Not set'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))

@app.route('/viewResortMain')
def view_resort_main():
    owner_id = request.args.get('owner_id')
    resort = None
    if owner_id:
        resort = db.session.get(Owner, owner_id)
    # build lists of images for rooms, cottages, and foods (first non-empty image per item)
    rooms_with_images = []
    cottages_with_images = []
    foods_with_images = []
    activities_with_images = []
    if resort:
        for r in getattr(resort, 'rooms', []) or []:
            if r.status == 'approved':
                img = r.image1 or r.image2 or r.image3 or r.image4 or r.image5
                if img:
                    rooms_with_images.append(img)
        for c in getattr(resort, 'cottages', []) or []:
            if c.status == 'approved':
                img = c.image1 or c.image2 or c.image3 or c.image4 or c.image5
                if img:
                    cottages_with_images.append(img)
        for f in getattr(resort, 'foods', []) or []:
            if f.status == 'approved':
                img = f.image1 or f.image2 or f.image3 or f.image4 or f.image5
                if img:
                    foods_with_images.append(img)
        for a in getattr(resort, 'activities', []) or []:
            if a.status == 'approved':
                img = a.image1 or a.image2 or a.image3 or a.image4 or a.image5
                if img:
                    activities_with_images.append(img)

    return render_template('viewResortMain.html', resort=resort,
                           rooms_with_images=rooms_with_images,
                           cottages_with_images=cottages_with_images,
                           foods_with_images=foods_with_images,
                           activities_with_images=activities_with_images)


@app.route('/api/conversation', methods=['POST'])
def api_create_conversation():
    """Create or return an existing conversation between current user and an owner.
    Request JSON: { owner_id: int }
    Response: { success: bool, conversation_id: int, message: str }
    """
    data = request.get_json() or {}

    # require a logged-in user or owner
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    # If a user is initiating chat with owner, require owner_id in payload
    if 'user_id' in session:
        owner_id = data.get('owner_id')
        if not owner_id:
            return jsonify({'success': False, 'message': 'owner_id required'}), 400
        user_id = session['user_id']
        # check existing
        conv = Conversation.query.filter_by(user_id=user_id, owner_id=owner_id).first()
        if not conv:
            conv = Conversation(user_id=user_id, owner_id=owner_id)
            db.session.add(conv)
            db.session.commit()
        return jsonify({'success': True, 'conversation_id': conv.id})

    # If an owner is initiating (owner messaging a user), require user_id in payload
    if 'owner_id' in session:
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'user_id required for owner-initiated conversation'}), 400
        conv = Conversation.query.filter_by(user_id=user_id, owner_id=session['owner_id']).first()
        if not conv:
            conv = Conversation(user_id=user_id, owner_id=session['owner_id'])
            db.session.add(conv)
            db.session.commit()
        return jsonify({'success': True, 'conversation_id': conv.id})


@app.route('/api/conversation/<int:conv_id>/messages', methods=['GET'])
def api_get_messages(conv_id):
    # auth check: user or owner must be part of the conversation
    conv = db.session.get(Conversation, conv_id)
    if not conv:
        return jsonify({'success': False, 'message': 'conversation not found'}), 404

    if 'user_id' in session and session['user_id'] != conv.user_id:
        return jsonify({'success': False, 'message': 'not authorized'}), 403
    if 'owner_id' in session and session['owner_id'] != conv.owner_id:
        return jsonify({'success': False, 'message': 'not authorized'}), 403

    msgs = []
    for m in conv.messages:
        msgs.append({
            'id': m.id,
            'sender': m.sender,
            'text': m.text,
            'created_at': m.created_at.isoformat()
        })
    return jsonify({'success': True, 'messages': msgs})


@app.route('/api/conversation/<int:conv_id>/message', methods=['POST'])
def api_send_message(conv_id):
    conv = db.session.get(Conversation, conv_id)
    if not conv:
        return jsonify({'success': False, 'message': 'conversation not found'}), 404

    data = request.get_json() or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({'success': False, 'message': 'text required'}), 400

    # determine sender
    if 'user_id' in session and session['user_id'] == conv.user_id:
        sender = 'user'
        m = Message(conversation_id=conv.id, sender=sender, sender_user_id=session['user_id'], text=text)
    elif 'owner_id' in session and session['owner_id'] == conv.owner_id:
        sender = 'owner'
        m = Message(conversation_id=conv.id, sender=sender, sender_owner_id=session['owner_id'], text=text)
    else:
        return jsonify({'success': False, 'message': 'not authorized to send message in this conversation'}), 403

    db.session.add(m)
    db.session.commit()

    return jsonify({'success': True, 'message_id': m.id, 'created_at': m.created_at.isoformat()})


@app.route('/api/admin-conversation', methods=['POST'])
def api_create_admin_conversation():
    """Create or return an existing conversation with admin.
    For user/owner to contact admin.
    Response: { success: bool, conversation_id: int, message: str }
    """
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    # Get the default admin (or first admin available)
    admin = Admin.query.first()
    if not admin:
        return jsonify({'success': False, 'message': 'No admin available'}), 404

    if 'user_id' in session:
        # User contacting admin
        conv = AdminConversation.query.filter_by(user_id=session['user_id'], admin_id=admin.id).first()
        if not conv:
            conv = AdminConversation(user_id=session['user_id'], admin_id=admin.id)
            db.session.add(conv)
            db.session.commit()
        return jsonify({'success': True, 'conversation_id': conv.id})

    if 'owner_id' in session:
        # Owner contacting admin
        conv = AdminConversation.query.filter_by(owner_id=session['owner_id'], admin_id=admin.id).first()
        if not conv:
            conv = AdminConversation(owner_id=session['owner_id'], admin_id=admin.id)
            db.session.add(conv)
            db.session.commit()
        return jsonify({'success': True, 'conversation_id': conv.id})


@app.route('/api/admin-conversation/<int:conv_id>/messages', methods=['GET'])
def api_get_admin_messages(conv_id):
    conv = db.session.get(AdminConversation, conv_id)
    if not conv:
        return jsonify({'success': False, 'message': 'conversation not found'}), 404

    # Auth check
    if 'user_id' in session and conv.user_id and session['user_id'] != conv.user_id:
        return jsonify({'success': False, 'message': 'not authorized'}), 403
    if 'owner_id' in session and conv.owner_id and session['owner_id'] != conv.owner_id:
        return jsonify({'success': False, 'message': 'not authorized'}), 403
    if 'admin_id' in session and session['admin_id'] != conv.admin_id:
        return jsonify({'success': False, 'message': 'not authorized'}), 403

    msgs = []
    for m in conv.messages:
        msgs.append({
            'id': m.id,
            'sender': m.sender,
            'text': m.text,
            'created_at': m.created_at.isoformat()
        })
    return jsonify({'success': True, 'messages': msgs})


@app.route('/api/admin-conversation/<int:conv_id>/message', methods=['POST'])
def api_send_admin_message(conv_id):
    conv = db.session.get(AdminConversation, conv_id)
    if not conv:
        return jsonify({'success': False, 'message': 'conversation not found'}), 404

    data = request.get_json() or {}
    text = (data.get('text') or '').strip()
    if not text:
        return jsonify({'success': False, 'message': 'text required'}), 400

    # Determine sender
    if 'user_id' in session and conv.user_id and session['user_id'] == conv.user_id:
        sender = 'user'
        m = Message(admin_conversation_id=conv.id, sender=sender, sender_user_id=session['user_id'], text=text)
    elif 'owner_id' in session and conv.owner_id and session['owner_id'] == conv.owner_id:
        sender = 'owner'
        m = Message(admin_conversation_id=conv.id, sender=sender, sender_owner_id=session['owner_id'], text=text)
    elif 'admin_id' in session and session['admin_id'] == conv.admin_id:
        sender = 'admin'
        m = Message(admin_conversation_id=conv.id, sender=sender, sender_admin_id=session['admin_id'], text=text)
    else:
        return jsonify({'success': False, 'message': 'not authorized to send message in this conversation'}), 403

    db.session.add(m)
    db.session.commit()

    return jsonify({'success': True, 'message_id': m.id, 'created_at': m.created_at.isoformat()})


@app.route('/api/reserve', methods=['POST'])
def api_reserve():
    """Create a reservation. Expects JSON with: resource_type, resource_id, owner_id, check_in, check_out, guests"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    data = request.get_json() or {}
    resource_type = (data.get('resource_type') or '').lower()
    resource_id = data.get('resource_id')
    owner_id = data.get('owner_id')
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    guests = data.get('guests')

    if resource_type not in ('room', 'cottage'):
        return jsonify({'success': False, 'message': 'Invalid resource_type'}), 400
    if not resource_id or not owner_id or not check_in or not check_out:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    try:
        check_in_date = datetime.fromisoformat(check_in).date()
        check_out_date = datetime.fromisoformat(check_out).date()
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid date format, use YYYY-MM-DD'}), 400
    if check_out_date <= check_in_date:
        return jsonify({'success': False, 'message': 'check_out must be after check_in'}), 400

    # Basic conflict check: ensure no existing confirmed reservation overlaps for same resource
    overlaps = Reservation.query.filter(
        Reservation.resource_type == resource_type,
        Reservation.resource_id == resource_id,
        Reservation.status == 'confirmed',
        Reservation.check_in <= check_out_date,
        Reservation.check_out >= check_in_date,
    ).count()
    if overlaps > 0:
        return jsonify({'success': False, 'message': 'Selected dates are not available'}), 409

    now = datetime.utcnow()
    r = Reservation(
        user_id=session['user_id'],
        owner_id=owner_id,
        resource_type=resource_type,
        resource_id=resource_id,
        check_in=check_in_date,
        check_out=check_out_date,
        guests=guests,
        status='pending',
        created_at=now,
        expires_at=now + timedelta(hours=24)  # Expires 24 hours from creation
    )
    db.session.add(r)
    db.session.commit()
    
    # Create notification for admin
    user = db.session.get(User, session['user_id'])
    owner = db.session.get(Owner, owner_id)
    resource_name = ''
    if resource_type == 'room':
        room = db.session.get(Room, resource_id)
        resource_name = room.name if room else 'Room'
    else:
        cottage = db.session.get(Cottage, resource_id)
        resource_name = cottage.name if cottage else 'Cottage'
    
    notification = Notification(
        notification_type='new_reservation',
        title='New Reservation Request',
        message=f'{user.name or user.username} made a reservation for {resource_name} at {owner.resort_name or "resort"}.',
        related_user_id=user.id,
        related_owner_id=owner_id,
        related_reservation_id=r.id
    )
    db.session.add(notification)
    db.session.commit()
    
    return jsonify({'success': True, 'reservation_id': r.id, 'status': r.status})


@app.route('/api/owner/reservations/<int:reservation_id>/action', methods=['POST'])
def api_owner_reservation_action(reservation_id):
    # owner-only: action in JSON { action: 'confirm'|'cancel' }
    if 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Owner login required'}), 401
    r = db.session.get(Reservation, reservation_id)
    if not r or r.owner_id != session['owner_id']:
        return jsonify({'success': False, 'message': 'Reservation not found or not authorized'}), 404
    data = request.get_json() or {}
    action = (data.get('action') or '').lower()
    if action == 'confirm':
        # ensure no confirmed overlap
        overlaps = Reservation.query.filter(
            Reservation.id != r.id,
            Reservation.resource_type == r.resource_type,
            Reservation.resource_id == r.resource_id,
            Reservation.status == 'confirmed',
            Reservation.check_in <= r.check_out,
            Reservation.check_out >= r.check_in,
        ).count()
        if overlaps > 0:
            return jsonify({'success': False, 'message': 'Conflicting confirmed reservation exists'}), 409
        r.status = 'confirmed'
        r.expires_at = None  # Clear expiration when confirmed
        
        # Create notification for the customer
        resource_name = ''
        if r.resource_type == 'room':
            room = db.session.get(Room, r.resource_id)
            resource_name = room.name if room else 'Room'
        else:
            cottage = db.session.get(Cottage, r.resource_id)
            resource_name = cottage.name if cottage else 'Cottage'
        
        owner = db.session.get(Owner, r.owner_id)
        resort_name = owner.resort_name if owner else 'Resort'
        
        notification = Notification(
            notification_type='reservation_confirmed',
            title='Reservation Confirmed',
            message=f'Your reservation for {resource_name} at {resort_name} has been confirmed!',
            related_user_id=r.user_id,
            related_reservation_id=r.id
        )
        db.session.add(notification)
        
    elif action == 'cancel':
        r.status = 'cancelled'
        r.expires_at = None  # Clear expiration when cancelled
    else:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    db.session.commit()
    return jsonify({'success': True, 'status': r.status})


@app.route('/api/confirmed_reservations', methods=['GET'])
def api_confirmed_reservations():
    """Return list of confirmed reservation dates for an owner/resource in a given month.
    Query params: owner_id, resource_type (optional), resource_id (optional), month (1-12), year
    Response: { success: True, dates: ['YYYY-MM-DD', ...] }
    """
    owner_id = request.args.get('owner_id')
    resource_type = request.args.get('resource_type')
    resource_id = request.args.get('resource_id')
    try:
        month = int(request.args.get('month') or 0)
        year = int(request.args.get('year') or 0)
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid month/year'}), 400
    if not owner_id:
        return jsonify({'success': False, 'message': 'owner_id required'}), 400

    # build base query
    q = Reservation.query.filter_by(owner_id=owner_id, status='confirmed')
    if resource_type:
        q = q.filter(Reservation.resource_type == resource_type)
    if resource_id:
        q = q.filter(Reservation.resource_id == resource_id)

    results = q.all()

    # compute first and last day of month
    from calendar import monthrange
    from datetime import timedelta
    try:
        first_day = datetime(year, month, 1).date()
    except Exception:
        return jsonify({'success': False, 'message': 'Invalid month/year combination'}), 400
    last_day = datetime(year, month, monthrange(year, month)[1]).date()

    dates = set()
    for r in results:
        # if reservation overlaps the month
        if not r.check_in or not r.check_out:
            continue
        if r.check_out < first_day or r.check_in > last_day:
            continue
        # overlap -> enumerate dates within the overlap range
        start = max(r.check_in, first_day)
        end = min(r.check_out, last_day)
        d = start
        while d <= end:
            dates.add(d.isoformat())
            d = d + timedelta(days=1)

    return jsonify({'success': True, 'dates': sorted(list(dates))})


@app.route('/api/user/reservations', methods=['GET'])
def api_user_reservations():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    
    # Auto-expire pending reservations that are past 24 hours
    now = datetime.utcnow()
    expired = Reservation.query.filter(
        Reservation.user_id == session['user_id'],
        Reservation.status == 'pending',
        Reservation.expires_at != None,
        Reservation.expires_at <= now
    ).all()
    for r in expired:
        r.status = 'expired'
    if expired:
        db.session.commit()
    
    resvs = Reservation.query.filter_by(user_id=session['user_id']).order_by(Reservation.created_at.desc()).all()
    out = []
    for r in resvs:
        out.append({
            'id': r.id,
            'resource_type': r.resource_type,
            'resource_id': r.resource_id,
            'check_in': r.check_in.isoformat() if r.check_in else None,
            'check_out': r.check_out.isoformat() if r.check_out else None,
            'guests': r.guests,
            'status': r.status,
            'owner_id': r.owner_id,
            'expires_at': r.expires_at.isoformat() if r.expires_at else None,
        })
    return jsonify({'success': True, 'reservations': out})


@app.route('/api/user/reservations/<int:reservation_id>/action', methods=['POST'])
def api_user_reservation_action(reservation_id):
    # user-only actions like cancel
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    r = db.session.get(Reservation, reservation_id)
    if not r or r.user_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Reservation not found or not authorized'}), 404
    data = request.get_json() or {}
    action = (data.get('action') or '').lower()
    if action == 'cancel':
        r.status = 'cancelled'
        r.expires_at = None  # Clear expiration when cancelled
    else:
        return jsonify({'success': False, 'message': 'Invalid action'}), 400
    db.session.commit()
    return jsonify({'success': True, 'status': r.status})


@app.route('/api/user/reservations/<int:reservation_id>/details', methods=['GET'])
def api_user_reservation_details(reservation_id):
    # Get detailed reservation information for modal view
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'}), 401
    
    r = db.session.get(Reservation, reservation_id)
    if not r or r.user_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Reservation not found or not authorized'}), 404
    
    # Check if reservation has expired
    if r.status == 'pending' and r.expires_at and r.expires_at <= datetime.utcnow():
        r.status = 'expired'
        db.session.commit()
    
    # Get resource details
    resource = None
    resource_features = []
    resource_image = None
    
    if r.resource_type == 'room':
        resource = db.session.get(Room, r.resource_id)
        if resource:
            resource_features = [
                f"{resource.capacity} Person Capacity" if resource.capacity else None,
                f"{resource.beds} Beds" if resource.beds else None,
                resource.other_feature2,
                resource.other_feature3,
                resource.other_feature5
            ]
            resource_image = resource.image1 or resource.image2 or resource.image3
    else:  # cottage
        resource = db.session.get(Cottage, r.resource_id)
        if resource:
            resource_features = [
                f"{resource.capacity} Person Capacity" if resource.capacity else None,
                f"{resource.beds} Beds" if resource.beds else None,
                resource.other_feature2,
                resource.other_feature3,
                resource.other_feature5
            ]
            resource_image = resource.image1 or resource.image2 or resource.image3
    
    # Filter out None/empty features
    resource_features = [f for f in resource_features if f and f.strip()]
    
    # Get owner/resort info
    owner = db.session.get(Owner, r.owner_id)
    
    reservation_data = {
        'id': r.id,
        'title': resource.name if resource else (r.resource_type.title()),
        'resort_name': owner.resort_name if owner else 'Resort',
        'check_in': r.check_in.isoformat() if r.check_in else None,
        'check_out': r.check_out.isoformat() if r.check_out else None,
        'guests': r.guests or '1',
        'status': r.status,
        'resource_type': r.resource_type,
        'owner_id': r.owner_id,
        'created_at': r.created_at.isoformat() if r.created_at else None,
        'expires_at': r.expires_at.isoformat() if r.expires_at else None,
        'features': resource_features,
        'image': resource_image,
        'price': resource.price if resource else None
    }
    
    return jsonify({'success': True, 'reservation': reservation_data})


@app.route('/api/recent_conversations', methods=['GET'])
def api_recent_conversations():
    """Return recent conversations for the currently logged-in user or owner.
    Response: { success: True, conversations: [ { id, partner_name, partner_avatar, last_text, last_time, unread, owner_id, user_id } ] }
    """
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    convs = []
    if 'user_id' in session:
        rows = Conversation.query.filter_by(user_id=session['user_id']).order_by(Conversation.created_at.desc()).all()
        for c in rows:
            last_msg = c.messages[-1] if c.messages else None
            partner_name = c.owner.resort_name if c.owner and c.owner.resort_name else (c.owner.name if c.owner else 'Owner')
            unread = False
            if last_msg and last_msg.sender == 'owner':
                # treat last messages from owner as unread for the user (simple heuristic)
                unread = True
            convs.append({
                'id': c.id,
                'partner_name': partner_name,
                'partner_avatar': c.owner.avatar if c.owner else None,
                'last_text': last_msg.text if last_msg else None,
                'last_time': last_msg.created_at.isoformat() if last_msg else None,
                'unread': unread,
                'owner_id': c.owner_id,
                'user_id': c.user_id,
            })
    else:
        rows = Conversation.query.filter_by(owner_id=session['owner_id']).order_by(Conversation.created_at.desc()).all()
        for c in rows:
            last_msg = c.messages[-1] if c.messages else None
            partner_name = c.user.name if c.user and c.user.name else 'Customer'
            unread = False
            if last_msg and last_msg.sender == 'user':
                # treat last messages from user as unread for the owner
                unread = True
            convs.append({
                'id': c.id,
                'partner_name': partner_name,
                'partner_avatar': c.user.avatar if c.user else None,
                'last_text': last_msg.text if last_msg else None,
                'last_time': last_msg.created_at.isoformat() if last_msg else None,
                'unread': unread,
                'owner_id': c.owner_id,
                'user_id': c.user_id,
            })

    return jsonify({'success': True, 'conversations': convs})


@app.route('/api/pending_reservations', methods=['GET'])
def api_pending_reservations():
    """Return pending reservations for the currently logged-in user or owner.
    Response: { success: True, reservations: [ { id, resort_name, resource_name, resource_type, check_in, check_out, guests, status, created_at, can_cancel } ] }
    """
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401

    # Auto-expire pending reservations that are past 24 hours
    now = datetime.utcnow()
    expired = Reservation.query.filter(
        Reservation.status == 'pending',
        Reservation.expires_at != None,
        Reservation.expires_at <= now
    ).all()
    for r in expired:
        r.status = 'expired'
    if expired:
        db.session.commit()

    reservations = []
    
    if 'user_id' in session:
        # User view: show user's pending reservations
        resvs = Reservation.query.filter_by(
            user_id=session['user_id'], 
            status='pending'
        ).order_by(Reservation.created_at.desc()).all()
        
        for r in resvs:
            # Get resource details
            resource_name = 'Unknown'
            if r.resource_type == 'room':
                resource = db.session.get(Room, r.resource_id)
                resource_name = resource.name if resource else 'Room'
            elif r.resource_type == 'cottage':
                resource = db.session.get(Cottage, r.resource_id)
                resource_name = resource.name if resource else 'Cottage'
            
            # Get owner/resort info
            owner = db.session.get(Owner, r.owner_id)
            resort_name = owner.resort_name if owner else 'Resort'
            
            reservations.append({
                'id': r.id,
                'resort_name': resort_name,
                'resource_name': resource_name,
                'resource_type': r.resource_type,
                'check_in': r.check_in.isoformat() if r.check_in else None,
                'check_out': r.check_out.isoformat() if r.check_out else None,
                'guests': r.guests or '1',
                'status': r.status,
                'created_at': r.created_at.isoformat() if r.created_at else None,
                'expires_at': r.expires_at.isoformat() if r.expires_at else None,
                'can_cancel': True  # Users can cancel their own pending reservations
            })
    
    elif 'owner_id' in session:
        # Owner view: show pending reservations for owner's resources
        resvs = Reservation.query.filter_by(
            owner_id=session['owner_id'], 
            status='pending'
        ).order_by(Reservation.created_at.desc()).all()
        
        for r in resvs:
            # Get resource details
            resource_name = 'Unknown'
            if r.resource_type == 'room':
                resource = db.session.get(Room, r.resource_id)
                resource_name = resource.name if resource else 'Room'
            elif r.resource_type == 'cottage':
                resource = db.session.get(Cottage, r.resource_id)
                resource_name = resource.name if resource else 'Cottage'
            
            # Get user info
            user = db.session.get(User, r.user_id)
            customer_name = user.name if user else 'Customer'
            
            reservations.append({
                'id': r.id,
                'customer_name': customer_name,
                'resource_name': resource_name,
                'resource_type': r.resource_type,
                'check_in': r.check_in.isoformat() if r.check_in else None,
                'check_out': r.check_out.isoformat() if r.check_out else None,
                'guests': r.guests or '1',
                'status': r.status,
                'created_at': r.created_at.isoformat() if r.created_at else None,
                'expires_at': r.expires_at.isoformat() if r.expires_at else None,
                'can_approve': True,  # Owners can approve/decline reservations
                'user_id': r.user_id
            })

    return jsonify({'success': True, 'reservations': reservations})


@app.route('/api/user/notifications', methods=['GET'])
def api_user_notifications():
    """Return notifications for the currently logged-in user.
    Response: { success: True, notifications: [ { id, type, title, message, is_read, created_at } ] }
    """
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    # Get notifications for this user
    notifications = Notification.query.filter_by(
        related_user_id=session['user_id']
    ).order_by(Notification.created_at.desc()).limit(20).all()
    
    notification_list = []
    for notif in notifications:
        notification_list.append({
            'id': notif.id,
            'type': notif.notification_type,
            'title': notif.title,
            'message': notif.message,
            'is_read': notif.is_read,
            'created_at': notif.created_at.isoformat() if notif.created_at else None
        })
    
    return jsonify({'success': True, 'notifications': notification_list})


@app.route('/api/owner/notifications', methods=['GET'])
def api_owner_notifications():
    """Return notifications for the currently logged-in owner.
    Response: { success: True, notifications: [ { id, type, title, message, is_read, created_at } ] }
    """
    if 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    # Get notifications for this owner
    notifications = Notification.query.filter_by(
        related_owner_id=session['owner_id']
    ).order_by(Notification.created_at.desc()).limit(20).all()
    
    notification_list = []
    for notif in notifications:
        notification_list.append({
            'id': notif.id,
            'type': notif.notification_type,
            'title': notif.title,
            'message': notif.message,
            'is_read': notif.is_read,
            'created_at': notif.created_at.isoformat() if notif.created_at else None
        })
    
    return jsonify({'success': True, 'notifications': notification_list})


@app.route('/api/notifications/<int:notification_id>/mark-read', methods=['POST'])
def api_mark_notification_read(notification_id):
    """Mark a notification as read."""
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    notification = db.session.get(Notification, notification_id)
    if not notification:
        return jsonify({'success': False, 'message': 'Notification not found'}), 404
    
    # Verify ownership
    if 'user_id' in session and notification.related_user_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Not authorized'}), 403
    if 'owner_id' in session and notification.related_owner_id != session['owner_id']:
        return jsonify({'success': False, 'message': 'Not authorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/notifications/unread-count', methods=['GET'])
def api_unread_notification_count():
    """Get unread notification count for current user/owner."""
    if 'user_id' not in session and 'owner_id' not in session:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    count = 0
    if 'user_id' in session:
        count = Notification.query.filter_by(
            related_user_id=session['user_id'],
            is_read=False
        ).count()
    elif 'owner_id' in session:
        count = Notification.query.filter_by(
            related_owner_id=session['owner_id'],
            is_read=False
        ).count()
    
    return jsonify({'success': True, 'count': count})


@app.route('/viewResortRoom')
def view_resort_room():
    owner_id = request.args.get('owner_id')
    owner = None
    rooms = []
    if owner_id:
        owner = db.session.get(Owner, owner_id)
        if owner:
            rooms = [r for r in getattr(owner, 'rooms', []) or [] if r.status == 'approved']
    else:
        # show all approved rooms when no owner specified
        rooms = Room.query.filter_by(status='approved').all()

    return render_template('viewResortRoom.html', owner=owner, rooms=rooms)


@app.route('/viewResortCottage')
def view_resort_cottage():
    owner_id = request.args.get('owner_id')
    owner = None
    cottages = []
    if owner_id:
        owner = db.session.get(Owner, owner_id)
        if owner:
            cottages = [c for c in getattr(owner, 'cottages', []) or [] if c.status == 'approved']
    else:
        # show all approved cottages when no owner specified
        cottages = Cottage.query.filter_by(status='approved').all()

    return render_template('viewResortCottage.html', owner=owner, cottages=cottages)


@app.route('/viewResortFood')
def view_resort_food():
    owner_id = request.args.get('owner_id')
    owner = None
    foods = []
    if owner_id:
        owner = db.session.get(Owner, owner_id)
        if owner:
            foods = [f for f in getattr(owner, 'foods', []) or [] if f.status == 'approved']
    else:
        # show all approved foods when no owner specified
        foods = Food.query.filter_by(status='approved').all()

    return render_template('viewResortFood.html', owner=owner, foods=foods)


@app.route('/viewResortActivities')
def view_resort_activities():
    owner_id = request.args.get('owner_id')
    owner = None
    activities = []
    if owner_id:
        owner = db.session.get(Owner, owner_id)
        if owner:
            activities = [a for a in getattr(owner, 'activities', []) or [] if a.status == 'approved']
    else:
        # show all approved activities when no owner specified
        activities = Activity.query.filter_by(status='approved').all()

    return render_template('viewResortActivities.html', owner=owner, activities=activities)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

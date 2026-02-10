import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if not os.environ.get('DATABASE_URL'):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.environ['DATABASE_URL'] = f'sqlite:///{os.path.join(base_dir, "instance", "site.db")}'

from app import app, db, Rating
with app.app_context():
    r = db.session.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='rating'"))
    tables = list(r)
    if tables:
        print("✅ Rating table exists!")
        # Show columns
        cols = db.session.execute(db.text("PRAGMA table_info(rating)"))
        for col in cols:
            print(f"  - {col[1]} ({col[2]})")
    else:
        print("❌ Rating table does NOT exist")

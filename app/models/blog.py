from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

class User(db.Model):
    # __tablename__ specifies the name of the table in the database
    __tablename__ = "users"

    # Primary key uniquely identifies each record
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False means NOT NULL in SQL; unique=True prevents duplicate usernames/emails
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship: A helper property that doesn't exist as a physical column in the DB table,
    # but lets you access a user's posts via `user.posts`.
    # backref='author' allows you to access the User object from a Post via `post.author`.
    # cascade='all, delete-orphan' ensures deleting a user also deletes their posts.
    posts = db.relationship("Post", backref="author", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ForeignKey creates a relational constraint tying this post to a specific user's id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        """Helper method to serialize SQLAlchemy model instance to a standard Python dictionary for JSON responses."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "author_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<Post {self.title[:20]}>"
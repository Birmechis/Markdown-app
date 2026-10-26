from flask_wtf.file import FileRequired, FileAllowed
from app import db
from datetime import datetime, timezone
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

class AttachmentForm(FlaskForm):
    file = FileField('file', validators=[
        FileRequired(message="Please select a file to upload."),
        FileAllowed(['jpg', 'png', 'pdf', 'txt '], 'Images, PDFs, and Text only!')
    ])
    submit = SubmitField('Upload File')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False, unique=True)
    markdown_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"Note: {self.title}, {self.markdown_content}"

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    unique_name = db.Column(db.String(255), nullable=False, unique=True)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    note_id = db.Column(db.Integer, db.ForeignKey(Note.id), nullable=False)

    def __repr__(self):
        return f"Attachment: {self.original_name}, {self.unique_name}"

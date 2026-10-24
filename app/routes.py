from flask import request, jsonify, Blueprint
from app.models import Note
from app import db

bp = Blueprint('api', __name__)

@bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()

    title = data.get('title')
    markdown_content = data.get('markdown_content')
    notes = Note(
        title=title,
        markdown_content=markdown_content
    )

    db.session.add(notes)
    db.session.commit()

    return jsonify({
        "id": notes.id,
        "title": notes.title,
        "markdown_content": notes.markdown_content,
        "created_at": notes.created_at.isoformat() if notes.created_at else None,
        "updated_at": notes.updated_at.isoformat() if notes.updated_at else None
    }), 201

@bp.route('/notes', methods=['GET'])
def get_notes():
    data = Note.query.all()

    output = []
    for note in data:
        output.append({
            "id": note.id,
            "title": note.title,
            "markdown_content": note.markdown_content,
            "created_at": note.created_at.isoformat() if note.created_at else None,
            "updated_at": note.updated_at.isoformat() if note.updated_at else None
        })

    return {"notes": output}, 200

@bp.route('/notes/<int:id>', methods=['GET'])
def get_note(id):

    data = Note.query.filter_by(id=id).first()

    if not data:
        return jsonify({
            "error": "Note not found"
        }), 404

    return jsonify({
        "id": data.id,
        "title": data.title,
        "markdown_content": data.markdown_content,
        "created_at": data.created_at.isoformat() if data.created_at else None,
        "updated_at": data.updated_at.isoformat() if data.updated_at else None
    }), 200

@bp.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):

    data = request.get_json()

    if not data or "title" not in data or "markdown_content" not in data:
        return jsonify({
            "error": "Missing fields"
        }), 400

    title = data.get('title')
    markdown_content = data.get('markdown_content')

    note = Note.query.filter_by(id=id).first()

    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    note.title = title
    note.markdown_content = markdown_content

    db.session.commit()

    return jsonify({
        "id": note.id,
        "title": note.title,
        "markdown_content": note.markdown_content,
        "created_at": note.created_at.isoformat() if note.created_at else None,
        "updated_at": note.updated_at.isoformat() if note.updated_at else None
    }), 200

@bp.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):

    note = Note.query.filter_by(id=id).first()

    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    db.session.delete(note)
    db.session.commit()

    return "", 204
from flask import request, jsonify, Blueprint
from app.models import Note
from app import db

bp = Blueprint('api', __name__)

@bp.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()

    title = data.get('title')
    markdown_content = data.get('markdown_content')

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    if not title or not markdown_content:
        return jsonify({
            "error": "Missing 'title' and 'markdown_content'"
        }), 400

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
        "created_at": notes.created_at.isoformat(),
        "updated_at": notes.updated_at.isoformat()
    }), 201

@bp.route('/notes', methods=['GET'])
def get_notes():
    data = Note.query.all()

    if not data:
        return jsonify({
            "error": "Note not found"
        }), 404

    output = []
    for note in data:
        output.append({
            "id": note.id,
            "title": note.title,
            "markdown_content": note.markdown_content,
            "created_at": note.created_at.isoformat()
        })

    return {"Notes": output}, 200

@bp.route('/notes/<int:id>', methods=['GET'])
def get_note(id):

    data = Note.query.get(id)

    if not data:
        return jsonify({
            "error": "Note not found"
        }), 404

    return jsonify({
        "id": data.id,
        "title": data.title,
        "markdown_content": data.markdown_content,
        "created_at": data.created_at.isoformat()
    }), 200

@bp.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Data not found"
        }), 404

    note = Note.query.filter_by(id=id).first()

    if not note:
        return jsonify({
            "error": "Note not found"
        }), 404

    note.title = data.get('title', note.title)
    note.markdown_content = data.get('markdown_content', note.markdown_content)

    db.session.commit()

    return jsonify({
        "id": note.id,
        "title": note.title,
        "markdown_content": note.markdown_content,
        "created_at": note.created_at.isoformat(),
        "updated_at": note.updated_at.isoformat()
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
import uuid
import language_tool_python
import markdown
from pathlib import Path
from flask import request, jsonify, Blueprint, Response, render_template, current_app
from werkzeug.utils import secure_filename
from app.models import Note, AttachmentForm, Attachment
from app import db

bp = Blueprint('api', __name__, template_folder='templates')
tool = language_tool_python.LanguageTool('en-US')



@bp.route('/notes', methods=['POST'])
def create_note():

    if not request.is_json:
        return jsonify({
            "error": "Request must be json object"
        }), 425

    data = request.get_json()

    title = data.get('title')
    markdown_content = data.get('markdown_content')

    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "The title field is required and must be a non-empty string"
        }), 400

    if not markdown_content or not isinstance(markdown_content, str) or not markdown_content.strip():
        return jsonify({
            "error": "The markdown_content field is required and must be a non-empty string"
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

    if not request.is_json:
        return jsonify({
            "error": "Request must be json object"
        }), 415

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing or invalid JSON request body"
        }), 400

    title = data.get('title')
    markdown_content = data.get('markdown_content')

    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "The title field is required and must be a non-empty string"
        }), 400

    if not markdown_content or not isinstance(markdown_content, str) or not markdown_content.strip():
        return jsonify({
            "error": "The markdown_content field is required and must be a non-empty string"
        }), 400

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

@bp.route('/notes/<int:id>/checks', methods=['POST'])
def grammar_check():

    if not request.is_json:
        return jsonify({
            "error": "Request must be json object"
        }), 415

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Missing or invalid JSON request body"
        }), 400

    title = data.get('title')
    markdown_content = data.get('markdown_content')

    if not title or not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "The title field is required and must be a non-empty string"
        }), 400

    if not markdown_content or not isinstance(markdown_content, str) or not markdown_content.strip():
        return jsonify({
            "error": "The markdown_content field is required and must be a non-empty string"
        }), 400

    clean_title = title.strip()
    clean_markdown_content = markdown_content.strip()

    full_text = f"{clean_title}\n{clean_markdown_content}"

    matches = tool.check(full_text)

    results = []
    for match in matches:
        results.append({
            "message": match.message,
            "sentence": match.sentence,
            "offset": match.offset,
            "error_length": match.error_length,
            "replacement": match.replacements,
        })

    return jsonify({
        "original_text": full_text,
        "errors": len(results),
        "matches": results
    }), 200

@bp.route('/notes/<int:id>/render', methods=['GET'])
def render_note(id):

    data = Note.filter_by(id=id).first()

    if not data:
        return jsonify({
            "error": "Note not found"
        }), 404

    html_output = markdown.markdown(data.markdown_content)

    return Response(html_output, mimetype='text/html')

@bp.route('/notes/<int:id>/attachments', methods=['POST'])
def attach_note(id):

    note = Note.query.get_or_404(id)

    form = AttachmentForm()

    if form.validate_on_submit():
        file = form.file.data

        original_name = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}{Path(original_name).suffix}"

        target_path = current_app.config['UPLOAD_FOLDER']/unique_filename
        file.save(str(target_path))

        new_attachment = Attachment(
            original_name=original_name,
            unique_name=unique_filename,
            note_id=note.id,
        )

        db.session.add(new_attachment)
        db.session.commit()

        return jsonify({
            "msg": "Note successfully uploaded",
            "attachment": {
                "id": new_attachment.id,
                "original_name": new_attachment.original_name,
                "unique_name": new_attachment.unique_name,
                "note_id": new_attachment.note_id
            }
        }), 200

    return render_template('index.html', form=form, note=note)

@bp.route('/notes/<int:id>/attachments', methods=['GET'])
def get_attachment(id):

    note = Note.query.get_or_404(id)

    attachments = note.attachments

    if not attachments:
        return jsonify({"attachments": []}), 200

    results = []
    for item in attachments:
        results.append({
            "id": item.id,
            "original_name": item.original_name,
            "unique_name": item.unique_name,
            "uploaded_at": item.uploaded_at.isoformat() if item.uploaded_at else None,
            "note_id": item.note_id
        })

    return jsonify({
        "attachments": results
    }), 200
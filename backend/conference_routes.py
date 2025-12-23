from flask import Blueprint, request
from datetime import datetime
from .models import db, Conference, Track
from .utils import error_response, success_response

conference_bp = Blueprint('conference_bp', __name__)

@conference_bp.route('/conference', methods=['POST'])
def create_conference():
    data = request.get_json()
    name = data.get('name')
    start_date = datetime.fromisoformat(data.get('start_date'))
    end_date = datetime.fromisoformat(data.get('end_date'))
    submission_deadline = datetime.fromisoformat(data.get('submission_deadline'))

    if submission_deadline > end_date:
        return error_response("Submission deadline must be before end date")

    conf = Conference(
        name=name,
        start_date=start_date,
        end_date=end_date,
        submission_deadline=submission_deadline,
        description=data.get('description')
    )
    db.session.add(conf)
    db.session.commit()
    return success_response({"id": conf.id}, "Conference created successfully")

@conference_bp.route('/conference/active', methods=['GET'])
def get_active_conferences():
    now = datetime.now()
    active_confs = Conference.query.filter(Conference.submission_deadline >= now).all()
    data = [
        {
            "id": c.id,
            "name": c.name,
            "submission_deadline": c.submission_deadline.isoformat(),
            "end_date": c.end_date.isoformat()
        } for c in active_confs
    ]
    return success_response(data)

@conference_bp.route('/track', methods=['POST'])
def create_track():
    data = request.get_json()
    name = data.get('name')
    conference_id = data.get('conference_id')

    track = Track(name=name, conference_id=conference_id)
    db.session.add(track)
    db.session.commit()
    return success_response({"id": track.id}, "Track created successfully")

@conference_bp.route('/track/<int:track_id>', methods=['PUT'])
def update_track(track_id):
    track = Track.query.get(track_id)
    if not track:
        return error_response("Track not found", 404)
    data = request.get_json()
    track.name = data.get('name', track.name)
    db.session.commit()
    return success_response(message="Track updated successfully")

@conference_bp.route('/track/<int:track_id>', methods=['DELETE'])
def delete_track(track_id):
    track = Track.query.get(track_id)
    if not track:
        return error_response("Track not found", 404)
    db.session.delete(track)
    db.session.commit()
    return success_response(message="Track deleted successfully")

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Asset, Request
from schemas import UserSchema, AssetSchema, RequestSchema
from decorators import role_required
from marshmallow import ValidationError
import cloudinary.uploader
import logging

bp = Blueprint('inventory', __name__)
user_schema = UserSchema()
asset_schema = AssetSchema()
request_schema = RequestSchema()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def success_response(message, data=None):
    response = {'status': 'success', 'message': message}
    if data:
        response['data'] = data
    return jsonify(response)

def error_response(message, errors=None):
    response = {'status': 'error', 'message': message}
    if errors:
        response['errors'] = errors
    return jsonify(response)

@bp.route('/assets', methods=['POST'])
@jwt_required()
@role_required('admin', 'procurement_manager')
def add_asset():
    data = request.form.to_dict()
    files = request.files.to_dict()
    logger.debug(f"Received data: {data}")
    logger.debug(f"Received files: {files}")

    try:
        asset_data = asset_schema.load(data)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return error_response('Validation error', err.messages), 400

    image_url = None
    if 'image' in request.files:
        image = request.files['image']
        try:
            upload_response = cloudinary.uploader.upload(image)
            image_url = upload_response['secure_url']
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return error_response('Image upload error'), 500

    new_asset = Asset(
        name=asset_data['name'],
        description=asset_data['description'],
        category=asset_data['category'],
        image_url=image_url
    )
    db.session.add(new_asset)
    db.session.commit()
    logger.debug(f"Asset added: {asset_schema.dump(new_asset)}")
    return success_response('Asset added successfully', asset_schema.dump(new_asset))

@bp.route('/assets/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return success_response('Asset retrieved successfully', asset_schema.dump(asset))

@bp.route('/assets/<int:asset_id>', methods=['PUT'])
@jwt_required()
@role_required('admin', 'procurement_manager')
def update_asset(asset_id):
    data = request.form.to_dict()
    logger.debug(f"Received data: {data}")

    try:
        asset_data = asset_schema.load(data, partial=True)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return error_response('Validation error', err.messages), 400

    asset = Asset.query.get_or_404(asset_id)
    for key, value in asset_data.items():
        setattr(asset, key, value)

    if 'image' in request.files:
        image = request.files['image']
        try:
            upload_response = cloudinary.uploader.upload(image)
            asset.image_url = upload_response['secure_url']
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return error_response('Image upload error'), 500

    db.session.commit()
    logger.debug(f"Asset updated: {asset_schema.dump(asset)}")
    return success_response('Asset updated successfully', asset_schema.dump(asset))

@bp.route('/assets/<int:asset_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin', 'procurement_manager')
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return success_response('Asset deleted successfully')

@bp.route('/assets', methods=['GET'])
@jwt_required()
def get_all_assets():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    assets = Asset.query.paginate(page, per_page, False)
    return success_response('Assets retrieved successfully', asset_schema.dump(assets.items, many=True))

@bp.route('/assets/<int:asset_id>/allocate', methods=['POST'])
@jwt_required()
@role_required('procurement_manager')
def allocate_asset(asset_id):
    data = request.get_json()
    asset = Asset.query.get_or_404(asset_id)
    user = User.query.get_or_404(data['user_id'])
    asset.allocated_to = user.id
    db.session.commit()
    return success_response('Asset allocated successfully')

@bp.route('/requests', methods=['POST'])
@jwt_required()
@role_required('employee')
def create_request():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_request = Request(
        asset_id=data['asset_id'],
        user_id=current_user['id'],
        reason=data['reason'],
        quantity=data['quantity'],
        urgency=data['urgency']
    )
    db.session.add(new_request)
    db.session.commit()
    return success_response('Request submitted successfully', request_schema.dump(new_request))

@bp.route('/requests/<int:request_id>', methods=['PATCH'])
@jwt_required()
@role_required('procurement_manager')
def update_request(request_id):
    data = request.get_json()
    req = Request.query.get_or_404(request_id)
    req.status = data.get('status', req.status)
    db.session.commit()
    return success_response('Request updated successfully')

@bp.route('/requests/pending', methods=['GET'])
@jwt_required()
@role_required('procurement_manager')
def get_pending_requests():
    requests = Request.query.filter_by(status='Pending').all()
    return success_response('Pending requests retrieved successfully', [{
        'id': req.id,
        'asset_id': req.asset_id,
        'user_id': req.user_id,
        'reason': req.reason,
        'quantity': req.quantity,
        'urgency': req.urgency,
        'status': req.status
    } for req in requests])

@bp.route('/requests/completed', methods=['GET'])
@jwt_required()
@role_required('procurement_manager')
def get_completed_requests():
    requests = Request.query.filter_by(status='approved').all()
    return success_response('Completed requests retrieved successfully', [{
        'id': req.id,
        'asset_id': req.asset_id,
        'user_id': req.user_id,
        'reason': req.reason,
        'quantity': req.quantity,
        'urgency': req.urgency,
        'status': req.status
    } for req in requests])

@bp.route('/user/requests', methods=['GET'])
@jwt_required()
def get_user_requests():
    current_user = get_jwt_identity()
    requests = Request.query.filter_by(user_id=current_user['id']).all()
    return success_response('User requests retrieved successfully', [{
        'id': req.id,
        'asset_id': req.asset_id,
        'reason': req.reason,
        'quantity': req.quantity,
        'urgency': req.urgency,
        'status': req.status
    } for req in requests])

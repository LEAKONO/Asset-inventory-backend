from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Asset, Request
from schemas import UserSchema, AssetSchema, RequestSchema
from decorators import role_required
from marshmallow import ValidationError

bp = Blueprint('inventory', __name__)
user_schema = UserSchema()
asset_schema = AssetSchema()
request_schema = RequestSchema()

# Add an asset (including category and image)
@bp.route('/assets', methods=['POST'])
@jwt_required()
@role_required('admin', 'procurement_manager')
def add_asset():
    data = request.get_json()
    try:
        asset = asset_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_asset = Asset(
        name=asset['name'],
        description=asset['description'],
        category=asset['category'],
        image_url=asset.get('image_url')
    )
    db.session.add(new_asset)
    db.session.commit()
    return jsonify({'message': 'Asset added successfully'}), 201

# Get details of a specific asset
@bp.route('/assets/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return jsonify(asset_schema.dump(asset))

# Update an asset (including category and image)
@bp.route('/assets/<int:asset_id>', methods=['PUT'])
@jwt_required()
@role_required('admin', 'procurement_manager')
def update_asset(asset_id):
    data = request.get_json()
    try:
        asset_data = asset_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    asset = Asset.query.get_or_404(asset_id)
    for key, value in asset_data.items():
        setattr(asset, key, value)
    db.session.commit()
    return jsonify({'message': 'Asset updated successfully'})

# Delete an asset
@bp.route('/assets/<int:asset_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin', 'procurement_manager')
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    return jsonify({'message': 'Asset deleted successfully'})

# Get all assets
@bp.route('/assets', methods=['GET'])
@jwt_required()
def get_all_assets():
    assets = Asset.query.all()
    return jsonify(asset_schema.dump(assets, many=True))

# Allocate an asset to a user
@bp.route('/assets/<int:asset_id>/allocate', methods=['POST'])
@jwt_required()
@role_required('procurement_manager')
def allocate_asset(asset_id):
    data = request.get_json()
    asset = Asset.query.get_or_404(asset_id)
    user = User.query.get_or_404(data['user_id'])
    asset.allocated_to = user.id
    db.session.commit()
    return jsonify({'message': 'Asset allocated successfully'})

# Create a request for an asset
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
    return jsonify({'message': 'Request submitted successfully'}), 201

# Update a request
@bp.route('/requests/<int:request_id>', methods=['PATCH'])
@jwt_required()
@role_required('procurement_manager')
def update_request(request_id):
    data = request.get_json()
    req = Request.query.get_or_404(request_id)
    req.status = data.get('status', req.status)
    db.session.commit()
    return jsonify({'message': 'Request updated successfully'})

# Get pending requests
@bp.route('/requests/pending', methods=['GET'])
@jwt_required()
@role_required('procurement_manager')
def get_pending_requests():
    requests = Request.query.filter_by(status='Pending').all()
    return jsonify([{
        'id': req.id,
        'asset_id': req.asset_id,
        'user_id': req.user_id,
        'reason': req.reason,
        'quantity': req.quantity,
        'urgency': req.urgency,
        'status': req.status
    } for req in requests])

# Get completed requests
@bp.route('/requests/completed', methods=['GET'])
@jwt_required()
@role_required('procurement_manager')
def get_completed_requests():
    requests = Request.query.filter_by(status='approved').all()
    return jsonify([{
        'id': req.id,
        'asset_id': req.asset_id,
        'user_id': req.user_id,
        'reason': req.reason,
        'quantity': req.quantity,
        'urgency': req.urgency,
        'status': req.status
    } for req in requests])

# Get user-specific requests
@bp.route('/user/requests', methods=['GET'])
@jwt_required()
def get_user_requests():
    current_user = get_jwt_identity()
    requests = Request.query.filter_by(user_id=current_user['id']).all()
    return jsonify([{
        'id': req.id,
        'asset_id': req.asset_id,
        'reason': req.reason,
        'quantity': req.quantity,
        'urgency': req.urgency,
        'status': req.status
    } for req in requests])


from flask import Blueprint

def register_routes(app):
    """
    Registers all Flask blueprints to the application instance.
    Currently includes:
    - upload_bp: handles CSV upload routes
    """
    from backend.routes.upload import upload_bp
    app.register_blueprint(upload_bp)

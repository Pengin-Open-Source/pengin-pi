from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.db import db
from app.db.models import User, Company, CompanyMembers

company_info = Blueprint('company_info', __name__, url_prefix="/companies")

# TODO Split profile routes into companies and profiles routes. Follow single responsibility principle.
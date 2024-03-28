from collections import namedtuple
from functools import partial, wraps


from flask import abort, request
from flask_principal import Permission, RoleNeed


admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
hiring_permission = Permission(RoleNeed('hiring_manager'))

# Wrapping a Permission function that uses an id (orders, posts, companies, etc)
# Using this so we can make decorators out of Permissions that need to check ids
# Apparently Google Gemini found a function from github.com/Gibson-Gichuru/Memy.
# I reworked it with Gemini to accept any kinds of ids.


def permission_required(permission, id_kind):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            id_used = request.view_args.get(id_kind)
            if not id_used:
                abort(404)  # HTTP NOT Found if id_kind is not found in URL
            if not permission(id_used).can():
                abort(403)  # HTTP Forbidden
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def set_need(func_str):
    nt = namedtuple(func_str, ['method', 'value'])
    return partial(nt, func_str)


delete_comment_need = set_need("delete_comment")
edit_comment_need = set_need("edit_comment")
delete_post_need = set_need("delete_post")
edit_post_need = set_need("edit_post")
delete_ticket_need = set_need("delete_ticket")
delete_ticket_comment_need = set_need("delete_ticket_comment")
edit_ticket_need = set_need("edit_ticket_comment")
edit_ticket_comment_need = set_need("edit_ticket")
view_ticket_need = set_need("view_ticket")


edit_status_need = set_need('edit_status')
accept_applicant_need = set_need('accept_applicant')
reject_applicant_need = set_need('reject_applicant')
delete_applicant_need = set_need('delete_applicant')

my_applications_need = set_need('my_applications')


view_company_need = set_need("view_company")
access_event_need = set_need("access_event")
view_thread_need = set_need("view_thread")


def delete_comment_permission(post_id): return RoutePermission(
    delete_comment_need, post_id)


def edit_comment_permission(post_id): return RoutePermission(
    edit_comment_need, post_id)


def delete_post_permission(post_id): return RoutePermission(
    delete_post_need, post_id)


def edit_post_permission(post_id): return RoutePermission(
    edit_post_need, post_id)


def delete_ticket_permission(ticket_id): return RoutePermission(
    delete_ticket_need, ticket_id)


def delete_ticket_comment_permission(ticket_id): return RoutePermission(
    delete_ticket_comment_need, ticket_id)


def edit_ticket_permission(ticket_id): return RoutePermission(
    edit_ticket_need, ticket_id)


def view_ticket_permission(ticket_id): return RoutePermission(
    view_ticket_need, ticket_id)


def edit_ticket_comment_permission(ticket_id): return RoutePermission(
    edit_ticket_comment_need, ticket_id)


def edit_status_permission(application_id): return RoutePermission(
    edit_status_need, application_id)


def accept_applicant_permission(application_id): return RoutePermission(
    accept_applicant_need, application_id)


def reject_applicant_permission(application_id): return RoutePermission(
    reject_applicant_need, application_id)


def delete_applicant_permission(application_id): return RoutePermission(
    delete_applicant_need, application_id)


def my_applications_permission(user_id): return RoutePermission(
    my_applications_need, user_id)


def view_company_permission(company_id): return RoutePermission(
    view_company_need, company_id)


def access_event_permission(event_id): return RoutePermission(
    access_event_need, event_id)


def view_thread_permission(thread_id): return RoutePermission(
    view_thread_need, thread_id)


class RoutePermission(Permission):
    def __init__(self, func, id):
        need = func(id)
        super(RoutePermission, self).__init__(need)

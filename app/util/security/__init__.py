from collections import namedtuple
from functools import partial

from flask_principal import Permission, RoleNeed

admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
hiring_permission = Permission(RoleNeed('hiring_manager'))


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

edit_status_need = set_need('edit_status')
contact_applicant_need = set_need('contact_applicant')
reject_applicant_need = set_need('reject_applicant')
delete_applicant_need = set_need('delete_applicant')

my_applications_need = set_need('my_applications')

# TODO put into proper functions do not assign lamda expressions
delete_comment_permission = lambda post_id:RoutePermission(delete_comment_need,post_id) 
edit_comment_permission = lambda post_id:RoutePermission(edit_comment_need,post_id)
delete_post_permission = lambda post_id:RoutePermission(delete_post_need,post_id) 
edit_post_permission = lambda post_id:RoutePermission(edit_post_need,post_id)
delete_ticket_permission = lambda ticket_id:RoutePermission(delete_ticket_need,ticket_id) 
delete_ticket_comment_permission = lambda ticket_id:RoutePermission(delete_ticket_comment_need,ticket_id) 
edit_ticket_permission = lambda ticket_id:RoutePermission(edit_ticket_need,ticket_id) 
edit_ticket_comment_permission = lambda ticket_id:RoutePermission(edit_ticket_comment_need,ticket_id) 

edit_status_permission = lambda application_id:RoutePermission(edit_status_need,application_id)
contact_applicant_permission = lambda application_id:RoutePermission(contact_applicant_need,application_id)
reject_applicant_permission = lambda application_id:RoutePermission(reject_applicant_need,application_id)
delete_applicant_permission = lambda application_id:RoutePermission(delete_applicant_need,application_id)

my_applications_permission = lambda user_id:RoutePermission(my_applications_need, user_id)

class RoutePermission(Permission):
    def __init__(self, func, id):
        need = func(id)
        super(RoutePermission, self).__init__(need)
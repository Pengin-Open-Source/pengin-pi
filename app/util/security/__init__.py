from collections import namedtuple
from functools import partial

from flask_principal import Permission, RoleNeed

admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
hiring_permission = Permission(RoleNeed('hiring_manager'))
reviewer_permission = Permission(RoleNeed('reviewer'))

# helper function to help set up needs
def set_need(func_str):
    nt = namedtuple(func_str, ['method', 'value'])
    return partial(nt, func_str)


delete_comment_need = set_need("delete_comment")
edit_comment_need = set_need("edit_comment")
delete_post_need = set_need("delete_post")
edit_post_need = set_need("edit_post")
# creates the delete_ticket_need with the name 'delete_ticket' (no value is set yet - see below)
delete_ticket_need = set_need("delete_ticket")
delete_ticket_comment_need = set_need("delete_ticket_comment")
edit_ticket_need = set_need("edit_ticket_comment")
edit_ticket_comment_need = set_need("edit_ticket")

edit_status_need = set_need('edit_status')
accept_applicant_need = set_need('accept_applicant')
reject_applicant_need = set_need('reject_applicant')
delete_applicant_need = set_need('delete_applicant')
my_application_need = set_need('my_application')

# lambda functions create the value for the need
# TODO put into proper functions do not assign lamda expressions
delete_comment_permission = lambda post_id:RoutePermission(delete_comment_need,post_id) 
edit_comment_permission = lambda post_id:RoutePermission(edit_comment_need,post_id)
delete_post_permission = lambda post_id:RoutePermission(delete_post_need,post_id) 
edit_post_permission = lambda post_id:RoutePermission(edit_post_need,post_id)
delete_ticket_permission = lambda ticket_id:RoutePermission(delete_ticket_need,ticket_id) 

# value will be whatever 'ticket_id' is
# so this permission will be for deleting a particular ticket
delete_ticket_comment_permission = lambda ticket_id:RoutePermission(delete_ticket_comment_need,ticket_id) 

edit_ticket_permission = lambda ticket_id:RoutePermission(edit_ticket_need,ticket_id) 
edit_ticket_comment_permission = lambda ticket_id:RoutePermission(edit_ticket_comment_need,ticket_id) 

edit_status_permission = lambda application_id:RoutePermission(edit_status_need,application_id)
accept_applicant_permission = lambda application_id:RoutePermission(accept_applicant_need,application_id)
reject_applicant_permission = lambda application_id:RoutePermission(reject_applicant_need,application_id)
delete_applicant_permission = lambda application_id:RoutePermission(delete_applicant_need,application_id)
my_application_permission = lambda application_id:RoutePermission(my_application_need,application_id)

class RoutePermission(Permission):
    def __init__(self, func, id):
        need = func(id)
        super(RoutePermission, self).__init__(need)
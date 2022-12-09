from functools import partial
from collections import namedtuple
from flask_principal import Permission, RoleNeed


admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

def set_need(func_str):
    nt = namedtuple(func_str, ['method', 'value'])
    return partial(nt, func_str)

delete_comment_need = set_need("delete_comment") 
edit_comment_need = set_need("edit_comment")
delete_post_need = set_need("delete_post") 
edit_post_need = set_need("edit_post")
delete_ticket_need = set_need("delete_ticket") 
delete_ticket_comment_need = set_need("delete_ticket_comment") 
delete_comment_permission = lambda post_id:RoutePermission(delete_comment_need,post_id) 
edit_comment_permission = lambda post_id:RoutePermission(edit_comment_need,post_id)
delete_post_permission = lambda post_id:RoutePermission(delete_post_need,post_id) 
edit_post_permission = lambda post_id:RoutePermission(edit_post_need,post_id)
delete_ticket_permission = lambda post_id:RoutePermission(delete_ticket_need,post_id) 
delete_ticket_comment_permission = lambda post_id:RoutePermission(delete_ticket_comment_need,post_id) 


class RoutePermission(Permission):
    def __init__(self, func, id):
        need = func(id)
        super(RoutePermission, self).__init__(need)
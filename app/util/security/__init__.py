from functools import partial
from collections import namedtuple
from flask_principal import Permission


PostNeed = namedtuple('forum_post', ['method', 'value'])
PostDelNeed = namedtuple('forum_post', ['method'])
EditPostNeed = partial(PostNeed, 'edit')
DeletePostNeed = partial(PostNeed, 'delete')


class DeletePostPermission(Permission):
    def __init__(self, post_id):
        need = DeletePostNeed(post_id)
        super(DeletePostPermission, self).__init__(need)


class EditPostPermission(Permission):
    def __init__(self, post_id):
        need = EditPostNeed(post_id)
        super(EditPostPermission, self).__init__(need)
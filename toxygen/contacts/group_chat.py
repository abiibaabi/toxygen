from contacts import contact
from contacts.contact_menu import GroupMenuGenerator
import utils.util as util
from groups.group_peer import GroupChatPeer
from wrapper import toxcore_enums_and_consts as constants


class GroupChat(contact.Contact):

    def __init__(self, tox, profile_manager, message_getter, number, name, status_message, widget, tox_id):
        super().__init__(profile_manager, message_getter, number, name, status_message, widget, tox_id)
        self._tox = tox
        self.set_status(constants.TOX_USER_STATUS['NONE'])
        self._peers = []
        self._add_self_to_gc()

    def set_topic(self, topic):
        self._tox.group_set_topic(self._number, topic.encode('utf-8'))
        super().set_status_message(topic)

    def remove_invalid_unsent_files(self):
        pass

    def get_context_menu_generator(self):
        return GroupMenuGenerator(self)

    # -----------------------------------------------------------------------------------------------------------------
    # Peers methods
    # -----------------------------------------------------------------------------------------------------------------

    def get_self_name(self):
        return self._peers[0].name

    def add_peer(self, peer_id):
        peer = GroupChatPeer(peer_id,
                             self._tox.group_peer_get_name(self._number, peer_id),
                             self._tox.group_peer_get_status(self._number, peer_id),
                             self._tox.group_peer_get_role(self._number, peer_id),
                             self._tox.group_peer_get_public_key(self._number, peer_id))
        self._peers.append(peer)

    def get_peer(self, peer_id):
        peers = list(filter(lambda p: p.id == peer_id, self._peers))

        return peers[0]

    # -----------------------------------------------------------------------------------------------------------------
    # Private methods
    # -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _get_default_avatar_path():
        return util.join_path(util.get_images_directory(), 'group.png')

    def _add_self_to_gc(self):
        peer_id = self._tox.group_self_get_peer_id(self._number)
        self.add_peer(peer_id)

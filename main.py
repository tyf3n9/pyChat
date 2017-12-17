from login_controller import *
from channel_list_controller import *
from select_channel_controller import *
from check_messages_controller import *
from send_message_controller import *
from keep_alive_controller import *
from repeated_timer import *
from cleanup import *
from jwt_middleware import *
from refresh_token_controller import *
import sys
from constants import *

db_path = None
if len(sys.argv) > 1:
    db_path = sys.argv[1]
Storage.load(db_path)

server = WebServer()
server.register_mw(JwtMiddleWare)

server.add_route('/login', LoginController, [JwtMiddleWare])
server.add_route('/refreshtoken', RefreshTokenController, [JwtMiddleWare])
server.add_route('/channellist', ChannelListController)
server.add_route('/selectchannel', SelectChannelController)
server.add_route('/sendmessage', SendMessageController)
server.add_route('/checkmessages', CheckMessagesController)
server.add_route('/keepalive', KeepAliveController)


rt = RepeatedTimer(Const.CLEANUP_TIMEOUT, clean_up)
server.start()

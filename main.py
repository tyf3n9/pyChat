from web_server import *
from login_controller import *
from channel_list_controller import *
from select_channel_controller import *
from check_messages_controller import *
from send_message_controller import *
from keep_alive_controller import *
from repeated_timer import *
from cleanup import *


server = WebServer()
server.add_route('/login', LoginController)
server.add_route('/channellist', ChannelListController)
server.add_route('/selectchannel', SelectChannelController)
server.add_route('/sendmessage', SendMessageController)
server.add_route('/checkmessages', CheckMessagesController)
server.add_route('/keepalive', KeepAliveController)


rt = RepeatedTimer(Const.CLEANUP_TIMEOUT, clean_up)
server.start()

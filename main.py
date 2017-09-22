from web_server import *
from login_controller import *
from channel_list_controller import *
from select_channel_controller import *
from check_messages_controller import *
from send_message_controller import *

server = WebServer()
server.add_route('/login', LoginController)
server.add_route('/channellist', ChannelListController)
server.add_route('/selectchannel', SelectChannelController)
server.add_route('/sendmessage', SendMessageController)
server.add_route('/checkmessages', CheckMessagesController)

server.start()

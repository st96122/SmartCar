from cantools.db import load_file as load_dbc_file

can_msg_parser = load_dbc_file('dbc/521.dbc')

print can_msg_parser.messages


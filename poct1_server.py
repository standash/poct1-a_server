#!/usr/bin/env python3

import sys
import socket
import traceback
import conversations

own_sequence_number = 4000

def print_help_message():
    print("\nThis is a simple POCT1-A server that implements \nbasic profile conversation flow for Siemens DCA Vantage.")
    print("The server waits for a connection from DCA, requests patient \ntests and establishes continuos conversation mode.\n")
    print("To run the server, type:\n")
    print("\t./poct1_server.py [server-ip-address] [server-port]\n")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] == "" or sys.argv[2] == "":
        print_help_message()
        sys.exit(0)

    poc_host, poc_port = sys.argv[1], int(sys.argv[2])

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((poc_host, poc_port))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print("Connected by {}".format(addr))

            # perform the basic confersation flow and establish communication with the device
            latest_timestamp = conversations.basic_conversation_flow(conn)
            
            # update operator list
            if latest_timestamp:
                latest_timestamp = conversations.update_operators_list_flow(latest_timestamp, "Bruce Wayne", "gotham", conn)
            else:
                raise Exception("ERROR: previous conversation flow did not return the latest timestamp!")

            # send a remote command
            if latest_timestamp:
                latest_timestamp = conversations.send_remote_command_flow(latest_timestamp, "FORCE_HIGH", conn)
            else:
                raise Exception("ERROR: previous conversation flow did not return the latest timestamp!")
            

    except Exception as e:
        print("ERROR: {}".format(e))
        track = traceback.format_exc()
        print(track)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        sock.close()

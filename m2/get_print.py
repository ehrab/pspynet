#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Demonstrate using SSH via paramiko to get information from
the network and print it to the screen.
"""

import time
import paramiko


def send_cmd(conn, command):
    """
    Given an open connection and a command, issue the command and wait
    500 ms for the command to be processed.
    """
    conn.send(command + "\n")
    time.sleep(0.5)


def get_output(conn):
    """
    Given an open connection, read all the data from the buffer and
    decode the byte string as UTF-8.
    """
    return conn.recv(65535).decode("utf-8")


def main():
    """
    Execution starts here.
    """

    host_dict = {
        "csr": "show running-config | section vrf_definition",
        "xrv": "show running-config vrf",
    }
    for hostname, vrf_cmd in host_dict.items():
        conn_params = paramiko.SSHClient()
        conn_params.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn_params.connect(
            hostname=hostname,
            port=22,
            username="pyuser",
            password="pypass",
            look_for_keys=False,
            allow_agent=False,
        )

        # Get an interactive shell and wait a bit for the prompt to appear
        conn = conn_params.invoke_shell()
        time.sleep(0.5)

        print(f"Logged into {get_output(conn).strip()} successfully")

        # Iterate over the list of commands, sending each one in series
        # The final command in the list is the OS-specific VRF "show" command
        commands = [
            "terminal length 0",
            "show version | include Software,",
            vrf_cmd,
        ]
        for command in commands:
            send_cmd(conn, command)
            print(get_output(conn))


if __name__ == "__main__":
    main()
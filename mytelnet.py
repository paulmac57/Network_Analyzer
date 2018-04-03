import telnetlib

if __name__ == "__main__":

    ip = "192.168.0.118"
    username = ""
    password = "cisco"

    TELNET_PORT = 23
    TELNET_TIMEOUT = 6
    READ_TIMEOUT = 6

    remote_conn = telnetlib.Telnet(ip, TELNET_PORT, TELNET_TIMEOUT)

    print (dir(remote_conn))
    print (help(remote_conn.read_until))
    output = remote_conn.read_until(b"sername:", READ_TIMEOUT)
    remote_conn.write(username.encode() + b"\n")

    output = remote_conn.read_until(b"ssword:", READ_TIMEOUT)
    remote_conn.write(password.encode() + b"\n")

    time.sleep(delay)

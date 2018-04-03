import telnetlib
import time

TELNET_PORT = 23
TELNET_TIMEOUT = 6
READ_TIMEOUT = 6

def disable_paging(remote_conn, command="terminal length 0\n", delay=1):
    '''
    Disable router paging i.e. --More--
    Returns the output buffer
    '''

    remote_conn.write(command.encode())
    time.sleep(delay)
    return remote_conn.read_very_eager().decode()

def show_version(remote_conn, command="\nshow version\n", delay=1):
    '''
    gets all the device information
    Returns the output buffer'
    '''
    remote_conn.write(command.encode())    
    time.sleep(delay)
    return remote_conn.read_very_eager().decode()

def show_cdp_neighbors(remote_conn, command="\nshow cdp neighbor\n", delay=1):
    '''
    gets all the device information
    Returns the output buffer'
    '''
    remote_conn.write(command.encode())    
    time.sleep(delay)
    return remote_conn.read_very_eager().decode()

def set_hostname(remote_conn, command, delay=1):
    '''
    sets the hostname
    
    '''
######## ENABLE_PASSWORD SHOULD TO BE SET WITHIN INTERFACE (this needs more work)
    enable_password="cisco"

    remote_conn.write(b"\nenable\n")
    time.sleep(delay)

    output = remote_conn.read_until(b"ssword:", READ_TIMEOUT)
    remote_conn.write(enable_password.encode() + b"\n")
    time.sleep(delay)
    
    output = remote_conn.read_very_eager()
    time.sleep(delay)
    remote_conn.write(b"\nconf t\n")
    output = remote_conn.read_very_eager()

    time.sleep(delay)
    remote_conn.write(command.encode()+ b"\n")
    time.sleep(delay)
    output = remote_conn.read_very_eager()

    time.sleep(delay)
    return remote_conn.read_very_eager().decode()

def establish_connection(ip, username='', password='', delay=1):
    '''
    Establish the telnet connection and login
    '''

    remote_conn = telnetlib.Telnet(ip, TELNET_PORT, TELNET_TIMEOUT)
    remote_conn.write(b"\n")
    
    output = remote_conn.read_until(b"ssword:", READ_TIMEOUT)
    print (output)
    remote_conn.write(password.encode() + b"\n")

    time.sleep(delay)
    output = remote_conn.read_very_eager()
    print (output)
    return remote_conn


def main():
    '''
    '''
    ip = '192.168.0.118'
    username = ''
    password = 'cisco'

    remote_conn = establish_connection(ip, username, password)

    output = disable_paging(remote_conn)

    remote_conn.write(b"\n")
    remote_conn.write("show version".encode() + b"\n")

    time.sleep(1)
    output = remote_conn.read_very_eager()
    print (output)

    remote_conn.close()


if __name__ == "__main__":
    main()

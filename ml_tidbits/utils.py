from paramiko import SSHClient  # https://pypi.org/project/paramiko/
from scp import SCPClient   # https://pypi.org/project/scp/


def get_ssh_connection(host, username, password):
    """ Creates & returns an ssh connection client programatically.

    :param host: (str) host of machine to connect to
    :param username: (str) username to use for ssh credentials
    :param password: (str) password to use for ssh credentials
    :return: ssh client object
    """

    try:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(host, username=username, password=password)
        return ssh
    except Exception as e:
        print(e)
        return False


def scp_files(host, username, password, remote_dir, local_dir, direction="from"):
    """ SCPs files either from a given remote dir to a local one or vice versa.

    :param host: (str) host of machine to connect to
    :param username: (str) username to use for ssh credentials
    :param password: (str) password to use for ssh credentials
    :remote_dir: (Path) remote directory to/from which to copy files
    :local_dir: (Path) local directory to/from which to copy files
    :direction: (str) either 'from' or 'to' indicating which way we are copying
    :return True if successful, False otherwise.
    """

    try:
        ssh_client = get_ssh_connection(host, username, password)
        with SCPClient(ssh_client.get_transport()) as scp:
            if direction == "from":
                scp.get(remote_dir, local_dir)
            elif direction == "to":
                scp.put(local_dir, remote_path=remote_dir)
            else:
                print("you don't know where you're going...")
                return False
        return True
    except Exception as e:
        print(e)
        return False

import subprocess
import optparse
import re


def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--interface", dest="interface", help="interface to change")
    parse_object.add_option("-m", "--mac", dest="mac_address", help="new MAC address")

    return parse_object.parse_args()


def change_mac_address(user_interface, user_mac_address):
    subprocess.call(["ifconfig", user_interface, "down"])
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac_address])
    subprocess.call(["ifconfig", user_interface, "up"])


def control_new_mac(interface):
    ifconfig = str(subprocess.check_output(["ifconfig", interface]), 'ascii')
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig)

    if new_mac:
        return new_mac.group(0)
    else:
        return None


print("MyMacChanger started!")

(user_input, arguments) = get_user_input()
old_mac_config = str(subprocess.check_output(["ifconfig", user_input.interface]), 'ascii')
old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", old_mac_config).group(0)
change_mac_address(user_input.interface, user_input.mac_address)
finalized_mac = control_new_mac(user_input.interface)

if finalized_mac == user_input.mac_address:
    print("Success")
    print(f"[-] Your old MAC Address: {old_mac}")
    print(f"[+] Your new MAC Address: {finalized_mac}")
else:
    print("Error!!!")

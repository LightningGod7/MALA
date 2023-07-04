
import os

__name__ = "test scanner"
__description__ = "test"


def wpscan_enumeration(target, disable_tls_checks=False, enumeration_flag=['a', 'p', 'v', 't']):
    """Perform WordPress enumeration using wpscan"""
    valid_flags = ['a', 'p', 'v', 't', 'u', 'e', 'd', 'c', 'm', 'i', 'r', 'f']

    # Validate each element in enumeration_flag
    valid_enumeration_flags = [flag for flag in enumeration_flag if flag in valid_flags]

    if not valid_enumeration_flags:
        print("No valid enumeration flags specified.")
        return

    command = f"wpscan --url {target}"
    if disable_tls_checks:
        command += " --disable-tls-checks"

    command += f" --enumerate {''.join(valid_enumeration_flags)}"
    os.system(command)
    os.system(command)

def wpscan_brute_force(target, username, password_list, disable_tls_checks=False):
    """Perform WordPress login brute force using wpscan"""
    command = f"wpscan --url {target} --username {username} --passwords {password_list}"
    if disable_tls_checks:
        command += " --disable-tls-checks"
    os.system(command)
#!/usr/bin/env python3
"""
WhatsApp Profile Checker v1.0.1
Author: Your Name <your.email@example.com>
License: MIT

A command-line tool to check if a phone number is associated with a WhatsApp account.

Usage:
  whatsapp_checker.py [options] <country_code> <phone_number>
  whatsapp_checker.py (-h | --help)
  whatsapp_checker.py --version

Options:
  -h --help       Show this help message
  --version       Show version information
  -v --verbose    Show detailed output

Example:
  whatsapp_checker.py 91 9876543210
  whatsapp_checker.py -v 44 2079460018
"""

import sys
import requests
from docopt import docopt

VERSION = "1.0.1"

def validate_input(country_code: str, phone_number: str) -> bool:
    """Validate country code and phone number formats"""
    if not country_code.isdigit():
        print(f"❌ Invalid country code: {country_code} (must be numeric)", file=sys.stderr)
        return False
    if len(country_code) < 1 or len(country_code) > 4:
        print(f"❌ Invalid country code length: {country_code} (1-4 digits)", file=sys.stderr)
        return False
    if not phone_number.isdigit():
        print(f"❌ Invalid phone number: {phone_number} (must be numeric)", file=sys.stderr)
        return False
    if len(phone_number) < 5 or len(phone_number) > 15:
        print(f"❌ Invalid phone number length: {phone_number} (5-15 digits)", file=sys.stderr)
        return False
    return True

def check_whatsapp_account(country_code: str, phone_number: str, verbose: bool = False) -> None:
    """Check if WhatsApp account exists and display results"""
    full_number = f"{country_code}{phone_number}"
    
    try:
        response = requests.get(
            f"https://wa.me/{full_number}",
            timeout=10,
            allow_redirects=False
        )
        
        if verbose:
            print(f"🔍 Checking: +{full_number}")
            print(f"HTTP Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            print(f"✓ ACTIVE: WhatsApp account found for +{full_number}")
        elif response.status_code == 302:
            print(f"✗ INACTIVE: No WhatsApp account for +{full_number}")
        else:
            print(f"⚠️ UNEXPECTED RESPONSE: HTTP {response.status_code} for +{full_number}")

    except requests.exceptions.Timeout:
        print("⚠️ Request timed out. Check your internet connection or try again later.")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network error occurred: {str(e)}")

def main() -> None:
    """Main entry point for the CLI tool"""
    arguments = docopt(__doc__, version=VERSION)
    
    country_code = arguments['<country_code>']
    phone_number = arguments['<phone_number>']
    verbose = arguments['--verbose']
    
    if validate_input(country_code, phone_number):
        check_whatsapp_account(country_code, phone_number, verbose)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
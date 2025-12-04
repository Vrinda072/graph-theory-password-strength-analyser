# cli.py
import argparse
from .password_analyzer import PasswordAnalyzer
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('password', help='password to analyze')
    args = parser.parse_args()
    pa = PasswordAnalyzer()
    out = pa.analyze(args.password)
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()

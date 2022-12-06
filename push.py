
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Copy the SOURCE to the destination", type=str, required=False)
    parser.add_argument("destination", help="Copy the source to the DESTINATION", type=str, required=False)
    parser.add_argument("-u", "--user", help="User for login", type=str, default="fabian", required=False)
    parser.add_argument("-ip", "--ip", help="The IP for the SCP", type=str, default="192.168.240.200", required=False)
    args = parser.parse_args()
    os.system(f"scp {args.source if args.source != '' else 'output/*.jpg'} {args.user}@{args.ip}:{args.destination if args.destination != '' else '/share/Henrik/output/'}")

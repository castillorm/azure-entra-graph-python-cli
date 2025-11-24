"""
graph.py

Simple CLI for Azure AD user management via Microsoft Graph.
Reads configuration from config.json.
"""

import argparse
import sys
from typing import Any

from graph_client import list_users, search_users, create_user, delete_user

def print_user(user: dict[str, Any]) -> None:
    display_name = user.get("displayName", "")
    upn = user.get("userPrincipalName", "")
    user_id = user.get("id", "")
    print(f"- {display_name} | {upn} | id={user_id}")

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Microsoft Graph CLI for Azure AD users")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-users", nargs="?", const=10, type=int, help="List first N users")
    group.add_argument("--search", type=str, help="Search users by prefix")
    group.add_argument("--create-user", action="store_true", help="Create a new user")
    group.add_argument("--delete-user", type=str, help="Delete a user by ID or UPN")

    parser.add_argument("--display-name", type=str)
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)

    args = parser.parse_args(argv)

    if args.list_users is not None:
        users = list_users(top=args.list_users)
        for u in users:
            print_user(u)
        return 0

    if args.search:
        users = search_users(args.search)
        for u in users:
            print_user(u)
        return 0

    if args.create_user:
        if not (args.display_name and args.username and args.password):
            print("ERROR: --create-user requires --display-name, --username, --password", file=sys.stderr)
            return 1

        user = create_user(args.display_name, args.username, args.password)
        print("User created:")
        print_user(user)
        return 0

    if args.delete_user:
        delete_user(args.delete_user)
        print("User deleted.")
        return 0

    parser.print_help()
    return 1

if __name__ == "__main__":
    raise SystemExit(main())

#! venv/bin/python
import os
import dotenv
from imaplib import IMAP4_SSL
import logging
import math

log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='log', level=logging.DEBUG, format=log_format)
logging.getLogger().addHandler(logging.StreamHandler())

dotenv.load_dotenv()
host = os.environ.get("HOST", "localhost")
port = os.environ.get("PORT", "993")
user = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
pattern = os.environ.get("PATTERN")
target_mailboxes = os.environ.get("MAILBOXES", "INBOX")
output_loc = os.environ.get("OUTPUT_LOC", "./output")


def connect_to_mailbox():
    M = IMAP4_SSL(host, port)
    M.login(user, password)
    logging.info("Successfully logged in!")
    return M


def get_n_for_mailbox(M, mname, pattern):
    logging.info(f"connecting to mailbox {mname}...")
    res, _ = M.select(mname)
    logging.info(res)
    res, mails = M.search(None, f'(SUBJECT "{pattern}")')
    mails = mails[0].decode()
    n = len(mails.split())
    logging.info(f"{n} emails matching pattern found")
    return n


def count_for_all_inboxes(M):
    mailboxes = target_mailboxes.split(",")
    mailboxes = map(lambda x: f'"{x}"', mailboxes)

    logging.info(f'will search for pattern "{pattern}"')
    n = sum(map(lambda x: get_n_for_mailbox(M, x, pattern), mailboxes))
    logging.info(f'found {n} emails in total')
    return n


def main():

    if os.path.isfile(output_loc):
        with open(output_loc, "r") as f:
            old_n = int(f.read())
    else:
        old_n = 0

    M = connect_to_mailbox()
    n = count_for_all_inboxes(M)

    if old_n > n:
        logging.error(
            f"Number of submissions shouldn't go down({old_n} to {n}). Aborting!"
        )
        logging.shutdown()
        return 1

    logging.info("writing result to file")

    with open(output_loc, "w") as f:
        f.write(str(n))

    logging.info("all done!")
    logging.shutdown()


if __name__ == "__main__":
    main()

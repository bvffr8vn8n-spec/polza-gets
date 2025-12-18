import sys
import re
import dns.resolver

STATUS_VALID = "домен валиден"
STATUS_NO_DOMAIN = "домен отсутствует"
STATUS_BAD_MX = "MX-записи отсутствуют или некорректны"

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

resolver = dns.resolver.Resolver(configure=True)
resolver.nameservers = ["1.1.1.1", "8.8.8.8"]
resolver.timeout = 2
resolver.lifetime = 5


def load_emails(args: list[str]) -> list[str]:
    if len(args) < 2:
        print("Usage:\n  python mx_check.py emails.txt\n  python mx_check.py a@b.com c@d.com")
        sys.exit(1)

    first = args[1].strip()

    if first.lower().endswith(".txt"):
        with open(first, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    return [x.strip() for x in args[1:] if x.strip()]


def check_mx(email: str) -> str:
    if not EMAIL_REGEX.match(email):
        return STATUS_BAD_MX

    domain = email.split("@", 1)[1].strip().lower()

    try:
        answers = resolver.resolve(domain, "MX")
        mx_hosts = [
            str(r.exchange).strip().rstrip(".")
            for r in answers
            if str(r.exchange).strip()
        ]
        return STATUS_VALID if mx_hosts else STATUS_BAD_MX

    except dns.resolver.NXDOMAIN:
        return STATUS_NO_DOMAIN
    except (dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout):
        return STATUS_BAD_MX
    except Exception:
        return STATUS_BAD_MX


def main() -> None:
    emails = load_emails(sys.argv)
    for email in emails:
        print(f"{email}\t{check_mx(email)}")


if __name__ == "__main__":
    main()

import sys
from app.auto_renewer import AutoRenewer


def main():
    browser = ''
    if len(sys.argv) == 2:
        browser = sys.argv[1]

    auto_renewer = AutoRenewer(browser)
    auto_renewer.run()


if __name__ == '__main__':
    main()

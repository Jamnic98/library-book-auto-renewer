 #!/usr/bin/env python3
from app.auto_renewer import AutoRenewer


def main():
    auto_renewer = AutoRenewer(browser_name='chromium')
    auto_renewer.run()


if __name__ == '__main__':
    main()

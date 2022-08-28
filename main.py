from app.auto_renewer import AutoRenewer


def main():
    auto_renewer = AutoRenewer(browser_name='Chrome')
    auto_renewer.run()


if __name__ == '__main__':
    main()

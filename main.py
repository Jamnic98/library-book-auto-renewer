from app.auto_renewer import AutoRenewer


async def main():
    auto_renewer = AutoRenewer()
    await auto_renewer.run()

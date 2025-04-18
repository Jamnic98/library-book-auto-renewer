import asyncio
from app.auto_renewer import AutoRenewer
from app.utlis.settings import config

async def main():
    auto_renewer = AutoRenewer(config)
    await auto_renewer.run()

if __name__ == "__main__":
    asyncio.run(main())

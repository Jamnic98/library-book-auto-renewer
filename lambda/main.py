import asyncio
from app.auto_renewer import AutoRenewer

async def main():
    auto_renewer = AutoRenewer()
    await auto_renewer.run()

# Lambda-compatible handler
def lambda_handler(_event, _context):
    return asyncio.run(main())

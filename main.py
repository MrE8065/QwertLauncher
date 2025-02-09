import asyncio
from minecraft_launcher.menu import check

async def inicio():
    await check()
    
if __name__ == '__main__':
    asyncio.run(inicio())
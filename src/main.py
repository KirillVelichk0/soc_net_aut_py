import logging
from AuthServer import serve
import asyncio

if __name__ == '__main__':                                                      
    logging.basicConfig(level=logging.INFO)                                     
    asyncio.run(serve())
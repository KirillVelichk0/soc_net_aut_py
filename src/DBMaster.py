import asyncio
import asyncpg
import json
import ssl
from pathlib import Path

class DbMaster:
    def __init__(self):
        #cred data parsing
        base_dir = Path(__file__).parent.parent.resolve()
        cur_path = base_dir.joinpath('configs', 'db_auth_config.json')
        with open(cur_path) as json_config:
            pg_cred_data_json = json.load(json_config)
        self.user = pg_cred_data_json['user']
        self.db_name = pg_cred_data_json['db_name']
        self.host = pg_cred_data_json['host']
        pass_path = pg_cred_data_json['pathToPassword']
        with open(pass_path) as json_config:
            pg_cred_data_json = json.load(json_config)
        self.password = pg_cred_data_json['password']
        

    async def Connect(self):
        self.connection = await asyncpg.connect(user=self.user, database=self.db_name,\
                                                 host=self.host, password=self.password, ssl='prefer')



    async def TryRegistrate(self, email:str, password: str, salt: str, random_token: str) -> int:
        row = await self.connection.fetchrow('SELECT try_register as temp_uid\
                                  from try_register($1, $2, $3, $4)', email, password, salt, random_token)
        temp_uid = row['temp_uid']
        return temp_uid
        

    async def TryVerifyRegistration(self, uid: int, random_data: str) -> str:
        row = await self.connection.fetchrow('SELECT try_verify as verify_message\
                                             from try_verify($1, $2)', uid, random_data)
        return row['verify_message']
        
        
    async def InsertJWTToken(self, uid: int, max_time: int, open_key: str):
        row = await self.connection.fetchrow('SELECT insert_token as token_id\
                                       from insert_token($1, $2, $3)', uid, max_time, open_key)
        return row['token_id']


    async def GetJwtFromTokenId(self, token_id: int):
        row = await self.connection.fetchrow('SELECT open_key from users_tokens_info WHERE tid = $1', token_id)
        if row is None:
            return None
        return row['open_key']
    
    async def GetUserId_HashedPassAndSalt(self, email: str):
        row = await self.connection.fetchrow('SELECT uid, pass_h, salt from users_main_table WHERE email = $1', email)
        if row is None:
            return None
        return (row['uid'], row['pass_h'], row['salt'])


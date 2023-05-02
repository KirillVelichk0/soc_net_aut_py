import sys, os
lib_path = os.path.abspath(os.path.join(__file__, '..', 'proto_gen'))
sys.path.append(lib_path)

import proto_gen.AuthServ_pb2 as AuthServ, proto_gen.AuthServ_pb2_grpc as AuthServGrpc
import AuthLib, DBMaster, emailSender
import json
import grpc
import logging
from pathlib import Path
class Soc_net_server(AuthServGrpc.AuthAndRegistService):
    def __init__(self, connected_db_master):
        self.auth_master = AuthLib.AuthMaster(DBMaster= connected_db_master, EmailServer=emailSender.MailServer())
        self.init_str = 'localhost:8091'
        #ssl cred init
        base_dir = Path(__file__).parent.parent.resolve()
        cur_path = base_dir.joinpath('configs', 'ssl_config.json')
        with open(cur_path) as json_config:
            path_to_cred_json = json.load(json_config)
        key_cred = path_to_cred_json['CredsKey']
        pem_cred = path_to_cred_json["CredsPem"]
        with open(key_cred, 'rb') as f:
            private_key = f.read()
        with open(pem_cred, 'rb') as f:
            certificate_chain = f.read()
        print("config parsed")
        ssl_data = grpc.ssl_server_credentials(((private_key, certificate_chain), ), require_client_auth=False)
        self.credential = ssl_data
        print("creds getted")
        
    async def GetSecureChannel(self):
        return await grpc.aio.secure_channel(self.channel_data, self.credential)
    
    def GetCreds(self):
        return self.credential
    
    async def TryRegistr(self, request, context):
        isOk = await self.auth_master.TryRegistrate(request.email, request.password)
        if isOk:
            answer = "На вашу почту отправлено письмо с ссылкой для подтверждения регистрации"
        else:
            answer = 'Аккаунт с данной почтой уже существует. Если эта ваша почта, но вы не регистрировались\
                , обратитесь в службу поддержки'
            
        return AuthServ.RegistrationResult(answer=answer, isOk=isOk)
    

    async def TryVerifRegistr(self, request, context):
        resp_message = await self.auth_master.TryVerify(request.randomDataToken)
        return AuthServ.RegistrationVerificationResult(resp_message)
    
    async def Authenticate(self, request, context):
        auth_res = await self.auth_master.LoginUsingJWT(request.jwtToken)
        if auth_res is None:
            response = AuthServ.AuthResult(-1, '')
        else:
            next_jwt, user_id = auth_res
            response = AuthServ.AuthResult(user_id, next_jwt)
        return response
    
    async def AuthFromPassword(self, request, context):
        auth_result = await self.auth_master.LoginUsingPassword(request.email, request.password)
        if auth_result is None:
            response = AuthServ.PasswordAuthResult('', -1)
        else:
            jwt, uid = auth_result
            response = AuthServ.PasswordAuthResult(jwt, uid)
        return response 
    

async def serve():
    server = grpc.aio.server()
    db_master = DBMaster.DbMaster()
    await db_master.Connect()
    server_instanse = Soc_net_server(db_master)
    AuthServGrpc.add_AuthAndRegistServiceServicer_to_server(server_instanse, server)
    listen_addr = '0.0.0.0:8091'
    server.add_secure_port(listen_addr, server_instanse.GetCreds())
    logging.info("Starting server on %s", listen_addr)
    await server.start()                                                        
    await server.wait_for_termination() 



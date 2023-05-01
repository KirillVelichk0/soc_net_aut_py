import proto_gen.AuthServ_pb2 as AuthServ, proto_gen.AuthServ_pb2_grpc as AuthServGrpc
import AuthLib, DBMaster, emailSender
import json
import grpc
from pathlib import Path
class Soc_net_server(AuthServGrpc.AuthAndRegistService):
    def __init__(self):
        self.auth_master = AuthLib.AuthMaster(DBMaster=DBMaster.DbMaster(), EmailServer=emailSender.MailServer())
        self.init_str = 'localhost:8091'
        #ssl cred init
        base_dir = Path(__file__).parent.parent.resolve()
        cur_path = base_dir.joinpath('configs', 'ssl_config.json')
        with open(cur_path) as json_config:
            path_to_cred_json = json.load(json_config)
        path_to_cred = path_to_cred_json['PathToCreds']
        print("config parsed")
        self.credential = grpc.ssl_channel_credentials(open(path_to_cred, 'rb').read())
        print("creds getted")
        
    async def GetSecureChannel(self):
        return await grpc.aio.secure_channel(self.channel_data, self.credential)
    
    async def TryRegistr(self, request, context):
        isOk = await self.auth_master.TryRegistrate(request.email, request.password)
        if isOk:
            answer = "На вашу почту отправлено письмо с ссылкой для подтверждения регистрации"
        else:
            answer = 'Аккаунт с данной почтой уже существует. Если эта ваша почта, но вы не регистрировались\
                , обратитесь в службу поддержки'
        return AuthServ.RegistrationResult(answer=answer, isOk=isOk)

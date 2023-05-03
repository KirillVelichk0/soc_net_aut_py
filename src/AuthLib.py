import CryptLib
import DBMaster
import emailSender
class AuthMaster:
    def __init__(self, EmailServer: emailSender.MailServer, DBMaster : DBMaster.DbMaster):
        self.DBMaster = DBMaster
        self.EmailServer = EmailServer
        self.CryptInstanse = CryptLib.CryptMaster()
    async def TryRegistrate(self, email: str, password:str) -> bool:
        (hashed_b64, salt_b64) = self.CryptInstanse.GetHashedAndSaltInUrl(password)
        token_data = self.CryptInstanse.GenerateRandomVerificationTokenData()
        uid = await self.DBMaster.TryRegistrate(email, hashed_b64.decode(), salt_b64.decode(), token_data)
        if uid == -1:
            return False
        verification_token = self.CryptInstanse.ConfigureVerificationToken(uid, token_data)
        try:
            self.EmailServer.TrySendToEmail(email, verification_token)
        except:
            return False
        return True

    async def TryVerify(self, verify_token: str) -> str:
        parsed_token = self.CryptInstanse.TryParseRandomVerificationToken(verify_token)
        if parsed_token is None:
            return 'Uncorrect token format'
        else:
            return await self.DBMaster.TryVerifyRegistration(parsed_token[0], parsed_token[1])
        
    async def LoginUsingPassword(self, email: str, password: str):
        search_result = await self.DBMaster.GetUserId_HashedPassAndSalt(email)
        if search_result is None:
            return None
        else:
            uid, pass_h_b64, salt_b64 = search_result
        isEq = self.CryptInstanse.ComparePasswords(password_from_user=password,\
                                                    hashed_b64_password=pass_h_b64, salt_b64=salt_b64)
        if isEq:
            return await self.CryptInstanse.CreateJWTToken(self.DBMaster.InsertJWTToken, uid), uid
        else:
            return None
        
    async def LoginUsingJWT(self, jwt: str):
        result = await self.CryptInstanse.VerifyJWTToken(self.DBMaster.GetJwtFromTokenId, jwt)
        if result[0] == CryptLib.JWTState.BadOld or CryptLib.JWTState.DontEq:
            return None
        else:
            state, uid = result
            if state is CryptLib.JWTState.GoodOld:
                jwt = await self.CryptInstanse.CreateJWTToken(self.DBMaster.InsertJWTToken, uid)
            return jwt, uid
        


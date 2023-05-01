from base64 import urlsafe_b64decode, urlsafe_b64encode
import scrypt, secrets
import time
from Crypto.PublicKey import RSA
from enum import Enum
import jwt, re

class JWTState(Enum):
    Ok =0
    DontEq = 1
    GoodOld = 2
    BadOld = 3



class CryptMaster:
    GoodHoursCount = 720
    LimForNewGenInSeconds = 360 * 3600
    #Hash password in scrypt using random salt and encode results in base64_url
    def HashAndGetUrlWithSalt(password: str, salt: str):
        return urlsafe_b64encode(scrypt.hash(password, salt, 16384, 8, 1, 32))
    

    def GetHashedAndSaltInUrl(password: str):
        salt = secrets.token_bytes(32)
        hashed_pass = scrypt.hash(password, salt, 16384, 8, 1, 32)
        salt = urlsafe_b64encode(salt)
        hashed_pass = urlsafe_b64encode(hashed_pass)
        return (hashed_pass, salt)
    
    def CheckBase64ToFormat(b64_data: str) -> bool:
        match = re.search('^[A-Za-z0-9_-]+$', b64_data)
        if match:
            return match[0] == b64_data
        else:
            return False


    def ComparePasswords(self, password_from_user: str, hashed_b64_password: str, salt_b64: str) -> bool:
        try:
            salt = urlsafe_b64decode(salt_b64)
            url_from_user = self.HashAndGetUrlWithSalt(password_from_user, salt)
            return url_from_user == hashed_b64_password
        except:
             return False

    def GenerateRsaKeys():
        rsaKey = RSA.generate(2048)
        return (rsaKey, rsaKey.public_key())
    
    def GenerateRandomVerificationTokenData():
        randomData = secrets.token_bytes(32)
        randomData = urlsafe_b64encode(randomData).decode()
        return randomData
    
    def ConfigureVerificationToken(uid:int, token_data:str):
        return str(uid) + '.' + token_data
    
    def TryParseRandomVerificationToken(token: str):
        data = token.split('.', 1)
        try:
            uid = int(data[0])
            random_token = data[1]
            return (uid, random_token)
        except:
            return None

    async def CreateJWTToken(self, registrator, userId: int):
        cur_unix_time = int(time.time())
        unix_time_lifetime = cur_unix_time + self.GoodHoursCount * 60 * 60
        private_key, public_key = self.GenerateRsaKeys()
        public_key_str = public_key.export_key().decode()
        token_id = await registrator(userId, public_key_str, unix_time_lifetime)
        token_data = {"userId": userId, "exp": unix_time_lifetime}
        token_header = {"tokenId": token_id}
        encoded_jwt = jwt.encode(token_data, private_key.export_key(), algorithm="RS256", headers=token_header)
        return encoded_jwt
    
    async def VerifyJWTToken(self, openKeyGetter, token: str):
        try:
            cur_unix_time = int(time.time())
            header = jwt.get_unverified_header(token)
            tokenId = header['tokenId']
            openKey = await openKeyGetter(tokenId)
            if openKey is None:
                raise Exception()
            token_data = jwt.decode(token, openKey, algorithms="RS256")
            token_data = (token_data["userId"], token_data["exp"])
            state = JWTState.Ok
            if token_data[1] < cur_unix_time:
                state = JWTState.BadOld
            elif cur_unix_time > token_data[1] - self.LimForNewGenInSeconds:
                state = JWTState.GoodOld
            return (state, token_data[0], token_data[1])
        except:
            return JWTState.DontEq, None, None

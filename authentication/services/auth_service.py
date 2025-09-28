from repositories.token_repository import TokenRepository
from repositories.user_repository import UserRepository
import utils as auth_utils
from schemas.user_schema import RegisterRequest, TokenResponse
from settings import settings

class AuthService:
    def __init__(self, user_repo: UserRepository, token_repo: TokenRepository):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def register(self, register_request: RegisterRequest) -> TokenResponse:
        """Register a new user"""
        try:
            # print(f"DEBUG: Registering user: {register_request.email}")
            # print(f"DEBUG: Password length: {len(register_request.password)}")
            # print(f"DEBUG: Password: {register_request.password}")
            # print(f"DEBUG: Full name: {register_request.full_name}")
            # print(f"DEBUG: Avatar URL: {register_request.avatar_url}")

            # Check if user already exists
            if self.user_repo.user_exists_by_email(register_request.email):
                raise Exception("User with this email already exists")
            
            # Prepare user data
            user_data = register_request.model_dump()
            # print(f"DEBUG: Original password length: {len(user_data['password'])}")
            
            # Hash password
            user_data['password'] = auth_utils.hash_password(user_data['password'])
            # print(f"DEBUG: Password hashed successfully")
            
            # Create user
            created_user = self.user_repo.create_user(user_data)
            # print(f"DEBUG: User created with ID: {created_user['id']}")
            
            # Generate tokens
            tokens = self._generate_tokens(created_user['id'])
            print(f"DEBUG: Tokens generated successfully")
            
            return tokens
            
        except Exception as e:
            print(f"DEBUG: Registration error: {str(e)}")
            raise e

    def login(self, email: str, password: str) -> TokenResponse:
        """Authenticate user and return tokens"""
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise Exception("Invalid email or password")
        
        # # Check if user is active
        # if not user.get('is_active', True):
        #     raise Exception("Account is deactivated")
            
        # Verify password
        if not auth_utils.verify_password(password, user["password"]):
            raise Exception("Invalid email or password")
        
        # Generate tokens
        return self._generate_tokens(user['id'])
    
    def decode_token(self, token: str):
        """Decode JWT token"""
        return auth_utils.decode_token(token)

    def refresh(self, user_id: str, refresh_token: str) -> TokenResponse:
        """Refresh access token"""
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")
            
        stored = self.token_repo.get_refresh_token(user_id)
        if not stored or stored["token"] != refresh_token:
            raise Exception("Invalid refresh token")
            
        # Verify token is still valid
        try:
            auth_utils.decode_token(refresh_token)
        except:
            raise Exception("Refresh token expired")
        
        # Generate new tokens
        return self._generate_tokens(user['id'])

    def logout(self, user_id: str):
        """Logout user by revoking refresh token"""
        self.token_repo.revoke_refresh_token(user_id)
        return {"message": "Logged out successfully"}

    def _generate_tokens(self, user_id: str) -> TokenResponse:
        """Generate access and refresh tokens"""
        try:
            print(f"DEBUG: Generating tokens for user: {user_id}")
            access_token = auth_utils.create_access_token({"sub": user_id})
            refresh_token = auth_utils.create_refresh_token({"sub": user_id})
            print(f"DEBUG: Tokens created, access_token length: {len(access_token)}")
            
            # Try to store refresh token, but don't fail if Redis is down
            try:
                user = self.user_repo.get_user_by_id(user_id)
                self.token_repo.save_refresh_token(user, refresh_token)
                print(f"DEBUG: Refresh token saved to Redis")
            except Exception as redis_error:
                print(f"DEBUG: Redis error (continuing anyway): {redis_error}")
                # Continue without Redis - just return tokens
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        except Exception as e:
            print(f"DEBUG: Token generation error: {str(e)}")
            raise e
            
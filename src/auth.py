import hashlib

class AuthManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password):
        """Регистрация нового пользователя"""
        if len(password) < 4:
            return False, "Пароль должен содержать минимум 4 символа"
        
        password_hash = self.hash_password(password)
        return self.db.create_user(username, password_hash)
    
    def login_user(self, username, password):
        """Аутентификация пользователя"""
        user = self.db.get_user(username)
        if not user:
            return False, "Пользователь не найден", None
        
        password_hash = self.hash_password(password)
        if user['password_hash'] == password_hash:
            return True, "Вход выполнен успешно", user
        else:
            return False, "Неверный пароль", None
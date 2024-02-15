from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from flask import request

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession

class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """Creates and stores a new instance of User session"""
        if user_id is None:
            return None

        # Call the parent class's method to generate the session ID
        session_id = super().create_session(user_id)

        # Create a new UserSession instance
        user_session = UserSession(user_id=user_id, session_id=session_id)

        # Save the UserSession instance to the database
        user_session.save()

        # Return the generated session ID
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves user_id based on session_id"""
        if session_id is None:
            return None

        user_session = UserSession.get(session_id)
        
        # Check if the user session exists
        if user_session is None:
            return None
        
        # Retrieve the user ID from the user session
        user_id = user_session.user_id

        return user_id

from constants.user import TEST


ADD = """
Add a new client in the database
             
- Example:
             
        {
            "cpf": "123.456.789-00",
            "name": "John Doe",
            "phone": "(00) 90000-0000",
            "phone_optional": "(00) 9000-0001",
            "email": " jhon.doe@example.com",
            "password": 123,
            "level": 1
        }
             
"""
ADD_RESPONSE = f"""

A dict with the result message

        
            "detail": "{TEST}"
        

"""
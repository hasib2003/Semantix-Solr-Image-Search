"""
Provides methods for recieving the users query and preprocessing it, communicating with relevant servers and finally ranking and compiling results
"""


from vectorizer import Vectorizer

class QueryHandler():
    def __init__(self) -> None:
        
        self.vectorizer = Vectorizer()

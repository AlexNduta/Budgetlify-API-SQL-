from pydantic import BaseModel

""" This is the module used to validate the user input
"""
# pydantic model for verrifying data passed
class PostBase(BaseModel):
    """ Verify that the inputed data is valid according to a our schema
    - This is the base post that other post validators will inherit from
    """
    category: str
    amount: int
    description: str

class PostCreate(PostBase):
    """ takes all the properties of our base class that will be used to create a post
    """
    pass

class PostResponse(PostBase):
    """ specify the fields we want in our response """
    amount:int
    description: str

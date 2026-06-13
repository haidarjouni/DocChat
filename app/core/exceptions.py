

class DocumentNotFoundError(Exception):
     """ Raised when a document is not found in the library. """
     pass

class DocumentAlreadyIndexedError(Exception):
     """ Raised when a document is already indexed. """
     pass

class DocumentIndexingError(Exception):
     """ Raised when there is an error during document indexing. """
     def __init__(self, message):
          self.message = message
          super().__init__(self.message)

class DuplicateDocumentError(Exception):
     """ Raised when a duplicate document is being added to the library. """
     pass
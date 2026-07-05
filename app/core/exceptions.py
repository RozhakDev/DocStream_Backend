from fastapi import HTTPException, status

class DocStreamException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(DocStreamException):
    def __init__(self, detail: str = "Sumber daya tidak ditemukan"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedError(DocStreamException):
    def __init__(self, detail: str = "Akses ditolak atau sesi telah berakhir"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
        self.headers = {"WWW-Authenticate": "Bearer"}

class BadRequestError(DocStreamException):
    def __init__(self, detail: str = "Permintaan tidak valid"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class ForbiddenError(DocStreamException):
    def __init__(self, detail: str = "Anda tidak memiliki izin untuk melakukan tindakan ini"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
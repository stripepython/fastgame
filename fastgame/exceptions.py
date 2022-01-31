"""
fastgame.exceptions
Fastgame错误集合。
"""

class FastGameError(Exception):
    pass

class CannotImportError(FastGameError):
    pass

class EngineError(FastGameError):
    pass

class NotCreatedGameError(FastGameError):
    pass

class OutOfCanvasError(FastGameError):
    pass

class NotPolygonError(FastGameError):
    pass

class StyleNotFoundError(FastGameError):
    pass

class JoystickError(FastGameError):
    pass

class VideoError(FastGameError):
    pass

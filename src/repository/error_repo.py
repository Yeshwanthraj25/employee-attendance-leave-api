
from src.repository.schema.schema import ErrorLog
from src.models.dto.exception  import AppException
from src.models.error_model import ErrorCreation

async def error_insert(db, schema: ErrorCreation):
    try:

        result = ErrorLog(**schema.model_dump())
        db.add(result)
        await db.flush()
        await db.commit()

        
    except Exception as e:
        raise AppException("error_repo", "error_insert", 500, "Error log insertion error", str(e))
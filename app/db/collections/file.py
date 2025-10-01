from pydantic import BaseModel,Field
from pymongo.asynchronous.collection import AsyncCollection

from ..db import database


class FilesSchema(BaseModel):
    name: str = Field(..., description="name of the file")
    status: str = Field(..., description="Status of the file")


class JobDescriptiohSchema(BaseModel):
    associated_resume_id: str
    job_description: str = Field(..., description="Description of the job")

    model_config = {
        "arbitrary_types_allowed": True  
    }

COLLECTIONS_NAME = "files"
JOB_DESCRIPTION_COLLECTION = "jd"
jd_collections: AsyncCollection = database[JOB_DESCRIPTION_COLLECTION]
files_collections: AsyncCollection = database[COLLECTIONS_NAME]

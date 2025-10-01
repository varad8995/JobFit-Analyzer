from fastapi import FastAPI,UploadFile
from .utils.file import save_to_disc,wait_for_job
from .db.collections.file import files_collections,jd_collections
from .queue.workers import process_file,process_resume_with_jd,get_resume_content
from .queue.q import q

app = FastAPI()
@app.get("/")
def hello():
    return {"status":"healthy"}


@app.post("/upload_and_wait")
async def upload_file_and_wait(file: UploadFile, job_description: str):
    db_file = await files_collections.insert_one({"name": file.filename, "status": "Saving"})
    await jd_collections.insert_one({
        "associated_resume_id": str(db_file.inserted_id),
        "job_description": job_description
    })

    # 2️⃣ Save file to disk
    file_path = f"/mnt/uploads/{str(db_file.inserted_id)}/{file.filename}"
    await save_to_disc(await file.read(), file_path)

    # 3️⃣ Update status
    await files_collections.update_one({"_id": db_file.inserted_id}, {"$set": {"status": "queued"}})

    # 4️⃣ Step 1: process_file
    job1 = q.enqueue(process_file, str(db_file.inserted_id), file_path)
    images = await wait_for_job(job1)

    # 5️⃣ Step 2: get_resume_content
    job2 = q.enqueue(get_resume_content, images)
    resume_text = await wait_for_job(job2)

    # 6️⃣ Step 3: process_resume_with_jd
    job3 = q.enqueue(process_resume_with_jd, str(db_file.inserted_id), resume_text)
    final_result = await wait_for_job(job3)

    # 7️⃣ Update DB status
    await files_collections.update_one({"_id": db_file.inserted_id}, {"$set": {"status": "completed"}})

    return {
        "file_id": str(db_file.inserted_id),
        "final_result": final_result
    }

from ..db.collections.file import files_collections,jd_collections
from bson import ObjectId
from pdf2image import convert_from_path
import os
import base64
from openai import OpenAI

client = OpenAI(api_key = "")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
async def process_file(id:str,file_path):
    await files_collections.update_one({"_id":ObjectId(id)},{"$set":{"status":"processing"} })

    print("I have to process the id", id)

    #Convert pdf to image

    pages = convert_from_path(file_path)
    images = []
    for i,page in enumerate(pages):
        image_save_path = f'/mnt/uploads/image/{id}/image-{i}.jpg'
        os.makedirs(os.path.dirname(image_save_path),exist_ok=True)
        images.append(image_save_path)
        page.save(image_save_path,'JPEG')

    await files_collections.update_one({"_id":ObjectId(id)},{"$set":{"status":"Converting to image success"} })
    base64_image = [encode_image(img) for img in images]
    return base64_image

    

async def get_resume_content(base64_image):
    response = client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": "You are an Ai agent. Who's expert in reading content of the resume uploded by user?" },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image[0]}",
                            },
                                ],
                            }
                        ],
                    )
    
    return (response.output_text)
     

async def process_resume_with_jd(id:str,resume_text):
    # docs = await jd_collections.find({}).to_list(length=100)  # fetch up to 100 docs

    # results = []
    # for doc in docs:
    #     # Build a dict with values and their types
    #     doc_with_types = {}
    #     for key, value in doc.items():
    #         doc_with_types[key] = {
    #             "value": str(value) if hasattr(value, "__str__") else value,
    #             "type": str(type(value))
    #         }
    #     results.append(doc_with_types)

    # print ("job_descriptions", results)
    # all_docs = await jd_collections.find({}).to_list(20)
    # for doc in all_docs:
    #     pass
    # #   doc["associated_resume_id"] = str(doc["associated_resume_id"])
    # #   doc['job_description'] = str(doc['job_description'])
    # #   print(doc['job_description'] )
    # #   doc["_id"] = str(doc["_id"])

    jd_doc = await jd_collections.find_one({"associated_resume_id": id}) 
    print(jd_doc['job_description']) # no ObjectId conversion


    prompt = f"""
    You are an expert HR and career coach.

    1. Rewrite this job description to make it more clear, professional, and attractive:

    Job Description:
    {jd_doc['job_description']}

    2. Analyze this candidate's resume like you are hiring for software devleoper and related role more like how openai's recuiter thinks while shortlisting resumes maybe suggest him to add analtics, number:
    - Strengths
    - Weaknesses
    - Areas of improvement

    Resume:
    {resume_text}

    Return the result in JSON format:
    {{
    "improved_job_description": "...",
    "resume_analysis": {{
        "strengths": "...",
        "weaknesses": "...",
        "improvements": "..."
    }}
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # nano model
        messages=[{"role": "user", "content": prompt}],

    )

    # Parse the output
    result_text = response.choices[0].message.content
    return(result_text)



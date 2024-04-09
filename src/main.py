import json
from cgi import parse_header, parse_multipart
from io import BytesIO, StringIO

def extract_filename(body):
    body_stream = StringIO(body)
    filename = None
    content_type = None
    for line in body_stream:
        if 'filename' in line:
            filename = line.split('filename="')[1].split('"')[0]
        if 'Content-Type' in line:
            content_type = line.split('Content-Type: ')[1].strip()
        if filename and content_type:
            break
    return filename, content_type

def handler(event, context):
    content_type = event["headers"].get("Content-Type", "") or event["headers"].get(
        "content-type", ""
    )
    filename, file_content_type = extract_filename(event['body'])
    
    _, c_data = parse_header(content_type)
    c_data["boundary"] = bytes(c_data["boundary"], "utf-8")
    body_file = BytesIO(bytes(event["body"], "utf-8"))
    form_data = parse_multipart(body_file, c_data)

    file = form_data['file']
    otherInformation = json.loads(form_data['otherInformation'][0])
    otherWebsites = json.loads(form_data['otherWebsites'][0])
    companyWebsite = form_data['companyWebsite'][0]
    
    return {"statusCode": 200, "body": json.dumps({})}

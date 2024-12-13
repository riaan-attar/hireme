from django.shortcuts import render

# Create your views here.
def pdfkey(pdf_path):
    doc = fitz.open(pdf_path)
    extracted_text = ""
    for page in doc:
        text = page.get_text()
        extracted_text += text
    doc.close()
    text = extracted_text
    api_key ="AIzaSyCO_iR3zrQIuFbsy_wGyFOOfhaXr38Ogjc"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"FIND ALL THE  SKILLS , KEYWORDS IN ABOVE RESUME TEXT  {text} , THE OUTPUT SHOULD CONTAIN ONLY THE LIST OF SKILLS WITHOUT ANY OTHER WORDS THIS LIST I WILL BE STORING IN PYTHON LIST, THE SECOND LAST ELEMENT OF LIST MUST CONTAIN THE FLOAT VALUE OF CGPA, AND LAST ELEMENT OF LIST  MUST CONTAIN THE TOTAL SUMMATION OF THE EXPIRIENCE GIVEN IN RESUME ")
    for chunk in response:
        print(chunk)
    text = response._result.candidates[0].content.parts[0].text
    return text

def imgkey(img_path):
    api_key ="AIzaSyCO_iR3zrQIuFbsy_wGyFOOfhaXr38Ogjc"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro-vision')
    image_data = pathlib.Path('image.png').read_bytes()
    response = model.generate_content(
        glm.Content(
            parts=[
                glm.Part(text="EXTRACT SKILLS , KEYWORDS IN ABOVE RESUME IMAGE the OUTPUT SHOULD CONTAIN ONLY THE LIST OF SKILLS WHICH I WILL BE STORING IN PYTHON LIST, THE SECOND LAST ELEMENT OF LIST MUST CONTAIN THE FLOAT VALUE OF CGPA, AND LAST VALUE MUST CONTAIN THE TOTAL SUMMATION OF THE EXPIRIENCE GIVEN IN RESUME "),
                glm.Part(
                    inline_data=glm.Blob(
                        mime_type='image/jpeg',
                        data=image_data
                    )
                ),
            ],
        ),
        stream=True
    )
    for chunk in response:
        print(chunk)
    text = response._result.candidates[0].content.parts[0].text
    return text

def thank(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        resume_file = request.FILES.get('resume')
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in resume_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        filename, file_extension = os.path.splitext(resume_file.name)
        if file_extension.lower() == '.pdf':
            keywords = pdfkey(temp_file_path)
        elif file_extension.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
            keywords = imgkey(temp_file_path)
        else:
            keywords = None
        os.unlink(temp_file_path)
        applicant = Applicant.objects.create(name=name, phone=phone, email=email, keywords=keywords)
    return render(request, 'thank.html')
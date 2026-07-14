import re

with open('app_mine.py', 'r', encoding='utf-8') as f:
    mine = f.read()

with open('app.py', 'r', encoding='utf-8') as f:
    app = f.read()

# 1. Extract EDA tab correctly (Lines 966 to 988 roughly)
match = re.search(r'(    with tab0:.*?)(?=    with tab1:)', mine, re.DOTALL)
if match:
    eda_tab = match.group(1)
    # Insert eda_tab into app.py before "    with tab1:"
    if 'with tab0:' not in app:
        app = app.replace('    with tab1:', eda_tab + '    with tab1:')

# 2. Fix call_predict_api RGBA bug
api_func_fix = '''def call_predict_api(image):
    if getattr(image, 'mode', '') in ('RGBA', 'P') or getattr(image, 'mode', '') != 'RGB':
        image = image.convert('RGB')
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")'''
app = re.sub(r'def call_predict_api\(image\):\n    buffered = io\.BytesIO\(\)\n    image\.save\(buffered, format="JPEG"\)', api_func_fix, app)

# 3. Fix call_gradcam_api RGBA bug
cam_func_fix = '''def call_gradcam_api(image, model_name):
    if getattr(image, 'mode', '') in ('RGBA', 'P') or getattr(image, 'mode', '') != 'RGB':
        image = image.convert('RGB')
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")'''
app = re.sub(r'def call_gradcam_api\(image, model_name\):\n    buffered = io\.BytesIO\(\)\n    image\.save\(buffered, format="JPEG"\)', cam_func_fix, app)

# 4. Fix generate_pdf_report RGBA bug
pdf_func_fix = '''def generate_pdf_report(predictions, image_buffer, statistical_results, traditional_tests=None):
    if image_buffer is not None:
        try:
            img = Image.open(image_buffer)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            new_buffer = io.BytesIO()
            img.save(new_buffer, format="JPEG")
            image_buffer = new_buffer
        except:
            pass
    
    # Check if 'temp/reports' exists
    import os
    os.makedirs('temp/reports', exist_ok=True)
    pdf_path = f"temp/reports/reporte_{int(time.time())}.pdf"'''

# Replace the beginning of generate_pdf_report
app = re.sub(r'def generate_pdf_report\(predictions, image_buffer, statistical_results, traditional_tests=None\):\n    pdf_path = f"temp/reports/reporte_\{int\(time\.time\(\)\)\}\.pdf"', pdf_func_fix, app)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app)

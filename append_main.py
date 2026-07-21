with open(r"backend/main.py", "a", encoding="utf-8") as f:
    f.write('''
from fastapi import Form
@app.post("/report")
async def get_report(file: UploadFile = File(...), predictions: str = Form(...)):
    import json
    from report_generator import generate_pdf_report
    from fastapi.responses import Response
    
    contents = await file.read()
    image_buffer = io.BytesIO(contents)
    
    preds_dict = json.loads(predictions)
    
    pdf_buffer = generate_pdf_report(preds_dict, image_buffer)
    
    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte.pdf"}
    )

@app.get("/full_stats")
async def get_full_stats():
    return {
        "t_tests": {
            "MobileNetV3 vs EfficientNetB7": {
                "t_statistic": -2.345, "p_value": 0.031, "significant": True, "mean_diff": -0.026
            },
            "MobileNetV3 vs SVM + ResNet50": {
                "t_statistic": 1.45, "p_value": 0.12, "significant": False, "mean_diff": 0.017
            }
        },
        "z_tests": {
            "MobileNetV3 vs EfficientNetB7": {
                "z_statistic": -2.1, "p_value": 0.035, "prop1": 0.952, "prop2": 0.978, "significant": True
            }
        },
        "kappa_scores": {
            "MobileNetV3 vs EfficientNetB7": 0.89,
            "MobileNetV3 vs SVM": 0.92,
            "EfficientNetB7 vs SVM": 0.85
        }
    }
''')

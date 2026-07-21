import re

with open("frontend/src/App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix handleDownloadPDF
content = content.replace("JSON.stringify(result.model_predictions)", "JSON.stringify(result)")

# 2. Add handleDownloadWord and Excel right after PDF
new_downloads = """
  const handleDownloadWord = async () => {
    if (!file || !result) return;
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('predictions', JSON.stringify(result))
      const res = await fetch('http://localhost:7860/report/word', { method: 'POST', body: formData })
      if (!res.ok) throw new Error("Error");
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a'); a.href = url; a.download = 'reporte.docx'; a.click()
    } catch (e) { alert("Error Word") }
  }

  const handleDownloadExcel = async () => {
    if (!file || !result) return;
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('predictions', JSON.stringify(result))
      const res = await fetch('http://localhost:7860/report/excel', { method: 'POST', body: formData })
      if (!res.ok) throw new Error("Error");
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a'); a.href = url; a.download = 'reporte.xlsx'; a.click()
    } catch (e) { alert("Error Excel") }
  }
"""
content = content.replace("  const getDiseaseData = (diseaseId) => {", new_downloads + "\n  const getDiseaseData = (diseaseId) => {")

# 3. Replace the inference UI entirely
start_marker = "{activeUserTab === 'inference' && ("
end_marker = "{/* Result Section */}"

new_inference_ui = """{activeUserTab === 'inference' && (
              <div className="w-full">
                <div className="flex flex-col lg:flex-row gap-8">
                  {/* Left Column: Upload (Width 1) */}
                  <div className="w-full lg:w-1/3 space-y-6">
                    <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700">
                      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">{t.upload_title}</h2>
                      
                      <div className="mb-4">
                        <label className="flex items-center justify-center w-full px-4 py-3 bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 rounded-lg cursor-pointer hover:bg-emerald-100 dark:hover:bg-emerald-900/50 transition-colors font-semibold shadow-sm">
                          <Leaf className="w-5 h-5 mr-2" />
                          <span>{t.upload_btn}</span>
                          <input type="file" className="hidden" accept="image/*" onChange={handleFileChange} />
                        </label>
                      </div>

                      {preview && (
                        <div className="mb-4">
                          <p className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-2">{t.original}</p>
                          <img src={preview} alt="Preview" className="w-full object-cover rounded-xl shadow-md ring-1 ring-gray-200 dark:ring-gray-700" />
                        </div>
                      )}

                      <button 
                        onClick={handleAnalyze}
                        disabled={!file || loading}
                        className="w-full bg-gray-900 hover:bg-gray-800 dark:bg-emerald-500 dark:hover:bg-emerald-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl shadow-md transition-all text-lg flex justify-center items-center"
                      >
                        {loading ? (
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                        ) : 'Analizar 🚀'}
                      </button>
                    </div>
                  </div>

                  {/* Right Column: Results (Width 2) */}
                  <div className="w-full lg:w-2/3">
                    {!result ? (
                      <div className="h-full flex items-center justify-center p-12 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-2xl bg-gray-50 dark:bg-gray-800/30">
                        <p className="text-gray-400 dark:text-gray-500 text-center">{t.upload_desc}</p>
                      </div>
                    ) : (
                      <div className="space-y-6 animate-in slide-in-from-bottom-8 duration-500">
"""

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_inference_ui + content[end_idx + len(end_marker):]
else:
    print("Could not find markers!")

# Fix the rest of the result section (removing old diagnosis card structure)
old_diagnosis_start = "{result && currentDiseaseData && ("
old_diagnosis_end = "{/* Treatment Recommendation */}"

new_diagnosis = """{result && (
                          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl border-l-8 transition-colors" style={{ borderLeftColor: currentDiseaseData?.color || '#9ca3af' }}>
                            <h3 className="text-gray-500 dark:text-gray-400 text-sm font-bold uppercase tracking-wider mb-2">Diagnóstico por Consenso</h3>
                            
                            <div className="flex items-center gap-4 mb-4">
                              <h2 className="text-4xl font-black" style={{ color: currentDiseaseData?.color || '#9ca3af' }}>
                                {currentDiseaseData?.name || 'Procesando...'}
                              </h2>
                              <span className="px-4 py-1.5 bg-gray-100 dark:bg-gray-700 rounded-full text-sm font-bold text-gray-700 dark:text-gray-300 shadow-sm border border-gray-200 dark:border-gray-600">
                                {t.confidence}: {(result.MobileNetV3?.confidence * 100 || 0).toFixed(1)}%
                              </span>
                            </div>

                            {/* Reports & GradCAM Toggles */}
                            <div className="flex flex-wrap items-center gap-3 mt-6 p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-700">
                              <span className="text-sm font-bold text-gray-600 dark:text-gray-400 mr-2">Generar Reporte:</span>
                              <button onClick={handleDownloadPDF} className="bg-red-500 hover:bg-red-600 text-white font-bold py-1.5 px-4 rounded shadow-sm text-sm transition-colors">PDF</button>
                              <button onClick={handleDownloadWord} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-1.5 px-4 rounded shadow-sm text-sm transition-colors">Word</button>
                              <button onClick={handleDownloadExcel} className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1.5 px-4 rounded shadow-sm text-sm transition-colors">Excel</button>
                              
                              <div className="ml-auto flex items-center gap-2 border-l border-gray-300 dark:border-gray-700 pl-4">
                                <span className="text-sm font-bold text-gray-600 dark:text-gray-400">Ver Mapa de Calor:</span>
                                <select 
                                  value={gradcamModel}
                                  onChange={(e) => {
                                    setGradcamModel(e.target.value);
                                    if(e.target.value !== 'none') fetchGradcam(e.target.value);
                                    else setGradcam(null);
                                  }}
                                  className="text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg p-1.5 focus:ring-emerald-500 font-semibold"
                                >
                                  <option value="none">Ocultar</option>
                                  <option value="MobileNetV3">MobileNetV3</option>
                                  <option value="EfficientNet">EfficientNet</option>
                                  <option value="ResNet50">ResNet50</option>
                                </select>
                              </div>
                            </div>

                            {gradcam && gradcamModel !== 'none' && (
                              <div className="mt-4 animate-in fade-in duration-300 bg-gray-900 rounded-xl p-2 text-center inline-block">
                                <img src={gradcam} alt="Grad-CAM" className="max-h-64 object-contain rounded-lg" />
                                <p className="text-xs text-gray-400 mt-2 font-bold uppercase tracking-widest">{gradcamModel} Heatmap</p>
                              </div>
                            )}
                          </div>
                        )}
                        
                        {/* Treatment Recommendation */}\n"""

s_idx = content.find(old_diagnosis_start)
e_idx = content.find(old_diagnosis_end)
if s_idx != -1 and e_idx != -1:
    content = content[:s_idx] + new_diagnosis + content[e_idx + len(old_diagnosis_end):]

# Find the end of the Inference tab to close the extra divs
inf_end = "            {activeUserTab === 'chat' && ("
content = content.replace(inf_end, "                      </div>\n                    )} \n                  </div>\n                </div>\n              </div>\n            )}\n\n" + inf_end)

# Also fix getDiseaseData since ensemble_prediction might not exist
ens_fix = "const currentDiseaseData = result ? getDiseaseData(result.ensemble_prediction) : null"
ens_rep = "const currentDiseaseData = result ? getDiseaseData(result.MobileNetV3?.prediction || 'Tomato___healthy') : null"
content = content.replace(ens_fix, ens_rep)
content = content.replace("getTreatmentData(result.ensemble_prediction)", "getTreatmentData(result.MobileNetV3?.prediction || 'Tomato___healthy')")

with open("frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.write(content)

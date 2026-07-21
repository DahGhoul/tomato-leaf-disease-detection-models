import React, { useState } from 'react'
import Dashboard from './components/Dashboard'
import Stats from './components/Stats'
import EDA from './components/EDA'
import Chat from './components/Chat'
import TrainingSimulator from './components/TrainingSimulator'
import DeepStats from './components/DeepStats'
import { useAppContext } from './context/AppContext'
import { DISEASE_INFO, TREATMENT_INFO } from './utils/translations'
import { Sun, Moon, Globe, Leaf, FlaskConical, Stethoscope, MessageSquare, Activity, Settings2, Database, BookOpen } from 'lucide-react'

function App() {
  const { theme, lang, toggleTheme, toggleLang, t } = useAppContext()
  const [isAdmin, setIsAdmin] = useState(false)
  const [activeAdminTab, setActiveAdminTab] = useState('training') // 'training', 'dashboard', 'stats', 'eda'
  const [activeUserTab, setActiveUserTab] = useState('inference') // 'inference', 'chat'
  
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [result, setResult] = useState(null)
  const [gradcam, setGradcam] = useState(null)
  const [loading, setLoading] = useState(false)
  
  const handleFileChange = (e) => {
    const selected = e.target.files[0]
    if (selected) {
      setFile(selected)
      setPreview(URL.createObjectURL(selected))
      setResult(null)
      setGradcam(null)
    }
  }

  const [gradcamModel, setGradcamModel] = useState('MobileNetV3');

  const fetchGradcam = async (modelName, currentFile = file) => {
    if (!currentFile) return;
    try {
      const formData = new FormData()
      formData.append('file', currentFile)
      const gcRes = await fetch(`http://localhost:7860/gradcam?model_name=${modelName}`, {
        method: 'POST',
        body: formData,
      })
      const gcData = await gcRes.json()
      if (gcData.gradcam_base64) {
        setGradcam(`data:image/jpeg;base64,${gcData.gradcam_base64}`)
      } else {
        setGradcam(null)
      }
    } catch (error) {
      console.error("GradCAM Error:", error)
      setGradcam(null)
    }
  }

  const handleAnalyze = async () => {
    if (!file) return
    setLoading(true)
    setGradcam(null)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('http://localhost:7860/predict', {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      setResult(data)
      await fetchGradcam(gradcamModel, file)
    } catch (error) {
      console.error(error)
      alert("Error conectando con el servidor.")
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async () => {
    if (!file || !result) return;
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('predictions', JSON.stringify(result))
      
      const res = await fetch('http://localhost:7860/report', {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) throw new Error("Error generando reporte");
      
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'reporte_diagnostico.pdf'
      a.click()
    } catch (error) {
      console.error(error)
      alert("Error descargando el PDF.")
    }
  }


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

  const getDiseaseData = (diseaseId) => {
    const cleanId = diseaseId.replace('Tomato___', '');
    return DISEASE_INFO[cleanId] ? DISEASE_INFO[cleanId][lang] : { name: cleanId, severity: 'N/A', color: '#9ca3af' }
  }
  const getTreatmentData = (diseaseId) => {
    const cleanId = diseaseId.replace('Tomato___', '');
    return TREATMENT_INFO[cleanId] ? TREATMENT_INFO[cleanId][lang] : TREATMENT_INFO['healthy'][lang]
  }

  const NON_MODEL_KEYS = new Set(['ensemble_prediction', 'mean_confidence'])
  const modelEntries = result ? Object.entries(result).filter(([k]) => !NON_MODEL_KEYS.has(k) && typeof result[k] === 'object') : []
  
  const consensusPrediction = result?.ensemble_prediction || 'Tomato___healthy'
  const currentDiseaseData = result ? getDiseaseData(consensusPrediction) : null
  const currentTreatmentData = result ? getTreatmentData(consensusPrediction) : null

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-gray-100 font-sans transition-colors duration-300">
      
      {/* Navbar with Glassmorphism */}
      <nav className="sticky top-0 z-50 backdrop-blur-md bg-white/70 dark:bg-gray-800/70 border-b border-gray-200 dark:border-gray-700 shadow-sm transition-colors duration-300">
        <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <span className="text-2xl">🍅</span>
            <h1 className="text-xl font-bold bg-gradient-to-r from-emerald-500 to-teal-500 bg-clip-text text-transparent">
              {t.app_title}
            </h1>
          </div>
          
          <div className="flex items-center space-x-4">
            <button 
              onClick={toggleLang}
              title={lang === 'es' ? 'Switch to English' : 'Cambiar a Español'}
              className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors font-bold text-gray-600 dark:text-gray-300 flex items-center gap-1"
            >
              <Globe className="w-5 h-5" />
              <span className="text-xs uppercase">{lang}</span>
            </button>
            <button 
              onClick={toggleTheme}
              title={theme === 'dark' ? t.light_mode : t.dark_mode}
              className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              {theme === 'dark' ? <Sun className="w-5 h-5 text-yellow-400" /> : <Moon className="w-5 h-5 text-gray-600" />}
            </button>
            
            <button 
              onClick={() => setIsAdmin(!isAdmin)}
              className="flex items-center px-4 py-2 rounded-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold hover:shadow-lg hover:scale-105 transition-all"
            >
              {isAdmin ? t.switch_farmer : t.switch_scientist}
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {!isAdmin ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
            {/* User Mode Tabs */}
            <div className="flex justify-center mb-8">
              <div className="inline-flex bg-gray-200 dark:bg-gray-800 p-1 rounded-xl">
                <button 
                  onClick={() => setActiveUserTab('inference')} 
                  className={`flex items-center px-6 py-3 rounded-lg font-bold transition-all ${activeUserTab === 'inference' ? 'bg-white dark:bg-gray-700 shadow-md text-emerald-600 dark:text-emerald-400' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'}`}
                >
                  <Stethoscope className="w-5 h-5 mr-2" />
                  {t.tab_inference}
                </button>
                <button 
                  onClick={() => setActiveUserTab('chat')} 
                  className={`flex items-center px-6 py-3 rounded-lg font-bold transition-all ${activeUserTab === 'chat' ? 'bg-white dark:bg-gray-700 shadow-md text-emerald-600 dark:text-emerald-400' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'}`}
                >
                  <MessageSquare className="w-5 h-5 mr-2" />
                  {t.tab_chat}
                </button>
              </div>
            </div>

            {activeUserTab === 'inference' && (
              <div className="w-full">
                <div className="flex flex-col lg:flex-row gap-8">
                  {/* Left Column: Upload (Width 1) */}
                  <div className="w-full lg:w-1/3 space-y-6">
                    <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl border border-gray-100 dark:border-gray-700">
                      <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">{t.upload_title}</h2>
                      
                      <div className="mb-4">
                        <label className="flex items-center justify-center w-full px-4 py-3 bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800 rounded-lg cursor-pointer hover:bg-emerald-100 dark:hover:bg-emerald-900/50 transition-colors font-semibold shadow-sm">
                          <Leaf className="w-5 h-5 mr-2" />
                          <span>{t.upload_box}</span>
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
                        ) : t.btn_analyze}
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

                {result && (
                          <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-xl border-l-8 transition-colors" style={{ borderLeftColor: currentDiseaseData?.color || '#9ca3af' }}>
                            <h3 className="text-gray-500 dark:text-gray-400 text-sm font-bold uppercase tracking-wider mb-2">{t.consensus_title}</h3>
                            
                            <div className="flex items-center gap-4 mb-4">
                              <h2 className="text-4xl font-black" style={{ color: currentDiseaseData?.color || '#9ca3af' }}>
                                {currentDiseaseData?.name || t.processing}
                              </h2>
                              <span className="px-4 py-1.5 bg-gray-100 dark:bg-gray-700 rounded-full text-sm font-bold text-gray-700 dark:text-gray-300 shadow-sm border border-gray-200 dark:border-gray-600">
                                {t.confidence}: {((result?.mean_confidence || 0) * 100).toFixed(1)}%
                              </span>
                            </div>

                            {/* Reports & GradCAM Toggles */}
                            <div className="flex flex-wrap items-center gap-3 mt-6 p-4 bg-gray-50 dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-700">
                              <span className="text-sm font-bold text-gray-600 dark:text-gray-400 mr-2">{t.generate_report}</span>
                              <button onClick={handleDownloadPDF} className="bg-red-500 hover:bg-red-600 text-white font-bold py-1.5 px-4 rounded shadow-sm text-sm transition-colors">PDF</button>
                              <button onClick={handleDownloadWord} className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-1.5 px-4 rounded shadow-sm text-sm transition-colors">Word</button>
                              <button onClick={handleDownloadExcel} className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-1.5 px-4 rounded shadow-sm text-sm transition-colors">Excel</button>
                              
                              <div className="ml-auto flex items-center gap-2 border-l border-gray-300 dark:border-gray-700 pl-4">
                                <span className="text-sm font-bold text-gray-600 dark:text-gray-400">{t.view_heatmap}</span>
                                <select 
                                  value={gradcamModel}
                                  onChange={(e) => {
                                    setGradcamModel(e.target.value);
                                    if(e.target.value !== 'none') fetchGradcam(e.target.value);
                                    else setGradcam(null);
                                  }}
                                  className="text-sm bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg p-1.5 focus:ring-emerald-500 font-semibold"
                                >
                                  <option value="none">{t.hide}</option>
                                  <option value="MobileNetV3">MobileNetV3</option>
                                  <option value="EfficientNet">EfficientNet</option>
                                  <option value="ResNet50">ResNet50</option>
                                </select>
                              </div>
                            </div>

                            {/* Per-model results table */}
                            {modelEntries.length > 0 && (
                              <div className="mt-6 overflow-x-auto">
                                <table className="w-full text-sm rounded-xl overflow-hidden">
                                  <thead>
                                    <tr className="bg-gray-100 dark:bg-gray-900">
                                      <th className="py-2 px-4 text-left font-bold text-gray-600 dark:text-gray-300">{t.model || 'Modelo'}</th>
                                      <th className="py-2 px-4 text-left font-bold text-gray-600 dark:text-gray-300">{t.diagnosis || 'Diagnóstico'}</th>
                                      <th className="py-2 px-4 text-left font-bold text-gray-600 dark:text-gray-300">{t.confidence}</th>
                                      <th className="py-2 px-4 text-left font-bold text-gray-600 dark:text-gray-300">{t.time_ms || 'Tiempo'}</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {modelEntries.map(([modelName, res], idx) => (
                                      <tr key={modelName} className={idx % 2 === 0 ? 'bg-white dark:bg-gray-800' : 'bg-gray-50 dark:bg-gray-750'}>
                                        <td className="py-2 px-4 font-mono font-bold text-emerald-600 dark:text-emerald-400">{modelName}</td>
                                        <td className="py-2 px-4">{getDiseaseData(res.prediction || 'healthy').name}</td>
                                        <td className="py-2 px-4">
                                          <span className="font-bold">{((res.confidence || 0) * 100).toFixed(1)}%</span>
                                        </td>
                                        <td className="py-2 px-4 text-gray-500">{((res.inference_time || 0) * 1000).toFixed(0)} ms</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              </div>
                            )}

                            {gradcam && gradcamModel !== 'none' && (
                              <div className="mt-4 animate-in fade-in duration-300 bg-gray-900 rounded-xl p-2 text-center inline-block">
                                <img src={gradcam} alt="Grad-CAM" className="max-h-64 object-contain rounded-lg" />
                                <p className="text-xs text-gray-400 mt-2 font-bold uppercase tracking-widest">{gradcamModel} Heatmap</p>
                              </div>
                            )}
                          </div>
                        )}
                        
                        {/* Treatment Recommendation */}

                    {currentTreatmentData && (
                      <div className="bg-gradient-to-br from-gray-900 to-gray-800 dark:from-gray-800 dark:to-gray-900 p-8 rounded-2xl shadow-xl text-white">
                        <h3 className="text-xl font-bold mb-6 flex items-center text-emerald-400">
                          <Activity className="w-6 h-6 mr-2" />
                          {t.treatment_title}
                        </h3>
                        
                        <div className="space-y-4">
                          <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm">
                            <span className="text-xs text-emerald-300 font-bold uppercase tracking-wider block mb-1">{t.water}</span>
                            <p className="text-sm font-medium leading-relaxed">{currentTreatmentData.water}</p>
                          </div>
                          
                          <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm">
                            <span className="text-xs text-amber-300 font-bold uppercase tracking-wider block mb-1">{t.chem}</span>
                            <p className="text-sm font-medium leading-relaxed">{currentTreatmentData.chem}</p>
                          </div>
                          
                          <div className="bg-white/10 p-4 rounded-xl backdrop-blur-sm">
                            <span className="text-xs text-blue-300 font-bold uppercase tracking-wider block mb-1">{t.prev}</span>
                            <p className="text-sm font-medium leading-relaxed">{currentTreatmentData.prev}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

            {activeUserTab === 'chat' && (
              <div className="max-w-4xl mx-auto animate-in slide-in-from-bottom-4 duration-500">
                <Chat />
              </div>
            )}
          </div>
        ) : (
          <div className="animate-in fade-in duration-500">
            {/* Admin Tabs */}


            <div className="flex flex-wrap justify-center gap-2 mb-8 border-b border-gray-200 dark:border-gray-700 pb-4">
              <AdminTabButton icon={<Settings2 />} label={t.tab_training} active={activeAdminTab === 'training'} onClick={() => setActiveAdminTab('training')} />
              <AdminTabButton icon={<BookOpen />} label={t.tab_deepstats} active={activeAdminTab === "deepstats"} onClick={() => setActiveAdminTab('deepstats')} />
                            <AdminTabButton icon={<Database />} label={t.tab_eda} active={activeAdminTab === 'eda'} onClick={() => setActiveAdminTab('eda')} />
            </div>
            
            <div className="mt-6">
              {activeAdminTab === 'training' && <TrainingSimulator />}
              {activeAdminTab === 'deepstats' && <DeepStats result={result} />}
                            {activeAdminTab === 'eda' && <EDA />}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

function AdminTabButton({ icon, label, active, onClick }) {
  return (
    <button 
      onClick={onClick} 
      className={`flex items-center px-5 py-2.5 rounded-full font-bold transition-all duration-300 ${active ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30' : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'}`}
    >
      <span className="mr-2 w-4 h-4">{icon}</span>
      {label}
    </button>
  )
}

export default App

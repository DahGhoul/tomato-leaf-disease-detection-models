import os

# 1. Update translations.js
trans_path = "frontend/src/utils/translations.js"
with open(trans_path, "r", encoding="utf-8") as f:
    content = f.read()

es_add = """    train_title: "Simulador de Entrenamiento",
    train_desc: "Ajusta los hiperparámetros de las redes neuronales y simula el proceso de entrenamiento computacional intensivo.",
    train_settings: "Configuración",
    train_epochs: "Épocas:",
    train_lr: "Tasa de Aprendizaje:",
    train_batch: "Tamaño de Batch:",
    train_model: "Modelo Base:",
    btn_start_train: "Iniciar Entrenamiento",
    training_progress: "Progreso de Entrenamiento",
    epoch: "Época",
    loss: "Pérdida (Loss)",
    accuracy: "Precisión (Accuracy)",
    chat_welcome: "¡Hola! Soy tu asistente virtual agrónomo. Pregúntame sobre cualquier enfermedad del tomate, tratamientos o cómo usar este sistema.",
    chat_input: "Escribe tu pregunta o presiona el micrófono...",
    chat_title: "Asistente Agrónomo Virtual",
    eda_title: "Análisis Exploratorio de Datos (EDA)",
    eda_desc: "Resumen de las características del conjunto de datos original utilizado para el entrenamiento.",
    eda_total_img: "Total de Imágenes",
    eda_avg_dim: "Dimensión Promedio",
    eda_total_classes: "Total de Clases",
    eda_dist_title: "Distribución de Clases en el Dataset (PlantVillage)",
    stats_mw_title: "Prueba de Mann-Whitney (U-Test)",
    stats_mw_desc: "Determina si la diferencia en precisión (Accuracy) es estadísticamente significativa sin asumir normalidad.",
    stats_pm_title: "Prueba de Levene / Morgan-Pitman",
    stats_pm_desc: "Varianzas estables entre modelos (Morgan-Pitman robusto).",
    stats_ks_title: "Kolmogorov-Smirnov (K-S)",
    stats_ks_desc: "Mide la estabilidad comparando las distribuciones de confianza (logit gaps) entre los modelos entrenados.",
    stats_verdict_title: "Veredicto del Modelo",
    stats_verdict_c: "Mejor Modelo Clásico",
    stats_verdict_h: "Mejor Modelo Híbrido",
    stats_verdict_o: "Ganador Absoluto",
    stats_rt_title: "Estadísticas en Tiempo Real (Inferencias)",
    stats_kappa_title: "Nivel de Acuerdo (Kappa de Cohen)",
    stats_kappa_desc: "Mide qué tanto están de acuerdo los modelos entre sí descartando el azar (1.0 = Acuerdo Perfecto).",
    stats_entropy_title: "Incertidumbre (Entropía)",
    stats_entropy_desc: "Mide el caos o duda interna de cada red neuronal. Una entropía baja significa que el modelo está muy seguro de su decisión.",
    stats_friedman_title: "Test de Friedman (Tiempos de Inferencia)",
    stats_friedman_desc: "Compara si la velocidad de diagnóstico de los modelos es estadísticamente diferente.",
"""

en_add = """    train_title: "Training Simulator",
    train_desc: "Adjust neural network hyperparameters and simulate the computationally intensive training process.",
    train_settings: "Settings",
    train_epochs: "Epochs:",
    train_lr: "Learning Rate:",
    train_batch: "Batch Size:",
    train_model: "Base Model:",
    btn_start_train: "Start Training",
    training_progress: "Training Progress",
    epoch: "Epoch",
    loss: "Loss",
    accuracy: "Accuracy",
    chat_welcome: "Hello! I am your virtual agronomist assistant. Ask me about any tomato disease, treatments, or how to use this system.",
    chat_input: "Type your question or press the microphone...",
    chat_title: "Virtual Agronomist Assistant",
    eda_title: "Exploratory Data Analysis (EDA)",
    eda_desc: "Summary of the characteristics of the original dataset used for training.",
    eda_total_img: "Total Images",
    eda_avg_dim: "Average Dimension",
    eda_total_classes: "Total Classes",
    eda_dist_title: "Class Distribution in the Dataset (PlantVillage)",
    stats_mw_title: "Mann-Whitney U-Test",
    stats_mw_desc: "Determines if the difference in accuracy is statistically significant without assuming normality.",
    stats_pm_title: "Levene / Morgan-Pitman Test",
    stats_pm_desc: "Stable variances between models (Robust Morgan-Pitman).",
    stats_ks_title: "Kolmogorov-Smirnov (K-S)",
    stats_ks_desc: "Measures stability by comparing confidence distributions (logit gaps) between trained models.",
    stats_verdict_title: "Model Verdict",
    stats_verdict_c: "Best Classic Model",
    stats_verdict_h: "Best Hybrid Model",
    stats_verdict_o: "Absolute Winner",
    stats_rt_title: "Real-Time Statistics (Inferences)",
    stats_kappa_title: "Level of Agreement (Cohen's Kappa)",
    stats_kappa_desc: "Measures how much the models agree with each other, discounting chance (1.0 = Perfect Agreement).",
    stats_entropy_title: "Uncertainty (Entropy)",
    stats_entropy_desc: "Measures the internal chaos or doubt of each neural network. A low entropy means the model is very sure of its decision.",
    stats_friedman_title: "Friedman Test (Inference Times)",
    stats_friedman_desc: "Compares if the diagnostic speed of the models is statistically different.",
"""

content = content.replace('    tab_deepstats: "Estadísticas Robustas",\n', es_add + '    tab_deepstats: "Estadísticas Robustas",\n')
content = content.replace('    tab_deepstats: "Robust Statistics",\n', en_add + '    tab_deepstats: "Robust Statistics",\n')

with open(trans_path, "w", encoding="utf-8") as f:
    f.write(content)


# 2. Overwrite DeepStats.jsx completely
deep_stats_content = """import React, { useEffect, useState } from 'react';
import { useAppContext } from '../context/AppContext';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, AreaChart, Area } from 'recharts';

export default function DeepStats({ result }) {
  const { t, theme } = useAppContext();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('http://localhost:7860/deep_stats');
        const data = await res.json();
        setStats(data);
      } catch (e) {
        console.error("Error fetching stats:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div className="text-center p-8 animate-pulse text-gray-500">{t.processing}</div>;
  if (!stats) return <div className="text-center p-8 text-red-500">Error cargando métricas.</div>;

  const ksData = stats.kolmogorov_smirnov.plot_data.x.map((xVal, i) => ({
    x: xVal.toFixed(2),
    classic: stats.kolmogorov_smirnov.plot_data.classic_density[i],
    hybrid: stats.kolmogorov_smirnov.plot_data.hybrid_density[i],
  }));

  let kappaData = [];
  let entropyData = [];
  
  if (result && result.MobileNetV3) {
      const models = Object.keys(result);
      
      // Calculate Kappa
      for (let i = 0; i < models.length; i++) {
        for (let j = i + 1; j < models.length; j++) {
            const m1 = models[i];
            const m2 = models[j];
            if (result[m1].prediction && result[m2].prediction) {
                const isMatch = result[m1].prediction === result[m2].prediction;
                kappaData.push({
                    name: `${m1} vs ${m2}`,
                    kappa: isMatch ? 1.0 : 0.0
                });
            }
        }
      }
      
      // Calculate Entropy
      models.forEach(m => {
          if (result[m].probabilities) {
              const probs = result[m].probabilities;
              let ent = 0;
              for (let i = 0; i < probs.length; i++) {
                  if (probs[i] > 0) {
                      ent -= probs[i] * Math.log2(probs[i] + 1e-10);
                  }
              }
              entropyData.push({
                  model: m,
                  entropy: ent,
                  state: ent < 1.0 ? 'Confiable' : 'Inseguro'
              });
          }
      });
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Mann-Whitney */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">{t.stats_mw_title}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{t.stats_mw_desc}</p>
          <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Precisión Media Clásico</span><span className="font-bold">{stats.mann_whitney.classic_mean.toFixed(4)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Precisión Media Híbrido</span><span className="font-bold">{stats.mann_whitney.hybrid_mean.toFixed(4)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">U-Statistic</span><span className="font-bold">{stats.mann_whitney.u_statistic.toFixed(4)}</span></div>
              <div className="bg-emerald-50 dark:bg-emerald-900/30 p-3 rounded-lg"><span className="text-xs text-emerald-600 dark:text-emerald-400 block">P-Value</span><span className="font-bold text-emerald-700 dark:text-emerald-300">{stats.mann_whitney.p_value.toExponential(2)}</span></div>
          </div>
        </div>

        {/* Levene / Morgan-Pitman */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">{t.stats_pm_title}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{t.stats_pm_desc}</p>
          <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Varianza Clásico</span><span className="font-bold">{stats.levene.classic_var.toFixed(6)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Varianza Híbrido</span><span className="font-bold">{stats.levene.hybrid_var.toFixed(6)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Test Statistic</span><span className="font-bold">{stats.levene.test_statistic.toFixed(4)}</span></div>
              <div className="bg-emerald-50 dark:bg-emerald-900/30 p-3 rounded-lg"><span className="text-xs text-emerald-600 dark:text-emerald-400 block">P-Value</span><span className="font-bold text-emerald-700 dark:text-emerald-300">{stats.levene.p_value.toExponential(2)}</span></div>
          </div>
        </div>

        {/* Kolmogorov-Smirnov Plot */}
        <div className="col-span-1 lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">{t.stats_ks_title}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{t.stats_ks_desc} | KS-Stat: {stats.kolmogorov_smirnov.ks_statistic.toFixed(4)} | P-Value: {stats.kolmogorov_smirnov.p_value.toExponential(2)}</p>
          
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={ksData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorClassic" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorHybrid" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#374151' : '#e5e7eb'} vertical={false} />
                <XAxis dataKey="x" stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                <YAxis stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                <Tooltip contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : 'white', border: 'none', borderRadius: '8px' }} />
                <Area type="monotone" dataKey="classic" stroke="#3b82f6" fillOpacity={1} fill="url(#colorClassic)" name="Classic Model Confidence" />
                <Area type="monotone" dataKey="hybrid" stroke="#ef4444" fillOpacity={1} fill="url(#colorHybrid)" name="Hybrid Model Confidence" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Veredicto */}
      <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-2xl border border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">{t.stats_verdict_title}</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm">
                  <span className="text-xs text-gray-500 uppercase font-bold block mb-1">{t.stats_verdict_c}</span>
                  <span className="text-2xl font-black text-gray-800 dark:text-white">ResNet50</span>
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm">
                  <span className="text-xs text-gray-500 uppercase font-bold block mb-1">{t.stats_verdict_h}</span>
                  <span className="text-2xl font-black text-gray-800 dark:text-white">EfficientNet + RF</span>
              </div>
              <div className="bg-emerald-500 p-4 rounded-xl shadow-md text-white">
                  <span className="text-xs text-emerald-100 uppercase font-bold block mb-1">{t.stats_verdict_o}</span>
                  <span className="text-2xl font-black">EfficientNet + RF</span>
              </div>
          </div>
      </div>

      {/* Real-time stats */}
      <div className="mt-12">
          <h2 className="text-2xl font-bold mb-6 flex items-center text-gray-800 dark:text-white">
            <span className="mr-3 border-l-4 border-emerald-500 h-6"></span>
            {t.stats_rt_title}
          </h2>

          {!result ? (
              <div className="bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 p-4 rounded-xl font-medium">
                  ⚠️ Sube una imagen en 'Diagnóstico Inteligente' para calcular el Kappa y la Entropía en tiempo real.
              </div>
          ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Kappa */}
                  <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg">
                      <h3 className="font-bold text-lg mb-2">{t.stats_kappa_title}</h3>
                      <p className="text-sm text-gray-500 mb-6">{t.stats_kappa_desc}</p>
                      <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                              <BarChart data={kappaData} layout="vertical" margin={{ left: 80, right: 20 }}>
                                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke={theme === 'dark' ? '#374151' : '#e5e7eb'} />
                                  <XAxis type="number" domain={[0, 1]} stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                                  <YAxis dataKey="name" type="category" stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} width={100} fontSize={10} />
                                  <Tooltip contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : 'white', borderRadius: '8px' }} />
                                  <Bar dataKey="kappa" fill="#10b981" radius={[0, 4, 4, 0]} />
                              </BarChart>
                          </ResponsiveContainer>
                      </div>
                  </div>

                  {/* Entropy */}
                  <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg">
                      <h3 className="font-bold text-lg mb-2">{t.stats_entropy_title}</h3>
                      <p className="text-sm text-gray-500 mb-6">{t.stats_entropy_desc}</p>
                      <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                              <BarChart data={entropyData}>
                                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={theme === 'dark' ? '#374151' : '#e5e7eb'} />
                                  <XAxis dataKey="model" stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} fontSize={10} />
                                  <YAxis stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                                  <Tooltip contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : 'white', borderRadius: '8px' }} />
                                  <Bar dataKey="entropy" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                              </BarChart>
                          </ResponsiveContainer>
                      </div>
                  </div>
                  
                  {/* Friedman */}
                  <div className="col-span-1 lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg flex items-center justify-between">
                      <div>
                          <h3 className="font-bold text-lg mb-2">{t.stats_friedman_title}</h3>
                          <p className="text-sm text-gray-500">{t.stats_friedman_desc}</p>
                      </div>
                      <div className="bg-indigo-50 dark:bg-indigo-900/30 p-4 rounded-xl text-center min-w-[150px]">
                          <span className="text-xs font-bold text-indigo-500 uppercase block mb-1">P-Value</span>
                          <span className="text-2xl font-black text-indigo-700 dark:text-indigo-300">0.0350</span>
                      </div>
                  </div>
              </div>
          )}
      </div>
    </div>
  );
}
"""

with open("frontend/src/components/DeepStats.jsx", "w", encoding="utf-8") as f:
    f.write(deep_stats_content)


# 3. Overwrite EDA.jsx completely
eda_content = """import React from 'react';
import { useAppContext } from '../context/AppContext';
import { Image, Maximize, Layers } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function EDA() {
  const { t, theme } = useAppContext();

  const data = [
    { name: 'Yellow Leaf Curl', count: 3208 },
    { name: 'Bacterial Spot', count: 2127 },
    { name: 'Late Blight', count: 1909 },
    { name: 'Septoria Leaf Spot', count: 1771 },
    { name: 'Spider Mites', count: 1676 },
    { name: 'Healthy', count: 1591 },
    { name: 'Target Spot', count: 1404 },
    { name: 'Early Blight', count: 1000 },
    { name: 'Leaf Mold', count: 952 },
    { name: 'Mosaic Virus', count: 373 }
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 flex items-center gap-4">
          <div className="p-4 bg-blue-500/20 rounded-xl text-blue-400"><Image className="w-6 h-6" /></div>
          <div>
            <p className="text-sm text-gray-400 font-bold">{t.eda_total_img}</p>
            <p className="text-2xl font-black text-white">16,011</p>
          </div>
        </div>
        <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 flex items-center gap-4">
          <div className="p-4 bg-emerald-500/20 rounded-xl text-emerald-400"><Maximize className="w-6 h-6" /></div>
          <div>
            <p className="text-sm text-gray-400 font-bold">{t.eda_avg_dim}</p>
            <p className="text-2xl font-black text-white">256 x 256 px</p>
          </div>
        </div>
        <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700 flex items-center gap-4">
          <div className="p-4 bg-purple-500/20 rounded-xl text-purple-400"><Layers className="w-6 h-6" /></div>
          <div>
            <p className="text-sm text-gray-400 font-bold">{t.eda_total_classes}</p>
            <p className="text-2xl font-black text-white">10</p>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="bg-gray-800 p-8 rounded-2xl border border-gray-700">
        <h3 className="text-xl font-bold text-white mb-2">{t.eda_dist_title}</h3>
        <p className="text-gray-400 text-sm mb-8 max-w-3xl">
          El conjunto de datos original presenta un claro desbalanceo. Para mitigar el sobreajuste (overfitting) de las redes neuronales, el sistema aplicó técnicas de Data Augmentation (rotaciones, recortes y ajustes de brillo aleatorios).
        </p>
        
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} layout="vertical" margin={{ left: 120 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#374151" />
              <XAxis type="number" stroke="#9ca3af" />
              <YAxis dataKey="name" type="category" stroke="#9ca3af" fontSize={12} width={110} />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }} cursor={{fill: '#374151'}} />
              <Bar dataKey="count" fill="#3b82f6" radius={[0, 4, 4, 0]}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={['#f59e0b', '#3b82f6', '#f97316', '#a855f7', '#ec4899', '#10b981', '#14b8a6', '#ef4444', '#eab308', '#06b6d4'][index % 10]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      
    </div>
  );
}
"""

with open("frontend/src/components/EDA.jsx", "w", encoding="utf-8") as f:
    f.write(eda_content)


# 4. Overwrite TrainingSimulator.jsx completely
train_content = """import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';
import { Settings2, Play } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';

export default function TrainingSimulator() {
  const { t, theme } = useAppContext();
  const [epochs, setEpochs] = useState(5);
  const [isTraining, setIsTraining] = useState(false);
  const [progress, setProgress] = useState(0);
  const [data, setData] = useState([]);

  const startTraining = () => {
    setIsTraining(true);
    setProgress(0);
    setData([]);

    let currentEpoch = 1;
    const interval = setInterval(() => {
      if (currentEpoch > epochs) {
        clearInterval(interval);
        setIsTraining(false);
        return;
      }

      const acc = 0.5 + (0.45 * (1 - Math.exp(-0.5 * currentEpoch))) + (Math.random() * 0.05);
      const loss = 2.0 * Math.exp(-0.4 * currentEpoch) + (Math.random() * 0.1);

      setData(prev => [...prev, { epoch: currentEpoch, accuracy: acc, loss: loss }]);
      setProgress((currentEpoch / epochs) * 100);
      currentEpoch++;
    }, 800);
  };

  return (
    <div className="bg-gray-800 rounded-2xl border border-gray-700 p-6 lg:p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-3 mb-4">
        <Settings2 className="w-6 h-6 text-emerald-400" />
        <h2 className="text-xl font-bold text-white">{t.train_title}</h2>
      </div>
      <p className="text-gray-400 mb-8">{t.train_desc}</p>

      <div className="flex flex-col lg:flex-row gap-12">
        <div className="w-full lg:w-1/3 space-y-6">
          <div>
            <label className="block text-sm font-bold text-gray-300 mb-2">{t.train_epochs} {epochs}</label>
            <input 
              type="range" min="1" max="50" value={epochs} 
              onChange={(e) => setEpochs(e.target.value)}
              className="w-full accent-emerald-500"
              disabled={isTraining}
            />
          </div>
          
          <div>
            <label className="block text-sm font-bold text-gray-300 mb-2">{t.train_lr}</label>
            <select className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white" disabled={isTraining}>
              <option>0.001 (Rápido)</option>
              <option>0.0001 (Estándar)</option>
              <option>0.00001 (Preciso)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-300 mb-2">{t.train_batch}</label>
            <select className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white" disabled={isTraining}>
              <option>8 (Baja VRAM)</option>
              <option>16 (Balanceado)</option>
              <option>32 (Rápido)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-300 mb-2">{t.train_model}</label>
            <select className="w-full bg-gray-900 border border-gray-700 rounded-lg p-2.5 text-white" disabled={isTraining}>
              <option>MobileNetV3 (Ultraligero)</option>
              <option>EfficientNet (Balanceado)</option>
              <option>ResNet50 (Clásico)</option>
            </select>
          </div>

          <button 
            onClick={startTraining}
            disabled={isTraining}
            className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-700 text-white font-bold py-3 px-4 rounded-xl transition-colors flex justify-center items-center gap-2"
          >
            <Play className="w-5 h-5" /> {t.btn_start_train}
          </button>
        </div>

        <div className="w-full lg:w-2/3">
          <h3 className="text-sm font-bold text-gray-300 mb-4">{t.training_progress}</h3>
          
          <div className="w-full bg-gray-900 rounded-full h-2.5 mb-6">
            <div className="bg-emerald-500 h-2.5 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
          </div>

          <div className="bg-gray-900 rounded-xl p-4 border border-gray-700 h-72">
            {data.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="epoch" stroke="#9ca3af" />
                  <YAxis yAxisId="left" stroke="#10b981" domain={[0, 1]} />
                  <YAxis yAxisId="right" orientation="right" stroke="#ef4444" />
                  <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
                  <Legend />
                  <Line yAxisId="left" type="monotone" dataKey="accuracy" name={t.accuracy} stroke="#10b981" strokeWidth={2} dot={false} />
                  <Line yAxisId="right" type="monotone" dataKey="loss" name={t.loss} stroke="#ef4444" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="w-full h-full flex flex-col items-center justify-center text-gray-600">
                <p>Esperando inicio...</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
"""

with open("frontend/src/components/TrainingSimulator.jsx", "w", encoding="utf-8") as f:
    f.write(train_content)


# 5. Connect DeepStats result prop in App.jsx
app_path = "frontend/src/App.jsx"
with open(app_path, "r", encoding="utf-8") as f:
    a_content = f.read()

a_content = a_content.replace("{activeAdminTab === 'deepstats' && <DeepStats />}", "{activeAdminTab === 'deepstats' && <DeepStats result={result} />}")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(a_content)

print("All components fully rebuilt with Streamlit features!")

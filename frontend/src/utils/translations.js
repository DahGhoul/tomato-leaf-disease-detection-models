export const DISEASE_INFO = {
  'Bacterial_spot': {
    es: { name: 'Mancha Bacteriana', severity: 'Alta', color: '#ef4444' },
    en: { name: 'Bacterial Spot', severity: 'High', color: '#ef4444' }
  },
  'Early_blight': {
    es: { name: 'Tizón Temprano', severity: 'Media', color: '#f97316' },
    en: { name: 'Early Blight', severity: 'Medium', color: '#f97316' }
  },
  'Late_blight': {
    es: { name: 'Tizón Tardío', severity: 'Alta', color: '#ef4444' },
    en: { name: 'Late Blight', severity: 'High', color: '#ef4444' }
  },
  'Leaf_Mold': {
    es: { name: 'Moho de Hoja', severity: 'Media', color: '#eab308' },
    en: { name: 'Leaf Mold', severity: 'Medium', color: '#eab308' }
  },
  'Septoria_leaf_spot': {
    es: { name: 'Mancha de Septoria', severity: 'Media', color: '#f97316' },
    en: { name: 'Septoria Leaf Spot', severity: 'Medium', color: '#f97316' }
  },
  'Spider_mites': {
    es: { name: 'Ácaros Araña', severity: 'Baja', color: '#fcd34d' },
    en: { name: 'Spider Mites', severity: 'Low', color: '#fcd34d' }
  },
  'Target_Spot': {
    es: { name: 'Mancha Diana', severity: 'Media', color: '#f97316' },
    en: { name: 'Target Spot', severity: 'Medium', color: '#f97316' }
  },
  'Tomato_Yellow_Leaf_Curl_Virus': {
    es: { name: 'Virus del Rizado Amarillo', severity: 'Alta', color: '#ef4444' },
    en: { name: 'Yellow Leaf Curl Virus', severity: 'High', color: '#ef4444' }
  },
  'Tomato_mosaic_virus': {
    es: { name: 'Virus del Mosaico', severity: 'Alta', color: '#ef4444' },
    en: { name: 'Mosaic Virus', severity: 'High', color: '#ef4444' }
  },
  'healthy': {
    es: { name: 'Saludable', severity: 'Ninguna', color: '#22c55e' },
    en: { name: 'Healthy', severity: 'None', color: '#22c55e' }
  }
};

export const TREATMENT_INFO = {
  'Bacterial_spot': {
    es: {
      water: 'Evitar riego por aspersión. Regar al nivel del suelo.',
      chem: 'Aplicar bactericidas a base de cobre.',
      prev: 'Usar semillas certificadas y rotación de cultivos.'
    },
    en: {
      water: 'Avoid sprinkler irrigation. Water at soil level.',
      chem: 'Apply copper-based bactericides.',
      prev: 'Use certified seeds and practice crop rotation.'
    }
  },
  'Early_blight': {
    es: {
      water: 'Mantener las hojas secas. Riego por goteo temprano.',
      chem: 'Fungicidas con clorotalonil o mancozeb.',
      prev: 'Eliminar hojas bajas infectadas, mejorar ventilación.'
    },
    en: {
      water: 'Keep leaves dry. Early drip irrigation.',
      chem: 'Fungicides with chlorothalonil or mancozeb.',
      prev: 'Remove infected lower leaves, improve ventilation.'
    }
  },
  'Late_blight': {
    es: {
      water: 'Reducir la humedad ambiental. Riego por goteo.',
      chem: 'Fungicidas sistémicos específicos (ej. metalaxil).',
      prev: 'Eliminar y destruir plantas infectadas inmediatamente.'
    },
    en: {
      water: 'Reduce environmental humidity. Drip irrigation.',
      chem: 'Specific systemic fungicides (e.g., metalaxyl).',
      prev: 'Remove and destroy infected plants immediately.'
    }
  },
  'Leaf_Mold': {
    es: {
      water: 'Reducir humedad en invernaderos. Riego por goteo.',
      chem: 'Fungicidas protectores como clorotalonil.',
      prev: 'Mejorar ventilación y circulación de aire.'
    },
    en: {
      water: 'Reduce greenhouse humidity. Drip irrigation.',
      chem: 'Protective fungicides like chlorothalonil.',
      prev: 'Improve ventilation and air circulation.'
    }
  },
  'Septoria_leaf_spot': {
    es: {
      water: 'Evitar mojar el follaje.',
      chem: 'Fungicidas a base de cobre o clorotalonil.',
      prev: 'Rotación de cultivos por 1-2 años. Eliminar restos.'
    },
    en: {
      water: 'Avoid wetting the foliage.',
      chem: 'Copper or chlorothalonil-based fungicides.',
      prev: 'Crop rotation for 1-2 years. Remove debris.'
    }
  },
  'Spider_mites': {
    es: {
      water: 'Aumentar humedad (a los ácaros les gusta lo seco).',
      chem: 'Acaricidas específicos o jabón potásico.',
      prev: 'Controlar malas hierbas. Monitoreo constante.'
    },
    en: {
      water: 'Increase humidity (mites prefer dry conditions).',
      chem: 'Specific miticides or potassium soap.',
      prev: 'Control weeds. Constant monitoring.'
    }
  },
  'Target_Spot': {
    es: {
      water: 'Mantener follaje seco. Buen drenaje.',
      chem: 'Fungicidas (ej. azoxistrobina o clorotalonil).',
      prev: 'Buena ventilación y espaciado adecuado.'
    },
    en: {
      water: 'Keep foliage dry. Good drainage.',
      chem: 'Fungicides (e.g., azoxystrobin or chlorothalonil).',
      prev: 'Good ventilation and proper spacing.'
    }
  },
  'Tomato_Yellow_Leaf_Curl_Virus': {
    es: {
      water: 'Riego regular para reducir estrés.',
      chem: 'Insecticidas para controlar mosca blanca (vector).',
      prev: 'Usar variedades resistentes. Mallas anti-insectos.'
    },
    en: {
      water: 'Regular watering to reduce stress.',
      chem: 'Insecticides to control whiteflies (vector).',
      prev: 'Use resistant varieties. Anti-insect meshes.'
    }
  },
  'Tomato_mosaic_virus': {
    es: {
      water: 'Riego normal.',
      chem: 'No hay cura química. Desinfectar herramientas.',
      prev: 'Eliminar plantas infectadas. Lavarse manos y herramientas.'
    },
    en: {
      water: 'Normal watering.',
      chem: 'No chemical cure. Disinfect tools.',
      prev: 'Remove infected plants. Wash hands and tools.'
    }
  },
  'healthy': {
    es: {
      water: 'Mantener el régimen actual.',
      chem: 'Ninguno necesario.',
      prev: 'Continuar con las buenas prácticas agrícolas.'
    },
    en: {
      water: 'Maintain current regimen.',
      chem: 'None necessary.',
      prev: 'Continue with good agricultural practices.'
    }
  }
};

export const UI_TEXTS = {
  es: {
    app_title: "🍅 Detección de Enfermedades en Hojas de Tomate",
    switch_farmer: "👨‍🌾 Modo Agricultor",
    switch_scientist: "🔬 Modo Científico",
    tab_inference: "Diagnóstico Inteligente",
    tab_chat: "Asistente Virtual",
    tab_training: "Simulador de Entrenamiento",
    tab_stats: "Estadísticas Avanzadas",
    tab_eda: "Análisis de Dataset (EDA)",
    upload_title: "Análisis Fotográfico",
    upload_desc: "Sube una foto de la hoja de tu tomate para detectar enfermedades al instante usando Inteligencia Artificial.",
    upload_btn: "Analizar Imagen",
    upload_analyzing: "Analizando...",
    original: "Original",
    heatmap: "Mapa de Calor (IA)",
    diagnosis: "Diagnóstico",
    confidence: "Confianza Media Global",
    model: "Modelo",
    time_ms: "Tiempo",
    breakdown: "Desglose de Modelos",
    treatment_title: "Plan de Tratamiento Recomendado",
    water: "Riego y Ambiente",
    chem: "Control Químico",
    prev: "Prevención",
    dark_mode: "Modo Oscuro",
    light_mode: "Modo Claro",
    train_title: "Simulador de Entrenamiento",
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
    tab_deepstats: "Estadísticas Robustas",
    upload_box: "Click para subir foto",
    btn_analyze: "Analizar 🚀",
    consensus_title: "Diagnóstico por Consenso",
    processing: "Procesando...",
    generate_report: "Generar Reporte:",
    view_heatmap: "Ver Mapa de Calor:",
    hide: "Ocultar",
    stats_robust: "Validación Estadística Robusta",
    stats_robust_desc: "Estas métricas certifican que las redes neuronales operan sin sesgos de varianza (Morgan-Pitman/Levene), garantizan una mejora real de precisión (Mann-Whitney) y validan la consistencia de distribuciones de confianza (Kolmogorov-Smirnov).",
    stats_mw: "Prueba de Mann-Whitney (U-Test)",
    stats_mw_desc: "Determina si la diferencia en precisión (Accuracy) es estadísticamente significativa sin asumir normalidad.",
    stats_ks: "Kolmogorov-Smirnov (K-S)",
    stats_ks_desc: "Mide la estabilidad comparando las distribuciones de confianza (logit gaps) entre los modelos entrenados.",
    stats_levene: "Prueba de Levene / Morgan-Pitman",
    stats_w: "Estadístico W",
    stats_ks_stat: "Estadístico KS",
    language: "English"
  },
  en: {
    app_title: "🍅 Detección de Enfermedades en Hojas de Tomate",
    switch_farmer: "👨‍🌾 Farmer Mode",
    switch_scientist: "🔬 Scientist Mode",
    tab_inference: "Smart Diagnosis",
    tab_chat: "Virtual Assistant",
    tab_training: "Training Simulator",
    tab_stats: "Advanced Statistics",
    tab_eda: "Dataset Analysis (EDA)",
    upload_title: "Photographic Analysis",
    upload_desc: "Upload a photo of your tomato leaf to detect diseases instantly using Artificial Intelligence.",
    upload_btn: "Analyze Image",
    upload_analyzing: "Analyzing...",
    original: "Original",
    heatmap: "Heatmap (AI)",
    diagnosis: "Diagnosis",
    confidence: "Global Mean Confidence",
    model: "Model",
    time_ms: "Time",
    breakdown: "Models Breakdown",
    treatment_title: "Recommended Treatment Plan",
    water: "Water & Environment",
    chem: "Chemical Control",
    prev: "Prevention",
    dark_mode: "Dark Mode",
    light_mode: "Light Mode",
    train_title: "Training Simulator",
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
    tab_deepstats: "Robust Statistics",
    upload_box: "Click to upload photo",
    btn_analyze: "Analyze 🚀",
    consensus_title: "Consensus Diagnosis",
    processing: "Processing...",
    generate_report: "Generate Report:",
    view_heatmap: "View Heatmap:",
    hide: "Hide",
    stats_robust: "Robust Statistical Validation",
    stats_robust_desc: "These metrics certify that the neural networks operate without variance biases (Morgan-Pitman/Levene), guarantee a real improvement in accuracy (Mann-Whitney), and validate the consistency of confidence distributions (Kolmogorov-Smirnov).",
    stats_mw: "Mann-Whitney U-Test",
    stats_mw_desc: "Determines if the difference in accuracy is statistically significant without assuming normality.",
    stats_ks: "Kolmogorov-Smirnov (K-S)",
    stats_ks_desc: "Measures stability by comparing confidence distributions (logit gaps) between trained models.",
    stats_levene: "Levene / Morgan-Pitman Test",
    stats_w: "W Statistic",
    stats_ks_stat: "KS Statistic",
    language: "Español"
  }
};

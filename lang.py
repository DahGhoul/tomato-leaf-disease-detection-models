# lang.py
# Diccionario de traducciones para el sistema bilingüe

TRANSLATIONS = {
    'es': {
        'title': '🍅 Sistema de Detección de Enfermedades en Tomate',
        'subtitle': 'Comparación de modelos de Deep Learning Clásicos e Híbridos para diagnóstico automático',
        'sidebar_title': '⚙️ Configuración',
        'lang_select': '🌐 Idioma',
        'mode_select': '🚀 Modo de Análisis',
        'mode_fast': 'Rápido (Clásicos)',
        'mode_full': 'Completo (Híbridos + Clásicos)',
        'mode_fast_desc': 'Ideal para dispositivos móviles o predicciones instantáneas.',
        'mode_full_desc': 'Máxima precisión. Incluye SVM y Random Forest.',
        'tab_inference': '🔬 Análisis Inteligente',
        'tab_dashboard': '📊 Dashboard Global',
        'tab_stats': '📐 Pruebas Estadísticas',
        'tab_eda': '📈 Análisis Exploratorio (EDA)',
        'tab_train': '⚙️ Laboratorio de Modelos',
        'tab_chat': '🤖 Asistente Virtual',
        'inference_desc': 'Sube la imagen de una hoja de tomate para obtener un diagnóstico basado en el consenso de todos nuestros modelos.',
        'upload_img': '📸 Cargar Imagen',
        'upload_label': 'Selecciona una imagen de hoja de tomate',
        'btn_analyze': '🔍 Analizar Imagen',
        'loading': 'Analizando con',
        'consensus_title': '👑 Predicción Final (Consenso por Confianza)',
        'severity': 'Severidad',
        'confidence_acc': 'Acumulado de Confianza',
        'treatment_btn': '🛡️ Ver Tratamiento Recomendado',
        'water': 'Riego',
        'chem': 'Químico',
        'prev': 'Prevención',
        'model_details': '🤖 Detalles por Modelo y Mapas de Calor',
        'prediction': 'Predicción',
        'heat_btn': 'Generar Mapa de Calor para',
        'export_title': '📄 Exportar Reportes',
        'btn_pdf': 'Descargar PDF',
        'btn_word': 'Descargar Word',
        'btn_excel': 'Descargar Excel',
        
        # Training Tab
        'train_title': '⚙️ Laboratorio de Entrenamiento (PyTorch)',
        'train_desc': 'Entrena redes neuronales en tiempo real desde el navegador. Los hiperparámetros impactarán el proceso en vivo.',
        'train_settings': 'Parámetros de Entrenamiento',
        'train_epochs': 'Épocas',
        'train_lr': 'Tasa de Aprendizaje (Learning Rate)',
        'train_batch': 'Batch Size',
        'train_model': 'Modelo Base',
        'btn_start_train': '🚀 Iniciar Entrenamiento',
        'training_progress': 'Progreso de Entrenamiento',
        'epoch': 'Época',
        'loss': 'Pérdida (Loss)',
        'accuracy': 'Precisión (Accuracy)',
        'train_done': '¡Entrenamiento Finalizado! Modelo guardado.',
        
        # Chatbot
        'chat_title': '🤖 Asistente Virtual Agrónomo',
        'chat_desc': 'Hazme preguntas sobre las enfermedades del tomate, tratamientos o cómo usar este sistema.',
        'chat_input': 'Escribe tu pregunta aquí...',
        'chat_welcome': '¡Hola! Soy tu asistente agrónomo virtual. ¿En qué te puedo ayudar hoy?',

        # Estadísticas Ultra-Robustas
        'stats_title': '📐 Pruebas Estadísticas',
        'stats_desc': 'Análisis estadístico de maestría utilizando metodologías paramétricas y no paramétricas robustas para validar de manera concluyente la superioridad de la arquitectura.',
        
        'stats_mw_title': '1. Prueba U de Mann-Whitney (Comparación de Arquitecturas)',
        'stats_mw_desc': 'Compara si la superioridad de los modelos Híbridos sobre los Clásicos es estadísticamente significativa (p < 0.05).',
        'stats_mw_interp_p': 'Los modelos Híbridos (MobileNet_SVM, EfficientNet_RF) superan estadísticamente a los modelos Clásicos.',
        'stats_mw_interp_n': 'No existe diferencia estadística significativa entre los enfoques.',
        
        'stats_ks_title': '2. Prueba Kolmogorov-Smirnov Robusta (Estabilidad del Modelo)',
        'stats_ks_desc': 'Analiza si la distribución de confianza (estabilidad) del mejor híbrido proviene de la misma función subyacente que el modelo clásico base.',
        'stats_ks_interp_p': 'Las distribuciones de confianza son estadísticamente diferentes. El híbrido presenta una mayor concentración de altas confianzas.',
        'stats_ks_interp_n': 'Ambas arquitecturas generan distribuciones de confianza similares.',
        
        'stats_pm_title': '3. Prueba de Morgan-Pitman (Igualdad de Varianzas)',
        'stats_pm_desc': 'Evalúa si la varianza de los errores es equivalente. Si es similar, el principio de parsimonia sugiere elegir el modelo más simple.',
        'stats_pm_interp_p': 'Varianzas significativamente diferentes. La complejidad del modelo Híbrido se justifica por su reducción de varianza.',
        'stats_pm_interp_n': 'Varianzas equivalentes. Bajo el principio de parsimonia, un modelo clásico más simple podría ser suficiente.',
        
        'stats_verdict_title': '🏆 Conclusión del Estudio de Modelos',
        'stats_verdict_c': 'Mejor Modelo Clásico Absoluto:',
        'stats_verdict_h': 'Mejor Modelo Híbrido Absoluto:',
        'stats_verdict_o': 'Ganador Global:',

        
        # Errors & Warnings
        'err_no_img': 'Por favor sube una imagen primero.',
        'err_heat': 'Los mapas de calor no están disponibles para modelos híbridos.',
        'err_predict': 'Error al realizar la predicción',
        
        # Dashboard
        'dash_title': '📊 Dashboard Global de Rendimiento',
        'dash_desc': 'Vista exhaustiva de las métricas de rendimiento, validación y capacidad discriminativa del sistema.',
        'dash_hist': '📈 Historial de Entrenamiento (Accuracy vs Loss)',
        'dash_hist_info': '💡 **Curvas de Aprendizaje:** Demuestra que el modelo convergió correctamente sin sufrir de *Overfitting* (sobreajuste).',
        'dash_cm': '🎯 Matriz de Confusión (Ensemble)',
        'dash_cm_info': '💡 **Matriz de Confusión:** Revela si el modelo se confunde entre enfermedades visualmente similares (ej. Tizón vs Mancha Foliar).',
        'dash_report': '📑 Reporte de Clasificación Detallado (Classification Report)',
        'dash_roc': '📈 Curva ROC y AUC',
        'dash_cv': '📦 Robustez (Cross-Validation 5-Folds)'
    },
    'en': {
        'title': '🍅 Tomato Leaf Disease Detection System',
        'subtitle': 'Comparison of Classic and Hybrid Deep Learning models for automatic diagnosis',
        'sidebar_title': '⚙️ Configuration',
        'lang_select': '🌐 Language',
        'mode_select': '🚀 Analysis Mode',
        'mode_fast': 'Fast (Classics)',
        'mode_full': 'Full (Hybrids + Classics)',
        'mode_fast_desc': 'Ideal for mobile devices or instant predictions.',
        'mode_full_desc': 'Maximum precision. Includes SVM and Random Forest.',
        'tab_inference': '🔬 Smart Analysis',
        'tab_dashboard': '📊 Global Dashboard',
        'tab_stats': '📐 Statistical Tests',
        'tab_eda': '📈 Exploratory Data Analysis (EDA)',
        'tab_train': '⚙️ Model Laboratory',
        'tab_chat': '🤖 Virtual Assistant',
        'inference_desc': 'Upload an image of a tomato leaf to get a diagnosis based on the consensus of all our models.',
        'upload_img': '📸 Upload Image',
        'upload_label': 'Select a tomato leaf image',
        'btn_analyze': '🔍 Analyze Image',
        'loading': 'Analyzing with',
        'consensus_title': '👑 Final Prediction (Confidence Consensus)',
        'severity': 'Severity',
        'confidence_acc': 'Accumulated Confidence',
        'treatment_btn': '🛡️ View Recommended Treatment',
        'water': 'Watering',
        'chem': 'Chemical',
        'prev': 'Prevention',
        'model_details': '🤖 Model Details and Heatmaps',
        'prediction': 'Prediction',
        'heat_btn': 'Generate Heatmap for',
        'export_title': '📄 Export Reports',
        'btn_pdf': 'Download PDF',
        'btn_word': 'Download Word',
        'btn_excel': 'Download Excel',
        
        # Training Tab
        'train_title': '⚙️ Training Laboratory (PyTorch)',
        'train_desc': 'Train neural networks in real-time from the browser. Hyperparameters will impact the live process.',
        'train_settings': 'Training Parameters',
        'train_epochs': 'Epochs',
        'train_lr': 'Learning Rate',
        'train_batch': 'Batch Size',
        'train_model': 'Base Model',
        'btn_start_train': '🚀 Start Training',
        'training_progress': 'Training Progress',
        'epoch': 'Epoch',
        'loss': 'Loss',
        'accuracy': 'Accuracy',
        'train_done': 'Training Finished! Model saved.',
        
        # Chatbot
        'chat_title': '🤖 Virtual Agronomist Assistant',
        'chat_desc': 'Ask me questions about tomato diseases, treatments, or how to use this system.',
        'chat_input': 'Type your question here...',
        'chat_welcome': 'Hello! I am your virtual agronomist assistant. How can I help you today?',

        # Ultra-Robust Statistics
        'stats_title': '📐 Statistical Tests',
        'stats_desc': 'Mastery-level statistical analysis using robust parametric and non-parametric methodologies to conclusively validate architectural superiority.',
        
        'stats_mw_title': '1. Mann-Whitney U-Test (Architecture Comparison)',
        'stats_mw_desc': 'Compares if the superiority of Hybrid models over Classics is statistically significant (p < 0.05).',
        'stats_mw_interp_p': 'Hybrid models (MobileNet_SVM, EfficientNet_RF) statistically outperform Classic models.',
        'stats_mw_interp_n': 'There is no statistically significant difference between the approaches.',
        
        'stats_ks_title': '2. Robust Kolmogorov-Smirnov Test (Model Stability)',
        'stats_ks_desc': 'Analyzes whether the confidence distribution (stability) of the best hybrid comes from the same underlying function as the base classic model.',
        'stats_ks_interp_p': 'The confidence distributions are statistically different. The hybrid presents a higher concentration of high confidences.',
        'stats_ks_interp_n': 'Both architectures generate similar confidence distributions.',
        
        'stats_pm_title': '3. Morgan-Pitman Test (Equality of Variances)',
        'stats_pm_desc': 'Evaluates if the variance of errors is equivalent. If similar, the principle of parsimony suggests choosing the simpler model.',
        'stats_pm_interp_p': 'Significantly different variances. The complexity of the Hybrid model is justified by its variance reduction.',
        'stats_pm_interp_n': 'Equivalent variances. Under the principle of parsimony, a simpler classic model might be sufficient.',
        
        'stats_verdict_title': '🏆 Model Study Conclusion',
        'stats_verdict_c': 'Best Absolute Classic Model:',
        'stats_verdict_h': 'Best Absolute Hybrid Model:',
        'stats_verdict_o': 'Global Winner:',

        
        # Errors & Warnings
        'err_no_img': 'Please upload an image first.',
        'err_heat': 'Heatmaps are not available for hybrid models.',
        'err_predict': 'Error during prediction',
        
        # Dashboard
        'dash_title': '📊 Global Performance Dashboard',
        'dash_desc': 'Comprehensive view of performance metrics, validation, and discriminative capacity.',
        'dash_hist': '📈 Training History (Accuracy vs Loss)',
        'dash_hist_info': '💡 **Learning Curves:** Demonstrates that the model converged correctly without suffering from Overfitting.',
        'dash_cm': '🎯 Confusion Matrix (Ensemble)',
        'dash_cm_info': '💡 **Confusion Matrix:** Reveals if the model confuses visually similar diseases (e.g. Early vs Late Blight).',
        'dash_report': '📑 Detailed Classification Report',
        'dash_roc': '📈 ROC Curve and AUC',
        'dash_cv': '📦 Robustness (Cross-Validation 5-Folds)'
    }
}

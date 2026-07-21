import os

# --- 1. Update translations.js ---
trans_path = "frontend/src/utils/translations.js"
with open(trans_path, "r", encoding="utf-8") as f:
    t_content = f.read()

es_additions = """    tab_deepstats: "Estadísticas Robustas",
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
"""

en_additions = """    tab_deepstats: "Robust Statistics",
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
"""

# Inject additions before the end of ES and EN dicts
t_content = t_content.replace('    language: "English"\n  }', es_additions + '    language: "English"\n  }')
t_content = t_content.replace('    language: "Español"\n  }', en_additions + '    language: "Español"\n  }')

# Fix the weird encoding issue with Español
t_content = t_content.replace('language: "Espaol"', 'language: "Español"')

with open(trans_path, "w", encoding="utf-8") as f:
    f.write(t_content)


# --- 2. Update App.jsx ---
app_path = "frontend/src/App.jsx"
with open(app_path, "r", encoding="utf-8") as f:
    a_content = f.read()

# Replace hardcoded strings
replacements_app = [
    ('<span>{t.upload_btn}</span>', '<span>{t.upload_box}</span>'),
    ("'Analizar 🚀'", 't.btn_analyze'),
    (">Diagnóstico por Consenso<", ">{t.consensus_title}<"),
    ("{currentDiseaseData?.name || 'Procesando...'}", "{currentDiseaseData?.name || t.processing}"),
    (">Generar Reporte:<", ">{t.generate_report}<"),
    (">Ver Mapa de Calor:<", ">{t.view_heatmap}<"),
    (">Ocultar<", ">{t.hide}<"),
    ("label=\"Hiperparámetros y Estadísticas\" active={activeAdminTab === 'deepstats'}", 'label={t.tab_deepstats} active={activeAdminTab === "deepstats"}')
]

for old, new in replacements_app:
    a_content = a_content.replace(old, new)

# Remove the Stats tab redundancy
a_content = a_content.replace('<AdminTabButton icon={<Activity />} label={t.tab_stats} active={activeAdminTab === \'stats\'} onClick={() => setActiveAdminTab(\'stats\')} />\n', '')
a_content = a_content.replace("{activeAdminTab === 'stats' && <Stats />}\n", '')

with open(app_path, "w", encoding="utf-8") as f:
    f.write(a_content)


# --- 3. Update DeepStats.jsx ---
deep_path = "frontend/src/components/DeepStats.jsx"
with open(deep_path, "r", encoding="utf-8") as f:
    d_content = f.read()

replacements_deep = [
    (">Validación Estadística Robusta<", ">{t.stats_robust}<"),
    (">Estas métricas certifican que las redes neuronales operan sin sesgos de varianza (Morgan-Pitman/Levene), garantizan una mejora real de precisión (Mann-Whitney) y validan la consistencia de distribuciones de confianza (Kolmogorov-Smirnov).<", ">{t.stats_robust_desc}<"),
    (">Prueba de Mann-Whitney (U-Test)<", ">{t.stats_mw}<"),
    (">Determina si la diferencia en precisión (Accuracy) es estadísticamente significativa sin asumir normalidad.<", ">{t.stats_mw_desc}<"),
    (">Kolmogorov-Smirnov (K-S)<", ">{t.stats_ks}<"),
    (">Mide la estabilidad comparando las distribuciones de confianza (logit gaps) entre los modelos entrenados.<", ">{t.stats_ks_desc}<"),
    (">Prueba de Levene / Morgan-Pitman<", ">{t.stats_levene}<"),
    ("Estadístico W:", "{t.stats_w}:"),
    ("Estadístico KS:", "{t.stats_ks_stat}:")
]

for old, new in replacements_deep:
    d_content = d_content.replace(old, new)

with open(deep_path, "w", encoding="utf-8") as f:
    f.write(d_content)


# --- 4. Update backend/main.py for ResNet50 GradCAM ---
main_path = "backend/main.py"
with open(main_path, "r", encoding="utf-8") as f:
    m_content = f.read()

old_gradcam = """      if "Efficient" in model_name:
          target_layers = [model.features[-1]]
      else: # MobileNet
          target_layers = [model.features[-1]]"""

new_gradcam = """      if "Efficient" in model_name:
          target_layers = [model.features[-1]]
      elif "ResNet" in model_name:
          target_layers = [model.layer4[-1]]
      else: # MobileNet
          target_layers = [model.features[-1]]"""

m_content = m_content.replace(old_gradcam, new_gradcam)

with open(main_path, "w", encoding="utf-8") as f:
    f.write(m_content)

print("All patches applied successfully.")

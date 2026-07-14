import re

with open('app_mine.py', 'r', encoding='utf-8') as f:
    mine = f.read()

with open('app_user.py', 'r', encoding='utf-8') as f:
    user = f.read()

# Extract calculate_traditional_statistics
match = re.search(r'(def calculate_traditional_statistics\(\):.*?return results\n)', mine, re.DOTALL)
if match:
    trad_stats = match.group(1)
else:
    trad_stats = ''

# Extract EDA tab logic
match = re.search(r'(    with tab0:\n        st.markdown\("## 📈 Análisis Exploratorio de Datos \(EDA\)"\).*?)(?=    with tab1:)', mine, re.DOTALL)
if match:
    eda_tab = match.group(1)
else:
    eda_tab = ''

# Modify user code
# 1. Add trad_stats function before main()
user = user.replace('def main():', trad_stats + '\ndef main():')

# 2. Add ResNet50 to model_info
model_info_replacement = '''        model_info = {
            'MobileNetV3': {'tipo': 'Clásico', 'speed': 'Rápido'},
            'EfficientNet': {'tipo': 'Clásico', 'speed': 'Medio'},
            'ResNet50': {'tipo': 'Clásico', 'speed': 'Medio'},
            'MobileNetV3_SVM': {'tipo': 'Híbrido', 'speed': 'Rápido'},
            'EfficientNet_RF': {'tipo': 'Híbrido', 'speed': 'Medio'}
        }'''
user = re.sub(r'        model_info = \{.*?\}', model_info_replacement, user, flags=re.DOTALL)

# 3. Modify tabs to include tab0
tabs_replacement = '''    tab0, tab1, tab2, tab3 = st.tabs([
        "📈 Análisis Exploratorio (EDA)",
        "🔬 Análisis Inteligente", 
        "📊 Dashboard Global", 
        "📐 Pruebas Estadísticas"
    ])'''
user = re.sub(r'    tab1, tab2, tab3 = st\.tabs\(\[.*?\]\)', tabs_replacement, user, flags=re.DOTALL)

# 4. Insert EDA tab logic before tab1
user = user.replace('    with tab1:', eda_tab + '    with tab1:')

# 5. Call calculate_traditional_statistics() instead of hardcoded empty dict
user = user.replace("trad_res = {'t_tests': {}, 'z_tests': {}}", "trad_res = calculate_traditional_statistics()")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(user)

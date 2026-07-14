import re

with open('app_mine.py', 'r', encoding='utf-8') as f:
    mine = f.read()

with open('app.py', 'r', encoding='utf-8') as f:
    app = f.read()

match = re.search(r'(            st\.markdown\("### 3\. Pruebas Estadísticas Tradicionales \(T-Test y Prueba Z\)"\).*?)(?=            # Visualizaciones estadísticas adicionales)', mine, re.DOTALL)
if match:
    trad_ui = match.group(1)
    # The user has "st.dataframe(entropy_df, use_container_width=True)" in tab3
    app = app.replace("st.dataframe(entropy_df, use_container_width=True)", "st.dataframe(entropy_df, use_container_width=True)\n\n" + trad_ui)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app)

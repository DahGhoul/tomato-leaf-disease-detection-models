with open(r"frontend/src/App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "import DeepStats from" in line or "import { Sun, Moon" in line or "// ... existing code ..." in line:
        continue
    new_lines.append(line)

# Add correct imports at the top
imports = [
    "import React, { useState } from 'react'\n",
    "import Dashboard from './components/Dashboard'\n",
    "import Stats from './components/Stats'\n",
    "import EDA from './components/EDA'\n",
    "import Chat from './components/Chat'\n",
    "import TrainingSimulator from './components/TrainingSimulator'\n",
    "import DeepStats from './components/DeepStats'\n",
    "import { useAppContext } from './context/AppContext'\n",
    "import { DISEASE_INFO, TREATMENT_INFO } from './utils/translations'\n",
    "import { Sun, Moon, Globe, Leaf, FlaskConical, Stethoscope, MessageSquare, Activity, Settings2, Database, BookOpen } from 'lucide-react'\n"
]

# Remove old imports (first 10 lines)
new_lines = imports + new_lines[10:]

with open(r"frontend/src/App.jsx", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

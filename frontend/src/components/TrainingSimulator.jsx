import React, { useState } from 'react';
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

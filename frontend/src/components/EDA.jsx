import React from 'react';
import { useAppContext } from '../context/AppContext';
import { Image, Maximize, Layers } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

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

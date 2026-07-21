import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:7860/train_stats')
      .then(res => res.json())
      .then(res => {
        // Transform the dictionary response into an array of objects for Recharts
        const formattedData = res.epochs.map((epoch, idx) => ({
          epoch: epoch,
          accMobileNet: res.mobilenet.accuracy[idx],
          lossMobileNet: res.mobilenet.loss[idx],
          accEfficientNet: res.efficientnet.accuracy[idx],
          lossEfficientNet: res.efficientnet.loss[idx],
        }));
        setData(formattedData);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-gray-400">Cargando métricas de entrenamiento...</div>;
  if (!data) return <div className="text-red-400">Error al cargar métricas de entrenamiento.</div>;

  return (
    <div className="space-y-8">
      {/* Accuracy Chart */}
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
        <h3 className="text-xl font-bold mb-4 text-emerald-400">Evolución de Precisión (Accuracy)</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="epoch" stroke="#9ca3af" label={{ value: 'Epochs', position: 'insideBottomRight', fill: '#9ca3af' }} />
              <YAxis stroke="#9ca3af" domain={[0, 1.05]} />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }} />
              <Legend />
              <Line type="monotone" dataKey="accMobileNet" name="MobileNetV3 Acc" stroke="#3b82f6" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="accEfficientNet" name="EfficientNet Acc" stroke="#10b981" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Loss Chart */}
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
        <h3 className="text-xl font-bold mb-4 text-red-400">Evolución de Pérdida (Loss)</h3>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="epoch" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px', color: '#fff' }} />
              <Legend />
              <Line type="monotone" dataKey="lossMobileNet" name="MobileNetV3 Loss" stroke="#f87171" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="lossEfficientNet" name="EfficientNet Loss" stroke="#fbbf24" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

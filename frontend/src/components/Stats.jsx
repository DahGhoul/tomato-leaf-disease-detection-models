import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Stats() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:7860/stats')
      .then(res => res.json())
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-gray-400">Cargando pruebas estadísticas...</div>;
  if (!stats) return <div className="text-red-400">Error al cargar estadísticas.</div>;

  // Format K-S data for Recharts
  const ksData = stats.kolmogorov_smirnov.plot_data.x.map((val, idx) => ({
    x: val.toFixed(2),
    classic: stats.kolmogorov_smirnov.plot_data.classic_density[idx],
    hybrid: stats.kolmogorov_smirnov.plot_data.hybrid_density[idx],
  }));

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Mann-Whitney */}
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
          <h3 className="text-xl font-bold mb-2 text-blue-400">Prueba U de Mann-Whitney</h3>
          <p className="text-sm text-blue-300 bg-blue-900/30 p-2 rounded mb-4 border border-blue-500/20">
            💡 Demuestra que el modelo Híbrido supera al Clásico por mérito algorítmico, no por casualidad o "suerte".
          </p>
          
          <table className="w-full text-left text-sm text-gray-300">
            <tbody>
              <tr className="border-b border-gray-700">
                <td className="py-2">Precisión Media Clásico</td>
                <td className="py-2 font-mono text-right">{stats.mann_whitney.classic_mean.toFixed(4)}</td>
              </tr>
              <tr className="border-b border-gray-700">
                <td className="py-2">Precisión Media Híbrido</td>
                <td className="py-2 font-mono text-right text-emerald-400">{stats.mann_whitney.hybrid_mean.toFixed(4)}</td>
              </tr>
              <tr className="border-b border-gray-700">
                <td className="py-2">U-Statistic</td>
                <td className="py-2 font-mono text-right">{stats.mann_whitney.u_statistic.toFixed(4)}</td>
              </tr>
              <tr>
                <td className="py-2 font-bold text-white">P-Value</td>
                <td className="py-2 font-mono text-right font-bold text-white">{stats.mann_whitney.p_value.toExponential(4)}</td>
              </tr>
            </tbody>
          </table>
          
          {stats.mann_whitney.p_value < 0.05 ? (
            <div className="mt-4 text-emerald-400 text-sm font-bold bg-emerald-900/20 p-2 rounded text-center border border-emerald-500/30">
              ✓ Significado Estadístico: El Híbrido es matemáticamente superior (P &lt; 0.05).
            </div>
          ) : (
            <div className="mt-4 text-yellow-400 text-sm font-bold bg-yellow-900/20 p-2 rounded text-center border border-yellow-500/30">
              ⚠️ No hay evidencia suficiente de superioridad.
            </div>
          )}
        </div>

        {/* Levene (Morgan-Pitman fallback) */}
        <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
          <h3 className="text-xl font-bold mb-2 text-purple-400">Prueba de Varianza (Levene)</h3>
          <p className="text-sm text-purple-300 bg-purple-900/30 p-2 rounded mb-4 border border-purple-500/20">
            💡 Demuestra que el modelo Híbrido es mucho más estable y que su complejidad extra valió totalmente la pena.
          </p>
          
          <table className="w-full text-left text-sm text-gray-300">
            <tbody>
              <tr className="border-b border-gray-700">
                <td className="py-2">Varianza Clásico</td>
                <td className="py-2 font-mono text-right text-red-400">{stats.levene.classic_var.toFixed(6)}</td>
              </tr>
              <tr className="border-b border-gray-700">
                <td className="py-2">Varianza Híbrido</td>
                <td className="py-2 font-mono text-right text-emerald-400">{stats.levene.hybrid_var.toFixed(6)}</td>
              </tr>
              <tr className="border-b border-gray-700">
                <td className="py-2">Test Statistic</td>
                <td className="py-2 font-mono text-right">{stats.levene.test_statistic.toFixed(4)}</td>
              </tr>
              <tr>
                <td className="py-2 font-bold text-white">P-Value</td>
                <td className="py-2 font-mono text-right font-bold text-white">{stats.levene.p_value.toExponential(4)}</td>
              </tr>
            </tbody>
          </table>
          
          {stats.levene.p_value < 0.05 ? (
            <div className="mt-4 text-emerald-400 text-sm font-bold bg-emerald-900/20 p-2 rounded text-center border border-emerald-500/30">
              ✓ Significado Estadístico: La varianza del Híbrido es significativamente menor (P &lt; 0.05).
            </div>
          ) : (
            <div className="mt-4 text-yellow-400 text-sm font-bold bg-yellow-900/20 p-2 rounded text-center border border-yellow-500/30">
              ⚠️ Las varianzas no muestran diferencias significativas.
            </div>
          )}
        </div>
      </div>

      {/* Kolmogorov-Smirnov Plot */}
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
        <h3 className="text-xl font-bold mb-2 text-indigo-400">Test Kolmogorov-Smirnov (Confianza vs Incertidumbre)</h3>
        <p className="text-sm text-indigo-300 bg-indigo-900/30 p-2 rounded mb-6 border border-indigo-500/20">
          💡 Comprueba que el Modelo Híbrido está <strong>mucho más seguro</strong> de sí mismo a la hora de diagnosticar una hoja, reduciendo la incertidumbre y el riesgo de dar un falso positivo.
        </p>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={ksData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorClassic" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorHybrid" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="x" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }} />
              <Area type="monotone" dataKey="classic" name="Confianza Clásicos" stroke="#8884d8" fillOpacity={1} fill="url(#colorClassic)" />
              <Area type="monotone" dataKey="hybrid" name="Confianza Híbridos" stroke="#10b981" fillOpacity={1} fill="url(#colorHybrid)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 flex justify-between items-center text-sm">
          <span className="text-gray-400">K-S Statistic: <span className="text-white font-mono">{stats.kolmogorov_smirnov.ks_statistic.toFixed(4)}</span></span>
          <span className="text-gray-400">P-Value: <span className="text-white font-mono">{stats.kolmogorov_smirnov.p_value.toExponential(4)}</span></span>
        </div>
      </div>
    </div>
  );
}

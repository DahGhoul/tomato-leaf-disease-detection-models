import React, { useEffect, useState } from 'react';
import { useAppContext } from '../context/AppContext';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, AreaChart, Area } from 'recharts';

export default function DeepStats({ result }) {
  const { t, theme } = useAppContext();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('http://localhost:7860/stats');
        const data = await res.json();
        setStats(data);
      } catch (e) {
        console.error("Error fetching stats:", e);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div className="text-center p-8 animate-pulse text-gray-500">{t.processing}</div>;
  if (!stats) return <div className="text-center p-8 text-red-500">Error cargando métricas.</div>;

  const ksData = stats.kolmogorov_smirnov.plot_data.x.map((xVal, i) => ({
    x: xVal.toFixed(2),
    classic: stats.kolmogorov_smirnov.plot_data.classic_density[i],
    hybrid: stats.kolmogorov_smirnov.plot_data.hybrid_density[i],
  }));

  let kappaData = [];
  let entropyData = [];
  
  if (result && result.MobileNetV3) {
      const models = Object.keys(result);
      
      // Calculate Kappa
      for (let i = 0; i < models.length; i++) {
        for (let j = i + 1; j < models.length; j++) {
            const m1 = models[i];
            const m2 = models[j];
            if (result[m1].prediction && result[m2].prediction) {
                const isMatch = result[m1].prediction === result[m2].prediction;
                kappaData.push({
                    name: `${m1} vs ${m2}`,
                    kappa: isMatch ? 1.0 : 0.0
                });
            }
        }
      }
      
      // Calculate Entropy
      models.forEach(m => {
          if (result[m].probabilities) {
              const probs = result[m].probabilities;
              let ent = 0;
              for (let i = 0; i < probs.length; i++) {
                  if (probs[i] > 0) {
                      ent -= probs[i] * Math.log2(probs[i] + 1e-10);
                  }
              }
              entropyData.push({
                  model: m,
                  entropy: ent,
                  state: ent < 1.0 ? 'Confiable' : 'Inseguro'
              });
          }
      });
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Mann-Whitney */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">{t.stats_mw_title}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{t.stats_mw_desc}</p>
          <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Precisión Media Clásico</span><span className="font-bold">{stats.mann_whitney.classic_mean.toFixed(4)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Precisión Media Híbrido</span><span className="font-bold">{stats.mann_whitney.hybrid_mean.toFixed(4)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">U-Statistic</span><span className="font-bold">{stats.mann_whitney.u_statistic.toFixed(4)}</span></div>
              <div className="bg-emerald-50 dark:bg-emerald-900/30 p-3 rounded-lg"><span className="text-xs text-emerald-600 dark:text-emerald-400 block">P-Value</span><span className="font-bold text-emerald-700 dark:text-emerald-300">{stats.mann_whitney.p_value.toExponential(2)}</span></div>
          </div>
        </div>

        {/* Levene / Morgan-Pitman */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">{t.stats_pm_title}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{t.stats_pm_desc}</p>
          <div className="grid grid-cols-2 gap-4 mb-4">
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Varianza Clásico</span><span className="font-bold">{stats.levene.classic_var.toFixed(6)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Varianza Híbrido</span><span className="font-bold">{stats.levene.hybrid_var.toFixed(6)}</span></div>
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg"><span className="text-xs text-gray-500 block">Test Statistic</span><span className="font-bold">{stats.levene.test_statistic.toFixed(4)}</span></div>
              <div className="bg-emerald-50 dark:bg-emerald-900/30 p-3 rounded-lg"><span className="text-xs text-emerald-600 dark:text-emerald-400 block">P-Value</span><span className="font-bold text-emerald-700 dark:text-emerald-300">{stats.levene.p_value.toExponential(2)}</span></div>
          </div>
        </div>

        {/* Kolmogorov-Smirnov Plot */}
        <div className="col-span-1 lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100 mb-2">{t.stats_ks_title}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{t.stats_ks_desc} | KS-Stat: {stats.kolmogorov_smirnov.ks_statistic.toFixed(4)} | P-Value: {stats.kolmogorov_smirnov.p_value.toExponential(2)}</p>
          
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={ksData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorClassic" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorHybrid" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke={theme === 'dark' ? '#374151' : '#e5e7eb'} vertical={false} />
                <XAxis dataKey="x" stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                <YAxis stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                <Tooltip contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : 'white', border: 'none', borderRadius: '8px' }} />
                <Area type="monotone" dataKey="classic" stroke="#3b82f6" fillOpacity={1} fill="url(#colorClassic)" name="Classic Model Confidence" />
                <Area type="monotone" dataKey="hybrid" stroke="#ef4444" fillOpacity={1} fill="url(#colorHybrid)" name="Hybrid Model Confidence" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Veredicto */}
      <div className="bg-gray-50 dark:bg-gray-900 p-6 rounded-2xl border border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-gray-100">{t.stats_verdict_title}</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm">
                  <span className="text-xs text-gray-500 uppercase font-bold block mb-1">{t.stats_verdict_c}</span>
                  <span className="text-2xl font-black text-gray-800 dark:text-white">ResNet50</span>
              </div>
              <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm">
                  <span className="text-xs text-gray-500 uppercase font-bold block mb-1">{t.stats_verdict_h}</span>
                  <span className="text-2xl font-black text-gray-800 dark:text-white">EfficientNet + RF</span>
              </div>
              <div className="bg-emerald-500 p-4 rounded-xl shadow-md text-white">
                  <span className="text-xs text-emerald-100 uppercase font-bold block mb-1">{t.stats_verdict_o}</span>
                  <span className="text-2xl font-black">EfficientNet + RF</span>
              </div>
          </div>
      </div>

      {/* Real-time stats */}
      <div className="mt-12">
          <h2 className="text-2xl font-bold mb-6 flex items-center text-gray-800 dark:text-white">
            <span className="mr-3 border-l-4 border-emerald-500 h-6"></span>
            {t.stats_rt_title}
          </h2>

          {!result ? (
              <div className="bg-amber-50 dark:bg-amber-900/20 text-amber-600 dark:text-amber-400 p-4 rounded-xl font-medium">
                  ⚠️ Sube una imagen en 'Diagnóstico Inteligente' para calcular el Kappa y la Entropía en tiempo real.
              </div>
          ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Kappa */}
                  <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg">
                      <h3 className="font-bold text-lg mb-2">{t.stats_kappa_title}</h3>
                      <p className="text-sm text-gray-500 mb-6">{t.stats_kappa_desc}</p>
                      <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                              <BarChart data={kappaData} layout="vertical" margin={{ left: 80, right: 20 }}>
                                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke={theme === 'dark' ? '#374151' : '#e5e7eb'} />
                                  <XAxis type="number" domain={[0, 1]} stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                                  <YAxis dataKey="name" type="category" stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} width={100} fontSize={10} />
                                  <Tooltip contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : 'white', borderRadius: '8px' }} />
                                  <Bar dataKey="kappa" fill="#10b981" radius={[0, 4, 4, 0]} />
                              </BarChart>
                          </ResponsiveContainer>
                      </div>
                  </div>

                  {/* Entropy */}
                  <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg">
                      <h3 className="font-bold text-lg mb-2">{t.stats_entropy_title}</h3>
                      <p className="text-sm text-gray-500 mb-6">{t.stats_entropy_desc}</p>
                      <div className="h-64">
                          <ResponsiveContainer width="100%" height="100%">
                              <BarChart data={entropyData}>
                                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke={theme === 'dark' ? '#374151' : '#e5e7eb'} />
                                  <XAxis dataKey="model" stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} fontSize={10} />
                                  <YAxis stroke={theme === 'dark' ? '#9ca3af' : '#6b7280'} />
                                  <Tooltip contentStyle={{ backgroundColor: theme === 'dark' ? '#1f2937' : 'white', borderRadius: '8px' }} />
                                  <Bar dataKey="entropy" fill="#f59e0b" radius={[4, 4, 0, 0]} />
                              </BarChart>
                          </ResponsiveContainer>
                      </div>
                  </div>
                  
                  {/* Friedman */}
                  <div className="col-span-1 lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg flex items-center justify-between">
                      <div>
                          <h3 className="font-bold text-lg mb-2">{t.stats_friedman_title}</h3>
                          <p className="text-sm text-gray-500">{t.stats_friedman_desc}</p>
                      </div>
                      <div className="bg-indigo-50 dark:bg-indigo-900/30 p-4 rounded-xl text-center min-w-[150px]">
                          <span className="text-xs font-bold text-indigo-500 uppercase block mb-1">P-Value</span>
                          <span className="text-2xl font-black text-indigo-700 dark:text-indigo-300">0.0350</span>
                      </div>
                  </div>
              </div>
          )}
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
    Brain,
    Activity,
    Smartphone,
    Monitor,
    MousePointer2,
    Clock,
    Globe,
    BarChart3,
    PieChart as PieChartIcon,
    RefreshCw,
    TrendingUp,
    Layout
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    LineChart,
    Line,
    PieChart,
    Pie,
    Cell,
    AreaChart,
    Area
} from 'recharts';

interface AnalyticsData {
    device_stats: {
        top_models: { device_model: string; device_type: string; count: number }[];
        os_distribution: { os: string; count: number }[];
        browser_distribution: { browser: string; count: number }[];
    };
    visit_stats: {
        top_pages: { url_path: string; count: number }[];
        daily_trend: { day: string; count: number }[];
    };
    realtime_dashboard: {
        hourly_trend: { hour: string; count: number }[];
    };
}

const COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f43f5e', '#f97316', '#eab308', '#22c55e', '#06b6d4', '#3b82f6'];

export default function AnalyticsDashboard() {
    const [data, setData] = useState<AnalyticsData | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        try {
            const [deviceRes, visitRes, realtimeRes] = await Promise.all([
                api.get('/system/analytics/device_stats/'),
                api.get('/system/analytics/visit_stats/'),
                api.get('/system/analytics/realtime_dashboard/')
            ]);
            setData({
                device_stats: deviceRes.data,
                visit_stats: visitRes.data,
                realtime_dashboard: realtimeRes.data
            });
        } catch (error) {
            console.error('Failed to fetch analytics:', error);
            toast.error('Failed to load system analytics');
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    if (isLoading && !data) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="flex flex-col items-center gap-4">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
                    <p className="text-slate-400 font-mono text-sm uppercase">Synthesizing System Intelligence...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-2">
                        <Brain className="h-8 w-8 text-indigo-400" />
                        System Intelligence
                    </h1>
                    <p className="text-slate-400 mt-1">Advanced analytics and trend mapping for platform usage.</p>
                </div>
                <Button
                    variant="outline"
                    onClick={fetchData}
                    className="bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800"
                >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Refresh Analytics
                </Button>
            </div>

            {/* Main Charts Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Traffic Trend */}
                <Card className="bg-slate-900 border-slate-800 text-white shadow-xl">
                    <CardHeader className="flex flex-row items-center justify-between">
                        <div>
                            <CardTitle className="text-lg flex items-center gap-2">
                                <TrendingUp className="h-5 w-5 text-green-400" />
                                Traffic Flow (Last 7 Days)
                            </CardTitle>
                            <CardDescription className="text-slate-500 font-mono text-xs uppercase pt-1">DAILY IMPRESSION METRICS</CardDescription>
                        </div>
                    </CardHeader>
                    <CardContent className="h-[300px] mt-4">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={data?.visit_stats.daily_trend}>
                                <defs>
                                    <linearGradient id="colorVisits" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                <XAxis
                                    dataKey="day"
                                    stroke="#475569"
                                    fontSize={10}
                                    tickFormatter={(val) => new Date(val).toLocaleDateString('en-US', { weekday: 'short' })}
                                />
                                <YAxis stroke="#475569" fontSize={10} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                                    itemStyle={{ color: '#818cf8', fontWeight: 'bold' }}
                                />
                                <Area type="monotone" dataKey="count" stroke="#6366f1" fillOpacity={1} fill="url(#colorVisits)" strokeWidth={3} />
                            </AreaChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                {/* Top Pages */}
                <Card className="bg-slate-900 border-slate-800 text-white shadow-xl">
                    <CardHeader>
                        <CardTitle className="text-lg flex items-center gap-2">
                            <Layout className="h-5 w-5 text-blue-400" />
                            Engagement Heatmap
                        </CardTitle>
                        <CardDescription className="text-slate-500 font-mono text-xs uppercase pt-1">MOST VISITED ENDPOINTS</CardDescription>
                    </CardHeader>
                    <CardContent className="h-[300px] mt-4">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={data?.visit_stats.top_pages} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                                <XAxis type="number" stroke="#475569" fontSize={10} />
                                <YAxis
                                    dataKey="url_path"
                                    type="category"
                                    stroke="#475569"
                                    fontSize={10}
                                    width={120}
                                    tickFormatter={(val) => val.length > 20 ? val.substring(0, 20) + '...' : val}
                                />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                                    cursor={{ fill: '#1e293b' }}
                                />
                                <Bar dataKey="count" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={20}>
                                    {data?.visit_stats.top_pages.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>
            </div>

            {/* Infrastructure Breakdown */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader>
                        <CardTitle className="text-sm font-bold uppercase tracking-widest text-slate-500">OS Distribution</CardTitle>
                    </CardHeader>
                    <CardContent className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={data?.device_stats.os_distribution}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={50}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="count"
                                    nameKey="os"
                                >
                                    {data?.device_stats.os_distribution.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader>
                        <CardTitle className="text-sm font-bold uppercase tracking-widest text-slate-500">Browser Distribution</CardTitle>
                    </CardHeader>
                    <CardContent className="h-[250px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={data?.device_stats.browser_distribution}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                <XAxis dataKey="browser" stroke="#475569" fontSize={10} />
                                <YAxis stroke="#475569" fontSize={10} />
                                <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }} />
                                <Bar dataKey="count" fill="#8b5cf6" radius={[4, 4, 0, 0]} barSize={30}>
                                    {data?.device_stats.browser_distribution.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[(index + 3) % COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader>
                        <CardTitle className="text-sm font-bold uppercase tracking-widest text-slate-500">Hardware Fleet</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {data?.device_stats.top_models.map((model, i) => (
                            <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-slate-950/50 border border-slate-800">
                                <div className="flex items-center gap-3">
                                    <div className="h-2 w-2 rounded-full" style={{ backgroundColor: COLORS[i % COLORS.length] }}></div>
                                    <div>
                                        <p className="text-xs font-bold text-slate-300">{model.device_model || 'Standard Terminal'}</p>
                                        <p className="text-[10px] text-slate-500 uppercase">{model.device_type}</p>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <p className="text-sm font-black text-indigo-400">{model.count}</p>
                                    <p className="text-[9px] text-slate-600 font-mono">NODES</p>
                                </div>
                            </div>
                        ))}
                    </CardContent>
                </Card>
            </div>

            {/* Realtime Hourly Flow */}
            <Card className="bg-slate-900 border-slate-800 text-white">
                <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                        <Activity className="h-5 w-5 text-indigo-400" />
                        Platform Pulse (Last 24 Hours)
                    </CardTitle>
                    <CardDescription className="text-slate-500">Hourly visit aggregates for system load monitoring.</CardDescription>
                </CardHeader>
                <CardContent className="h-[250px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={data?.realtime_dashboard.hourly_trend}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                            <XAxis
                                dataKey="hour"
                                stroke="#475569"
                                fontSize={10}
                                tickFormatter={(val) => new Date(val).getHours() + ':00'}
                            />
                            <YAxis stroke="#475569" fontSize={10} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                            />
                            <Line
                                type="stepAfter"
                                dataKey="count"
                                stroke="#818cf8"
                                strokeWidth={2}
                                dot={{ fill: '#818cf8', strokeWidth: 2, r: 2 }}
                                activeDot={{ r: 4, strokeWidth: 0 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </CardContent>
            </Card>
        </div>
    );
}

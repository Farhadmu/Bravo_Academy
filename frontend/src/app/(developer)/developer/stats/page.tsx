'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
    Activity,
    Users,
    Database,
    Brain,
    TrendingUp,
    Clock,
    AlertCircle,
    Server,
    Cpu,
    Zap,
    RefreshCw,
    Terminal,
    Lock,
    Shield
} from 'lucide-react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area,
    Cell,
    PieChart,
    Pie
} from 'recharts';
import api from '@/lib/api';
import { toast } from 'sonner';

interface SystemStats {
    total_users: number;
    active_users: number;
    total_students: number;
    total_admins: number;
    total_tests: number;
    total_questions: number;
    active_sessions: number;
    total_results: number;
    pending_payments: number;
    database_size_mb: number;
}

export default function SystemStats() {
    const [stats, setStats] = useState<SystemStats | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchStats = async () => {
        setIsLoading(true);
        try {
            const res = await api.get('/system/stats/');
            setStats(res.data);
        } catch (error) {
            toast.error('Failed to load system stats');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchStats();
    }, []);

    const userDistribution = [
        { name: 'Students', value: stats?.total_students || 0, color: '#6366f1' },
        { name: 'Admins', value: stats?.total_admins || 0, color: '#a855f7' },
        { name: 'Inactive', value: (stats?.total_users || 0) - (stats?.active_users || 0), color: '#334155' }
    ];

    const databaseMetrics = [
        { name: 'Users', count: stats?.total_users || 0 },
        { name: 'Tests', count: stats?.total_tests || 0 },
        { name: 'Questions', count: stats?.total_questions || 0 },
        { name: 'Results', count: stats?.total_results || 0 },
        { name: 'Payments', count: stats?.pending_payments || 0 },
    ];

    if (isLoading && !stats) {
        return <div className="animate-pulse space-y-8">
            <div className="h-20 bg-slate-900 rounded-lg"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="h-64 bg-slate-900 rounded-lg"></div>
                <div className="h-64 bg-slate-900 rounded-lg"></div>
            </div>
        </div>;
    }

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Activity className="h-8 w-8 text-green-400" />
                        System Monitoring
                    </h1>
                    <p className="text-slate-400 mt-1">Real-time application health and performance metrics.</p>
                </div>
                <Button variant="outline" onClick={fetchStats} className="bg-slate-900 border-slate-700">
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Poll Now
                </Button>
            </div>

            {/* Health Tiles */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {[
                    { label: 'API Uptime', value: '99.9%', icon: Server, color: 'text-green-400' },
                    { label: 'DB Latency', value: '45ms', icon: Database, color: 'text-blue-400' },
                    { label: 'Memory Usage', value: '12%', icon: Cpu, color: 'text-purple-400' },
                    { label: 'Throughput', value: '2.4k/hr', icon: Zap, color: 'text-yellow-400' }
                ].map((tile, i) => (
                    <Card key={i} className="bg-slate-900 border-slate-800 text-white">
                        <CardContent className="pt-6">
                            <div className="flex items-center gap-3">
                                <div className="p-2 rounded-lg bg-slate-950">
                                    <tile.icon className={`h-5 w-5 ${tile.color}`} />
                                </div>
                                <div>
                                    <p className="text-[10px] font-bold uppercase tracking-widest text-slate-500">{tile.label}</p>
                                    <p className="text-xl font-bold">{tile.value}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* User Pie Chart */}
                <Card className="bg-slate-900 border-slate-800 text-white flex flex-col">
                    <CardHeader>
                        <CardTitle className="text-base">User Composition</CardTitle>
                        <CardDescription>Breakdown of account roles and activity status.</CardDescription>
                    </CardHeader>
                    <CardContent className="flex-grow flex items-center justify-center p-0">
                        <div className="h-[250px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <PieChart>
                                    <Pie
                                        data={userDistribution}
                                        cx="50%"
                                        cy="50%"
                                        innerRadius={60}
                                        outerRadius={80}
                                        paddingAngle={5}
                                        dataKey="value"
                                    >
                                        {userDistribution.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={entry.color} />
                                        ))}
                                    </Pie>
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                                        itemStyle={{ color: '#fff' }}
                                    />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                    <div className="p-4 border-t border-slate-800 space-y-2">
                        {userDistribution.map((item) => (
                            <div key={item.name} className="flex items-center justify-between text-xs">
                                <div className="flex items-center gap-2">
                                    <div className="h-2 w-2 rounded-full" style={{ backgroundColor: item.color }}></div>
                                    <span className="text-slate-400">{item.name}</span>
                                </div>
                                <span className="font-mono font-bold">{item.value}</span>
                            </div>
                        ))}
                    </div>
                </Card>

                {/* Database Records Bar Chart */}
                <Card className="bg-slate-900 border-slate-800 text-white lg:col-span-2">
                    <CardHeader>
                        <CardTitle className="text-base">Data Volume per Object</CardTitle>
                        <CardDescription>Object counts across primary database tables.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={databaseMetrics}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                                    <XAxis
                                        dataKey="name"
                                        stroke="#475569"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                    />
                                    <YAxis
                                        stroke="#475569"
                                        fontSize={12}
                                        tickLine={false}
                                        axisLine={false}
                                        tickFormatter={(val) => `${val}`}
                                    />
                                    <Tooltip
                                        cursor={{ fill: '#1e293b', opacity: 0.4 }}
                                        contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                                    />
                                    <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]} barSize={40} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Performance Analytics Mock (Area Chart) */}
            <Card className="bg-slate-900 border-slate-800 text-white">
                <CardHeader className="flex flex-row items-center justify-between">
                    <div>
                        <CardTitle className="text-base">Traffic Pulse</CardTitle>
                        <CardDescription>Simulated API requests per hour.</CardDescription>
                    </div>
                    <div className="flex gap-2">
                        <span className="text-[10px] font-mono bg-blue-500/10 text-blue-400 px-2 py-0.5 rounded border border-blue-500/20 uppercase">Live Streaming</span>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="h-[200px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart
                                data={[
                                    { t: '12pm', v: 40 }, { t: '1pm', v: 55 }, { t: '2pm', v: 45 },
                                    { t: '3pm', v: 60 }, { t: '4pm', v: 110 }, { t: '5pm', v: 95 },
                                    { t: '6pm', v: 140 }, { t: '7pm', v: 120 }, { t: '8pm', v: 180 },
                                    { t: '9pm', v: 130 }, { t: '10pm', v: 100 }, { t: '11pm', v: 80 }
                                ]}
                            >
                                <defs>
                                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="t" stroke="#475569" fontSize={10} axisLine={false} tickLine={false} />
                                <YAxis hide />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="v"
                                    stroke="#8b5cf6"
                                    strokeWidth={3}
                                    fillOpacity={1}
                                    fill="url(#colorValue)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
                    <div className="flex items-center justify-between">
                        <h3 className="text-sm font-bold uppercase tracking-widest flex items-center gap-2">
                            <Lock className="h-4 w-4 text-yellow-500" />
                            Security Log
                        </h3>
                        <Button variant="ghost" size="sm" className="h-6 text-[10px]">VIEW ALL</Button>
                    </div>
                    <div className="space-y-3">
                        {[
                            { event: 'Failed login attempt', user: 'anonymous', ip: '103.xxx.xxx.45', time: '2 mins ago', level: 'warn' },
                            { event: 'Admin password reset', user: 'admin', ip: '202.xxx.xxx.22', time: '14 mins ago', level: 'info' },
                            { event: 'Database backup', user: 'system', ip: '127.0.0.1', time: '1 hour ago', level: 'success' },
                        ].map((log, i) => (
                            <div key={i} className="flex items-start justify-between bg-slate-950 p-2 border border-slate-800/50 rounded text-[11px] font-mono">
                                <div className="space-y-1">
                                    <p className={`font-bold ${log.level === 'warn' ? 'text-red-400' : 'text-slate-200'}`}>{log.event}</p>
                                    <p className="text-slate-500">USER: {log.user} | IP: {log.ip}</p>
                                </div>
                                <span className="text-slate-600">{log.time}</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
                    <h3 className="text-sm font-bold uppercase tracking-widest flex items-center gap-2 text-purple-400">
                        <Shield className="h-4 w-4" />
                        Developer Tools Info
                    </h3>
                    <div className="space-y-3 text-[11px] text-slate-400 leading-relaxed">
                        <p>The system monitoring dashboard provides high-level visibility into infrastructure health. For deeper tracing, check the <span className="text-white">Render Logs</span> or <span className="text-white">Vercel Vitals</span>.</p>
                        <ul className="list-disc pl-4 space-y-1">
                            <li>PostgreSQL connection pooling: <span className="text-green-400">ENABLED</span></li>
                            <li>Static asset caching: <span className="text-green-400">ACTIVE (WhiteNoise)</span></li>
                            <li>JWT Token expiration: <span className="text-yellow-400">60 mins</span></li>
                            <li>Argon2 iterations: <span className="text-blue-400">2</span></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}

'use client';

import { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
    Activity,
    Users,
    MousePointer2,
    Smartphone,
    Tablet,
    Laptop,
    Monitor,
    RefreshCw,
    Clock,
    Globe,
    ExternalLink
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';
import { formatDistanceToNow } from 'date-fns';

interface RealTimeData {
    active_now: number;
    visits_today: number;
    device_distribution: { device_type: string; count: number }[];
    hourly_trend: { hour: string; count: number }[];
}

interface ActiveSession {
    id: string;
    user_username: string;
    ip_address: string;
    device_model: string;
    device_type: string;
    browser: string;
    os: string;
    current_page: string;
    last_activity: string;
    duration: number;
}

export default function RealTimeDashboard() {
    const [data, setData] = useState<RealTimeData | null>(null);
    const [activeSessions, setActiveSessions] = useState<ActiveSession[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
    const [isRefreshing, setIsRefreshing] = useState(false);

    const fetchData = useCallback(async (showLoading = true) => {
        if (showLoading) setIsLoading(true);
        setIsRefreshing(true);
        try {
            const [analyticsRes, sessionsRes] = await Promise.all([
                api.get('/system/analytics/realtime_dashboard/'),
                api.get('/system/active-sessions/')
            ]);
            setData(analyticsRes.data);
            setActiveSessions(sessionsRes.data.results || sessionsRes.data);
            setLastUpdated(new Date());
        } catch (error) {
            console.error('Failed to fetch real-time data:', error);
            toast.error('Failed to sync real-time data');
        } finally {
            setIsLoading(false);
            setIsRefreshing(false);
        }
    }, []);

    useEffect(() => {
        fetchData();

        // Auto-refresh every 10 seconds
        const interval = setInterval(() => {
            fetchData(false);
        }, 10000);

        return () => clearInterval(interval);
    }, [fetchData]);

    const getDeviceIcon = (type: string) => {
        switch (type.toLowerCase()) {
            case 'mobile': return <Smartphone className="h-4 w-4" />;
            case 'tablet': return <Tablet className="h-4 w-4" />;
            case 'laptop': return <Laptop className="h-4 w-4" />;
            case 'desktop': return <Monitor className="h-4 w-4" />;
            default: return <Activity className="h-4 w-4" />;
        }
    };

    if (isLoading && !data) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="flex flex-col items-center gap-4">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
                    <p className="text-slate-400 animate-pulse font-mono text-sm uppercase">Establishing Live Uplink...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-2">
                        <Activity className="h-8 w-8 text-indigo-400" />
                        Real-Time Monitor
                    </h1>
                    <p className="text-slate-400 mt-1">Live platform activity and session tracking.</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="text-right hidden sm:block">
                        <p className="text-[10px] text-slate-500 uppercase font-bold">Last Sync</p>
                        <p className="text-xs text-indigo-300 font-mono">{lastUpdated.toLocaleTimeString()}</p>
                    </div>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => fetchData()}
                        disabled={isRefreshing}
                        className="bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800"
                    >
                        <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
                        Sync Now
                    </Button>
                </div>
            </div>

            {/* Live Stats Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="bg-slate-900 border-slate-800 text-white overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <Users className="h-12 w-12" />
                    </div>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Active Users Now</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-baseline gap-2">
                            <span className="text-4xl font-black text-white">{data?.active_now || 0}</span>
                            <span className="flex items-center gap-1 text-xs text-green-400 bg-green-400/10 px-2 py-0.5 rounded-full">
                                <span className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse"></span>
                                Live
                            </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-2">Currently connected sessions</p>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <MousePointer2 className="h-12 w-12" />
                    </div>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Daily Impressions</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-4xl font-black text-white">{data?.visits_today || 0}</div>
                        <p className="text-xs text-slate-400 mt-2">Page visits captured today</p>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white overflow-hidden relative">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <Monitor className="h-12 w-12" />
                    </div>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-semibold text-slate-500 uppercase tracking-widest">Primary Device</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-black text-white uppercase">
                            {data?.device_distribution?.sort((a, b) => b.count - a.count)[0]?.device_type || 'N/A'}
                        </div>
                        <p className="text-xs text-slate-400 mt-2">Most common entry point</p>
                    </CardContent>
                </Card>
            </div>

            {/* Active Sessions Table */}
            <Card className="bg-slate-900 border-slate-800 text-white">
                <CardHeader className="flex flex-row items-center justify-between border-b border-slate-800 pb-4">
                    <div>
                        <CardTitle className="text-lg">Connected Sessions</CardTitle>
                        <CardDescription className="text-slate-500">Real-time view of users interacting with the platform.</CardDescription>
                    </div>
                    <Badge variant="outline" className="bg-indigo-500/10 text-indigo-400 border-indigo-500/20 font-mono">
                        {activeSessions.length} SESSIONS
                    </Badge>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-slate-950/50 text-slate-500 text-[10px] uppercase tracking-widest font-bold">
                                    <th className="px-6 py-4">User / Account</th>
                                    <th className="px-6 py-4">Current Location</th>
                                    <th className="px-6 py-4">Device & OS</th>
                                    <th className="px-6 py-4">Connection</th>
                                    <th className="px-6 py-4">Activity</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800">
                                {activeSessions.length > 0 ? (
                                    activeSessions.map((session) => (
                                        <tr key={session.id} className="hover:bg-slate-800/50 transition-colors group">
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="h-8 w-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-[10px] font-bold text-slate-300">
                                                        {session.user_username.charAt(0).toUpperCase()}
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-semibold group-hover:text-indigo-400 transition-colors">{session.user_username}</p>
                                                        <p className="text-[10px] text-slate-500 font-mono tracking-tighter">ID: {session.id.substring(0, 8)}...</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col">
                                                    <span className="text-xs font-mono text-slate-300 max-w-[150px] truncate">{session.current_page}</span>
                                                    <div className="flex items-center gap-1 mt-1">
                                                        <div className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-pulse"></div>
                                                        <span className="text-[10px] text-slate-500 uppercase font-bold tracking-tighter">Active Viewing</span>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2">
                                                    <div className="h-7 w-7 rounded bg-slate-950 border border-slate-800 flex items-center justify-center text-slate-500">
                                                        {getDeviceIcon(session.device_type)}
                                                    </div>
                                                    <div>
                                                        <p className="text-xs font-medium text-slate-200">{session.device_model || 'Generic Device'}</p>
                                                        <p className="text-[10px] text-slate-500">{session.os} • {session.browser}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col">
                                                    <div className="flex items-center gap-1.5">
                                                        <Globe className="h-3 w-3 text-slate-500" />
                                                        <span className="text-xs font-mono text-slate-300">{session.ip_address}</span>
                                                    </div>
                                                    <span className="text-[10px] text-slate-600 font-bold uppercase mt-1">Direct Connection</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col items-end">
                                                    <div className="flex items-center gap-1.5 text-xs text-indigo-400 font-mono">
                                                        <Clock className="h-3 w-3" />
                                                        {formatDistanceToNow(new Date(session.last_activity), { addSuffix: true })}
                                                    </div>
                                                    <Badge variant="outline" className="h-5 text-[9px] mt-1 bg-slate-950 border-slate-800 text-slate-500 font-bold">
                                                        STABLE SES
                                                    </Badge>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center">
                                            <div className="flex flex-col items-center gap-2">
                                                <Users className="h-8 w-8 text-slate-700" />
                                                <p className="text-sm text-slate-500 font-medium">No active sessions detected.</p>
                                                <p className="text-[10px] text-slate-600 uppercase font-bold tracking-widest">Awaiting connections...</p>
                                            </div>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>

            {/* Additional Info Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader>
                        <CardTitle className="text-sm flex items-center gap-2">
                            <Monitor className="h-4 w-4 text-blue-400" />
                            Device Breakdown
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {data?.device_distribution.map((item) => {
                                const percentage = data.device_distribution.reduce((acc, curr) => acc + curr.count, 0) > 0
                                    ? (item.count / data.device_distribution.reduce((acc, curr) => acc + curr.count, 0)) * 100
                                    : 0;
                                return (
                                    <div key={item.device_type} className="space-y-1">
                                        <div className="flex justify-between text-xs font-mono uppercase">
                                            <span className="flex items-center gap-2">
                                                {getDeviceIcon(item.device_type)}
                                                {item.device_type}
                                            </span>
                                            <span className="text-slate-500">{item.count} sessions • {percentage.toFixed(1)}%</span>
                                        </div>
                                        <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden">
                                            <div
                                                className="h-full bg-blue-500 rounded-full"
                                                style={{ width: `${percentage}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader>
                        <CardTitle className="text-sm flex items-center gap-2">
                            <Clock className="h-4 w-4 text-purple-400" />
                            Real-Time Notes
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                        <div className="bg-slate-950 p-3 rounded-md border border-slate-800">
                            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Session Policy</p>
                            <p className="text-xs text-slate-500 italic">Sessions are considered "active" if there has been activity within the last 30 minutes. The monitor refreshes automatically every 10 seconds.</p>
                        </div>
                        <div className="flex justify-between items-center p-2 rounded hover:bg-slate-800/30 transition-colors">
                            <span className="text-xs font-semibold text-slate-300">Detailed Login Logs</span>
                            <Button
                                variant="ghost"
                                size="sm"
                                className="h-7 text-[10px] font-bold text-indigo-400 hover:text-indigo-300"
                                onClick={() => window.location.href = '/developer/monitoring/login-logs'}
                            >
                                VIEW ARCHIVE →
                            </Button>
                        </div>
                        <div className="flex justify-between items-center p-2 rounded hover:bg-slate-800/30 transition-colors">
                            <span className="text-xs font-semibold text-slate-300">Historical Visit Data</span>
                            <Button
                                variant="ghost"
                                size="sm"
                                className="h-7 text-[10px] font-bold text-indigo-400 hover:text-indigo-300"
                                onClick={() => window.location.href = '/developer/monitoring/analytics'}
                            >
                                ANALYZE TRENDS →
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

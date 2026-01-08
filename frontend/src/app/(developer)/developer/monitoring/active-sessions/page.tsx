'use client';

import { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
    Users,
    Activity,
    Smartphone,
    Tablet,
    Laptop,
    Monitor,
    RefreshCw,
    Clock,
    Globe,
    ExternalLink,
    Search,
    Filter,
    ShieldAlert
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';
import { formatDistanceToNow } from 'date-fns';
import { Input } from '@/components/ui/input';

interface ActiveSession {
    id: string;
    user_username: string;
    session_key: string;
    login_time: string;
    last_activity: string;
    ip_address: string;
    device_model: string;
    device_type: string;
    browser: string;
    os: string;
    current_page: string;
    duration: number;
    is_session_active: boolean;
}

export default function ActiveSessionsPage() {
    const [sessions, setSessions] = useState<ActiveSession[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [isRefreshing, setIsRefreshing] = useState(false);

    const fetchData = useCallback(async (showLoading = true) => {
        if (showLoading) setIsLoading(true);
        setIsRefreshing(true);
        try {
            const res = await api.get('/system/active-sessions/');
            setSessions(res.data.results || res.data);
        } catch (error) {
            console.error('Failed to fetch sessions:', error);
            toast.error('Failed to load active sessions');
        } finally {
            setIsLoading(false);
            setIsRefreshing(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
        const interval = setInterval(() => fetchData(false), 30000);
        return () => clearInterval(interval);
    }, [fetchData]);

    const filteredSessions = sessions.filter(s =>
        s.user_username.toLowerCase().includes(search.toLowerCase()) ||
        s.ip_address.includes(search) ||
        s.current_page.toLowerCase().includes(search.toLowerCase())
    );

    const getDeviceIcon = (type: string) => {
        switch (type.toLowerCase()) {
            case 'mobile': return <Smartphone className="h-4 w-4" />;
            case 'tablet': return <Tablet className="h-4 w-4" />;
            case 'laptop': return <Laptop className="h-4 w-4" />;
            case 'desktop': return <Monitor className="h-4 w-4" />;
            default: return <Activity className="h-4 w-4" />;
        }
    };

    if (isLoading && sessions.length === 0) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="flex flex-col items-center gap-4">
                    <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
                    <p className="text-slate-400 font-mono text-sm uppercase">Scanning Active Nodes...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-2">
                        <Users className="h-8 w-8 text-indigo-400" />
                        Active Sessions
                    </h1>
                    <p className="text-slate-400 mt-1">Live tracking of all users currently authenticated.</p>
                </div>
                <div className="flex items-center gap-2">
                    <div className="relative w-full md:w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                        <Input
                            placeholder="Filter sessions..."
                            className="pl-9 bg-slate-900 border-slate-700 text-white placeholder:text-slate-600"
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                        />
                    </div>
                    <Button
                        variant="outline"
                        onClick={() => fetchData()}
                        disabled={isRefreshing}
                        className="bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800"
                    >
                        <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
                        Refresh
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="bg-slate-900 border-slate-800 text-white shadow-xl shadow-black/20">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-widest">Connected Users</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-black">{sessions.length}</div>
                        <p className="text-[10px] text-green-400 font-mono mt-1">● LIVE UPLINK ESTABLISHED</p>
                    </CardContent>
                </Card>
                <Card className="bg-slate-900 border-slate-800 text-white shadow-xl shadow-black/20">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-widest">Avg Session Duration</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-black">
                            {sessions.length > 0
                                ? Math.round(sessions.reduce((acc, s) => acc + s.duration, 0) / sessions.length)
                                : 0} min
                        </div>
                        <p className="text-[10px] text-slate-500 font-mono mt-1 italic tracking-tight">Mean activity time across all nodes</p>
                    </CardContent>
                </Card>
                <Card className="bg-slate-900 border-slate-800 text-white shadow-xl shadow-black/20">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-xs font-bold text-slate-500 uppercase tracking-widest">Security Health</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2 text-green-400">
                            <ShieldAlert className="h-6 w-6" />
                            <span className="text-xl font-bold uppercase tracking-tighter">Secure</span>
                        </div>
                        <p className="text-[10px] text-slate-500 font-mono mt-1">Multi-device blocking active</p>
                    </CardContent>
                </Card>
            </div>

            <Card className="bg-slate-900 border-slate-800 text-white">
                <CardHeader className="border-b border-slate-800 pb-4">
                    <CardTitle className="text-lg">Live Connection Manifest</CardTitle>
                    <CardDescription className="text-slate-500">Authenticated user sessions being monitored in real-time.</CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-slate-950/50 text-slate-500 text-[10px] uppercase tracking-widest font-bold">
                                    <th className="px-6 py-4">Session ID / User</th>
                                    <th className="px-6 py-4">Terminal & OS</th>
                                    <th className="px-6 py-4">Network Node</th>
                                    <th className="px-6 py-4">Current View</th>
                                    <th className="px-6 py-4">Activity Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800">
                                {filteredSessions.length > 0 ? (
                                    filteredSessions.map((session) => (
                                        <tr key={session.id} className="hover:bg-slate-800/50 transition-colors group">
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="h-10 w-10 rounded-lg bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center text-indigo-400 font-bold uppercase">
                                                        {session.user_username.charAt(0)}
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-bold group-hover:text-indigo-400 transition-colors">{session.user_username}</p>
                                                        <p className="text-[10px] text-slate-500 font-mono">KEY: {session.session_key.substring(0, 12)}...</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2">
                                                    <div className="h-8 w-8 rounded bg-slate-950 border border-slate-800 flex items-center justify-center text-slate-400">
                                                        {getDeviceIcon(session.device_type)}
                                                    </div>
                                                    <div>
                                                        <p className="text-xs font-semibold text-slate-200">{session.device_model || 'Standard Terminal'}</p>
                                                        <p className="text-[10px] text-slate-500 italic tracking-tighter">{session.os} • {session.browser}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col">
                                                    <div className="flex items-center gap-1.5 text-xs font-mono text-slate-300">
                                                        <Globe className="h-3 w-3 text-slate-600" />
                                                        {session.ip_address}
                                                    </div>
                                                    <Badge variant="outline" className="h-4 text-[8px] mt-1.5 w-fit bg-slate-950 border-slate-800 text-slate-500 font-mono tracking-tighter">
                                                        IPV4 STATIC
                                                    </Badge>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col">
                                                    <span className="text-xs font-bold text-indigo-300 max-w-[180px] truncate">{session.current_page}</span>
                                                    <span className="text-[9px] text-slate-600 uppercase font-black mt-1">Live Endpoint</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col items-end">
                                                    <div className="flex items-center gap-1.5 text-xs text-green-400 font-mono">
                                                        <Clock className="h-3 w-3" />
                                                        {formatDistanceToNow(new Date(session.last_activity), { addSuffix: true })}
                                                    </div>
                                                    <div className="flex items-center gap-2 mt-1.5">
                                                        <span className="h-1.5 w-1.5 rounded-full bg-green-500 animate-pulse"></span>
                                                        <span className="text-[9px] text-slate-500 font-bold uppercase tracking-widest">Active Link</span>
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center">
                                            <p className="text-sm text-slate-500 uppercase tracking-widest font-bold">Scanning... No active nodes detected.</p>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

'use client';

import { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
    Lock,
    Search,
    Filter,
    Smartphone,
    Tablet,
    Laptop,
    Monitor,
    RefreshCw,
    AlertCircle,
    CheckCircle2,
    XCircle,
    ChevronLeft,
    ChevronRight,
    Calendar,
    Globe,
    Info
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';
import { format } from 'date-fns';

interface LoginLog {
    id: string;
    user_username: string;
    username_attempted: string;
    timestamp: string;
    ip_address: string;
    device_model: string;
    device_type: string;
    browser: string;
    os: string;
    status: 'success' | 'failed';
    failure_reason: string;
}

export default function LoginLogsPage() {
    const [logs, setLogs] = useState<LoginLog[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);
    const [totalCount, setTotalCount] = useState(0);
    const [isRefreshing, setIsRefreshing] = useState(false);

    const fetchLogs = useCallback(async (showLoading = true) => {
        if (showLoading) setIsLoading(true);
        setIsRefreshing(true);
        try {
            const res = await api.get(`/system/login-logs/?page=${page}&search=${search}&ordering=-timestamp`);
            setLogs(res.data.results);
            setTotalCount(res.data.count);
        } catch (error) {
            console.error('Failed to fetch login logs:', error);
            toast.error('Failed to load login records');
        } finally {
            setIsLoading(false);
            setIsRefreshing(false);
        }
    }, [page, search]);

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchLogs();
        }, 300);
        return () => clearTimeout(timer);
    }, [fetchLogs]);

    const getDeviceIcon = (type: string) => {
        switch (type?.toLowerCase()) {
            case 'mobile': return <Smartphone className="h-4 w-4" />;
            case 'tablet': return <Tablet className="h-4 w-4" />;
            case 'laptop': return <Laptop className="h-4 w-4" />;
            case 'desktop': return <Monitor className="h-4 w-4" />;
            default: return <AlertCircle className="h-4 w-4" />;
        }
    };

    const totalPages = Math.ceil(totalCount / 50); // Assuming PAGE_SIZE is 50 for logs

    return (
        <div className="space-y-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-2">
                        <Lock className="h-8 w-8 text-indigo-400" />
                        Login Logs
                    </h1>
                    <p className="text-slate-400 mt-1">Archive of authentication attempts and security events.</p>
                </div>
                <div className="flex items-center gap-2">
                    <div className="relative w-full md:w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                        <Input
                            placeholder="Find user, IP, or device..."
                            className="pl-9 bg-slate-900 border-slate-700 text-white placeholder:text-slate-600 focus:ring-indigo-500"
                            value={search}
                            onChange={(e) => {
                                setSearch(e.target.value);
                                setPage(1);
                            }}
                        />
                    </div>
                    <Button
                        variant="outline"
                        size="icon"
                        onClick={() => fetchLogs()}
                        disabled={isRefreshing}
                        className="bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800"
                    >
                        <RefreshCw className={`h-4 w-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                    </Button>
                </div>
            </div>

            <Card className="bg-slate-900 border-slate-800 text-white">
                <CardHeader className="flex flex-row items-center justify-between border-b border-slate-800 pb-4">
                    <div>
                        <CardTitle className="text-lg">Security Archive</CardTitle>
                        <CardDescription className="text-slate-500">Chronological history of all login interactions.</CardDescription>
                    </div>
                    <div className="text-right">
                        <p className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Database Record</p>
                        <p className="text-lg font-black text-white">{totalCount.toLocaleString()}</p>
                    </div>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-slate-950/50 text-slate-500 text-[10px] uppercase tracking-widest font-bold">
                                    <th className="px-6 py-4">Timestamp</th>
                                    <th className="px-6 py-4">Attempted User</th>
                                    <th className="px-6 py-4">Status & Origin</th>
                                    <th className="px-6 py-4">Hardware Info</th>
                                    <th className="px-6 py-4">Terminal Details</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800">
                                {isLoading && logs.length === 0 ? (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center">
                                            <div className="flex flex-col items-center gap-2">
                                                <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-indigo-500"></div>
                                                <p className="text-sm text-slate-500 font-mono tracking-widest uppercase mt-4">Pulling Encrypted Logs...</p>
                                            </div>
                                        </td>
                                    </tr>
                                ) : logs.length > 0 ? (
                                    logs.map((log) => (
                                        <tr key={log.id} className="hover:bg-slate-800/50 transition-colors group">
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2 text-slate-300">
                                                    <Calendar className="h-3 w-3 text-slate-500" />
                                                    <div className="flex flex-col">
                                                        <span className="text-xs font-mono">{format(new Date(log.timestamp), 'MMM dd, yyyy')}</span>
                                                        <span className="text-[10px] text-slate-500 font-mono">{format(new Date(log.timestamp), 'HH:mm:ss')}</span>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className={`h-8 w-8 rounded bg-slate-950 border ${log.status === 'success' ? 'border-indigo-500/30' : 'border-red-500/30'} flex items-center justify-center text-[10px] font-bold`}>
                                                        {log.username_attempted.charAt(0).toUpperCase()}
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-semibold group-hover:text-indigo-400 transition-colors">{log.username_attempted}</p>
                                                        <p className="text-[10px] text-slate-500 font-mono italic">{log.user_username || 'No linked account'}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="space-y-1.5">
                                                    <div className="flex items-center gap-1.5">
                                                        {log.status === 'success' ? (
                                                            <Badge className="bg-green-500/10 text-green-400 border-green-500/20 hover:bg-green-500/10 text-[9px] uppercase h-5">
                                                                <CheckCircle2 className="h-2.5 w-2.5 mr-1" />
                                                                Authorized
                                                            </Badge>
                                                        ) : (
                                                            <Badge className="bg-red-500/10 text-red-400 border-red-500/20 hover:bg-red-500/10 text-[9px] uppercase h-5">
                                                                <XCircle className="h-2.5 w-2.5 mr-1" />
                                                                Denial
                                                            </Badge>
                                                        )}
                                                    </div>
                                                    <div className="flex items-center gap-1 text-[10px] text-slate-400 font-mono">
                                                        <Globe className="h-3 w-3 text-slate-600" />
                                                        {log.ip_address}
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2">
                                                    <div className="h-7 w-7 rounded-full bg-slate-950 border border-slate-800 flex items-center justify-center text-slate-500">
                                                        {getDeviceIcon(log.device_type)}
                                                    </div>
                                                    <div>
                                                        <p className="text-xs font-medium text-slate-200">{log.device_model || 'Unknown Device'}</p>
                                                        <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tighter">{log.device_type}</p>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col">
                                                    <div className="flex items-center gap-1 text-[10px] text-slate-400">
                                                        <Info className="h-3 w-3 text-slate-600" />
                                                        <span className="font-medium text-slate-300">{log.browser}</span>
                                                    </div>
                                                    <span className="text-[10px] text-slate-500 mt-0.5">{log.os}</span>
                                                    {log.failure_reason && (
                                                        <p className="text-[9px] text-red-400 mt-1 italic font-mono bg-red-400/5 px-1 py-0.5 rounded border border-red-400/10 truncate max-w-[150px]">
                                                            ERR: {log.failure_reason}
                                                        </p>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center">
                                            <div className="flex flex-col items-center gap-2">
                                                <Lock className="h-10 w-10 text-slate-800" />
                                                <p className="text-sm text-slate-500 font-medium">No login logs found matching your criteria.</p>
                                            </div>
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
                <div className="px-6 py-4 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <p className="text-xs text-slate-500 font-mono">
                        Page <span className="text-white">{page}</span> of <span className="text-white">{totalPages || 1}</span>
                    </p>
                    <div className="flex items-center gap-2">
                        <Button
                            variant="outline"
                            size="sm"
                            disabled={page === 1 || isLoading}
                            onClick={() => setPage(p => p - 1)}
                            className="bg-slate-900 border-slate-700 text-slate-300"
                        >
                            <ChevronLeft className="h-4 w-4 mr-1" />
                            Prev
                        </Button>
                        <Button
                            variant="outline"
                            size="sm"
                            disabled={page >= totalPages || isLoading}
                            onClick={() => setPage(p => p + 1)}
                            className="bg-slate-900 border-slate-700 text-slate-300"
                        >
                            Next
                            <ChevronRight className="h-4 w-4 ml-1" />
                        </Button>
                    </div>
                </div>
            </Card>
        </div>
    );
}

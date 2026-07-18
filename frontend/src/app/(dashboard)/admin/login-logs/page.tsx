'use client';

import { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
    Lock,
    Search,
    RefreshCw,
    Smartphone,
    Tablet,
    Monitor,
    Loader2,
    AlertTriangle,
    CheckCircle2,
    XCircle,
    ChevronLeft,
    ChevronRight,
    Calendar,
    Globe,
    Info,
    Users,
    Laptop
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';
import { format } from 'date-fns';

interface LoginLogEntry {
    id: string;
    username: string;
    full_name: string;
    role: string;
    ip_address: string;
    device_type: string;
    browser: string;
    os: string;
    login_time: string;
    success: boolean;
}

export default function AdminLoginLogsPage() {
    const [logs, setLogs] = useState<LoginLogEntry[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [page, setPage] = useState(1);
    const [totalCount, setTotalCount] = useState(0);
    const [nextPage, setNextPage] = useState<number | null>(null);
    const [prevPage, setPrevPage] = useState<number | null>(null);
    const [error, setError] = useState<string | null>(null);

    const fetchLogs = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            const searchParams = new URLSearchParams();
            searchParams.set('page', String(page));
            searchParams.set('page_size', '50');
            if (search) searchParams.set('username', search);

            const res = await api.get(`/auth/login-logs/?${searchParams.toString()}`);
            const data = res.data;
            setLogs(data.results);
            setTotalCount(data.count);
            setNextPage(data.next);
            setPrevPage(data.previous);
        } catch (err: any) {
            console.error('Failed to fetch login logs:', err);
            setError('Failed to load login logs. Please try again.');
            toast.error('Failed to load login records');
        } finally {
            setLoading(false);
        }
    }, [page, search]);

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchLogs();
        }, 300);
        return () => clearTimeout(timer);
    }, [fetchLogs]);

    const handleSearch = (value: string) => {
        setSearch(value);
        setPage(1);
    };

    const getDeviceIcon = (type: string) => {
        switch (type?.toLowerCase()) {
            case 'mobile': return <Smartphone className="h-4 w-4" />;
            case 'tablet': return <Tablet className="h-4 w-4" />;
            case 'laptop': return <Laptop className="h-4 w-4" />;
            case 'desktop': return <Monitor className="h-4 w-4" />;
            default: return <Monitor className="h-4 w-4" />;
        }
    };

    const totalPages = Math.ceil(totalCount / 50);

    if (loading && logs.length === 0) {
        return (
            <div className="flex justify-center items-center min-h-[60vh]">
                <div className="flex flex-col items-center gap-3">
                    <Loader2 className="h-10 w-10 text-blue-600 animate-spin" />
                    <p className="text-gray-500 font-medium">Loading login logs...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-gray-900 flex items-center gap-2">
                        <Lock className="h-8 w-8 text-blue-600" />
                        Login Logs
                    </h1>
                    <p className="text-gray-500 mt-1">
                        Monitor user authentication history — who logged in, when, and from which device.
                    </p>
                </div>
                <div className="flex items-center gap-2">
                    <div className="relative w-full md:w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <Input
                            placeholder="Search by username..."
                            className="pl-9"
                            value={search}
                            onChange={(e) => handleSearch(e.target.value)}
                        />
                    </div>
                    <Button
                        variant="outline"
                        size="icon"
                        onClick={() => fetchLogs()}
                        disabled={loading}
                    >
                        <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                    </Button>
                </div>
            </div>

            {/* Error State */}
            {error && (
                <div className="bg-red-50 border border-red-100 text-red-600 p-4 rounded-md flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4" />
                    {error}
                </div>
            )}

            {/* Logs Table */}
            <Card>
                <CardHeader className="flex flex-row items-center justify-between border-b pb-4">
                    <div>
                        <CardTitle className="text-lg">Authentication History</CardTitle>
                        <CardDescription>
                            Chronological record of all successful logins.
                        </CardDescription>
                    </div>
                    <div className="text-right">
                        <p className="text-xs text-gray-500 uppercase font-medium tracking-wider">Total Records</p>
                        <p className="text-2xl font-bold text-gray-900">{totalCount.toLocaleString()}</p>
                    </div>
                </CardHeader>
                <CardContent className="p-0">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left">
                            <thead>
                                <tr className="bg-gray-50 text-gray-500 text-xs uppercase tracking-wider font-medium">
                                    <th className="px-6 py-4">Timestamp</th>
                                    <th className="px-6 py-4">User</th>
                                    <th className="px-6 py-4">Status &amp; IP</th>
                                    <th className="px-6 py-4">Device</th>
                                    <th className="px-6 py-4">Browser &amp; OS</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-100">
                                {logs.length > 0 ? (
                                    logs.map((log) => (
                                        <tr key={log.id} className="hover:bg-gray-50 transition-colors group">
                                            {/* Timestamp */}
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2 text-gray-600">
                                                    <Calendar className="h-3.5 w-3.5 text-gray-400" />
                                                    <div className="flex flex-col">
                                                        <span className="text-sm font-mono text-gray-700">
                                                            {format(new Date(log.login_time), 'MMM dd, yyyy')}
                                                        </span>
                                                        <span className="text-xs text-gray-400 font-mono">
                                                            {format(new Date(log.login_time), 'HH:mm:ss')}
                                                        </span>
                                                    </div>
                                                </div>
                                            </td>

                                            {/* User */}
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-3">
                                                    <div className="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm">
                                                        {(log.full_name || log.username).charAt(0).toUpperCase()}
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-semibold text-gray-900">
                                                            {log.full_name || log.username}
                                                        </p>
                                                        <p className="text-xs text-gray-400 font-mono">
                                                            @{log.username}
                                                            <span className="ml-1.5 inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-600 capitalize">
                                                                {log.role}
                                                            </span>
                                                        </p>
                                                    </div>
                                                </div>
                                            </td>

                                            {/* Status & IP */}
                                            <td className="px-6 py-4">
                                                <div className="space-y-1.5">
                                                    <div className="flex items-center gap-1.5">
                                                        {log.success ? (
                                                            <Badge variant="secondary" className="bg-green-50 text-green-700 border-green-200 text-xs">
                                                                <CheckCircle2 className="h-3 w-3 mr-1" />
                                                                Success
                                                            </Badge>
                                                        ) : (
                                                            <Badge variant="secondary" className="bg-red-50 text-red-700 border-red-200 text-xs">
                                                                <XCircle className="h-3 w-3 mr-1" />
                                                                Failed
                                                            </Badge>
                                                        )}
                                                    </div>
                                                    <div className="flex items-center gap-1 text-xs text-gray-400 font-mono">
                                                        <Globe className="h-3 w-3 text-gray-400" />
                                                        {log.ip_address || 'Unknown'}
                                                    </div>
                                                </div>
                                            </td>

                                            {/* Device */}
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2">
                                                    <div className="h-8 w-8 rounded-lg bg-gray-100 border border-gray-200 flex items-center justify-center text-gray-500">
                                                        {getDeviceIcon(log.device_type)}
                                                    </div>
                                                    <div className="flex flex-col">
                                                        <span className="text-sm font-medium text-gray-700 capitalize">
                                                            {log.device_type || 'Unknown'}
                                                        </span>
                                                    </div>
                                                </div>
                                            </td>

                                            {/* Browser & OS */}
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col gap-1">
                                                    <div className="flex items-center gap-1 text-xs text-gray-600">
                                                        <Info className="h-3 w-3 text-gray-400" />
                                                        <span>{log.browser || 'Unknown'}</span>
                                                    </div>
                                                    <span className="text-xs text-gray-400 ml-4">
                                                        {log.os || 'Unknown OS'}
                                                    </span>
                                                </div>
                                            </td>
                                        </tr>
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} className="px-6 py-12 text-center">
                                            {search ? (
                                                <div className="flex flex-col items-center gap-2 text-gray-400">
                                                    <Search className="h-10 w-10 text-gray-300" />
                                                    <p className="text-sm font-medium">No login logs found for &quot;{search}&quot;.</p>
                                                    <p className="text-xs text-gray-400">Try a different search term.</p>
                                                </div>
                                            ) : (
                                                <div className="flex flex-col items-center gap-2 text-gray-400">
                                                    <Lock className="h-10 w-10 text-gray-300" />
                                                    <p className="text-sm font-medium">No login logs recorded yet.</p>
                                                    <p className="text-xs text-gray-400">Login logs will appear here after users sign in.</p>
                                                </div>
                                            )}
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>

                {/* Pagination */}
                {totalCount > 0 && (
                    <div className="px-6 py-4 border-t border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                        <p className="text-sm text-gray-500">
                            Page <span className="font-medium text-gray-700">{page}</span> of{' '}
                            <span className="font-medium text-gray-700">{totalPages || 1}</span>
                            {' '}&middot;{' '}
                            <span className="font-medium text-gray-700">{logs.length}</span> records shown
                        </p>
                        <div className="flex items-center gap-2">
                            <Button
                                variant="outline"
                                size="sm"
                                disabled={page === 1 || loading}
                                onClick={() => setPage(p => p - 1)}
                            >
                                <ChevronLeft className="h-4 w-4 mr-1" />
                                Previous
                            </Button>
                            <Button
                                variant="outline"
                                size="sm"
                                disabled={!nextPage || loading}
                                onClick={() => setPage(p => p + 1)}
                            >
                                Next
                                <ChevronRight className="h-4 w-4 ml-1" />
                            </Button>
                        </div>
                    </div>
                )}
            </Card>
        </div>
    );
}

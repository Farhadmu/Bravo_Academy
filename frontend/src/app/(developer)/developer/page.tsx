'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
    Users,
    Brain,
    CreditCard,
    Activity,
    Database,
    Shield,
    Lock,
    CheckCircle,
    XCircle,
    Terminal,
    AlertTriangle,
    AlertCircle,
    RefreshCw
} from 'lucide-react';
import { useAuthStore } from '@/store/auth';
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

interface MaintenanceStatus {
    is_active: boolean;
    target_roles: string[];
    message: string;
}

export default function DeveloperDashboard() {
    const { user } = useAuthStore();
    const [stats, setStats] = useState<SystemStats | null>(null);
    const [maintenance, setMaintenance] = useState<MaintenanceStatus | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchData = async () => {
        setIsLoading(true);
        try {
            const [statsRes, maintenanceRes] = await Promise.all([
                api.get('/system/stats/'),
                api.get('/system/maintenance/current/')
            ]);
            setStats(statsRes.data);
            setMaintenance(maintenanceRes.data);
        } catch (error) {
            console.error('Failed to fetch developer data:', error);
            toast.error('Failed to load system data');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    // Toggle function removed - use dedicated maintenance page for control

    if (isLoading && !stats) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-500"></div>
            </div>
        );
    }

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-2">
                        <Terminal className="h-8 w-8 text-purple-400" />
                        Developer Console
                    </h1>
                    <p className="text-slate-400 mt-1">Full system overview and control panel.</p>
                </div>
                <div className="flex gap-3">
                    <Button
                        variant="outline"
                        onClick={fetchData}
                        className="bg-slate-900 border-slate-700 text-slate-300 hover:bg-slate-800"
                    >
                        <RefreshCw className="h-4 w-4 mr-2" />
                        Refresh Data
                    </Button>
                </div>
            </div>

            {/* Status Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-wider">System Status</CardTitle>
                        <Activity className="h-4 w-4 text-green-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold flex items-center gap-2">
                            <span className="h-3 w-3 rounded-full bg-green-500 animate-pulse"></span>
                            Healthy
                        </div>
                        <p className="text-xs text-slate-500 mt-1 font-mono">Backend API v1.0.0</p>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-wider">Database Size</CardTitle>
                        <Database className="h-4 w-4 text-blue-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.database_size_mb || '0'} MB</div>
                        <p className="text-xs text-slate-500 mt-1 font-mono">PostgreSQL @ Supabase</p>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-wider">Active Sessions</CardTitle>
                        <Brain className="h-4 w-4 text-purple-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.active_sessions || '0'}</div>
                        <p className="text-xs text-slate-500 mt-1 font-mono">In-progress sessions</p>
                    </CardContent>
                </Card>

                <Card className={`bg-slate-900 border-slate-800 text-white ${maintenance?.is_active ? 'ring-2 ring-yellow-500/50' : ''}`}>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-wider">Maintenance</CardTitle>
                        <Lock className={`h-4 w-4 ${maintenance?.is_active ? 'text-yellow-400' : 'text-slate-600'}`} />
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div className="text-2xl font-bold uppercase">{maintenance?.is_active ? 'ON' : 'OFF'}</div>
                            <p className="text-xs text-slate-500 font-mono">Login blocker system</p>
                            <Button
                                size="sm"
                                variant="outline"
                                className="w-full h-7 text-[10px] font-bold bg-slate-800 border-slate-700 hover:bg-slate-700"
                                onClick={() => window.location.href = '/developer/maintenance'}
                            >
                                Configure →
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* System Breakdown */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="bg-slate-900 border-slate-800 text-white md:col-span-2">
                    <CardHeader>
                        <CardTitle>Global Metrics</CardTitle>
                        <CardDescription className="text-slate-500">Live data from across the platform database.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
                            <div className="space-y-1">
                                <p className="text-sm text-slate-500">Total Users</p>
                                <p className="text-3xl font-bold text-white">{stats?.total_users || 0}</p>
                                <div className="flex gap-2 text-[10px]">
                                    <span className="text-blue-400 font-mono">{stats?.total_students || 0} Students</span>
                                    <span className="text-indigo-400 font-mono">{stats?.total_admins || 0} Admins</span>
                                </div>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-slate-500">Assessment Data</p>
                                <p className="text-3xl font-bold text-white">{stats?.total_tests || 0}</p>
                                <p className="text-[10px] text-green-400 font-mono italic">{stats?.total_questions || 0} Questions Total</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-slate-500">Historical Results</p>
                                <p className="text-3xl font-bold text-white">{stats?.total_results || 0}</p>
                                <p className="text-[10px] text-slate-400 font-mono">Completed since launch</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-slate-500">Revenue Queue</p>
                                <p className="text-3xl font-bold text-white text-yellow-500">{stats?.pending_payments || 0}</p>
                                <p className="text-[10px] text-yellow-600 font-mono uppercase font-bold">Pending bKash</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Shield className="h-5 w-5 text-purple-400" />
                            Portal Navigation
                        </CardTitle>
                        <CardDescription className="text-slate-500">Access developer tools and monitoring</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <Button className="w-full justify-start font-mono text-xs uppercase bg-slate-800 hover:bg-slate-700 border border-slate-700 h-10" onClick={() => (window.location.href = '/developer/maintenance')}>
                            <Lock className="h-4 w-4 mr-2" />
                            Maintenance Control
                        </Button>
                        <Button className="w-full justify-start font-mono text-xs uppercase bg-slate-800 hover:bg-slate-700 border border-slate-700 h-10" onClick={() => (window.location.href = '/developer/database')}>
                            <Database className="h-4 w-4 mr-2" />
                            Database Inspector
                        </Button>
                        <Button className="w-full justify-start font-mono text-xs uppercase bg-slate-800 hover:bg-slate-700 border border-slate-700 h-10" onClick={() => (window.location.href = '/developer/stats')}>
                            <Activity className="h-4 w-4 mr-2" />
                            System Stats
                        </Button>
                        <div className="pt-2 space-y-2">
                            <p className="px-2 mb-1 text-[10px] font-semibold text-slate-500 uppercase tracking-widest">Testing Portals</p>
                            <Button className="w-full justify-start font-mono text-[10px] uppercase bg-indigo-900/20 hover:bg-indigo-900/40 border border-indigo-500/30 text-indigo-300 h-9" onClick={() => (window.location.href = '/admin/dashboard')}>
                                <Shield className="h-3.5 w-3.5 mr-2" />
                                User Management (Admin)
                            </Button>
                            <Button className="w-full justify-start font-mono text-[10px] uppercase bg-blue-900/20 hover:bg-blue-900/40 border border-blue-500/30 text-blue-300 h-9" onClick={() => (window.location.href = '/dashboard')}>
                                <Eye className="h-3.5 w-3.5 mr-2" />
                                Student Portal
                            </Button>
                        </div>
                        <div className="pt-4 border-t border-slate-800 mt-4">
                            <div className="bg-blue-950/20 border border-blue-900/40 p-3 rounded-md">
                                <p className="text-[10px] font-bold text-blue-400 flex items-center gap-1 mb-1 uppercase tracking-widest">
                                    <AlertCircle className="h-3 w-3" />
                                    Read-Only Portal
                                </p>
                                <p className="text-[10px] text-blue-300">This portal is for monitoring only. Critical system changes require master developer access.</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

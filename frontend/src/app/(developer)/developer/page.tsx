'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge'; // Added Badge import
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
    RefreshCw,
    Settings, // Added Settings import
    Eye
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
                <Card className="bg-slate-900 border-slate-800 text-white group hover:border-green-500/30 transition-all">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-widest">System Health</CardTitle>
                        <Activity className="h-4 w-4 text-green-400 group-hover:animate-pulse" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold flex items-center gap-2">
                            <span className="h-2.5 w-2.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span>
                            Operational
                        </div>
                        <p className="text-[10px] text-slate-500 mt-2 font-mono uppercase tracking-tighter">API V1.0 • CLOUD NODES ACTIVE</p>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white group hover:border-blue-500/30 transition-all">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-widest">Database</CardTitle>
                        <Database className="h-4 w-4 text-blue-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.database_size_mb || '0'} MB</div>
                        <p className="text-[10px] text-slate-500 mt-2 font-mono uppercase tracking-tighter">PostgreSQL @ Supabase</p>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white group hover:border-purple-500/30 transition-all">
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-widest">Active Users</CardTitle>
                        <Users className="h-4 w-4 text-purple-400" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.active_sessions || '0'}</div>
                        <p className="text-[10px] text-slate-500 mt-2 font-mono uppercase tracking-tighter cursor-pointer hover:text-purple-400" onClick={() => window.location.href = '/developer/monitoring/realtime'}>View Live Map →</p>
                    </CardContent>
                </Card>

                <Card className={`bg-slate-900 border-slate-800 text-white transition-all ${maintenance?.is_active ? 'ring-1 ring-yellow-500/50 border-yellow-500/20' : 'hover:border-slate-700'}`}>
                    <CardHeader className="flex flex-row items-center justify-between pb-2">
                        <CardTitle className="text-sm font-medium text-slate-400 uppercase tracking-widest">Maintenance</CardTitle>
                        <Lock className={`h-4 w-4 ${maintenance?.is_active ? 'text-yellow-400' : 'text-slate-600'}`} />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold uppercase">{maintenance?.is_active ? 'ACTIVE' : 'INACTIVE'}</div>
                        <Button
                            size="sm"
                            variant="ghost"
                            className="w-full h-6 text-[9px] font-bold bg-slate-800/50 border border-slate-700 mt-2 hover:bg-slate-800"
                            onClick={() => window.location.href = '/developer/maintenance'}
                        >
                            CONFIGURE GATEWAY →
                        </Button>
                    </CardContent>
                </Card>
            </div>

            {/* Monitoring Section */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="bg-slate-900 border-slate-800 text-white md:col-span-2 shadow-2xl">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Activity className="h-5 w-5 text-indigo-400" />
                            Platform Pulse Indices
                        </CardTitle>
                        <CardDescription className="text-slate-500">Live monitoring data and aggregated metrics.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
                            <div className="space-y-1">
                                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Total Population</p>
                                <p className="text-3xl font-black text-white">{stats?.total_users || 0}</p>
                                <div className="flex gap-2 text-[10px] font-mono">
                                    <span className="text-blue-400">{stats?.total_students || 0}S</span>
                                    <span className="text-purple-400">{stats?.total_admins || 0}A</span>
                                </div>
                            </div>
                            <div className="space-y-1">
                                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Academic Assets</p>
                                <p className="text-3xl font-black text-white">{stats?.total_tests || 0}</p>
                                <p className="text-[10px] text-green-500 font-bold uppercase tracking-tighter">{stats?.total_questions || 0} Items</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Evaluation Logs</p>
                                <p className="text-3xl font-black text-white">{stats?.total_results || 0}</p>
                                <p className="text-[10px] text-slate-600 font-mono tracking-tighter">Processed</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Revenue Queue</p>
                                <p className="text-3xl font-black text-yellow-500">{stats?.pending_payments || 0}</p>
                                <p className="text-[10px] text-yellow-600 font-bold uppercase tracking-widest animate-pulse">Pending</p>
                            </div>
                        </div>

                        <div className="mt-8 pt-6 border-t border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <Button variant="outline" className="h-20 bg-slate-950 border-slate-800 hover:bg-slate-800 flex flex-col items-center justify-center gap-1 group" onClick={() => window.location.href = '/developer/monitoring/realtime'}>
                                <Activity className="h-5 w-5 text-indigo-400 group-hover:scale-110 transition-transform" />
                                <span className="text-[9px] font-bold uppercase tracking-widest">Real-time Dashboard</span>
                            </Button>
                            <Button variant="outline" className="h-20 bg-slate-950 border-slate-800 hover:bg-slate-800 flex flex-col items-center justify-center gap-1 group" onClick={() => window.location.href = '/developer/monitoring/analytics'}>
                                <Brain className="h-5 w-5 text-purple-400 group-hover:scale-110 transition-transform" />
                                <span className="text-[9px] font-bold uppercase tracking-widest">Intelligence Toolkit</span>
                            </Button>
                            <Button variant="outline" className="h-20 bg-slate-950 border-slate-800 hover:bg-slate-800 flex flex-col items-center justify-center gap-1 group" onClick={() => window.location.href = '/developer/monitoring/login-logs'}>
                                <Shield className="h-5 w-5 text-blue-400 group-hover:scale-110 transition-transform" />
                                <span className="text-[9px] font-bold uppercase tracking-widest">Security Archives</span>
                            </Button>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-slate-900 border-slate-800 text-white shadow-2xl">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Terminal className="h-5 w-5 text-purple-400" />
                            Command Center
                        </CardTitle>
                        <CardDescription className="text-slate-500 text-xs">Direct access to core subsystems.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-2">
                        <Button className="w-full justify-start font-mono text-[10px] uppercase bg-slate-950 hover:bg-slate-800 border border-slate-800 h-11 group" onClick={() => (window.location.href = '/developer/database')}>
                            <Database className="h-4 w-4 mr-3 text-blue-500 group-hover:scale-110 transition-transform" />
                            Database Inspector
                        </Button>
                        <Button className="w-full justify-start font-mono text-[10px] uppercase bg-slate-950 hover:bg-slate-800 border border-slate-800 h-11 group" onClick={() => (window.location.href = '/developer/feature-flags')}>
                            <Settings className="h-4 w-4 mr-3 text-purple-500 group-hover:rotate-45 transition-transform" />
                            Feature Flags
                        </Button>
                        <Button className="w-full justify-start font-mono text-[10px] uppercase bg-slate-950 hover:bg-slate-800 border border-slate-800 h-11 group" onClick={() => (window.location.href = '/developer/monitoring/users')}>
                            <Users className="h-4 w-4 mr-3 text-indigo-500 group-hover:scale-110 transition-transform" />
                            User Monitoring
                        </Button>

                        <div className="pt-4 mt-4 border-t border-slate-800">
                            <p className="px-1 mb-2 text-[9px] font-black text-slate-600 uppercase tracking-widest">Testing Portals</p>
                            <div className="flex gap-2">
                                <Button className="flex-1 font-mono text-[9px] uppercase bg-indigo-900/10 hover:bg-indigo-900/30 border border-indigo-500/20 text-indigo-400 h-9" onClick={() => (window.location.href = '/admin/dashboard')}>
                                    Admin View
                                </Button>
                                <Button className="flex-1 font-mono text-[9px] uppercase bg-blue-900/10 hover:bg-blue-900/30 border border-blue-500/20 text-blue-400 h-9" onClick={() => (window.location.href = '/dashboard')}>
                                    Student View
                                </Button>
                            </div>
                        </div>

                        <div className="mt-6 bg-indigo-950/20 border border-indigo-900/40 p-4 rounded-xl">
                            <div className="flex items-center gap-2 mb-2 text-indigo-400">
                                <Shield className="h-4 w-4" />
                                <span className="text-[10px] font-black uppercase tracking-widest">Developer Access</span>
                            </div>
                            <p className="text-[10px] text-indigo-300 leading-relaxed italic">You are currently in monitoring mode. All platform interactions across these tools are strictly read-only for security integrity.</p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

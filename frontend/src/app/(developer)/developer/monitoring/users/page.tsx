'use client';

import { useEffect, useState, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import {
    Users,
    Search,
    ChevronRight,
    History,
    MousePointer2,
    Lock,
    Globe,
    Calendar,
    ArrowLeft,
    ShieldCheck,
    Smartphone,
    Monitor,
    Clock,
    UserCircle
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';
import { format, formatDistanceToNow } from 'date-fns';

interface UserRecord {
    id: string | number;
    username: string;
    full_name: string;
    email: string;
    last_login: string;
}

interface LoginLog {
    id: string;
    timestamp: string;
    ip_address: string;
    device_model: string;
    device_type: string;
    browser: string;
    os: string;
    status: string;
    failure_reason: string;
}

interface PageVisit {
    id: string;
    timestamp: string;
    url_path: string;
    page_title: string;
    time_spent: number;
}

interface UserDetail extends UserRecord {
    login_history: LoginLog[];
    recent_visits: PageVisit[];
    role: string;
    is_active: boolean;
}

export default function UserMonitoring() {
    const [users, setUsers] = useState<UserRecord[]>([]);
    const [selectedUser, setSelectedUser] = useState<UserDetail | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [isDetailLoading, setIsDetailLoading] = useState(false);
    const [search, setSearch] = useState('');

    const fetchUsers = useCallback(async () => {
        setIsLoading(true);
        try {
            const res = await api.get(`/system/user-monitoring/?search=${search}`);
            setUsers(res.data);
        } catch (error) {
            console.error('Failed to fetch users:', error);
            toast.error('Failed to load student directory');
        } finally {
            setIsLoading(false);
        }
    }, [search]);

    const fetchUserDetail = async (userId: string | number) => {
        setIsDetailLoading(true);
        try {
            const res = await api.get(`/system/user-monitoring/${userId}/`);
            setSelectedUser(res.data);
        } catch (error) {
            console.error('Failed to fetch user detail:', error);
            toast.error('Failed to load user intelligence data');
        } finally {
            setIsDetailLoading(false);
        }
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchUsers();
        }, 300);
        return () => clearTimeout(timer);
    }, [fetchUsers]);

    const getDeviceIcon = (type: string) => {
        switch (type?.toLowerCase()) {
            case 'mobile': return <Smartphone className="h-4 w-4" />;
            case 'desktop': return <Monitor className="h-4 w-4" />;
            default: return <UserCircle className="h-4 w-4" />;
        }
    };

    if (selectedUser) {
        return (
            <div className="space-y-6">
                <div className="flex items-center gap-4">
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setSelectedUser(null)}
                        className="text-slate-400 hover:text-white"
                    >
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back to List
                    </Button>
                    <h1 className="text-2xl font-bold flex items-center gap-2">
                        <Badge variant="outline" className="bg-indigo-500/10 text-indigo-400 border-indigo-500/20 font-mono">
                            USER INTEL
                        </Badge>
                        {selectedUser.full_name}
                    </h1>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Profile Summary */}
                    <Card className="bg-slate-900 border-slate-800 text-white lg:col-span-1">
                        <CardHeader className="flex flex-col items-center border-b border-slate-800 pb-6">
                            <div className="h-20 w-20 rounded-2xl bg-indigo-600 flex items-center justify-center text-3xl font-black mb-4 shadow-xl shadow-indigo-900/20">
                                {selectedUser.username.charAt(0).toUpperCase()}
                            </div>
                            <CardTitle>{selectedUser.username}</CardTitle>
                            <CardDescription className="text-slate-500">@{selectedUser.id}</CardDescription>
                            <div className="flex gap-2 mt-4">
                                <Badge className="bg-blue-500/10 text-blue-400 border-blue-500/20 uppercase text-[9px]">
                                    {selectedUser.role}
                                </Badge>
                                <Badge className={selectedUser.is_active ? 'bg-green-500/10 text-green-400 border-green-500/20 uppercase text-[9px]' : 'bg-red-500/10 text-red-400 border-red-500/20 uppercase text-[9px]'}>
                                    {selectedUser.is_active ? 'Active' : 'Locked'}
                                </Badge>
                            </div>
                        </CardHeader>
                        <CardContent className="pt-6 space-y-4">
                            <div className="space-y-1">
                                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Email Address</p>
                                <p className="text-sm font-mono text-slate-300">{selectedUser.email}</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Last Access</p>
                                <p className="text-sm text-slate-300">
                                    {selectedUser.last_login ? format(new Date(selectedUser.last_login), 'PPP p') : 'Never'}
                                </p>
                            </div>
                            <div className="pt-4 border-t border-slate-800">
                                <div className="bg-slate-950 p-3 rounded-lg border border-slate-800">
                                    <p className="text-[10px] font-bold text-slate-500 uppercase flex items-center gap-1.5 mb-2">
                                        <ShieldCheck className="h-3 w-3 text-indigo-400" />
                                        Monitoring Status
                                    </p>
                                    <p className="text-[11px] text-slate-400 italic">This user is currently under active system monitoring. All page visits and login attempts are logged for security.</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Activity Intel */}
                    <div className="lg:col-span-2 space-y-6">
                        {/* Login History */}
                        <Card className="bg-slate-900 border-slate-800 text-white">
                            <CardHeader className="flex flex-row items-center gap-2 border-b border-slate-800 pb-4">
                                <History className="h-5 w-5 text-indigo-400" />
                                <div className="flex-1">
                                    <CardTitle className="text-base">Authentication History</CardTitle>
                                    <CardDescription className="text-slate-500">Recent login attempts and device vectors.</CardDescription>
                                </div>
                            </CardHeader>
                            <CardContent className="p-0">
                                <div className="divide-y divide-slate-800">
                                    {selectedUser.login_history.length > 0 ? (
                                        selectedUser.login_history.map((log) => (
                                            <div key={log.id} className="p-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors">
                                                <div className="flex items-center gap-4">
                                                    <div className={`h-8 w-8 rounded-lg flex items-center justify-center ${log.status === 'success' ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                                                        {getDeviceIcon(log.device_type)}
                                                    </div>
                                                    <div>
                                                        <div className="flex items-center gap-2">
                                                            <span className="text-xs font-bold text-slate-200">{log.device_model || 'Generic Node'}</span>
                                                            <span className="text-[10px] text-slate-500 font-mono">@{log.ip_address}</span>
                                                        </div>
                                                        <p className="text-[10px] text-slate-500">{log.os} • {log.browser}</p>
                                                    </div>
                                                </div>
                                                <div className="text-right">
                                                    <p className="text-xs font-mono text-slate-300">{formatDistanceToNow(new Date(log.timestamp), { addSuffix: true })}</p>
                                                    <Badge className={log.status === 'success' ? 'bg-green-500/10 text-green-400 border-green-500/20 text-[8px] uppercase h-4' : 'bg-red-500/10 text-red-500 border-red-500/20 text-[8px] uppercase h-4'}>
                                                        {log.status === 'success' ? 'AUTHORIZED' : 'DENIED'}
                                                    </Badge>
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="p-8 text-center text-slate-600 text-sm font-mono tracking-widest uppercase italic">NO RECENT AUTH LOGS FOUND</div>
                                    )}
                                </div>
                            </CardContent>
                        </Card>

                        {/* Recent Page Interactions */}
                        <Card className="bg-slate-900 border-slate-800 text-white">
                            <CardHeader className="flex flex-row items-center gap-2 border-b border-slate-800 pb-4">
                                <MousePointer2 className="h-5 w-5 text-blue-400" />
                                <div className="flex-1">
                                    <CardTitle className="text-base">Interaction Pulse</CardTitle>
                                    <CardDescription className="text-slate-500">Real-time page visit stream and dwell time.</CardDescription>
                                </div>
                            </CardHeader>
                            <CardContent className="p-0">
                                <div className="divide-y divide-slate-800">
                                    {selectedUser.recent_visits.length > 0 ? (
                                        selectedUser.recent_visits.map((visit) => (
                                            <div key={visit.id} className="p-4 flex items-center justify-between hover:bg-slate-800/30 transition-colors">
                                                <div className="flex items-center gap-4">
                                                    <div className="h-8 w-8 rounded-lg bg-blue-500/10 text-blue-400 flex items-center justify-center">
                                                        <Globe className="h-4 w-4" />
                                                    </div>
                                                    <div>
                                                        <p className="text-sm font-bold text-indigo-300">{visit.page_title || 'Untitled Page'}</p>
                                                        <p className="text-[10px] font-mono text-slate-500">{visit.url_path}</p>
                                                    </div>
                                                </div>
                                                <div className="text-right">
                                                    <div className="flex items-center gap-1.5 justify-end mb-1">
                                                        <Clock className="h-3 w-3 text-slate-600" />
                                                        <span className="text-[10px] text-slate-400 font-mono tracking-tighter">
                                                            {format(new Date(visit.timestamp), 'HH:mm:ss')}
                                                        </span>
                                                    </div>
                                                    <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest">
                                                        {visit.time_spent ? `${visit.time_spent}s` : 'PASSING'}
                                                    </p>
                                                </div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="p-8 text-center text-slate-600 text-sm font-mono tracking-widest uppercase italic">NO INTERACTION DATA RECORDED</div>
                                    )}
                                </div>
                            </CardContent>
                        </Card>
                    </div>
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
                        Target Directory
                    </h1>
                    <p className="text-slate-400 mt-1">Select a student record to initiate deep activity analysis.</p>
                </div>
                <div className="relative w-full md:w-64">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                    <Input
                        placeholder="Search by identity..."
                        className="pl-9 bg-slate-900 border-slate-700 text-white placeholder:text-slate-600"
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                    />
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {isLoading ? (
                    Array(6).fill(0).map((_, i) => (
                        <Card key={i} className="bg-slate-900/50 border-slate-800 h-24 animate-pulse" />
                    ))
                ) : users.length > 0 ? (
                    users.map((user) => (
                        <Card
                            key={user.id}
                            className="bg-slate-900 border-slate-800 text-white hover:border-indigo-500/50 hover:bg-slate-800/50 transition-all cursor-pointer group"
                            onClick={() => fetchUserDetail(user.id)}
                        >
                            <CardContent className="p-4 flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className="h-12 w-12 rounded-xl bg-slate-800 flex items-center justify-center text-lg font-black group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                                        {user.username.charAt(0).toUpperCase()}
                                    </div>
                                    <div className="overflow-hidden">
                                        <p className="font-bold truncate">{user.full_name}</p>
                                        <p className="text-xs text-slate-500 font-mono truncate">@{user.username}</p>
                                    </div>
                                </div>
                                <ChevronRight className="h-5 w-5 text-slate-700 group-hover:text-indigo-400 transition-colors" />
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <div className="col-span-full py-12 text-center">
                        <UserCircle className="h-12 w-12 text-slate-800 mx-auto mb-4" />
                        <p className="text-slate-500 font-medium">No students found in directory.</p>
                    </div>
                )}
            </div>
        </div>
    );
}

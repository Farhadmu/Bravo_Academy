'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import {
    Lock,
    ShieldCheck,
    AlertCircle,
    Save,
    Users,
    Shield,
    AlertTriangle,
    Terminal,
    History
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';

interface MaintenanceConfig {
    is_active: boolean;
    target_roles: string[];
    message: string;
    updated_at?: string;
    updated_by_username?: string;
}

export default function MaintenanceControl() {
    const [config, setConfig] = useState<MaintenanceConfig | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchConfig = async () => {
        try {
            const res = await api.get('/system/maintenance/current/');
            setConfig(res.data);
        } catch (error) {
            toast.error('Failed to load maintenance configuration');
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchConfig();
    }, []);

    if (isLoading) {
        return <div className="animate-pulse space-y-4">
            <div className="h-40 bg-slate-900 rounded-lg"></div>
            <div className="h-80 bg-slate-900 rounded-lg"></div>
        </div>;
    }

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Lock className="h-8 w-8 text-yellow-500" />
                        Maintenance Mode
                    </h1>
                    <p className="text-slate-400 mt-1">Status of system access and maintenance protocols.</p>
                </div>
                <div className="flex items-center gap-4 bg-slate-900 px-4 py-2 rounded-lg border border-slate-800">
                    <Label htmlFor="global-status" className="font-mono text-xs font-bold uppercase tracking-wider">GLOBAL LOCK</Label>
                    <Switch
                        id="global-status"
                        checked={config?.is_active}
                        disabled
                        className="data-[state=checked]:bg-yellow-500 opacity-50 cursor-not-allowed"
                    />
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 space-y-6">
                    {/* Status Card */}
                    <Card className={`bg-slate-900 border-slate-800 text-white ${config?.is_active ? 'ring-2 ring-yellow-500/30' : ''}`}>
                        <CardHeader>
                            <CardTitle>Display Message</CardTitle>
                            <CardDescription className="text-slate-500">Current message shown to users when they try to login.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="space-y-2">
                                <Label className="text-xs uppercase tracking-widest text-slate-500">System Message</Label>
                                <div className="min-h-[100px] p-4 bg-slate-950 border border-slate-800 rounded-lg text-slate-300 font-mono text-sm whitespace-pre-wrap">
                                    {config?.message || 'No maintenance message set.'}
                                </div>
                            </div>

                            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg">
                                <p className="text-[10px] font-bold text-slate-500 mb-2 uppercase tracking-tighter">Login Screen Preview</p>
                                <div className="border border-dashed border-slate-800 p-6 flex flex-col items-center justify-center text-center">
                                    <AlertCircle className="h-10 w-10 text-yellow-500 mb-3" />
                                    <h2 className="text-xl font-bold mb-2">Maintenance Mode</h2>
                                    <p className="text-slate-400 max-w-sm italic">{config?.message || 'The system is currently under maintenance...'}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Target Roles */}
                    <Card className="bg-slate-900 border-slate-800 text-white">
                        <CardHeader>
                            <CardTitle>System Lock Targets</CardTitle>
                            <CardDescription className="text-slate-500">User roles currently blocked from signing in.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                                {[
                                    { id: 'student', label: 'Students', icon: Users, color: 'text-blue-400' },
                                    { id: 'staff', label: 'Staff', icon: Shield, color: 'text-indigo-400' },
                                    { id: 'admin', label: 'Admins', icon: ShieldCheck, color: 'text-green-400' }
                                ].map((role) => (
                                    <div
                                        key={role.id}
                                        className={`
                                            flex flex-col items-center justify-center p-6 border rounded-xl transition-all
                                            ${config?.target_roles.includes(role.id)
                                                ? 'bg-yellow-500/10 border-yellow-500/50 shadow-[0_0_15px_rgba(234,179,8,0.1)]'
                                                : 'bg-slate-950 border-slate-800 opacity-50'}
                                        `}
                                    >
                                        <role.icon className={`h-8 w-8 mb-3 ${config?.target_roles.includes(role.id) ? 'text-yellow-500' : role.color}`} />
                                        <span className={`font-bold uppercase text-xs tracking-widest ${config?.target_roles.includes(role.id) ? 'text-yellow-500' : 'text-slate-500'}`}>
                                            {role.label}
                                        </span>
                                        {config?.target_roles.includes(role.id) && (
                                            <span className="mt-2 text-[10px] bg-yellow-500 text-black px-2 py-0.5 rounded font-black uppercase">Blocked</span>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>
                </div>

                <div className="space-y-6">
                    <Card className="bg-slate-900 border-slate-800 text-white h-fit">
                        <CardHeader>
                            <CardTitle className="text-sm font-mono uppercase tracking-widest">Global Status</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="bg-slate-950 p-4 border border-slate-800 rounded-lg text-center">
                                <p className="text-[10px] text-slate-500 font-bold uppercase mb-1">Current State</p>
                                <p className={`text-xl font-black uppercase ${config?.is_active ? 'text-yellow-500 animate-pulse' : 'text-slate-700'}`}>
                                    {config?.is_active ? 'SYSTEM LOCKED' : 'ONLINE'}
                                </p>
                            </div>
                            <div className="p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg text-xs text-blue-400 text-center font-bold">
                                🔒 VIEW ONLY ACCESS
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-slate-900 border-slate-800 text-white h-fit">
                        <CardHeader>
                            <CardTitle className="text-sm font-mono uppercase tracking-widest">Information</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4 text-sm text-slate-400">
                            <div className="flex items-start gap-3">
                                <Terminal className="h-5 w-5 text-purple-400 flex-shrink-0" />
                                <p>Developers are <span className="text-white font-bold">exempt</span> from maintenance locks.</p>
                            </div>
                            <div className="flex items-start gap-3">
                                <AlertTriangle className="h-5 w-5 text-yellow-500 flex-shrink-0" />
                                <p>Access is restricted to <span className="text-yellow-500 font-bold underline">Read-Only</span> for audit security.</p>
                            </div>
                            <div className="pt-4 border-t border-slate-800 flex items-center gap-2 text-xs font-mono">
                                <History className="h-3 w-3" />
                                Last Status: {config?.updated_at ? new Date(config.updated_at).toLocaleTimeString() : 'Never'}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}

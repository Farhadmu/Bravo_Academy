'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import {
    Flag,
    Plus,
    Trash2,
    Search,
    RefreshCw,
    Terminal,
    Shield,
    Users,
    Info
} from 'lucide-react';
import api from '@/lib/api';
import { toast } from 'sonner';

interface FeatureFlag {
    id: string;
    name: string;
    description: string;
    is_enabled: boolean;
    enabled_for_roles: string[];
}

export default function FeatureFlags() {
    const [flags, setFlags] = useState<FeatureFlag[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    const fetchFlags = async () => {
        setIsLoading(true);
        try {
            const res = await api.get('/system/feature-flags/');
            setFlags(res.data);
        } catch (error) {
            toast.error('Failed to load feature flags');
        } finally {
            setIsLoading(false);
        }
    };

    // Mutation operations removed - this is now a read-only monitor

    useEffect(() => {
        fetchFlags();
    }, []);

    const filteredFlags = flags.filter(f =>
        f.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        f.description.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="space-y-8">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Flag className="h-8 w-8 text-indigo-400" />
                        Feature Flags Monitor
                    </h1>
                    <p className="text-slate-400 mt-1">View current feature flag states (read-only).</p>
                </div>
            </div>

            {/* Filter */}
            <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                <Input
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    placeholder="Search flags..."
                    className="pl-10 bg-slate-900 border-slate-800 text-white"
                />
            </div>



            {/* Flags Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {isLoading ? (
                    Array(6).fill(0).map((_, i) => (
                        <div key={i} className="h-48 bg-slate-900 animate-pulse rounded-xl border border-slate-800"></div>
                    ))
                ) : filteredFlags.length > 0 ? (
                    filteredFlags.map((flag) => (
                        <Card key={flag.id} className={`bg-slate-900 border-slate-800 hover:border-indigo-500/30 transition-all ${flag.is_enabled ? 'ring-1 ring-indigo-500/20 shadow-lg shadow-indigo-900/10' : 'opacity-60'}`}>
                            <CardHeader className="pb-2">
                                <div className="space-y-1">
                                    <div className="flex items-center gap-2">
                                        <CardTitle className="text-white font-mono text-sm uppercase tracking-wider">{flag.name}</CardTitle>
                                        {flag.is_enabled ? (
                                            <span className="text-[10px] bg-green-500/10 text-green-400 px-1.5 py-0.5 rounded border border-green-500/20 font-bold">ENABLED</span>
                                        ) : (
                                            <span className="text-[10px] bg-slate-500/10 text-slate-400 px-1.5 py-0.5 rounded border border-slate-500/20 font-bold">DISABLED</span>
                                        )}
                                    </div>
                                    <CardDescription className="text-slate-400 text-xs line-clamp-2 h-8">{flag.description || 'No description provided.'}</CardDescription>
                                </div>
                            </CardHeader>
                            <CardContent className="pt-4 border-t border-slate-800">
                                <div className="flex items-center gap-1 text-[10px] text-slate-500">
                                    <Users className="h-3 w-3" />
                                    {flag.enabled_for_roles.length > 0 ? flag.enabled_for_roles.join(', ') : 'All Roles'}
                                </div>
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <div className="col-span-full py-20 text-center text-slate-600">
                        <Flag className="h-16 w-16 mx-auto mb-4 opacity-20" />
                        <p className="text-lg">No feature flags found.</p>
                    </div>
                )}
            </div>

            {/* Read-Only Notice */}
            <div className="p-4 bg-blue-950/20 border border-blue-900/40 rounded-xl flex gap-3">
                <Info className="h-5 w-5 text-blue-400 flex-shrink-0" />
                <div className="text-xs text-blue-300">
                    <p className="font-bold uppercase tracking-widest mb-1">Read-Only Monitor</p>
                    <p>This page displays current feature flag status for monitoring purposes. Feature flag management requires admin access.</p>
                </div>
            </div>
        </div>
    );
}

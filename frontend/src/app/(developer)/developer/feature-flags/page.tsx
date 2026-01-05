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
    const [isCreating, setIsCreating] = useState(false);
    const [newFlag, setNewFlag] = useState({ name: '', description: '' });

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

    const toggleFlag = async (id: string) => {
        try {
            const res = await api.post(`/system/feature-flags/${id}/toggle/`);
            setFlags(flags.map(f => f.id === id ? res.data : f));
            toast.success(`Feature "${res.data.name}" ${res.data.is_enabled ? 'Enabled' : 'Disabled'}`);
        } catch (error) {
            toast.error('Failed to toggle feature flag');
        }
    };

    const deleteFlag = async (id: string) => {
        if (!confirm('Are you sure you want to delete this feature flag?')) return;
        try {
            await api.delete(`/system/feature-flags/${id}/`);
            setFlags(flags.filter(f => f.id !== id));
            toast.success('Feature flag deleted');
        } catch (error) {
            toast.error('Failed to delete feature flag');
        }
    };

    const createFlag = async () => {
        if (!newFlag.name) return;
        try {
            const res = await api.post('/system/feature-flags/', newFlag);
            setFlags([...flags, res.data]);
            setNewFlag({ name: '', description: '' });
            setIsCreating(false);
            toast.success('Feature flag created');
        } catch (error) {
            toast.error('Failed to create feature flag');
        }
    };

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
                        Feature Management
                    </h1>
                    <p className="text-slate-400 mt-1">Deploy changes without code by toggling features live.</p>
                </div>
                <div className="flex gap-2">
                    <Button onClick={() => setIsCreating(true)} className="bg-indigo-600 hover:bg-indigo-700">
                        <Plus className="h-4 w-4 mr-2" />
                        New Flag
                    </Button>
                    <Button variant="outline" onClick={fetchFlags} className="bg-slate-900 border-slate-700">
                        <RefreshCw className="h-4 w-4" />
                    </Button>
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

            {/* Create Modal Mock */}
            {isCreating && (
                <Card className="bg-slate-900 border-indigo-500/50 text-white animate-in zoom-in-95 duration-200">
                    <CardHeader>
                        <CardTitle>Create New Feature Flag</CardTitle>
                        <CardDescription>Give your feature a unique identifier and description.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label className="text-xs uppercase tracking-widest text-slate-500">Flag ID (Slug)</Label>
                                <Input
                                    value={newFlag.name}
                                    onChange={(e) => setNewFlag({ ...newFlag, name: e.target.value })}
                                    placeholder="e.g., enable_results_v2"
                                    className="bg-slate-950 border-slate-800"
                                />
                            </div>
                            <div className="space-y-2">
                                <Label className="text-xs uppercase tracking-widest text-slate-500">Description</Label>
                                <Input
                                    value={newFlag.description}
                                    onChange={(e) => setNewFlag({ ...newFlag, description: e.target.value })}
                                    placeholder="What does this feature do?"
                                    className="bg-slate-950 border-slate-800"
                                />
                            </div>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="ghost" onClick={() => setIsCreating(false)}>Cancel</Button>
                            <Button className="bg-indigo-600 hover:bg-indigo-700" onClick={createFlag}>Create Flag</Button>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Flags Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {isLoading ? (
                    Array(6).fill(0).map((_, i) => (
                        <div key={i} className="h-48 bg-slate-900 animate-pulse rounded-xl border border-slate-800"></div>
                    ))
                ) : filteredFlags.length > 0 ? (
                    filteredFlags.map((flag) => (
                        <Card key={flag.id} className={`bg-slate-900 border-slate-800 hover:border-indigo-500/30 transition-all ${flag.is_enabled ? 'ring-1 ring-indigo-500/20 shadow-lg shadow-indigo-900/10' : 'opacity-60'}`}>
                            <CardHeader className="flex flex-row items-start justify-between pb-2">
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
                                <Switch
                                    checked={flag.is_enabled}
                                    onCheckedChange={() => toggleFlag(flag.id)}
                                    className="data-[state=checked]:bg-indigo-600"
                                />
                            </CardHeader>
                            <CardContent className="pt-4 border-t border-slate-800">
                                <div className="flex items-center justify-between">
                                    <div className="flex gap-2">
                                        <div className="flex items-center gap-1 text-[10px] text-slate-500">
                                            <Users className="h-3 w-3" />
                                            {flag.enabled_for_roles.length > 0 ? flag.enabled_for_roles.join(', ') : 'All Roles'}
                                        </div>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="h-8 w-8 text-slate-500 hover:text-red-400 hover:bg-red-950/20"
                                        onClick={() => deleteFlag(flag.id)}
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <div className="col-span-full py-20 text-center text-slate-600">
                        <Flag className="h-16 w-16 mx-auto mb-4 opacity-20" />
                        <p className="text-lg">No feature flags found.</p>
                        <Button variant="link" className="text-indigo-400" onClick={() => setIsCreating(true)}>Create the first one</Button>
                    </div>
                )}
            </div>

            {/* Usage Tip */}
            <div className="p-4 bg-indigo-950/20 border border-indigo-900/40 rounded-xl flex gap-3">
                <Info className="h-5 w-5 text-indigo-400 flex-shrink-0" />
                <div className="text-xs text-indigo-300">
                    <p className="font-bold uppercase tracking-widest mb-1">Developer Implementation Helper</p>
                    <p className="mb-2">Use the following React hook pattern to consume these flags in the frontend:</p>
                    <pre className="bg-slate-950 p-3 rounded font-mono text-[10px] text-indigo-400 border border-indigo-900/30">
                        {`const { isEnabled } = useFeatureFlag('${flags[0]?.name || 'feature_name'}');\nif (isEnabled) return <NewFeature />;`}
                    </pre>
                </div>
            </div>
        </div>
    );
}

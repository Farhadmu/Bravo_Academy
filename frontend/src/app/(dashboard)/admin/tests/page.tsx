'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Plus, Trash2, Brain, AlertTriangle, Eye, Edit } from "lucide-react";
import api from '@/lib/api';
import { toast } from 'sonner';

interface Test {
    id: string;
    name: string;
    description: string;
    duration_minutes: number;
    total_questions: number;
    is_free: boolean;
    price: string;
    is_active: boolean;
    category: 'verbal' | 'non-verbal' | 'wat';
    created_at: string;
}

interface ConfirmDialog {
    open: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
    loading?: boolean;
}

export default function AdminTestsPage() {
    const router = useRouter();
    const [tests, setTests] = useState<Test[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [confirmDialog, setConfirmDialog] = useState<ConfirmDialog>({
        open: false,
        title: '',
        message: '',
        onConfirm: () => { }
    });

    useEffect(() => {
        fetchTests();
    }, []);

    const fetchTests = async () => {
        try {
            setLoading(true);
            const response = await api.get('/tests/tests/');
            // Handle pagination if present
            if (Array.isArray(response.data)) {
                setTests(response.data);
            } else if (response.data.results) {
                setTests(response.data.results);
            }
            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch tests", err);
            setError("Failed to load tests.");
            setLoading(false);
        }
    };

    const handleDelete = (id: string, name: string) => {
        setConfirmDialog({
            open: true,
            title: 'Delete Test',
            message: `Are you sure you want to delete "${name}"? This action cannot be undone.`,
            onConfirm: async () => {
                try {
                    setConfirmDialog(prev => ({ ...prev, loading: true }));
                    await api.delete(`/tests/tests/${id}/`);
                    setTests(prev => prev.filter(t => t.id !== id));
                    toast.success("Test deleted successfully.");
                } catch (err: any) {
                    const msg = err.response?.data?.detail || "Failed to delete test";
                    toast.error(msg);
                } finally {
                    setConfirmDialog(prev => ({ ...prev, open: false, loading: false }));
                }
            }
        });
    };

    if (loading && tests.length === 0) return <div className="flex justify-center p-8"><Loader2 className="animate-spin" /></div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold tracking-tight">Test Management</h1>
                <Button onClick={() => router.push('/admin/tests/new')} className="bg-blue-600 hover:bg-blue-700 text-white">
                    <Plus className="mr-2 h-4 w-4" /> Create New Test
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Brain className="h-5 w-5 text-blue-600" />
                        Available IQ Tests
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {error && (
                        <div className="bg-red-50 border border-red-100 text-red-600 p-4 rounded-md flex items-center gap-2 mb-4">
                            <AlertTriangle className="h-4 w-4" />
                            {error}
                        </div>
                    )}

                    <div className="rounded-md border overflow-x-auto">
                        <table className="w-full text-sm text-left min-w-[700px] md:min-w-full">
                            <thead className="bg-gray-50 border-b">
                                <tr>
                                    <th className="p-4 font-medium text-gray-500">Test Name</th>
                                    <th className="p-4 font-medium text-gray-500">Duration</th>
                                    <th className="p-4 font-medium text-gray-500">Questions</th>
                                    <th className="p-4 font-medium text-gray-500">Price</th>
                                    <th className="p-4 font-medium text-gray-500">Category</th>
                                    <th className="p-4 font-medium text-gray-500">Type</th>
                                    <th className="p-4 font-medium text-gray-500 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {tests.map((test) => (
                                    <tr key={test.id} className="border-b last:border-0 hover:bg-gray-50 transition-colors">
                                        <td className="p-4">
                                            <div className="font-medium text-gray-900">{test.name}</div>
                                            <div className="text-xs text-gray-500 mt-1 line-clamp-1">{test.description}</div>
                                        </td>
                                        <td className="p-4 text-gray-600">{test.duration_minutes} mins</td>
                                        <td className="p-4 text-gray-600">{test.total_questions} Qs</td>
                                        <td className="p-4 font-medium">
                                            {parseFloat(test.price) === 0 ? 'Free' : `৳${test.price}`}
                                        </td>
                                        <td className="p-4 text-gray-600">
                                            <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${test.category === 'verbal' ? 'bg-blue-100 text-blue-800' :
                                                    test.category === 'non-verbal' ? 'bg-purple-100 text-purple-800' :
                                                        'bg-amber-100 text-amber-800'
                                                }`}>
                                                {test.category === 'verbal' ? 'Verbal' :
                                                    test.category === 'non-verbal' ? 'Non-Verbal' : 'WAT'}
                                            </span>
                                        </td>
                                        <td className="p-4">
                                            {test.is_free ? (
                                                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                    Sample
                                                </span>
                                            ) : (
                                                <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                    Standard
                                                </span>
                                            )}
                                        </td>
                                        <td className="p-4 text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button variant="ghost" size="sm" onClick={() => router.push(`/admin/tests/${test.id}`)} className="text-blue-600 hover:text-blue-700 hover:bg-blue-50" title="View Details">
                                                    <Eye className="h-4 w-4" />
                                                </Button>
                                                <Button variant="ghost" size="sm" onClick={() => router.push(`/admin/tests/${test.id}/edit`)} className="text-amber-600 hover:text-amber-700 hover:bg-amber-50" title="Edit Test">
                                                    <Edit className="h-4 w-4" />
                                                </Button>
                                                <Button
                                                    variant="ghost"
                                                    size="sm"
                                                    onClick={() => handleDelete(test.id, test.name)}
                                                    className="text-red-600 hover:text-red-700 hover:bg-red-50"
                                                    title="Delete Test"
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                                {tests.length === 0 && (
                                    <tr>
                                        <td colSpan={6} className="p-8 text-center text-gray-500">
                                            <Brain className="h-10 w-10 mx-auto mb-2 text-gray-300 opacity-50" />
                                            No tests found. Click "Create New Test" to get started.
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>

            {/* Confirmation Modal */}
            {confirmDialog.open && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in zoom-in-95 duration-200">
                    <Card className="w-full max-w-md shadow-2xl border-none">
                        <CardHeader className="flex flex-row items-center gap-3 border-b pb-4">
                            <div className="p-2 rounded-full bg-red-100">
                                <Trash2 className="h-5 w-5 text-red-600" />
                            </div>
                            <CardTitle className="text-xl font-bold">{confirmDialog.title}</CardTitle>
                        </CardHeader>
                        <CardContent className="pt-6">
                            <p className="text-gray-600 leading-relaxed">
                                {confirmDialog.message}
                            </p>
                        </CardContent>
                        <div className="p-4 bg-gray-50 flex justify-end gap-3 rounded-b-lg border-t mt-4">
                            <Button variant="outline" onClick={() => setConfirmDialog(prev => ({ ...prev, open: false }))} disabled={confirmDialog.loading}>
                                Cancel
                            </Button>
                            <Button
                                variant="destructive"
                                onClick={confirmDialog.onConfirm}
                                disabled={confirmDialog.loading}
                            >
                                {confirmDialog.loading ? <Loader2 className="animate-spin mr-2 h-4 w-4" /> : null}
                                Confirm Delete
                            </Button>
                        </div>
                    </Card>
                </div>
            )}
        </div>
    );
}

"use client";

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Loader2, ArrowLeft, Save, Brain } from "lucide-react";
import api from '@/lib/api';
import { toast } from 'sonner';

export default function EditTestPage({ params }: { params: Promise<{ id: string }> }) {
    const router = useRouter();
    const { id } = use(params);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        category: 'verbal',
        duration_minutes: 30,
        total_questions: 100,
        price: '0.00',
        passing_score: 50,
        is_free_sample: false,
        is_active: true
    });

    useEffect(() => {
        if (id) {
            fetchTest();
        }
    }, [id]);

    const fetchTest = async () => {
        try {
            const res = await api.get(`/tests/tests/${id}/`);
            const { name, description, category, duration_minutes, total_questions, price, passing_score, is_free_sample, is_active } = res.data;
            setFormData({
                name: name || '',
                description: description || '',
                category: category || 'verbal',
                duration_minutes: duration_minutes || 0,
                total_questions: total_questions || 0,
                price: price || '0.00',
                passing_score: passing_score || 0,
                is_free_sample: !!is_free_sample,
                is_active: !!is_active
            });
            setLoading(false);
        } catch (err) {
            console.error(err);
            toast.error("Failed to load test details.");
            router.push('/admin/tests');
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value, type } = e.target as HTMLInputElement;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked :
                type === 'number' ? parseInt(value) : value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            setSaving(true);
            await api.patch(`/tests/tests/${id}/`, formData);
            toast.success("Test updated successfully.");
            router.push(`/admin/tests/${id}`);
        } catch (err: any) {
            console.error(err);
            const msg = err.response?.data?.detail || "Failed to update test.";
            toast.error(msg);
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div className="flex justify-center p-8"><Loader2 className="animate-spin" /></div>;

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <div className="flex items-center gap-4">
                <Button variant="ghost" size="icon" onClick={() => router.push(`/admin/tests/${id}`)}>
                    <ArrowLeft className="h-4 w-4" />
                </Button>
                <h1 className="text-3xl font-bold tracking-tight">Edit Test</h1>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Brain className="h-5 w-5 text-blue-600" />
                        Test Details
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="test-name">Test Name</Label>
                            <Input
                                id="test-name"
                                name="name"
                                value={formData.name}
                                onChange={handleChange}
                                placeholder="e.g., Advanced IQ Evaluation"
                                required
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="category">Category</Label>
                            <select
                                id="category"
                                name="category"
                                value={formData.category}
                                onChange={(e) => setFormData(p => ({ ...p, category: e.target.value as any }))}
                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                required
                            >
                                <option value="verbal">Verbal IQ</option>
                                <option value="non-verbal">Non-Verbal IQ</option>
                                <option value="wat">Word Association (WAT)</option>
                            </select>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="description">Description</Label>
                            <Textarea
                                id="description"
                                name="description"
                                value={formData.description}
                                onChange={handleChange}
                                placeholder="Describe the test..."
                                rows={4}
                            />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="duration">Duration (Minutes)</Label>
                                <Input
                                    id="duration"
                                    type="number"
                                    name="duration_minutes"
                                    value={formData.duration_minutes}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="total-questions">Total Questions</Label>
                                <Input
                                    id="total-questions"
                                    type="number"
                                    name="total_questions"
                                    value={formData.total_questions}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="price">Price (৳)</Label>
                                <Input
                                    id="price"
                                    type="text"
                                    name="price"
                                    value={formData.price}
                                    onChange={handleChange}
                                    placeholder="0.00"
                                    required
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="passing-score">Passing Score (%)</Label>
                                <Input
                                    id="passing-score"
                                    type="number"
                                    name="passing_score"
                                    value={formData.passing_score}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                        </div>

                        <div className="flex items-center gap-6 pt-4">
                            <label className="flex items-center gap-2 cursor-pointer">
                                <input
                                    type="checkbox"
                                    name="is_free_sample"
                                    checked={formData.is_free_sample}
                                    onChange={(e) => setFormData(p => ({ ...p, is_free_sample: e.target.checked }))}
                                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-600"
                                />
                                <span className="text-sm font-medium text-gray-700">Free Sample Test</span>
                            </label>

                            <label className="flex items-center gap-2 cursor-pointer">
                                <input
                                    type="checkbox"
                                    name="is_active"
                                    checked={formData.is_active}
                                    onChange={(e) => setFormData(p => ({ ...p, is_active: e.target.checked }))}
                                    className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-600"
                                />
                                <span className="text-sm font-medium text-gray-700">Active</span>
                            </label>
                        </div>

                        <div className="pt-6 flex justify-end gap-3">
                            <Button variant="outline" type="button" onClick={() => router.push(`/admin/tests/${id}`)}>
                                Cancel
                            </Button>
                            <Button type="submit" disabled={saving} className="bg-blue-600 hover:bg-blue-700">
                                {saving ? <Loader2 className="animate-spin mr-2 h-4 w-4" /> : <Save className="mr-2 h-4 w-4" />}
                                Save Changes
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}

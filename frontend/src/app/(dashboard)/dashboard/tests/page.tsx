'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Clock, HelpCircle, ArrowRight, Loader2, Brain } from "lucide-react";
import Link from 'next/link';
import api from '@/lib/api';

interface Test {
    id: string;
    name: string;
    category: 'verbal' | 'non-verbal' | 'wat';
    duration_minutes: number;
    total_questions: number;
    price: number;
    is_free: boolean;
    is_free_sample: boolean;
}

const CATEGORY_LABELS = {
    'verbal': 'Verbal IQ Tests',
    'non-verbal': 'Non-Verbal IQ Tests',
    'wat': 'Word Association Tests (WAT)'
};

export default function TestsPage() {
    const searchParams = useSearchParams();
    const categoryFilter = searchParams.get('category');

    const [tests, setTests] = useState<Test[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchTests = async () => {
            setLoading(true);
            try {
                const res = await api.get('/tests/tests/', {
                    params: categoryFilter ? { category: categoryFilter } : {}
                });
                const testsData = res.data.results || res.data;
                setTests(Array.isArray(testsData) ? testsData : []);
                setLoading(false);
            } catch {
                setError("Failed to load tests.");
                setLoading(false);
            }
        };
        fetchTests();
    }, [categoryFilter]);

    if (loading) return <div className="flex justify-center py-20"><Loader2 className="animate-spin w-8 h-8 text-blue-600" /></div>;
    if (error) return <div className="text-center py-20 text-red-600">{error}</div>;

    // Group tests by category if no filter is applied
    const categories = categoryFilter
        ? [categoryFilter as keyof typeof CATEGORY_LABELS]
        : ['verbal', 'non-verbal', 'wat'] as Array<keyof typeof CATEGORY_LABELS>;

    return (
        <div className="space-y-10">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">
                    {categoryFilter ? CATEGORY_LABELS[categoryFilter as keyof typeof CATEGORY_LABELS] : 'Available Tests'}
                </h1>
                <p className="text-gray-600 mt-2">
                    {categoryFilter
                        ? `Practice your skills in ${CATEGORY_LABELS[categoryFilter as keyof typeof CATEGORY_LABELS].toLowerCase()}.`
                        : 'Select a category to begin practicing. Remember, time management is key!'}
                </p>
            </div>

            {tests.length === 0 ? (
                <div className="text-center py-20 bg-gray-50 rounded-lg border-2 border-dashed">
                    <p className="text-gray-500">No tests available in this category at the moment.</p>
                </div>
            ) : (
                <div className="space-y-12">
                    {categories.map(cat => {
                        const catTests = tests.filter(t => t.category === cat);
                        if (catTests.length === 0) return null;

                        return (
                            <section key={cat} className="space-y-6">
                                {!categoryFilter && (
                                    <div className="flex items-center gap-2 pb-2 border-b">
                                        <Brain className="w-6 h-6 text-blue-600" />
                                        <h2 className="text-2xl font-bold text-gray-800">{CATEGORY_LABELS[cat]}</h2>
                                    </div>
                                )}
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    {catTests.map((test) => (
                                        <Card key={test.id} className="flex flex-col hover:shadow-lg transition-shadow border-slate-200">
                                            <CardHeader className="pb-4">
                                                <div className="flex justify-between items-start">
                                                    <span className={`px-2 py-1 rounded text-xs font-bold uppercase tracking-wide
                                                        ${test.is_free_sample ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}`}>
                                                        {test.is_free_sample ? 'Free' : 'Premium'}
                                                    </span>
                                                    {test.price > 0 && (
                                                        <span className="text-sm font-semibold text-gray-900">৳{test.price}</span>
                                                    )}
                                                </div>
                                                <CardTitle className="mt-2 text-xl">{test.name}</CardTitle>
                                            </CardHeader>
                                            <CardContent className="flex-grow space-y-4">
                                                <div className="flex items-center gap-2 text-sm text-gray-500">
                                                    <Clock className="w-4 h-4" />
                                                    {test.duration_minutes} Minutes
                                                </div>
                                                <div className="flex items-center gap-2 text-sm text-gray-500">
                                                    <HelpCircle className="w-4 h-4" />
                                                    {test.total_questions} Questions
                                                </div>
                                            </CardContent>
                                            <CardFooter className="pt-2">
                                                <Link
                                                    href={`/dashboard/tests/${test.id}`}
                                                    className="w-full"
                                                >
                                                    <Button className="w-full gap-2">
                                                        Start Test <ArrowRight className="w-4 h-4" />
                                                    </Button>
                                                </Link>
                                            </CardFooter>
                                        </Card>
                                    ))}
                                </div>
                            </section>
                        );
                    })}
                </div>
            )}
        </div>
    )
}

'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Clock, HelpCircle, AlertTriangle, Loader2 } from "lucide-react";
import Link from 'next/link';
import api from '@/lib/api';

interface Test {
    id: string;
    name: string;
    duration_minutes: number;
    total_questions: number;
    price: number;
    is_free: boolean;
    is_free_sample: boolean;
}

export default function TestsPage() {
    const [tests, setTests] = useState<Test[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchTests = async () => {
            try {
                const res = await api.get('/tests/tests/');
                const testsData = res.data.results || res.data;
                setTests(Array.isArray(testsData) ? testsData : []);
                setLoading(false);
            } catch {
                setError("Failed to load tests.");
                setLoading(false);
            }
        };
        fetchTests();
    }, []);

    if (loading) return <div className="flex justify-center py-20"><Loader2 className="animate-spin w-8 h-8 text-blue-600" /></div>;
    if (error) return <div className="text-center py-20 text-red-600">{error}</div>;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Available Tests</h1>
                <p className="text-gray-600 mt-2">Select a test to begin practicing. Remember, time management is key!</p>
            </div>

            {tests.length === 0 ? (
                <div className="text-center py-20 bg-gray-50 rounded-lg border-2 border-dashed">
                    <p className="text-gray-500">No tests available at the moment.</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {tests.map((test) => (
                        <Card key={test.id} className="flex flex-col">
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
                                        Start Test <AlertTriangle className="w-4 h-4" />
                                    </Button>
                                </Link>
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            )}
        </div>
    )
}

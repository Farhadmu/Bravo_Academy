'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle, XCircle, Clock, Calendar, Loader2 } from "lucide-react";
import Link from 'next/link';
import api from '@/lib/api';

interface Result {
    id: string;
    test_name: string;
    test_category?: string;
    created_at: string;
    score_percentage: string;
    passed: boolean;
    total_questions: number;
    time_taken_seconds: number;
}

export default function ResultsListPage() {
    const [results, setResults] = useState<Result[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchResults = async () => {
            try {
                const res = await api.get('/results/results/');
                const resultsData = res.data.results || res.data;
                setResults(Array.isArray(resultsData) ? resultsData : []);
                setLoading(false);
            } catch (err) {
                console.error("Failed to load results", err);
                setError("Failed to load results. Please try again.");
                setLoading(false);
            }
        };

        fetchResults();
    }, []);

    const formatTime = (seconds: number) => {
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    };

    if (loading) return <div className="flex justify-center py-20"><Loader2 className="animate-spin w-8 h-8 text-blue-600" /></div>;
    if (error) return <div className="text-center py-20 text-red-600">{error}</div>;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">My Results</h1>
                <p className="text-gray-600 mt-2">Track your performance and review your answers.</p>
            </div>

            <div className="space-y-4">
                {results.length === 0 ? (
                    <div className="text-center py-20 bg-gray-50 rounded-lg border-2 border-dashed">
                        <p className="text-gray-500">You haven't taken any tests yet.</p>
                    </div>
                ) : (
                    results.map((result) => (
                        <Card key={result.id} className="transition-shadow hover:shadow-md">
                            <CardContent className="p-6 flex flex-col md:flex-row items-center justify-between gap-4">
                                <div className="flex items-center gap-4">
                                    <div className={`p-3 rounded-full ${(result.test_category === 'wat' || result.test_category === 'verbal')
                                            ? 'bg-blue-100 text-blue-600'
                                            : result.passed
                                                ? 'bg-green-100 text-green-600'
                                                : 'bg-red-100 text-red-600'
                                        }`}>
                                        {(result.test_category === 'wat' || result.test_category === 'verbal') ? <CheckCircle className="w-6 h-6" /> : (result.passed ? <CheckCircle className="w-6 h-6" /> : <XCircle className="w-6 h-6" />)}
                                    </div>
                                    <div>
                                        <h3 className="font-bold text-lg text-gray-900">{result.test_name}</h3>
                                        <div className="flex flex-wrap gap-4 text-sm text-gray-500 mt-1">
                                            <span className="flex items-center gap-1"><Calendar className="w-3 h-3" /> {new Date(result.created_at).toLocaleDateString()}</span>
                                            <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {formatTime(result.time_taken_seconds)}</span>
                                        </div>
                                    </div>
                                </div>

                                <div className="flex items-center gap-6 w-full md:w-auto justify-between md:justify-end">
                                    <div className="text-center">
                                        <p className="text-xs text-gray-500 uppercase font-bold">{(result.test_category === 'wat' || result.test_category === 'verbal') ? 'Status' : 'Score'}</p>
                                        <p className={`text-xl font-bold ${(result.test_category === 'wat' || result.test_category === 'verbal')
                                                ? 'text-blue-600'
                                                : result.passed
                                                    ? 'text-green-600'
                                                    : 'text-red-600'
                                            }`}>
                                            {(result.test_category === 'wat' || result.test_category === 'verbal') ? 'Completed' : `${parseFloat(result.score_percentage)}%`}
                                        </p>
                                    </div>
                                    <Link href={`/dashboard/results/${result.id}`}>
                                        <Button variant="outline">View Detailed Analysis</Button>
                                    </Link>
                                </div>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
}

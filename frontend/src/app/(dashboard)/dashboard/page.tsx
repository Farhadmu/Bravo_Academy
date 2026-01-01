'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuthStore } from '@/store/auth';
import { Brain, Trophy, Clock, CheckCircle, ArrowRight, Loader2 } from "lucide-react";
import Link from 'next/link';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import api from '@/lib/api';

import { toast } from 'sonner';

interface Analytics {
    total_tests_taken: number;
    average_score: string;
    average_accuracy: string;
    highest_score: string;
    average_time_taken: number;
    total_time_spent: number;
    average_questions_answered: string;
}

interface Activity {
    id: string;
    test_name: string;
    score_percentage: string;
    accuracy: string;
    passed: boolean;
    created_at: string;
}

export default function DashboardPage() {
    const { user } = useAuthStore();
    const [analytics, setAnalytics] = useState<Analytics | null>(null);
    const [activities, setActivities] = useState<Activity[]>([]);
    const [loading, setLoading] = useState(true);
    const [slowLoadId, setSlowLoadId] = useState<string | number | null>(null);

    useEffect(() => {
        const fetchDashboardData = async () => {
            const timer = setTimeout(() => {
                const id = toast.info('Dashboard is loading...', {
                    description: 'Our backend might be waking up from sleep. This will only take a moment.',
                    duration: 10000,
                });
                setSlowLoadId(id);
            }, 5000);

            try {
                // Fetch analytics and recent results in parallel
                const [analyticsRes, activitiesRes] = await Promise.all([
                    api.get('/results/analytics/'),
                    api.get('/results/results/')
                ]);

                setAnalytics(analyticsRes.data);

                const activitiesData = activitiesRes.data.results || activitiesRes.data;
                setActivities(Array.isArray(activitiesData) ? activitiesData : []);

                clearTimeout(timer);
                if (slowLoadId) toast.dismiss(slowLoadId);
                setLoading(false);
            } catch (err) {
                clearTimeout(timer);
                if (slowLoadId) toast.dismiss(slowLoadId);
                console.error("Failed to load dashboard data", err);
                setLoading(false);
                toast.error("Failed to load dashboard data. Please refresh the page.", {
                    duration: 8000
                });
            }
        };

        fetchDashboardData();
    }, []);

    if (loading) return <div className="flex justify-center py-20"><Loader2 className="animate-spin w-8 h-8 text-blue-600" /></div>;

    const chartData = activities.slice().reverse().map((act, i) => ({
        name: `Test ${i + 1}`,
        score: parseFloat(act.score_percentage)
    }));

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.username || 'Candidate'}!</h1>
                <p className="text-gray-600 mt-2">Here's an overview of your progress and upcoming tests.</p>
            </div>

            {/* Stats Grid - Now 7 metrics in responsive layout */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-4 bg-blue-100 rounded-full">
                            <Brain className="h-6 w-6 text-blue-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Tests Taken</p>
                            <h3 className="text-2xl font-bold text-gray-900">{analytics?.total_tests_taken || 0}</h3>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-4 bg-green-100 rounded-full">
                            <Trophy className="h-6 w-6 text-green-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Average Score</p>
                            <h3 className="text-2xl font-bold text-gray-900">{analytics?.average_score || 0}%</h3>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-4 bg-indigo-100 rounded-full">
                            <CheckCircle className="h-6 w-6 text-indigo-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Avg Accuracy</p>
                            <h3 className="text-2xl font-bold text-gray-900">{Math.round(parseFloat(analytics?.average_accuracy || '0'))}%</h3>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-4 bg-purple-100 rounded-full">
                            <Trophy className="h-6 w-6 text-purple-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Highest Score</p>
                            <h3 className="text-2xl font-bold text-gray-900">{analytics?.highest_score || 0}%</h3>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-4 bg-orange-100 rounded-full">
                            <Clock className="h-6 w-6 text-orange-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Avg Time</p>
                            <h3 className="text-2xl font-bold text-gray-900">{Math.round((analytics?.average_time_taken || 0) / 60)}m</h3>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-4 bg-teal-100 rounded-full">
                            <Clock className="h-6 w-6 text-teal-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Total Time Spent</p>
                            <h3 className="text-2xl font-bold text-gray-900">{Math.round((analytics?.total_time_spent || 0) / 3600)}h</h3>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-4 bg-pink-100 rounded-full">
                            <CheckCircle className="h-6 w-6 text-pink-600" />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Avg Questions Answered</p>
                            <h3 className="text-2xl font-bold text-gray-900">{Math.round(parseFloat(analytics?.average_questions_answered || '0'))}</h3>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Chart */}
                <Card className="col-span-1 lg:col-span-2">
                    <CardHeader>
                        <CardTitle>Performance History</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[300px] w-full">
                            {chartData.length > 0 ? (
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={chartData}>
                                        <defs>
                                            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#2563eb" stopOpacity={0.8} />
                                                <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                        <XAxis dataKey="name" />
                                        <YAxis />
                                        <Tooltip />
                                        <Area type="monotone" dataKey="score" stroke="#2563eb" fillOpacity={1} fill="url(#colorScore)" />
                                    </AreaChart>
                                </ResponsiveContainer>
                            ) : (
                                <div className="h-full flex items-center justify-center text-gray-400">
                                    Take some tests to see your progress chart!
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>

                {/* Quick Actions / Recent */}
                <div className="space-y-6">
                    <Card className="bg-blue-600 text-white border-none">
                        <CardHeader>
                            <CardTitle className="text-white">Start New Practice</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-blue-100 mb-6">
                                Ready to challenge yourself? Take a new timed IQ test to improve your skills.
                            </p>
                            <Link href="/dashboard/tests">
                                <Button variant="secondary" className="w-full gap-2 font-bold text-blue-700">
                                    <Brain className="h-4 w-4" /> Start Now
                                </Button>
                            </Link>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader>
                            <CardTitle>Recent Activity</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {activities.length > 0 ? activities.slice(0, 5).map((act) => (
                                    <div key={act.id} className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0">
                                        <div className="flex items-center gap-3">
                                            <div className="h-10 w-10 rounded-lg bg-gray-100 flex items-center justify-center font-bold text-gray-500">
                                                iq
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900">{act.test_name}</p>
                                                <p className="text-xs text-gray-500">{new Date(act.created_at).toLocaleDateString()}</p>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <p className={`font-bold ${act.passed ? 'text-green-600' : 'text-red-600'}`}>
                                                {act.passed ? 'Passed' : 'Failed'}
                                            </p>
                                            <p className="text-xs text-gray-500">Score: {parseFloat(act.score_percentage)}%</p>
                                            <p className="text-xs text-gray-400">Acc: {Math.round(parseFloat(act.accuracy || '0'))}%</p>
                                        </div>
                                    </div>
                                )) : (
                                    <p className="text-center text-gray-400 py-4">No activity yet.</p>
                                )}
                            </div>
                            <Button variant="ghost" className="w-full mt-4 text-blue-600" asChild>
                                <Link href="/dashboard/results">View All History <ArrowRight className="ml-2 h-4 w-4" /></Link>
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div >
    );
}

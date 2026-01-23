'use client';
import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Clock, AlertCircle, Loader2, CheckCircle, XCircle, BarChart2 } from "lucide-react";
import Link from 'next/link';
import api from '@/lib/api';
import { toast } from 'sonner';

interface Question {
    id: string;
    question_text: string;
    options: { id: string; text: string }[];
    order: number;
}

interface ReviewItem {
    id: string;
    question_text: string;
    options: { id: string; text: string }[];
    correct_answer: string;
    user_answer: string | null;
    explanation: string;
    is_correct: boolean;
}

interface EvaluationResult {
    score: number;
    total: number;
    percentage: number;
    accuracy: number;
    review: ReviewItem[];
}

const LOCAL_STORAGE_KEY = 'defense_sample_test_state';

export default function SampleTestPage() {
    const [started, setStarted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [questions, setQuestions] = useState<Question[]>([]);
    const [currentQ, setCurrentQ] = useState(0);
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [result, setResult] = useState<EvaluationResult | null>(null);
    const [timeLeft, setTimeLeft] = useState(30 * 60);
    const [testId, setTestId] = useState<string | null>(null);
    const [slowLoadId, setSlowLoadId] = useState<string | number | null>(null);

    // 1. Fetch sample test ID on mount
    useEffect(() => {
        const fetchId = async () => {
            try {
                const res = await api.get('/tests/tests/get_sample_test/');
                setTestId(res.data.id);
            } catch (err) {
                console.error("Failed to fetch sample test ID", err);
            }
        };
        fetchId();
    }, []);

    // 2. Check for active session in localStorage once testId is available
    useEffect(() => {
        if (!testId || started || result) return;

        const savedState = localStorage.getItem(LOCAL_STORAGE_KEY);
        if (savedState) {
            try {
                const { startTime, savedAnswers, savedTestId } = JSON.parse(savedState);
                if (savedTestId === testId) {
                    const elapsed = Math.floor((Date.now() - startTime) / 1000);
                    const durationSeconds = 30 * 60;

                    if (elapsed < durationSeconds) {
                        const resumeTest = async () => {
                            setLoading(true);
                            try {
                                const res = await api.get(`/tests/tests/${testId}/public_questions/`);
                                setQuestions(res.data);
                                setAnswers(savedAnswers);
                                setTimeLeft(durationSeconds - elapsed);
                                setStarted(true);
                                setLoading(false);
                                toast.info("Welcome back!", {
                                    description: "Continuing your practice session.",
                                });
                            } catch (err) {
                                console.error("Failed to resume test questions", err);
                                setLoading(false);
                            }
                        };
                        resumeTest();
                    } else {
                        localStorage.removeItem(LOCAL_STORAGE_KEY);
                    }
                }
            } catch (e) {
                console.error("Failed to parse saved state", e);
            }
        }
    }, [testId, started, result]);

    const startTest = async () => {
        if (!navigator.onLine) {
            toast.error('No internet connection. Please check your network.');
            return;
        }

        if (!testId) {
            toast.error('Test ID is not ready. Please try again in 5 seconds.');
            return;
        }

        setLoading(true);
        // Global cold-boot detection now handled in api.ts

        try {
            const res = await api.get(`/tests/tests/${testId}/public_questions/`);

            if (slowLoadId) toast.dismiss(slowLoadId);

            setQuestions(res.data);
            setStarted(true);
            setLoading(false);
            setAnswers({});
            setResult(null);
            setCurrentQ(0);
            setTimeLeft(30 * 60);

            // Save initial state to localStorage
            localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify({
                startTime: Date.now(),
                savedAnswers: {},
                savedTestId: testId
            }));

            toast.success('Test started successfully!');
        } catch (err) {
            if (slowLoadId) toast.dismiss(slowLoadId);
            console.error("Failed to load sample test:", err);
            setLoading(false);
            toast.error("Failed to load test. Please try again.");
        }
    };

    const handleAnswer = (optionId: string) => {
        setAnswers(prev => {
            const newAnswers = { ...prev, [questions[currentQ].id]: optionId };
            const savedState = localStorage.getItem(LOCAL_STORAGE_KEY);
            if (savedState) {
                const parsed = JSON.parse(savedState);
                localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify({
                    ...parsed,
                    savedAnswers: newAnswers
                }));
            }
            return newAnswers;
        });
    };

    // Use a ref to prevent double submission
    const submissionInProgress = useRef(false);

    useEffect(() => {
        if (!started || !questions.length || result || timeLeft <= 0 || loading) return;

        const timer = setInterval(() => {
            setTimeLeft((prev) => Math.max(0, prev - 1));
        }, 1000);

        return () => clearInterval(timer);
    }, [started, questions.length, result, timeLeft, loading]);

    useEffect(() => {
        if (started && timeLeft === 0 && !result && !loading && !submissionInProgress.current) {
            handleSubmit(answers);
        }
    }, [timeLeft, started, result, loading, answers]);

    const handleNext = () => {
        if (currentQ < questions.length - 1) {
            setCurrentQ(currentQ + 1);
        } else {
            handleSubmit(answers);
        }
    };

    const handleSubmit = async (currentAnswers: Record<string, string> = answers) => {
        if (!testId || submissionInProgress.current) return;

        submissionInProgress.current = true;
        setLoading(true);

        try {
            const res = await api.post(`/tests/tests/${testId}/public_evaluate/`, { answers: currentAnswers });
            setResult(res.data);
            setLoading(false);
            localStorage.removeItem(LOCAL_STORAGE_KEY);
        } catch (err) {
            console.error("Failed to submit test:", err);
            setLoading(false);
            submissionInProgress.current = false;
            alert("Failed to submit test. Please try again.");
        }
    };

    const formatTime = (seconds: number) => {
        if (seconds <= 0) return "00:00";
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <Loader2 className="w-12 h-12 text-blue-600 animate-spin mb-4" />
                <p className="text-gray-600">Loading...</p>
            </div>
        );
    }

    if (!started && !result) {
        return (
            <div className="max-w-4xl mx-auto py-20 px-4 text-center">
                <div className="bg-white p-12 rounded-2xl shadow-lg border">
                    <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                        <Clock className="w-10 h-10 text-blue-600" />
                    </div>
                    <h1 className="text-4xl font-bold text-gray-900 mb-6">Free IQ Practice Test (Set 1)</h1>
                    <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
                        Take a full-length sample test from our premium collection.
                        <br /><br />
                        <strong>Details:</strong> 30 Minutes • Real Questions • Instant Results & Explanations.
                    </p>
                    <Button size="lg" className="text-lg px-12 py-6" onClick={startTest}>
                        Start Free Test
                    </Button>
                </div>
            </div>
        );
    }

    if (result) {
        return (
            <div className="max-w-4xl mx-auto py-12 px-4">
                <div className="text-center mb-12">
                    <Card className="shadow-lg mb-8">
                        <CardHeader>
                            <CardTitle className="text-3xl">Test Complete!</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="py-8">
                                <p className="text-gray-600 mb-2">You scored:</p>
                                <h2 className="text-6xl font-bold text-blue-600 mb-6">{result.score} / {result.total}</h2>
                                <p className="text-gray-500">
                                    That&apos;s {Math.round(result.accuracy)}% accuracy.
                                </p>
                            </div>

                            <div className="bg-blue-50 p-6 rounded-lg text-left max-w-2xl mx-auto">
                                <h3 className="font-bold text-blue-900 mb-2 flex items-center gap-2">
                                    <AlertCircle className="w-5 h-5" /> Want to track your progress?
                                </h3>
                                <p className="text-blue-800 text-sm mb-4">
                                    Create a free account to save your results, track improvement over time, and access more tests.
                                </p>
                                <div className="flex gap-4">
                                    <Link href="/register" className="flex-1">
                                        <Button className="w-full">Sign Up Free</Button>
                                    </Link>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    <h2 className="text-2xl font-bold text-gray-900 mb-6 text-left">Answers & Explanations</h2>

                    <div className="space-y-6 text-left">
                        {result.review.map((item, index) => (
                            <div key={item.id} className={`p-6 rounded-lg border ${item.is_correct ? 'bg-green-50/30 border-green-100' : 'bg-red-50/30 border-red-100'}`}>
                                <div className="flex justify-between items-start gap-4 mb-4">
                                    <h4 className="font-medium text-gray-900 leading-relaxed">
                                        {index + 1}. {item.question_text}
                                    </h4>
                                    {item.is_correct ? (
                                        <span className="flex items-center gap-1 text-xs font-bold text-green-600 whitespace-nowrap bg-green-100 px-2 py-1 rounded">
                                            <CheckCircle className="w-3 h-3" /> CORRECT
                                        </span>
                                    ) : (
                                        <span className="flex items-center gap-1 text-xs font-bold text-red-600 whitespace-nowrap bg-red-100 px-2 py-1 rounded">
                                            <XCircle className="w-3 h-3" /> {item.user_answer ? 'WRONG' : 'SKIPPED'}
                                        </span>
                                    )}
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                                    <div className="text-sm">
                                        <span className="text-gray-500 block mb-1">Your Answer:</span>
                                        <span className={`font-medium ${item.is_correct ? 'text-green-700' : 'text-red-700'}`}>
                                            {item.user_answer !== null
                                                ? item.options.find(o => o.id === item.user_answer)?.text || 'Unknown'
                                                : <span className="text-gray-400 italic">No answer provided</span>
                                            }
                                        </span>
                                    </div>
                                    <div className="text-sm">
                                        <span className="text-gray-500 block mb-1">Correct Answer:</span>
                                        <span className="font-medium text-green-700">
                                            {item.options.find(o => o.id === item.correct_answer)?.text}
                                        </span>
                                    </div>
                                </div>

                                {item.explanation && (
                                    <div className="bg-white/60 p-4 rounded border border-dashed border-gray-200 text-sm">
                                        <span className="font-bold text-gray-700 block mb-1 flex items-center gap-2">
                                            <BarChart2 className="w-4 h-4" /> Explanation:
                                        </span>
                                        <p className="text-gray-600 leading-relaxed">
                                            {item.explanation}
                                        </p>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    if (questions.length > 0) {
        return (
            <div className="max-w-3xl mx-auto py-8 md:py-12 px-4">
                <div className="flex flex-col sm:flex-row justify-between items-center mb-6 sticky top-[64px] md:top-0 bg-gray-50/95 backdrop-blur-sm py-4 z-10 gap-4">
                    <div className="flex flex-col">
                        <span className="text-sm font-bold text-gray-500 uppercase tracking-wide">Question {currentQ + 1} of {questions.length}</span>
                        <div className="w-full bg-gray-200 h-1.5 rounded-full mt-2 w-32">
                            <div className="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style={{ width: `${((currentQ + 1) / questions.length) * 100}%` }}></div>
                        </div>
                    </div>
                    <div className={`text-xl font-mono font-bold px-4 py-2 rounded-lg ${timeLeft < 300 ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-white text-gray-900 shadow-sm border'}`}>
                        {formatTime(timeLeft)}
                    </div>
                </div>

                <Card className="shadow-md min-h-[400px] flex flex-col">
                    <CardContent className="pt-8 flex-grow">
                        <h2 className="text-2xl font-bold text-gray-900 mb-8 leading-relaxed">{questions[currentQ].question_text}</h2>
                        <div className="space-y-3">
                            {questions[currentQ].options.map((opt, idx) => (
                                <Button
                                    key={opt.id}
                                    variant={answers[questions[currentQ].id] === opt.id ? "default" : "outline"}
                                    className={`w-full justify-start text-left h-auto py-4 text-lg border-2 hover:border-blue-500 hover:bg-blue-50 ${answers[questions[currentQ].id] === opt.id ? 'border-blue-600 bg-blue-50 text-blue-900 ring-2 ring-blue-200' : ''
                                        }`}
                                    onClick={() => handleAnswer(opt.id)}
                                >
                                    <span className={`w-8 h-8 rounded-full mr-4 flex items-center justify-center text-sm font-bold flex-shrink-0 ${answers[questions[currentQ].id] === opt.id ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-500'
                                        }`}>
                                        {String.fromCharCode(65 + idx)}
                                    </span>
                                    <span>{opt.text}</span>
                                </Button>
                            ))}
                        </div>
                    </CardContent>
                    <CardFooter className="border-t p-6 bg-gray-50 flex justify-between items-center rounded-b-xl">
                        <Button
                            variant="ghost"
                            disabled={currentQ === 0}
                            onClick={() => setCurrentQ(prev => prev - 1)}
                        >
                            Previous
                        </Button>
                        <Button
                            onClick={handleNext}
                            size="lg"
                            className="px-8"
                        >
                            {currentQ === questions.length - 1 ? 'Submit Test' : 'Next Question'}
                        </Button>
                    </CardFooter>
                </Card>

                <div className="mt-8">
                    <p className="text-sm font-medium text-gray-500 mb-4">Question Navigator</p>
                    <div className="flex flex-wrap gap-2">
                        {questions.map((q, idx) => (
                            <button
                                key={q.id}
                                onClick={() => setCurrentQ(idx)}
                                className={`w-10 h-10 rounded-lg text-sm font-bold flex items-center justify-center transition-all border-2
                                    ${idx === currentQ
                                        ? 'bg-blue-600 text-white border-blue-600 shadow-md transform scale-105'
                                        : answers[q.id]
                                            ? 'bg-blue-50 text-blue-700 border-blue-200 hover:border-blue-300'
                                            : 'bg-white text-gray-500 border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                                    }`}
                            >
                                {idx + 1}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        );
    }

    return null;
}

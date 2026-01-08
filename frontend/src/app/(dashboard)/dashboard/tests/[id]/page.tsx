'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Clock, Loader2 } from "lucide-react";
import api from '@/lib/api';

interface Question {
    id: string;
    question_text: string;
    options: { id: string; text: string }[];
    question_type: 'mcq' | 'true_false' | 'wat';
    images?: { id: string; image: string; caption: string }[];
}

interface TestDetail {
    id: string;
    name: string;
    description: string;
    duration_minutes: number;
    total_questions: number;
    is_bank?: boolean;
}

export default function TestRunnerPage({ params }: { params: Promise<{ id: string }> }) {
    const unwrappedParams = React.use(params);
    const id = unwrappedParams.id;
    const router = useRouter();

    const [test, setTest] = useState<TestDetail | null>(null);
    const [questions, setQuestions] = useState<Question[]>([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState<Record<string, string>>({}); // valid option id
    const [timeLeft, setTimeLeft] = useState(0);
    const [watTimeLeft, setWatTimeLeft] = useState(10); // 10 seconds for WAT
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [sessionId, setSessionId] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Use a ref to always have access to the latest answers in the timer closure
    const answersRef = useRef(answers);
    useEffect(() => {
        answersRef.current = answers;
    }, [answers]);

    // Fetch Test Data - OPTIMIZED: Single API call instead of 3
    useEffect(() => {
        const fetchTestData = async () => {
            try {
                // Single optimized API call that returns test, session, and questions together
                const response = await api.post(`/tests/tests/${id}/start_test/`);
                const { test: testData, session, questions: questionsData } = response.data;

                setTest(testData);
                setQuestions(Array.isArray(questionsData) ? questionsData : []);
                setSessionId(session.id);

                if (session.answers) {
                    setAnswers(session.answers);
                }


                // Use robust server-side calculation if available to avoid timezone issues
                if (typeof session.remaining_seconds === 'number') {
                    setTimeLeft(session.remaining_seconds);
                } else {
                    // Fallback to client-side calculation
                    const sessionStartTime = session.started_at || session.created_at;
                    const sessionLimit = session.time_limit_seconds || (testData.duration_minutes * 60) || 1800;
                    const startTime = new Date(sessionStartTime).getTime();
                    const elapsed = isNaN(startTime) ? 0 : Math.max(0, Math.floor((Date.now() - startTime) / 1000));
                    const remaining = sessionLimit - elapsed;
                    setTimeLeft(Math.max(0, remaining));
                }

                setLoading(false);
            } catch (err: any) {
                console.error("Failed to load test:", err);
                setError(err.response?.data?.detail || "Failed to load test. Please try again.");
                setLoading(false);
            }
        };

        if (id) {
            fetchTestData();
        }
    }, [id]);

    const handleSubmit = async (auto = false, currentAnswers: Record<string, string> = answers) => {
        if (submitting || isSubmitted || submissionInProgress.current) return;

        if (!auto && !confirm("Are you sure you want to submit?")) return;

        submissionInProgress.current = true;
        setSubmitting(true);
        try {
            await api.post(`/tests/test-sessions/${sessionId}/submit/`, { answers: currentAnswers });

            setIsSubmitted(true);
            router.push(`/dashboard/results/${sessionId}`);
        } catch (err) {
            console.error("Submit failed", err);
            alert("Failed to submit test. Please try again.");
            setSubmitting(false);
            submissionInProgress.current = false;
        }
    };

    // Use a ref to prevent double submission
    const submissionInProgress = useRef(false);

    useEffect(() => {
        if (!loading && timeLeft > 0 && !isSubmitted && questions.length > 0) {
            // Global timer
            const timer = setInterval(() => {
                setTimeLeft((prev) => Math.max(0, prev - 1));
            }, 1000);

            // WAT specific timer
            let watTimer: NodeJS.Timeout | null = null;
            if (questions[currentQuestionIndex]?.question_type === 'wat') {
                // Reset WAT timer when question changes
                // This is handled by a separate effect watching currentQuestionIndex
            }

            return () => clearInterval(timer);
        }
    }, [timeLeft, loading, isSubmitted, currentQuestionIndex, questions]);

    // Sound Logic for WAT - High Impact "Bip Bang"
    const playBeep = () => {
        try {
            const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
            const masterGain = audioCtx.createGain();
            masterGain.connect(audioCtx.destination);
            masterGain.gain.setValueAtTime(0, audioCtx.currentTime);
            masterGain.gain.linearRampToValueAtTime(0.8, audioCtx.currentTime + 0.01); // Loud start
            masterGain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.4);

            // "Bip" - High frequency bite (Square wave)
            const bip = audioCtx.createOscillator();
            bip.type = 'square';
            bip.frequency.setValueAtTime(880, audioCtx.currentTime); // A5
            bip.connect(masterGain);

            // "Bang" - Low frequency body (Sine wave)
            const bang = audioCtx.createOscillator();
            bang.type = 'sine';
            bang.frequency.setValueAtTime(110, audioCtx.currentTime); // A2
            bang.connect(masterGain);

            bip.start();
            bang.start();
            bip.stop(audioCtx.currentTime + 0.1);
            bang.stop(audioCtx.currentTime + 0.4);

            // Auto-close context to save resources
            setTimeout(() => audioCtx.close(), 1000);
        } catch (err) {
            console.error("Audio play failed:", err);
        }
    };

    // Separate effect for WAT timer and auto-advance
    useEffect(() => {
        if (!loading && !isSubmitted && questions[currentQuestionIndex]?.question_type === 'wat') {
            setWatTimeLeft(10); // Reset to 10s on question change
            playBeep(); // Play sound immediately on change

            const timer = setInterval(() => {
                setWatTimeLeft((prev) => {
                    if (prev <= 1) {
                        // Auto advance
                        if (currentQuestionIndex < questions.length - 1) {
                            setCurrentQuestionIndex((curr) => curr + 1);
                            return 10;
                        } else {
                            // Last question, submit
                            clearInterval(timer);
                            if (!submissionInProgress.current) {
                                handleSubmit(true);
                            }
                            return 0;
                        }
                    }
                    return prev - 1;
                });
            }, 1000);

            return () => clearInterval(timer);
        }
    }, [currentQuestionIndex, loading, isSubmitted, questions.length]);

    useEffect(() => {
        if (!loading && timeLeft === 0 && !isSubmitted && !submissionInProgress.current) {
            handleSubmit(true, answersRef.current);
        }
    }, [timeLeft, loading, isSubmitted]);


    const handleOptionSelect = async (optionId: string) => {
        if (!questions[currentQuestionIndex]) return;
        const newAnswers = {
            ...answers,
            [questions[currentQuestionIndex].id]: optionId
        };
        setAnswers(newAnswers);

        // Sync to backend (Fire and forget, but log errors)
        try {
            await api.patch(`/tests/test-sessions/${sessionId}/`, { answers: newAnswers });
        } catch (err) {
            console.error("Failed to sync answers to server", err);
        }
    };

    const handleNext = () => {
        if (currentQuestionIndex < questions.length - 1) {
            setCurrentQuestionIndex(currentQuestionIndex + 1);
        }
    };

    const handlePrev = () => {
        if (currentQuestionIndex > 0) {
            setCurrentQuestionIndex(currentQuestionIndex - 1);
        }
    };


    const formatTime = (seconds: number) => {
        if (isNaN(seconds) || seconds <= 0) return "00:00";
        const m = Math.floor(seconds / 60);
        const s = seconds % 60;
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    };

    if (loading) return <div className="flex justify-center py-20"><Loader2 className="animate-spin w-8 h-8 text-blue-600" /></div>;
    if (error) return <div className="text-center py-20 text-red-600">{error}</div>;
    if (!test || questions.length === 0) return <div className="text-center py-20">Test not found or has no questions.</div>;

    const currentQuestion = questions[currentQuestionIndex];
    const progressPercentage = ((currentQuestionIndex + 1) / questions.length) * 100;

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Header with Timer */}
            <div className="flex flex-col sm:flex-row items-center justify-between bg-white p-4 rounded-lg shadow-sm sticky top-[64px] md:top-0 z-10 border-b gap-4">
                <div className="text-center sm:text-left">
                    <h2 className="font-bold text-gray-800">{test.name}</h2>
                    <div className="text-xs text-gray-500">Question {currentQuestionIndex + 1} of {questions.length}</div>
                </div>
                <div className={`flex items-center gap-2 font-mono text-xl font-bold px-4 py-2 rounded-md ${timeLeft < 300 ? 'bg-red-100 text-red-600 animate-pulse' : 'bg-blue-50 text-blue-600'}`}>
                    <Clock className="w-5 h-5" />
                    {formatTime(timeLeft)}
                </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 h-2 rounded-full overflow-hidden">
                <div className="bg-blue-600 h-full transition-all duration-300" style={{ width: `${progressPercentage}%` }}></div>
            </div>

            {/* Question Card */}
            <Card className="min-h-[400px] flex flex-col justify-between">
                <CardContent className="pt-6">
                    {currentQuestion.images && currentQuestion.images.length > 0 && (
                        <div className="mb-6 flex justify-center">
                            {/* eslint-disable-next-line @next/next/no-img-element */}
                            <img
                                src={currentQuestion.images[0].image}
                                alt={currentQuestion.images[0].caption || "Question Image"}
                                className="max-w-full max-h-[400px] object-contain rounded-lg border"
                            />
                        </div>
                    )}
                    <h3 className="text-xl font-medium text-gray-900 mb-8 leading-relaxed">
                        {currentQuestionIndex + 1}. {currentQuestion.question_text}
                    </h3>

                    <div className="space-y-4">
                        {currentQuestion.question_type === 'wat' ? (
                            <div className="flex flex-col items-center justify-center py-20">
                                <h1 className="text-6xl font-black text-gray-900 mb-8 tracking-wider">{currentQuestion.question_text}</h1>
                                <p className="mt-8 text-gray-500 italic">Write a sentence with this word on your paper.</p>
                            </div>
                        ) : (
                            currentQuestion.options.map((option, idx) => (
                                <label
                                    key={idx}
                                    className={`flex items-center p-4 border rounded-lg cursor-pointer transition-colors hover:bg-gray-50 
                    ${answers[currentQuestion.id] === option.id ? 'border-blue-500 bg-blue-50 ring-1 ring-blue-500' : 'border-gray-200'}`}
                                >
                                    <input
                                        type="radio"
                                        name={`question-${currentQuestion.id}`}
                                        value={option.id}
                                        checked={answers[currentQuestion.id] === option.id}
                                        onChange={() => handleOptionSelect(option.id)}
                                        className="w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500 mr-3"
                                    />
                                    <span className="text-gray-700">{option.text}</span>
                                </label>
                            ))
                        )}
                    </div>
                </CardContent>

                <CardFooter className="border-t bg-gray-50 p-6 flex justify-between gap-4">
                    <Button
                        variant="outline"
                        onClick={handlePrev}
                        disabled={currentQuestionIndex === 0}
                    >
                        Previous
                    </Button>

                    {currentQuestionIndex === questions.length - 1 ? (
                        <Button
                            className="bg-green-600 hover:bg-green-700"
                            onClick={() => handleSubmit(false)}
                            disabled={submitting}
                        >
                            {submitting ? <Loader2 className="animate-spin w-4 h-4 mr-2" /> : null}
                            Submit Test
                        </Button>
                    ) : (
                        <Button onClick={handleNext} disabled={currentQuestion.question_type === 'wat'}>
                            {currentQuestion.question_type === 'wat' ? 'Auto-advancing...' : 'Next Question'}
                        </Button>
                    )}
                </CardFooter>
            </Card>

            <div className="bg-white p-4 rounded-lg shadow-sm border">
                <p className="text-xs font-bold text-gray-500 uppercase mb-3 text-center sm:text-left">Question Navigator</p>
                <div className="flex justify-center sm:justify-start flex-wrap gap-2 max-h-40 overflow-y-auto p-1">
                    {questions.map((q, idx) => (
                        <button
                            key={q.id}
                            onClick={() => setCurrentQuestionIndex(idx)}
                            className={`w-10 h-10 rounded-lg text-xs font-bold flex items-center justify-center transition-all border
                ${idx === currentQuestionIndex ? 'bg-blue-600 text-white border-blue-600 shadow-md transform scale-105' :
                                    answers[q.id] ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-white text-gray-500 border-gray-200 hover:border-gray-300'}`}
                        >
                            {idx + 1}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

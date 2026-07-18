'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { CheckCircle, Loader2, ArrowLeft, Save, Copy, X } from "lucide-react";
import api from '@/lib/api';

function generatePassword(): string {
    const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
    let pwd = '';
    for (let i = 0; i < 8; i++) {
        pwd += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return pwd;
}

export default function NewUserPage() {
    const router = useRouter();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        full_name: '',
        role: 'student',
        is_active: true
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [successResult, setSuccessResult] = useState<{ username: string; password: string } | null>(null);
    const [copied, setCopied] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const payload: any = { ...formData };
            if (!payload.username) delete payload.username;
            const passwordIsSet = !!payload.password;
            if (!payload.password) delete payload.password;

            const response = await api.post('/auth/users/', payload);
            const createdUser = response.data;

            setSuccessResult({
                username: createdUser.username || payload.full_name?.toLowerCase().replace(/[^a-z0-9]/g, '') || 'user',
                password: passwordIsSet ? payload.password : (createdUser.username || payload.full_name?.toLowerCase().replace(/[^a-z0-9]/g, '') || 'user')
            });
        } catch (err: any) {
            console.error("Create failed", err);
            setError(err.response?.data ? JSON.stringify(err.response.data) : "Failed to create user");
        } finally {
            setLoading(false);
        }
    };

    const copyCredentials = () => {
        if (!successResult) return;
        const text = `Username: ${successResult.username}\nPassword: ${successResult.password}`;
        navigator.clipboard.writeText(text).then(() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        });
    };

    if (successResult) {
        return (
            <div className="max-w-lg mx-auto space-y-6">
                <Card className="border-green-200">
                    <CardHeader className="text-center">
                        <div className="mx-auto bg-green-100 p-3 rounded-full w-fit mb-4">
                            <CheckCircle className="w-8 h-8 text-green-600" />
                        </div>
                        <CardTitle className="text-2xl font-bold text-green-700">User Created!</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="bg-green-50 border border-green-200 rounded-lg p-4 space-y-3">
                            <div>
                                <span className="text-sm font-medium text-green-800">Username</span>
                                <div className="text-xl font-mono font-bold text-green-900 bg-white border border-green-300 rounded px-3 py-2 mt-1">{successResult.username}</div>
                            </div>
                            <div>
                                <span className="text-sm font-medium text-green-800">Password</span>
                                <div className="text-xl font-mono font-bold text-green-900 bg-white border border-green-300 rounded px-3 py-2 mt-1">{successResult.password}</div>
                            </div>
                        </div>
                        <p className="text-sm text-green-700 text-center">
                            Share these credentials with the student.
                        </p>
                        <div className="flex gap-2">
                            <Button onClick={copyCredentials} variant="outline" className="flex-1">
                                {copied ? <><CheckCircle className="mr-2 h-4 w-4" /> Copied</> : <><Copy className="mr-2 h-4 w-4" /> Copy Credentials</>}
                            </Button>
                            <Button onClick={() => router.push('/admin/users')} className="flex-1">
                                Go to User List
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        );
    }

    const suggestedPassword = formData.password || generatePassword();

    return (
        <div className="max-w-2xl mx-auto space-y-6">
            <div className="flex items-center gap-4">
                <Button variant="ghost" size="icon" onClick={() => router.back()}>
                    <ArrowLeft className="h-4 w-4" />
                </Button>
                <h1 className="text-3xl font-bold tracking-tight">Create New User</h1>
            </div>

            <Card>
                <form onSubmit={handleSubmit}>
                    <CardHeader>
                        <CardTitle>User Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {error && (
                            <div className="bg-red-50 border border-red-200 text-red-700 p-3 rounded-md text-sm break-words">
                                {error}
                            </div>
                        )}

                        <div className="space-y-2">
                            <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70" htmlFor="full_name">Full Name *</label>
                            <Input
                                id="full_name"
                                name="full_name"
                                value={formData.full_name}
                                onChange={handleChange}
                                required
                                placeholder="John Doe"
                            />
                            <p className="text-xs text-muted-foreground text-gray-500">Username will be auto-generated from name.</p>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70" htmlFor="email">Email</label>
                            <Input
                                id="email"
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="john@example.com"
                            />
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70" htmlFor="role">Role *</label>
                            <select
                                id="role"
                                name="role"
                                value={formData.role}
                                onChange={handleChange}
                                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                            >
                                <option value="student">Student</option>
                                <option value="admin">Admin</option>
                                <option value="staff">Staff</option>
                            </select>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70" htmlFor="password">
                                Password <span className="text-gray-400 font-normal">(optional)</span>
                            </label>
                            <div className="flex gap-2">
                                <Input
                                    id="password"
                                    name="password"
                                    type="text"
                                    value={formData.password}
                                    onChange={handleChange}
                                    placeholder={suggestedPassword}
                                    className="font-mono"
                                />
                                <Button
                                    type="button"
                                    variant="outline"
                                    size="icon"
                                    onClick={() => setFormData(prev => ({ ...prev, password: generatePassword() }))}
                                    title="Generate random password"
                                >
                                    <Loader2 className="h-4 w-4 rotate-45" />
                                </Button>
                                {formData.password && (
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        size="icon"
                                        onClick={() => setFormData(prev => ({ ...prev, password: '' }))}
                                        title="Auto-generate from username"
                                    >
                                        <X className="h-4 w-4" />
                                    </Button>
                                )}
                            </div>
                            <p className="text-xs text-muted-foreground text-gray-500">
                                {formData.password
                                    ? 'Custom password will be used.'
                                    : 'Leave empty to auto-generate from username (password = username).'}
                            </p>
                        </div>

                    </CardContent>
                    <CardFooter className="flex justify-between">
                        <Button type="button" variant="ghost" onClick={() => router.back()}>Cancel</Button>
                        <Button type="submit" disabled={loading}>
                            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
                            Create User
                        </Button>
                    </CardFooter>
                </form>
            </Card>
        </div>
    );
}

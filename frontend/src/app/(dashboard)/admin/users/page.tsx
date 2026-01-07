'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Loader2, Plus, Trash2, KeyRound, Smartphone, X, Save, AlertTriangle } from "lucide-react";
import api from '@/lib/api';
import { toast } from 'sonner';

interface User {
    id: string;
    username: string;
    email: string;
    role: string;
    is_active: boolean;
    date_joined: string;
}

interface ConfirmDialog {
    open: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
    loading?: boolean;
}

export default function AdminUsersPage() {
    const router = useRouter();
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [page, setPage] = useState(1);
    const [totalCount, setTotalCount] = useState(0);
    const [nextPage, setNextPage] = useState<string | null>(null);
    const [prevPage, setPrevPage] = useState<string | null>(null);
    const [resetPasswordUser, setResetPasswordUser] = useState<User | null>(null);
    const [newPassword, setNewPassword] = useState('');
    const [actionLoading, setActionLoading] = useState(false);
    const [confirmDialog, setConfirmDialog] = useState<ConfirmDialog>({
        open: false,
        title: '',
        message: '',
        onConfirm: () => { }
    });

    useEffect(() => {
        fetchUsers(page);
    }, [page]);

    const fetchUsers = async (pageNumber: number) => {
        try {
            setLoading(true);
            const response = await api.get(`/auth/users/?page=${pageNumber}`);
            if (Array.isArray(response.data)) {
                setUsers(response.data);
                setTotalCount(response.data.length);
                setNextPage(null);
                setPrevPage(null);
            } else if (response.data.results) {
                setUsers(response.data.results);
                setTotalCount(response.data.count);
                setNextPage(response.data.next);
                setPrevPage(response.data.previous);
            }
            setLoading(false);
        } catch (err) {
            console.error("Failed to fetch users", err);
            setError("Failed to load users.");
            setLoading(false);
        }
    };

    const handleDelete = (id: string, username: string) => {
        setConfirmDialog({
            open: true,
            title: 'Delete User',
            message: `Are you sure you want to delete ${username}? This action cannot be undone.`,
            onConfirm: async () => {
                try {
                    setConfirmDialog(prev => ({ ...prev, loading: true }));
                    await api.delete(`/auth/users/${id}/`);
                    setUsers(prev => prev.filter(u => u.id !== id));
                    toast.success("User deleted successfully.", { duration: 8000 });
                } catch (err: any) {
                    const msg = err.response?.data?.detail || "Failed to delete user";
                    toast.error(msg, { duration: 8000 });
                } finally {
                    setConfirmDialog(prev => ({ ...prev, open: false, loading: false }));
                }
            }
        });
    };

    const handleResetPassword = async () => {
        if (!resetPasswordUser || !newPassword) return;
        try {
            setActionLoading(true);
            await api.post(`/auth/users/${resetPasswordUser.id}/reset_password/`, { password: newPassword });
            toast.success(`Password for ${resetPasswordUser.username} has been reset.`, { duration: 8000 });
            setResetPasswordUser(null);
            setNewPassword('');
        } catch (err: any) {
            console.error("Reset password failed", err);
            const msg = err.response?.data?.error || err.response?.data?.detail || "Failed to reset password";
            toast.error(msg, { duration: 8000 });
        } finally {
            setActionLoading(false);
        }
    };

    const handleResetDevice = (id: string, username: string) => {
        setConfirmDialog({
            open: true,
            title: 'Clear Device Lock',
            message: `Are you sure you want to clear the device lock for ${username}?`,
            onConfirm: async () => {
                try {
                    setConfirmDialog(prev => ({ ...prev, loading: true }));
                    await api.post(`/auth/users/${id}/reset_device/`);
                    toast.success(`Device lock for ${username} has been cleared.`, { duration: 8000 });
                } catch (err: any) {
                    const msg = err.response?.data?.error || err.response?.data?.detail || "Failed to clear device lock";
                    toast.error(msg, { duration: 8000 });
                } finally {
                    setConfirmDialog(prev => ({ ...prev, open: false, loading: false }));
                }
            }
        });
    };

    if (loading && users.length === 0) return <div className="flex justify-center p-8"><Loader2 className="animate-spin" /></div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold tracking-tight">User Management</h1>
                <Button onClick={() => router.push('/admin/users/new')}>
                    <Plus className="mr-2 h-4 w-4" /> Add User
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Users</CardTitle>
                </CardHeader>
                <CardContent>
                    {error && <div className="text-red-500 mb-4">{error}</div>}
                    <div className="rounded-md border overflow-x-auto">
                        <table className="w-full text-sm text-left min-w-[600px] md:min-w-full">
                            <thead className="bg-gray-50 border-b">
                                <tr>
                                    <th className="p-4 font-medium text-gray-500">Username</th>
                                    <th className="p-4 font-medium text-gray-500">Email</th>
                                    <th className="p-4 font-medium text-gray-500">Role</th>
                                    <th className="p-4 font-medium text-gray-500">Status</th>
                                    <th className="p-4 font-medium text-gray-500 text-right">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((user) => (
                                    <tr key={user.id} className="border-b last:border-0 hover:bg-gray-50 transition-colors">
                                        <td className="p-4 font-medium">{user.username}</td>
                                        <td className="p-4 text-gray-500">{user.email}</td>
                                        <td className="p-4">
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize
                                                ${user.role === 'admin' ? 'bg-purple-100 text-purple-800' :
                                                    user.role === 'staff' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                                                {user.role}
                                            </span>
                                        </td>
                                        <td className="p-4">
                                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                                                ${user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                                {user.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        <td className="p-4 text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button variant="ghost" size="sm" onClick={() => router.push(`/admin/users/${user.id}`)} className="text-blue-600 hover:text-blue-700 hover:bg-blue-50">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-eye"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0" /><circle cx="12" cy="12" r="3" /></svg>
                                                </Button>
                                                <Button variant="ghost" size="sm" onClick={() => router.push(`/admin/users/${user.id}/edit`)} className="text-amber-600 hover:text-amber-700 hover:bg-amber-50">
                                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-pencil"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z" /><path d="m15 5 4 4" /></svg>
                                                </Button>
                                                <Button variant="ghost" size="sm" onClick={() => setResetPasswordUser(user)} className="text-blue-600 hover:text-blue-700 hover:bg-blue-50" title="Reset Password">
                                                    <KeyRound className="h-4 w-4" />
                                                </Button>
                                                <Button variant="ghost" size="sm" onClick={() => handleResetDevice(user.id, user.username)} className="text-cyan-600 hover:text-cyan-700 hover:bg-cyan-50" title="Reset Device Lock">
                                                    <Smartphone className="h-4 w-4" />
                                                </Button>
                                                <Button variant="ghost" size="sm" onClick={() => handleDelete(user.id, user.username)} className="text-red-600 hover:text-red-700 hover:bg-red-50" title="Delete User">
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                                {users.length === 0 && (
                                    <tr>
                                        <td colSpan={5} className="p-8 text-center text-gray-500">No users found</td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>

                    {/* Pagination Controls */}
                    {totalCount > 0 && (
                        <div className="flex items-center justify-between mt-6 px-2">
                            <p className="text-sm text-gray-500">
                                Showing <span className="font-medium">{users.length}</span> of <span className="font-medium">{totalCount}</span> users
                            </p>
                            <div className="flex gap-2">
                                <Button
                                    variant="outline"
                                    size="sm"
                                    disabled={!prevPage || loading}
                                    onClick={() => setPage(p => p - 1)}
                                >
                                    Previous
                                </Button>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    disabled={!nextPage || loading}
                                    onClick={() => setPage(p => p + 1)}
                                >
                                    Next
                                </Button>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Reset Password Modal */}
            {resetPasswordUser && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in duration-300">
                    <Card className="w-full max-w-sm shadow-2xl border-none">
                        <CardHeader className="flex flex-row items-center justify-between border-b pb-4">
                            <CardTitle className="text-xl font-bold flex items-center gap-2">
                                <KeyRound className="w-5 h-5 text-blue-600" />
                                Reset Password
                            </CardTitle>
                            <Button variant="ghost" size="sm" onClick={() => setResetPasswordUser(null)} className="rounded-full">
                                <X className="h-4 w-4" />
                            </Button>
                        </CardHeader>
                        <CardContent className="space-y-4 pt-6">
                            <p className="text-sm text-gray-500">
                                Enter a new password for <span className="font-semibold text-gray-900">{resetPasswordUser.username}</span>.
                            </p>
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-gray-700">New Password</label>
                                <Input
                                    type="text"
                                    placeholder="Enter new password"
                                    value={newPassword}
                                    onChange={(e) => setNewPassword(e.target.value)}
                                    autoFocus
                                    className="focus-visible:ring-blue-600"
                                />
                            </div>
                        </CardContent>
                        <div className="p-4 bg-gray-50 flex justify-end gap-3 rounded-b-lg border-t">
                            <Button variant="outline" onClick={() => setResetPasswordUser(null)}>
                                Cancel
                            </Button>
                            <Button onClick={handleResetPassword} disabled={!newPassword || actionLoading} className="bg-blue-600 hover:bg-blue-700">
                                {actionLoading ? <Loader2 className="animate-spin mr-2 h-4 w-4" /> : <Save className="mr-2 h-4 w-4" />}
                                Update Password
                            </Button>
                        </div>
                    </Card>
                </div>
            )}

            {/* Confirmation Modal */}
            {confirmDialog.open && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 animate-in fade-in zoom-in-95 duration-200">
                    <Card className="w-full max-w-md shadow-2xl border-none">
                        <CardHeader className="flex flex-row items-center gap-3 border-b pb-4">
                            <div className={`p-2 rounded-full ${confirmDialog.title.includes('Delete') ? 'bg-red-100' : 'bg-blue-100'}`}>
                                {confirmDialog.title.includes('Delete') ?
                                    <Trash2 className="h-5 w-5 text-red-600" /> :
                                    <Smartphone className="h-5 w-5 text-blue-600" />
                                }
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
                                variant={confirmDialog.title.includes('Delete') ? "destructive" : "default"}
                                onClick={confirmDialog.onConfirm}
                                disabled={confirmDialog.loading}
                                className={confirmDialog.title.includes('Delete') ? "" : "bg-blue-600 hover:bg-blue-700"}
                            >
                                {confirmDialog.loading ? <Loader2 className="animate-spin mr-2 h-4 w-4" /> : null}
                                {confirmDialog.title.includes('Delete') ? 'Confirm Delete' : 'Confirm Action'}
                            </Button>
                        </div>
                    </Card>
                </div>
            )}
        </div>
    );
}



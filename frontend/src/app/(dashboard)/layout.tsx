'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth';
import {
    LayoutDashboard,
    Brain,
    History,
    User,
    LogOut,
    Shield,
    Menu,
    X
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const pathname = usePathname();
    const router = useRouter();
    const { user, isAuthenticated, logout } = useAuthStore();
    const [mounted, setMounted] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setMounted(true), 0);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        if (!isAuthenticated) {
            router.push('/login');
        }
    }, [isAuthenticated, router]);

    if (!mounted || !isAuthenticated) {
        return null; // Or a loading spinner
    }

    const sidebarLinks = [
        { href: '/dashboard', label: 'Overview', icon: LayoutDashboard },
        { href: '/dashboard/tests', label: 'Take IQ Test', icon: Brain },
        { href: '/dashboard/results', label: 'My Results', icon: History },
        { href: '/dashboard/profile', label: 'Profile', icon: User },
    ];

    const adminLinks = [
        { href: '/admin/dashboard', label: 'Overview', icon: LayoutDashboard },
        { href: '/admin/users', label: 'Users', icon: User },
        { href: '/admin/tests', label: 'Tests', icon: Brain },
        { href: '/admin/settings', label: 'Settings', icon: Shield },
    ];

    const links = user?.role === 'admin' ? adminLinks : sidebarLinks;

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col md:flex-row">
            {/* Mobile Header */}
            <div className="md:hidden fixed top-0 left-0 right-0 h-16 bg-white border-b z-30 flex items-center justify-between px-4">
                <Link href="/" className="flex items-center gap-2">
                    <Shield className="h-6 w-6 text-blue-600" />
                    <span className="font-bold text-lg text-gray-900">Bravo Academy</span>
                </Link>
                <Button variant="ghost" size="icon" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
                    {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                </Button>
            </div>

            {/* Mobile Sidebar Overlay */}
            {isMobileMenuOpen && (
                <div className="fixed inset-0 z-40 bg-black/50 md:hidden animate-in fade-in duration-200" onClick={() => setIsMobileMenuOpen(false)}>
                    <div
                        className="fixed inset-y-0 left-0 w-3/4 max-w-xs bg-white shadow-xl flex flex-col animate-in slide-in-from-left duration-200"
                        onClick={e => e.stopPropagation()}
                    >
                        <div className="h-16 flex items-center px-6 border-b">
                            <span className="font-bold text-lg text-gray-900">Menu</span>
                        </div>
                        <div className="p-4 flex-grow overflow-y-auto">
                            <div className="space-y-1">
                                {links.map((link) => (
                                    <Link key={link.href} href={link.href} onClick={() => setIsMobileMenuOpen(false)}>
                                        <Button
                                            variant={pathname === link.href ? 'secondary' : 'ghost'}
                                            className="w-full justify-start gap-3 mb-1"
                                        >
                                            <link.icon className="h-5 w-5" />
                                            {link.label}
                                        </Button>
                                    </Link>
                                ))}
                            </div>
                        </div>
                        <div className="p-4 border-t">
                            <div className="flex items-center gap-3 mb-4 px-2">
                                <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold">
                                    {user?.username?.charAt(0).toUpperCase()}
                                </div>
                                <div className="overflow-hidden">
                                    <p className="text-sm font-medium text-gray-900 truncate">{user?.username}</p>
                                    <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
                                </div>
                            </div>
                            <Button
                                variant="outline"
                                className="w-full justify-start gap-3"
                                onClick={() => {
                                    setIsMobileMenuOpen(false);
                                    logout();
                                    router.push('/login');
                                }}
                            >
                                <LogOut className="h-5 w-5" />
                                Logout
                            </Button>
                        </div>
                    </div>
                </div>
            )}

            {/* Desktop Sidebar */}
            <aside className="w-64 bg-white border-r hidden md:flex flex-col fixed h-full z-20">
                <div className="h-16 flex items-center px-6 border-b">
                    <Link href="/" className="flex items-center gap-2">
                        <Shield className="h-8 w-8 text-blue-600" />
                        <span className="font-bold text-lg text-gray-900">Bravo Academy</span>
                    </Link>
                </div>

                <div className="p-4 flex-grow">
                    <div className="space-y-1">
                        {links.map((link) => (
                            <Link key={link.href} href={link.href}>
                                <Button
                                    variant={pathname === link.href ? 'secondary' : 'ghost'}
                                    className="w-full justify-start gap-3 mb-1"
                                >
                                    <link.icon className="h-5 w-5" />
                                    {link.label}
                                </Button>
                            </Link>
                        ))}
                    </div>
                </div>

                <div className="p-4 border-t">
                    <div className="flex items-center gap-3 mb-4 px-2">
                        <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold">
                            {user?.username?.charAt(0).toUpperCase()}
                        </div>
                        <div className="overflow-hidden">
                            <p className="text-sm font-medium text-gray-900 truncate">{user?.username}</p>
                            <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
                        </div>
                    </div>
                    <Button
                        variant="outline"
                        className="w-full justify-start gap-3"
                        onClick={() => {
                            logout();
                            router.push('/login');
                        }}
                    >
                        <LogOut className="h-5 w-5" />
                        Logout
                    </Button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 md:ml-64 p-4 md:p-8 pt-20 md:pt-8">
                {children}
            </main>
        </div>
    );
}

'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/auth';
import {
    LayoutDashboard,
    Database,
    Settings,
    Shield,
    Terminal,
    LogOut,
    Menu,
    X,
    Users,
    Activity,
    Lock,
    Eye
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';

export default function DeveloperLayout({
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
        setMounted(true);
    }, []);

    useEffect(() => {
        if (mounted && (!isAuthenticated || user?.role !== 'developer')) {
            router.push('/login');
        }
    }, [mounted, isAuthenticated, user, router]);

    if (!mounted || !isAuthenticated || user?.role !== 'developer') {
        return null;
    }

    const devLinks = [
        { href: '/developer', label: 'Dev Dashboard', icon: Terminal },
        { href: '/developer/maintenance', label: 'Maintenance Control', icon: Lock },
        { href: '/developer/database', label: 'DB Inspector', icon: Database },
        { href: '/developer/feature-flags', label: 'Feature Flags', icon: Settings },
        { href: '/developer/stats', label: 'System Stats', icon: Activity },
    ];

    const portalLinks = [
        { href: '/admin/dashboard', label: 'Admin Portal', icon: Shield },
        { href: '/dashboard', label: 'Student Portal', icon: Eye },
    ];

    return (
        <div className="min-h-screen bg-slate-900 text-white flex flex-col md:flex-row">
            {/* Mobile Header */}
            <div className="md:hidden fixed top-0 left-0 right-0 h-16 bg-slate-800 border-b border-slate-700 z-30 flex items-center justify-between px-4">
                <Link href="/developer" className="flex items-center gap-2">
                    <Terminal className="h-6 w-6 text-purple-400" />
                    <span className="font-bold text-lg">Dev Portal</span>
                </Link>
                <Button variant="ghost" size="icon" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
                    {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                </Button>
            </div>

            {/* Sidebar */}
            <aside className={`
                fixed inset-y-0 left-0 z-40 w-64 bg-slate-800 border-r border-slate-700 flex flex-col transition-transform duration-200 ease-in-out
                ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
            `}>
                <div className="h-16 flex items-center px-6 border-b border-slate-700">
                    <Link href="/developer" className="flex items-center gap-2">
                        <Terminal className="h-8 w-8 text-purple-400" />
                        <div className="flex flex-col">
                            <span className="font-bold text-lg leading-tight uppercase tracking-wider">Dev Portal</span>
                            <span className="text-[10px] text-purple-400 font-mono tracking-tighter">GOD MODE ACTIVE</span>
                        </div>
                    </Link>
                </div>

                <div className="p-4 flex-grow overflow-y-auto">
                    <div className="mb-6">
                        <p className="px-2 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-widest">Core Tools</p>
                        <div className="space-y-1">
                            {devLinks.map((link) => (
                                <Link key={link.href} href={link.href} onClick={() => setIsMobileMenuOpen(false)}>
                                    <Button
                                        variant={pathname === link.href ? 'secondary' : 'ghost'}
                                        className={`w-full justify-start gap-3 mb-1 ${pathname === link.href ? 'bg-purple-600/20 text-purple-400 hover:bg-purple-600/30' : 'text-slate-300 hover:bg-slate-700'}`}
                                    >
                                        <link.icon className="h-5 w-5" />
                                        {link.label}
                                    </Button>
                                </Link>
                            ))}
                        </div>
                    </div>

                    <div>
                        <p className="px-2 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-widest">Portal Access</p>
                        <div className="space-y-1">
                            {portalLinks.map((link) => (
                                <Link key={link.href} href={link.href} onClick={() => setIsMobileMenuOpen(false)}>
                                    <Button
                                        variant="ghost"
                                        className="w-full justify-start gap-3 mb-1 text-slate-300 hover:bg-slate-700"
                                    >
                                        <link.icon className="h-5 w-5" />
                                        {link.label}
                                    </Button>
                                </Link>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="p-4 border-t border-slate-700 bg-slate-900/50">
                    <div className="flex items-center gap-3 mb-4 px-2">
                        <div className="h-10 w-10 rounded-lg bg-purple-600 flex items-center justify-center text-white font-bold shadow-lg shadow-purple-900/20">
                            {user?.username?.charAt(0).toUpperCase()}
                        </div>
                        <div className="overflow-hidden">
                            <p className="text-sm font-medium truncate">{user?.username}</p>
                            <p className="text-[10px] text-purple-400 font-mono uppercase">Master Dev</p>
                        </div>
                    </div>
                    <Button
                        variant="ghost"
                        className="w-full justify-start gap-3 text-red-400 hover:bg-red-950/30 hover:text-red-300"
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
            <main className="flex-1 md:ml-64 p-4 md:p-8 pt-20 md:pt-8 bg-slate-950 min-h-screen">
                <div className="max-w-7xl mx-auto animate-in fade-in slide-in-from-bottom-2 duration-500">
                    {children}
                </div>
            </main>

            {/* Backdrop for mobile */}
            {isMobileMenuOpen && (
                <div
                    className="fixed inset-0 bg-black/60 z-30 md:hidden backdrop-blur-sm"
                    onClick={() => setIsMobileMenuOpen(false)}
                />
            )}
        </div>
    );
}

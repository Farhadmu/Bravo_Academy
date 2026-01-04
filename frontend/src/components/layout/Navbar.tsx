'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuthStore } from '@/store/auth';
import { Button } from '@/components/ui/button';
import { Menu, X, Shield, User, LogOut } from 'lucide-react';
import { useState } from 'react';

export default function Navbar() {
    const pathname = usePathname();
    const { user, isAuthenticated, logout } = useAuthStore();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const isActive = (path: string) => pathname === path;

    const publicLinks = [
        { href: '/', label: 'Home' },
        { href: '/about', label: 'About' },
        { href: '/leadership', label: 'Leadership' },
        { href: '/contact', label: 'Contact' },
        { href: '/sample-test', label: 'Free Sample Test' },
    ];

    const dashboardLinks = [
        { href: user?.role === 'admin' ? '/admin/dashboard' : '/dashboard', label: 'Overview' },
        { href: user?.role === 'admin' ? '/admin/tests' : '/dashboard/tests', label: user?.role === 'admin' ? 'Tests' : 'Take IQ Test' },
        { href: user?.role === 'admin' ? '/admin/users' : '/dashboard/results', label: user?.role === 'admin' ? 'Users' : 'My Results' },
        { href: user?.role === 'admin' ? '/admin/settings' : '/dashboard/profile', label: user?.role === 'admin' ? 'Settings' : 'Profile' },
    ];

    const isPortal = pathname.startsWith('/admin') || pathname.startsWith('/dashboard');

    if (isPortal) return null;

    return (
        <nav className="bg-white border-b sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex items-center">
                        <Link href="/" className="flex items-center gap-2">
                            <Shield className="h-8 w-8 text-blue-600" />
                            <span className="font-bold text-xl text-gray-900">Bravo Academy</span>
                        </Link>
                    </div>

                    {/* Desktop Menu */}
                    <div className="hidden md:flex items-center space-x-8">
                        {publicLinks.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={`text-sm font-medium transition-colors hover:text-blue-600 ${isActive(link.href) ? 'text-blue-600' : 'text-gray-600'
                                    }`}
                            >
                                {link.label}
                            </Link>
                        ))}

                        {isAuthenticated ? (
                            <div className="flex items-center gap-4">
                                <Link href={user?.role === 'admin' ? '/admin/dashboard' : '/dashboard'}>
                                    <Button variant="ghost" className="flex items-center gap-2">
                                        <User className="h-4 w-4" />
                                        Dashboard
                                    </Button>
                                </Link>
                                <Button variant="outline" onClick={() => logout()} className="flex items-center gap-2">
                                    <LogOut className="h-4 w-4" />
                                    Logout
                                </Button>
                            </div>
                        ) : (
                            <div className="flex items-center gap-4">
                                <Link href="/login">
                                    <Button variant="ghost">Login</Button>
                                </Link>
                                <Link href="/register">
                                    <Button>Register</Button>
                                </Link>
                            </div>
                        )}
                    </div>

                    {/* Mobile menu button */}
                    <div className="flex items-center md:hidden">
                        <button
                            onClick={() => setIsMenuOpen(!isMenuOpen)}
                            className="text-gray-600 hover:text-gray-900 focus:outline-none"
                        >
                            {isMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMenuOpen && (
                <div className="md:hidden">
                    <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white border-b">
                        {publicLinks.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                className={`block px-3 py-2 rounded-md text-base font-medium ${isActive(link.href)
                                    ? 'bg-blue-50 text-blue-600'
                                    : 'text-gray-600 hover:bg-gray-50'
                                    }`}
                                onClick={() => setIsMenuOpen(false)}
                            >
                                {link.label}
                            </Link>
                        ))}
                        {isAuthenticated ? (
                            <>
                                <div className="border-t border-gray-200 my-2 pt-2">
                                    <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                                        Dashboard
                                    </div>
                                    {dashboardLinks.map((link) => (
                                        <Link
                                            key={link.href}
                                            href={link.href}
                                            className={`block px-3 py-2 rounded-md text-base font-medium ${isActive(link.href)
                                                ? 'bg-blue-50 text-blue-600'
                                                : 'text-gray-600 hover:bg-gray-50'
                                                }`}
                                            onClick={() => setIsMenuOpen(false)}
                                        >
                                            {link.label}
                                        </Link>
                                    ))}
                                </div>
                                <button
                                    onClick={() => {
                                        logout();
                                        setIsMenuOpen(false);
                                    }}
                                    className="w-full text-left block px-3 py-2 rounded-md text-base font-medium text-red-600 hover:bg-red-50"
                                >
                                    Logout
                                </button>
                            </>
                        ) : (
                            <div className="mt-4 flex flex-col gap-2 px-3">
                                <Link href="/login" onClick={() => setIsMenuOpen(false)}>
                                    <Button variant="outline" className="w-full">Login</Button>
                                </Link>
                                <Link href="/register" onClick={() => setIsMenuOpen(false)}>
                                    <Button className="w-full">Register</Button>
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </nav>
    );
}

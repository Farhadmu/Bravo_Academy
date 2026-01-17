'use client';
import { usePathname } from 'next/navigation';

export default function Footer() {
    const pathname = usePathname();
    const isPortal = pathname.startsWith('/admin') || pathname.startsWith('/dashboard');

    if (isPortal) return null;

    return (
        <footer className="bg-gray-900 text-white">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div>
                        <div className="flex items-center gap-3 mb-4">
                            <img src="/images/logo.jpg" alt="Bravo Academy" className="h-8 w-8 rounded-md object-cover" />
                            <h3 className="text-lg font-semibold">Bravo Academy</h3>
                        </div>
                        <p className="text-gray-400 text-sm">
                            Premium preparation platform for IQ tests and comprehensive coaching.
                            Master your skills with our expert-led practice materials.
                        </p>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
                        <ul className="space-y-2 text-sm text-gray-400">
                            <li><a href="/about" className="hover:text-white transition-colors">About Us</a></li>
                            <li><a href="/leadership" className="hover:text-white transition-colors">Leadership</a></li>
                            <li><a href="/contact" className="hover:text-white transition-colors">Contact</a></li>
                            <li><a href="/sample-test" className="hover:text-white transition-colors">Free Sample Test</a></li>
                            <li><a href="/dashboard" className="hover:text-white transition-colors">Student Dashboard</a></li>
                        </ul>
                    </div>
                    <div>
                        <h3 className="text-lg font-semibold mb-4">Contact Info</h3>
                        <ul className="space-y-2 text-sm text-gray-400">
                            <li>Phone: 01979486096</li>
                            <li>WhatsApp: 01979486096</li>
                        </ul>
                    </div>
                </div>
                <div className="mt-8 pt-8 border-t border-gray-800 text-center text-sm text-gray-400">
                    <p>&copy; {new Date().getFullYear()} Bravo Academy. All rights reserved.</p>
                </div>
            </div>
        </footer>
    );
}

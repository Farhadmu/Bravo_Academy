'use client';

import { Toaster } from 'sonner';
import { BackendWakeupManager } from '@/components/common/BackendWakeupManager';

export function Providers({ children }: { children: React.ReactNode }) {
    return (
        <>
            {children}
            <BackendWakeupManager />
            <Toaster position="top-center" richColors closeButton duration={5000} />
        </>
    );
}

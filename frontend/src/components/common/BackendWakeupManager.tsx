"use client";

import { create } from "zustand";
import { useEffect, useRef } from "react";
import { toast } from "sonner";
import { Spinner } from "@/components/ui/spinner";

interface WakeupState {
    isWakingUp: boolean;
    setWakingUp: (waking: boolean) => void;
}

export const useWakeupStore = create<WakeupState>((set) => ({
    isWakingUp: false,
    setWakingUp: (waking) => set({ isWakingUp: waking }),
}));

function wakeUpBackend() {
    const { setWakingUp } = useWakeupStore.getState();
    setWakingUp(true);
    const base = process.env.NEXT_PUBLIC_API_URL || 'https://online-education-platform-fypx.onrender.com/api';
    const url = base.replace(/\/+$/, '');
    fetch(`${url}/health/`, { method: 'GET', mode: 'cors' })
        .then(() => setWakingUp(false))
        .catch(() => {
            // Retry once after a short delay in case of cold-start failure
            setTimeout(() => {
                fetch(`${url}/health/`, { method: 'GET', mode: 'cors' })
                    .then(() => setWakingUp(false))
                    .catch(() => setWakingUp(false));
            }, 5000);
        });
}

export function BackendWakeupManager() {
    const isWakingUp = useWakeupStore((state) => state.isWakingUp);
    const toastIdRef = useRef<string | number | null>(null);
    const wokenRef = useRef(false);

    useEffect(() => {
        if (!wokenRef.current) {
            wokenRef.current = true;
            wakeUpBackend();
        }
    }, []);

    useEffect(() => {
        if (isWakingUp && !toastIdRef.current) {
            toastIdRef.current = toast.info(
                "Connecting to our secure servers...",
                {
                    description: "We are warming up the engine to provide you with the best experience. This usually takes about 30 seconds after a period of inactivity.",
                    icon: <Spinner size="sm" className="text-blue-500" />,
                    duration: Infinity,
                    dismissible: false,
                    className: "bg-background border-primary/20 shadow-lg",
                }
            );
        } else if (!isWakingUp && toastIdRef.current) {
            toast.dismiss(toastIdRef.current);
            toastIdRef.current = null;
            toast.success("Connection established! Welcome back.", {
                duration: 3000,
            });
        }
    }, [isWakingUp]);

    return null;
}

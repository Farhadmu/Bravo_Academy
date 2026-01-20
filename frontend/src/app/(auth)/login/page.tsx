'use client';

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuthStore } from '@/store/auth'
import api from '@/lib/api'
import { Shield, AlertCircle, Info } from "lucide-react"
import { toast } from 'sonner'

const loginSchema = z.object({
    username: z.string().min(1, 'Username is required'),
    password: z.string().min(1, 'Password is required'),
})

type FormData = z.infer<typeof loginSchema>

export default function LoginPage() {
    const router = useRouter()
    const login = useAuthStore((state) => state.login)
    const { user, isAuthenticated } = useAuthStore()
    const [isLoading, setIsLoading] = useState(false)
    const [mounted, setMounted] = useState(false)
    const [slowLoadId, setSlowLoadId] = useState<string | number | null>(null)
    const [maintenance, setMaintenance] = useState<{ is_active: boolean; message: string } | null>(null)

    useEffect(() => {
        setMounted(true)
        // Check maintenance status
        api.get('/system/maintenance/current/')
            .then(res => setMaintenance(res.data))
            .catch(() => { })
    }, [])

    useEffect(() => {
        if (mounted && isAuthenticated && user) {
            if (user.role === 'developer') {
                router.push('/developer')
            } else if (user.role === 'admin') {
                router.push('/admin/dashboard')
            } else {
                router.push('/dashboard')
            }
        }
    }, [mounted, isAuthenticated, user, router])

    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(loginSchema),
    })

    const onSubmit = async (data: FormData) => {
        if (!navigator.onLine) {
            toast.error('No internet connection. Please check your network.', {
                description: 'Weak or missing internet detected.'
            })
            return
        }

        setIsLoading(true)

        // Setup cold-start timer
        const timer = setTimeout(() => {
            const id = toast.info('Our server is waking up...', {
                description: 'It might take up to a minute to start the backend. Please stay with us!',
                duration: 10000,
                icon: <Info className="w-4 h-4" />
            })
            setSlowLoadId(id)
        }, 5000)

        try {
            const response = await api.post('/auth/login/', {
                username: data.username,
                password: data.password,
            });

            const { user, access, refresh } = response.data

            // Clear slow load toast if it exists
            if (slowLoadId) toast.dismiss(slowLoadId)
            clearTimeout(timer)

            login(user, access, refresh)
            toast.success('Logged in successfully!')

            if (user.role === 'developer') {
                router.push('/developer')
            } else if (user.role === 'admin') {
                router.push('/admin/dashboard')
            } else {
                router.push('/dashboard')
            }
        } catch (err: any) {
            clearTimeout(timer)
            if (slowLoadId) toast.dismiss(slowLoadId)

            let message = 'Login failed'
            let description = 'Please check your username and password and try again.'

            if (err.response?.status === 503) {
                message = 'Maintenance Mode'
                description = err.response.data.message || 'The system is under maintenance. Please try again later.'
            } else if (err.response?.status === 403) {
                message = 'Device Lock Active'
                description = err.response.data.error || err.response.data.detail || 'This ID is already logged in on another device.'
            } else if (err.response?.status === 401) {
                message = err.response.data.error || 'Invalid Credentials'
                description = err.response.data.detail || 'The username or password you entered is incorrect.'
            } else if (!err.response) {
                message = 'Network Error'
                description = 'Could not reach the server. Your internet might be weak or our server is down.'
            }

            toast.error(message, {
                description,
                duration: 8000
            })
        } finally {
            setIsLoading(false)
        }
    }

    if (!mounted || isAuthenticated) {
        return null
    }

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 px-4 py-12 sm:px-6 lg:px-8">
            {maintenance?.is_active && (
                <div className="w-full max-w-md mb-4 animate-in slide-in-from-top duration-500">
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex gap-3 shadow-md">
                        <AlertCircle className="h-5 w-5 text-yellow-600 flex-shrink-0" />
                        <div>
                            <p className="text-sm font-bold text-yellow-800 uppercase tracking-wider mb-1">System Maintenance</p>
                            <p className="text-xs text-yellow-700">{maintenance.message}</p>
                        </div>
                    </div>
                </div>
            )}
            <Card className="w-full max-w-md shadow-xl">
                <CardHeader className="text-center">
                    <div className="mx-auto bg-blue-100 p-3 rounded-full w-fit mb-4">
                        <Shield className="w-8 h-8 text-blue-600" />
                    </div>
                    <CardTitle className="text-2xl font-bold">Welcome Back</CardTitle>
                    <CardDescription>Enter your credentials to access your dashboard</CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                        <div className="space-y-2">
                            <label htmlFor="username" className="text-sm font-medium text-gray-700">Username</label>
                            <Input
                                id="username"
                                type="text"
                                {...register('username')}
                                className={errors.username ? "border-red-500" : ""}
                            />
                            {errors.username && <p className="text-red-500 text-xs">{errors.username.message}</p>}
                        </div>

                        <div className="space-y-2">
                            <label htmlFor="password" className="text-sm font-medium text-gray-700">Password</label>
                            <Input
                                id="password"
                                type="password"
                                {...register('password')}
                                className={errors.password ? "border-red-500" : ""}
                            />
                            {errors.password && <p className="text-red-500 text-xs">{errors.password.message}</p>}
                        </div>

                        <Button type="submit" className="w-full h-10" disabled={isLoading}>
                            {isLoading ? "Connecting..." : "Login"}
                        </Button>
                    </form>
                </CardContent>
                <CardFooter className="justify-center flex-col gap-2 border-t pt-6 bg-gray-50/50 rounded-b-lg">
                    <p className="text-sm text-gray-600">
                        Don't have an account?{' '}
                        <Link href="/register" className="text-blue-600 hover:underline font-medium">
                            Register Now
                        </Link>
                    </p>
                    <p className="text-xs text-gray-400 max-w-xs text-center">
                        Note: You are only allowed to login from one designated device.
                    </p>
                </CardFooter>
            </Card>
        </div>
    )
}

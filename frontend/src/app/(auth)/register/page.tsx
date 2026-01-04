'use client';

import Link from 'next/link'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { CheckCircle, Shield, Smartphone, Banknote } from "lucide-react"

export default function RegisterPage() {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-12 sm:px-6 lg:px-8">
            <Card className="w-full max-w-2xl shadow-xl">
                <CardHeader className="text-center">
                    <div className="mx-auto bg-blue-100 p-3 rounded-full w-fit mb-4">
                        <Shield className="w-8 h-8 text-blue-600" />
                    </div>
                    <CardTitle className="text-2xl font-bold">Join Our Premium Program</CardTitle>
                    <CardDescription>Follow the steps below to get your access credentials</CardDescription>
                </CardHeader>
                <CardContent className="space-y-8">

                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                        <h3 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
                            <Shield className="w-5 h-5" /> Account Activation Process
                        </h3>
                        <p className="text-sm text-blue-800">
                            For security and premium quality control, we manually verify all students.
                            Please complete the payment and send verification to receive your username and password.
                        </p>
                    </div>

                    <div className="space-y-6">
                        <div className="flex gap-4">
                            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">1</div>
                            <div>
                                <h4 className="font-bold text-gray-900">Make Payment</h4>
                                <p className="text-sm text-gray-600 mb-2">Send <span className="font-bold text-gray-900">1000 BDT</span> to our official bKash number:</p>
                                <div className="bg-pink-50 border border-pink-200 p-3 rounded-md inline-flex items-center gap-2">
                                    <span className="font-mono text-lg font-bold text-pink-700">01979-486096</span>
                                    <span className="text-xs bg-pink-200 text-pink-800 px-2 py-0.5 rounded-full">Personal</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex gap-4">
                            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">2</div>
                            <div>
                                <h4 className="font-bold text-gray-900">Take a Screenshot</h4>
                                <p className="text-sm text-gray-600">
                                    After successful payment, take a clear screenshot of the transaction.
                                </p>
                            </div>
                        </div>

                        <div className="flex gap-4">
                            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">3</div>
                            <div>
                                <h4 className="font-bold text-gray-900">Send via WhatsApp</h4>
                                <p className="text-sm text-gray-600 mb-2">
                                    Send the screenshot along with your <span className="font-semibold">Full Name</span> to our WhatsApp number:
                                </p>
                                <Button asChild className="bg-green-600 hover:bg-green-700 text-white w-full sm:w-auto h-12 text-lg cursor-pointer">
                                    <a href="https://wa.me/8801979486096" target="_blank" rel="noopener noreferrer" className="flex items-center">
                                        <Smartphone className="w-5 h-5 mr-2" />
                                        Chat on WhatsApp
                                    </a>
                                </Button>
                            </div>
                        </div>

                        <div className="flex gap-4">
                            <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold">4</div>
                            <div>
                                <h4 className="font-bold text-gray-900">Get Credentials</h4>
                                <p className="text-sm text-gray-600">
                                    Our admin will verify your payment and send your unique <strong>Username</strong> and <strong>Password</strong> on WhatsApp within 30 minutes.
                                </p>
                            </div>
                        </div>
                    </div>

                </CardContent>
                <CardFooter className="justify-center border-t pt-6 bg-gray-50/50 rounded-b-lg">
                    <p className="text-sm text-gray-600">
                        Already received your credentials?{' '}
                        <Link href="/login" className="text-blue-600 hover:underline font-medium">
                            Login to Dashboard
                        </Link>
                    </p>
                </CardFooter>
            </Card>
        </div>
    )
}

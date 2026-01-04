'use client';

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Mail, Phone, MapPin, Send } from "lucide-react"

export default function ContactPage() {
    return (
        <div className="py-12 bg-gray-50 min-h-screen">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="text-center mb-16">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">Contact Us</h1>
                    <p className="text-xl text-gray-600 max-w-2xl mx-auto">
                        Have questions about our programs or need assistance? We&apos;re here to help you on your journey.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                    {/* Contact Form */}
                    <Card className="shadow-lg border-none">
                        <CardHeader>
                            <CardTitle>Send us a Message</CardTitle>
                            <CardDescription>Fill out the form below and we&apos;ll get back to you shortly.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form className="space-y-6">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label htmlFor="name" className="text-sm font-medium text-gray-700">Name</label>
                                        <Input id="name" placeholder="John Doe" />
                                    </div>
                                    <div className="space-y-2">
                                        <label htmlFor="email" className="text-sm font-medium text-gray-700">Email</label>
                                        <Input id="email" type="email" placeholder="john@example.com" />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="subject" className="text-sm font-medium text-gray-700">Subject</label>
                                    <Input id="subject" placeholder="Course Inquiry" />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="message" className="text-sm font-medium text-gray-700">Message</label>
                                    <textarea
                                        id="message"
                                        rows={4}
                                        className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                        placeholder="How can we help you?"
                                    />
                                </div>
                                <Button className="w-full h-11 text-lg">
                                    <Send className="w-4 h-4 mr-2" /> Send Message
                                </Button>
                            </form>
                        </CardContent>
                    </Card>

                    {/* Contact Info */}
                    <div className="space-y-8">
                        <Card className="shadow-md border-none">
                            <CardContent className="pt-6 flex items-start gap-4">
                                <div className="p-3 bg-green-100 rounded-lg">
                                    <Phone className="w-6 h-6 text-green-600" />
                                </div>
                                <div>
                                    <h3 className="font-bold text-gray-900 mb-1">Contact Details</h3>
                                    <p className="text-gray-600">Phone: 01979486096</p>
                                    <p className="text-gray-600">WhatsApp: 01979486096</p>
                                    <div className="mt-4">
                                        <Button asChild className="bg-green-600 hover:bg-green-700 text-white cursor-pointer w-full">
                                            <a href="https://wa.me/8801979486096" target="_blank" rel="noopener noreferrer">
                                                Message on WhatsApp
                                            </a>
                                        </Button>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        <div className="bg-blue-50 p-6 rounded-xl border border-blue-100">
                            <h3 className="font-bold text-blue-900 mb-2">Office Hours</h3>
                            <p className="text-blue-800 text-sm">
                                We are available on WhatsApp and Phone from 9:00 AM to 9:00 PM every day.
                            </p>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    )
}

import { Card, CardContent } from "@/components/ui/card"
import { Shield, Target, Award, Users } from "lucide-react"

export default function AboutPage() {
    return (
        <div className="py-12 bg-gray-50 min-h-screen">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                {/* Header */}
                <div className="text-center mb-16">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">About Bravo Academy</h1>
                    <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                        We are dedicated to shaping the future leaders through comprehensive preparation and expert guidance.
                    </p>
                </div>

                {/* Mission & Vision */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-20">
                    <div className="bg-white p-8 rounded-2xl shadow-sm">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="p-3 bg-blue-100 rounded-lg">
                                <Target className="w-8 h-8 text-blue-600" />
                            </div>
                            <h2 className="text-2xl font-bold text-gray-900">Our Mission</h2>
                        </div>
                        <p className="text-gray-600 leading-relaxed">
                            To provide the highest quality IQ training and coaching for aspirants, enabling them to realize their dreams of serving with honor and distinction. We prioritize integrity, excellence, and discipline in all our endeavors.
                        </p>
                    </div>
                    <div className="bg-white p-8 rounded-2xl shadow-sm">
                        <div className="flex items-center gap-4 mb-6">
                            <div className="p-3 bg-green-100 rounded-lg">
                                <Shield className="w-8 h-8 text-green-600" />
                            </div>
                            <h2 className="text-2xl font-bold text-gray-900">Our Vision</h2>
                        </div>
                        <p className="text-gray-600 leading-relaxed">
                            To be the premier coaching institution in the country, recognized for our exceptional success rate, innovative teaching methodologies, and commitment to holistic development.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}

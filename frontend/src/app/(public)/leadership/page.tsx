import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Mail, Shield, Code, Server, BarChart, Zap } from 'lucide-react';

export default function LeadershipPage() {
    return (
        <div className="min-h-screen bg-slate-50">
            {/* Hero Section */}
            <div className="bg-white border-b">
                <div className="max-w-7xl mx-auto px-4 py-12 md:py-20 sm:px-6 lg:px-8">
                    <div className="text-center">
                        <h1 className="text-3xl font-extrabold text-slate-900 sm:text-5xl sm:tracking-tight lg:text-7xl">
                            Leadership & Technology
                        </h1>
                        <p className="mt-4 md:mt-6 max-w-2xl mx-auto text-lg md:text-xl text-slate-500 leading-relaxed px-2">
                            Driving the technical vision and engineering excellence behind the Bangladesh Bravo Academy digital ecosystem.
                        </p>
                    </div>
                </div>
            </div>

            {/* Profile Section */}
            <div className="max-w-7xl mx-auto px-4 py-12 md:py-20 sm:px-6 lg:px-8">
                <div className="flex flex-col lg:grid lg:grid-cols-12 lg:gap-16 items-start">
                    <div className="w-full lg:col-span-5 relative group">
                        <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                        <div className="relative aspect-[4/5] sm:aspect-[3/4] lg:aspect-[3/4] overflow-hidden rounded-2xl shadow-2xl mx-auto max-w-md lg:max-w-none">
                            <Image
                                src="/sakibur-rahman.jpg"
                                alt="Sakibur Rahman"
                                fill
                                className="object-cover transition duration-500 group-hover:scale-105"
                                priority
                            />
                        </div>
                    </div>

                    <div className="w-full lg:col-span-7 mt-10 lg:mt-0">
                        <div className="space-y-6 md:space-y-8">
                            <div className="text-center lg:text-left">
                                <h2 className="text-3xl md:text-4xl font-bold text-slate-900 tracking-tight">Sakibur Rahman</h2>
                                <p className="text-blue-600 font-bold uppercase tracking-widest mt-2 text-sm md:text-base">
                                    Lead Software Architect & Platform Engineer
                                </p>
                            </div>

                            <div className="prose prose-slate text-slate-600 max-w-none space-y-4 md:space-y-6">
                                <p className="text-base md:text-lg leading-relaxed text-center lg:text-left">
                                    Sakibur Rahman is responsible for the design, engineering, and ongoing technical development of the Bangladesh Bravo Academy digital testing platform.
                                </p>
                                <p className="text-base md:text-lg leading-relaxed text-center lg:text-left">
                                    The system was architected as a proprietary, internal platform to meet the specific operational requirements of ISSB cognitive preparation, including strict time enforcement, controlled access, and detailed performance analysis.
                                </p>
                                <div className="bg-blue-50/50 p-6 rounded-xl border-l-4 border-blue-500">
                                    <p className="text-base md:text-lg leading-relaxed italic text-slate-700 m-0">
                                        The platform was developed to avoid reliance on generic third-party testing tools and to maintain full control over security, data integrity, and system evolution.
                                    </p>
                                </div>
                            </div>

                            <div className="flex flex-col sm:flex-row gap-4 pt-4 justify-center lg:justify-start">
                                <Link href="mailto:sakiburrahmannnn@gmail.com" className="w-full sm:w-auto">
                                    <Button className="w-full flex items-center justify-center gap-2 h-12 text-base shadow-lg shadow-blue-600/20">
                                        <Mail className="h-5 w-5" />
                                        Contact via Email
                                    </Button>
                                </Link>
                                <Link href="/about" className="w-full sm:w-auto">
                                    <Button variant="outline" className="w-full h-12 text-base">Learn About Academy</Button>
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Technical Responsibilities */}
            <div className="bg-slate-900 py-16 md:py-24 text-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-12 md:mb-20">
                        <h2 className="text-3xl md:text-4xl font-bold tracking-tight">Technical Responsibilities</h2>
                        <div className="mt-4 h-1 w-20 bg-blue-500 mx-auto rounded-full"></div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 lg:gap-10">
                        {[
                            {
                                icon: <Server className="h-6 w-6" />,
                                title: "System Architecture",
                                desc: "End-to-end architecture design focusing on scalability, security, and high-performance backend engineering."
                            },
                            {
                                icon: <Shield className="h-6 w-6" />,
                                title: "Authentication & Control",
                                desc: "Implementation of secure JWT-based authentication and advanced device fingerprinting for session control."
                            },
                            {
                                icon: <Zap className="h-6 w-6" />,
                                title: "Testing Engine",
                                desc: "Development of a highly accurate, time-enforced IQ testing engine tailored for defense selection board standards."
                            },
                            {
                                icon: <BarChart className="h-6 w-6" />,
                                title: "Performance Analytics",
                                desc: "Construction of complex progress evaluation systems and real-time performance analytics for officer candidates."
                            },
                            {
                                icon: <Code className="h-6 w-6" />,
                                title: "Frontend Engineering",
                                desc: "Crafting modern, responsive UI/UX using Next.js to provide an immersive digital testing experience."
                            },
                            {
                                icon: <Shield className="h-6 w-6" />,
                                title: "Production Infrastructure",
                                desc: "Managing global deployment infrastructure, ensuring maximum uptime and data reliability for all users."
                            }
                        ].map((item, idx) => (
                            <div key={idx} className="bg-slate-800/40 p-6 md:p-8 rounded-2xl border border-slate-700/50 hover:border-blue-500/50 transition-all duration-300 hover:shadow-2xl hover:shadow-blue-500/5 group">
                                <div className="p-3 bg-blue-600/10 rounded-xl w-fit text-blue-500 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300 mb-6 shadow-inner">
                                    {item.icon}
                                </div>
                                <h3 className="text-xl font-bold mb-3 tracking-tight">{item.title}</h3>
                                <p className="text-slate-400 leading-relaxed text-sm md:text-base">
                                    {item.desc}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Engagement Section */}
            <div className="max-w-7xl mx-auto px-4 py-16 md:py-24 sm:px-6 lg:px-8">
                <div className="bg-white rounded-3xl p-8 md:p-12 lg:p-16 shadow-2xl shadow-slate-200/50 border border-slate-100 flex flex-col lg:flex-row items-center gap-10 lg:gap-16">
                    <div className="flex-1 text-center lg:text-left">
                        <h2 className="text-2xl md:text-3xl font-bold text-slate-900 mb-4 md:mb-6">Independent Technical Engagements</h2>
                        <p className="text-base md:text-lg text-slate-600 mb-8 max-w-2xl mx-auto lg:mx-0">
                            For organizations or institutions seeking the design and development of secure, large-scale assessment platforms or similar digital systems, technical discussions may be directed to the architect.
                        </p>
                        <div className="flex justify-center lg:justify-start">
                            <Link href="mailto:sakiburrahmannnn@gmail.com" className="text-xl md:text-2xl font-bold text-blue-600 hover:text-blue-700 transition-colors flex items-center gap-3 break-all">
                                <Mail className="h-6 w-6 flex-shrink-0" />
                                <span>sakiburrahmannnn@gmail.com</span>
                            </Link>
                        </div>
                    </div>
                    <div className="w-full lg:w-auto">
                        <div className="p-6 bg-slate-50 rounded-2xl border-2 border-dashed border-slate-200">
                            <p className="text-center font-bold text-slate-500 uppercase tracking-widest text-sm">Available for Enterprise Solutions</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Footer Text */}
            <div className="max-w-7xl mx-auto px-4 pb-16 text-center">
                <p className="text-slate-400 italic text-sm md:text-base max-w-3xl mx-auto">
                    The platform represents a long-term technical investment in building reliable, scalable, and secure digital infrastructure aligned with defense-oriented training standards.
                </p>
            </div>
        </div>
    );
}

import { motion } from "framer-motion";
import {
    Search,
    Globe,
    Code,
    Database,
    FileText,
    MessageSquare,
    Zap,
} from "lucide-react";
import { PowerUpCard } from "@/components/power-ups/PowerUpCard";
import { ChatPane } from "@/components/power-ups/ChatPane";
import { PowerUpBlocks } from "@/components/power-ups/PowerUpBlocks";
import { isMobile } from "react-device-detect";
import Image from "next/image";
import { useState } from "react";
import toast from "react-hot-toast";

const cardColors = [
    "from-purple-500 to-blue-500",
    "from-blue-500 to-cyan-500",
    "from-emerald-500 to-green-500",
    "from-amber-500 to-orange-500",
    "from-pink-500 to-rose-500",
];

const powerUps = [
    {
        icon: Search,
        name: "Google Search",
        description: "Search the web",
    },
    {
        icon: Globe,
        name: "Browse Website",
        description: "Navigate and analyze web content intelligently",
    },
    {
        icon: Code,
        name: "Code Assistant",
        description: "Get help with coding and debugging",
    },
    {
        icon: Database,
        name: "Data Processing",
        description: "Process and analyze data efficiently",
    },
    {
        icon: FileText,
        name: "Document Analysis",
        description: "Extract insights from documents",
    },
    {
        icon: MessageSquare,
        name: "Chat Enhancement",
        description: "Advanced conversation capabilities",
    },
    {
        icon: Zap,
        name: "Quick Actions",
        description: "Perform common tasks instantly",
    },
];

function App() {
    const [activeTools, setActiveTools] = useState<string[]>([]);

    const handleActiveToolsChange = (tools: string[]) => {
        setActiveTools(tools);
    };

    return (
        <div className="min-h-screen bg-[none]">
            <motion.div
                className="absolute inset-0 opacity-30"
                initial={{ scale: 0 }}
                animate={{ scale: 2 }}
                transition={{ duration: 0.5 }}
            >
                <div className="from-[rgba(255, 255, 255, 0.80)] to-[rgba(129, 255, 254, 0.50)] absolute inset-0 bg-gradient-to-r blur-3xl" />
            </motion.div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.8, ease: "easeOut" }}
                style={{
                    position: "absolute",
                    top: isMobile ? "30vh" : "-15vh",
                    left: 0,
                    right: 0,
                    width: isMobile ? "100vw" : "100vw",
                    margin: "0 auto",
                    zIndex: 0,
                    height: isMobile ? "50vh" : "150%",
                    opacity: 0.7,
                }}
            >
                <Image
                    src="/images/v3/hero/bg-glow-new.png"
                    alt="Background glow effect"
                    priority
                    width={2000}
                    height={2000}
                    loading="eager"
                    className="opacity-50"
                />
            </motion.div>

            {/* Hero Section */}
            <section className="relative overflow-hidden">
                <div className="container relative mx-auto px-4 pb-16 pt-24 text-center">
                    <motion.h1
                        className="mb-6 text-4xl font-bold md:text-6xl"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.5 }}
                        style={{
                            background:
                                "linear-gradient(90deg, rgba(255, 255, 255, 0.80) -9.85%, rgba(129, 255, 254, 0.50) 99.95%)",
                            backgroundClip: "text",
                            WebkitBackgroundClip: "text",
                            WebkitTextFillColor: "transparent",
                            textShadow:
                                "0px 0px 16px rgba(255, 255, 255, 0.32)",
                        }}
                    >
                        PowerUps 4 All
                    </motion.h1>
                    <motion.p
                        className="mx-auto max-w-2xl text-xl"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.7 }}
                        style={{
                            background:
                                "linear-gradient(90deg, rgba(255, 255, 255, 0.72) 0%, rgba(255, 255, 255, 0.36) 100%)",
                            backgroundClip: "text",
                            WebkitBackgroundClip: "text",
                            WebkitTextFillColor: "transparent",
                        }}
                    >
                        Plug and play function tools to pass to GPT / Claude.{" "}
                        <br />
                        Don't reinvent wheels, just use powerups.
                    </motion.p>
                </div>
            </section>

            {/* Split Pane Section */}
            <motion.div
                className="container mx-auto max-w-5xl py-4"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
            >
                <div
                    className="flex flex-col items-center justify-center"
                    style={{
                        background:
                            "linear-gradient(179deg, rgba(0, 135, 145, 0.2) 0.52%, rgba(0, 40, 43, 0.4) 99.46%)",
                        backdropFilter: "blur(10px)",
                        boxShadow:
                            "0px 16px 32px 0px rgba(255, 255, 255, 0.05) inset",
                        border: "1px solid rgba(255, 255, 255, 0.1)",
                        borderRadius: "1.5rem",
                    }}
                >
                    <div
                        className="flex w-full flex-row items-start justify-center"
                        style={{ height: "65vh" }}
                    >
                        <PowerUpBlocks
                            onActiveBlocksChange={handleActiveToolsChange}
                        />
                        <div
                            className="mx-auto h-[90%] w-[0.5px]"
                            style={{
                                opacity: 0.5,
                                background:
                                    "linear-gradient(to bottom, rgba(129, 255, 254, 0.7), rgba(0, 135, 145, 0.3))",
                                boxShadow:
                                    "0px 0px 8px rgba(129, 255, 254, 0.3)",
                            }}
                        />
                        <ChatPane activeTools={activeTools} />
                    </div>
                </div>
            </motion.div>

            {/* Copy Code Button */}
            <motion.button
                className="mx-auto mb-4 mt-2 flex w-64 items-center justify-center space-x-2 rounded-full py-2"
                onClick={() => {
                    const codeString = `openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = openai_client.responses.create(
    model="gpt-4o",
    input=[{"role": "user", "content": request.message}],
    tools=[${activeTools
        .map((tool) => `get_tool_definition("${tool}")`)
        .join(", ")}]
)`;
                    navigator.clipboard.writeText(codeString);
                    // Optional: Add feedback for successful copy
                    toast.success("Code copied to clipboard!");
                }}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                whileHover={{ scale: 1.05 }}
                style={{
                    background: "rgba(0, 0, 0, 0.1)",
                    backdropFilter: "blur(5px)",
                    border: "1px solid rgba(129, 255, 254, 0.3)",
                }}
            >
                <Code size={16} className="text-gray-300" />
                <span className="text-gray-300">Copy Integration Code</span>
            </motion.button>

            {/* Scrolling Gallery */}
            <section className=" mx-auto w-screen overflow-hidden px-4 py-12">
                <div className="space-y-0">
                    {/* First Row - Left to Right */}
                    <div className="relative">
                        <div
                            className="animate-infinite-scroll flex space-x-6 py-4"
                            style={{
                                animation: "scroll-left 30s linear infinite",
                            }}
                        >
                            {[...powerUps, ...powerUps]
                                .slice(0, 12)
                                .map((powerUp, index) => (
                                    <div
                                        key={`row1-${index}`}
                                        className="w-72 flex-shrink-0"
                                    >
                                        <PowerUpCard
                                            icon={powerUp.icon}
                                            name={powerUp.name}
                                            description={powerUp.description}
                                            gradient={
                                                cardColors[
                                                    index % cardColors.length
                                                ]
                                            }
                                        />
                                    </div>
                                ))}
                        </div>
                    </div>

                    {/* Second Row - Right to Left */}
                    <div className="relative">
                        <div
                            className="flex space-x-6 py-4"
                            style={{
                                animation: "scroll-right 35s linear infinite",
                            }}
                        >
                            {[...powerUps, ...powerUps]
                                .slice(0, 12)
                                .map((powerUp, index) => (
                                    <div
                                        key={`row2-${index}`}
                                        className="w-72 flex-shrink-0"
                                    >
                                        <PowerUpCard
                                            icon={powerUp.icon}
                                            name={powerUp.name}
                                            description={powerUp.description}
                                            gradient={
                                                cardColors[
                                                    (index + 3) %
                                                        cardColors.length
                                                ]
                                            }
                                        />
                                    </div>
                                ))}
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default App;

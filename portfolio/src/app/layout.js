import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "LoveDoLove - Full-Stack Developer & DevOps Engineer",
  description: "Innovative Full-Stack Developer & DevOps Engineer specializing in enterprise-level web applications, cross-platform automation, and scalable cloud infrastructure. Expert in C#/.NET, PHP/Laravel, Python, React/Next.js, and DevOps automation.",
  keywords: "Full-Stack Developer, DevOps Engineer, C# .NET, PHP Laravel, Python, React Next.js, GitHub Actions, FreeBSD, System Architecture, AI Machine Learning",
  author: "LoveDoLove",
  viewport: "width=device-width, initial-scale=1",
  charset: "utf-8",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}

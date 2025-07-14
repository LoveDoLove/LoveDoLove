export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <section className="text-center mb-16">
          <div className="animate-fadeIn">
            <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-6">
              LoveDoLove
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed">
              Innovative Full-Stack Developer & DevOps Engineer specializing in
              enterprise-level web applications, cross-platform automation, and
              scalable cloud infrastructure. Expert in building production-ready
              systems from concept to deployment.
            </p>
            <div className="flex flex-wrap justify-center gap-4 mb-8">
              <span className="px-4 py-2 bg-blue-600/20 rounded-full text-blue-300 border border-blue-500/30">
                Full-Stack Development
              </span>
              <span className="px-4 py-2 bg-purple-600/20 rounded-full text-purple-300 border border-purple-500/30">
                DevOps & Automation
              </span>
              <span className="px-4 py-2 bg-green-600/20 rounded-full text-green-300 border border-green-500/30">
                System Architecture
              </span>
              <span className="px-4 py-2 bg-orange-600/20 rounded-full text-orange-300 border border-orange-500/30">
                AI & Machine Learning
              </span>
            </div>
          </div>
        </section>
        <section className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Key Skills & Technology Stack
          </h2>
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            {/* Skillicons bar for visual stack, matching README */}
            <img
              src="https://skillicons.dev/icons?i=cs,dotnet,js,nodejs,express,vue,windows,githubactions,cloudflare,nginx,markdown,ci,firebase,azure,aws,selenium,php,py,html,css,tailwind,bootstrap,laravel,flask,mysql,sqlserver,open-source,freebsd,bash,raspberrypi,opencv,postman,git,vscode,visualstudio,apache,jupyter,matplotlib,numpy,pandas,c&perline=11"
              alt="Key Skills & Technology Stack"
              className="mx-auto"
              style={{ maxWidth: "100%" }}
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-800/50 rounded-lg p-6 border border-gray-700/50">
              <h3 className="text-xl font-semibold text-blue-400 mb-2">
                Top Mastery
              </h3>
              <ul className="text-gray-300 text-sm space-y-1">
                <li>
                  C#, .NET Core/ASP.NET Core, JavaScript, Node.js, Express,
                  Vue.js, Windows, GitHub Actions, Cloudflare, Nginx, Markdown,
                  CI/CD, Firebase, Azure, AWS, Selenium
                </li>
              </ul>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-6 border border-gray-700/50">
              <h3 className="text-xl font-semibold text-purple-400 mb-2">
                Intermediate
              </h3>
              <ul className="text-gray-300 text-sm space-y-1">
                <li>
                  PHP, Python, HTML, CSS, Tailwind, Bootstrap, Laravel, Flask,
                  MySQL, SQL Server, Open Source
                </li>
              </ul>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-6 border border-gray-700/50">
              <h3 className="text-xl font-semibold text-orange-400 mb-2">
                Exploratory/Support
              </h3>
              <ul className="text-gray-300 text-sm space-y-1">
                <li>
                  FreeBSD, Bash, Raspberry Pi, OpenCV, Postman, Git, VS Code,
                  Visual Studio, Apache, Jupyter Notebook, Matplotlib, NumPy,
                  Pandas, C
                </li>
              </ul>
            </div>
          </div>
        </section>
        {/* Projects Section */}
        <section className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Featured Projects
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: "Hotel Management System",
                description:
                  "Enterprise-grade hotel reservation platform with user registration, room booking, payment processing, admin dashboard, and comprehensive reporting features.",
                tech: [
                  "C#",
                  ".NET Core",
                  "Entity Framework",
                  "SQL Server",
                  "Bootstrap",
                ],
                status: "Production",
                link: "https://hotel.lovedolove.nyc.mn/",
              },
              {
                title: "FreeBSD Cross-Compilation Suite",
                description:
                  "Automated CI/CD pipelines for building popular applications (Alist, Memos, Cloudreve) for FreeBSD, featuring GitHub Actions and cross-platform toolchains.",
                tech: ["Shell", "GitHub Actions", "FreeBSD", "Go", "Docker"],
                status: "Open Source",
              },
              {
                title: "EasyKit - Windows Automation",
                description:
                  "Comprehensive Windows toolkit for automating common tasks, system maintenance, and productivity enhancement with intuitive GUI and batch processing.",
                tech: [
                  "C#",
                  "WinForms",
                  "PowerShell",
                  "Windows API",
                  "Automation",
                ],
                status: "Active",
              },
              {
                title: "Face Recognition Attendance System",
                description:
                  "AI-powered attendance tracking system using facial recognition technology with real-time processing, database integration, and administrative controls.",
                tech: ["PHP", "Python", "OpenCV", "MySQL", "Machine Learning"],
                status: "Live",
              },
              {
                title: "CS Common Utilities Library",
                description:
                  "Production-ready C#/.NET utility library featuring captcha generation, QR codes, email services, image processing, Stripe integration, and security tools.",
                tech: [
                  "C#",
                  ".NET 8",
                  "NuGet",
                  "Stripe API",
                  "Image Processing",
                ],
                status: "Package",
              },
              {
                title: "Laravel Setup Kit",
                description:
                  "Comprehensive Laravel starter template with Firebase integration, Spatie permissions, Stripe payments, SweetAlert2, and modern UI components.",
                tech: ["Laravel", "PHP", "Firebase", "Stripe", "Tailwind CSS"],
                status: "Template",
              },
            ].map((project, index) => (
              <div
                key={index}
                className="bg-gray-800/50 rounded-lg p-6 backdrop-blur-sm border border-gray-700/50 hover:border-blue-500/50 transition-all duration-300 hover:transform hover:scale-105"
              >
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-semibold text-white">
                    {project.title}
                  </h3>
                  <span
                    className={`px-2 py-1 rounded-full text-xs ${
                      project.status === "Production" ||
                      project.status === "Live"
                        ? "bg-green-600/20 text-green-300 border border-green-500/30"
                        : project.status === "Open Source"
                        ? "bg-purple-600/20 text-purple-300 border border-purple-500/30"
                        : project.status === "Template" ||
                          project.status === "Package"
                        ? "bg-orange-600/20 text-orange-300 border border-orange-500/30"
                        : "bg-blue-600/20 text-blue-300 border border-blue-500/30"
                    }`}
                  >
                    {project.status}
                  </span>
                </div>
                <p className="text-gray-300 mb-4 leading-relaxed text-sm">
                  {project.description}
                </p>
                <div className="flex flex-wrap gap-2 mb-3">
                  {project.tech.map((tech, techIndex) => (
                    <span
                      key={techIndex}
                      className="px-2 py-1 bg-gray-700/50 rounded text-xs text-gray-300"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
                {project.link && (
                  <a
                    href={project.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-blue-400 hover:text-blue-300 transition-colors text-sm"
                  >
                    View Live Demo →
                  </a>
                )}
              </div>
            ))}
          </div>
        </section>
        {/* Experience Highlights */}
        <section className="mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Development Highlights
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-gray-800/50 rounded-lg p-8 backdrop-blur-sm border border-gray-700/50">
              <h3 className="text-2xl font-semibold text-blue-400 mb-4">
                Academic Excellence
              </h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>
                    Developed 15+ comprehensive academic projects including AI
                    chatbots, face recognition systems, and e-commerce platforms
                  </span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>
                    Expertise in computer systems architecture, data structures
                    & algorithms, and system design
                  </span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>
                    Multiple programming languages: Assembly, Java, C#, PHP,
                    Python, HTML/CSS/JS
                  </span>
                </li>
              </ul>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-8 backdrop-blur-sm border border-gray-700/50">
              <h3 className="text-2xl font-semibold text-purple-400 mb-4">
                Open Source Contributions
              </h3>
              <ul className="space-y-3 text-gray-300">
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>
                    Created specialized FreeBSD build automation for popular
                    open-source projects
                  </span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>
                    Published reusable CI/CD templates and GitHub Actions
                    workflows
                  </span>
                </li>
                <li className="flex items-start">
                  <span className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>
                    Developed cross-platform utilities and starter kits for
                    rapid development
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </section>
        {/* Contact Section */}
        <section className="text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-8 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Let's Build Something Amazing
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Looking for a developer who can handle everything from frontend UX
            to backend architecture, DevOps automation, and system deployment?
            Let's discuss your next project.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a
              href="https://github.com/LoveDoLove"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-gray-800/50 hover:bg-gray-700/50 px-6 py-3 rounded-lg transition-all duration-300 text-gray-300 hover:text-white border border-gray-700/50 hover:border-blue-500/50"
            >
              GitHub Portfolio
            </a>
            <a
              href="https://github.com/LoveDoLove-School-Projects"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-purple-600/20 hover:bg-purple-600/30 px-6 py-3 rounded-lg transition-all duration-300 text-purple-300 hover:text-purple-200 border border-purple-500/30 hover:border-purple-400/50"
            >
              Academic Projects
            </a>
            <a
              href="mailto:contact@lovedolove.dev"
              className="bg-blue-600/20 hover:bg-blue-600/30 px-6 py-3 rounded-lg transition-all duration-300 text-blue-300 hover:text-blue-200 border border-blue-500/30 hover:border-blue-400/50"
            >
              Get in Touch
            </a>
          </div>
        </section>
      </div>
    </main>
  );
}

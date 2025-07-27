## LeoHire & LeoTalent – SaaS Platform for Smarter Hiring & Job Discovery

### 🧩 Project Overview
**LeoHire** is a SaaS-based recruitment platform designed to streamline and simplify the end-to-end hiring process for organizations. I had the opportunity to contribute to this project, which is currently under active development. The primary goal of LeoHire is to eliminate manual bottlenecks in hiring by allowing recruiters and admins to manage job roles, candidate progress, assessments, and onboarding seamlessly.

In parallel, we are also building **LeoTalent**, a candidate-facing module that intelligently recommends suitable jobs based on individual profiles, skills, and experience — turning hiring into a two-sided intelligent matchmaking process.

---

### 🎯 LeoHire – Features & Functionality
- 🏢 **Multi-Domain Job Creation**: Admins can define multiple domains (e.g., tech, HR, marketing) and create job listings under each.
- 🧪 **Dynamic Assessment Stages**: Recruiters can create customized assessments and evaluation flows for various roles.
- 🔁 **Stage Management**: Recruiters can move candidates from one hiring stage to another (e.g., Applied → Quiz → Interview → Offer → Pre-boarding).
- 🤝 **Collaborators & Feedback**: Collaborators (interviewers or hiring managers) can be assigned to stages, leave feedback on candidate performance, and manage interview outcomes.
- 📊 **Evaluator Integration**: Assessments are scored and evaluated automatically or by designated evaluators.

---

### 👤 LeoTalent – Candidate Module
- 📋 **Profile-Based Job Matching**: Candidates fill out a detailed profile including skills, experience, and preferences.
- 🎯 **Smart Job Recommendations**: The platform suggests hundreds of relevant job listings tailored to the user's background.
- 🛠️ **Module in Progress**: This module is currently under development and is being closely aligned with the recruiter-side functionality.

---

### 🧠 Technical Architecture
LeoHire and LeoTalent are designed using a **microservices architecture**, making the system scalable and modular. Each service runs independently and communicates efficiently via gRPC.

#### 🧱 Backend Microservices:
- **Job Service**: Manages job creation, editing, and domain segmentation
- **Library Service**: Hosts assessment templates and question banks
- **Application Service**: Tracks candidate progress and metadata
- **Assessment Service**: Evaluates quiz and test submissions
- **Preboarding Service**: Handles final steps before onboarding

#### 🧰 Tech Stack:
- **PostgreSQL**: Used across services to maintain relational integrity and structured data storage
- **gRPC**: Enables efficient communication between microservices
- **FastAPI (REST API)**: Serves as the API gateway from frontend to backend microservices

---

### ✅ Summary
LeoHire (and the upcoming LeoTalent) represents a modern approach to intelligent hiring and talent discovery. By merging granular recruiter control with scalable microservices, it ensures seamless coordination between stages, teams, and applicants. It’s a system built for efficiency — both for organizations seeking talent and individuals seeking opportunity.
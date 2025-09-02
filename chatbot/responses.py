HELP_OVERVIEW = (
    "👋 Welcome to EduSync Chatbot!\n\n"
    "Here’s what I can help you with:\n\n"
    "- Account access: login, signup, email verification, reset password\n"
    "- Course creation: create course, module, lesson, quiz, add question\n"
    "- Taking quizzes and earning certificates\n"
    "- Browsing and enrolling in courses\n"
    "- Privacy, data, and terms of service\n"
    "- Contacting support\n\n"
    "If you're not sure where to start, try typing 'help' to see what I can do!"
)

RESPONSES = {
    # Greetings
    "hello": "👋 Hi there! How can I help you today?",
    "hi": "Hello! Ready to learn something new? 😊",
    "bye": "Goodbye! Have a wonderful day 🎉",

    # Help overview
    "help": (
        "I can guide you with things like:\n\n"
        "📌 'Account' → login, signup, verification, reset password\n"
        "📌 'Courses' → create course, add modules/lessons/quizzes\n"
        "📌 'Learning' → take quizzes, earn certificates\n"
        "📌 'Info' → privacy, terms, support\n\n"
        "Just type what you're curious about, and I’ll help!"
    ),

    # Login & signup
    "login": (
        "To log in, click the 'Login' button at the top right and enter your email + password. "
        "If you don’t have an account yet, sign up first. 👍"
    ),
    "signup": (
        "To sign up, click 'Login' (top right), then choose 'Create an account'. "
        "You'll get a verification email to confirm your account."
    ),
    "email verification": (
        "After signing up, we’ll send a verification link to your email (valid for 10 minutes). "
        "If it expires, just log in again to automatically receive a new one."
    ),
    "login failed": (
        "😕 Having trouble logging in? Double-check your email and password. "
        "If your account isn’t verified, logging in will resend the verification email. "
        "Still stuck? Contact support at 'kmh61030@gmail.com'."
    ),
    "reset password": (
        "Forgot your password? No worries! Email 'kmh61030@gmail.com', "
        "and our admin will help you reset it."
    ),

    # Courses
    "create course": (
        "To create a course, head to your 'Dashboard' and click 'Create New Course'. 🚀"
    ),
    "add module": (
        "Modules organize your course. From your dashboard, select a course and click 'Add Module'."
    ),
    "add lesson": (
        "Lessons go inside modules. Open your course → pick a module → click 'Add Lesson'."
    ),
    "add quiz": (
        "To add a quiz, open your course → go to the module/lesson → click 'Add Quiz'."
    ),
    "add question": (
        "When you create a quiz, you'll be prompted to add questions. "
        "To add more later, go to 'View Quiz' → 'Add Question'."
    ),

    # Certificates
    "certificate": (
        "🏅 To earn a certificate: complete all lessons and mark them as finished. "
        "Once done, your certificate will be available for download at the bottom of the course page."
    ),

    # Info & support
    "privacy": "🔒 We value your privacy. Check the 'Privacy Policy' link in the footer.",
    "terms": "📜 You can review our 'Terms of Service' anytime from the footer.",
    "support": "💌 Need help? Email us at 'kmh61030@gmail.com', and we’ll assist you.",
}

DEFAULT_RESPONSE = (
    "🤔 Sorry, I’m not sure about that. Try typing 'help' to see what I can do!"
)

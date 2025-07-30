RESPONSES = {
    # Greetings & general
    "hello": "Hi there! How can I assist you today?",
    "hi": "Hello! How can I help you?",
    "help": (
        "I'm here to assist you! You can ask about any of the following topics:\n\n"
        "- Account access: login, signup, email verification, reset password\n"
        "- Course creation: create course, module, lesson, quiz, add question\n"
        "- Taking quizzes and earning certificates\n"
        "- Browsing and enrolling in courses\n"
        "- Privacy, data, and terms of service\n"
        "- Contacting support\n\n"
        "Try asking things like:\n"
        "• How do I create a course?\n"
        "• What happens if my verification link expires?\n"
        "• How do I earn a certificate?\n"
        "• Where can I find the Privacy Policy?\n\n"
        "If you're not sure where to start, just type something you're curious about!"
    ),
    "bye": "Goodbye! Have a great day!",

    # Platform access
    "login": "To log in, click the 'Login' button at the top right and enter your email and password.",
    "sign up": "To create a new account, click the 'Login' button, then select 'Create an account' to register.",
    "signup": "To create a new account, click the 'Login' button, then select 'Create an account' to register.",
    "email verification": (
        "Once you sign up, a verification link will be sent to your email. "
        "It is valid for 10 minutes. If it expires, simply log in with your credentials again, and a new link will be sent."
    ),
    "verification expired": (
        "Your verification link may have expired. Please log in with your credentials to receive a new one."
    ),
     # Login failure responses
    "login failed": (
        "Unable to log in. Please ensure your credentials are correct. "
        "If your account is unverified, logging in will automatically resend a new verification email."
    ),
    "can't login": (
        "Unable to log in. Please ensure your credentials are correct. "
        "If your account is unverified, logging in will automatically resend a new verification email."
    ),
    "cant login": (
        "Unable to log in. Please ensure your credentials are correct. "
        "If your account is unverified, logging in will automatically resend a new verification email."
    ),
    "cannot login": (
        "Unable to log in. Please ensure your credentials are correct. "
        "If your account is unverified, logging in will automatically resend a new verification email."
    ),
    "couldn't login": (
        "Unable to log in. Please ensure your credentials are correct. "
        "If your account is unverified, logging in will automatically resend a new verification email."
    ),
    "couldnt login": (
        "Unable to log in. Please ensure your credentials are correct. "
        "If your account is unverified, logging in will automatically resend a new verification email."
    ),

    # Signup failure responses
    "signup failed": (
        "We're sorry, we couldn't create your account. Please try again with valid and unique information."
        "If your account is unverified, you will not be able to login until you verify your email."
    ),
    "can't sign up": (
        "We're sorry, we couldn't create your account. Please try again with valid and unique information."
        "If your account is unverified, you will not be able to login until you verify your email."
    ),
     "cant sign up": (
        "We're sorry, we couldn't create your account. Please try again with valid and unique information."
        "If your account is unverified, you will not be able to login until you verify your email."
    ),
    "cannot sign up": (
        "We're sorry, we couldn't create your account. Please try again with valid and unique information."
        "If your account is unverified, you will not be able to login until you verify your email."
    ),
    "couldn't sign up": (
        "We're sorry, we couldn't create your account. Please try again with valid and unique information."
        "If your account is unverified, you will not be able to login until you verify your email."
    ),
    "couldnt sign up": (
        "We're sorry, we couldn't create your account. Please try again with valid and unique information."
        "If your account is unverified, you will not be able to login until you verify your email."
    ),
    "reset password": (
        "If you've forgotten your password or can't access your account, please contact the admin at "
        "kmh61030@gmail.com for assistance with resetting it."
    ),

    # Course creation flow
    "create course": "To create a course, go to your dashboard and click the 'Create New Course' button.",
    "create a course": "To create a course, go to your dashboard and click the 'Create New Course' button.",
    "create courses": "To create a course, go to your dashboard and click the 'Create New Course' button.",

    "create module": "To add a module, go to your dashboard, select the course you want to update, and click 'Add Module'.",
    "add module": "To add a module, go to your dashboard, select the course you want to update, and click 'Add Module'.",

    "create lesson": "To create a lesson, open your course, find the appropriate module, and click 'Add Lesson'.",
    "add lesson": "To create a lesson, open your course, find the appropriate module, and click 'Add Lesson'.",

    "create quiz": "To create a quiz, open your course, go to the relevant module and lesson, and click 'Add Quiz'.",
    "add quiz": "To create a quiz, open your course, go to the relevant module and lesson, and click 'Add Quiz'.",

    "add question": (
        "After creating a quiz, you'll be redirected to add questions. "
        "To add more questions later, go to 'View Quiz' and click 'Add Question'."
    ),
    "create question": (
        "After creating a quiz, you'll be redirected to add questions. "
        "To add more questions later, go to 'View Quiz' and click 'Add Question'."
    ),

    "take quiz": "To take a quiz, open the lesson and scroll to the bottom where the quiz section appears.",

    # Course & certificate info
    "course": "You can browse available courses from the Browse section on your dashboard.",
    "courses": "You can browse available courses from the Browse section on your dashboard.",
    "browse": "You can browse available courses from the Browse section on your dashboard.",

    "certificate": (
        "To earn a certificate, you must complete all lessons and manually mark all lessons as completed. "
        "Once everything is completed, your certificate will be available for download at the bottom of the course page."
    ),
    "cert": (
        "To earn a certificate, you must complete all lessons and manually mark all lessons as completed. "
        "Once everything is completed, your certificate will be available for download at the bottom of the course page."
    ),
    "certification": (
        "To earn a certificate, you must complete all lessons and manually mark all lessons as completed."
        "Once everything is completed, your certificate will be available for download at the bottom of the course page."
    ),

    # Privacy, terms, and data
    "privacy": "We value your privacy. You can view our full Privacy Policy from the footer.",
    "data": "We collect only necessary data to enhance your experience and issue certificates securely.",
    "security": "We use encryption and secure storage to protect your data.",
    "cookies": "We use cookies to improve your experience and analyze platform usage patterns.",
    "terms": "You can review our Terms of Service at any time using the link in the footer.",
    "prohibited": "Please refrain from any illegal or disruptive behavior while using the platform.",
    "termination": "Accounts that violate our terms may be suspended or terminated.",
    "modifications": "We may update our terms periodically. Continued use means you agree to the latest version.",

    # Account & eligibility
    "account": "Ensure your account details are accurate and secure. Do not share your login credentials.",
    "eligibility": "You must be at least 13 years old to use our platform.",

    # FAQ-style responses
    "what can i do": "You can create and take interactive courses with lessons, quizzes, and certificates.",
    "free": "Yes, EduSync is completely free to use. Just sign up and start learning or creating.",
    "cost": "Yes, EduSync is completely free to use. Just sign up and start learning or creating.",

    # Contact & support
    "contact": "For support, please email us at kmh61030@gmail.com.",
    "support": "For support, please email us at kmh61030@gmail.com.",
}

DEFAULT_RESPONSE = (
    "I'm sorry, I didn't understand that. Try asking about 'course', 'certificate', 'help', or 'privacy'."
)

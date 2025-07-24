import requests
from django.conf import settings 

VT_API_KEY = settings.VT_API_KEY

def scan_url_with_virustotal(url):
    headers = {"x-apikey": VT_API_KEY}
    scan_url = "https://www.virustotal.com/api/v3/urls"

    try:
        response = requests.post(scan_url, headers=headers, data={"url": url})
        response.raise_for_status()
        data = response.json()

        if 'data' in data:
            analysis_id = data['data']['id']
            report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

            report = requests.get(report_url, headers=headers)
            report.raise_for_status()
            report_data = report.json()

            vt_status = report_data['data']['attributes']['status']

            if vt_status in ["queued", "in-progress"]:
                return "pending"

            if vt_status == "completed":
                stats = report_data['data']['attributes']['stats']
                if stats['malicious'] == 0 and stats['suspicious'] == 0:
                    return "clean"
                else:
                    return "malicious"

        return "error"

    except Exception:
        return "error"

def scan_file_with_virustotal(file_path):
    headers = {"x-apikey": VT_API_KEY}
    scan_url = "https://www.virustotal.com/api/v3/files"

    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path, f)}
            response = requests.post(scan_url, headers=headers, files=files)
            response.raise_for_status()
            data = response.json()

        if 'data' in data:
            analysis_id = data['data']['id']
            report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

            report = requests.get(report_url, headers=headers)
            report.raise_for_status()
            report_data = report.json()

            vt_status = report_data['data']['attributes']['status']

            if vt_status in ["queued", "in-progress"]:
                return "pending"

            if vt_status == "completed":
                stats = report_data['data']['attributes']['stats']
                if stats['malicious'] == 0 and stats['suspicious'] == 0:
                    return "clean"
                else:
                    return "malicious"

        return "error"

    except Exception:
        return "error"


def is_course_completed(user, course):
    total_lessons = sum(module.lessons.count() for module in course.modules.all())
    completed_lessons = user.lessonprogress_set.filter(
        lesson__module__course=course,
        completed=True
    ).count()

    total_quizzes = sum(1 for module in course.modules.all() for lesson in module.lessons.all() if lesson.quiz)
    passed_quizzes = sum(
        1 for module in course.modules.all() for lesson in module.lessons.all()
        if lesson.quiz and lesson.quiz.quizattempt_set.filter(user=user, score__gte=5).exists()
    )

    return (total_lessons == completed_lessons) and (total_quizzes == passed_quizzes)
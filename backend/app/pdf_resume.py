from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

OUTPUT_FOLDER = "generated_resumes"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def create_resume_pdf(data):
    filename = f"{data['name'].replace(' ', '_')}_Resume.pdf"
    filepath = os.path.join(OUTPUT_FOLDER, filename)

    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>PROFESSIONAL RESUME</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Name:</b> {data['name']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Email:</b> {data['email']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Phone:</b> {data['phone']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Location:</b> {data['location']}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Summary</b>", styles["Heading2"]))
    story.append(Paragraph(data["summary"], styles["BodyText"]))

    story.append(Paragraph("<br/><b>Skills</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(data["skills"]), styles["BodyText"]))

    story.append(Paragraph("<br/><b>Experience</b>", styles["Heading2"]))
    story.append(Paragraph(data["experience"], styles["BodyText"]))

    story.append(Paragraph("<br/><b>Projects</b>", styles["Heading2"]))
    story.append(Paragraph(data["projects"], styles["BodyText"]))

    story.append(Paragraph("<br/><b>Education</b>", styles["Heading2"]))
    story.append(Paragraph(data["education"], styles["BodyText"]))

    doc.build(story)

    return filepath
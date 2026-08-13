import re


async def extract_document(text, document_type):

    try:

        if document_type == "invoice":

            vendor_name = None
            invoice_number = None
            total_amount = None
            date = None

            lines = text.splitlines()

            if lines:
                vendor_name = lines[0].strip()

            invoice_match = re.search(
                r"Invoice Number[:\s]+([A-Z0-9-]+)",
                text,
                re.IGNORECASE
            )

            if invoice_match:
                invoice_number = invoice_match.group(1)

            total_match = re.search(
                r"Total Amount[:\s]+([0-9]+(?:\.[0-9]+)?)",
                text,
                re.IGNORECASE
            )

            if total_match:
                total_amount = total_match.group(1)

            date_match = re.search(
                r"Date[:\s]+([A-Za-z0-9 ,/-]+)",
                text,
                re.IGNORECASE
            )

            if date_match:
                date = date_match.group(1).strip()

            return {
                "vendor_name": {
                    "value": vendor_name,
                    "confidence": "high" if vendor_name else "low"
                },
                "invoice_number": {
                    "value": invoice_number,
                    "confidence": "high" if invoice_number else "low"
                },
                "total_amount": {
                    "value": total_amount,
                    "confidence": "high" if total_amount else "low"
                },
                "date": {
                    "value": date,
                    "confidence": "medium" if date else "low"
                }
            }

        elif document_type == "resume":

            # Email
            email_match = re.search(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
                text
            )

            email = email_match.group(0) if email_match else None

            # Phone number
            phone_match = re.search(
                r"(?:\+91[\s-]?)?[6-9]\d{9}\b",
                text
            )

            phone = phone_match.group(0) if phone_match else None

            # Name
            lines = [
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ]

            name = None

            if lines:
                for line in lines[:10]:

                    if (
                        len(line.split()) >= 2
                        and len(line) <= 60
                        and not any(char.isdigit() for char in line)
                        and "@" not in line
                    ):
                        name = line
                        break

            # Common technical skills
            skill_list = [
                "Python",
                "C",
                "C++",
                "Java",
                "JavaScript",
                "HTML",
                "CSS",
                "React",
                "Node.js",
                "Express",
                "FastAPI",
                "Django",
                "Flask",
                "SQL",
                "MongoDB",
                "MySQL",
                "PostgreSQL",
                "Git",
                "GitHub",
                "Docker",
                "AWS",
                "Machine Learning",
                "Deep Learning",
                "NLP",
                "AI"
            ]

            detected_skills = []

            text_lower = text.lower()

            for skill in skill_list:
                if skill.lower() in text_lower:
                    detected_skills.append(skill)

            return {
                "name": {
                    "value": name,
                    "confidence": "high" if name else "low"
                },

                "email": {
                    "value": email,
                    "confidence": "high" if email else "low"
                },

                "phone": {
                    "value": phone,
                    "confidence": "high" if phone else "low"
                },

                "skills": {
                    "value": detected_skills,
                    "confidence": "medium" if detected_skills else "low"
                }
            }

        else:

            return {
                "error": "Unsupported document type"
            }

    except Exception as e:

        return {
            "error": str(e)
        }

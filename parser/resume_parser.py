import spacy
import re

class ResumeParser:
    def __init__(self, resume_text):
        self.nlp = spacy.load('en_core_web_sm')
        self.raw_text = resume_text
        self.cleaned_text = re.sub(r'\s+', ' ', resume_text)
        self.doc = self.nlp(self.cleaned_text)
        
        # --- Run all extraction methods ---
        self.email = self._extract_email()
        self.name = self._extract_name()
        self.experience = self._extract_experience()
        self.education = self._extract_education()

    def _extract_email(self):
        """A highly robust, two-step regex to find emails, even with typos."""
        # --- Strategy 1: The standard, clean regex for correctly formatted emails ---
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_regex, self.raw_text)
        if match:
            return match.group(0)

        # --- Strategy 2: Super-forgiving fallback for malformed emails ---
        forgiving_regex = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+)'
        matches = re.findall(forgiving_regex, self.raw_text)
        for potential_match in matches:
            if 'gmail' in potential_match or 'outlook' in potential_match or 'yahoo' in potential_match:
                return potential_match
        return "Email Not Found"

    def _extract_name(self):
        """Our proven, multi-tiered strategy for name extraction."""
        doc_start = self.nlp(self.cleaned_text[:300])
        person_ents = [ent.text.strip() for ent in doc_start.ents if ent.label_ == 'PERSON']
        for name in person_ents:
            if 2 <= len(name.split()) <= 4 and len(name) < 35:
                return name.title()

        if self.email and self.email != "Email Not Found":
            name_from_email = self.email.split('@')[0]
            name_from_email = re.sub(r'[\._0-9]+', ' ', name_from_email).strip()
            name_parts = name_from_email.split()
            if len(name_parts) >= 2 and all(part.lower() in self.raw_text[:150].lower() for part in name_parts):
                return name_from_email.title()

        for line in self.raw_text.split('\n')[:5]:
            line = line.strip()
            if re.match(r'^([A-Z][a-z]+(?: [A-Z]\.)? [A-Z][a-z]+)$', line) and len(line) < 35:
                return line.title()
        
        for line in self.raw_text.split('\n')[:5]:
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line.split()) <= 4 and len(line) < 35:
                if not any(kw in line.lower() for kw in ['email', 'phone', 'linkedin', 'github', 'resume']):
                    return line.title()

        return "Name Not Found"

    def _extract_section(self, section_keywords):
        """A helper function to find the text under a specific section header."""
        text = self.raw_text.split('\n')
        section_text = ""
        found_section = False
        for line in text:
            # Check if the line is a section header
            if any(re.match(r'^\s*' + keyword + r'\s*$', line, re.IGNORECASE) for keyword in section_keywords):
                found_section = True
                continue
            
            # If we've found the section, start capturing text
            if found_section:
                # Stop if we hit another major section header
                if any(re.match(r'^\s*' + kw + r'\s*$', line, re.IGNORECASE) for kw in ['skills', 'education', 'experience', 'projects', 'awards']):
                    # But don't stop if the line itself is part of the current section
                    if not any(re.match(r'^\s*' + current_kw + r'\s*$', line, re.IGNORECASE) for current_kw in section_keywords):
                        break
                section_text += line + '\n'
        return section_text

    def _extract_experience(self):
        """Extracts work experience by finding the relevant section and parsing it."""
        experience_text = self._extract_section(['professional experience', 'experience', 'work history'])
        if not experience_text:
            return []
        
        experience_list = []
        # A basic pattern to find job titles and companies. This can be improved.
        # Example: "Gen Al Intern" followed by "Tata Motors Limited"
        for match in re.finditer(r'([A-Z][a-z\s\(\)]+)\n(.*(?:Limited|Technologies|Solutions))', experience_text, re.IGNORECASE):
            title = match.group(1).strip()
            company = match.group(2).strip()
            experience_list.append({'title': title, 'company': company})
        return experience_list


    def _extract_education(self):
        """Extracts education by finding the relevant section and parsing it."""
        education_text = self._extract_section(['education', 'academic background'])
        if not education_text:
            return []
            
        education_list = []
        # A pattern to find University or Institute names
        for match in re.finditer(r'([A-Z][a-z\s]+(?:University|Institute|College))', education_text, re.IGNORECASE):
            university = match.group(1).strip()
            # This is a placeholder for degree parsing
            education_list.append({'degree': 'Degree Not Parsed', 'university': university})
        return education_list

    def get_details(self):
        """Returns all extracted details as a dictionary."""
        return {
            'name': self.name,
            'email': self.email,
            'resume_text': self.cleaned_text,
            'experience': self.experience,
            'education': self.education
        }